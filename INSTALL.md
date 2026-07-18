# WHODIS — Installation Guide

## ⚡ Quick Install (Recommended)

The **installer.py** handles everything automatically:

```bash
cd /path/to/whodis
python3 installer.py
```

That's ONE command. That's it.

---

## ✅ Installation Includes

The installer automatically:

✅ Checks Python 3.8+ and pip  
✅ Upgrades pip with **PEP 668 handling** (no virtual env needed)  
✅ Installs all 9 dependencies  
✅ Installs WHODIS package  
✅ Creates config directories:
   - ~/.config/whodis/config.json
   - ~/.cache/whodis/
   - ~/.local/share/whodis/
✅ Adds shell aliases to ~/.bashrc and ~/.zshrc  
✅ Verifies everything works  
✅ Shows next steps  

**No virtual environment. No multiple commands. No complicated setup.**

---

## 🚀 After Installation

### 1. Reload your shell
```bash
source ~/.bashrc
# or
source ~/.zshrc
```

### 2. Test the command
```bash
whodis --help
```

### 3. Run your first scan
```bash
whodis -n +6285242508966
```

---

## 📋 Usage Examples

### Basic phone scan
```bash
whodis -n +6285242508966
```

### Verbose output (see what's happening)
```bash
whodis -n +6285242508966 -v
```

### Use specific sources only
```bash
whodis -n +6285242508966 -s validator,whatsapp,telegram
```

### Save results to file
```bash
whodis -n +6285242508966 -o results.txt
```

### JSON output (for scripts)
```bash
whodis -n +6285242508966 -j
```

### Force fresh scan (skip cache)
```bash
whodis -n +6285242508966 --no-cache
```

### Batch process multiple numbers
```bash
whodis -f numbers.txt -o results.json
```

### Deep scan with all options
```bash
whodis -n +6285242508966 -v -j -d --no-cache -t 15
```

---

## 📊 Available Data Sources

WHODIS checks **13+ data sources**:

| Source | Type | Returns |
|--------|------|---------|
| **Validator** | Phone Metadata | Country, Carrier, Type, Region |
| **Truecaller** | Caller ID | Name, Occupation |
| **Getcontact** | Contact DB | Name, Profile |
| **WhatsApp** | Messaging App | Account Status |
| **Telegram** | Messaging App | Username, Profile URL |
| **Instagram** | Social Media | Username, Profile |
| **Facebook** | Social Media | Profile Name, URL |
| **LinkedIn** | Professional | Profile, Job Title |
| **Twitter/X** | Social Media | Handle, URL |
| **Breach DB** | Data Leaks | Email Breaches |
| **Virtual Detector** | VoIP | Virtual Number Detection |
| **Spam Database** | Spam Reports | Report Count |
| **Forums** | Dark Web | Mentions, Posts |

---

## 🛠️ Configuration

Config file: `~/.config/whodis/config.json`

```json
{
  "version": "0.1",
  "cache_enabled": true,
  "cache_ttl_days": 7,
  "timeout_seconds": 10,
  "verbose": false
}
```

---

## 🐛 Troubleshooting

### "Command not found: whodis"

```bash
# Reload shell
source ~/.bashrc
# or
source ~/.zshrc

# Then test
whodis --help
```

### Reinstall if needed

```bash
python3 installer.py
```

### PEP 668 Errors

The installer handles this automatically. If you still get `externally-managed-environment` errors:

```bash
# Try manual install with --break-system-packages
python3 -m pip install -e . --break-system-packages
```

### Missing Python

```bash
# Ubuntu/Debian
sudo apt install python3 python3-pip

# CentOS/RHEL
sudo dnf install python3 python3-pip

# macOS
brew install python3
```

### Slow Scans

Increase timeout:
```bash
whodis -n +62... -t 30
```

### Clear Cache

```bash
rm -rf ~/.cache/whodis/*
```

---

## 🔄 Uninstall

Remove WHODIS:
```bash
pip3 uninstall whodis -y
```

Remove config and cache:
```bash
rm -rf ~/.config/whodis
rm -rf ~/.cache/whodis
rm -rf ~/.local/share/whodis
```

Remove alias from ~/.bashrc and ~/.zshrc:
```bash
# Edit and remove:
# alias whodis='python3 -m whodis.main'
```

---

## 💡 Pro Tips

