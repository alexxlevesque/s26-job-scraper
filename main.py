import yaml
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict

from scraper.database.models import JobDatabase
from scraper.scrapers.linkedin_scraper import LinkedInScraper
from scraper.scrapers.custom_scraper import CustomScraper
from scraper.notifications.email_notifier import EmailNotifier
from config.settings import DATABASE_PATH, LOG_FILE, LOG_LEVEL

class JobScraper:
    def __init__(self):
        self.setup_logging()
        self.db = JobDatabase(DATABASE_PATH)
        self.email_notifier = EmailNotifier()
        self.config = self.load_config()
        
        # Initialize scrapers
        self.scrapers = {
            'linkedin': LinkedInScraper(),
            'custom': CustomScraper()
        }
    
    def setup_logging(self):
        """Setup logging configuration"""
        Path('logs').mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=getattr(logging, LOG_LEVEL),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(LOG_FILE),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def load_config(self) -> Dict:
        """Load configuration from YAML file"""
        try:
            with open('config/job_sources.yaml', 'r') as file:
                return yaml.safe_load(file)
        except Exception as e:
            self.logger.error(f"Error loading config: {e}")
            return {}
    
    def run_scraping(self) -> List[Dict]:
        """Run all scrapers and return new jobs"""
        all_new_jobs = []
        
        self.logger.info("🚀 Starting job scraping...")
        
        # Scrape from major job sites
        for source, scraper in self.scrapers.items():
            if source == 'custom':
                continue  # Handle custom URLs separately
                
            if not self.config.get('job_sources', {}).get(source, {}).get('enabled', True):
                continue
            
            try:
                self.logger.info(f"Scraping {source}...")
                search_params = self.config['job_sources'][source]['search_params']
                jobs = scraper.scrape_jobs(search_params)
                
                # Filter and add new jobs
                new_jobs = self._process_jobs(jobs, source)
                all_new_jobs.extend(new_jobs)
                
                self.logger.info(f"Found {len(new_jobs)} new jobs from {source}")
                
            except Exception as e:
                self.logger.error(f"Error scraping {source}: {e}")
        
        # Scrape custom URLs
        custom_urls = self.config.get('custom_urls', [])
        if custom_urls:
            try:
                self.logger.info("Scraping custom URLs...")
                jobs = self.scrapers['custom'].scrape_jobs(custom_urls)
                new_jobs = self._process_jobs(jobs, 'custom')
                all_new_jobs.extend(new_jobs)
                
                self.logger.info(f"Found {len(new_jobs)} new jobs from custom URLs")
                
            except Exception as e:
                self.logger.error(f"Error scraping custom URLs: {e}")
        
        return all_new_jobs
    
    def _process_jobs(self, jobs: List[Dict], source: str) -> List[Dict]:
        """Process jobs and add new ones to database"""
        new_jobs = []
        
        for job in jobs:
            if not self.db.job_exists(job['job_id']):
                if self.db.add_job(job):
                    new_jobs.append(job)
        
        return new_jobs
    
    def send_notifications(self, new_jobs: List[Dict]):
        """Send email notifications for new jobs"""
        if new_jobs:
            self.email_notifier.send_job_notifications(new_jobs)
        else:
            self.logger.info("No new jobs to notify about")
    
    def run(self):
        """Main execution method"""
        try:
            # Run scraping
            new_jobs = self.run_scraping()
            
            # Send notifications
            self.send_notifications(new_jobs)
            
            self.logger.info(f"✅ Scraping completed! Found {len(new_jobs)} new jobs")
            
        except Exception as e:
            self.logger.error(f"❌ Error in main execution: {e}")

if __name__ == "__main__":
    scraper = JobScraper()
    scraper.run() 