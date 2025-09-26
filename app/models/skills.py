from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from app.models import member_skill, gen_uuid_str
from app.db import Base

class Skill(Base):
    __tablename__ = "skills"
    id = Column(String(36), primary_key=True, default=gen_uuid_str, index=True)
    name = Column(String(255), nullable=False, unique=True, index=True)
    members = relationship("Member", secondary=member_skill, back_populates="skills")

