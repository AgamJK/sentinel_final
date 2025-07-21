#!/usr/bin/env python3
"""
Pre-deployment validation script
Checks if your backend is ready for deployment
"""

import os
import sys
from dotenv import load_dotenv

def check_deployment_readiness():
    """Check if the app is ready for deployment"""
    print("🔍 Checking Deployment Readiness...")
    print("=" * 50)
    
    issues = []
    warnings = []
    
    # Load environment variables
    load_dotenv()
    
    # Check 1: Required environment variables
    print("\n1️⃣ Environment Variables:")
    required_vars = ['MONGODB_URI', 'GEMINI_API_KEY']
    for var in required_vars:
        if os.getenv(var):
            print(f"   ✅ {var}: Present")
        else:
            print(f"   ❌ {var}: MISSING")
            issues.append(f"Missing required environment variable: {var}")
    
    # Check 2: Dependencies
    print("\n2️⃣ Dependencies:")
    try:
        import flask
        import flask_cors
        import pymongo
        import google.generativeai as genai
        import gunicorn
        print("   ✅ All required packages installed")
    except ImportError as e:
        print(f"   ❌ Missing package: {e}")
        issues.append(f"Missing Python package: {e}")
    
    # Check 3: Database connection
    print("\n3️⃣ Database Connection:")
    try:
        from database import get_database_manager
        db_manager = get_database_manager()
        count = db_manager.get_message_count()
        print(f"   ✅ MongoDB connected successfully (messages: {count})")
        db_manager.close_connection()
    except Exception as e:
        print(f"   ❌ Database connection failed: {e}")
        issues.append(f"Database connection error: {e}")
    
    # Check 4: API endpoints
    print("\n4️⃣ API Endpoints:")
    try:
        from app import app
        routes = []
        for rule in app.url_map.iter_rules():
            routes.append(f"{rule.methods} {rule.rule}")
        print(f"   ✅ {len(routes)} endpoints configured")
        
        # Check key endpoints
        key_endpoints = ['/dashboard', '/api/emotion-overview', '/api/emotion-trends']
        for endpoint in key_endpoints:
            if any(endpoint in route for route in routes):
                print(f"      ✅ {endpoint}")
            else:
                print(f"      ❌ {endpoint} MISSING")
                issues.append(f"Missing endpoint: {endpoint}")
                
    except Exception as e:
        print(f"   ❌ Failed to load Flask app: {e}")
        issues.append(f"Flask app error: {e}")
    
    # Check 5: CORS configuration
    print("\n5️⃣ CORS Configuration:")
    try:
        with open('app.py', 'r') as f:
            content = f.read()
            if 'flask_cors' in content and 'CORS(' in content:
                print("   ✅ CORS enabled")
            else:
                print("   ❌ CORS not properly configured")
                issues.append("CORS not configured - frontend will be blocked")
    except Exception as e:
        print(f"   ⚠️  Could not verify CORS: {e}")
        warnings.append("Could not verify CORS configuration")
    
    # Check 6: Production files
    print("\n6️⃣ Production Files:")
    prod_files = ['Procfile', 'Dockerfile', 'requirements.txt']
    for file in prod_files:
        if os.path.exists(file):
            print(f"   ✅ {file}")
        else:
            print(f"   ⚠️  {file} missing")
            warnings.append(f"Missing {file} - needed for some deployment platforms")
    
    # Final assessment
    print("\n" + "=" * 50)
    if issues:
        print("❌ DEPLOYMENT NOT READY")
        print("\n🚨 Critical Issues to Fix:")
        for issue in issues:
            print(f"   • {issue}")
        
        if warnings:
            print("\n⚠️  Warnings:")
            for warning in warnings:
                print(f"   • {warning}")
        
        return False
    else:
        print("✅ DEPLOYMENT READY!")
        print("\n🎉 Your backend is ready to deploy!")
        
        if warnings:
            print("\n⚠️  Minor Warnings (non-critical):")
            for warning in warnings:
                print(f"   • {warning}")
        
        print("\n🚀 Deployment Options:")
        print("   • Heroku: Use Procfile")
        print("   • Railway/Render: Connect GitHub repo")
        print("   • Docker: Use Dockerfile")
        print("   • VPS: Install dependencies and run with gunicorn")
        
        return True

if __name__ == "__main__":
    ready = check_deployment_readiness()
    sys.exit(0 if ready else 1)
