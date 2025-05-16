FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/root/.local/bin:$PATH"

ENV APP_HOST="0.0.0.0"
# Set working directory
WORKDIR /app

# Install curl and build tools
RUN apt-get update && apt-get install -y curl build-essential

# Copy project dependency files
COPY pyproject.toml uv.lock ./

# Install uv and use it to install dependencies
RUN curl -Ls https://astral.sh/uv/install.sh | sh && \
    uv pip install --system --no-deps .

# Copy project files
COPY . .

# Expose port
EXPOSE 5000

# Run the Flask app using uv
CMD ["uv", "run", "run.py"]
