# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Routers
from routers.reinforce import router as reinforce_router
from routers.feedback_prompt import router as feedback_prompt_router
from routers.feed import router as feed_router  # Optional
from routers.auth import router as register_router  # New

app = FastAPI(
    title="Curie Content Agent",
    version="0.1.0",
    description="Personalized content recommendation based on user intent, mood, and feedback."
)

# CORS for local/frontend dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with frontend domain in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all routers with tags
app.include_router(register_router, prefix="/api", tags=["Onboarding"])
app.include_router(feedback_prompt_router, prefix="/api", tags=["Feedback"])
app.include_router(reinforce_router, prefix="/api", tags=["Reinforcement"])
app.include_router(feed_router, prefix="/api", tags=["Feed"])  # When implemented

@app.get("/")
def health_check():
    return {"message": "Curie backend is running ✅"}
