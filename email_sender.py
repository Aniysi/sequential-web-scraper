import smtplib
import os
import json
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


class EmailSender:
    def __init__(self, smtp_server: str = "smtp.gmail.com", smtp_port: int = 587, config_file: str = "email_config.json"):
        """
        Initialize email sender.
        
        Args:
            smtp_server: SMTP server address (default: Gmail)
            smtp_port: SMTP server port (default: 587 for TLS)
            config_file: Path to configuration file for storing credentials
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.config_file = Path(config_file)
    
    def load_config(self) -> dict:
        """
        Load email configuration from file.
        
        Returns:
            Dictionary with email configuration or empty dict if file doesn't exist
        """
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️  Error reading config file: {e}")
                return {}
        return {}
    
    def save_config(self, sender_email: str, sender_password: str, recipient_email: str):
        """
        Save email configuration to file.
        
        Args:
            sender_email: Sender's email address
            sender_password: Sender's email password
            recipient_email: Default recipient's email address
        """
        config = {
            "sender_email": sender_email,
            "sender_password": sender_password,
            "recipient_email": recipient_email,
            "smtp_server": self.smtp_server,
            "smtp_port": self.smtp_port
        }
        
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
            print(f"✅ Configuration saved to {self.config_file}")
        except Exception as e:
            print(f"⚠️  Error saving config: {e}")
    
    def get_credentials(self) -> tuple[str, str, str]:
        """
        Get email credentials either from config file or user input.
        
        Returns:
            Tuple of (sender_email, sender_password, recipient_email)
        """
        config = self.load_config()
        
        if config and all(k in config for k in ['sender_email', 'sender_password', 'recipient_email']):
            print("📧 Using saved email configuration.")
            print(f"   Sender: {config['sender_email']}")
            print(f"   Recipient: {config['recipient_email']}")
            
            use_saved = input("Use these settings? (y/n): ").strip().lower()
            if use_saved == 'y':
                return config['sender_email'], config['sender_password'], config['recipient_email']
        
        # Ask for credentials
        print("\n📧 Email Configuration:")
        sender_email = input("Your email address: ").strip()
        sender_password = input("Your email password (or app password): ").strip()
        recipient_email = input("Recipient email address: ").strip()
        
        # Ask if user wants to save
        save = input("\nSave these credentials for future use? (y/n): ").strip().lower()
        if save == 'y':
            self.save_config(sender_email, sender_password, recipient_email)
        
        return sender_email, sender_password, recipient_email
    
    def send_epub(self, 
                  epub_file: str,
                  sender_email: str,
                  sender_password: str,
                  recipient_email: str,
                  subject: str = "EPUB Book",
                  body: str = "Please find the attached EPUB file.") -> bool:
        """
        Send EPUB file via email.
        
        Args:
            epub_file: Path to the EPUB file to send
            sender_email: Sender's email address
            sender_password: Sender's email password (or app-specific password)
            recipient_email: Recipient's email address
            subject: Email subject line
            body: Email body text
            
        Returns:
            True if email was sent successfully, False otherwise
        """
        if not os.path.exists(epub_file):
            print(f"❌ Error: File '{epub_file}' not found.")
            return False
        
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = recipient_email
            msg['Subject'] = subject
            
            # Attach body text
            msg.attach(MIMEText(body, 'plain'))
            
            # Attach EPUB file
            with open(epub_file, 'rb') as attachment:
                part = MIMEBase('application', 'epub+zip')
                part.set_payload(attachment.read())
            
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename= {os.path.basename(epub_file)}'
            )
            msg.attach(part)
            
            # Connect to SMTP server and send email
            print(f"📧 Connecting to {self.smtp_server}...")
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()  # Enable TLS encryption
            
            print("🔐 Logging in...")
            server.login(sender_email, sender_password)
            
            print("📨 Sending email...")
            text = msg.as_string()
            server.sendmail(sender_email, recipient_email, text)
            
            server.quit()
            print(f"✅ Email sent successfully to {recipient_email}")
            return True
            
        except smtplib.SMTPAuthenticationError:
            print("❌ Authentication failed. Check your email and password.")
            print("   For Gmail, you may need to use an App Password:")
            print("   https://support.google.com/accounts/answer/185833")
            return False
            
        except smtplib.SMTPException as e:
            print(f"❌ SMTP error occurred: {e}")
            return False
            
        except Exception as e:
            print(f"❌ Error sending email: {e}")
            return False
