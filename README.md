# WHODIS — Full OSINT Phone Number Investigator 📱🔍

**WHODIS** is a powerful command-line OSINT tool for investigating phone numbers across 13+ data sources. It automatically searches public databases, social media, breach records, and more to identify phone number owners.

## 🎯 Purpose

Investigate the ownership of any phone number by gathering intelligence from:
- ✅ Phone number validators (Truecaller, GetContact)
- ✅ Messaging platforms (WhatsApp, Telegram)
- ✅ Social media (Instagram, Facebook, LinkedIn, Twitter)
- ✅ Data breach databases
- ✅ Virtual number detection
- ✅ Spam database checks
- ✅ Forum mentions and dark web searches

## 🚀 Features

- **13+ Data Sources**: Automatically search across multiple platforms
- **Smart Caching**: Avoid redundant requests using local cache
- **Batch Processing**: Investigate multiple numbers from a file
- **Multiple Export Formats**: JSON, CSV, or TXT output
- **Verbose Debugging**: Track exactly what the tool is doing
- **Anti-Bot Protection**: Random user-agents and delays to avoid detection
- **Deep Scan Mode**: Search forums and public forums (optional)
- **Color-Coded Output**: Easy-to-read results with color highlighting
- **Cross-Platform**: Works on Windows, Linux, macOS, and Kali

## 📋 Requirements

- Python 3.8 or higher
- Internet connection
- pip or conda

## 🔧 Installation

### Option 1: Install from source

```bash
# Clone repository
git clone https://github.com/yourusername/whodis.git
cd WHODIS

# Install dependencies
pip install -r requirements.txt

# Install as CLI command
pip install -e .
```

### Option 2: Manual setup

```bash
cd WHODIS

# Create virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

## 📖 Usage

### Basic Usage

```bash
# Investigate a single number
whodis -n +62812345678

# Use short form (without +)
whodis -n 62812345678

# Or run directly
python3 -m whodis.main -n +62812345678
```

### Advanced Options

```bash
# Use specific sources only (comma-separated)
whodis -n +62812345678 -s truecaller,whatsapp,instagram

# Save results to file
whodis -n +62812345678 -o results.json

# JSON output
whodis -n +62812345678 -j

# Verbose/debug mode
whodis -n +62812345678 -v

# Deep scan (includes forum searches)
whodis -n +62812345678 -d

# Skip cache (force fresh request)
whodis -n +62812345678 --no-cache

# Custom timeout (seconds)
whodis -n +62812345678 -t 15
```

### Batch Processing

```bash
# Create a file with phone numbers (one per line)
# cat numbers.txt
# +62812345678
# +62813456789
# +62814567890

# Process all numbers
whodis -f numbers.txt -o results.json -v

# Process with CSV output
whodis -f numbers.txt -o results.csv

# Process with TXT output
whodis -f numbers.txt -o results.txt
```

### Help

```bash
whodis --help
```

## 📊 Available Sources

| Source | Description | Notes |
|--------|-------------|-------|
| **validator** | Phone number validation & metadata | Always enabled |
| **truecaller** | Name, location, spam reports | Web scraping |
| **getcontact** | Contact name and tags | Web scraping |
| **whatsapp** | WhatsApp registration check | API check |
| **telegram** | Telegram presence | Limited by JS rendering |
| **instagram** | Instagram profiles search | Google Dork search |
| **facebook** | Facebook profiles search | Google Dork search |
| **linkedin** | LinkedIn profiles search | Google Dork search |
| **twitter** | Twitter/X accounts search | Google Dork search |
| **breach** | Data breach database check | HIBP-like search |
| **virtual** | Virtual/VoIP number detection | Local database |
| **spam** | Spam database lookup | Database query |
| **forum** | Forum & web mentions search | Google Dork search |

## 📖 Dokumentasi

- **[README.md](README.md)** - Dokumentasi lengkap
- **[QUICKSTART.md](QUICKSTART.md)** - Panduan cepat memulai
- **[READING_GUIDE.md](READING_GUIDE.md)** - **📌 Panduan membaca hasil WHODIS** ← START HERE!

## 📖 Cara Membaca Hasil

### Console Output (Actual Format)

```
┌─────────────────────────────────────────────────────────┐
│  HASIL INVESTIGASI WHODIS
├─────────────────────────────────────────────────────────┤
│  Nomor Target               : +62812345678
│  Sumber Ditemukan          : 3/13
└─────────────────────────────────────────────────────────┘

============================================================
✅ IDENTITAS DITEMUKAN
============================================================

