# Email service for OTP verification using Replit Mail API
# Referenced from blueprint:replitmail integration

import os
import requests
import json
from flask import current_app

class EmailService:
    def __init__(self, app=None):
        self.app = app
        self.auth_token = None
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize email service with Replit authentication"""
        # Get Replit authentication token
        repl_identity = os.environ.get('REPL_IDENTITY')
        web_repl_renewal = os.environ.get('WEB_REPL_RENEWAL')
        
        if repl_identity:
            self.auth_token = f"repl {repl_identity}"
        elif web_repl_renewal:
            self.auth_token = f"depl {web_repl_renewal}"
        else:
            current_app.logger.warning("No Replit authentication token found")
            self.auth_token = None
        
        self.app = app
    
    def _send_replit_email(self, to_email, subject, html_content, text_content):
        """Send email using Replit's mail API"""
        if not self.auth_token:
            current_app.logger.error("No authentication token available for email service")
            return False
        
        url = "https://connectors.replit.com/api/v2/mailer/send"
        headers = {
            "Content-Type": "application/json",
            "X_REPLIT_TOKEN": self.auth_token,
        }
        
        data = {
            "to": to_email,
            "subject": subject,
            "html": html_content,
            "text": text_content
        }
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                current_app.logger.info(f"Email sent successfully to {to_email}: {result}")
                return True
            else:
                current_app.logger.error(f"Failed to send email to {to_email}: {response.status_code} - {response.text}")
                return False
                
        except requests.exceptions.RequestException as e:
            current_app.logger.error(f"Request error sending email to {to_email}: {str(e)}")
            return False
        except Exception as e:
            current_app.logger.error(f"Unexpected error sending email to {to_email}: {str(e)}")
            return False
    
    def send_otp_email(self, recipient_email, otp_code, user_name):
        """Send OTP verification email to SSN email address"""
        if not self.auth_token:
            current_app.logger.error("Email service not properly initialized - no auth token")
            return False
        
        subject = "SSN Email Verification - College Portal"
        
        # Create HTML email content
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>SSN Email Verification</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .header {{
                    background-color: #0d6efd;
                    color: white;
                    padding: 20px;
                    text-align: center;
                    border-radius: 8px 8px 0 0;
                }}
                .content {{
                    background-color: #f8f9fa;
                    padding: 30px;
                    border-radius: 0 0 8px 8px;
                }}
                .otp-code {{
                    background-color: #fff;
                    border: 2px solid #0d6efd;
                    border-radius: 8px;
                    padding: 20px;
                    text-align: center;
                    margin: 20px 0;
                }}
                .otp-number {{
                    font-size: 36px;
                    font-weight: bold;
                    color: #0d6efd;
                    letter-spacing: 8px;
                }}
                .warning {{
                    background-color: #fff3cd;
                    border-left: 4px solid #ffc107;
                    padding: 15px;
                    margin: 20px 0;
                }}
                .footer {{
                    text-align: center;
                    color: #6c757d;
                    font-size: 14px;
                    margin-top: 20px;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h2>🎓 College Materials & PYQs Portal</h2>
                <h3>SSN Email Verification</h3>
            </div>
            
            <div class="content">
                <p>Hello <strong>{user_name}</strong>,</p>
                
                <p>You have requested to verify your SSN email address to gain <strong>Contributor</strong> privileges on the College Materials & PYQs Portal.</p>
                
                <div class="otp-code">
                    <p>Your verification code is:</p>
                    <div class="otp-number">{otp_code}</div>
                </div>
                
                <p>Please enter this code on the verification page to complete the process.</p>
                
                <div class="warning">
                    <strong>⚠️ Important Security Notes:</strong>
                    <ul>
                        <li>This code will expire in <strong>10 minutes</strong></li>
                        <li>Do not share this code with anyone</li>
                        <li>Only use this code on the official College Portal website</li>
                        <li>We will never ask for your password</li>
                    </ul>
                </div>
                
                <p>After verification, you will have access to:</p>
                <ul>
                    <li>✅ Upload academic files and materials</li>
                    <li>✅ Edit and manage content</li>
                    <li>✅ Delete inappropriate content</li>
                    <li>✅ Full contributor privileges</li>
                </ul>
                
                <p>If you didn't request this verification, please ignore this email.</p>
            </div>
            
            <div class="footer">
                <p>This is an automated email from College Materials & PYQs Portal</p>
                <p>Please do not reply to this email</p>
            </div>
        </body>
        </html>
        """
        
        # Create plain text version
        text_body = f"""
        SSN Email Verification - College Portal
        
        Hello {user_name},
        
        You have requested to verify your SSN email address to gain Contributor privileges.
        
        Your verification code is: {otp_code}
        
        Please enter this code on the verification page within 10 minutes.
        
        SECURITY NOTES:
        - This code expires in 10 minutes
        - Do not share this code with anyone
        - We will never ask for your password
        
        If you didn't request this verification, please ignore this email.
        
        College Materials & PYQs Portal
        """
        
        # Use the new Replit email API
        return self._send_replit_email(recipient_email, subject, html_body, text_body)
    
    def send_verification_success_email(self, recipient_email, user_name):
        """Send confirmation email after successful verification"""
        if not self.auth_token:
            current_app.logger.error("Email service not properly initialized - no auth token")
            return False
        
        subject = "Welcome to College Portal - Contributor Access Granted"
        
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Contributor Access Granted</title>
        </head>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="background-color: #28a745; color: white; padding: 20px; text-align: center; border-radius: 8px;">
                <h2>🎉 Verification Successful!</h2>
                <h3>Welcome to the Contributors Team</h3>
            </div>
            
            <div style="background-color: #f8f9fa; padding: 30px; border-radius: 8px; margin-top: 10px;">
                <p>Congratulations <strong>{user_name}</strong>!</p>
                
                <p>Your SSN email address has been successfully verified. You now have <strong>Contributor</strong> access to the College Materials & PYQs Portal.</p>
                
                <h4>Your new privileges include:</h4>
                <ul>
                    <li>✅ Upload academic files, question papers, and study materials</li>
                    <li>✅ Edit and update existing content</li>
                    <li>✅ Delete inappropriate or outdated content</li>
                    <li>✅ Manage events, clubs, and campus information</li>
                    <li>✅ Full administrative access to help build the portal</li>
                </ul>
                
                <p>Thank you for contributing to the academic community at SSN!</p>
                
                <div style="text-align: center; margin: 30px 0;">
                    <p style="background-color: #e9ecef; padding: 15px; border-radius: 8px;">
                        <strong>🚀 Start contributing today!</strong><br>
                        Visit the portal and click on your name in the navigation bar to access upload features.
                    </p>
                </div>
                
                <p>Best regards,<br>College Materials & PYQs Portal Team</p>
            </div>
        </body>
        </html>
        """
        
        text_body = f"""
        Welcome to College Portal - Contributor Access Granted
        
        Congratulations {user_name}!
        
        Your SSN email address has been successfully verified. You now have Contributor access to the College Materials & PYQs Portal.
        
        Your new privileges include:
        - Upload academic files, question papers, and study materials
        - Edit and update existing content
        - Delete inappropriate or outdated content
        - Manage events, clubs, and campus information
        - Full administrative access to help build the portal
        
        Thank you for contributing to the academic community at SSN!
        
        Start contributing today! Visit the portal and access upload features.
        
        Best regards,
        College Materials & PYQs Portal Team
        """
        
        # Use the new Replit email API
        return self._send_replit_email(recipient_email, subject, html_body, text_body)

# Global email service instance
email_service = EmailService()