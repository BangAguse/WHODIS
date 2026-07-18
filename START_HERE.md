# 🔍 WHODIS — START HERE

Welcome to WHODIS — Full OSINT Phone Number Investigator!

---

## ⚡ Installation (One Command)

```bash
python3 installer.py
```

Then reload your shell:
```bash
source ~/.bashrc
```

Done! You now have `whodis` command available globally.

---

## 🚀 First Scan

```bash
whodis -n +6285242508966
```

Real OSINT data from **13+ sources** will appear in seconds.

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| **START_HERE.md** | This file - quick overview |
| **QUICKSTART.md** | Usage examples & common patterns |
| **README.md** | Full feature documentation |
| **INSTALL.md** | Complete installation guide |
| **INSTALLATION_SUCCESS.md** | What was installed & verified |
| **IMPLEMENTATION_SUMMARY.md** | Technical improvements made |

---

## 💡 Common Commands

```bash
# Show help
whodis --help

# Basic scan
whodis -n +6285242508966

# Verbose (see all operations)
whodis -n +6285242508966 -v

# Specific sources only
whodis -n +6285242508966 -s validator,telegram,whatsapp

# Save to file
whodis -n +6285242508966 -o results.txt

# JSON output
whodis -n +6285242508966 -j

# Skip cache (fresh data)
whodis -n +6285242508966 --no-cache

# Batch process
whodis -f numbers.txt -o results.json -j

# Deep scan
whodis -n +6285242508966 -d -v
```

---

## 🎯 What WHODIS Does

Investigates phone numbers across **13+ data sources**:

✅ **Validator** - Phone metadata (country, carrier, type)  
✅ **Truecaller** - Caller ID & name lookup  
✅ **Getcontact** - Contact database  
✅ **WhatsApp** - Registration status  
✅ **Telegram** - Username & profile  
✅ **Instagram** - Profile search  
✅ **Facebook** - Profile lookup  
✅ **LinkedIn** - Professional profile  
✅ **Twitter/X** - Account search  
✅ **Breach DB** - Data leak detection  
✅ **Virtual Detector** - VoIP detection  
✅ **Spam Database** - Spam reports  
✅ **Forums** - Dark web mentions  

---

## 🔧 Configuration

Edit file: `~/.config/whodis/config.json`

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

## 📂 File Structure

```
~/.config/whodis/
  └── config.json         # Settings

~/.cache/whodis/
  └── [cache files]       # Results cache (7 days)

~/.local/share/whodis/
  └── [data files]        # Additional data
```

---

## ✅ Verification

Is everything working?

```bash
# Check command is available
which whodis

# Show version
whodis --version

# Run test scan
whodis -n +6285242508966 --no-cache
```

---

## 🛠️ Troubleshooting

### Command not found
```bash
source ~/.bashrc
```

### Module errors
```bash
python3 installer.py
```

### Slow scans
```bash
whodis -n +62... -t 30
```

### Clear cache
```bash
rm -rf ~/.cache/whodis/*
```

---

## 📖 Next Steps

1. **Read QUICKSTART.md** for usage patterns
2. **Check README.md** for full features
3. **Try examples** with your own phone numbers
4. **Explore options** with `whodis --help`

---

## 🎉 You're Ready!

Everything is installed and configured.

Now use WHODIS to investigate phone numbers:

```bash
whodis -n +YOUR_PHONE_NUMBER
```

Happy investigating! 🔍

---

## 📝 Quick Reference

| Task | Command |
|------|---------|
| Help | `whodis --help` |
| Test | `whodis -n +62...` |
| Verbose | `whodis -n +62... -v` |
| Save file | `whodis -n +62... -o results.txt` |
| JSON | `whodis -n +62... -j` |
| No cache | `whodis -n +62... --no-cache` |
| Batch | `whodis -f file.txt -o results.json` |
| Deep | `whodis -n +62... -d` |

---

**All set! Start investigating! 🔍**
