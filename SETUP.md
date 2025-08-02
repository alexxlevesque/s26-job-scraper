# Job Scraper Setup Guide

## 🚀 Quick Start

Your job scraper project is now fully set up! Here's how to get it running:

### 1. Install Dependencies

```bash
# Navigate to the project directory
cd ~/Desktop/Projects\ 2025/job-scraper

# Install required packages
pip3 install -r requirements.txt
```

### 2. Configure Email Settings

```bash
# Copy the environment template
cp env.example .env

# Edit the .env file with your email credentials
nano .env
```

**For Gmail users:**
- Enable 2-Factor Authentication on your Google account
- Generate an App Password: https://myaccount.google.com/apppasswords
- Use the App Password instead of your regular password

Example `.env` file:
```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
RECIPIENT_EMAIL=your-email@gmail.com
```

### 3. Configure Job Preferences

Edit `config/job_sources.yaml` to customize your job search:

```yaml
job_sources:
  linkedin:
    enabled: true
    search_params:
      keywords: ["python developer", "software engineer", "data scientist"]
      location: "Remote"
      experience_level: "Entry level"
  
  indeed:
    enabled: true
    search_params:
      q: ["python", "software engineer", "data scientist"]
      l: "Remote"
      exp: "entry"

# Add custom company URLs
custom_urls:
  - name: "Your Dream Company"
    url: "https://company.com/careers"
    enabled: true
```

### 4. Test the Setup

```bash
# Run the test script to verify everything is working
python3 test_setup.py
```

### 5. Run the Scraper

```bash
# Run once to test
python3 main.py

# Run with daily scheduling (runs at 9 AM daily)
python3 run_scraper.py
```

## 📧 Email Configuration

### Gmail Setup
1. Go to your Google Account settings
2. Enable 2-Factor Authentication
3. Generate an App Password:
   - Go to Security → App passwords
   - Select "Mail" and your device
   - Copy the generated password
4. Use this password in your `.env` file

### Other Email Providers
- **Outlook/Hotmail**: Use `smtp-mail.outlook.com` port 587
- **Yahoo**: Use `smtp.mail.yahoo.com` port 587
- **Custom SMTP**: Use your provider's SMTP settings

## 🔧 Customization

### Adding Custom URLs
Add any company career page to `config/job_sources.yaml`:

```yaml
custom_urls:
  - name: "Google Careers"
    url: "https://careers.google.com/jobs/results/"
    enabled: true
  - name: "Microsoft Jobs"
    url: "https://careers.microsoft.com/us/en/search-results"
    enabled: true
```

### Job Filtering
Configure salary ranges and locations in `config/job_sources.yaml`:

```yaml
filters:
  min_salary: 60000
  max_salary: 150000
  locations: ["Remote", "New York", "San Francisco"]
  required_skills: ["python", "javascript", "aws"]
  excluded_keywords: ["senior", "lead", "manager"]
```

## ⏰ Automation

### Daily Scheduling
The scraper can run automatically every day:

```bash
# Run with built-in scheduler
python3 run_scraper.py
```

### Cron Job (Recommended)
Add to your crontab for reliable scheduling:

```bash
# Edit crontab
crontab -e

# Add this line to run daily at 9 AM
0 9 * * * cd ~/Desktop/Projects\ 2025/job-scraper && python3 main.py
```

### GitHub Actions (Cloud)
Create `.github/workflows/job-scraper.yml`:

```yaml
name: Job Scraper
on:
  schedule:
    - cron: '0 9 * * *'  # Daily at 9 AM UTC
  workflow_dispatch:  # Manual trigger

jobs:
  scrape:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - run: pip install -r requirements.txt
      - run: python main.py
```

## 🐛 Troubleshooting

### Common Issues

**Email not sending:**
- Check your `.env` file configuration
- Verify App Password for Gmail
- Check firewall/antivirus settings

**No jobs found:**
- Check your keywords in `config/job_sources.yaml`
- Some sites may block automated requests
- Try adjusting delays in `config/settings.py`

**Import errors:**
- Run `pip3 install -r requirements.txt`
- Make sure you're using Python 3.7+

### Logs
Check the logs for detailed information:
```bash
tail -f logs/scraper.log
```

## 📊 Database

The scraper uses SQLite to store job data:
- Location: `data/jobs.db`
- View with: `sqlite3 data/jobs.db`
- Backup regularly if needed

## 🔒 Security Notes

- Never commit your `.env` file to version control
- Use App Passwords instead of regular passwords
- The scraper respects robots.txt and includes delays
- Consider using proxies for high-volume scraping

## 📈 Next Steps

Once the basic scraper is working:

1. **Add more job sites** by creating new scraper classes
2. **Build a web dashboard** to view jobs and statistics
3. **Add machine learning** for job matching
4. **Integrate with job application tracking**
5. **Add Slack/Discord notifications**

## 🆘 Support

If you encounter issues:
1. Check the logs in `logs/scraper.log`
2. Run `python3 test_setup.py` to verify setup
3. Check that all dependencies are installed
4. Verify your email configuration

Happy job hunting! 🎯 