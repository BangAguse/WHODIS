# WHODIS — Quick Start Guide 🚀

## Installation & Setup

### Step 1: Navigate to project directory
```bash
cd ~/Mylab/WHODIS
```

### Step 2: Activate virtual environment
```bash
source venv/bin/activate
```

### Step 3: Run WHODIS

## 📱 Basic Usage Examples

### Single Number Investigation
```bash
# Simple investigation
python3 -m whodis.main -n +62812345678

# With verbose output
python3 -m whodis.main -n +62812345678 -v

# JSON format
python3 -m whodis.main -n +62812345678 -j

# Save to file
python3 -m whodis.main -n +62812345678 -o results.json
```

### Specific Sources Only
```bash
# Only Truecaller and WhatsApp
python3 -m whodis.main -n +62812345678 -s truecaller,whatsapp

# Only validator (fastest)
python3 -m whodis.main -n +62812345678 -s validator
```

### Batch Processing
```bash
# Create file with numbers (one per line)
cat > numbers.txt << EOF
+62812345678
+62813456789
+62814567890
EOF

# Process all numbers
python3 -m whodis.main -f numbers.txt -v

# Save to file
python3 -m whodis.main -f numbers.txt -o batch_results.json
```

### Advanced Features
```bash
# Deep scan (includes forum searches)
python3 -m whodis.main -n +62812345678 -d

# Skip cache (force fresh request)
python3 -m whodis.main -n +62812345678 --no-cache

# Custom timeout
python3 -m whodis.main -n +62812345678 -t 20
```

## 🎯 Available Sources

1. **validator** - Phone number validation & metadata
2. **truecaller** - Truecaller lookup
3. **getcontact** - GetContact lookup
4. **whatsapp** - WhatsApp registration check
5. **telegram** - Telegram presence check
6. **instagram** - Instagram profile search
7. **facebook** - Facebook profile search
8. **linkedin** - LinkedIn profile search
9. **twitter** - Twitter/X account search
10. **breach** - Data breach check
11. **virtual** - Virtual/VoIP detection
12. **spam** - Spam database lookup
13. **forum** - Forum & web mention search

## 📊 Export Formats

```bash
# JSON export
python3 -m whodis.main -n +62812345678 -o results.json

# CSV export
python3 -m whodis.main -n +62812345678 -o results.csv

# TXT export
python3 -m whodis.main -n +62812345678 -o results.txt
```

## 🛠️ Troubleshooting

### Command not found?
Make sure virtual environment is activated:
```bash
source venv/bin/activate
```

### Dependencies error?
Reinstall dependencies:
```bash
pip install -r requirements.txt
```

### Getting blocked?
Use `--no-cache` or adjust timeout:
```bash
python3 -m whodis.main -n +62812345678 --no-cache -t 20
```

### No results found?
Try with verbose mode to debug:
```bash
python3 -m whodis.main -n +62812345678 -v
```

## 📁 Project Structure

```
WHODIS/
├── whodis/
│   ├── sources/          # Data source modules
│   ├── utils/            # Utility modules
│   ├── data/             # Data files (JSON)
│   ├── main.py           # CLI entry point
│   └── __main__.py       # Module entry point
├── cache/                # Cached results
├── venv/                 # Virtual environment
├── requirements.txt      # Dependencies
├── setup.py              # Package setup
└── README.md             # Full documentation
```

## 🔧 Tips & Tricks

### Speed up investigation
- Use specific sources: `-s validator,whatsapp`
- Use cache (enabled by default)
- Skip deep scan (don't use `-d`)

### Better results
- Use international format (+62...)
- Enable verbose mode (`-v`)
- Try deep scan (`-d`)
- Clear cache and retry (`--no-cache`)

### Batch processing
- Put numbers in a text file
- Use `-f filename.txt`
- Combine with `-o output.json` to save results

## 📞 Phone Number Format

Always use international format:

| Country | Format |
|---------|--------|
| Indonesia | +62... |
| Malaysia | +60... |
| Singapore | +65... |
| USA | +1... |
| UK | +44... |
| Australia | +61... |

## ⚠️ Important Notes

- Only investigate numbers you own or have permission to investigate
- This tool is for educational purposes and authorized security research
- Results depend on data source availability
- Some sources may require API keys in the future

## 🎓 Learning Resources

- Read full README.md for detailed documentation
- Check help message: `python3 -m whodis.main --help`
- Review source code in `whodis/sources/` folder
- Check cache folder to understand data structure

## 🐛 Reporting Issues

If you encounter issues:
1. Check verbose output: `-v`
2. Review error messages
3. Try with `--no-cache`
4. Check README.md for troubleshooting
5. Verify internet connection
6. Try a different source with `-s`

---

**Happy investigating! 🎯**
