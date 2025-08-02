import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict
from config.settings import EMAIL_HOST, EMAIL_PORT, EMAIL_USER, EMAIL_PASSWORD, RECIPIENT_EMAIL

class EmailNotifier:
    def __init__(self):
        self.host = EMAIL_HOST
        self.port = EMAIL_PORT
        self.username = EMAIL_USER
        self.password = EMAIL_PASSWORD
        self.recipient = RECIPIENT_EMAIL
    
    def send_job_notifications(self, new_jobs: List[Dict]) -> bool:
        """Send email notification with new jobs"""
        if not new_jobs:
            return True
        
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"🚀 {len(new_jobs)} New Job Opportunities Found!"
            msg['From'] = self.username
            msg['To'] = self.recipient
            
            # Create HTML content
            html_content = self._create_html_content(new_jobs)
            msg.attach(MIMEText(html_content, 'html'))
            
            # Send email
            with smtplib.SMTP(self.host, self.port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)
            
            print(f"✅ Email notification sent with {len(new_jobs)} new jobs")
            return True
            
        except Exception as e:
            print(f"❌ Error sending email notification: {e}")
            return False
    
    def _create_html_content(self, jobs: List[Dict]) -> str:
        """Create HTML email content"""
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
                .header { background: #0073b1; color: white; padding: 20px; text-align: center; }
                .job-card { border: 1px solid #ddd; margin: 10px 0; padding: 15px; border-radius: 5px; }
                .job-title { font-size: 18px; font-weight: bold; color: #0073b1; margin-bottom: 5px; }
                .company { font-weight: bold; color: #666; }
                .location { color: #888; font-size: 14px; }
                .salary { color: #28a745; font-weight: bold; }
                .apply-btn { background: #0073b1; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block; margin-top: 10px; }
                .source { font-size: 12px; color: #999; margin-top: 5px; }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🎯 New Job Opportunities</h1>
                <p>Found {count} new positions matching your criteria</p>
            </div>
        """.format(count=len(jobs))
        
        for job in jobs:
            salary_text = ""
            if job.get('salary_min') and job.get('salary_max'):
                salary_text = f"💰 ${job['salary_min']:,.0f} - ${job['salary_max']:,.0f}"
            elif job.get('salary_min'):
                salary_text = f"💰 ${job['salary_min']:,.0f}+"
            
            html += f"""
            <div class="job-card">
                <div class="job-title">{job['title']}</div>
                <div class="company">{job['company']}</div>
                <div class="location">📍 {job['location']}</div>
                {f'<div class="salary">{salary_text}</div>' if salary_text else ''}
                <a href="{job['url']}" class="apply-btn" target="_blank">View Job</a>
                <div class="source">Source: {job['source']}</div>
            </div>
            """
        
        html += """
        </body>
        </html>
        """
        
        return html 