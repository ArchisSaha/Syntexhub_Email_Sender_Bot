import smtplib
import csv
import os
import logging
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
from typing import List, Dict, Optional
import getpass


class EmailSenderBot:
    """
    Automated email sender bot with CSV recipient management,
    attachment support, retry logic, and detailed logging.
    """
    
    def __init__(self, smtp_server: str = "smtp.gmail.com", smtp_port: int = 587):
        """
        Initialize the Email Sender Bot.
        
        Args:
            smtp_server: SMTP server address (default: Gmail)
            smtp_port: SMTP server port (default: 587 for TLS)
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = None
        self.password = None
        self.setup_logging()
        
    def setup_logging(self):
        """Setup logging configuration."""
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        log_file = os.path.join(log_dir, f"email_bot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def authenticate(self):
        """Securely authenticate with email service provider."""
        print("\n" + "="*50)
        print("EMAIL SENDER BOT AUTHENTICATION")
        print("="*50)
        
        self.sender_email = input("Enter your email address: ").strip()
        
        print("\nFor Gmail users:")
        print("1. Enable 2-Step Verification (if not already)")
        print("2. Generate an 'App Password' at: https://myaccount.google.com/apppasswords")
        print("3. Enter the 16-character app password below\n")
        
        self.password = getpass.getpass("Enter your app password: ")
        
        # Test authentication
        if self.test_connection():
            self.logger.info(f"Successfully authenticated as: {self.sender_email}")
            print(f"\n✓ Authentication successful!")
            return True
        else:
            self.logger.error("Authentication failed")
            return False
    
    def test_connection(self) -> bool:
        """Test SMTP connection."""
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.password)
            return True
        except Exception as e:
            self.logger.error(f"Connection test failed: {str(e)}")
            return False
    
    def read_recipients_from_csv(self, csv_file: str) -> List[Dict]:
        """
        Read recipient list from CSV file.
        
        Expected CSV format:
        email,name,company,other_fields...
        
        Args:
            csv_file: Path to CSV file
            
        Returns:
            List of recipient dictionaries
        """
        recipients = []
        
        try:
            with open(csv_file, 'r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                
                for i, row in enumerate(csv_reader, 1):
                    if 'email' not in row:
                        self.logger.warning(f"Row {i}: Missing 'email' field, skipping")
                        continue
                    
                    if not row['email'] or '@' not in row['email']:
                        self.logger.warning(f"Row {i}: Invalid email '{row.get('email')}', skipping")
                        continue
                    
                    recipients.append(row)
                    self.logger.info(f"Loaded recipient: {row.get('email', 'Unknown')}")
            
            self.logger.info(f"Successfully loaded {len(recipients)} recipients from {csv_file}")
            return recipients
            
        except FileNotFoundError:
            self.logger.error(f"CSV file not found: {csv_file}")
            return []
        except Exception as e:
            self.logger.error(f"Error reading CSV file: {str(e)}")
            return []
    
    def create_email_message(self, recipient: Dict, subject: str, 
                            body_template: str, attachments: List[str] = None) -> Optional[MIMEMultipart]:
        """
        Create a personalized email message with attachments.
        
        Args:
            recipient: Recipient dictionary with email and other fields
            subject: Email subject (can include placeholders like {name})
            body_template: Email body template (can include placeholders)
            attachments: List of file paths to attach
            
        Returns:
            MIME message object or None if creation fails
        """
        try:
            # Personalize subject and body
            personalized_subject = subject.format(**recipient)
            personalized_body = body_template.format(**recipient)
            
            # Create message container
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = recipient['email']
            msg['Subject'] = personalized_subject
            
            # Add body
            msg.attach(MIMEText(personalized_body, 'plain'))
            
            # Add attachments
            if attachments:
                for attachment_path in attachments:
                    if os.path.exists(attachment_path):
                        self.attach_file(msg, attachment_path)
                    else:
                        self.logger.warning(f"Attachment not found: {attachment_path}")
            
            return msg
            
        except Exception as e:
            self.logger.error(f"Error creating message for {recipient.get('email')}: {str(e)}")
            return None
    
    def attach_file(self, msg: MIMEMultipart, filepath: str):
        """Attach a file to the email message."""
        try:
            filename = os.path.basename(filepath)
            
            with open(filepath, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
            
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {filename}",
            )
            
            msg.attach(part)
            self.logger.info(f"Attached: {filename}")
            
        except Exception as e:
            self.logger.error(f"Failed to attach {filepath}: {str(e)}")
    
    def send_email_with_retry(self, msg: MIMEMultipart, recipient_email: str, 
                             max_retries: int = 3) -> bool:
        """
        Send email with retry logic.
        
        Args:
            msg: Email message object
            recipient_email: Recipient's email address
            max_retries: Maximum number of retry attempts
            
        Returns:
            True if sent successfully, False otherwise
        """
        for attempt in range(max_retries):
            try:
                with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                    server.starttls()
                    server.login(self.sender_email, self.password)
                    server.send_message(msg)
                
                self.logger.info(f"✓ Email sent successfully to {recipient_email}")
                return True
                
            except smtplib.SMTPRecipientsRefused:
                self.logger.error(f"Recipient refused: {recipient_email}")
                return False
            except smtplib.SMTPSenderRefused:
                self.logger.error(f"Sender refused. Check authentication.")
                return False
            except Exception as e:
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt  # Exponential backoff
                    self.logger.warning(
                        f"Attempt {attempt + 1}/{max_retries} failed for {recipient_email}. "
                        f"Retrying in {wait_time} seconds... Error: {str(e)}"
                    )
                    time.sleep(wait_time)
                else:
                    self.logger.error(
                        f"Failed to send to {recipient_email} after {max_retries} attempts. "
                        f"Error: {str(e)}"
                    )
        
        return False
    
    def send_bulk_emails(self, recipients: List[Dict], subject: str, 
                        body_template: str, attachments: List[str] = None,
                        delay: float = 1.0) -> Dict:
        """
        Send bulk emails to all recipients.
        
        Args:
            recipients: List of recipient dictionaries
            subject: Email subject template
            body_template: Email body template
            attachments: List of attachment file paths
            delay: Delay between emails (seconds)
            
        Returns:
            Dictionary with send statistics
        """
        stats = {
            'total': len(recipients),
            'success': 0,
            'failed': 0,
            'failed_recipients': []
        }
        
        print("\n" + "="*50)
        print("SENDING EMAILS")
        print("="*50)
        
        for i, recipient in enumerate(recipients, 1):
            recipient_email = recipient.get('email', 'Unknown')
            
            print(f"\n[{i}/{len(recipients)}] Processing: {recipient_email}")
            
            # Create personalized message
            msg = self.create_email_message(recipient, subject, body_template, attachments)
            
            if not msg:
                stats['failed'] += 1
                stats['failed_recipients'].append(recipient_email)
                continue
            
            # Send with retry logic
            if self.send_email_with_retry(msg, recipient_email):
                stats['success'] += 1
            else:
                stats['failed'] += 1
                stats['failed_recipients'].append(recipient_email)
            
            # Delay between emails to avoid rate limiting
            if i < len(recipients):
                time.sleep(delay)
        
        return stats
    
    def generate_report(self, stats: Dict, output_file: str = None):
        """Generate and save a send report."""
        report = [
            "\n" + "="*50,
            "EMAIL SEND REPORT",
            "="*50,
            f"Total Recipients: {stats['total']}",
            f"Successfully Sent: {stats['success']}",
            f"Failed: {stats['failed']}",
            f"Success Rate: {(stats['success']/stats['total']*100 if stats['total']>0 else 0):.1f}%",
        ]
        
        if stats['failed_recipients']:
            report.extend([
                "\nFailed Recipients:",
                "-" * 20
            ])
            for email in stats['failed_recipients']:
                report.append(f"  • {email}")
        
        # Print report
        print("\n".join(report))
        
        # Save to file
        if output_file:
            try:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write("\n".join(report))
                self.logger.info(f"Report saved to: {output_file}")
            except Exception as e:
                self.logger.error(f"Failed to save report: {str(e)}")


def main():
    """Main function to run the Email Sender Bot."""
    print("\n" + "="*50)
    print("SYNTECXHUB - EMAIL SENDER BOT")
    print("CREATE | THINK | SOLVE")
    print("="*50)
    
    # Initialize bot
    bot = EmailSenderBot()
    
    # Step 1: Authentication
    if not bot.authenticate():
        print("\n✗ Authentication failed. Please check your credentials.")
        return
    
    # Step 2: Get recipient CSV file
    csv_file = input("\nEnter path to recipients CSV file: ").strip()
    
    if not os.path.exists(csv_file):
        print(f"✗ File not found: {csv_file}")
        return
    
    # Step 3: Load recipients
    recipients = bot.read_recipients_from_csv(csv_file)
    
    if not recipients:
        print("✗ No valid recipients found in CSV file.")
        return
    
    # Step 4: Email content
    print("\n" + "-"*50)
    print("EMAIL CONTENT SETUP")
    print("-"*50)
    
    subject = input("Enter email subject (use {name} for personalization): ").strip()
    
    print("\nEnter email body (use placeholders like {name}, {company}):")
    print("Press Enter twice when finished:")
    body_lines = []
    while True:
        line = input()
        if line == "":
            if body_lines and body_lines[-1] == "":
                body_lines.pop()
                break
        body_lines.append(line)
    
    body_template = "\n".join(body_lines)
    
    # Step 5: Attachments
    attachments = []
    add_attachments = input("\nAdd attachments? (y/n): ").lower().strip()
    
    while add_attachments == 'y':
        file_path = input("Enter attachment file path (or 'done' to finish): ").strip()
        
        if file_path.lower() == 'done':
            break
        
        if os.path.exists(file_path):
            attachments.append(file_path)
            print(f"✓ Added: {file_path}")
        else:
            print(f"✗ File not found: {file_path}")
    
    # Step 6: Send confirmation
    print("\n" + "-"*50)
    print("SEND CONFIRMATION")
    print("-"*50)
    print(f"Recipients: {len(recipients)}")
    print(f"Subject: {subject}")
    print(f"Attachments: {len(attachments)} file(s)")
    
    confirm = input("\nAre you ready to send? (y/n): ").lower().strip()
    
    if confirm != 'y':
        print("\nEmail sending cancelled.")
        return
    
    # Step 7: Send emails
    stats = bot.send_bulk_emails(
        recipients=recipients,
        subject=subject,
        body_template=body_template,
        attachments=attachments if attachments else None,
        delay=2.0  # 2-second delay between emails
    )
    
    # Step 8: Generate report
    report_file = f"email_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    bot.generate_report(stats, report_file)
    
    print("\n" + "="*50)
    print("PROJECT COMPLETED SUCCESSFULLY!")
    print("="*50)


if __name__ == "__main__":
    main()