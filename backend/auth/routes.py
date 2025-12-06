from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from database import SessionLocal, get_db
from auth.models import User, RevokedToken
from auth.utils import hash_password, verify_password, create_access_token, SECRET_KEY, ALGORITHM
from pydantic import BaseModel
from limiter import limiter
from auth.dependencies import get_current_user, oauth2_scheme
import jwt
from datetime import datetime

router = APIRouter(prefix="/auth", tags=["Authentication"])

class SignupModel(BaseModel):
    email: str
    password: str

class LoginModel(BaseModel):
    email: str
    password: str

class ChangePasswordModel(BaseModel):
    email: str
    old_password: str
    new_password: str

@router.post("/signup")
def signup(data: SignupModel, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if user:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = User(
        email=data.email,
        hashed_password=hash_password(data.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "Signup successful", "user_id": new_user.id}

@router.post("/login")
@limiter.limit("5/minute")
def login(request: Request, data: LoginModel, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/logout")
def logout(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Calculate expiration
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        exp = payload.get("exp")
        expires_at = datetime.fromtimestamp(exp).isoformat()
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    revoked_token = RevokedToken(
        token=token,
        revoked_at=datetime.utcnow().isoformat(),
        expires_at=expires_at
    )
    db.add(revoked_token)
    db.commit()
    return {"message": "Logged out successfully"}

@router.post("/change-password")
def change_password(data: ChangePasswordModel, db: Session = Depends(get_db)):
    # Verify user credentials (email + old_password)
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.old_password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or old password")
    
    # Update password
    user.hashed_password = hash_password(data.new_password)
    db.commit()
    
    # Generate new token
    token = create_access_token({"sub": user.email})
    
    return {"message": "Password changed successfully", "access_token": token, "token_type": "bearer"}