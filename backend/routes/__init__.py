from routes.customers import router as customers_router
from routes.contracts import router as contracts_router
from routes.events import router as events_router
from routes.notes import router as notes_router
from routes.actions import router as actions_router

__all__ = [
    "customers_router",
    "contracts_router",
    "events_router",
    "notes_router",
    "actions_router",
]
