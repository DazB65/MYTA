#!/usr/bin/env python3
"""
Script to fix import errors in the Vidalytics codebase by converting relative imports to absolute imports.
"""

import os
import re
import sys
import argparse
from pathlib import Path
from typing import List, Dict, Tuple, Optional, Set

def fix_relative_imports(file_path: str) -> bool:
    """
    Fix relative imports in a Python file by adding the 'backend.App' prefix.
    
    Args:
        file_path: Path to the Python file
        
    Returns:
        True if changes were made, False otherwise
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Skip files that are already using absolute imports consistently
    if 'from backend.App' in content and 'from ' in content and not re.search(r'from (?!backend\.App)[a-zA-Z_][a-zA-Z0-9_]*(?:\.[a-zA-Z_][a-zA-Z0-9_]*)* import', content):
        return False
    
    # Convert relative imports to absolute imports
    new_content = re.sub(
        r'from ([a-zA-Z_][a-zA-Z0-9_]*(?:\.[a-zA-Z_][a-zA-Z0-9_]*)*) import',
        lambda m: f'from backend.App.{m.group(1)} import' if m.group(1) != 'backend.App' and not m.group(1).startswith('backend.App.') and not m.group(1) in ['typing', 'os', 'sys', 'datetime', 're', 'json', 'time', 'logging', 'pathlib', 'uuid', 'enum', 'collections', 'functools', 'itertools', 'math', 'random', 'hashlib', 'base64', 'urllib', 'http', 'email', 'tempfile', 'shutil', 'subprocess', 'threading', 'multiprocessing', 'asyncio', 'contextlib', 'inspect', 'importlib', 'traceback', 'warnings', 'pydantic', 'pydantic.v1', 'fastapi', 'starlette', 'slowapi', 'redis', 'sqlalchemy', 'google', 'googleapiclient', 'google_auth_oauthlib', 'google.oauth2', 'anthropic', 'openai', 'supabase'] else f'from {m.group(1)} import',
        content,
        flags=re.MULTILINE
    )
    
    # Convert import statements
    new_content = re.sub(
        r'import ([a-zA-Z_][a-zA-Z0-9_]*(?:\.[a-zA-Z_][a-zA-Z0-9_]*)*)',
        lambda m: f'import backend.App.{m.group(1)}' if m.group(1) != 'backend.App' and not m.group(1).startswith('backend.App.') and not m.group(1) in ['typing', 'os', 'sys', 'datetime', 're', 'json', 'time', 'logging', 'pathlib', 'uuid', 'enum', 'collections', 'functools', 'itertools', 'math', 'random', 'hashlib', 'base64', 'urllib', 'http', 'email', 'tempfile', 'shutil', 'subprocess', 'threading', 'multiprocessing', 'asyncio', 'contextlib', 'inspect', 'importlib', 'traceback', 'warnings', 'pydantic', 'pydantic.v1', 'fastapi', 'starlette', 'slowapi', 'redis', 'sqlalchemy', 'google', 'googleapiclient', 'google_auth_oauthlib', 'google.oauth2', 'anthropic', 'openai', 'supabase'] else f'import {m.group(1)}',
        new_content,
        flags=re.MULTILINE
    )
    
    # If changes were made, write the new content back to the file
    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(new_content)
        
        print(f"✅ Fixed imports in {file_path}")
        return True
    
    return False

def find_python_files(directory: str, exclude_dirs: List[str] = None) -> List[str]:
    """
    Find all Python files in a directory and its subdirectories.
    
    Args:
        directory: Directory to search
        exclude_dirs: List of directories to exclude
        
    Returns:
        List of Python file paths
    """
    if exclude_dirs is None:
        exclude_dirs = ['venv', '__pycache__', '.git']
    
    python_files = []
    
    for root, dirs, files in os.walk(directory):
        # Skip excluded directories
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    
    return python_files

def main():
    """Main function to run the import fixer."""
    parser = argparse.ArgumentParser(description='Fix import errors in the Vidalytics codebase.')
    parser.add_argument('--dir', type=str, default='backend/App', help='Directory to process (default: backend/App)')
    parser.add_argument('--file', type=str, help='Specific file to process')
    
    args = parser.parse_args()
    
    # Get the base directory
    base_dir = os.path.abspath(args.dir)
    print(f"Processing directory: {base_dir}")
    
    # Process a specific file if provided
    if args.file:
        file_path = os.path.abspath(args.file)
        if os.path.exists(file_path):
            fix_relative_imports(file_path)
        else:
            print(f"⚠️ File not found: {file_path}")
        return
    
    # Find Python files
    python_files = find_python_files(base_dir)
    print(f"Found {len(python_files)} Python files")
    
    # Fix imports in all files
    fixed_count = 0
    for file_path in python_files:
        if fix_relative_imports(file_path):
            fixed_count += 1
    
    print(f"Fixed imports in {fixed_count} files")
    print("Done!")

if __name__ == "__main__":
    main()