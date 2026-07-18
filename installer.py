#!/usr/bin/env python3
"""
WHODIS — Complete Auto-Installer
Handles PEP 668, dependencies, installation, and configuration
Usage: python3 installer.py
"""

import sys
import os
import subprocess
from pathlib import Path
import json

# Color codes
GREEN = '\033[0;32m'
RED = '\033[0;31m'
YELLOW = '\033[1;33m'
BLUE = '\033[0;34m'
NC = '\033[0m'

def print_header(title):
    """Print a formatted header"""
    print(f"\n{BLUE}{'='*70}{NC}")
    print(f"{BLUE}{title}{NC}")
    print(f"{BLUE}{'='*70}{NC}\n")

def run_cmd(cmd, description, show_output=False):
    """Run a command and handle errors"""
    if show_output:
        print(f"{BLUE}→{NC} {description}")
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if show_output:
        if result.returncode == 0:
            print(f"{GREEN}✓{NC} {description}\n")
        else:
            print(f"{YELLOW}⚠{NC} {description} - may have warnings\n")
    
    return result

# Entry point
if __name__ == "__main__":
    print("\n" + "="*70)
    print(f"{BLUE}WHODIS — Full OSINT Phone Number Investigator{NC}")
    print("Complete Auto-Installation with Configuration")
    print("="*70 + "\n")

    # Check Python
    py_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    print(f"{GREEN}✓{NC} Python: {py_version}")

    if sys.version_info < (3, 8):
        print(f"{RED}✗{NC} Python 3.8+ required!")
        sys.exit(1)

    # Check pip
    try:
        import pip
        print(f"{GREEN}✓{NC} pip: {pip.__version__}\n")
    except:
        print(f"{RED}✗{NC} pip not found!")
        sys.exit(1)

    version = "0.1"
    home = Path.home()
    project_root = Path(__file__).parent

    # All dependencies
    DEPS = [
        "requests>=2.31.0",
        "beautifulsoup4>=4.12.2",
        "lxml>=4.9.3",
        "phonenumbers>=8.13.0",
        "colorama>=0.4.6",
        "tqdm>=4.66.1",
        "aiohttp>=3.9.1",
        "selenium>=4.15.2",
        "webdriver-manager>=4.0.1",
    ]

    print("📦 Installation Plan:")
    for dep in DEPS:
        print(f"   {BLUE}•{NC} {dep}")
    
    # Step 1: Upgrade pip
    print_header("STEP 1: Upgrade pip")
    
    result = run_cmd(
        [sys.executable, "-m", "pip", "install", "--upgrade", "pip", "setuptools", "wheel"],
        "Upgrading pip...",
        show_output=True
    )

    if result.returncode != 0 and ("externally-managed" in result.stderr or "PEP 668" in result.stderr):
        print(f"{YELLOW}⚠{NC} PEP 668 detected, using --break-system-packages\n")
        result = run_cmd(
            [sys.executable, "-m", "pip", "install", "--upgrade", 
             "--break-system-packages", "pip", "setuptools", "wheel"],
            "Upgrading pip with --break-system-packages...",
            show_output=True
        )

    # Step 2: Install dependencies
    print_header("STEP 2: Install Dependencies")
    
    print(f"{BLUE}→{NC} Installing packages...\n")
    
    # Try with --break-system-packages
    cmd = [sys.executable, "-m", "pip", "install", "--upgrade", "--break-system-packages"] + DEPS
    result = run_cmd(cmd, "Installing with --break-system-packages")

    if result.returncode != 0:
        # Fallback to without --break-system-packages
        print(f"{YELLOW}⚠{NC} Trying standard install...\n")
        cmd = [sys.executable, "-m", "pip", "install", "--upgrade"] + DEPS
        result = run_cmd(cmd, "Installing packages")
        
        if result.returncode != 0:
            print(f"{RED}✗{NC} Failed to install dependencies")
            print(f"Error: {result.stderr}")
            sys.exit(1)

    print(f"{GREEN}✓{NC} All dependencies installed\n")

    # Step 3: Install WHODIS package
    print_header("STEP 3: Install WHODIS")
    
    print(f"{BLUE}→{NC} Installing WHODIS package...\n")
    
    # Method 1: pip install -e (editable)
    cmd = [sys.executable, "-m", "pip", "install", "-e", str(project_root), "--break-system-packages"]
    result = run_cmd(cmd, "Installing WHODIS")

    if result.returncode != 0:
        # Method 2: Without break-system-packages
        cmd = [sys.executable, "-m", "pip", "install", "-e", str(project_root)]
        result = run_cmd(cmd, "Installing WHODIS")
        
        if result.returncode != 0:
            print(f"{RED}✗{NC} Failed to install WHODIS")
            print(f"Error: {result.stderr}")
            sys.exit(1)

    print(f"{GREEN}✓{NC} WHODIS installed\n")

    # Step 4: Setup directories
    print_header("STEP 4: Setup Configuration")
    
    dirs = {
        "Config": home / ".config" / "whodis",
        "Cache": home / ".cache" / "whodis",
        "Data": home / ".local" / "share" / "whodis",
    }

    for name, path in dirs.items():
        path.mkdir(parents=True, exist_ok=True)
        print(f"{GREEN}✓{NC} {name}: {path}")

    # Create config
    config_file = home / ".config" / "whodis" / "config.json"
    if not config_file.exists():
        config = {
            "version": version,
            "cache_enabled": True,
            "cache_ttl_days": 7,
            "timeout_seconds": 10,
            "verbose": False,
        }
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"{GREEN}✓{NC} Config created")
    
    print()

    # Step 5: Setup aliases
    print_header("STEP 5: Setup Shell Aliases")
    
    alias_line = "alias whodis='python3 -m whodis.main'"

    for rc_file, shell in [(home / ".bashrc", "bash"), (home / ".zshrc", "zsh")]:
        if rc_file.exists():
            with open(rc_file, 'r') as f:
                content = f.read()
            
            if alias_line not in content:
                with open(rc_file, 'a') as f:
                    f.write(f"\n# WHODIS alias\n{alias_line}\n")
                print(f"{GREEN}✓{NC} Alias added to .{shell}rc")
            else:
                print(f"{GREEN}✓{NC} Alias already in .{shell}rc")

    print()

    # Step 6: Verify
    print_header("STEP 6: Verify Installation")
    
    try:
        from whodis.main import main
        print(f"{GREEN}✓{NC} WHODIS module imports successfully")
    except ImportError as e:
        print(f"{YELLOW}⚠{NC} Warning: {e}")

    print(f"{GREEN}✓{NC} Python: {py_version}")
    print()

    # Summary
    print("="*70)
    print(f"{GREEN}✓ INSTALLATION COMPLETE!{NC}")
    print("="*70 + "\n")

    print(f"{BLUE}Next Steps:{NC}\n")
    print("1. Reload your shell:")
    print("   $ source ~/.bashrc   # or ~/.zshrc\n")

    print("2. Test WHODIS:")
    print("   $ whodis --help\n")

    print("3. Scan a phone number:")
    print("   $ whodis -n +6285242508966\n")

    print(f"{BLUE}Examples:{NC}\n")
    print("Verbose output:")
    print("   $ whodis -n +6285242508966 -v\n")

    print("Specific sources:")
    print("   $ whodis -n +6285242508966 -s validator,whatsapp,telegram\n")

    print("Save to file:")
    print("   $ whodis -n +6285242508966 -o results.txt\n")

    print("JSON output:")
    print("   $ whodis -n +6285242508966 -j\n")

    print(f"{BLUE}Documentation:{NC}\n")
    print("• QUICKSTART.md - Quick usage guide")
    print("• README.md - Full documentation")
    print("• INSTALL.md - Detailed installation guide\n")

    print("="*70 + "\n")
