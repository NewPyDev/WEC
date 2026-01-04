#!/usr/bin/env python3
"""
Django Ecommerce Inventory Manager - Cloud Startup Script
This script is designed to work in cloud environments without virtual environments.
"""

import os
import sys
import subprocess
import platform

def check_python():
    """Check if Python is available and get version."""
    try:
        version = sys.version.split()[0]
        print(f"✓ Python {version} found")
        return True
    except Exception as e:
        print(f"✗ Python check failed: {e}")
        return False

def check_django():
    """Check if Django is installed and importable."""
    try:
        import django
        print(f"✓ Django {django.get_version()} found")
        return True
    except ImportError:
        print("✗ Django not found")
        return False

def install_requirements():
    """Install requirements if requirements.txt exists."""
    if os.path.exists('requirements.txt'):
        print("📦 Installing requirements...")
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                         check=True)
            print("✓ Requirements installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"⚠️ Warning: Requirements installation failed: {e}")
            return False
    else:
        print("ℹ️ No requirements.txt found, skipping installation")
        return True

def run_migrations():
    """Run Django database migrations."""
    print("🗄️ Running database migrations...")
    try:
        subprocess.run([sys.executable, 'manage.py', 'migrate'], check=True)
        print("✓ Migrations completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Warning: Migrations failed: {e}")
        return False

def collect_static():
    """Collect static files for production."""
    print("📁 Collecting static files...")
    try:
        subprocess.run([sys.executable, 'manage.py', 'collectstatic', '--noinput'], 
                      check=True)
        print("✓ Static files collected successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"ℹ️ Static files collection skipped: {e}")
        return True

def start_server():
    """Start the Django development server."""
    # Get host and port from environment variables (cloud-friendly)
    host = os.environ.get('HOST', '0.0.0.0')
    port = os.environ.get('PORT', '8000')
    
    print(f"🚀 Starting Django server on {host}:{port}")
    print("📱 Access your app at:")
    print(f"   Local: http://localhost:{port}")
    print(f"   Network: http://{host}:{port}")
    print("\n🛑 Press Ctrl+C to stop the server\n")
    
    try:
        subprocess.run([sys.executable, 'manage.py', 'runserver', f'{host}:{port}'])
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Server failed to start: {e}")
        return False
    
    return True

def main():
    """Main startup function."""
    print("=" * 60)
    print("🏪 Django Ecommerce Inventory Manager")
    print("=" * 60)
    print(f"🖥️  Platform: {platform.system()} {platform.release()}")
    print(f"📁 Working directory: {os.getcwd()}")
    print()
    
    # Change to script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Check if this is a Django project
    if not os.path.exists('manage.py'):
        print("❌ ERROR: manage.py not found!")
        print("Make sure you're in a Django project directory.")
        sys.exit(1)
    
    # System checks
    print("🔍 Performing system checks...")
    
    if not check_python():
        sys.exit(1)
    
    if not check_django():
        print("🔧 Attempting to install Django...")
        install_requirements()
        if not check_django():
            print("❌ Django installation failed!")
            sys.exit(1)
    
    # Setup steps
    print("\n🔧 Setup steps...")
    run_migrations()
    
    # For production/cloud deployments
    if os.environ.get('DJANGO_SETTINGS_MODULE') and 'production' in os.environ.get('DJANGO_SETTINGS_MODULE', ''):
        collect_static()
    
    # Start the server
    print("\n" + "=" * 60)
    start_server()
    
    print("\n👋 Goodbye!")

if __name__ == '__main__':
    main()
