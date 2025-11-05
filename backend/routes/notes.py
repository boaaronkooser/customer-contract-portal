from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from models import get_db, Note, Contract
from schemas import NoteCreate, NoteUpdate, NoteResponse

router = APIRouter(
    prefix="/notes",
    tags=["notes"]
)


@router.post("/", response_model=NoteResponse, status_code=201)
def create_note(
    note: NoteCreate,
    db: Session = Depends(get_db)
):
    """Create a new note"""
    # Check if contract exists
    contract = db.query(Contract).filter(Contract.contract_id == note.contract_id).first()
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    
    # If parent_comment_id is provided, check if it exists
    if note.parent_comment_id:
        parent = db.query(Note).filter(Note.note_id == note.parent_comment_id).first()
        if not parent:
            raise HTTPException(status_code=404, detail="Parent comment not found")
    
    db_note = Note(**note.model_dump())
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


@router.get("/", response_model=List[NoteResponse])
def get_notes(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    contract_id: int = Query(None),
    db: Session = Depends(get_db)
):
    """Get all notes with optional filtering"""
    query = db.query(Note)
    
    if contract_id:
        query = query.filter(Note.contract_id == contract_id)
    
    notes = query.order_by(Note.created_at.desc()).offset(skip).limit(limit).all()
    return notes


@router.get("/{note_id}", response_model=NoteResponse)
def get_note(
    note_id: int,
    db: Session = Depends(get_db)
):
    """Get a note by ID"""
    note = db.query(Note).filter(Note.note_id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.put("/{note_id}", response_model=NoteResponse)
def update_note(
    note_id: int,
    note_update: NoteUpdate,
    db: Session = Depends(get_db)
):
    """Update a note"""
    note = db.query(Note).filter(Note.note_id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    update_data = note_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(note, field, value)
    
    note.edited_at = datetime.now()
    db.commit()
    db.refresh(note)
    return note


@router.delete("/{note_id}", status_code=204)
def delete_note(
    note_id: int,
    db: Session = Depends(get_db)
):
    """Delete a note"""
    note = db.query(Note).filter(Note.note_id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    db.delete(note)
    db.commit()
    return None
