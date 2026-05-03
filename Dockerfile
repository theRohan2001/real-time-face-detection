FROM python:3.12-slim

WORKDIR /app

# Install system dependencies for build (if any needed for Pillow/MediaPipe)
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Install uv for fast dependency management
RUN pip install uv

# Copy pyproject.toml and lockfile if using uv
COPY pyproject.toml ./ 

# Create virtual env and install dependencies directly
RUN uv venv --python 3.12 && uv add Pillow mediapipe sqlalchemy "uvicorn[standard]" fastapi pydantic

# Explicitly ensure the app uses the venv python
ENV PATH="/app/.venv/bin:$PATH"

COPY . .

# Expose port
EXPOSE 8000

# Start app using uvicorn from the venv
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
