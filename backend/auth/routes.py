from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from database import SessionLocal, get_db
from auth.models import User, RevokedToken
from auth.utils import hash_password, verify_password, create_access_token, SECRET_KEY, ALGORITHM
from datetime import datetime, timedelta
from pydantic import BaseModel
from limiter import limiter
from auth.dependencies import get_current_user, oauth2_scheme
import jwt
from datetime import datetime
from audit import log_action

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
@limiter.limit("5/minute")
def signup(request: Request, data: SignupModel, db: Session = Depends(get_db)):
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

    log_action(db, "SIGNUP", new_user.id, request.client.host, f"Email: {data.email}")
    return {"message": "Signup successful", "user_id": new_user.id}

@router.post("/login")
@limiter.limit("5/minute")
def login(request: Request, data: LoginModel, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token({"sub": user.email})
    log_action(db, "LOGIN", user.id, request.client.host, f"Email: {data.email}")
    return {"access_token": token, "token_type": "bearer"}

@router.post("/logout")
def logout(request: Request, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
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
    log_action(db, "LOGOUT", current_user.id, request.client.host, "User logged out")
    return {"message": "Logged out successfully"}

@router.post("/change-password")
@limiter.limit("5/minute")
def change_password(request: Request, data: ChangePasswordModel, db: Session = Depends(get_db)):
    # Verify user credentials (email + old_password)
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.old_password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or old password")
    
    # Update password
    user.hashed_password = hash_password(data.new_password)
    db.commit()
    
    # Generate new token
    token = create_access_token({"sub": user.email})
    
    # Attempt to revoke the current token if provided in the header
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        old_token = auth_header.split(" ")[1]
        # Check if already revoked to avoid duplicates
        if not db.query(RevokedToken).filter(RevokedToken.token == old_token).first():
            revoked = RevokedToken(
                token=old_token,
                revoked_at=datetime.utcnow().isoformat(),
                expires_at=(datetime.utcnow() +  timedelta(minutes=60)).isoformat() # Approximation
            )
            db.add(revoked)
            db.commit()

    log_action(db, "CHANGE_PASSWORD", user.id, request.client.host, "Password changed")
    return {"message": "Password changed successfully", "access_token": token, "token_type": "bearer"}