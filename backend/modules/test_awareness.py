import json
import os
import random
from typing import Optional

# ── Load question bank ────────────────────────────────────────────────────────
def _load_questions() -> list[dict]:
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "question_bank.json")
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# ── Role normalizer ───────────────────────────────────────────────────────────
ROLE_MAP = {
    "software developer":    "software_developer",
    "software engineer":     "software_developer",
    "backend developer":     "software_developer",
    "frontend developer":    "full_stack_developer",
    "full stack developer":  "full_stack_developer",
    "fullstack developer":   "full_stack_developer",
    "data analyst":          "data_analyst",
    "data scientist":        "data_analyst",
    "business analyst":      "data_analyst",
    "ai engineer":           "ai_ml_engineer",
    "ml engineer":           "ai_ml_engineer",
    "machine learning engineer": "ai_ml_engineer",
    "ai/ml engineer":        "ai_ml_engineer",
    "cybersecurity analyst": "cybersecurity_analyst",
    "security engineer":     "cybersecurity_analyst",
    "penetration tester":    "cybersecurity_analyst",
}

COMPANY_MAP = {
    "google":    "google",
    "amazon":    "amazon",
    "microsoft": "microsoft",
    "meta":      "meta",
    "facebook":  "meta",
    "tcs":       "tcs",
    "tata":      "tcs",
    "infosys":   "infosys",
    "wipro":     "general",
    "accenture": "general",
}

def _norm_role(role: str) -> str:
    return ROLE_MAP.get(role.strip().lower(), "software_developer")

def _norm_company(company: str) -> str:
    c = company.strip().lower()
    for key, val in COMPANY_MAP.items():
        if key in c:
            return val
    return "general"


# ── Question generation ───────────────────────────────────────────────────────

def get_mock_test(role: str, company: str, count: int = 20) -> list[dict]:
    """
    Returns a randomized set of `count` questions for the given role and company.
    
    Priority:
    1. Company-specific + role-specific questions
    2. Role-specific "general" company questions
    3. Any remaining general questions (to fill up to count)
    
    Returns questions WITHOUT the answer field (for test delivery).
    """
    all_qs = _load_questions()
    role_key    = _norm_role(role)
    company_key = _norm_company(company)

    # Tier 1: company-specific + role match
    tier1 = [q for q in all_qs if q["role"] == role_key and q["company"] == company_key]
    # Tier 2: general + role match
    tier2 = [q for q in all_qs if q["role"] == role_key and q["company"] == "general"]
    # Tier 3: any general question (different role for variety)
    tier3 = [q for q in all_qs if q["company"] == "general" and q["role"] != role_key]

    pool: list[dict] = []
    random.shuffle(tier1)
    random.shuffle(tier2)
    random.shuffle(tier3)

    # Try to fill from higher tiers first
    pool.extend(tier1)
    needed = count - len(pool)
    if needed > 0:
        pool.extend(tier2[:needed])
    needed = count - len(pool)
    if needed > 0:
        pool.extend(tier3[:needed])

    selected = pool[:count]
    random.shuffle(selected)

    # Strip the answer field — never send correct answer to frontend
    delivering = []
    for q in selected:
        delivering.append({
            "id":         q["id"],
            "type":       q["type"],
            "difficulty": q["difficulty"],
            "question":   q["question"],
            "options":    q["options"],
        })
    return delivering


def grade_submission(answers: dict) -> dict:
    """
    Score the user's answers.
    
    `answers`: {"q001": 2, "q003": 0, ...}  — question_id → chosen option index
    
    Returns:
        score, total, percentage, per_question detail with
        correctAnswer, userAnswer, explanation, isCorrect
    """
    all_qs = _load_questions()
    qs_by_id = {q["id"]: q for q in all_qs}

    results = []
    correct = 0

    for qid, user_ans in answers.items():
        q = qs_by_id.get(qid)
        if not q:
            continue
        is_correct = (user_ans == q["answer"])
        if is_correct:
            correct += 1
        results.append({
            "id":            qid,
            "question":      q["question"],
            "options":       q["options"],
            "type":          q["type"],
            "difficulty":    q["difficulty"],
            "userAnswer":    user_ans,
            "correctAnswer": q["answer"],
            "explanation":   q["explanation"],
            "isCorrect":     is_correct,
        })

    total      = len(answers)
    percentage = round((correct / total) * 100, 1) if total else 0

    # Difficulty breakdown
    easy   = [r for r in results if r["difficulty"] == "easy"]
    medium = [r for r in results if r["difficulty"] == "medium"]
    hard   = [r for r in results if r["difficulty"] == "hard"]

    # Skill suggestions based on wrong answers
    wrong_types = [r["type"] for r in results if not r["isCorrect"]]
    suggestions = _get_suggestions(wrong_types, percentage)

    return {
        "score":      correct,
        "total":      total,
        "percentage": percentage,
        "grade":      _grade(percentage),
        "breakdown": {
            "easy":   {"total": len(easy),   "correct": sum(1 for r in easy   if r["isCorrect"])},
            "medium": {"total": len(medium), "correct": sum(1 for r in medium if r["isCorrect"])},
            "hard":   {"total": len(hard),   "correct": sum(1 for r in hard   if r["isCorrect"])},
        },
        "suggestions": suggestions,
        "results":     results,
    }


