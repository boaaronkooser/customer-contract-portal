from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from models import get_db, Event, Customer
from schemas import EventCreate, EventResponse

router = APIRouter(
    prefix="/events",
    tags=["events"]
)


@router.post("/", response_model=EventResponse, status_code=201)
def create_event(
    event: EventCreate,
    db: Session = Depends(get_db)
):
    """Create a new event"""
    # Check if customer exists
    customer = db.query(Customer).filter(Customer.customer_id == event.customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    db_event = Event(**event.model_dump())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


@router.get("/", response_model=List[EventResponse])
def get_events(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    customer_id: int = Query(None),
    event_type: str = Query(None),
    start_date: datetime = Query(None),
    end_date: datetime = Query(None),
    db: Session = Depends(get_db)
):
    """Get all events with optional filtering"""
    query = db.query(Event)
    
    if customer_id:
        query = query.filter(Event.customer_id == customer_id)
    if event_type:
        query = query.filter(Event.event_type == event_type)
    if start_date:
        query = query.filter(Event.timestamp >= start_date)
    if end_date:
        query = query.filter(Event.timestamp <= end_date)
    
    events = query.order_by(Event.timestamp.desc()).offset(skip).limit(limit).all()
    return events


@router.get("/{event_id}", response_model=EventResponse)
def get_event(
    event_id: int,
    db: Session = Depends(get_db)
):
    """Get an event by ID"""
    event = db.query(Event).filter(Event.event_id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@router.delete("/{event_id}", status_code=204)
def delete_event(
    event_id: int,
    db: Session = Depends(get_db)
):
    """Delete an event"""
    event = db.query(Event).filter(Event.event_id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    db.delete(event)
    db.commit()
    return None
