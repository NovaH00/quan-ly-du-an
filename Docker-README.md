# Docker Setup for Project Management Dashboard

This project can be run using Docker and Docker Compose. Follow these instructions to set up and run the application.

## Prerequisites

- Docker
- Docker Compose
- A `credentials.json` file with Google API credentials
- Environment variables set in a `.env` file

## Setup

1. Make sure you have the following files in your project root:
   - `credentials.json` - Google API credentials file
   - `.env` - Environment variables file

2. Example `.env` file content:
   ```bash
   GOOGLE_SHEET_ID=your_google_sheet_id_here
   CREDENTIALS=credentials.json
   UPDATE_INTERVAL=10
   MANAGEMENT_SHEET_NAME=Quản Lý
   ```

## Running the Application

### Using Docker Compose (Recommended)

```bash
# Build and start the service
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the service
docker-compose down
```

### Using Docker

```bash
# Build the image
docker build -t project-dashboard .

# Run the container
docker run -d \
  --name project-dashboard \
  --env-file .env \
  -v $(pwd)/credentials.json:/app/credentials.json:ro \
  project-dashboard
```

## Environment Variables

- `GOOGLE_SHEET_ID` (required): The ID of your Google Sheet
- `CREDENTIALS` (optional): Path to credentials file (default: credentials.json)
- `UPDATE_INTERVAL` (optional): Update interval in seconds (default: 10)
- `MANAGEMENT_SHEET_NAME` (optional): Name of the management sheet (default: "Quản Lý")

## Volumes

The Docker setup mounts:
- `credentials.json` as read-only for authentication
- `.env` file to provide environment variables to the container