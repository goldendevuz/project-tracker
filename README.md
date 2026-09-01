# Project Timeline Tracker

A modern, full-stack project management system built with **FastAPI (DDD)**, **SQLAlchemy**, **PostgreSQL**, and **Docker Compose**.

## Features

✨ **Live Timeline View** - Real-time elapsed time calculation for projects
🎨 **Beautiful UI** - Dark tech aesthetic inspired by Neal.Fun
📊 **Admin Panel** - Full CRUD operations for project management
🏗️ **DDD Architecture** - Domain-Driven Design with FastAPI
🐳 **Docker Compose** - Multi-container setup with PostgreSQL, FastAPI, and Nginx
📝 **Alembic Migrations** - Version-controlled database schema
⚡ **Async/Await** - Built-in support for async operations

## Architecture

### Domain-Driven Design (DDD) Structure

```
backend/app/
├── domain/              # Core business logic
│   ├── entities.py     # Project entity
│   └── repositories.py # Repository interface
├── application/         # Use cases & services
│   ├── services.py     # ProjectService
│   └── dto.py          # Data Transfer Objects
├── infrastructure/      # Database & external services
│   ├── models.py       # SQLAlchemy models
│   ├── repositories.py # Repository implementation
│   └── db.py           # Database configuration
└── presentation/        # API endpoints
    └── routes.py       # FastAPI routes
```

## Technology Stack

- **Backend**: FastAPI + SQLAlchemy + Asyncpg
- **Database**: PostgreSQL 16
- **Migrations**: Alembic
- **Frontend**: Vanilla JavaScript + CSS
- **Server**: Nginx (reverse proxy)
- **Containerization**: Docker & Docker Compose

## Quick Start

### Prerequisites

- Docker & Docker Compose
- Make (optional, but recommended)

### Setup & Run

1. **Clone the repository**
   ```bash
   cd project-tracker
   ```

2. **Build and start services**
   ```bash
   make build
   make up
   ```

   Or without Make:
   ```bash
   docker-compose build
   docker-compose up -d
   ```

3. **Access the application**
   - **Frontend**: http://localhost
   - **Admin Panel**: http://localhost/admin
   - **API Docs**: http://localhost:8000/docs

4. **Run migrations (optional, auto-runs on startup)**
   ```bash
   make db-migrate
   ```

## API Endpoints

### Projects

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/projects/` | Get all projects |
| POST | `/api/projects/` | Create new project |
| GET | `/api/projects/{id}` | Get project by ID |
| PUT | `/api/projects/{id}` | Update project |
| DELETE | `/api/projects/{id}` | Delete project |
| PATCH | `/api/projects/{id}/status` | Change project status |

### Health Check

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | API health status |

## Example API Usage

### Create Project

```bash
curl -X POST http://localhost/api/projects/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "OpenDB",
    "description": "Open data API for Uzbekistan",
    "github_url": "https://github.com/goldendevuz/opendb",
    "color": "#00d4aa"
  }'
```

### Get All Projects

```bash
curl http://localhost/api/projects/
```

### Update Project

```bash
curl -X PUT http://localhost/api/projects/1 \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Updated description",
    "status": "completed"
  }'
```

### Change Status

```bash
curl -X PATCH http://localhost/api/projects/1/status \
  -H "Content-Type: application/json" \
  -d '{"status": "completed"}'
```

## Useful Commands

```bash
# View logs
make logs
make logs-backend
make logs-db

# Database operations
make db-migrate       # Run migrations
make db-downgrade     # Downgrade one migration
make shell            # Access backend shell

# Service management
make up               # Start services
make down             # Stop services
make restart          # Restart services
make clean            # Remove containers & volumes
make ps               # Show running containers
make status           # Check service status
```

## Project Structure

```
project-tracker/
├── backend/
│   ├── app/
│   │   ├── domain/
│   │   ├── application/
│   │   ├── infrastructure/
│   │   └── presentation/
│   ├── alembic/
│   │   └── versions/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── main.py
│   └── .env.example
├── frontend/
│   ├── index.html        # Timeline view
│   ├── admin.html        # Admin panel
│   ├── app.js            # Frontend logic
│   ├── admin.js          # Admin logic
│   └── style.css         # Styles
├── nginx/
│   └── nginx.conf
├── docker-compose.yml
├── Makefile
└── README.md
```

## Database Schema

### Projects Table

```sql
CREATE TABLE projects (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    description VARCHAR(1000),
    start_date DATETIME NOT NULL,
    github_url VARCHAR(500) NOT NULL,
    color VARCHAR(7) DEFAULT '#00d4aa',
    status ENUM('active', 'paused', 'completed', 'archived'),
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL
);
```

## DDD Principles Applied

### Domain Layer
- **Entities**: `Project` entity with business logic
- **Value Objects**: `ProjectStatus` enum
- **Repositories**: `ProjectRepository` interface (contract)
- **Pure Business Logic**: Methods like `get_elapsed_time()`, `update_github_url()`

### Application Layer
- **Services**: `ProjectService` orchestrates domain operations
- **DTOs**: Request/response data transfer objects
- **Use Cases**: Each service method represents a use case

### Infrastructure Layer
- **Repository Implementation**: SQLAlchemy-based `SQLAlchemyProjectRepository`
- **ORM Models**: Database models using SQLAlchemy
- **Database Configuration**: Connection pooling and session management

### Presentation Layer
- **API Routes**: FastAPI endpoints
- **Schema Validation**: Pydantic models for request/response validation

## Environment Variables

Create a `.env` file in the `backend/` directory:

```env
DATABASE_URL=postgresql+asyncpg://projectuser:projectpass@db:5432/projectdb
SQL_ECHO=false
```

## Troubleshooting

### Port Already in Use
```bash
# Change port in docker-compose.yml
# Or kill existing process
sudo lsof -i :80
sudo kill -9 <PID>
```

### Database Connection Error
```bash
# Check if database is ready
make logs-db

# Restart services
make restart
```

### Migration Issues
```bash
# Reset database
make clean
make up
```

## Performance Considerations

- **Async/Await**: All database operations are asynchronous
- **Connection Pooling**: SQLAlchemy NullPool for Asyncpg
- **Gzip Compression**: Nginx compresses responses
- **Static Files Caching**: 30-day cache for frontend assets

## Security Features

- CORS enabled for API access
- Input validation with Pydantic
- SQL injection protection via SQLAlchemy ORM
- No sensitive data in logs (SQL_ECHO=false)

## Future Enhancements

- [ ] User authentication & authorization
- [ ] Project categories/tags
- [ ] Milestone tracking
- [ ] Team collaboration features
- [ ] Analytics & statistics
- [ ] Export to CSV/PDF
- [ ] WebSocket for real-time updates

## License

MIT License

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Author

Abdulmajid - Backend Developer & Cybersecurity Enthusiast  
Tashkent, Uzbekistan

## Support

For issues or questions, open an issue on GitHub or contact via email.
