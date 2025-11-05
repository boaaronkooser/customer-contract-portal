# Customer Contract Management Portal - Backend

FastAPI backend for the Customer Contract Management Portal.

## Architecture

### Models (SQLAlchemy)
- **Customer**: Customer master data with segments and risk levels
- **Contract**: Contracts linked to customers with lifecycle states
- **Event**: Customer activity event logs
- **Note**: Comments on contracts with threading support
- **Action**: Contract lifecycle actions (approve, reject, etc.)

### Relationships
- Customer 1:N Contracts
- Customer 1:N Events  
- Contract 1:N Notes
- Contract 1:N Actions
- Notes self-referencing (parent-child for threading)

### Schemas (Pydantic)
Pydantic schemas for request/response validation:
- CustomerCreate, CustomerUpdate, CustomerResponse
- ContractCreate, ContractUpdate, ContractResponse
- EventCreate, EventResponse
- NoteCreate, NoteUpdate, NoteResponse
- ActionCreate, ActionResponse

### Routers (CRUD Operations)

#### `/customers`
- `POST /` - Create customer
- `GET /` - List customers (paginated)
- `GET /{customer_id}` - Get customer by ID
- `PUT /{customer_id}` - Update customer
- `DELETE /{customer_id}` - Delete customer

#### `/contracts`
- `POST /` - Create contract
- `GET /` - List contracts (paginated, with filters)
- `GET /{contract_id}` - Get contract by ID
- `PUT /{contract_id}` - Update contract
- `DELETE /{contract_id}` - Delete contract

#### `/events`
- `POST /` - Create event
- `GET /` - List events (paginated, with filters)
- `GET /{event_id}` - Get event by ID
- `DELETE /{event_id}` - Delete event

#### `/notes`
- `POST /` - Create note/comment
- `GET /` - List notes (paginated, with filters)
- `GET /{note_id}` - Get note by ID
- `PUT /{note_id}` - Update note
- `DELETE /{note_id}` - Delete note

#### `/actions`
- `POST /` - Create action (automatically updates contract status)
- `GET /` - List actions (paginated, with filters)
- `GET /{action_id}` - Get action by ID
- `DELETE /{action_id}` - Delete action

## Setup

1. Activate virtual environment:
```bash
.\venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the server:
```bash
python -m uvicorn main:app --reload
```

Or directly:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

## API Documentation

- Interactive API docs: `http://localhost:8000/docs` (Swagger UI)
- Alternative docs: `http://localhost:8000/redoc` (ReDoc)
- OpenAPI schema: `http://localhost:8000/openapi.json`

## Database

- SQLite database at `./customer_contracts.db`
- Tables are automatically created on first run via `init_db()`
- All foreign key relationships are enforced

## Features

- **Pagination**: All list endpoints support `skip` and `limit` parameters
- **Filtering**: Contracts, Events, and Actions support filtering by various fields
- **Validation**: All inputs validated using Pydantic schemas
- **Error Handling**: Proper HTTP status codes and error messages
- **CORS**: Configured for cross-origin requests
- **Audit Trail**: All contract actions track prior and new status

## State Machine (Contracts)

Contract status transitions through actions:
- **Draft** → Pending Approval (created)
- **Pending Approval** → Approved (approve action)
- **Pending Approval** → Rejected (reject action)
- **Approved/Rejected** → Pending Approval (reopen action)

## Notes/Comments Threading

Notes support parent-child relationships for threaded discussions:
- Set `parent_comment_id` when creating a reply
- Replies are tracked in the database

## Best Practices Implemented

1. Separation of concerns (models, schemas, routes)
2. Dependency injection for database sessions
3. Proper HTTP status codes
4. Input validation with Pydantic
5. Database relationships with cascade deletes
6. Timestamps on all models
7. Consistent error handling


