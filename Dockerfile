# Use Python 3.12 as base image (matches your pyproject.toml requirement)
FROM python:3.12-slim

# Install uv package manager
RUN pip install --no-cache-dir uv

# Set working directory
WORKDIR /app

# Copy project files
COPY pyproject.toml uv.lock ./
COPY src ./src
COPY main.py ./
COPY credentials.json ./ 2>/dev/null || true  # Optional copy, won't fail if file doesn't exist
COPY .env ./ 2>/dev/null || true  # Optional copy, won't fail if file doesn't exist

# Install project dependencies using uv
RUN uv sync --no-dev

# Create a non-root user for security
RUN useradd --create-home --shell /bin/bash app
USER app
WORKDIR /home/app

# Copy the project to the user's home
COPY --chown=app:app . /home/app/

# Switch to the virtual environment
ENV PATH="/app/.venv/bin:$PATH"

# Expose a port (though this is a background service, so it's for convention)
EXPOSE 8000

# Run the application
CMD ["uv", "run", "main.py"]