# Setup & Deployment Guide

This guide details instructions for setting up the Swiggy Instamart AI Product Discovery Engine locally and deploying it to production hosting.

---

## 💻 Local Developer Setup

### Prerequisites
*   **Python**: Version 3.10 to 3.14.
*   **Package Manager**: `uv` is highly recommended for faster downloads and resolving dependency versions.

### 1. Installation
Clone/copy the workspace directory to your local drive and run:
```bash
cd swiggy_instamart_discovery

# Initialize a virtual environment
uv venv
source .venv/bin/activate  # On Linux/macOS
# OR on Windows PowerShell:
# .venv\Scripts\activate

# Install all requirements
uv pip install -r requirements.txt
```

### 2. Setting up Environment Variables (`.env`)
Create a `.env` file in the root directory. Copy the template from `.env.example`:
```env
# Database Path
DATABASE_PATH=data/database.db
CSV_PATH=data/instamart_feedback_1000.csv

# AI Agent Keys (Optional: Falls back to rule-based engine if blank)
GEMINI_API_KEY=your-gemini-api-key
OPENAI_API_KEY=your-openai-api-key

# Reddit Scraper Credentials (Optional)
REDDIT_CLIENT_ID=your-reddit-id
REDDIT_CLIENT_SECRET=your-reddit-secret
REDDIT_USER_AGENT=instamart-discovery-engine/0.1
```

### 3. Execution Commands
```bash
# Run the pipeline to collect and analyze 1,000 reviews
uv run python run.py --pipeline

# Run the Streamlit Dashboard locally
uv run python run.py --dashboard

# Run the FastAPI REST backend
uv run python run.py --api
```

---

## 🐳 Docker Deployment

The engine can be containerized using Docker to run the FastAPI backend and Streamlit dashboard together.

### 1. Create a `Dockerfile`
Create a `Dockerfile` in the root:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose ports for FastAPI (8000) and Streamlit (8501)
EXPOSE 8000
EXPOSE 8501

# Start script
CMD ["sh", "-c", "python run.py --pipeline && python run.py --api & streamlit run src/dashboard/app.py --server.port=8501 --server.address=0.0.0.0"]
```

### 2. Build and Run Container
```bash
docker build -t instamart-discovery-engine .
docker run -p 8501:8501 -p 8000:8000 --env-file .env instamart-discovery-engine
```

---

## ☁️ Cloud Deployment Guides

### Streamlit Community Cloud (Frontend)
1.  Push the project code to a public/private GitHub repository.
2.  Log in to [share.streamlit.io](https://share.streamlit.io).
3.  Click **New app**, select your repository, branch, and set the entrypoint file to `src/dashboard/app.py`.
4.  In **Advanced Settings**, paste your `.env` variables (e.g. `GEMINI_API_KEY`) into the secrets textarea.
5.  Click **Deploy**.

### Render / Fly.io (FastAPI Backend)
1.  Connect your GitHub repository to [Render](https://render.com).
2.  Create a new **Web Service**.
3.  Set the environment to `Python 3`, build command to `pip install -r requirements.txt`, and start command to `uvicorn src.api.main:app --host 0.0.0.0 --port $PORT`.
4.  Add your `GEMINI_API_KEY` or `OPENAI_API_KEY` under the **Environment Variables** tab.
5.  Click Deploy.
