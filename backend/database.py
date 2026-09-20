from pymongo import MongoClient
from urllib.parse import quote_plus
import os

# ─── MongoDB Connection ───────────────────────────────────────────────
username = "madhumahi210_db_user"
password = quote_plus("minnu2005***")   # URL-encodes special characters like *

MONGO_URI = os.getenv(
    "MONGO_URI",
    f"mongodb+srv://{username}:{password}@cluster0.6kmjzb5.mongodb.net/?appName=Cluster0"
)

client = MongoClient(MONGO_URI)
db = client["ai_resume_db"]

# Collections (equivalent to SQL tables)
users_col     = db["users"]
resumes_col   = db["resumes"]
applications_col = db["applications"]
jobs_col      = db["scraped_jobs"]
