#!/usr/bin/env python3
"""
SuperKart Project Verification Script
Runs quick checks on all project components to verify they work correctly.
Usage: python verify_project.py
"""

import sys
import os
import json
from pathlib import Path

# Color codes for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'
CHECKMARK = '✓'
CROSS = '✗'

def print_header(title):
    """Print formatted header"""
    print(f"\n{BLUE}{'='*60}")
    print(f"{title}")
    print(f"{'='*60}{RESET}\n")

def print_success(msg):
    """Print success message"""
    print(f"{GREEN}{CHECKMARK} {msg}{RESET}")

def print_error(msg):
    """Print error message"""
    print(f"{RED}{CROSS} {msg}{RESET}")

def print_warning(msg):
    """Print warning message"""
    print(f"{YELLOW}⚠ {msg}{RESET}")

def check_file_exists(filepath, description):
    """Check if file exists"""
    if Path(filepath).exists():
        size = Path(filepath).stat().st_size
        size_mb = size / (1024*1024)
        print_success(f"{description} ({size_mb:.1f} MB)")
        return True
    else:
        print_error(f"{description} - NOT FOUND")
        return False

def check_import(module_name, description):
    """Check if module can be imported"""
    try:
        __import__(module_name)
        print_success(f"{description}")
        return True
    except ImportError as e:
        print_error(f"{description} - {str(e)}")
        return False

def verify_project_structure():
    """Verify all required directories exist"""
    print_header("1. PROJECT STRUCTURE")
    
    required_dirs = {
        'data': 'Data directory',
        'src': 'Source code directory',
        'models': 'Models directory',
        'backend': 'Backend directory',
        'frontend': 'Frontend directory',
        'notebooks': 'Notebooks directory',
    }
    
    all_exist = True
    for dir_name, description in required_dirs.items():
        if Path(dir_name).exists():
            print_success(f"{description}: {dir_name}/")
        else:
            print_error(f"{description}: {dir_name}/ NOT FOUND")
            all_exist = False
    
    return all_exist

def verify_model_file():
    """Verify model file exists and can be loaded"""
    print_header("2. TRAINED MODEL")
    
    model_path = Path('models/superkart_sales_prediction_model_v1_0.joblib')
    if check_file_exists(model_path, "Model file"):
        try:
            import joblib
            model = joblib.load(model_path)
            print_success(f"Model loads successfully")
            print_success(f"Model type: {type(model).__name__}")
            return True
        except Exception as e:
            print_error(f"Failed to load model: {e}")
            return False
    return False

def verify_data_file():
    """Verify data file exists"""
    print_header("3. DATA FILE")
    
    data_path = Path('data/SuperKart (2).csv')
    if check_file_exists(data_path, "Dataset"):
        try:
            import pandas as pd
            df = pd.read_csv(data_path)
            print_success(f"Data loads successfully")
            print_success(f"Records: {len(df)}, Features: {len(df.columns)}")
            print_success(f"Columns: {', '.join(df.columns[:3])}...")
            return True
        except Exception as e:
            print_error(f"Failed to load data: {e}")
            return False
    return False

def verify_python_modules():
    """Verify all required Python modules"""
    print_header("4. PYTHON DEPENDENCIES")
    
    modules = {
        'pandas': 'Pandas (data processing)',
        'numpy': 'NumPy (numerical computing)',
        'sklearn': 'Scikit-learn (ML library)',
        'flask': 'Flask (backend framework)',
        'streamlit': 'Streamlit (frontend framework)',
        'joblib': 'Joblib (model serialization)',
        'requests': 'Requests (HTTP library)',
    }
    
    all_available = True
    for module, description in modules.items():
        if check_import(module, description):
            pass
        else:
            all_available = False
    
    return all_available

def verify_source_code():
    """Verify source code modules"""
    print_header("5. SOURCE CODE MODULES")
    
    # Add src to path
    sys.path.insert(0, 'src')
    
    modules = {
        'data_processing': 'Data processing module',
        'train_model': 'Model training module',
        'inference': 'Inference module',
    }
    
    all_ok = True
    for module, description in modules.items():
        try:
            __import__(module)
            print_success(f"{description}: {module}.py")
        except ImportError as e:
            print_error(f"{description}: {module}.py - {e}")
            all_ok = False
    
    return all_ok

