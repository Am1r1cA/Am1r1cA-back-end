from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.schemas import MembersList, MemberOut, MemberCreate, MemberUpdate
from app.db import get_session, member_to_dict, get_or_create_by_name
from app.models import User, Member, Interest, Skill, Trait
from app.api_v1 import get_current_user

router = APIRouter(
    prefix="/api/v1/members",
    tags=["Members"]
)

@router.get("", response_model=MembersList)
def list_members(limit: int = 50, offset: int = 0, db: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    if limit < 0 or offset < 0:
        raise HTTPException(status_code=400, detail={"error": "limit and offset must be non-negative integers"})
    members = db.execute(select(Member).order_by(Member.last_name, Member.first_name).offset(offset).limit(limit)).scalars().all()
    payload = [member_to_dict(m) for m in members]
    return {"members": payload}


@router.get("/{member_id}", response_model=MemberOut)
def get_member(member_id: str, db: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    m = db.execute(select(Member).filter_by(id=member_id)).scalar_one_or_none()
    if not m:
        raise HTTPException(status_code=404, detail={"error": "Member not found"})
    return member_to_dict(m)


@router.post("", response_model=MemberOut, status_code=201)
def create_member(req: MemberCreate, db: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    member = Member(
        first_name=req.first_name,
        last_name=req.last_name,
        photo=req.photo,
        birth_date=req.birth_date,
        field_of_study=req.field_of_study,
        nickname=req.nickname,
        current_job=req.current_job,
        curses_given=req.curses_given or 0,
        debts=req.debts or 0.0,
        credits=req.credits or 0.0,
        group_role=req.group_role,
        recommended_movie=req.recommended_movie,
        recommended_music=req.recommended_music,
        recommended_book=req.recommended_book,
        recommended_game=req.recommended_game,
        motto=req.motto,
    )
    db.add(member)
    db.commit()
    db.refresh(member)

    for name in req.interests or []:
        inst = get_or_create_by_name(db, Interest, name)
        if inst and inst not in member.interests:
            member.interests.append(inst)
    for name in req.skills or []:
        inst = get_or_create_by_name(db, Skill, name)
        if inst and inst not in member.skills:
            member.skills.append(inst)
    for name in req.personality_traits or []:
        inst = get_or_create_by_name(db, Trait, name)
        if inst and inst not in member.personality_traits:
            member.personality_traits.append(inst)

    db.add(member)
    db.commit()
    db.refresh(member)
    return member_to_dict(member)


@router.put("/{member_id}", response_model=MemberOut)
def update_member(member_id: str, updates: MemberUpdate, db: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    m = db.execute(select(Member).filter_by(id=member_id)).scalar_one_or_none()
    if not m:
        raise HTTPException(status_code=404, detail={"error": "Member not found"})

    data = updates.dict(exclude_unset=True)
    # update scalar fields
    scalar_fields = {"first_name", "last_name", "photo", "birth_date", "field_of_study", "nickname",
                     "current_job", "curses_given", "debts", "credits", "group_role",
                     "recommended_movie", "recommended_music", "recommended_book", "recommended_game", "motto"}
    for k, v in data.items():
        if k in scalar_fields:
            setattr(m, k, v)

    if "interests" in data:
        m.interests.clear()
        for name in data.get("interests") or []:
            inst = get_or_create_by_name(db, Interest, name)
            if inst:
                m.interests.append(inst)

    if "skills" in data:
        m.skills.clear()
        for name in data.get("skills") or []:
            inst = get_or_create_by_name(db, Skill, name)
            if inst:
                m.skills.append(inst)

    if "personality_traits" in data:
        m.personality_traits.clear()
        for name in data.get("personality_traits") or []:
            inst = get_or_create_by_name(db, Trait, name)
            if inst:
                m.personality_traits.append(inst)

    db.add(m)
    db.commit()
    db.refresh(m)
    return member_to_dict(m)


@router.delete("/{member_id}", status_code=204)
def delete_member(member_id: str, db: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    m = db.execute(select(Member).filter_by(id=member_id)).scalar_one_or_none()
    if not m:
        raise HTTPException(status_code=404, detail={"error": "Member not found"})
    db.delete(m)
    db.commit()
    return None

