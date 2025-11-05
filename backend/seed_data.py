"""
Seed data script for populating the database with fake data using Faker.
"""
from faker import Faker
from datetime import datetime
import random
from sqlalchemy.orm import Session

from models.database import SessionLocal, engine
from models.customer import Customer
from models.contract import Contract
from models.event import Event
from models.database import Base

# Initialize Faker
fake = Faker()

# Initialize database tables
Base.metadata.create_all(bind=engine)


def seed_customers(db: Session, count: int = 5):
    """Create fake customers"""
    customers = []
    segments = ["Retail", "Corporate", "SME", "Enterprise", "Government"]
    risk_levels = ["Low", "Medium", "High"]
    statuses = ["Active", "Inactive", "Pending"]
    
    for _ in range(count):
        customer = Customer(
            name=fake.company() if random.choice([True, False]) else fake.name(),
            email=fake.unique.email(),
            phone=fake.phone_number()[:20],  # Limit to 20 chars
            segment=random.choice(segments),
            risk_level=random.choice(risk_levels),
            status=random.choice(statuses)
        )
        db.add(customer)
        customers.append(customer)
    
    db.commit()
    return customers


def seed_contracts(db: Session, customers: list, count: int = 10):
    """Create fake contracts for customers"""
    contracts = []
    contract_types = ["Service Agreement", "License Agreement", "Maintenance Contract", 
                     "Support Contract", "NDA", "Purchase Agreement", "SLA"]
    contract_statuses = ["Draft", "Pending Approval", "Approved", "Rejected", "Active", "Expired"]
    users = ["admin", "john.doe", "jane.smith", "manager", "sales.rep"]
    
    for _ in range(count):
        customer = random.choice(customers)
        effective_date = fake.date_time_between(start_date="-2y", end_date="now")
        expiration_date = None
        if random.choice([True, False]):  # 50% chance of having expiration date
            expiration_date = fake.date_time_between(start_date=effective_date, end_date="+2y")
        
        contract = Contract(
            customer_id=customer.customer_id,
            type=random.choice(contract_types),
            status=random.choice(contract_statuses),
            effective_date=effective_date,
            expiration_date=expiration_date,
            terms_ref=fake.url() if random.choice([True, False]) else None,
            attachments_ref=fake.file_path(depth=2) if random.choice([True, False]) else None,
            created_by=random.choice(users),
            updated_by=random.choice(users),
            last_action_at=fake.date_time_between(start_date=effective_date, end_date="now") if random.choice([True, False]) else None
        )
        db.add(contract)
        contracts.append(contract)
    
    db.commit()
    return contracts


def seed_events(db: Session, customers: list, count: int = 20):
    """Create fake events for customers"""
    events = []
    event_types = ["Login", "Logout", "Password Reset", "Contract View", "Contract Download",
                  "Profile Update", "Payment", "Contract Sign", "Document Upload", "Query"]
    channels = ["Web", "Mobile", "API"]
    
    for _ in range(count):
        customer = random.choice(customers)
        timestamp = fake.date_time_between(start_date="-1y", end_date="now")
        
        event = Event(
            customer_id=customer.customer_id,
            event_type=random.choice(event_types),
            timestamp=timestamp,
            channel=random.choice(channels),
            ip_address=fake.ipv4() if random.choice([True, False]) else None,
            user_agent=fake.user_agent() if random.choice([True, False]) else None,
            metadata_json={"action": fake.word(), "result": fake.word(), "details": fake.sentence()} if random.choice([True, False]) else None,
            correlation_id=fake.uuid4() if random.choice([True, False]) else None
        )
        db.add(event)
        events.append(event)
    
    db.commit()
    return events


def main():
    """Main function to seed the database"""
    db: Session = SessionLocal()
    
    try:
        # Clear existing data (optional - comment out if you want to keep existing data)
        # db.query(Event).delete()
        # db.query(Contract).delete()
        # db.query(Customer).delete()
        # db.commit()
        
        # Seed data
        print("Creating customers...")
        customers = seed_customers(db, count=5)
        
        print("Creating contracts...")
        contracts = seed_contracts(db, customers, count=10)
        
        print("Creating events...")
        events = seed_events(db, customers, count=20)
        
        print("Seed data inserted")
        
    except Exception as e:
        print(f"Error seeding data: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()

