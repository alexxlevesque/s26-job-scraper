from flask import Flask, render_template, jsonify, request
import sqlite3
from datetime import datetime
import os
from pathlib import Path
import sys

# Add the parent directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = Flask(__name__)

def get_db_connection():
    """Create a database connection"""
    # Use a temporary database for Vercel since it's read-only
    db_path = '/tmp/jobs.db'
    
    # If database doesn't exist, create a sample one
    if not os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        conn.execute('''
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
        
        # Add some sample data
        sample_jobs = [
            ('sample1', 'Software Engineering Intern', 'Tech Corp', 'Toronto, Ontario, Canada', None, None, 'Sample internship', 'https://example.com', 'linkedin', '2025-08-02', '2025-08-02 10:00:00', 1, 0, '{}'),
            ('sample2', 'Data Science Intern', 'Data Inc', 'Vancouver, British Columbia, Canada', None, None, 'Sample data internship', 'https://example.com', 'linkedin', '2025-08-02', '2025-08-02 10:00:00', 1, 0, '{}'),
            ('sample3', 'Backend Developer Intern', 'Startup Co', 'Montreal, Quebec, Canada', None, None, 'Sample backend internship', 'https://example.com', 'linkedin', '2025-08-02', '2025-08-02 10:00:00', 1, 0, '{}'),
        ]
        
        conn.executemany('''
            INSERT OR IGNORE INTO jobs 
            (job_id, title, company, location, salary_min, salary_max, 
             description, url, source, posted_date, scraped_date, is_new, applied, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', sample_jobs)
        conn.commit()
        conn.close()
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def get_jobs(limit=None, offset=0, filter_new=False):
    """Get jobs from database"""
    conn = get_db_connection()
    
    query = """
    SELECT 
        job_id,
        title,
        company,
        location,
        description,
        url,
        source,
        scraped_date as created_at,
        is_new
    FROM jobs
    """
    
    if filter_new:
        query += " WHERE is_new = 1"
    
    query += " ORDER BY scraped_date DESC"
    
    if limit:
        query += f" LIMIT {limit} OFFSET {offset}"
    
    cursor = conn.execute(query)
    jobs = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return jobs

def get_job_stats():
    """Get job statistics"""
    conn = get_db_connection()
    
    # Total jobs
    total = conn.execute("SELECT COUNT(*) FROM jobs").fetchone()[0]
    
    # New jobs
    new_jobs = conn.execute("SELECT COUNT(*) FROM jobs WHERE is_new = 1").fetchone()[0]
    
    # Jobs by source
    sources = conn.execute("""
        SELECT source, COUNT(*) as count 
        FROM jobs 
        GROUP BY source 
        ORDER BY count DESC
    """).fetchall()
    
    conn.close()
    
    return {
        'total': total,
        'new_jobs': new_jobs,
        'sources': [dict(row) for row in sources]
    }

@app.route('/')
def index():
    """Main page showing job dashboard"""
    stats = get_job_stats()
    recent_jobs = get_jobs(limit=10)
    return render_template('index.html', stats=stats, recent_jobs=recent_jobs)

@app.route('/api/jobs')
def api_jobs():
    """API endpoint to get jobs"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    filter_new = request.args.get('new_only', 'false').lower() == 'true'
    
    offset = (page - 1) * per_page
    jobs = get_jobs(limit=per_page, offset=offset, filter_new=filter_new)
    
    return jsonify({
        'jobs': jobs,
        'page': page,
        'per_page': per_page,
        'has_more': len(jobs) == per_page
    })

@app.route('/api/stats')
def api_stats():
    """API endpoint to get statistics"""
    return jsonify(get_job_stats())

@app.route('/api/mark-seen/<job_id>')
def mark_seen(job_id):
    """Mark a job as seen (not new)"""
    conn = get_db_connection()
    conn.execute("UPDATE jobs SET is_new = 0 WHERE job_id = ?", (job_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/api/mark-all-seen')
def mark_all_seen():
    """Mark all jobs as seen"""
    conn = get_db_connection()
    conn.execute("UPDATE jobs SET is_new = 0")
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/api/run-scraper', methods=['POST'])
def run_scraper():
    """Run the job scraper (simplified version for Vercel)"""
    return jsonify({
        'success': True, 
        'message': 'Scraper endpoint ready. Note: Vercel is read-only, so scraping is limited.'
    })

# Vercel requires this for serverless deployment
app.debug = False

if __name__ == '__main__':
    app.run() 