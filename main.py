from fastapi import FastAPI, Depends, HTTPException
from models.user import User
from db.mongo import database
import jwt
import datetime
import os
from models.preferences import CollegePreferences
from services.chatgpt import get_college_ranking
from fastapi.middleware.cors import CORSMiddleware
import logging
from models.subscription import Subscription
from bcrypt import hashpw, gensalt, checkpw

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://got10in.com/"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO)

SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key_here")

def create_jwt_token(data: dict):
    expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    return jwt.encode({"exp": expiration, **data}, SECRET_KEY, algorithm="HS256")

def decode_jwt_token(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

@app.get("/generate_ranking/")
async def generate_ranking(token: str = Depends(decode_jwt_token)):
    username = token["username"]
    user = await database.users.find_one({"username": username})
    if not user or "preferences" not in user:
        raise HTTPException(status_code=400, detail="Preferences not set")
    preferences = user["preferences"]
    prompt = f"Based on a student's preference for {preferences['field_of_study']} and {preferences['location_preference']}, rank the top colleges."
    ranking = await get_college_ranking(prompt)
    return {"ranking": ranking}

@app.post("/register/")
async def register(user: User):
    existing_user = await database.users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")
    hashed_password = hashpw(user.password.encode('utf-8'), gensalt())
    user.password = hashed_password.decode('utf-8')
    await database.users.insert_one(user.dict())
    return {"message": "User registered successfully!"}

@app.post("/subscribe/")
async def subscribe(subscription: Subscription):
    existing_subscription = await database.subscriptions.find_one({"email": subscription.email})
    if existing_subscription:
        raise HTTPException(status_code=400, detail="Email already subscribed")
    await database.subscriptions.insert_one(subscription.dict())
    return {"message": "Subscribed successfully!"}

@app.post("/login/")
async def login(user: User):
    db_user = await database.users.find_one({"email": user.email})
    if not db_user or not checkpw(user.password.encode('utf-8'), db_user["password"].encode('utf-8')):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = create_jwt_token({"email": user.email})
    return {"access_token": token}

@app.post("/preferences/")
async def set_preferences(preferences: CollegePreferences, token: str = Depends(decode_jwt_token)):
    username = token["email"]
    await database.users.update_one({"email": username}, {"$set": {"preferences": preferences.dict()}})
    return {"message": "Preferences updated successfully!"}
