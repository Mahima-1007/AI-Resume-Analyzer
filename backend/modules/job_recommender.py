import json
import os
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")

def load_jobs() -> list[dict]:
    data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "jobs.json")
    if not os.path.exists(data_path):
        return []
    with open(data_path, "r", encoding="utf-8") as f:
        return json.load(f)

def recommend_jobs(resume_text: str, top_k: int = 5) -> list[dict]:
    """
    Recommend jobs from jobs.json based on semantic similarity to resume text.
    """
    jobs = load_jobs()
    if not jobs:
        return []
        
    resume_embedding = model.encode(resume_text)
    
    job_scores = []
    for job in jobs:
        job_description = f"{job['title']} {job['company']} {' '.join(job.get('skills', []))} {job.get('description', '')}"
        job_embedding = model.encode(job_description)
        score = util.cos_sim(resume_embedding, job_embedding).item()
        job_scores.append({
            "id": job["id"],
            "jobTitle": job["title"],
            "company": job["company"],
            "location": job.get("location", "Remote"),
            "skills": job.get("skills", []),
            "score": round(score * 100, 2),
            "applyUrl": job.get("link", ""),
            "jobDescription": job.get("description", ""),
            "source": "Mock Data"
        })
        
    # Sort by score descending
    job_scores.sort(key=lambda x: x["score"], reverse=True)
    return job_scores[:top_k]

MIN_MATCH_SCORE = 30  # Minimum score threshold

def recommend_scraped_jobs(resume_text: str, scraped_jobs: list[dict], top_k: int = 10) -> list[dict]:
    """
    Recommend jobs from dynamically scraped list based on semantic similarity to resume text.
    Always returns at least 5 jobs even if scores are low.
    """
    if not scraped_jobs:
        return []
        
    resume_embedding = model.encode(resume_text)
    
    job_scores = []
    for job in scraped_jobs:
        job_description = f"{job['jobTitle']} {job['company']} {' '.join(job.get('skills', []))} {job.get('jobDescription', '')}"
        job_embedding = model.encode(job_description)
        score = util.cos_sim(resume_embedding, job_embedding).item()
        score_pct = round(score * 100, 2)
        
        # Debug logging
        print(f"  Job: {job['jobTitle']} @ {job['company']} | Score: {score_pct}%")
        
        job_scores.append({
            "id": job.get("id", str(job.get("_id", ""))),
            "jobTitle": job["jobTitle"],
            "company": job["company"],
            "location": job.get("location", "Remote"),
            "skills": job.get("skills", []),
            "score": score_pct,
            "jobDescription": job.get("jobDescription", ""),
            "applyUrl": job.get("applyUrl", ""),
            "source": job.get("source", "Unknown")
        })
        
    # Sort by score descending
    job_scores.sort(key=lambda x: x["score"], reverse=True)
    
    # Filter by minimum score, but always keep at least 5 jobs
    matched = [j for j in job_scores if j["score"] >= MIN_MATCH_SCORE]
    if len(matched) < 5:
        matched = job_scores[:5]  # Guaranteed top 5 even at low scores
    
    return matched[:top_k]