📍 INSTAGRAM
   usernames           : ['johnsmith123']

📍 WHATSAPP
   active              : True
   whatsapp            : Registered

📍 FACEBOOK
   profiles            : ['John Smith']

============================================================
📊 Ringkasan Sumber
============================================================
  ✓ Instagram
  ✓ Whatsapp
  ✓ Facebook
============================================================
```

**📌 Untuk panduan lengkap membaca hasil, lihat [READING_GUIDE.md](READING_GUIDE.md)**

### JSON Output

```json
{
  "number": "+62812345678",
  "results": {
    "validator": {
      "valid": true,
      "country": "Indonesia",
      "carrier": "Telkomsel",
      "type": "MOBILE"
    },
    "truecaller": {
      "name": "Ahmad Fauzi",
      "location": "Jakarta"
    },
    "whatsapp": {
      "active": true
    }
  }
}
```

## 🔑 API Keys (Optional)

Some features may require API keys:

- **Have I Been Pwned API**: Get free at https://haveibeenpwned.com
- **Google Custom Search**: Get at https://console.cloud.google.com
- **Twitter API**: Get at https://developer.twitter.com

To use APIs:
1. Get API key from provider
2. Create `.env` file in project root:
   ```
   HIBP_API_KEY=your_key_here
   GOOGLE_API_KEY=your_key_here
   TWITTER_API_KEY=your_key_here
   ```

## 🛡️ Legal Disclaimer

**WARNING**: This tool is designed for security research and authorized investigations only.

- ⚠️ Only investigate phone numbers you own or have explicit permission to investigate
- ⚠️ Unauthorized investigation may violate privacy laws
- ⚠️ The author assumes no liability for misuse
- ⚠️ Use responsibly and ethically

## 🔒 Cache System

Results are automatically cached to avoid redundant requests:

```bash
# Cache location: ./cache/

# Skip cache for fresh results
whodis -n +62812345678 --no-cache

# Manual cache clearing
python3 -c "from whodis.utils import Cache; Cache.clear()"
```

## 🐛 Troubleshooting

### Interpreting Results

#### ✅ IDENTITAS DITEMUKAN
- Data ditemukan di setidaknya 1 sumber
- Baca setiap section dengan emoji 📍 untuk detail
- `Sumber Ditemukan: 3/13` = Data di 3 dari 13 sumber

**Contoh pembacaan:**
```
📍 INSTAGRAM
   usernames: ['profile1', 'profile2']
```
→ Nomor ini linked ke Instagram accounts: profile1, profile2

#### ❌ IDENTITAS TIDAK DITEMUKAN
- Nomor format valid tapi tidak ada di publik database
- Bisa berarti:
  - Nomor privacy/tersembunyi
  - Burner number/nomor sekali pakai
  - Nomor baru/jarang digunakan

**📌 BACA [READING_GUIDE.md](READING_GUIDE.md) UNTUK PANDUAN LENGKAP**

### Common Issues
```bash
# Increase timeout
whodis -n +62812345678 -t 20
```

### Getting Blocked (HTTP 429)
```bash
# Skip that source or use --no-cache
whodis -n +62812345678 -s truecaller,whatsapp --no-cache
```

### No Results Found
- Number may not be registered publicly
- Sources may be temporarily unavailable
- Try again with `--no-cache`
- Enable `-v` (verbose) to debug

## 📝 Configuration

Configuration in `whodis/utils/config.py`:

```python
DEFAULT_TIMEOUT = 10          # Request timeout
USER_AGENTS = [...]           # Random user agents list
SOURCES_LIST = [...]          # Available sources
```

## 🧪 Testing

```bash
# Test with a known number
whodis -n +62812345678 -v

# Batch test
whodis -f test_numbers.txt -o test_results.json
```

## 🚀 Performance

- Average investigation: **10-30 seconds** (depends on sources)
- Cached lookup: **< 1 second**
- Batch processing: **1-2 seconds per number**

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

MIT License - See LICENSE file for details

## ⚡ Changelog

### Version 0.1 (2024)
- Initial release
- 13 data sources
- Batch processing
- Multiple export formats
- Caching system
- Color output

## 👤 Author

BangAguse

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing documentation
- Review troubleshooting section

## ⚠️ Disclaimer

This tool is provided "as is" for educational and authorized security research purposes only. The author is not responsible for any misuse or damage caused by this tool. Always obtain proper authorization before investigating any phone numbers.

---

**Remember What Uncle Ben Say**: With great power comes great responsibility! 🎯

Last Updated: 2026