### Batch processing
```bash
# Create numbers.txt (one per line)
whodis -f numbers.txt -o report.json -j
```

### Export to CSV
```bash
whodis -n +62... -o results.csv
```

### Use in scripts
```bash
whodis -n +62... -j | jq '.validator.carrier'
```

### Monitor continuously
```bash
watch 'whodis -n +62... --no-cache'
```

---

## 📚 Documentation

- **QUICKSTART.md** - Quick usage guide
- **README.md** - Full documentation
- **INSTALL_SIMPLE.md** - Simplified installation
- Run `whodis --help` for CLI options

---

## 🎉 Installation Complete!

You're all set! Run:

```bash
whodis -n +YOUR_NUMBER
```

Get real OSINT intelligence! 🔍


### 1. System Dependencies (Ubuntu/Debian)

```bash
# Update package manager
sudo apt update

# Install build tools and Python dev
sudo apt install -y \
    build-essential \
    python3 \
    python3-pip \
    python3-dev \
    libxml2-dev \
    libxslt-dev \
    libssl-dev \
    git
```

**For CentOS/RHEL/Fedora:**
```bash
sudo dnf install -y \
    gcc \
    gcc-c++ \
    python3 \
    python3-pip \
    python3-devel \
    libxml2-devel \
    libxslt-devel \
    openssl-devel
```

**For Arch Linux:**
```bash
sudo pacman -S --noconfirm \
    base-devel \
    python \
    python-pip \
    libxml2 \
    libxslt
```

### 2. Install WHODIS

```bash
# Clone repository
git clone https://github.com/yourrepo/whodis.git
cd whodis

# Install in editable mode (recommended)
pip3 install -e .

# Or install normally
pip3 install .
```

### 3. Verify Installation

```bash
# Check if command is available
which whodis

# Check version
whodis --version

# Test import
python3 -c "from whodis.main import main; print('✓ OK')"
```

---

## Troubleshooting

### Issue 1: "Command 'whodis' not found"

**Solution 1:** Add pip's bin directory to PATH
```bash
# Find pip's location
python3 -m site --user-base

# Add to ~/.bashrc (or ~/.zshrc)
export PATH="$PATH:$(python3 -m site --user-base)/bin"

# Reload shell
source ~/.bashrc
```

**Solution 2:** Use python module directly
```bash
python3 -m whodis.main -n +6285242508966
```

**Solution 3:** Create symbolic link
```bash
# Find where whodis was installed
python3 -c "import whodis; print(whodis.__file__)"

# Create symlink
sudo ln -s /path/to/whodis/main.py /usr/local/bin/whodis
```

---

### Issue 2: "ModuleNotFoundError: No module named 'phonenumbers'"

**Solution:**
```bash
# Reinstall all dependencies
pip3 install --force-reinstall --no-cache-dir -r requirements.txt

# Or specifically
pip3 install phonenumbers beautifulsoup4 lxml requests colorama tqdm
```

---

### Issue 3: "lxml" or "xml" module errors

**Ubuntu/Debian:**
```bash
sudo apt install -y libxml2-dev libxslt-dev
pip3 install --upgrade lxml
```

**CentOS/RHEL:**
```bash
sudo dnf install -y libxml2-devel libxslt-devel
pip3 install --upgrade lxml
```

---

### Issue 4: Permission denied errors

**Solution 1:** Use --user flag
```bash
pip3 install --user -e .
```

**Solution 2:** Use sudo (not recommended)
```bash
sudo pip3 install -e .
```

**Solution 3:** Fix permissions
```bash
# Check ownership
ls -la ~/.local/lib/python*/

# Fix if needed
sudo chown -R $(whoami):$(whoami) ~/.local/
```

---

### Issue 5: "pip is configured with locations that require TLS/SSL"

**Ubuntu/Debian:**
```bash
sudo apt install -y libssl-dev python3-dev
pip3 install --upgrade pip setuptools
```

**Then retry:**
```bash
pip3 install -e .
```

---

### Issue 6: Old/broken packages preventing installation

**Nuclear option - clean install:**
```bash
# Remove old installation
pip3 uninstall -y whodis

# Clear pip cache
pip3 cache purge

# Remove old requirements
rm -rf ~/.cache/pip

# Fresh install with verbose output
pip3 install --no-cache-dir -e . -v
```

---

### Issue 7: Selenium/Chrome driver issues

If you get ChromeDriver errors:

