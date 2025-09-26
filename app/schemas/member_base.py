from typing import Optional, List
from pydantic import BaseModel, Field, validator
from datetime import date

class MemberBase(BaseModel):
    first_name: str
    last_name: str
    photo: Optional[str] = None
    birth_date: date
    field_of_study: str
    nickname: Optional[str] = ""
    current_job: str
    interests: Optional[List[str]] = Field(default_factory=list)
    skills: Optional[List[str]] = Field(default_factory=list)
    personality_traits: Optional[List[str]] = Field(default_factory=list)
    curses_given: Optional[int] = 0
    debts: Optional[float] = 0.0
    credits: Optional[float] = 0.0
    group_role: str
    recommended_movie: Optional[str] = None
    recommended_music: Optional[str] = None
    recommended_book: Optional[str] = None
    recommended_game: Optional[str] = None
    motto: Optional[str] = None

    @validator("birth_date")
    def validate_birth_date(cls, v: date):
        if not isinstance(v, date):
            raise ValueError("birth_date must be YYYY-MM-DD")
        return v

