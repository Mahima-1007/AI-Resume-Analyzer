from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from database import resumes_col, applications_col, jobs_col, db
from routes.auth import get_current_user
from fastapi.responses import Response
from datetime import datetime
from pydantic import BaseModel

class JobSearchRequest(BaseModel):
    role: str

import json, os

router = APIRouter()

# --------------- RESUME ANALYZE ---------------
@router.post("/analyze")
async def analyze_resume(
    file: UploadFile = File(None),
    jd_text: str = Form(...),
    current_user: dict = Depends(get_current_user)
):
    try:
        from modules.resume_parser import extract_text_from_pdf, extract_text_from_docx
        from modules.ats_analyzer import calculate_ats_score
    except ImportError as e:
        raise HTTPException(status_code=500, detail=f"AI module not available: {e}")

    if not file:
        raise HTTPException(status_code=400, detail="Resume file is required")

    contents = await file.read()
    try:
        if file.filename.endswith(".pdf"):
            resume_text = extract_text_from_pdf(contents)
        elif file.filename.endswith(".docx"):
            resume_text = extract_text_from_docx(contents)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format. Use PDF or DOCX.")
    except Exception as e:
        import traceback
        print("EXTRACTION ERROR:")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Extraction error: {e}")

    try:
        analysis_results = calculate_ats_score(resume_text, jd_text)
    except Exception as e:
        import traceback
        print("ATS SCORING ERROR:")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Analysis error: {e}")

    try:
        # 1. INSERT resume text -> resumes collection
        resume_data = {
            "user_id": current_user["id"],
            "content_text": resume_text,
            "file_name": file.filename,
            "created_at": datetime.utcnow()
        }
        resume_doc = resumes_col.insert_one(resume_data)
        print(f"Resume saved to database with id: {resume_doc.inserted_id}")

        # 2. INSERT ATS results -> ats_results collection, linked via resume_id
        ats_result = {
            "user_id": current_user["id"],
            "resume_id": str(resume_doc.inserted_id),
            "ats_score": int(analysis_results["ats_score"]),
            "keyword_match": float(analysis_results.get("keyword_match", 0.0)),
            "semantic_similarity": float(analysis_results.get("semantic_similarity", 0.0)),
            "matched_skills": analysis_results.get("matched_skills", []),
            "missing_skills": analysis_results.get("missing_skills", []),
            "created_at": datetime.utcnow()
        }
        db.ats_results.insert_one(ats_result)
        print("ATS result saved to ats_results collection")
    except Exception as e:
        import traceback
        print("DATABASE ERROR (ATS Save):")
        traceback.print_exc()
        # Non-fatal to return results
        
    return analysis_results

# --------------- SMART RESUME REGENERATION ---------------
@router.post("/regenerate_resume")
def regenerate_resume(
    payload: dict,
    current_user: dict = Depends(get_current_user)
):
    """
    Mocks an AI rewriting a resume based on ATS analysis suggestions.
    In a real app, this would use an LLM API (OpenAI/Gemini).
    """
    missing_skills = payload.get("missing_skills", [])
    
    # Mocking improved data
    improved_resume = {
        "name": "Jane / John Doe (Improved)",
        "email": "improved@example.com",
        "phone": "+1 234 567 8900",
        "summary": "Highly motivated and results-driven professional with a proven track record. " +
                   f"Expertise in {', '.join(missing_skills[:3]) if missing_skills else 'industry best practices'}. " +
                   "Demonstrated ability to increase efficiency by 40%.",
        "education": [{"institution": "Tech University", "degree": "B.S. Computer Science", "year": "2022"}],
        "skills": ["Python", "Docker", "REST API", "CI/CD", "Agile"] + missing_skills,
        "experience": [{
            "company": "Tech Innovators Inc.",
            "role": "Senior Developer",
            "duration": "2020 - Present",
            "description": "• Spearheaded the development of a microservices architecture.\n" +
                           "• Increased system throughput by 35%.\n" +
                           f"• Utilized {missing_skills[0] if missing_skills else 'advanced tools'} to solve critical workflow bottlenecks."
        }],
        "projects": [{
            "title": "Automated Deployment Pipeline",
            "description": "Designed and implemented a fully automated deployment pipeline reducing release time by 50%.",
            "technologies": "GitHub Actions, Docker, AWS"
        }]
    }
    
    return {"message": "Resume successfully optimized by AI.", "improved_data": improved_resume}

