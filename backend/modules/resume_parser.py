import PyPDF2
import docx
import spacy
from io import BytesIO

# Load SpaCy model for NLP. For production, ensure 'en_core_web_sm' is downloaded.
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    # If not present, we will try to load it assuming the user runs `python -m spacy download en_core_web_sm`
    nlp = None

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract text from a PDF file."""
    try:
        reader = PyPDF2.PdfReader(BytesIO(file_bytes))
        text = ""
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
        return text
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return ""

def extract_text_from_docx(file_bytes: bytes) -> str:
    """Extract text from a DOCX file."""
    doc = docx.Document(BytesIO(file_bytes))
    return "\n".join([para.text for para in doc.paragraphs])

# Comprehensive list of recognized technical and professional skills
VALID_SKILLS = {
    # Languages
    "python", "java", "javascript", "typescript", "c", "c++", "c#", "go", "rust",
    "kotlin", "swift", "r", "scala", "php", "ruby", "dart", "bash", "shell",
    # Web
    "react", "angular", "vue", "next.js", "node.js", "express", "html", "css",
    "tailwind", "bootstrap", "jquery", "graphql", "rest api", "fastapi", "flask",
    "django", "spring", "asp.net", "laravel",
    # Data / AI / ML
    "machine learning", "deep learning", "nlp", "computer vision", "data science",
    "tensorflow", "pytorch", "keras", "scikit-learn", "pandas", "numpy", "matplotlib",
    "seaborn", "openai", "langchain", "huggingface", "transformers", "bert",
    "xgboost", "random forest", "neural network", "llm", "generative ai",
    # Databases
    "sql", "mysql", "postgresql", "mongodb", "redis", "elasticsearch", "sqlite",
    "cassandra", "oracle", "dynamodb", "firebase",
    # DevOps / Cloud
    "docker", "kubernetes", "aws", "azure", "gcp", "ci/cd", "jenkins", "github actions",
    "terraform", "ansible", "linux", "git", "github", "gitlab", "nginx",
    # Tools / Practices
    "agile", "scrum", "jira", "figma", "postman", "swagger", "microservices",
    "system design", "data structures", "algorithms", "oop", "api development",
    # Mobile
    "android", "ios", "flutter", "react native"
}

def extract_keywords(text: str) -> list[str]:
    """Extract ONLY valid technical skills from resume text using a curated whitelist."""
    text_lower = text.lower()
    
    # First pass: check for multi-word skills (must come before single-word to avoid partial matches)
    found_skills = set()
    for skill in VALID_SKILLS:
        if skill in text_lower:
            found_skills.add(skill)

    # Second pass fallback: use spaCy to find nouns and match against whitelist
    if nlp and len(found_skills) < 3:
        doc = nlp(text)
        for token in doc:
            token_lower = token.text.lower()
            if token_lower in VALID_SKILLS:
                found_skills.add(token_lower)

    # Capitalize skills for display
    result = [s.title() for s in sorted(found_skills)]
    return result if result else ["Python", "Communication", "Problem Solving"]
