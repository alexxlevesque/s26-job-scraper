# Job Scraper

A Python-based job monitoring system that scrapes LinkedIn for Canadian internship and student opportunities and sends email notifications.

## Features

- 🔍 Scrapes LinkedIn for Canadian internships
- 📋 Supports custom URL scraping
- 📧 Email notifications for new jobs
- 💾 SQLite database for job tracking
- 🎯 Smart filtering and deduplication
- ⏰ Automated daily scraping
- 🇨🇦 Focused on Canadian job market
- 🎓 Specialized for student and internship opportunities

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure email settings:**
   - Copy `env.example` to `.env`
   - Add your email credentials
   - For Gmail, use an App Password

3. **Configure job sources:**
   - Edit `config/job_sources.yaml`
   - Add your preferred keywords and locations
   - Add custom URLs to monitor

4. **Run the scraper:**
   ```bash
   # Run once
   python main.py
   
   # Run with scheduling
   python run_scraper.py
   ```

## Configuration

### Job Sources (`config/job_sources.yaml`)
- Configure search keywords and locations
- Enable/disable specific job sites
- Add custom URLs to monitor

### Email Settings (`.env`)
- SMTP server configuration
- Email credentials
- Recipient email address

## Usage

### Manual Run
```bash
python main.py
```

### Scheduled Run
```bash
python run_scraper.py
```

### Cron Job (Linux/Mac)
```bash
# Add to crontab
0 9 * * * cd /path/to/job-scraper && python main.py
```

## Customization

### Adding New Job Sites
1. Create a new scraper class in `scraper/scrapers/`
2. Inherit from `BaseScraper`
3. Implement the `scrape_jobs` method
4. Add configuration to `job_sources.yaml`

### Custom URL Scraping
Add URLs to the `custom_urls` section in `config/job_sources.yaml`:

```yaml
custom_urls:
  - name: "Company Careers"
    url: "https://company.com/careers"
    enabled: true
```

## Troubleshooting

### Email Issues
- Check SMTP settings in `.env`
- For Gmail, ensure 2FA is enabled and use App Password
- Check firewall/antivirus settings

### Scraping Issues
- Some sites may block automated requests
- Try adjusting delays in `config/settings.py`
- Check if site structure has changed

## License

MIT License 