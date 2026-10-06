import smtplib
from email.message import EmailMessage

# Note: For Gmail, you will need to generate an "App Password" in your Google Account settings
SENDER_EMAIL = "khushi28.mail@gmail.com" 
APP_PASSWORD = "gjwq bgvd amll dscj" 
MANAGER_EMAIL = "janavi28yadav@gmail.com" # Route this to your mentor/teammate during the demo

def alert_manager_of_discrepancy(invoice_data, db_expected_amount):
    """
    HITL Workflow: Halts the autonomous agent and emails a human manager for intervention.
    """
    msg = EmailMessage()
    msg['Subject'] = f"⚠️ URGENT ACTION REQUIRED: Discrepancy in Invoice {invoice_data.get('invoice_id')}"
    msg['From'] = SENDER_EMAIL
    msg['To'] = MANAGER_EMAIL

    body = f"""
    Nexus ERP - Agentic RPA Alert
    -------------------------------------------
    The autonomous agent has halted processing for Vendor: {invoice_data.get('vendor_name')}
    
    Discrepancy Details:
    - Billed Amount on Invoice: ${invoice_data.get('total_amount')}
    - Approved Amount in Database: ${db_expected_amount}
    
    Human Intervention is required. Please log into the Nexus ERP dashboard to review the physical document.
    
    Action Link: http://localhost:5173
    
    - Agentic AI Node
    """
    
    msg.set_content(body)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(SENDER_EMAIL, APP_PASSWORD)
            smtp.send_message(msg)
        print("📧 Escalation email successfully dispatched to Human Manager.")
    except Exception as e:
        print(f"Failed to send email: {e}")