
from typing import Optional

from pydantic import BaseModel, EmailStr, Field

class SignupSchema(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class LoginSchema(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    name: Optional[str]
    email: EmailStr

class TradeRequest(BaseModel):
    coin: str
    trade_date: Optional[str] = None
    trader_position: str = "existing_buyer"
    duration: str = "short_term"
