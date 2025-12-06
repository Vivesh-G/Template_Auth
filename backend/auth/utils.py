from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta
import uuid
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "unsafe_fallback_secret")
ALGORITHM = "HS256"

pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str):
    return pwd_context.verify(password, hashed)

def create_access_token(data: dict, expires_minutes: int = 60):
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(minutes=expires_minutes)
    payload["jti"] = str(uuid.uuid4()) # Unique identifier for every token
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)