"""
Job API Service — fetches real job listings from open APIs.

Sources:
  - Arbeitnow: https://www.arbeitnow.com/api/job-board-api  (no auth, free)
  - Remotive:  https://remotive.com/api/remote-jobs         (no auth, free)

Features:
  - In-memory cache (10-minute TTL) per role to avoid repeat API calls
  - Role normalization: maps specialist titles to stable, high-result roles
  - Relevance scoring: ranks results by keyword match against the searched role
"""
import re
import uuid
import asyncio
import time
import aiohttp

# ── In-memory cache: { normalized_role: {"jobs": [...], "ts": float} } ────────
_cache: dict = {}
CACHE_TTL_SECONDS = 600  # 10 minutes


# ── Role normalization ─────────────────────────────────────────────────────────
# Maps specific / niche roles → stable roles that return good API results.
ROLE_NORMALIZE = {
    # DevOps / Cloud
    "devops engineer":             "software developer",
    "cloud engineer":              "software developer",
    "site reliability engineer":   "software developer",
    "sre":                         "software developer",
    "platform engineer":           "software developer",
    # ML / AI
    "machine learning engineer":   "software developer",
    "deep learning engineer":      "software developer",
    "ai engineer":                 "software developer",
    "nlp engineer":                "software developer",
    "data engineer":               "software developer",
    "computer vision engineer":    "software developer",
    "generative ai engineer":      "software developer",
    "llm engineer":                "software developer",
    # Frontend variants
    "react developer":             "frontend developer",
    "angular developer":           "frontend developer",
    "vue developer":               "frontend developer",
    "vue.js developer":            "frontend developer",
    "ember developer":             "frontend developer",
    # Backend variants
    "node.js developer":           "backend developer",
    "django developer":            "backend developer",
    "flask developer":             "backend developer",
    "fastapi developer":           "backend developer",
    "spring developer":            "backend developer",
    "laravel developer":           "backend developer",
    # Mobile
    "flutter developer":           "mobile developer",
    "react native developer":      "mobile developer",
    "android developer":           "mobile developer",
    "ios developer":               "mobile developer",
    # Data
    "data analyst":                "data scientist",
    "business analyst":            "data scientist",
    # .NET / C#
    "c# developer":                "dotnet developer",
    "asp.net developer":           "dotnet developer",
    ".net developer":              "dotnet developer",
}

def normalize_role(role: str) -> str:
    """Map niche roles to stable equivalents; otherwise return as-is."""
    key = role.strip().lower()
    return ROLE_NORMALIZE.get(key, key)


# ── Scoring helper ─────────────────────────────────────────────────────────────

def score_job(original_role: str, job_title: str) -> int:
    """
    Score how closely a job title matches the searched role.
    90 → all words match, 70 → at least one word matches, 50 → generic.
    """
    words = original_role.lower().split()
    title_lower = job_title.lower()
    matching = sum(1 for w in words if w in title_lower)
    if matching == len(words):
        return 90
    elif matching > 0:
        return 70
    return 50


# ── Arbeitnow ─────────────────────────────────────────────────────────────────

async def fetch_arbeitnow(session: aiohttp.ClientSession, role: str) -> list[dict]:
    jobs = []
    try:
        # Arbeitnow supports ?search= query param
        import urllib.parse
        encoded_role = urllib.parse.quote(role)
        url = f"https://www.arbeitnow.com/api/job-board-api?search={encoded_role}"
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=15)) as resp:
            if resp.status == 200:
                data = await resp.json(content_type=None)
                role_keywords = role.lower().split()
                for job in data.get("data", []):
                    title     = job.get("title", "")
                    apply_url = job.get("url", "")
                    if not title or not apply_url:
                        continue
                    # Filter: job title must contain at least one role keyword
                    title_lower = title.lower()
                    if not any(kw in title_lower for kw in role_keywords):
                        continue
                    raw_desc   = job.get("description", "")
                    clean_desc = re.sub(r"<[^>]+>", " ", raw_desc)[:300].strip()
                    jobs.append({
                        "id":             str(uuid.uuid4()),
                        "jobTitle":       title,
                        "company":        job.get("company_name", "Unknown"),
                        "location":       job.get("location", "Remote"),
                        "skills":         job.get("tags", [])[:5],
                        "jobDescription": clean_desc,
                        "applyUrl":       apply_url,
                        "source":         "Arbeitnow",
                        "score":          score_job(role, title),
                    })
            else:
                print(f"Arbeitnow returned status {resp.status}")
    except Exception as e:
        print(f"Arbeitnow API error: {e}")
    return jobs



