"""
Production FastAPI backend for MYTA - Vercel Serverless Deployment
Imports the full App/main.py application with all features
Configured for serverless environment
"""

import os
import sys

# Set serverless environment flag BEFORE importing the app
os.environ['VERCEL_SERVERLESS'] = 'true'

# Add the backend directory to Python path for imports
backend_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

# Import the full FastAPI app from App/main.py
# The app will detect VERCEL_SERVERLESS and skip startup/shutdown events
from App.main import app

# The app is now imported from App/main.py with all features:
# - Email verification and password reset
# - All agent routers
# - YouTube integration
# - Supabase integration
# - Security middleware
# - Rate limiting
# - And all other features

# Export for Vercel serverless functions
# Vercel will use this as the ASGI application handler
handler = app
