from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from models import get_db, Action, Contract
from schemas import ActionCreate, ActionResponse

router = APIRouter(
    prefix="/actions",
    tags=["actions"]
)


@router.post("/", response_model=ActionResponse, status_code=201)
def create_action(
    action: ActionCreate,
    db: Session = Depends(get_db)
):
    """Create a new action"""
    # Check if contract exists
    contract = db.query(Contract).filter(Contract.contract_id == action.contract_id).first()
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    
    # Capture prior status
    prior_status = contract.status
    
    # Create action
    db_action = Action(
        contract_id=action.contract_id,
        action_type=action.action_type,
        action_note=action.action_note,
        acted_by=action.acted_by,
        prior_status=prior_status
    )
    
    # Update contract status based on action type
    if action.action_type == "approve":
        contract.status = "Approved"
        db_action.new_status = "Approved"
    elif action.action_type == "reject":
        contract.status = "Rejected"
        db_action.new_status = "Rejected"
    elif action.action_type == "reopen":
        contract.status = "Pending Approval"
        db_action.new_status = "Pending Approval"
    
    db.add(db_action)
    db.commit()
    db.refresh(db_action)
    return db_action


@router.get("/", response_model=List[ActionResponse])
def get_actions(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    contract_id: int = Query(None),
    action_type: str = Query(None),
    db: Session = Depends(get_db)
):
    """Get all actions with optional filtering"""
    query = db.query(Action)
    
    if contract_id:
        query = query.filter(Action.contract_id == contract_id)
    if action_type:
        query = query.filter(Action.action_type == action_type)
    
    actions = query.order_by(Action.acted_at.desc()).offset(skip).limit(limit).all()
    return actions


@router.get("/{action_id}", response_model=ActionResponse)
def get_action(
    action_id: int,
    db: Session = Depends(get_db)
):
    """Get an action by ID"""
    action = db.query(Action).filter(Action.action_id == action_id).first()
    if not action:
        raise HTTPException(status_code=404, detail="Action not found")
    return action


@router.delete("/{action_id}", status_code=204)
def delete_action(
    action_id: int,
    db: Session = Depends(get_db)
):
    """Delete an action"""
    action = db.query(Action).filter(Action.action_id == action_id).first()
    if not action:
        raise HTTPException(status_code=404, detail="Action not found")
    
    db.delete(action)
    db.commit()
    return None
