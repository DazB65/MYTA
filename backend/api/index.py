"""
Production FastAPI backend for MYTA - Vercel deployment
Imports the full App/main.py application with all features
"""

import os
import sys

# Add the backend directory to Python path for imports
backend_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

# Import the full FastAPI app from App/main.py
from App.main import app

# The app is now imported from App/main.py with all features:
# - Email verification and password reset
# - All agent routers
# - YouTube integration
# - Supabase integration
# - Security middleware
# - Rate limiting
# - And all other features

# Vercel will use this app instance for serverless deployment
