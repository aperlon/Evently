"""
Vercel Serverless Function entry point for FastAPI backend
"""
import sys
import os
from pathlib import Path

# Add backend to Python path
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

# Set working directory to backend for CSV access
os.chdir(backend_path)

# Import FastAPI app
from app.main import app

# Export for Vercel
# Vercel will route /api/* requests to this handler
handler = app
