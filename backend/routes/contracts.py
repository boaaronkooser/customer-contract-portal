from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from models import get_db, Contract, Customer
from schemas import ContractCreate, ContractUpdate, ContractResponse

router = APIRouter(
    prefix="/contracts",
    tags=["contracts"]
)


@router.post("/", response_model=ContractResponse, status_code=201)
def create_contract(
    contract: ContractCreate,
    db: Session = Depends(get_db)
):
    """Create a new contract"""
    # Check if customer exists
    customer = db.query(Customer).filter(Customer.customer_id == contract.customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    db_contract = Contract(**contract.model_dump())
    db.add(db_contract)
    db.commit()
    db.refresh(db_contract)
    return db_contract


@router.get("/", response_model=List[ContractResponse])
def get_contracts(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    customer_id: int = Query(None),
    status: str = Query(None),
    db: Session = Depends(get_db)
):
    """Get all contracts with optional filtering"""
    query = db.query(Contract)
    
    if customer_id:
        query = query.filter(Contract.customer_id == customer_id)
    if status:
        query = query.filter(Contract.status == status)
    
    contracts = query.offset(skip).limit(limit).all()
    return contracts


@router.get("/{contract_id}", response_model=ContractResponse)
def get_contract(
    contract_id: int,
    db: Session = Depends(get_db)
):
    """Get a contract by ID"""
    contract = db.query(Contract).filter(Contract.contract_id == contract_id).first()
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    return contract


@router.put("/{contract_id}", response_model=ContractResponse)
def update_contract(
    contract_id: int,
    contract_update: ContractUpdate,
    db: Session = Depends(get_db)
):
    """Update a contract"""
    contract = db.query(Contract).filter(Contract.contract_id == contract_id).first()
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    
    update_data = contract_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(contract, field, value)
    
    db.commit()
    db.refresh(contract)
    return contract


@router.delete("/{contract_id}", status_code=204)
def delete_contract(
    contract_id: int,
    db: Session = Depends(get_db)
):
    """Delete a contract"""
    contract = db.query(Contract).filter(Contract.contract_id == contract_id).first()
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    
    db.delete(contract)
    db.commit()
    return None
