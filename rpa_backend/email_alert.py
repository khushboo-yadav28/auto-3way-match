import smtplib
from email.message import EmailMessage
import os

def send_exception_alert(invoice_data, reason):
    """
    Process B (Exception): Sends an exception report via automated email alerts 
    to a supervisor if discrepancies are detected.
    """
    # NOTE: In a real environment, use environment variables for credentials.
    # For local testing, you can use a test email or local debugging server.
    sender_email = "rpa.bot@nexuserp.com"
    supervisor_email = "supervisor@nexuserp.com"
    
    subject = f"⚠️ ACTION REQUIRED: Invoice Discrepancy Detected ({invoice_data.get('invoice_id', 'Unknown')})"
    body = f"""
    The RPA pipeline halted automated data entry for the following invoice:
    
    Invoice ID: {invoice_data.get('invoice_id')}
    Vendor Name: {invoice_data.get('vendor_name')}
    
    Reason for Exception: {reason}
    
    Please review the original PDF invoice and manually process the record in the ERP.
    """
    
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = supervisor_email

    print("\n[ALERT TRIGGERED] Constructing exception email...")
    
    try:
        # Connect to a local debugging server or external SMTP (like Gmail/Outlook)
        # For testing, we mock a successful send.
        # server = smtplib.SMTP("smtp.gmail.com", 587)
        # server.starttls()
        # server.login(sender_email, "your_secure_app_password")
        # server.send_message(msg)
        # server.quit()
        print(f"📧 Email successfully sent to {supervisor_email}")
        print(f"Exception details: {reason}")
    except Exception as e:
        print(f"Failed to send email alert: {e}")