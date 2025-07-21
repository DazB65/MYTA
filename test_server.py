#!/usr/bin/env python3
"""
Simple test server to verify port connectivity
"""
from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Test server is working!"}

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Test server healthy"}

if __name__ == "__main__":
    print("Starting test server on http://localhost:8890")
    uvicorn.run(app, host="0.0.0.0", port=8890)