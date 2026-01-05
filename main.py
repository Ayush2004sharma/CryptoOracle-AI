from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
import os

from schemas import (
    SignupSchema,
    LoginSchema,
    TokenResponse,
    TradeRequest,
)
from database import user_collection
from auth import hash_password, verify_password, create_access_token
from main_runner import run_trading_pipeline
 
load_dotenv()

app = FastAPI(
    title="AI Crypto Trading Research API",
    version="1.0.0"
)

# -----------------------------
# AUTH APIs
# -----------------------------

@app.post("/auth/signup")
async def signup(user: SignupSchema):
    existing = await user_collection.find_one({"email": user.email})
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    await user_collection.insert_one({
        "name": user.name,
        "email": user.email,
        "password": hash_password(user.password)
    })

    return {"message": "User registered successfully"}

@app.post("/auth/login", response_model=TokenResponse)
async def login(user: LoginSchema):
    db_user = await user_collection.find_one({"email": user.email})
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user.email})

    return {
        "access_token": token,
        "token_type": "bearer",
        "name": db_user.get("name"),
        "email": db_user.get("email"),
    }


# -----------------------------
# AI TRADING API
# -----------------------------

@app.post("/trade/analyze")
def analyze_trade(request: TradeRequest):
    try:
        result = run_trading_pipeline(
            coin=request.coin,
            trade_date=request.trade_date,
            trader_position=request.trader_position,
            duration=request.duration,
        )

        return {
            "status": "success",
            "data": result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
