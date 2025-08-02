from abc import ABC, abstractmethod
from typing import List, Dict
import requests
import time
import random
from config.settings import USER_AGENTS, REQUEST_DELAY

class BaseScraper(ABC):
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': random.choice(USER_AGENTS)
        })
    
    def make_request(self, url: str, retries: int = 3) -> requests.Response:
        """Make a request with retry logic and delays"""
        for attempt in range(retries):
            try:
                response = self.session.get(url, timeout=30)
                response.raise_for_status()
                
                # Add delay between requests
                time.sleep(random.uniform(REQUEST_DELAY, REQUEST_DELAY + 2))
                
                return response
            except requests.RequestException as e:
                if attempt == retries - 1:
                    raise e
                time.sleep(2 ** attempt)  # Exponential backoff
        
        raise requests.RequestException("Max retries exceeded")
    
    @abstractmethod
    def scrape_jobs(self, search_params: Dict) -> List[Dict]:
        """Scrape jobs from the source"""
        pass
    
    def generate_job_id(self, title: str, company: str, url: str) -> str:
        """Generate a unique job ID"""
        import hashlib
        content = f"{title}_{company}_{url}"
        return hashlib.md5(content.encode()).hexdigest() 