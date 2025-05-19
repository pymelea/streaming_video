# Infrastructure Setup

## Database
This project uses PostgreSQL as the primary database. 

### Docker Compose
To start the database:
```bash
docker-compose up -d
```

### Environment Variables
- Database Name: `streamdb`
- Database User: `streamuser`
- Database Password: `streampassword`

## Running the Application
1. Ensure Docker and Docker Compose are installed
2. Run `docker-compose up` to start services
3. The database will be accessible on port 5432
