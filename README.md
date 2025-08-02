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

| Date Added | Position | Company | Location | Source | Link |
|------------|----------|---------|----------|---------|------|
| 2025-08-02 | Machine Learning — Master-Level Internsh... | Vosyn | Etobicoke, Ontario, Canada | LinkedIn | [Apply](https://ca.linkedin.com/jobs/view/machine-learning-%E2%80%94-master-level-internship-at-vosyn-4262383783?position=1&pageNum=0&refId=02C%2F%2BIkgYsAS6aQXk4Fqsg%3D%3D&trackingId=gduXoxEJs5VdVHk%2BADoDSg%3D%3D) |
| 2025-08-02 | Scrum Master — Master-Level Internship | Vosyn | Etobicoke, Ontario, Canada | LinkedIn | [Apply](https://ca.linkedin.com/jobs/view/scrum-master-%E2%80%94-master-level-internship-at-vosyn-4262382824?position=2&pageNum=0&refId=02C%2F%2BIkgYsAS6aQXk4Fqsg%3D%3D&trackingId=qFPvaKdNGYkezySuhhzOLg%3D%3D) |
| 2025-08-02 | Capital Markets — Master-Level Internshi... | Vosyn | Etobicoke, Ontario, Canada | LinkedIn | [Apply](https://ca.linkedin.com/jobs/view/capital-markets-%E2%80%94-master-level-internship-at-vosyn-4262302423?position=3&pageNum=0&refId=02C%2F%2BIkgYsAS6aQXk4Fqsg%3D%3D&trackingId=QRxudU3INrSeoH2e%2BlwXkA%3D%3D) |
| 2025-08-02 | Product Analyst Intern | Synthesis Health | Vancouver, British Columbia, C... | LinkedIn | [Apply](https://ca.linkedin.com/jobs/view/product-analyst-intern-at-synthesis-health-4264968466?position=4&pageNum=0&refId=02C%2F%2BIkgYsAS6aQXk4Fqsg%3D%3D&trackingId=7o%2BzKtS6%2BIJ3U8czxc7xpw%3D%3D) |
| 2025-08-02 | Data Associate (Fall/Winter Internship) | Lumerate | Ontario, Canada | LinkedIn | [Apply](https://ca.linkedin.com/jobs/view/data-associate-fall-winter-internship-at-lumerate-4268384479?position=5&pageNum=0&refId=02C%2F%2BIkgYsAS6aQXk4Fqsg%3D%3D&trackingId=6QsIoL11hOJmdOK6hXoqqg%3D%3D) |
| 2025-08-02 | Frontend Developer Intern - Fall 2025 Se... | Blaise Transit | Montreal, Quebec, Canada | LinkedIn | [Apply](https://ca.linkedin.com/jobs/view/frontend-developer-intern-fall-2025-semester-sept-dec-remote-canada-at-blaise-transit-4271809699?position=6&pageNum=0&refId=02C%2F%2BIkgYsAS6aQXk4Fqsg%3D%3D&trackingId=bKsbfTCriaw4IPolrDpzig%3D%3D) |
| 2025-08-02 | Social Media Intern (Remote, Paid) | EDUopinions | Canada | LinkedIn | [Apply](https://ca.linkedin.com/jobs/view/social-media-intern-remote-paid-at-eduopinions-4276230336?position=7&pageNum=0&refId=02C%2F%2BIkgYsAS6aQXk4Fqsg%3D%3D&trackingId=FqaOLlW57IxojNaeJQz5og%3D%3D) |
| 2025-08-02 | Finance — Master-Level Internship | Vosyn | Etobicoke, Ontario, Canada | LinkedIn | [Apply](https://ca.linkedin.com/jobs/view/finance-%E2%80%94-master-level-internship-at-vosyn-4263124558?position=8&pageNum=0&refId=02C%2F%2BIkgYsAS6aQXk4Fqsg%3D%3D&trackingId=yMNWhsxeUetmQFTZhNQhxA%3D%3D) |
| 2025-08-02 | Backend Developer Intern - Fall 2025 Sem... | Blaise Transit | Montreal, Quebec, Canada | LinkedIn | [Apply](https://ca.linkedin.com/jobs/view/backend-developer-intern-fall-2025-semester-sept-dec-remote-canada-at-blaise-transit-4271811490?position=9&pageNum=0&refId=02C%2F%2BIkgYsAS6aQXk4Fqsg%3D%3D&trackingId=mEA6hyg0ncvR8wyUlCFSqA%3D%3D) |
| 2025-08-02 | Market Research Analyst — Master-Level I... | Vosyn | Toronto, Ontario, Canada | LinkedIn | [Apply](https://ca.linkedin.com/jobs/view/market-research-analyst-%E2%80%94-master-level-internship-at-vosyn-4262300615?position=10&pageNum=0&refId=02C%2F%2BIkgYsAS6aQXk4Fqsg%3D%3D&trackingId=r7RfLjcJ0dzcxC28enAjlA%3D%3D) |
| 2025-08-02 | Software Engineering Intern (12 Months) | Super.com | Canada | LinkedIn | [Apply](https://ca.linkedin.com/jobs/view/software-engineering-intern-12-months-at-super-com-4224023593?position=11&pageNum=0&refId=02C%2F%2BIkgYsAS6aQXk4Fqsg%3D%3D&trackingId=KkBO1PDnzZcH9K%2Bqp%2F8qsg%3D%3D) |
| 2025-08-02 | Intern, Workplace Operations (Fall 2025) | Wealthsimple | Toronto, Ontario, Canada | LinkedIn | [Apply](https://ca.linkedin.com/jobs/view/intern-workplace-operations-fall-2025-at-wealthsimple-4263148330?position=12&pageNum=0&refId=02C%2F%2BIkgYsAS6aQXk4Fqsg%3D%3D&trackingId=v8QauL42PpMNjjJE2evhQQ%3D%3D) |
| 2025-08-02 | Project Management Specialist — Master-L... | Vosyn | Etobicoke, Ontario, Canada | LinkedIn | [Apply](https://ca.linkedin.com/jobs/view/project-management-specialist-%E2%80%94-master-level-internship-at-vosyn-4262305158?position=13&pageNum=0&refId=02C%2F%2BIkgYsAS6aQXk4Fqsg%3D%3D&trackingId=Lf1aJtTGVDnScnipLNTEFw%3D%3D) |
| 2025-08-02 | Back End Developer - Master-Level Intern... | Vosyn | Etobicoke, Ontario, Canada | LinkedIn | [Apply](https://ca.linkedin.com/jobs/view/back-end-developer-master-level-internship-at-vosyn-4262304286?position=14&pageNum=0&refId=02C%2F%2BIkgYsAS6aQXk4Fqsg%3D%3D&trackingId=%2FIn6sXxyfvrOorDq7SHrIg%3D%3D) |
| 2025-08-02 | Financial Modeling — Master-Level Intern... | Vosyn | Etobicoke, Ontario, Canada | LinkedIn | [Apply](https://ca.linkedin.com/jobs/view/financial-modeling-%E2%80%94-master-level-internship-at-vosyn-4263121744?position=15&pageNum=0&refId=02C%2F%2BIkgYsAS6aQXk4Fqsg%3D%3D&trackingId=joCWIn4SJTn2hXRimCK5CQ%3D%3D) || 2025-08-02 | Financial Modeling — Master-Level Intern... | Vosyn | Etobicoke, Ontario, Canada | LinkedIn | [Apply](https://ca.linkedin.com/jobs/view/financial-modeling-%E2%80%94-master-level-internship-at-vosyn-4263121744?position=15&pageNum=0&refId=%2FvIbUF%2FwdWXM708GdUoBJg%3D%3D&trackingId=hc6MdsuP8a1jxjfsRNf37Q%3D%3D) || 2025-08-02 | Financial Modeling — Master-Level Internship | Vosyn | Etobicoke, Ontario, Canada | LinkedIn |*Last updated: August 02, 2025*

## 📈 Database Statistics

- **Total Jobs**: 794
- **Canadian Internships**: 681
- **Sources**: LinkedIn (primary)
- **Latest Scrape**: 2025-08-02
- **Active Keywords**: intern, summer analyst, summer intern, student intern, apprenticeship, internship, co-op, coop1. **Install dependencies:**
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