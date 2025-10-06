"""
Simple Vercel serverless function for MYTA backend
"""

import json
import time
import secrets
import hashlib
from urllib.parse import parse_qs

# In-memory storage
users_db = {}

def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
    return f"{salt}:{pwd_hash.hex()}"

def verify_password(password: str, hashed: str) -> bool:
    try:
        salt, pwd_hash = hashed.split(':')
        return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000).hex() == pwd_hash
    except:
        return False

def handler(request):
    """Vercel serverless function handler"""

    # CORS headers
    headers = {
        'Access-Control-Allow-Origin': 'https://myta-kgvke4oeq-mytas-projects.vercel.app',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Credentials': 'true',
        'Content-Type': 'application/json'
    }

    # Handle preflight OPTIONS request
    if request.method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': ''
        }

    path = request.url.path
    method = request.method

    try:
        # Health check
        if path == '/health' and method == 'GET':
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({
                    'status': 'healthy',
                    'timestamp': time.time(),
                    'service': 'MYTA Backend'
                })
            }

        # Root endpoint
        if path == '/' and method == 'GET':
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({
                    'message': 'MYTA Backend is running!',
                    'status': 'healthy',
                    'timestamp': time.time()
                })
            }

        # Registration endpoint
        if path == '/api/auth/register' and method == 'POST':
            try:
                body = json.loads(request.body)

                # Basic validation
                if body['password'] != body['confirm_password']:
                    return {
                        'statusCode': 400,
                        'headers': headers,
                        'body': json.dumps({'detail': 'Passwords do not match'})
                    }

                if len(body['password']) < 8:
                    return {
                        'statusCode': 400,
                        'headers': headers,
                        'body': json.dumps({'detail': 'Password must be at least 8 characters'})
                    }

                # Check if user exists
                if body['email'] in users_db:
                    return {
                        'statusCode': 400,
                        'headers': headers,
                        'body': json.dumps({'detail': 'User already exists'})
                    }

                # Create user
                user_id = f"user_{secrets.token_urlsafe(16)}"
                hashed_password = hash_password(body['password'])

                users_db[body['email']] = {
                    "user_id": user_id,
                    "name": body['name'],
                    "email": body['email'],
                    "password_hash": hashed_password,
                    "created_at": time.time()
                }

                token = f"jwt_token_{user_id}_{int(time.time())}"

                return {
                    'statusCode': 200,
                    'headers': headers,
                    'body': json.dumps({
                        "status": "success",
                        "message": "User registered successfully",
                        "data": {
                            "user_id": user_id,
                            "email": body['email'],
                            "name": body['name'],
                            "token": token,
                            "expires_in": 28800
                        }
                    })
                }

            except Exception as e:
                return {
                    'statusCode': 500,
                    'headers': headers,
                    'body': json.dumps({'detail': f'Registration error: {str(e)}'})
                }

        # Default 404
        return {
            'statusCode': 404,
            'headers': headers,
            'body': json.dumps({'detail': 'Not found'})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'detail': f'Server error: {str(e)}'})
        }
