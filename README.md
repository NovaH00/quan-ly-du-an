# Project Management Dashboard

This application aggregates data from multiple project sheets into a central management sheet in Google Sheets.

## Prerequisites

- Python 3.12 or higher
- Google API credentials
- `uv` package manager (or pip)

## Installation

1. Clone the repository
2. Install dependencies using uv:
   ```bash
   uv sync
   ```

## Configuration

Create a `.env` file with the following variables:

```bash
GOOGLE_SHEET_ID=your_google_sheet_id_here
CREDENTIALS=credentials.json
UPDATE_INTERVAL=10
MANAGEMENT_SHEET_NAME=Quản Lý
```

## Usage

Run the application with:

```bash
uv run main.py
```

## Docker Usage

The application can also be run using Docker:

1. Build and run with Docker Compose:
   ```bash
   docker-compose up -d
   ```

2. Or build and run with Docker:
   ```bash
   # Build the image
   docker build -t project-dashboard .
   
   # Run the container
   docker run -d --env-file .env --name project-dashboard project-dashboard
   ```

See the [Docker-README.md](Docker-README.md) file for detailed Docker instructions.