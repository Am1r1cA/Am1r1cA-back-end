from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from app.models import gen_uuid_str, member_trait
from app.db import Base

class Trait(Base):
    __tablename__ = "traits"
    id = Column(String(36), primary_key=True, default=gen_uuid_str, index=True)
    name = Column(String(255), nullable=False, unique=True, index=True)
    members = relationship("Member", secondary=member_trait, back_populates="personality_traits")

