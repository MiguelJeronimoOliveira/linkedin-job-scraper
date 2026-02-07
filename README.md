# LinkedIn Job Scraper

🔍 Python tool for scraping LinkedIn job postings using Selenium.

## ⚠️ Disclaimer

This tool is for **educational purposes only**. LinkedIn's Terms of Service prohibit automated scraping. Use at your own risk and always:
- Respect rate limits
- Don't overwhelm their servers
- Consider using the official LinkedIn API for production use

## 🚀 Features

- 🔐 Automated login with credentials **OR** cookies
- 🔒 **2FA/Captcha support** - manual login mode
- 🍪 Cookie persistence - login once, use many times
- 🔍 Search jobs by keywords and location
- 📄 Extract job details (title, company, description, etc.)
- 💾 Export to JSON/CSV
- 🖼️ Headless mode support

## 📋 Requirements

- Python 3.8+
- Chrome/Chromium browser
- ChromeDriver (auto-managed by webdriver-manager)

## 🔧 Installation

```bash
# Clone repository
git clone https://github.com/MiguelJeronimoOliveira/linkedin-job-scraper.git
cd linkedin-job-scraper

# Create virtual environment (recommended)
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## 📝 Configuration

Create a `.env` file:

```env
LINKEDIN_EMAIL=your_email@example.com
LINKEDIN_PASSWORD=your_password
```

## 🎯 Usage

### First Time Setup (with 2FA)

If you have 2FA enabled, run manual login first:

```bash
# This will open browser for you to login manually
python main.py --keywords "Python Developer" --location "Brazil" --manual-login --no-headless
```

After manual login, cookies are saved and you can run normally:

```bash
# Now runs headless with saved cookies
python main.py --keywords "Python Developer" --location "Brazil"
```

### Normal Usage (after first login)

```bash
# Basic search
python main.py --keywords "Python Developer" --location "Brazil" --limit 50

# With custom output
python main.py --keywords "Data Engineer" --location "Remote" --format csv --output jobs.csv

# Show browser window (for debugging)
python main.py --keywords "Java Developer" --no-headless
```

### Command Line Options

| Flag | Description | Default |
|------|-------------|---------|
| `--keywords, -k` | Job keywords to search | (required) |
| `--location, -l` | Job location | "" |
| `--limit, -n` | Number of jobs to scrape | 25 |
| `--output, -o` | Output filename | "linkedin_jobs" |
| `--format, -f` | Output format (json/csv/both) | json |
| `--email, -e` | LinkedIn email | from .env |
| `--password, -p` | LinkedIn password | from .env |
| `--manual-login, -m` | Login manually (for 2FA) | False |
| `--cookies, -c` | Custom cookies file | "linkedin_cookies.pkl" |
| `--no-cookies` | Don't use cookies | False |
| `--headless` | Run headless | True |
| `--no-headless` | Show browser | False |

### Python API

```python
from linkedin_scraper import LinkedInJobScraper

# Initialize scraper
scraper = LinkedInJobScraper(headless=True)

# Option 1: Auto login (uses cookies if available)
scraper.login(email="your@email.com", password="yourpass")

# Option 2: Manual login (for 2FA)
scraper.login_with_manual()

# Search for jobs
jobs = scraper.search_jobs(
    keywords="Python Developer",
    location="São Paulo, Brazil",
    limit=50
)

# Save results
scraper.save_to_json(jobs, "jobs.json")
scraper.save_to_csv(jobs, "jobs.csv")

# Close browser
scraper.close()
```

## 🍪 Cookie Management

Cookies are automatically saved after successful login:
- File: `linkedin_cookies.pkl` (default)
- Location: Same directory as script
- Usage: Automatically loaded on next run

**To force re-login:**
```bash
# Delete cookies file
rm linkedin_cookies.pkl

# Or use --no-cookies flag
python main.py --keywords "..." --no-cookies
```

## 📊 Output Format

```json
{
  "jobs": [
    {
      "title": "Senior Python Developer",
      "company": "Tech Corp",
      "location": "São Paulo, Brazil",
      "url": "https://linkedin.com/jobs/view/...",
      "description": "Job description text...",
      "posted_date": "2 days ago",
      "applicants": "45 applicants",
      "insights": ["Remote", "Full-time"],
      "scraped_at": "2026-02-07T10:30:00"
    }
  ],
  "count": 50
}
```

## 🔒 Security Tips

- Never commit your `.env` file or `linkedin_cookies.pkl`
- Both are already in `.gitignore`
- Use a dedicated LinkedIn account for scraping
- Enable 2FA on your main account
- Cookies expire after some time (~1-2 weeks)

## 🛠️ Troubleshooting

### "Login failed. Try --manual-login for 2FA."

You have 2FA enabled. Run:
```bash
python main.py --keywords "..." --manual-login --no-headless
```

### "Cookies expired"

Cookies are old. Either:
1. Delete `linkedin_cookies.pkl` and login again
2. Use `--manual-login` to refresh cookies

### ChromeDriver Version Mismatch

The `webdriver-manager` should auto-update. If not:
```bash
pip install --upgrade webdriver-manager
```

### LinkedIn Blocks Login

- Use `--no-headless` to see what's happening
- Try `--manual-login` mode
- Use a different LinkedIn account
- Wait a few hours between attempts

## 📚 Project Structure

```
linkedin-job-scraper/
├── .env                  # Your credentials (not in git)
├── .env.example          # Template for .env
├── .gitignore           # Git ignore rules
├── linkedin_cookies.pkl # Saved cookies (not in git)
├── linkedin_scraper.py  # Main scraper class
├── main.py              # CLI entry point
├── requirements.txt     # Python dependencies
├── README.md            # This file
└── linkedin_jobs.*      # Output files
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - see [LICENSE](LICENSE) file

## 👨‍💻 Author

**Miguel Jeronimo Oliveira**

---

<p align="center">Built by Treloso, the clawbot</p>

