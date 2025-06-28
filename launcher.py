#!/usr/bin/env python3
"""
Package installer and launcher script.
Installs packages from requirements.txt if needed, then runs wstesting.py
"""

import subprocess
import sys
import os
import pkg_resources
from pathlib import Path

def read_requirements(file_path="requirements.txt"):
    """Read and parse requirements.txt file."""
    if not os.path.exists(file_path):
        print(f"❌ {file_path} not found!")
        return []
    
    with open(file_path, 'r') as f:
        requirements = []
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                # Handle different requirement formats
                if '>=' in line:
                    pkg_name = line.split('>=')[0].strip()
                elif '==' in line:
                    pkg_name = line.split('==')[0].strip()
                elif '>' in line:
                    pkg_name = line.split('>')[0].strip()
                else:
                    pkg_name = line
                requirements.append((pkg_name, line))
        return requirements

def is_package_installed(package_name):
    """Check if a package is already installed."""
    try:
        pkg_resources.get_distribution(package_name)
        return True
    except pkg_resources.DistributionNotFound:
        return False

def install_package(package_spec):
    """Install a single package using pip."""
    try:
        print(f"📦 Installing {package_spec}...")
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", package_spec
        ], capture_output=True, text=True, check=True)
        print(f"✅ Successfully installed {package_spec}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install {package_spec}")
        print(f"Error: {e.stderr}")
        return False

def check_and_install_requirements():
    """Check requirements and install missing packages."""
    print("🔍 Checking requirements...")
    
    requirements = read_requirements()
    if not requirements:
        print("📝 No requirements.txt found or it's empty")
        return True
    
    missing_packages = []
    installed_packages = []
    
    for pkg_name, pkg_spec in requirements:
        if is_package_installed(pkg_name):
            installed_packages.append(pkg_name)
        else:
            missing_packages.append(pkg_spec)
    
    if installed_packages:
        print(f"✅ Already installed: {', '.join(installed_packages)}")
    
    if not missing_packages:
        print("🎉 All required packages are already installed!")
        return True
    
    print(f"📋 Need to install: {len(missing_packages)} package(s)")
    
    # Install missing packages
    all_installed = True
    for package_spec in missing_packages:
        if not install_package(package_spec):
            all_installed = False
    
    return all_installed

def run_wstesting():
    """Run the wstesting.py script."""
    if not os.path.exists("wstesting.py"):
        print("❌ wstesting.py not found in current directory!")
        return False
    
    print("\n🚀 Launching wstesting.py...")
    try:
        subprocess.run([sys.executable, "wstesting.py"], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running wstesting.py: {e}")
        return False
    except KeyboardInterrupt:
        print("\n⏹️ Execution interrupted by user")
        return True

def main():
    """Main function."""
    print("=" * 50)
    print("🔧 Package Installer & Launcher")
    print("=" * 50)
    
    # Check and install requirements
    if not check_and_install_requirements():
        print("\n❌ Failed to install some required packages. Exiting.")
        sys.exit(1)
    
    print("\n" + "=" * 50)
    
    # Run the main script
    if not run_wstesting():
        sys.exit(1)
    
    print("\n✨ Done!")

if __name__ == "__main__":
    main()
