# Database Schema

## Tables

### users
| Column | Type | Description |
|--------|------|-------------|
| id | UUID (PK) | Unique identifier |
| email | String (Unique) | User email |
| password_hash | String | Hashed password |
| created_at | Timestamp | Record creation time |

### routes
| Column | Type | Description |
|--------|------|-------------|
| id | UUID (PK) | Unique identifier |
| source_port | String | Name/ID of source port |
| destination_port | String | Name/ID of destination port |
| distance | Float | Total distance in nautical miles |
| eta | Float | Estimated time of arrival in days |
| risk_score | Int | Calculated risk score (0-100) |
| geometry | JSONB/GeoJSON | The path coordinates |
| created_at | Timestamp | Record creation time |

### route_history
| Column | Type | Description |
|--------|------|-------------|
| id | UUID (PK) | Unique identifier |
| user_id | UUID (FK) | Reference to users.id |
| route_id | UUID (FK) | Reference to routes.id |
| created_at | Timestamp | Record creation time |
