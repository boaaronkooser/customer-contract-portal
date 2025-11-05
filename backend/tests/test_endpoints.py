import sys
from pathlib import Path

# Add parent directory to Python path for imports
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from models.database import Base, get_db
from models.customer import Customer
from models.contract import Contract
from models.event import Event
from models.note import Note  # Import to ensure table is created
from models.action import Action  # Import to ensure table is created
from datetime import datetime


# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_customer_contracts.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database for each test"""
    # Drop all tables and create new ones
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Clean up after test
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def override_get_db(db_session):
    """Override the get_db dependency"""
    def _get_db():
        try:
            yield db_session
        finally:
            pass
    app.dependency_overrides[get_db] = _get_db
    yield
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def client(override_get_db):
    """Create async test client with overridden database dependency"""
    transport = ASGITransport(app=app)
    async_client = AsyncClient(transport=transport, base_url="http://test", follow_redirects=True)
    try:
        yield async_client
    finally:
        await async_client.aclose()


@pytest.fixture(scope="function")
def sample_customers(db_session):
    """Create sample customers for testing"""
    customers = [
        Customer(
            name="Test Company A",
            email="testa@example.com",
            phone="1234567890",
            segment="Enterprise",
            risk_level="Low",
            status="Active"
        ),
        Customer(
            name="Test Company B",
            email="testb@example.com",
            phone="0987654321",
            segment="Corporate",
            risk_level="Medium",
            status="Active"
        )
    ]
    for customer in customers:
        db_session.add(customer)
    db_session.commit()
    for customer in customers:
        db_session.refresh(customer)
    return customers


@pytest.fixture(scope="function")
def sample_contracts(db_session, sample_customers):
    """Create sample contracts for testing"""
    contracts = [
        Contract(
            customer_id=sample_customers[0].customer_id,
            type="Service Agreement",
            status="Approved",
            effective_date=datetime.now(),
            created_by="test_user",
            updated_by="test_user"
        ),
        Contract(
            customer_id=sample_customers[1].customer_id,
            type="License Agreement",
            status="Draft",
            effective_date=datetime.now(),
            created_by="test_user",
            updated_by="test_user"
        )
    ]
    for contract in contracts:
        db_session.add(contract)
    db_session.commit()
    for contract in contracts:
        db_session.refresh(contract)
    return contracts


@pytest.fixture(scope="function")
def sample_events(db_session, sample_customers):
    """Create sample events for testing"""
    events = [
        Event(
            customer_id=sample_customers[0].customer_id,
            event_type="Login",
            timestamp=datetime.now(),
            channel="Web"
        ),
        Event(
            customer_id=sample_customers[1].customer_id,
            event_type="Contract View",
            timestamp=datetime.now(),
            channel="API"
        )
    ]
    for event in events:
        db_session.add(event)
    db_session.commit()
    for event in events:
        db_session.refresh(event)
    return events


@pytest.mark.asyncio
async def test_get_customers_returns_200_and_non_empty_list(client, sample_customers):
    """Test that /customers returns 200 and a non-empty list"""
    response = await client.get("/customers")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    # Verify structure of customer response
    assert "customer_id" in data[0]
    assert "name" in data[0]
    assert "email" in data[0]


@pytest.mark.asyncio
async def test_get_contracts_returns_contracts_with_valid_customer_id(
    client, sample_customers, sample_contracts
):
    """Test that /contracts returns contracts with valid customer_id"""
    # Get all customers to verify their IDs
    customers_response = await client.get("/customers")
    assert customers_response.status_code == 200
    customers = customers_response.json()
    customer_ids = {customer["customer_id"] for customer in customers}
    
    # Get all contracts
    response = await client.get("/contracts")
    assert response.status_code == 200
    contracts = response.json()
    assert isinstance(contracts, list)
    assert len(contracts) > 0
    
    # Verify all contracts have valid customer_id
    for contract in contracts:
        assert "customer_id" in contract
        assert contract["customer_id"] in customer_ids, \
            f"Contract {contract.get('contract_id')} has invalid customer_id {contract['customer_id']}"


@pytest.mark.asyncio
async def test_get_events_returns_events_linked_to_existing_customers(
    client, sample_customers, sample_events
):
    """Test that /events returns events linked to existing customers"""
    # Get all customers to verify their IDs
    customers_response = await client.get("/customers")
    assert customers_response.status_code == 200
    customers = customers_response.json()
    customer_ids = {customer["customer_id"] for customer in customers}
    
    # Get all events
    response = await client.get("/events")
    assert response.status_code == 200
    events = response.json()
    assert isinstance(events, list)
    assert len(events) > 0
    
    # Verify all events are linked to existing customers
    for event in events:
        assert "customer_id" in event
        assert event["customer_id"] in customer_ids, \
            f"Event {event.get('event_id')} has invalid customer_id {event['customer_id']}"

