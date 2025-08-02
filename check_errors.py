#!/usr/bin/env python3
"""
Script to check for common Python errors in the codebase.
"""

import os
import sys
import ast
import importlib
import importlib.util
import traceback
from pathlib import Path

def check_syntax_errors(file_path):
    """Check for syntax errors in a Python file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        try:
            content = file.read()
            ast.parse(content)
            return []
        except SyntaxError as e:
            return [f"Syntax error in {file_path}: {e}"]

def check_import_errors(file_path):
    """Check for import errors in a Python file."""
    errors = []
    
    # Get the module name from the file path
    module_name = os.path.splitext(os.path.basename(file_path))[0]
    
    # Try to import the module
    try:
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        if spec is None:
            return [f"Could not create spec for {file_path}"]
        
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        
        # We don't actually execute the module to avoid side effects
        # Just check if imports can be resolved
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
                    lineno = node.lineno
                    if isinstance(node, ast.Import):
                        for name in node.names:
                            try:
                                importlib.import_module(name.name)
                            except ImportError as e:
                                errors.append(f"Import error in {file_path}:{lineno} - {name.name}: {e}")
                    elif isinstance(node, ast.ImportFrom) and node.module is not None:
                        try:
                            importlib.import_module(node.module)
                        except ImportError as e:
                            errors.append(f"Import error in {file_path}:{lineno} - from {node.module}: {e}")
    except Exception as e:
        errors.append(f"Error checking imports in {file_path}: {e}")
    
    return errors

def check_undefined_variables(file_path):
    """Check for potentially undefined variables in a Python file."""
    errors = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            tree = ast.parse(content)
            
            # Get all defined names in the module
            defined_names = set()
            for node in ast.walk(tree):
                if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
                    defined_names.add(node.id)
                elif isinstance(node, ast.FunctionDef):
                    defined_names.add(node.name)
                elif isinstance(node, ast.ClassDef):
                    defined_names.add(node.name)
                elif isinstance(node, ast.Import):
                    for name in node.names:
                        defined_names.add(name.asname if name.asname else name.name)
                elif isinstance(node, ast.ImportFrom):
                    for name in node.names:
                        defined_names.add(name.asname if name.asname else name.name)
            
            # Check for used names that aren't defined
            for node in ast.walk(tree):
                if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
                    if node.id not in defined_names and node.id not in __builtins__:
                        errors.append(f"Potentially undefined variable in {file_path}:{node.lineno} - {node.id}")
    except Exception as e:
        errors.append(f"Error checking undefined variables in {file_path}: {e}")
    
    return errors

def check_pydantic_version_issues(file_path):
    """Check for Pydantic v1/v2 compatibility issues."""
    errors = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            
            # Check for imports from both pydantic v1 and v2
            v1_imports = "from pydantic.v1" in content
            direct_imports = "from pydantic import" in content
            
            if v1_imports and direct_imports:
                errors.append(f"Potential Pydantic version conflict in {file_path}: mixing v1 and v2 imports")
            
            # Check for BaseModel usage which might be problematic
            if "class" in content and "BaseModel" in content:
                if v1_imports and "from pydantic.v1 import BaseModel" not in content:
                    errors.append(f"Potential Pydantic issue in {file_path}: using BaseModel without proper v1 import")
                if direct_imports and "from pydantic.v1 import BaseModel" not in content:
                    errors.append(f"Potential Pydantic issue in {file_path}: using BaseModel without direct import")
    except Exception as e:
        errors.append(f"Error checking Pydantic issues in {file_path}: {e}")
    
    return errors

def scan_directory(directory):
    """Scan a directory for Python files and check for errors."""
    all_errors = []
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                
                # Skip virtual environment files
                if 'venv' in file_path or '__pycache__' in file_path:
                    continue
                
                print(f"Checking {file_path}...")
                
                # Check for syntax errors
                syntax_errors = check_syntax_errors(file_path)
                if syntax_errors:
                    all_errors.extend(syntax_errors)
                    continue  # Skip further checks if there are syntax errors
                
                # Check for import errors
                import_errors = check_import_errors(file_path)
                if import_errors:
                    all_errors.extend(import_errors)
                
                # Check for undefined variables
                undefined_vars = check_undefined_variables(file_path)
                if undefined_vars:
                    all_errors.extend(undefined_vars)
                
                # Check for Pydantic version issues
                pydantic_issues = check_pydantic_version_issues(file_path)
                if pydantic_issues:
                    all_errors.extend(pydantic_issues)
    
    return all_errors

def main():
    """Main function to run the error checker."""
    print("Python Error Checker")
    print("===================")
    
    # Check the backend directory
    backend_dir = os.path.join(os.getcwd(), 'backend', 'App')
    if os.path.exists(backend_dir):
        print(f"\nChecking backend directory: {backend_dir}")
        backend_errors = scan_directory(backend_dir)
        
        if backend_errors:
            print("\nErrors found in backend:")
            for error in backend_errors:
                print(f"  - {error}")
        else:
            print("\nNo errors found in backend.")
    else:
        print(f"\nBackend directory not found: {backend_dir}")
    
    # Check the scripts directory if it exists
    scripts_dir = os.path.join(os.getcwd(), 'scripts')
    if os.path.exists(scripts_dir):
        print(f"\nChecking scripts directory: {scripts_dir}")
        scripts_errors = scan_directory(scripts_dir)
        
        if scripts_errors:
            print("\nErrors found in scripts:")
            for error in scripts_errors:
                print(f"  - {error}")
        else:
            print("\nNo errors found in scripts.")
    
    print("\nCheck completed.")

if __name__ == "__main__":
    main()