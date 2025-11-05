from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# SQLite database path
SQLALCHEMY_DATABASE_URL = "sqlite:///./customer_contracts.db"

# Create engine with check_same_thread=False for SQLite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models
Base = declarative_base()


def get_db():
    """Dependency for getting database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables"""
    # Import all models to ensure they are registered with Base
    from models.customer import Customer  # noqa
    from models.contract import Contract  # noqa
    from models.event import Event  # noqa
    from models.note import Note  # noqa
    from models.action import Action  # noqa
    
    Base.metadata.create_all(bind=engine)
