# LinkedIn Job Scraper

🔍 Python tool for scraping LinkedIn job postings using Selenium.

## ⚠️ Disclaimer

This tool is for **educational purposes only**. LinkedIn's Terms of Service prohibit automated scraping. Use at your own risk and always:
- Respect rate limits
- Don't overwhelm their servers
- Consider using the official LinkedIn API for production use

## 🚀 Features

- 🔐 Automated login with credentials
- 🔍 Search jobs by keywords and location
- 📄 Extract job details (title, company, description, etc.)
- 💾 Export to JSON/CSV
- 🖼️ Headless mode support

## 📋 Requirements

- Python 3.8+
- Chrome/Chromium browser
- ChromeDriver

## 🔧 Installation

```bash
# Clone repository
git clone https://github.com/MiguelJeronimoOliveira/linkedin-job-scraper.git
cd linkedin-job-scraper

# Install dependencies
pip install -r requirements.txt

# Download ChromeDriver (match your Chrome version)
# https://chromedriver.chromium.org/downloads
```

## 📝 Configuration

Create a `.env` file:

```env
LINKEDIN_EMAIL=your_email@example.com
LINKEDIN_PASSWORD=your_password
```

## 🎯 Usage

### Basic Usage

```python
from linkedin_scraper import LinkedInJobScraper

# Initialize scraper
scraper = LinkedInJobScraper(headless=True)

# Login
scraper.login(email="your@email.com", password="yourpass")

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

### Command Line

```bash
# Search and save to JSON
python main.py --keywords "Python Developer" --location "Remote" --limit 100 --output jobs.json

# Search and save to CSV
python main.py --keywords "Data Engineer" --location "Brazil" --format csv --output jobs.csv
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
      "easy_apply": true
    }
  ]
}
```

## 🔒 Security Tips

- Never commit your `.env` file
- Use a dedicated LinkedIn account for scraping
- Enable 2FA on your main account
- Use VPN if scraping frequently

## 🛠️ Troubleshooting

### ChromeDriver Version Mismatch
```bash
# Check Chrome version
google-chrome --version

# Download matching ChromeDriver
wget https://chromedriver.storage.googleapis.com/YOUR_VERSION/chromedriver_linux64.zip
```

### LinkedIn Blocks Login
- Use headless=False to see what's happening
- Add delays between actions
- Use different User-Agent
- Consider using cookies instead of login

### Rate Limiting
- Add `time.sleep()` between requests
- Use rotating proxies
- Limit scraping to ~100 jobs/day

## 📚 Project Structure

```
linkedin-job-scraper/
├── .env.example          # Environment variables template
├── .gitignore           # Git ignore rules
├── config.py            # Configuration settings
├── linkedin_scraper.py  # Main scraper class
├── main.py              # CLI entry point
├── requirements.txt     # Python dependencies
├── utils.py             # Helper functions
└── README.md            # This file
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

<p align="center">Built with 💙 and ☕</p>
