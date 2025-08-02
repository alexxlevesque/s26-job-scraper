from flask import Flask, render_template, jsonify, request
import sqlite3
from datetime import datetime
import os
from pathlib import Path

app = Flask(__name__)

def get_db_connection():
    """Create a database connection"""
    db_path = 'data/jobs.db'
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
    
    query += " ORDER BY created_at DESC"
    
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
    """Run the job scraper (simplified version)"""
    return jsonify({
        'success': True, 
        'message': 'Scraper endpoint ready. Use python3 main.py to run the scraper separately.'
    })

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    Path('templates').mkdir(exist_ok=True)
    Path('static').mkdir(exist_ok=True)
    
    print("🚀 Job Scraper Dashboard starting...")
    print("📊 Access the dashboard at: http://localhost:5001")
    print("🔧 To run the scraper: python3 main.py")
    
    app.run(debug=True, host='0.0.0.0', port=5001) 