# --------------- FETCH LATEST RESUME WITH ATS (AGGREGATION) ---------------
@router.get("/resumes/latest")
async def get_latest_resume(current_user: dict = Depends(get_current_user)):
    """
    Fetches the user's latest uploaded resume and JOINS it with its ATS results 
    from the ats_results collection using MongoDB $lookup.
    """
    pipeline = [
        # 1. Match only the current user's resumes
        {"$match": {"user_id": current_user["id"]}},
        
        # 2. Sort to get the most recent one first
        {"$sort": {"created_at": -1}},
        
        # 3. Limit to the 1 most recent resume
        {"$limit": 1},
        
        # 4. JOIN with the ats_results collection
        {
            "$lookup": {
                "from": "ats_results",            # Collection to join
                "let": {"resume_id_str": {"$toString": "$_id"}}, # Convert ObjectId to string
                "pipeline": [
                    # Match ats_results where resume_id string matches our local resume context
                    {"$match": {"$expr": {"$eq": ["$resume_id", "$$resume_id_str"]}}}
                ],
                "as": "ats_data"                  # Output array field name
            }
        },
        
        # 5. Extract the single ATS result object from the array (if it exists)
        {
            "$addFields": {
                "ats_result": {"$arrayElemAt": ["$ats_data", 0]}
            }
        },
        
        # 6. Clean up the output by removing the array
        {"$project": {"ats_data": 0}}
    ]

    result = list(resumes_col.aggregate(pipeline))
    
    if not result:
        return {"success": False, "message": "No resume found"}
        
    latest = result[0]
    
    # Fix ObjectId serialization for JSON
    latest["_id"] = str(latest["_id"])
    if "ats_result" in latest and latest["ats_result"]:
        latest["ats_result"]["_id"] = str(latest["ats_result"]["_id"])
        
    return {"success": True, "resume": latest}

# --------------- HTML LIVE PREVIEW ---------------
@router.post("/preview_html")
def preview_html(
    resume_data: dict,
    current_user: dict = Depends(get_current_user)
):
    """
    Returns the raw HTML string for the live preview matching the chosen template.
    """
    try:
        from modules.resume_generator import generate_resume_html
        template_id = resume_data.pop("template_id", "modern")
        html_str = generate_resume_html(resume_data, template_id)
        return {"html_content": html_str}
    except ImportError as e:
        raise HTTPException(status_code=500, detail=f"HTML module not available: {e}")

# --------------- RESUME GENERATE ---------------
@router.post("/generate")
def generate_resume(
    resume_data: dict,
    current_user: dict = Depends(get_current_user)
):
    try:
        from modules.resume_generator import create_resume_file
        template_id = resume_data.pop("template_id", "modern")
        pdf_bytes = create_resume_file(resume_data, template_id)
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=resume.pdf"}
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"PDF Generation failed: {e}")

