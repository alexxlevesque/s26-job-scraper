#!/usr/bin/env python3
"""
README Updater - Automatically updates the README.md with latest scraped jobs
"""

import sqlite3
import os
import re
from datetime import datetime
import subprocess
import sys

def get_db_connection():
    """Get database connection"""
    db_path = os.path.join(os.path.dirname(__file__), 'data', 'jobs.db')
    return sqlite3.connect(db_path)

def get_latest_jobs(limit=15):
    """Get the latest jobs from database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = """
    SELECT 
        scraped_date,
        title,
        company,
        location,
        'LinkedIn' as source
    FROM jobs 
    WHERE location LIKE '%Canada%' 
       OR location LIKE '%Ontario%'
       OR location LIKE '%Quebec%'
       OR location LIKE '%British Columbia%'
       OR location LIKE '%Alberta%'
       OR location LIKE '%Manitoba%'
       OR location LIKE '%Saskatchewan%'
       OR location LIKE '%Nova Scotia%'
       OR location LIKE '%New Brunswick%'
       OR location LIKE '%Newfoundland%'
       OR location LIKE '%Prince Edward Island%'
       OR location LIKE '%Northwest Territories%'
       OR location LIKE '%Nunavut%'
       OR location LIKE '%Yukon%'
       OR location LIKE '%Remote%'
    ORDER BY scraped_date DESC 
    LIMIT ?
    """
    
    cursor.execute(query, (limit,))
    jobs = cursor.fetchall()
    conn.close()
    return jobs

def format_date(date_str):
    """Format date string to YYYY-MM-DD"""
    if not date_str:
        return datetime.now().strftime('%Y-%m-%d')
    
    try:
        # Handle different date formats
        if isinstance(date_str, str):
            # Try to parse the date string
            date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            return date_obj.strftime('%Y-%m-%d')
        else:
            return datetime.now().strftime('%Y-%m-%d')
    except:
        return datetime.now().strftime('%Y-%m-%d')

def update_readme_table(jobs):
    """Update the README.md file with new job data"""
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    
    # Read current README
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Create new table content
    table_lines = [
        "| Date Added | Position | Company | Location | Source |",
        "|------------|----------|---------|----------|---------|"
    ]
    
    for job in jobs:
        scraped_date, title, company, location, source = job
        date_formatted = format_date(scraped_date)
        
        # Clean and truncate fields for table display
        title_clean = (title or "N/A")[:50] + "..." if len(title or "") > 50 else (title or "N/A")
        company_clean = (company or "N/A")[:30] + "..." if len(company or "") > 30 else (company or "N/A")
        location_clean = (location or "N/A")[:40] + "..." if len(location or "") > 40 else (location or "N/A")
        
        table_lines.append(f"| {date_formatted} | {title_clean} | {company_clean} | {location_clean} | {source} |")
    
    # Create the new table section
    new_table_section = "\n".join(table_lines)
    
    # Update the last updated date
    current_date = datetime.now().strftime('%B %d, %Y')
    
    # Replace the table section in README
    # Find the table section and replace it
    table_pattern = r'(\| Date Added \| Position \| Company \| Location \| Source \|\n\|-+\|.*?\n(?:\|.*\|\n)*)'
    
    if re.search(table_pattern, content, re.DOTALL):
        # Replace existing table
        new_content = re.sub(table_pattern, new_table_section, content, flags=re.DOTALL)
    else:
        # If no table found, this shouldn't happen but handle it
        print("Warning: Could not find existing table in README")
        return False
    
    # Update the last updated line
    last_updated_pattern = r'\*Last updated: .*\*'
    new_last_updated = f'*Last updated: {current_date}*'
    new_content = re.sub(last_updated_pattern, new_last_updated, new_content)
    
    # Write updated content back to README
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True

def get_database_stats():
    """Get database statistics"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Total jobs
    cursor.execute("SELECT COUNT(*) FROM jobs")
    total_jobs = cursor.fetchone()[0]
    
    # Canadian jobs
    cursor.execute("""
        SELECT COUNT(*) FROM jobs 
        WHERE location LIKE '%Canada%' 
           OR location LIKE '%Ontario%'
           OR location LIKE '%Quebec%'
           OR location LIKE '%British Columbia%'
           OR location LIKE '%Alberta%'
           OR location LIKE '%Manitoba%'
           OR location LIKE '%Saskatchewan%'
           OR location LIKE '%Nova Scotia%'
           OR location LIKE '%New Brunswick%'
           OR location LIKE '%Newfoundland%'
           OR location LIKE '%Prince Edward Island%'
           OR location LIKE '%Northwest Territories%'
           OR location LIKE '%Nunavut%'
           OR location LIKE '%Yukon%'
           OR location LIKE '%Remote%'
    """)
    canadian_jobs = cursor.fetchone()[0]
    
    # Latest scrape date
    cursor.execute("SELECT MAX(scraped_date) FROM jobs")
    latest_scrape = cursor.fetchone()[0]
    
    conn.close()
    
    return {
        'total_jobs': total_jobs,
        'canadian_jobs': canadian_jobs,
        'latest_scrape': latest_scrape
    }

def update_readme_stats(stats):
    """Update the database statistics section"""
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Format latest scrape date
    latest_date = format_date(stats['latest_scrape'])
    
    # Create new stats section
    new_stats_section = f"""## 📈 Database Statistics

- **Total Jobs**: {stats['total_jobs']:,}
- **Canadian Internships**: {stats['canadian_jobs']:,}
- **Sources**: LinkedIn (primary)
- **Latest Scrape**: {latest_date}
- **Active Keywords**: intern, summer analyst, summer intern, student intern, apprenticeship, internship, co-op, coop"""
    
    # Replace stats section
    stats_pattern = r'(## 📈 Database Statistics\n\n- \*\*Total Jobs\*\*: .*?\n- \*\*Active Keywords\*\*: .*?\n)'
    
    if re.search(stats_pattern, content, re.DOTALL):
        new_content = re.sub(stats_pattern, new_stats_section, content, flags=re.DOTALL)
    else:
        print("Warning: Could not find stats section in README")
        return False
    
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True

def git_commit_and_push():
    """Commit and push changes to git"""
    try:
        # Add README.md
        subprocess.run(['git', 'add', 'README.md'], check=True, capture_output=True)
        
        # Commit with timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        commit_message = f"Auto-update README with latest scraped jobs - {timestamp}"
        subprocess.run(['git', 'commit', '-m', commit_message], check=True, capture_output=True)
        
        # Push to remote
        subprocess.run(['git', 'push'], check=True, capture_output=True)
        
        print(f"✅ Successfully updated README and pushed to GitHub at {timestamp}")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Git operation failed: {e}")
        return False

def main():
    """Main function to update README"""
    print("🔄 Updating README with latest scraped jobs...")
    
    try:
        # Get latest jobs
        jobs = get_latest_jobs(15)
        
        if not jobs:
            print("⚠️  No jobs found in database")
            return
        
        print(f"📊 Found {len(jobs)} latest jobs")
        
        # Update the table
        if update_readme_table(jobs):
            print("✅ Updated jobs table in README")
        else:
            print("❌ Failed to update jobs table")
            return
        
        # Get and update stats
        stats = get_database_stats()
        if update_readme_stats(stats):
            print("✅ Updated database statistics")
        else:
            print("❌ Failed to update statistics")
        
        # Commit and push
        if git_commit_and_push():
            print("🎉 README update complete!")
        else:
            print("⚠️  README updated locally but failed to push to GitHub")
            
    except Exception as e:
        print(f"❌ Error updating README: {e}")
        return False

if __name__ == "__main__":
    main() 