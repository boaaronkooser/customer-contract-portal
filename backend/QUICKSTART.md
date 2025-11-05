# Quick Start Guide

## Starting the Server

1. Navigate to the backend directory:
```bash
cd backend
```

2. Activate the virtual environment:
```bash
# On Windows
.\venv\Scripts\activate

# On Linux/Mac
source venv/bin/activate
```

3. Install dependencies (if not already done):
```bash
pip install -r requirements.txt
```

4. Start the server:
```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload
```

The API will be available at: `http://localhost:8000`

## API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## Example API Calls

### Create a Customer
```bash
POST http://localhost:8000/customers
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john.doe@example.com",
  "phone": "1234567890",
  "segment": "Retail",
  "risk_level": "Low"
}
```

### Create a Contract
```bash
POST http://localhost:8000/contracts
Content-Type: application/json

{
  "customer_id": 1,
  "type": "Loan Agreement",
  "status": "Draft",
  "effective_date": "2024-01-01T00:00:00",
  "expiration_date": "2025-01-01T00:00:00",
  "created_by": "admin",
  "updated_by": "admin"
}
```

### Create an Event
```bash
POST http://localhost:8000/events
Content-Type: application/json

{
  "customer_id": 1,
  "event_type": "Login",
  "channel": "Web",
  "ip_address": "192.168.1.1"
}
```

### Create a Note (Comment)
```bash
POST http://localhost:8000/notes
Content-Type: application/json

{
  "contract_id": 1,
  "body": "This contract requires review",
  "created_by": "analyst1"
}
```

### Create an Action
```bash
POST http://localhost:8000/actions
Content-Type: application/json

{
  "contract_id": 1,
  "action_type": "approve",
  "action_note": "Contract reviewed and approved",
  "acted_by": "approver1"
}
```

## Using cURL (Windows PowerShell)

For Windows users, you can use PowerShell's `Invoke-RestMethod`:

```powershell
# Create customer
$body = @{
    name = "John Doe"
    email = "john.doe@example.com"
    phone = "1234567890"
    segment = "Retail"
    risk_level = "Low"
} | ConvertTo-Json

Invoke-RestMethod -Uri http://localhost:8000/customers -Method POST -Body $body -ContentType "application/json"
```

## Database

The SQLite database file `customer_contracts.db` is automatically created in the backend directory when the server starts.

To reset the database:
1. Stop the server
2. Delete `customer_contracts.db`
3. Restart the server

## Testing

The best way to test the API is using the interactive Swagger UI at http://localhost:8000/docs. It allows you to:
- View all available endpoints
- See request/response schemas
- Test endpoints directly from the browser
- View example payloads



