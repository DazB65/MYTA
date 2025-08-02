#!/usr/bin/env python3
"""
Script to check for specific errors in main.py
"""

import os
import ast
import sys

def find_undefined_functions(file_path):
    """Find undefined functions in a Python file."""
    errors = []
    
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        
    # Parse the file
    try:
        tree = ast.parse(content)
    except SyntaxError as e:
        return [f"Syntax error in {file_path}: {e}"]
    
    # Find all defined functions and imported names
    defined_names = set()
    imports = {}
    
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            defined_names.add(node.name)
        elif isinstance(node, ast.Import):
            for name in node.names:
                if name.asname:
                    defined_names.add(name.asname)
                else:
                    defined_names.add(name.name)
                    imports[name.name] = None
        elif isinstance(node, ast.ImportFrom):
            module = node.module
            for name in node.names:
                if name.asname:
                    defined_names.add(name.asname)
                else:
                    defined_names.add(name.name)
                    if module:
                        imports[name.name] = module
    
    # Find all function calls
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                func_name = node.func.id
                if func_name not in defined_names and func_name not in dir(__builtins__):
                    errors.append(f"Line {node.lineno}: Function '{func_name}' is called but not defined or imported")
            elif isinstance(node.func, ast.Attribute):
                # Handle method calls like obj.method()
                if isinstance(node.func.value, ast.Name):
                    obj_name = node.func.value.id
                    method_name = node.func.attr
                    
                    # Check if the object is imported but the method might not exist
                    if obj_name in imports and imports[obj_name] is not None:
                        # This is a potential issue, but we can't be sure without importing
                        # Just note it as a potential issue
                        pass
    
    # Find missing imports
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            if node.module is None:
                continue
            
            # Check for relative imports that might be problematic
            if node.module.startswith('backend.App') and not node.level:
                # This is an absolute import from backend.App
                module_parts = node.module.split('.')
                if len(module_parts) > 2:
                    # It's importing from a specific module in backend.App
                    module_name = module_parts[-1]
                    # Check if there's also a direct import of the same module
                    for other_node in ast.walk(tree):
                        if isinstance(other_node, ast.ImportFrom) and other_node.module == module_name:
                            errors.append(
                                f"Line {node.lineno}: Potential import conflict - "
                                f"importing from '{node.module}' and directly from '{module_name}'"
                            )
    
    # Check for undefined variables in function calls
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            for arg in node.args:
                if isinstance(arg, ast.Name):
                    var_name = arg.id
                    if var_name not in defined_names and var_name not in dir(__builtins__):
                        errors.append(f"Line {arg.lineno}: Variable '{var_name}' is used but not defined")
    
    return errors

def check_get_user_context_usage(file_path):
    """Check for get_user_context usage without proper import."""
    errors = []
    
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Check if get_user_context is used
    if "get_user_context(" in content:
        # Check if it's imported
        import_patterns = [
            "from enhanced_user_context import get_user_context",
            "from backend.App.enhanced_user_context import get_user_context",
            "import enhanced_user_context"
        ]
        
        if not any(pattern in content for pattern in import_patterns):
            errors.append("Function 'get_user_context' is used but not properly imported")
    
    return errors

def check_insights_engine_usage(file_path):
    """Check for insights_engine usage without proper import."""
    errors = []
    
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Check if insights_engine is used
    if "insights_engine." in content:
        # Check if it's imported
        import_patterns = [
            "from insights_engine import insights_engine",
            "from backend.App.insights_engine import insights_engine",
            "import insights_engine"
        ]
        
        if not any(pattern in content for pattern in import_patterns):
            errors.append("Module 'insights_engine' is used but not properly imported")
    
    return errors

def check_pydantic_version_issues(file_path):
    """Check for Pydantic v1/v2 compatibility issues."""
    errors = []
    
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Check for imports from both pydantic v1 and v2
    v1_imports = "from pydantic.v1" in content
    direct_imports = "from pydantic import" in content
    
    if v1_imports and direct_imports:
        errors.append("Potential Pydantic version conflict: mixing v1 and v2 imports")
    
    return errors

def check_sqlite3_dependency(file_path):
    """Check for sqlite3 dependency issues in requirements.txt."""
    errors = []
    
    with open(file_path, 'r', encoding='utf-8') as file:
        for i, line in enumerate(file, 1):
            line = line.strip()
            if line.startswith("sqlite3"):
                errors.append(f"Line {i}: sqlite3 is a built-in module and should not be in requirements.txt")
    
    return errors

def main():
    """Main function to run the error checker."""
    print("Checking for specific errors in main.py")
    print("======================================")
    
    # Check main.py
    main_py_path = os.path.join(os.getcwd(), 'backend', 'App', 'main.py')
    if os.path.exists(main_py_path):
        print(f"Checking {main_py_path}...")
        
        # Check for undefined functions
        undefined_funcs = find_undefined_functions(main_py_path)
        if undefined_funcs:
            print("\nPotential undefined functions or imports:")
            for error in undefined_funcs:
                print(f"  - {error}")
        
        # Check for get_user_context usage
        user_context_errors = check_get_user_context_usage(main_py_path)
        if user_context_errors:
            print("\nIssues with get_user_context:")
            for error in user_context_errors:
                print(f"  - {error}")
        
        # Check for insights_engine usage
        insights_engine_errors = check_insights_engine_usage(main_py_path)
        if insights_engine_errors:
            print("\nIssues with insights_engine:")
            for error in insights_engine_errors:
                print(f"  - {error}")
        
        # Check for Pydantic version issues
        pydantic_issues = check_pydantic_version_issues(main_py_path)
        if pydantic_issues:
            print("\nPydantic version issues:")
            for error in pydantic_issues:
                print(f"  - {error}")
    else:
        print(f"File not found: {main_py_path}")
    
    # Check requirements.txt
    requirements_path = os.path.join(os.getcwd(), 'requirements.txt')
    if os.path.exists(requirements_path):
        print(f"\nChecking {requirements_path}...")
        
        # Check for sqlite3 dependency
        sqlite3_issues = check_sqlite3_dependency(requirements_path)
        if sqlite3_issues:
            print("\nIssues with sqlite3 dependency:")
            for error in sqlite3_issues:
                print(f"  - {error}")
    else:
        print(f"File not found: {requirements_path}")
    
    print("\nCheck completed.")

if __name__ == "__main__":
    main()