# --------------- ROLE-BASED JOB SEARCH ---------------
@router.post("/jobs/search")
async def search_jobs_by_role(
    body: JobSearchRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Accept a job role string, call open APIs (Arbeitnow + Remotive),
    rank by relevance, save to MongoDB, return top results.
    Example: POST /api/jobs/search  {"role": "java developer"}
    """
    from modules.job_api_service import fetch_jobs_for_role

    role = body.role.strip()
    if not role:
        raise HTTPException(status_code=400, detail="Job role cannot be empty.")

    display_title = role.title()
    print(f"Job search role: '{display_title}'")

    try:
        # --- Step 1: Fetch from open APIs ---
        try:
            jobs = await fetch_jobs_for_role(role, top_k=15)
            print(f"Jobs scraped: {len(jobs)}")
        except Exception as e:
            print(f"API fetch error: {e}")
            jobs = []

        # --- Step 2: Deduplicate + save to MongoDB ---
        saved_jobs = []
        seen_urls: set = set()
        for job in jobs:
            url = job.get("applyUrl", "")
            if not url or url in seen_urls:
                continue
            seen_urls.add(url)
            try:
                existing = jobs_col.find_one({"applyUrl": url})
                if not existing:
                    job["scraped_at"] = datetime.utcnow()
                    job["user_id"] = current_user["id"]
                    jobs_col.insert_one(job)
            except Exception as db_err:
                print(f"DB error (non-fatal): {db_err}")
            saved_jobs.append(job)

        print(f"Returning {len(saved_jobs)} jobs for: {display_title}")
        return {"success": True, "role": display_title, "jobs": saved_jobs, "count": len(saved_jobs)}

    except Exception as outer_err:
        import traceback
        traceback.print_exc()
        print(f"Outer error in /jobs/search: {outer_err}")
        return {"success": False, "role": display_title, "jobs": [], "count": 0,
                "error": str(outer_err)}




# --------------- DYNAMIC JOB RECOMMENDATIONS ---------------
@router.post("/recommendations/analyze")
async def analyze_and_recommend_jobs(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    try:
        from modules.resume_parser import extract_text_from_pdf, extract_text_from_docx, extract_keywords
        from modules.job_recommender import recommend_scraped_jobs

        print(f"Received file: {file.filename}")
        contents = await file.read()
        if file.filename.endswith(".pdf"):
            print("Parsing PDF...")
            resume_text = extract_text_from_pdf(contents)
        elif file.filename.endswith(".docx"):
            print("Parsing DOCX...")
            resume_text = extract_text_from_docx(contents)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format.")
            
        print(f"Extracted resume text length: {len(resume_text)}")
        try:
            resumes_col.insert_one({
                "user_id": current_user["id"],
                "content_text": resume_text,
                "created_at": datetime.utcnow()
            })
        except Exception as e:
            print(f"DB Error: {e}")
            pass

        skills = extract_keywords(resume_text)
        print(f"Extracted skills: {skills}")
        print(f"Extracted skills count: {len(skills)}")
        
        scraped_jobs = []
        try:
            from modules.job_scraper import scrape_jobs
            scraped_jobs = await scrape_jobs(skills)
            print(f"Scraped jobs count: {len(scraped_jobs)}")
            
            # --- Deduplicate and Save to DB ---
            unique_jobs = []
            seen_urls = set()
            for job in scraped_jobs:
                job_url = job.get("applyUrl", "")
                if job_url in seen_urls:
                    continue
                seen_urls.add(job_url)
                
                existing = jobs_col.find_one({"applyUrl": job_url})
                if not existing:
                    job["scraped_at"] = datetime.utcnow()
                    job["user_id"] = current_user["id"]
                    jobs_col.insert_one(job)
                    unique_jobs.append(job)
                else:
                    unique_jobs.append(existing)

            scraped_jobs = unique_jobs
            print(f"Unique jobs after deduplication: {len(scraped_jobs)}")

        except Exception as scrape_err:
            print(f"Scraper failed: {scrape_err}")
            
        recommended_jobs = recommend_scraped_jobs(resume_text, scraped_jobs, top_k=10)
        print(f"Matched jobs: {len(recommended_jobs)}")
        return {
            "success": True,
            "skills": skills[:10],
            "jobs": recommended_jobs,
            "count": len(recommended_jobs)
        }
    except Exception as e:
        import traceback
        print("ERROR IN ANALYZE_AND_RECOMMEND_JOBS:")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to analyze resume and fetch jobs: {str(e)}")

@router.get("/recommendations/refresh")
async def refresh_recommendations(current_user: dict = Depends(get_current_user)):
    from modules.resume_parser import extract_keywords
    from modules.job_recommender import recommend_scraped_jobs

    latest_resume = resumes_col.find_one(
        {"user_id": current_user["id"]},
        sort=[("created_at", -1)]
    )
    if not latest_resume:
        raise HTTPException(status_code=400, detail="No resume found to analyze. Please upload one first.")
        
    resume_text = latest_resume["content_text"]
    skills = extract_keywords(resume_text)
    
    scraped_jobs = []
    try:
        from modules.job_scraper import scrape_jobs
        raw_scraped_jobs = await scrape_jobs(skills)
        
        # --- Deduplicate and Save to DB ---
        unique_jobs = []
        seen_urls = set()
        for job in raw_scraped_jobs:
            job_url = job.get("applyUrl", "")
            if job_url in seen_urls:
                continue
            seen_urls.add(job_url)
            
            existing = jobs_col.find_one({"applyUrl": job_url})
            if not existing:
                job["scraped_at"] = datetime.utcnow()
                job["user_id"] = current_user["id"]
                jobs_col.insert_one(job)
                unique_jobs.append(job)
            else:
                unique_jobs.append(existing)
                
        scraped_jobs = unique_jobs
    except Exception as e:
        print(f"Scraper error on refresh: {e}")
        
    recommended_jobs = recommend_scraped_jobs(resume_text, scraped_jobs, top_k=10)
    print(f"Matched jobs: {len(recommended_jobs)}")
    return {
        "success": True,
        "skills": skills[:10],
        "jobs": recommended_jobs,
        "count": len(recommended_jobs)
    }

# --------------- TEST AWARENESS (legacy) ---------------
@router.get("/test-awareness")
def test_awareness(company: str, role: str = "Software Engineer"):
    from modules.test_awareness import get_test_awareness
    return get_test_awareness(company, role)

# --------------- MOCK TEST — GENERATE ---------------
class MockTestRequest(BaseModel):
    role: str
    company: str
    count: int = 20

@router.post("/mock-test/generate")
def generate_mock_test(body: MockTestRequest, current_user: dict = Depends(get_current_user)):
    """Generate a set of questions for a mock test based on role and company."""
    from modules.test_awareness import get_mock_test
    questions = get_mock_test(body.role, body.company, body.count)
    return {
        "success": True,
        "role": body.role,
        "company": body.company,
        "total": len(questions),
        "questions": questions,
    }

# --------------- MOCK TEST — SUBMIT ---------------
class MockSubmitRequest(BaseModel):
    answers: dict  # { "q001": 2, "q003": 0, ... }

@router.post("/mock-test/submit")
def submit_mock_test(body: MockSubmitRequest, current_user: dict = Depends(get_current_user)):
    """Grade the user's mock test answers and return scored results."""
    from modules.test_awareness import grade_submission
    result = grade_submission(body.answers)
    return {"success": True, **result}

# --------------- MOCK APPLY ---------------
@router.post("/apply/{job_id}")
def apply_to_job(job_id: str, current_user: dict = Depends(get_current_user)):
    applications_col.insert_one({
        "user_id": current_user["id"],
        "job_id": job_id,
        "status": "Applied",
        "applied_at": datetime.utcnow()
    })
    return {"message": "Application submitted successfully", "status": "Applied"}

# --------------- MY APPLICATIONS ---------------
@router.get("/applications")
def get_applications(current_user: dict = Depends(get_current_user)):
    apps = list(applications_col.find({"user_id": current_user["id"]}))
    return [{"id": str(a["_id"]), "job_id": a["job_id"], "status": a["status"],
             "applied_at": str(a["applied_at"])} for a in apps]
