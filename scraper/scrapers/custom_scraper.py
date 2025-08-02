from .base_scraper import BaseScraper
from bs4 import BeautifulSoup
import re
from typing import List, Dict
from datetime import datetime

class CustomScraper(BaseScraper):
    def __init__(self):
        super().__init__()
    
    def scrape_jobs(self, custom_urls: List[Dict]) -> List[Dict]:
        jobs = []
        
        for url_config in custom_urls:
            if not url_config.get('enabled', True):
                continue
                
            try:
                response = self.make_request(url_config['url'])
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Try different selectors for job listings
                job_elements = self._find_job_elements(soup, url_config['name'])
                
                for element in job_elements[:10]:  # Limit to 10 jobs per custom URL
                    job = self._parse_job_element(element, url_config)
                    if job:
                        jobs.append(job)
                        
            except Exception as e:
                print(f"Error scraping custom URL {url_config['name']}: {e}")
        
        return jobs
    
    def _find_job_elements(self, soup: BeautifulSoup, source_name: str) -> List:
        """Find job elements using common selectors"""
        selectors = [
            'div[class*="job"]',
            'div[class*="position"]',
            'div[class*="career"]',
            'li[class*="job"]',
            'article[class*="job"]',
            '.job-listing',
            '.position-listing',
            '.career-listing'
        ]
        
        for selector in selectors:
            elements = soup.select(selector)
            if elements:
                return elements
        
        # Fallback: look for elements containing job-related text
        job_elements = []
        for element in soup.find_all(['div', 'li', 'article']):
            text = element.get_text().lower()
            if any(keyword in text for keyword in ['job', 'position', 'career', 'opportunity']):
                job_elements.append(element)
        
        return job_elements[:20]  # Limit results
    
    def _parse_job_element(self, element, url_config: Dict) -> Dict:
        """Parse individual job element"""
        try:
            # Extract job title
            title = self._extract_text(element, [
                'h1', 'h2', 'h3', 'h4',
                '[class*="title"]',
                '[class*="position"]',
                '[class*="job-title"]'
            ])
            
            # Extract company name
            company = self._extract_text(element, [
                '[class*="company"]',
                '[class*="employer"]',
                '[class*="organization"]'
            ]) or url_config.get('company', 'N/A')
            
            # Extract location
            location = self._extract_text(element, [
                '[class*="location"]',
                '[class*="place"]',
                '[class*="city"]'
            ]) or "N/A"
            
            # Extract job URL
            url = self._extract_url(element, url_config['url'])
            
            # Extract salary if available
            salary_text = self._extract_text(element, [
                '[class*="salary"]',
                '[class*="compensation"]',
                '[class*="pay"]'
            ])
            salary_min, salary_max = self._extract_salary(salary_text)
            
            # Generate job ID
            job_id = self.generate_job_id(title, company, url)
            
            return {
                'job_id': job_id,
                'title': title,
                'company': company,
                'location': location,
                'salary_min': salary_min,
                'salary_max': salary_max,
                'url': url,
                'source': f"custom_{url_config['name']}",
                'metadata': {
                    'source_url': url_config['url'],
                    'scraped_at': str(datetime.now())
                }
            }
            
        except Exception as e:
            print(f"Error parsing custom job element: {e}")
            return None
    
    def _extract_text(self, element, selectors: List[str]) -> str:
        """Extract text using multiple selectors"""
        for selector in selectors:
            found = element.select_one(selector)
            if found:
                text = found.get_text(strip=True)
                if text:
                    return text
        return "N/A"
    
    def _extract_url(self, element, base_url: str) -> str:
        """Extract job URL"""
        # Look for links
        link = element.find('a')
        if link and link.get('href'):
            href = link.get('href')
            if href.startswith('http'):
                return href
            elif href.startswith('/'):
                return base_url.rstrip('/') + href
            else:
                return f"{base_url}/{href}"
        
        return base_url
    
    def _extract_salary(self, salary_text: str) -> tuple:
        """Extract salary range from text"""
        if not salary_text:
            return None, None
        
        # Simple regex to extract numbers
        numbers = re.findall(r'\$?(\d+(?:,\d{3})*(?:\.\d{2})?)', salary_text)
        if len(numbers) >= 2:
            return float(numbers[0].replace(',', '')), float(numbers[1].replace(',', ''))
        elif len(numbers) == 1:
            return float(numbers[0].replace(',', '')), None
        
        return None, None 