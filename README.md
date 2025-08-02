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

## 📊 Latest Scraped Internships

| Date Added | Position | Company | Location | Source |
|------------|----------|---------|----------|---------|
| 2025-08-02 | Machine Learning — Master-Level Internship | Vosyn | Etobicoke, Ontario, Canada | LinkedIn |
| 2025-08-02 | Scrum Master — Master-Level Internship | Vosyn | Etobicoke, Ontario, Canada | LinkedIn |
| 2025-08-02 | Capital Markets — Master-Level Internship | Vosyn | Etobicoke, Ontario, Canada | LinkedIn |
| 2025-08-02 | Product Analyst Intern | Synthesis Health | Vancouver, British Columbia, Canada | LinkedIn |
| 2025-08-02 | Social Media Intern (Remote, Paid) | EDUopinions | Canada | LinkedIn |
| 2025-08-02 | Data Associate (Fall/Winter Internship) | Lumerate | Ontario, Canada | LinkedIn |
| 2025-08-02 | Finance — Master-Level Internship | Vosyn | Etobicoke, Ontario, Canada | LinkedIn |
| 2025-08-02 | Backend Developer Intern - Fall 2025 Semester (Sep... | Blaise Transit | Montreal, Quebec, Canada | LinkedIn |
| 2025-08-02 | Market Research Analyst — Master-Level Internship | Vosyn | Toronto, Ontario, Canada | LinkedIn |
| 2025-08-02 | Software Engineering Intern (12 Months) | Super.com | Canada | LinkedIn |
| 2025-08-02 | Intern, Workplace Operations (Fall 2025) | Wealthsimple | Toronto, Ontario, Canada | LinkedIn |
| 2025-08-02 | Project Management Specialist — Master-Level Inter... | Vosyn | Etobicoke, Ontario, Canada | LinkedIn |
| 2025-08-02 | Back End Developer - Master-Level Internship | Vosyn | Etobicoke, Ontario, Canada | LinkedIn |
| 2025-08-02 | Financial Modeling — Master-Level Internship | Vosyn | Etobicoke, Ontario, Canada | LinkedIn |
| 2025-08-02 | Software Intern Fall 2025 | Rocket Lab | Toronto, Ontario, Canada | LinkedIn |
*Last updated: August 02, 2025*

## 📈 Database Statistics

- **Total Jobs**: 344
- **Canadian Internships**: 231
- **Sources**: LinkedIn (primary)
- **Latest Scrape**: 2025-08-02
- **Active Keywords**: intern, summer analyst, summer intern, student intern, apprenticeship, internship, co-op, coop
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