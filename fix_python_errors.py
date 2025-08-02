#!/usr/bin/env python3
"""
Script to automatically fix common Python errors in the Vidalytics codebase.
"""

import os
import re
import sys
import argparse
from pathlib import Path
from typing import List, Dict, Tuple, Optional, Set

def fix_sqlite3_dependency(requirements_file: str) -> bool:
    """
    Fix the invalid sqlite3 dependency in requirements.txt.
    
    Args:
        requirements_file: Path to the requirements.txt file
        
    Returns:
        True if changes were made, False otherwise
    """
    with open(requirements_file, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Check if sqlite3 is listed as a dependency
    if re.search(r'^sqlite3\s', content, re.MULTILINE):
        # Replace the line with a comment
        new_content = re.sub(
            r'^sqlite3.*$',
            '# sqlite3 is built into Python and doesn\'t need to be in requirements.txt',
            content,
            flags=re.MULTILINE
        )
        
        # Write the changes back to the file
        with open(requirements_file, 'w', encoding='utf-8') as file:
            file.write(new_content)
        
        print(f"✅ Fixed sqlite3 dependency in {requirements_file}")
        return True
    
    return False

def fix_missing_imports(file_path: str) -> bool:
    """
    Fix missing imports in a Python file.
    
    Args:
        file_path: Path to the Python file
        
    Returns:
        True if changes were made, False otherwise
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    changes_made = False
    
    # Check for get_user_context usage without import
    if 'get_user_context(' in content and 'from backend.App.enhanced_user_context import get_user_context' not in content:
        # Find a good place to add the import
        if 'from backend.App.ai_services import' in content:
            new_content = re.sub(
                r'(from backend\.App\.ai_services import .+?\n)',
                r'\1from backend.App.enhanced_user_context import get_user_context\n\n',
                content
            )
            
            # Write the changes back to the file
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(new_content)
            
            print(f"✅ Added missing import for get_user_context in {file_path}")
            changes_made = True
    
    # Check for insights_engine usage without import
    if 'insights_engine.' in content and 'from insights_engine import insights_engine' not in content:
        # Find a good place to add the import
        if 'import' in content:
            # Add after the last import
            lines = content.split('\n')
            last_import_line = 0
            
            for i, line in enumerate(lines):
                if line.startswith('import ') or line.startswith('from '):
                    last_import_line = i
            
            if last_import_line > 0:
                lines.insert(last_import_line + 1, 'from insights_engine import insights_engine')
                
                # Write the changes back to the file
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write('\n'.join(lines))
                
                print(f"✅ Added missing import for insights_engine in {file_path}")
                changes_made = True
    
    return changes_made

def fix_pydantic_imports(file_path: str) -> bool:
    """
    Fix Pydantic imports to use consistent versioning.
    
    Args:
        file_path: Path to the Python file
        
    Returns:
        True if changes were made, False otherwise
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Check if the file uses both Pydantic v1 and v2 imports
    v1_imports = 'from pydantic.v1' in content
    direct_imports = re.search(r'from pydantic import(?! v1)', content)
    
    if direct_imports:  # Only check for direct imports, don't require v1 imports
        # Convert direct imports to v1 imports
        new_content = re.sub(
            r'from pydantic import ([^v].*?)$',
            r'from pydantic.v1 import \1',
            content,
            flags=re.MULTILINE
        )
        
        # Write the changes back to the file
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(new_content)
        
        print(f"✅ Standardized Pydantic imports to v1 in {file_path}")
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
    """Main function to run the error fixer."""
    parser = argparse.ArgumentParser(description='Fix common Python errors in the Vidalytics codebase.')
    parser.add_argument('--requirements', action='store_true', help='Fix requirements.txt issues')
    parser.add_argument('--imports', action='store_true', help='Fix missing imports')
    parser.add_argument('--pydantic', action='store_true', help='Fix Pydantic version issues')
    parser.add_argument('--all', action='store_true', help='Fix all issues')
    parser.add_argument('--dir', type=str, default='.', help='Directory to process (default: current directory)')
    
    args = parser.parse_args()
    
    # If no specific fixes are requested, show help
    if not (args.requirements or args.imports or args.pydantic or args.all):
        parser.print_help()
        return
    
    # Get the base directory
    base_dir = os.path.abspath(args.dir)
    print(f"Processing directory: {base_dir}")
    
    # Fix requirements.txt issues
    if args.requirements or args.all:
        requirements_file = os.path.join(base_dir, 'requirements.txt')
        if os.path.exists(requirements_file):
            fix_sqlite3_dependency(requirements_file)
        else:
            print(f"⚠️ Requirements file not found: {requirements_file}")
    
    # Find Python files
    if args.imports or args.pydantic or args.all:
        python_files = find_python_files(base_dir)
        print(f"Found {len(python_files)} Python files")
        
        # Fix missing imports
        if args.imports or args.all:
            for file_path in python_files:
                fix_missing_imports(file_path)
        
        # Fix Pydantic version issues
        if args.pydantic or args.all:
            for file_path in python_files:
                fix_pydantic_imports(file_path)
    
    print("Done!")

if __name__ == "__main__":
    main()