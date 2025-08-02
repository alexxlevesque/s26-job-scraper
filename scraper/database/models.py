import sqlite3
import json
from datetime import datetime
from typing import Dict, List, Optional

class JobDatabase:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database with required tables"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Jobs table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS jobs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    job_id TEXT UNIQUE,
                    title TEXT NOT NULL,
                    company TEXT NOT NULL,
                    location TEXT,
                    salary_min REAL,
                    salary_max REAL,
                    description TEXT,
                    url TEXT NOT NULL,
                    source TEXT NOT NULL,
                    posted_date TEXT,
                    scraped_date TEXT DEFAULT CURRENT_TIMESTAMP,
                    is_new BOOLEAN DEFAULT 1,
                    applied BOOLEAN DEFAULT 0,
                    metadata TEXT
                )
            ''')
            
            # Create indexes for better performance
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_job_id ON jobs(job_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_source ON jobs(source)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_posted_date ON jobs(posted_date)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_is_new ON jobs(is_new)')
            
            conn.commit()
    
    def add_job(self, job_data: Dict) -> bool:
        """Add a new job to the database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT OR IGNORE INTO jobs 
                    (job_id, title, company, location, salary_min, salary_max, 
                     description, url, source, posted_date, metadata)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    job_data.get('job_id'),
                    job_data.get('title'),
                    job_data.get('company'),
                    job_data.get('location'),
                    job_data.get('salary_min'),
                    job_data.get('salary_max'),
                    job_data.get('description'),
                    job_data.get('url'),
                    job_data.get('source'),
                    job_data.get('posted_date'),
                    json.dumps(job_data.get('metadata', {}))
                ))
                
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Error adding job: {e}")
            return False
    
    def get_new_jobs(self) -> List[Dict]:
        """Get all new jobs that haven't been processed"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM jobs 
                WHERE is_new = 1 
                ORDER BY scraped_date DESC
            ''')
            
            return [dict(row) for row in cursor.fetchall()]
    
    def mark_jobs_as_processed(self, job_ids: List[str]):
        """Mark jobs as processed (not new anymore)"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            placeholders = ','.join(['?' for _ in job_ids])
            cursor.execute(f'''
                UPDATE jobs 
                SET is_new = 0 
                WHERE job_id IN ({placeholders})
            ''', job_ids)
            
            conn.commit()
    
    def job_exists(self, job_id: str) -> bool:
        """Check if a job already exists in the database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT 1 FROM jobs WHERE job_id = ?', (job_id,))
            return cursor.fetchone() is not None 