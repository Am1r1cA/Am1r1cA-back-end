from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from app.models import gen_uuid_str, member_interest
from app.db import Base

class Interest(Base):
    __tablename__ = "interests"
    id = Column(String(36), primary_key=True, default=gen_uuid_str, index=True)
    name = Column(String(255), nullable=False, unique=True, index=True)
    members = relationship("Member", secondary=member_interest, back_populates="interests")