def _grade(pct: float) -> str:
    if pct >= 90: return "Excellent"
    if pct >= 75: return "Good"
    if pct >= 60: return "Average"
    if pct >= 40: return "Below Average"
    return "Needs Improvement"


def _get_suggestions(wrong_types: list[str], pct: float) -> list[str]:
    tips = []
    if wrong_types.count("aptitude") >= 2:
        tips.append("Practice quantitative aptitude: ratios, percentages, time-work, and series problems.")
    if wrong_types.count("logical") >= 2:
        tips.append("Work on logical reasoning: syllogisms, pattern detection, and analogy questions.")
    if wrong_types.count("mcq") >= 3:
        tips.append("Revise core technical concepts for your role — focus on theory and fundamentals.")
    if wrong_types.count("behavioural") >= 1:
        tips.append("Practice STAR method answers for behavioural interview questions.")
    if pct < 60:
        tips.append("Consider building more projects related to your target role to strengthen hands-on knowledge.")
    if pct >= 75:
        tips.append("Good performance! Focus on hard-level questions and system design to stand out.")
    if not tips:
        tips.append("Keep practicing company-specific questions and review missed explanations carefully.")
    return tips


# ── Legacy company awareness (preserve old endpoint functionality) ─────────────

def get_test_awareness(company_name: str, role: str) -> dict:
    awareness_db = {
        "google":    {
            "name": "Google",
            "rounds": ["Online Coding Test", "Technical Phone Screen", "3–5 Onsite Rounds (Algorithms + System Design)", "Googleyness & Leadership Round"],
            "preparation_tips": ["Master Data Structures and Algorithms (LeetCode Hard)", "Study System Design basics", "Practice STAR behavioural answers", "Review Google Engineering blogs"]
        },
        "amazon":    {
            "name": "Amazon",
            "rounds": ["Online Assessment (Coding + Work Simulation)", "Technical Phone Screen", "Onsite Loop (4–5 rounds)", "Leadership Principles Deep Dive"],
            "preparation_tips": ["Study Amazon's 16 Leadership Principles", "Practice LeetCode Medium", "Prepare multiple STAR stories", "Study System Design at scale"]
        },
        "microsoft": {
            "name": "Microsoft",
            "rounds": ["Recruiter Screen", "Technical Phone Interview", "Onsite (4 rounds: Coding + Design + Behavioral)", "As-Appropriate Round"],
            "preparation_tips": ["Focus on problem solving and code quality", "Practice Object-Oriented Design", "Be ready to explain your thought process aloud", "Review .NET/Azure technologies"]
        },
        "meta":      {
            "name": "Meta (Facebook)",
            "rounds": ["Recruiter Call", "Technical Screen (2 coding problems)", "Onsite (5 rounds: Coding, System Design, Behavioral)"],
            "preparation_tips": ["Study Graph algorithms and Dynamic Programming", "Practice System Design for social networks", "Understand Meta's core products deeply", "Practice explaining trade-offs"]
        },
        "tcs":       {
            "name": "TCS",
            "rounds": ["TCS NQT Online Test", "Technical Interview", "Managerial Round", "HR Round"],
            "preparation_tips": ["Practice Quantitative Aptitude", "Study basic C/Java/Python", "Review DBMS and OS concepts", "Prepare HR answers about relocation and flexibility"]
        },
        "infosys":   {
            "name": "Infosys",
            "rounds": ["HackWithInfy / Online Test", "Technical Interview", "HR Round"],
            "preparation_tips": ["Practice Reasoning and English sections", "Study OOP concepts", "Review SDLC methodologies", "Prepare for situational HR questions"]
        },
    }
    key = company_name.lower().strip()
    for k, v in awareness_db.items():
        if k in key or key in k:
            return {"company": v["name"], "rounds": v["rounds"], "preparation_tips": v["preparation_tips"]}
    return {
        "company": company_name,
        "rounds": ["Aptitude Test", "Technical Interview", "HR Interview"],
        "preparation_tips": ["Practice Data Structures and Algorithms", "Review core CS concepts", "Prepare STAR format behavioral answers"]
    }
