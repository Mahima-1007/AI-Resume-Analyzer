from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import auth, api

app = FastAPI(title="AI Resume & Job Matcher API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(api.router, prefix="/api", tags=["Main Features"])

@app.get("/")
def read_root():
    return {"message": "AI Resume and Job Matching System API - MongoDB Edition"}
