from typing import Optional
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models
import schemas
import crud
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/candidates", response_model=schemas.CandidateResponse, status_code=status.HTTP_201_CREATED)
def create_candidate(candidate: schemas.CandidateCreate, db: Session = Depends(get_db)):
    return crud.create_candidate(db=db, candidate=candidate)

@app.get("/candidates", response_model=list[schemas.CandidateResponse])
def get_candidates(status: Optional[str] = None, db: Session = Depends(get_db)):
    return crud.get_candidates(db=db, status=status)

@app.put("/candidates/{candidate_id}/status", response_model=schemas.CandidateResponse)
def update_candidate_status(
    candidate_id: int, 
    status_update: schemas.CandidateUpdate, 
    db: Session = Depends(get_db)
):
    updated_candidate = crud.update_candidate_status(db=db, candidate_id=candidate_id, status_update=status_update)
    if updated_candidate is None:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return updated_candidate
