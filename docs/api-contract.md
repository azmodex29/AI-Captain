# API Contract

## Base URL
`https://api.aicaptain.com/v1` (Placeholder)

## Endpoints

### Authentication
- `POST /api/auth/register`: Create a new user account.
- `POST /api/auth/login`: Authenticate and receive a JWT.

### Ports
- `GET /api/ports`: Retrieve a list of available major world ports.

### Routes
- `POST /api/routes`: Generate a new maritime route between two ports.
  - Body: `{ "source_id": int, "destination_id": int }`
- `GET /api/routes/{id}`: Retrieve details of a specific previously calculated route.
- `GET /api/routes`: Retrieve history of routes for the authenticated user.

### Health
- `GET /health`: Check backend system status.