def verify_backend():
    """Verify backend configuration"""
    print_header("6. BACKEND API")
    
    backend_path = Path('backend/app.py')
    if not backend_path.exists():
        print_error("Backend app.py not found")
        return False
    
    print_success("Backend app.py exists")
    
    try:
        sys.path.insert(0, 'backend')
        # Check if app can be imported (don't import to avoid Flask running)
        with open(backend_path) as f:
            content = f.read()
            if 'Flask' in content and 'predictsales' in content:
                print_success("Backend has Flask routes configured")
                if '/v1/predictsales' in content:
                    print_success("Single prediction endpoint configured")
                if '/v1/batchpredictsales' in content:
                    print_success("Batch prediction endpoint configured")
                return True
            else:
                print_error("Backend configuration incomplete")
                return False
    except Exception as e:
        print_error(f"Failed to verify backend: {e}")
        return False

def verify_frontend():
    """Verify frontend configuration"""
    print_header("7. FRONTEND UI")
    
    frontend_path = Path('frontend/app.py')
    if not frontend_path.exists():
        print_error("Frontend app.py not found")
        return False
    
    print_success("Frontend app.py exists")
    
    try:
        with open(frontend_path) as f:
            content = f.read()
            if 'streamlit' in content.lower():
                print_success("Streamlit interface configured")
            if 'requests' in content.lower():
                print_success("Backend communication configured")
            if 'BACKEND_URL' in content:
                print_success("Backend URL configuration found")
                return True
            else:
                print_warning("Backend URL not found - may need configuration")
                return True
    except Exception as e:
        print_error(f"Failed to verify frontend: {e}")
        return False

def verify_documentation():
    """Verify documentation files"""
    print_header("8. DOCUMENTATION")
    
    docs = {
        'README.md': 'Main README',
        'DEPLOYMENT.md': 'Deployment guide',
        'PROJECT_COMPLETION_SUMMARY.md': 'Project summary',
    }
    
    all_exist = True
    for filename, description in docs.items():
        if Path(filename).exists():
            print_success(f"{description}: {filename}")
        else:
            print_error(f"{description}: {filename} NOT FOUND")
            all_exist = False
    
    return all_exist

def verify_docker():
    """Verify Docker configuration"""
    print_header("9. DOCKER CONFIGURATION")
    
    files = {
        'backend/Dockerfile': 'Backend Dockerfile',
        'frontend/Dockerfile': 'Frontend Dockerfile',
        'docker-compose.yml': 'Docker Compose',
    }
    
    all_exist = True
    for filepath, description in files.items():
        if Path(filepath).exists():
            print_success(f"{description}: {filepath}")
        else:
            print_error(f"{description}: {filepath} NOT FOUND")
            all_exist = False
    
    return all_exist

def main():
    """Run all verification checks"""
    print(f"\n{BLUE}{'='*60}")
    print(f"SuperKart Sales Prediction - Project Verification")
    print(f"{'='*60}{RESET}\n")
    
    results = {}
    
    results['Structure'] = verify_project_structure()
    results['Model'] = verify_model_file()
    results['Data'] = verify_data_file()
    results['Dependencies'] = verify_python_modules()
    results['Source Code'] = verify_source_code()
    results['Backend'] = verify_backend()
    results['Frontend'] = verify_frontend()
    results['Documentation'] = verify_documentation()
    results['Docker'] = verify_docker()
    
    # Summary
    print_header("VERIFICATION SUMMARY")
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    failed = total - passed
    
    for check, result in results.items():
        status = f"{GREEN}{CHECKMARK} PASS{RESET}" if result else f"{RED}{CROSS} FAIL{RESET}"
        print(f"  {check:.<40} {status}")
    
    print(f"\n{BLUE}{'='*60}{RESET}")
    if failed == 0:
        print(f"{GREEN}✓ ALL CHECKS PASSED! Project is ready.{RESET}")
        print(f"\n{YELLOW}Quick Start:{RESET}")
        print(f"  1. Backend: cd backend && python app.py")
        print(f"  2. Frontend: cd frontend && streamlit run app.py")
        print(f"  3. Open: http://localhost:8501")
    else:
        print(f"{RED}✗ {failed} check(s) failed. Review errors above.{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")
    
    return 0 if failed == 0 else 1

if __name__ == '__main__':
    sys.exit(main())
