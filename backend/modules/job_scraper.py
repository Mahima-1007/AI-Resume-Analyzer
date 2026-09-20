"""
Naukri-only job scraper using Playwright with stealth patches to bypass
Akamai bot detection. No LinkedIn, no fallback APIs — Naukri only.
"""
import asyncio
import uuid
import random
from playwright.async_api import async_playwright

try:
    from playwright_stealth import stealth_async
    HAS_STEALTH = True
except ImportError:
    HAS_STEALTH = False
    print("playwright-stealth not installed; running without stealth patch")

# ── Skill → Naukri slug + display title mapping ──────────────────────────────
SKILL_TO_QUERY = {
    "python":           ("python-developer",          "Python Developer"),
    "java":             ("java-developer",             "Java Developer"),
    "javascript":       ("javascript-developer",       "JavaScript Developer"),
    "typescript":       ("typescript-developer",       "TypeScript Developer"),
    "react":            ("react-developer",            "React Developer"),
    "node.js":          ("node-js-developer",         "Node.js Developer"),
    "angular":          ("angular-developer",          "Angular Developer"),
    "vue":              ("vue-js-developer",           "Vue.js Developer"),
    "django":           ("django-developer",           "Django Developer"),
    "fastapi":          ("python-developer",           "Python Developer"),
    "flask":            ("flask-developer",            "Flask Developer"),
    "machine learning": ("machine-learning",           "Machine Learning Engineer"),
    "deep learning":    ("deep-learning",              "Deep Learning Engineer"),
    "data science":     ("data-scientist",             "Data Scientist"),
    "nlp":              ("nlp-engineer",               "NLP Engineer"),
    "sql":              ("sql-developer",              "SQL Developer"),
    "mysql":            ("mysql-developer",            "MySQL Developer"),
    "mongodb":          ("mongodb-developer",          "MongoDB Developer"),
    "docker":           ("devops-engineer",            "DevOps Engineer"),
    "kubernetes":       ("kubernetes-engineer",        "Kubernetes Engineer"),
    "aws":              ("aws-cloud-engineer",         "AWS Cloud Engineer"),
    "azure":            ("azure-developer",            "Azure Developer"),
    "gcp":              ("gcp-engineer",               "GCP Cloud Engineer"),
    "tensorflow":       ("machine-learning",           "Machine Learning Engineer"),
    "pytorch":          ("deep-learning",              "Deep Learning Engineer"),
    "android":          ("android-developer",          "Android Developer"),
    "flutter":          ("flutter-developer",          "Flutter Developer"),
    "react native":     ("react-native-developer",    "React Native Developer"),
    "c++":              ("cpp-developer",              "C++ Developer"),
    "c#":               ("dotnet-developer",           "C# .NET Developer"),
    "data structures":  ("software-engineer",          "Software Engineer"),
    "llm":              ("ai-engineer",                "AI Engineer"),
    "generative ai":    ("ai-engineer",                "Generative AI Engineer"),
    "full stack":       ("full-stack-developer",       "Full Stack Developer"),
    "html":             ("frontend-developer",         "Frontend Developer"),
    "css":              ("frontend-developer",         "Frontend Developer"),
    "linux":            ("linux-administrator",        "Linux Engineer"),
    "git":              ("software-engineer",          "Software Engineer"),
}


def generate_queries(skills: list[str]) -> list[tuple[str, str]]:
    """
    Converts extracted skill list into Naukri job role queries.
    Always includes generic roles; adds specific roles based on skill groups.
    Returns list of (naukri_slug, display_title) tuples (max 5).
    """
    skills_lower = {s.lower() for s in skills}
    queries: list[tuple[str, str]] = []
    seen_slugs: set[str] = set()

    def add(slug: str, title: str):
        if slug not in seen_slugs:
            seen_slugs.add(slug)
            queries.append((slug, title))

    # ── Skill-group specific roles (added first, highest priority) ──────────────
    # Java / JVM stack
    if skills_lower & {"java", "spring", "kotlin", "hibernate"}:
        add("java-developer", "Java Developer")

    # Python backend
    if skills_lower & {"python", "django", "flask", "fastapi"}:
        add("python-developer", "Python Developer")

    # MySQL / Flask → backend developer (per user rule)
    if skills_lower & {"mysql", "flask", "postgresql", "sql", "mongodb"}:
        add("backend-developer", "Backend Developer")

    # JavaScript / frontend
    if skills_lower & {"javascript", "typescript", "react", "angular", "vue", "node.js"}:
        add("javascript-developer", "JavaScript Developer")

    # Web / HTML / CSS → frontend + web developer (per user rule)
    if skills_lower & {"html", "css", "bootstrap", "tailwind", "jquery"}:
        add("frontend-developer", "Frontend Developer")
        add("web-developer", "Web Developer")

    # Data / ML
    if skills_lower & {"machine learning", "deep learning", "data science",
                       "tensorflow", "pytorch", "pandas", "numpy", "nlp"}:
        add("machine-learning", "Machine Learning Engineer")
        add("data-scientist", "Data Scientist")

    # DevOps / Cloud
    if skills_lower & {"docker", "kubernetes", "aws", "azure", "gcp", "jenkins", "linux"}:
        add("devops-engineer", "DevOps Engineer")

    # Mobile
    if skills_lower & {"android", "flutter", "react native", "ios", "dart"}:
        add("mobile-developer", "Mobile App Developer")

    # ── Always include generic roles regardless of skills detected ───────────
    add("software-developer",  "Software Developer")
    add("full-stack-developer", "Full Stack Developer")
    add("backend-developer",   "Backend Developer")
    add("frontend-developer",  "Frontend Developer")
    add("web-developer",       "Web Developer")

    print(f"Generated Naukri queries: {[t for _, t in queries]}")
    return queries[:8]   # Up to 8 queries for broad coverage




