import uuid
from datetime import date
from pydantic import BaseModel
from typing import Optional, List

class MemberOut(BaseModel):
    id: uuid.UUID
    first_name: str
    last_name: str
    photo: Optional[str]
    birth_date: date
    field_of_study: str
    nickname: Optional[str]
    current_job: str
    interests: List[str]
    skills: List[str]
    personality_traits: List[str]
    curses_given: Optional[int]
    debts: Optional[float]
    credits: Optional[float]
    group_role: str
    recommended_movie: Optional[str]
    recommended_music: Optional[str]
    recommended_book: Optional[str]
    recommended_game: Optional[str]
    motto: Optional[str]

    class Config:
        orm_mode = True

