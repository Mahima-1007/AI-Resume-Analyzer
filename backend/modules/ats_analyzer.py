from sentence_transformers import SentenceTransformer, util
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from modules.resume_parser import extract_keywords

# Load Sentence Transformer model
model = SentenceTransformer("all-MiniLM-L6-v2")

import re

def calculate_ats_score(resume_text: str, jd_text: str) -> dict:
    """
    Calculates ATS score based on Keyword Overlap, TF-IDF, and Semantic Similarity.
    Also provides detailed strengths, weaknesses, and improvement suggestions.
    """
    resume_keywords = set(extract_keywords(resume_text.lower()))
    jd_keywords = set(extract_keywords(jd_text.lower()))
    
    # 1. Keyword Overlap
    if not jd_keywords:
        keyword_score = 1.0
        missing_skills = []
        matched_skills = list(resume_keywords)[:5]
    else:
        overlap = resume_keywords.intersection(jd_keywords)
        keyword_score = len(overlap) / len(jd_keywords)
        missing_skills = list(jd_keywords - resume_keywords)
        matched_skills = list(overlap)
        
    # 2. TF-IDF Similarity
    vectorizer = TfidfVectorizer(stop_words='english')
    try:
        tfidf_matrix = vectorizer.fit_transform([resume_text, jd_text])
        tfidf_score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    except ValueError:
        tfidf_score = 0.0
        
    # 3. Semantic Similarity
    try:
        embeddings = model.encode([resume_text, jd_text])
        semantic_score = util.cos_sim(embeddings[0], embeddings[1]).item()
    except Exception:
        semantic_score = 0.0
    
    # Final Weighted Score (0-100)
    final_score = ((keyword_score * 0.40) + (tfidf_score * 0.30) + (semantic_score * 0.30)) * 100
    
    # --- Advanced Analysis: Strengths, Weaknesses & Suggestions ---
    strengths = []
    weaknesses = []
    suggestions = []
    
    # Strength: Good keyword match
    if keyword_score > 0.6:
        strengths.append(f"Strong keyword alignment ({round(keyword_score*100)}% match)")
    elif keyword_score < 0.3:
        weaknesses.append(f"Weak keyword alignment ({round(keyword_score*100)}% match)")
        suggestions.append(f"Add missing keywords: {', '.join(missing_skills[:5])}")

    # Weakness: Missing metrics (numbers/percentages)
    num_metrics = len(re.findall(r'\b\d+(?:%|k|m|b)?\b', resume_text, re.IGNORECASE))
    if num_metrics > 5:
        strengths.append("Good use of quantifiable metrics and numbers")
    else:
        weaknesses.append("Lacks quantifiable achievements")
        suggestions.append("Add measurable achievements (numbers, percentages, results) to your experience section")

    # Weakness: Action Verbs check (Simple heuristic)
    action_verbs = ['developed', 'managed', 'led', 'created', 'designed', 'built', 'improved', 'increased', 'reduced', 'implemented']
    found_verbs = [v for v in action_verbs if v in resume_text.lower()]
    if len(found_verbs) >= 4:
        strengths.append("Strong use of action verbs")
    else:
        weaknesses.append("Weak action verbs")
        suggestions.append("Strengthen project descriptions using strong action verbs (e.g., Developed, Managed, Implemented)")

    if len(resume_text.split()) < 200:
        weaknesses.append("Resume is too short")
        suggestions.append("Expand on your experience and projects. A good resume has at least 300 words.")
        
    if not missing_skills and not weaknesses:
        suggestions.append("Your resume is well tailored for this job!")

    return {
        "ats_score": round(max(0, min(100, final_score)), 2),
        "keyword_match_percent": round(keyword_score * 100, 2),
        "semantic_similarity": round(semantic_score * 100, 2),
        "missing_skills": missing_skills[:10],
        "matched_skills": matched_skills[:10],
        "strengths": strengths,
        "weaknesses": weaknesses,
        "suggestions": suggestions
    }