```bash
# Install chromium-browser
sudo apt install -y chromium-browser

# Or use Firefox
pip3 install geckodriver-autoinstaller

# Selenium will auto-download drivers with webdriver-manager
# Usually works automatically, but if not:
python3 -c "from webdriver_manager.chrome import ChromeDriverManager; ChromeDriverManager().install()"
```

---

## System Requirements

### Minimum
- **OS:** Linux/Ubuntu/macOS/Windows
- **Python:** 3.8+
- **RAM:** 512 MB
- **Disk:** 500 MB (including dependencies)

### Recommended
- **OS:** Ubuntu 20.04 LTS or later
- **Python:** 3.10+
- **RAM:** 2 GB
- **Disk:** 2 GB

### Required System Packages
- Python development headers (`python3-dev` or `python3-devel`)
- Build tools (`build-essential` or equivalent)
- XML libraries (`libxml2-dev`, `libxslt-dev`)
- SSL development files (`libssl-dev`)

---

## Uninstallation

### Remove WHODIS

```bash
# Uninstall package
pip3 uninstall -y whodis

# Remove development install
pip3 uninstall -y -e .

# Remove configuration (optional)
rm -rf ~/.config/whodis
```

### Remove Dependencies (optional)

```bash
# Show what was installed
pip3 list | grep -E "phonenumbers|beautifulsoup4|lxml|requests|colorama|tqdm|selenium"

# Remove specific packages (if you don't use them elsewhere)
pip3 uninstall -y phonenumbers beautifulsoup4 lxml requests colorama tqdm selenium
```

---

## Advanced Installation Options

### Install with Development Tools

```bash
# Install with dev dependencies
pip3 install -e ".[dev]"

# This includes pytest, black, flake8 for development
```

### Install from Requirements File

```bash
# Using requirements.txt
pip3 install -r requirements.txt
pip3 install -e .
```

### Install in Isolated Environment (Safe Method)

```bash
# Create virtual environment
python3 -m venv whodis_env

# Activate
source whodis_env/bin/activate

# Install
pip3 install -e .

# Use
whodis -n +6285242508966

# Deactivate when done
deactivate
```

---

## Verification Checklist

After installation, verify:

```bash
# ✓ Command available
which whodis

# ✓ Version check
whodis --version

# ✓ Help works
whodis --help

# ✓ Import works
python3 -c "import whodis; print('OK')"

# ✓ Can run scan
whodis -n +6285242508966 -v --no-cache
```

---

## Environment Variables

### Optional Configuration

```bash
# Set custom cache directory
export WHODIS_CACHE_DIR=~/.whodis/cache

# Set default timeout
export WHODIS_TIMEOUT=15

# Enable verbose logging
export WHODIS_VERBOSE=1
```

---

## Next Steps

After successful installation:

1. **Read QUICKSTART.md** for basic usage
2. **Check README.md** for full documentation
3. **Try examples**:
   ```bash
   whodis -n +6285242508966
   whodis -n +6281234567890 -s validator,whatsapp,telegram
   whodis -n +6281234567890 -o results.json -j
   ```

---

## Support

If you encounter issues:

1. Check the **Troubleshooting** section above
2. Review **error messages** carefully
3. Try **clean installation** if all else fails
4. Check **system requirements** are met

---

## Installation Log Example

```
✓ Operating System: Linux
✓ Python Version: 3.10.12
✓ pip Version: pip 23.2.1
✓ Installing system dependencies...
  Installing: build-essential... done
  Installing: libxml2-dev... done
  Installing: libxslt-dev... done
✓ Installing Python packages...
  Installing: requests... done
  Installing: beautifulsoup4... done
  Installing: lxml... done
  ... (more packages)
✓ Verifying installation...
✓ WHODIS command available globally
✓ WHODIS Installation Complete!
```

---

## Quick Reference

| Task | Command |
|------|---------|
| Install | `pip3 install -e .` |
| Update | `pip3 install --upgrade whodis` |
| Uninstall | `pip3 uninstall whodis` |
| Test | `whodis --help` |
| Run scan | `whodis -n +62xxx` |
| Show version | `whodis --version` |
| Verbose output | `whodis -n +62xxx -v` |
| Save results | `whodis -n +62xxx -o results.json` |
| Use cache | `whodis -n +62xxx` (default) |
| No cache | `whodis -n +62xxx --no-cache` |

---

Last Updated: June 2026
