from typing import Optional
from sqlalchemy.orm import Session
import models
import schemas

def get_candidates(db: Session, status: Optional[str] = None):
    query = db.query(models.Candidate)
    if status is not None:
        query = query.filter(models.Candidate.status == status)
    return query.order_by(models.Candidate.created_at.desc()).all()

def get_candidate(db: Session, candidate_id: int):
    return db.query(models.Candidate).filter(models.Candidate.id == candidate_id).first()

def create_candidate(db: Session, candidate: schemas.CandidateCreate):
    db_candidate = models.Candidate(
        name=candidate.name,
        email=candidate.email,
        skill=candidate.skill,
        status=candidate.status,
    )
    db.add(db_candidate)
    db.commit()
    db.refresh(db_candidate)
    return db_candidate

def update_candidate_status(db: Session, candidate_id: int, status_update: schemas.CandidateUpdate):
    db_candidate = get_candidate(db, candidate_id)
    if db_candidate:
        db_candidate.status = status_update.status
        db.commit()
        db.refresh(db_candidate)
    return db_candidate