async def scrape_naukri_query(slug: str, display_title: str, skills: list[str]) -> list[dict]:
    """
    Scrape one Naukri search page using Playwright + stealth.
    URL: https://www.naukri.com/{slug}-jobs
    """
    jobs = []
    url = f"https://www.naukri.com/{slug}-jobs"

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu",
            ]
        )
        context = await browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                f"Chrome/{random.randint(110, 116)}.0.0.0 Safari/537.36"
            ),
            viewport={"width": 1366, "height": 768},
            locale="en-IN",
            timezone_id="Asia/Kolkata",
            extra_http_headers={
                "Accept-Language": "en-IN,en;q=0.9",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            }
        )

        page = await context.new_page()

        # Apply stealth patches if available
        if HAS_STEALTH:
            await stealth_async(page)

        # Block heavy resources to speed up and reduce fingerprint
        await page.route("**/*", lambda route: (
            route.abort() if route.request.resource_type in ["image", "media", "font"]
            else route.continue_()
        ))

        print(f"  Opening: {url}")
        try:
            await page.goto(url, wait_until="domcontentloaded", timeout=25000)
        except Exception as e:
            print(f"  Goto failed for {url}: {e}")
            await browser.close()
            return jobs

        # Wait generously for JS to render job cards
        await page.wait_for_timeout(random.randint(3000, 5000))

        # Probe available selectors (Naukri changes class names frequently)
        card_selectors = [
            "div.jobTuple",
            "div.srp-jobtuple-wrapper",
            "div[class*='jobTuple']",
            "article.jobTuple",
            "div.cust-job-tuple",
            "div.list-container div[class*='tuple']",
        ]

        job_cards = []
        for sel in card_selectors:
            cards = await page.query_selector_all(sel)
            if cards:
                job_cards = cards
                print(f"  Found {len(cards)} job cards using: '{sel}'")
                break

        if not job_cards:
            # Last resort: dump page title to debug
            title_text = await page.title()
            print(f"  0 job cards found on {url}  (page title: '{title_text}')")

        # Extract data from each card
        for card in job_cards[:10]:
            try:
                # Title selectors (tried in order)
                title_elem = (
                    await card.query_selector("a.title")
                    or await card.query_selector("a[class*='title']")
                    or await card.query_selector("a.jobTitle")
                    or await card.query_selector("h2 a")
                    or await card.query_selector("a")
                )
                company_elem = (
                    await card.query_selector("a.subTitle")
                    or await card.query_selector("a.comp-name")
                    or await card.query_selector("span.comp-name")
                    or await card.query_selector("a[class*='company']")
                )
                loc_elem = (
                    await card.query_selector("li.location")
                    or await card.query_selector("span.locWdth")
                    or await card.query_selector("li[class*='location']")
                    or await card.query_selector("span[class*='location']")
                )

                if not title_elem:
                    continue

                title   = (await title_elem.inner_text()).strip()
                apply_url = await title_elem.get_attribute("href") or ""
                company = (await company_elem.inner_text()).strip() if company_elem else "Unknown"
                location = (await loc_elem.inner_text()).strip() if loc_elem else "India"

                if title and apply_url:
                    jobs.append({
                        "id":           str(uuid.uuid4()),
                        "jobTitle":     title,
                        "company":      company,
                        "location":     location,
                        "skills":       skills[:5],
                        "jobDescription": f"Click Apply to view full description for {display_title} on Naukri.",
                        "applyUrl":     apply_url,
                        "source":       "Naukri",
                    })
            except Exception as ce:
                print(f"  Card error: {ce}")
                continue

        await context.close()
        await browser.close()

    print(f"  Scraped {len(jobs)} jobs from {url}")
    return jobs


async def scrape_jobs(skills: list[str]) -> list[dict]:
    """
    Main entry: generates Naukri queries → scrapes each → deduplicates → returns results.
    Returns empty list (no fallback API) if Naukri is unreachable.
    """
    if not skills:
        return []

    queries = generate_queries(skills)
    print(f"Generated Naukri queries: {[t for _, t in queries]}")

    all_jobs: list[dict] = []
    seen_urls: set[str] = set()

    for slug, title in queries:
        batch = await scrape_naukri_query(slug, title, skills)
        for job in batch:
            url = job.get("applyUrl", "")
            if url and url not in seen_urls:
                seen_urls.add(url)
                all_jobs.append(job)
        # Respectful delay between queries
        await asyncio.sleep(random.uniform(2.0, 3.5))

    print(f"Scraped jobs count: {len(all_jobs)}")
    return all_jobs[:20]
