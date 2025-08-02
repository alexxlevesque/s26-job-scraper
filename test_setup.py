#!/usr/bin/env python3
"""
Test script to verify the job scraper setup is working correctly.
"""

import sys
import os

def test_imports():
    """Test that all required modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        import yaml
        print("✅ PyYAML imported successfully")
    except ImportError:
        print("❌ PyYAML not found. Run: pip install pyyaml")
        return False
    
    try:
        import requests
        print("✅ Requests imported successfully")
    except ImportError:
        print("❌ Requests not found. Run: pip install requests")
        return False
    
    try:
        import bs4
        print("✅ BeautifulSoup imported successfully")
    except ImportError:
        print("❌ BeautifulSoup not found. Run: pip install beautifulsoup4")
        return False
    
    try:
        from dotenv import load_dotenv
        print("✅ python-dotenv imported successfully")
    except ImportError:
        print("❌ python-dotenv not found. Run: pip install python-dotenv")
        return False
    
    try:
        import schedule
        print("✅ Schedule imported successfully")
    except ImportError:
        print("❌ Schedule not found. Run: pip install schedule")
        return False
    
    return True

def test_project_structure():
    """Test that all required files exist"""
    print("\n📁 Testing project structure...")
    
    required_files = [
        'config/settings.py',
        'config/job_sources.yaml',
        'scraper/database/models.py',
        'scraper/scrapers/base_scraper.py',
        'scraper/scrapers/linkedin_scraper.py',
        'scraper/scrapers/custom_scraper.py',
        'scraper/notifications/email_notifier.py',
        'main.py',
        'requirements.txt',
        'README.md'
    ]
    
    missing_files = []
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - MISSING")
            missing_files.append(file_path)
    
    return len(missing_files) == 0

def test_config_loading():
    """Test that configuration can be loaded"""
    print("\n⚙️ Testing configuration loading...")
    
    try:
        import yaml
        with open('config/job_sources.yaml', 'r') as f:
            config = yaml.safe_load(f)
        
        if 'job_sources' in config:
            print("✅ Job sources configuration loaded")
        else:
            print("❌ Job sources configuration missing")
            return False
        
        if 'custom_urls' in config:
            print("✅ Custom URLs configuration loaded")
        else:
            print("❌ Custom URLs configuration missing")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error loading configuration: {e}")
        return False

def test_database_initialization():
    """Test that database can be initialized"""
    print("\n💾 Testing database initialization...")
    
    try:
        from scraper.database.models import JobDatabase
        from config.settings import DATABASE_PATH
        
        # Create data directory if it doesn't exist
        os.makedirs('data', exist_ok=True)
        
        db = JobDatabase(DATABASE_PATH)
        print("✅ Database initialized successfully")
        return True
        
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Job Scraper Setup Test\n")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_project_structure,
        test_config_loading,
        test_database_initialization
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your job scraper is ready to use.")
        print("\nNext steps:")
        print("1. Copy env.example to .env and configure your email settings")
        print("2. Edit config/job_sources.yaml with your job preferences")
        print("3. Run: python main.py")
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 