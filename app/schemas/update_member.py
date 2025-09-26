from typing import Optional, List
from datetime import date
from pydantic import BaseModel, validator

class MemberUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    photo: Optional[str] = None
    birth_date: Optional[date] = None
    field_of_study: Optional[str] = None
    nickname: Optional[str] = None
    current_job: Optional[str] = None
    interests: Optional[List[str]] = None
    skills: Optional[List[str]] = None
    personality_traits: Optional[List[str]] = None
    curses_given: Optional[int] = None
    debts: Optional[float] = None
    credits: Optional[float] = None
    group_role: Optional[str] = None
    recommended_movie: Optional[str] = None
    recommended_music: Optional[str] = None
    recommended_book: Optional[str] = None
    recommended_game: Optional[str] = None
    motto: Optional[str] = None

    @validator("birth_date")
    def validate_birth_date(cls, v: Optional[date]):
        if v is None:
            return v
        if not isinstance(v, date):
            raise ValueError("birth_date must be YYYY-MM-DD")
        return v

