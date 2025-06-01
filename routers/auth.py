# curie/router/auth.py

from fastapi import APIRouter, HTTPException
from models.user import UserProfile
from supabase_client import supabase

router = APIRouter()

@router.post("/register")
def register_user(profile: UserProfile):
    # Check if user already exists
    existing = supabase.table("users").select("*").eq("email", profile.email).execute()
    if existing.data:
        raise HTTPException(status_code=400, detail="User already exists")

    # Insert user profile (only long-term data)
    response = supabase.table("users").insert(profile.dict()).execute()

    if response.data:
        return {"message": "User registered successfully", "data": response.data}

    raise HTTPException(status_code=500, detail="Failed to register user")