# ── Remotive ──────────────────────────────────────────────────────────────────

async def fetch_remotive(session: aiohttp.ClientSession, role: str) -> list[dict]:
    jobs = []
    try:
        import urllib.parse
        encoded = urllib.parse.quote(role)
        url = f"https://remotive.com/api/remote-jobs?search={encoded}&limit=20"
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=15)) as resp:
            if resp.status == 200:
                data = await resp.json(content_type=None)
                for job in data.get("jobs", []):
                    title     = job.get("title", "")
                    apply_url = job.get("url", "")
                    if not title or not apply_url:
                        continue
                    raw_desc   = job.get("description", "")
                    clean_desc = re.sub(r"<[^>]+>", " ", raw_desc)[:300].strip()
                    jobs.append({
                        "id":             str(uuid.uuid4()),
                        "jobTitle":       title,
                        "company":        job.get("company_name", "Unknown"),
                        "location":       job.get("candidate_required_location", "Remote"),
                        "skills":         job.get("tags", [])[:5],
                        "jobDescription": clean_desc,
                        "applyUrl":       apply_url,
                        "source":         "Remotive",
                        "score":          score_job(role, title),
                    })
            else:
                print(f"Remotive returned status {resp.status}")
    except Exception as e:
        print(f"Remotive API error: {e}")
    return jobs


# ── Main function ─────────────────────────────────────────────────────────────

async def fetch_jobs_for_role(role: str, top_k: int = 10) -> list[dict]:
    """
    Fetch and rank jobs for the given role.

    Order of operations:
      1. Normalize the role (e.g. "React Developer" → "Frontend Developer")
      2. Check the in-memory cache (TTL: 10 min)
      3. If cache miss → call Arbeitnow + Remotive in parallel
      4. Score, deduplicate, sort and cache the results
      5. Return top_k items
    """
    original_role  = role.strip()
    lookup_role    = normalize_role(original_role)       # stable search key
    cache_key      = lookup_role.lower()

    # ── Cache check ──────────────────────────────────────────────────────────
    if cache_key in _cache:
        entry = _cache[cache_key]
        age   = time.time() - entry["ts"]
        if age < CACHE_TTL_SECONDS:
            print(f"Cache HIT for '{lookup_role}' (age {age:.0f}s) → {len(entry['jobs'])} jobs")
            cached = entry["jobs"]
            # Re-score against the *original* role in case it differs from
            # what was cached (e.g. cached as "frontend developer", searched
            # as "react developer" → bump scores for matching titles).
            for j in cached:
                j["score"] = score_job(original_role, j["jobTitle"])
            cached.sort(key=lambda j: j["score"], reverse=True)
            return cached[:top_k]

    print(f"Cache MISS for '{lookup_role}' → fetching from APIs")

    # ── Fetch ─────────────────────────────────────────────────────────────────
    try:
        async with aiohttp.ClientSession() as session:
            arbeitnow_jobs, remotive_jobs = await asyncio.gather(
                fetch_arbeitnow(session, lookup_role),
                fetch_remotive(session, lookup_role),
            )
    except Exception as e:
        print(f"Network error fetching jobs: {e}")
        # Return stale cache as fallback if available
        if cache_key in _cache:
            print("Returning stale cache as fallback")
            return _cache[cache_key]["jobs"][:top_k]
        return []

    all_jobs = arbeitnow_jobs + remotive_jobs
    print(f"  Arbeitnow: {len(arbeitnow_jobs)} | Remotive: {len(remotive_jobs)} | Total: {len(all_jobs)}")

    # ── Deduplicate by URL ────────────────────────────────────────────────────
    seen, unique = set(), []
    for job in all_jobs:
        url = job.get("applyUrl", "")
        if url and url not in seen:
            seen.add(url)
            unique.append(job)

    # ── Re-score against original search term ────────────────────────────────
    for job in unique:
        job["score"] = score_job(original_role, job["jobTitle"])

    unique.sort(key=lambda j: j["score"], reverse=True)

    # ── Cache the full result set ─────────────────────────────────────────────
    _cache[cache_key] = {"jobs": unique, "ts": time.time()}
    print(f"Cached {len(unique)} jobs for '{lookup_role}'")

    return unique[:top_k]
