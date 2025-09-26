from sqlalchemy import Table, String, Column, ForeignKey, UniqueConstraint, Integer, Float, Date
from sqlalchemy.orm import relationship
from app.models import gen_uuid_str
from app.db import Base


member_interest = Table(
    "member_interests",
    Base.metadata,
    Column("member_id", String(36), ForeignKey("members.id", ondelete="CASCADE"), primary_key=True),
    Column("interest_id", String(36), ForeignKey("interests.id", ondelete="CASCADE"), primary_key=True),
    UniqueConstraint("member_id", "interest_id"),
)

member_skill = Table(
    "member_skills",
    Base.metadata,
    Column("member_id", String(36), ForeignKey("members.id", ondelete="CASCADE"), primary_key=True),
    Column("skill_id", String(36), ForeignKey("skills.id", ondelete="CASCADE"), primary_key=True),
    UniqueConstraint("member_id", "skill_id"),
)

member_trait = Table(
    "member_traits",
    Base.metadata,
    Column("member_id", String(36), ForeignKey("members.id", ondelete="CASCADE"), primary_key=True),
    Column("trait_id", String(36), ForeignKey("traits.id", ondelete="CASCADE"), primary_key=True),
    UniqueConstraint("member_id", "trait_id"),
)


class Member(Base):
    __tablename__ = "members"
    id = Column(String(36), primary_key=True, default=gen_uuid_str, index=True)
    first_name = Column(String(150), nullable=False)
    last_name = Column(String(150), nullable=False)
    photo = Column(String, nullable=True)
    birth_date = Column(Date, nullable=False)
    field_of_study = Column(String(255), nullable=False)
    nickname = Column(String(150), nullable=True)
    current_job = Column(String(255), nullable=False)
    curses_given = Column(Integer, nullable=True, default=0)
    debts = Column(Float, nullable=True, default=0.0)
    credits = Column(Float, nullable=True, default=0.0)
    group_role = Column(String(255), nullable=False)
    recommended_movie = Column(String, nullable=True)
    recommended_music = Column(String, nullable=True)
    recommended_book = Column(String, nullable=True)
    recommended_game = Column(String, nullable=True)
    motto = Column(String, nullable=True)

    # relationships (normalized)
    interests = relationship("Interest", secondary=member_interest, back_populates="members")
    skills = relationship("Skill", secondary=member_skill, back_populates="members")
    personality_traits = relationship("Trait", secondary=member_trait, back_populates="members")

