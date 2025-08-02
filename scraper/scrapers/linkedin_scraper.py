from .base_scraper import BaseScraper
from bs4 import BeautifulSoup
import re
from typing import List, Dict
import json
from datetime import datetime

class LinkedInScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.base_url = "https://www.linkedin.com/jobs/search"
    
    def scrape_jobs(self, search_params: Dict) -> List[Dict]:
        jobs = []
        
        keywords = search_params.get('keywords', [])
        location = search_params.get('location', 'Canada')
        
        for keyword in keywords:
            url = self._build_search_url(keyword, location, search_params)
            
            try:
                response = self.make_request(url)
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Find job listings
                job_cards = soup.find_all('div', class_='base-card')
                
                for card in job_cards[:20]:  # Limit to 20 jobs per search
                    job = self._parse_job_card(card, keyword)
                    if job:
                        jobs.append(job)
                        
            except Exception as e:
                print(f"Error scraping LinkedIn for {keyword}: {e}")
        
        return jobs
    
    def _build_search_url(self, keyword: str, location: str, params: Dict) -> str:
        """Build LinkedIn search URL"""
        base_params = {
            'keywords': keyword,
            'location': location,
            'f_E': params.get('experience_level', '1'),  # Entry level
            'f_JT': 'I',  # Internship
            'f_WT': '1,2',  # On-site and Remote
            'start': 0
        }
        
        query_string = '&'.join([f"{k}={v}" for k, v in base_params.items()])
        return f"{self.base_url}?{query_string}"
    
    def _parse_job_card(self, card, keyword: str) -> Dict:
        """Parse individual job card"""
        try:
            # Extract job title
            title_elem = card.find('h3', class_='base-search-card__title')
            title = title_elem.get_text(strip=True) if title_elem else "N/A"
            
            # Extract company name
            company_elem = card.find('h4', class_='base-search-card__subtitle')
            company = company_elem.get_text(strip=True) if company_elem else "N/A"
            
            # Extract location
            location_elem = card.find('span', class_='job-search-card__location')
            location = location_elem.get_text(strip=True) if location_elem else "N/A"
            
            # Extract job URL
            link_elem = card.find('a', class_='base-card__full-link')
            url = link_elem.get('href') if link_elem else ""
            
            # Extract posted date
            date_elem = card.find('time')
            posted_date = date_elem.get('datetime') if date_elem else ""
            
            # Generate job ID
            job_id = self.generate_job_id(title, company, url)
            
            return {
                'job_id': job_id,
                'title': title,
                'company': company,
                'location': location,
                'url': url,
                'posted_date': posted_date,
                'source': 'linkedin',
                'metadata': {
                    'keyword': keyword,
                    'scraped_at': str(datetime.now())
                }
            }
            
        except Exception as e:
            print(f"Error parsing LinkedIn job card: {e}")
            return None 