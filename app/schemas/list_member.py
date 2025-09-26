from typing import List
from pydantic import BaseModel
from app.schemas import MemberOut

class MembersList(BaseModel):
    members: List[MemberOut]
