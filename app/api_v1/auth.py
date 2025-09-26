from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import RegisterRequest, LoginRequest, LoginResponse
from app.auth import create_access_token, hash_password
from app.db import get_user_by_username, get_session, authenticate_user
from app.models import User

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"]
)


@router.post("/register", status_code=201)
def register(req: RegisterRequest = Body(...), db: Session = Depends(get_session)):
    if not req.username or not req.password:
        raise HTTPException(status_code=400, detail={"error": "username and password required"})
    if get_user_by_username(db, req.username):
        raise HTTPException(status_code=400, detail={"error": "username already exists"})
    user = User(username=req.username, hashed_password=hash_password(req.password), is_active=1)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"id": user.id, "username": user.username}


@router.post("/login", response_model=LoginResponse)
def login(req: LoginRequest = Body(...), db: Session = Depends(get_session)):
    user = authenticate_user(db, req.username, req.password)
    if not user:
        raise HTTPException(status_code=401, detail={"error": "Invalid username or password"})
    token = create_access_token(subject=user.username)
    return {"access_token": token, "token_type": "bearer"}

