#!/usr/bin/env python3
"""
LHM Repository Setup Script
Helps initialize the repository for first-time use
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_python_version():
    """Check if Python version is 3.8+"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required")
        return False
    print(f"✅ Python {sys.version.split()[0]} detected")
    return True

def install_requirements():
    """Install required packages"""
    print("📦 Installing requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install requirements")
        return False

def setup_environment():
    """Setup environment file"""
    env_example = Path(".env.example")
    env_file = Path(".env")
    
    if env_file.exists():
        print("✅ .env file already exists")
        return True
    
    if env_example.exists():
        shutil.copy(env_example, env_file)
        print("✅ Created .env file from template")
        print("⚠️  Please edit .env file with your API keys")
        return True
    else:
        print("❌ .env.example not found")
        return False

def create_data_directories():
    """Create necessary data directories"""
    directories = ["data", "output", "charts", "logs"]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created {directory}/ directory")

def check_jupyter():
    """Check if Jupyter is available"""
    try:
        subprocess.check_output([sys.executable, "-m", "jupyter", "--version"], 
                               stderr=subprocess.STDOUT)
        print("✅ Jupyter is available")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Jupyter not found")
        return False

def main():
    """Main setup process"""
    print("🚀 Setting up LHM Repository...")
    print("=" * 50)
    
    # Check prerequisites
    if not check_python_version():
        return False
    
    # Install requirements
    if not install_requirements():
        return False
    
    # Setup environment
    if not setup_environment():
        return False
    
    # Create directories
    create_data_directories()
    
    # Check Jupyter
    check_jupyter()
    
    print("\n" + "=" * 50)
    print("🎉 Setup complete!")
    print("\nNext steps:")
    print("1. Edit .env file with your API keys")
    print("2. Run 'jupyter lab' to start exploring")
    print("3. Check Documentation/README.md for detailed usage")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)