import schedule
import time
from main import JobScraper
import logging

def run_daily_scrape():
    """Run the scraper once"""
    scraper = JobScraper()
    scraper.run()

def main():
    # Schedule daily scraping at 9 AM
    schedule.every().day.at("09:00").do(run_daily_scrape)
    
    # Also run once immediately
    run_daily_scrape()
    
    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main() 