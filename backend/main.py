from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import (
    customers_router,
    contracts_router,
    events_router,
    notes_router,
    actions_router
)
from models.database import init_db

# Initialize database
init_db()

app = FastAPI(
    title="Customer Contract Management Portal API",
    description="Internal portal for managing customer contracts and event logs",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(customers_router)
app.include_router(contracts_router)
app.include_router(events_router)
app.include_router(notes_router)
app.include_router(actions_router)


@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "Customer Contract Management Portal API",
        "version": "1.0.0"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)