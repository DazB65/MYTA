"""
Vercel serverless function entry point for MYTA FastAPI backend
"""

import sys
import os

# Add the parent directory to the Python path so we can import from App
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the FastAPI app
from App.main import app

# Export the app for Vercel
# Vercel will automatically handle ASGI apps like FastAPI
app = app
