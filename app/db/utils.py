from typing import Optional, List, Dict, Any
import uuid
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models import User, Member
from app.auth import verify_password

def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.execute(select(User).filter_by(username=username)).scalar_one_or_none()


def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    user = get_user_by_username(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


def get_or_create_by_name(db: Session, Model, name: str):
    name = name.strip()
    if not name:
        return None
    instance = db.execute(select(Model).filter_by(name=name)).scalar_one_or_none()
    if instance:
        return instance
    instance = Model(name=name)
    db.add(instance)
    db.commit()
    db.refresh(instance)
    return instance


def names_from_relation(rel_list) -> List[str]:
    return [r.name for r in rel_list]


def member_to_dict(member: Member) -> Dict[str, Any]:
    return {
        "id": uuid.UUID(member.id),
        "first_name": member.first_name,
        "last_name": member.last_name,
        "photo": member.photo,
        "birth_date": member.birth_date,
        "field_of_study": member.field_of_study,
        "nickname": member.nickname,
        "current_job": member.current_job,
        "interests": names_from_relation(member.interests),
        "skills": names_from_relation(member.skills),
        "personality_traits": names_from_relation(member.personality_traits),
        "curses_given": member.curses_given,
        "debts": member.debts,
        "credits": member.credits,
        "group_role": member.group_role,
        "recommended_movie": member.recommended_movie,
        "recommended_music": member.recommended_music,
        "recommended_book": member.recommended_book,
        "recommended_game": member.recommended_game,
        "motto": member.motto,
    }

