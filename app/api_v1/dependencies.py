from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import JWTError
from app.auth import oauth2_scheme, decode_token
from app.db import get_session, get_user_by_username
from app.models import User

def get_current_user(db: Session = Depends(get_session), token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={"error": "Could not validate credentials"},
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        username = decode_token(token)
    except JWTError:
        raise credentials_exception
    user = get_user_by_username(db, username)
    if not user or not user.is_active:
        raise credentials_exception
    return user

