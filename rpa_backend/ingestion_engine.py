import os
import base64
import re
import pdfplumber
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Gmail API Scopes (Read-only access to emails)
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def download_invoices_from_gmail():
    """
    Live Ingestion: Connects to Gmail via OAuth to scan for unread emails 
    with PDF attachments and downloads them.
    """
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('gmail', 'v1', credentials=creds)
        print("Scanning Gmail for unread invoices...")
        
        # Query for unread emails with attachments
        results = service.users().messages().list(userId='me', q="is:unread has:attachment").execute()
        messages = results.get('messages', [])

        if not messages:
            print("No new invoices found.")
            return None

        # Process the first unread email found
        msg = service.users().messages().get(userId='me', id=messages[0]['id']).execute()
        
        for part in msg['payload'].get('parts', []):
            if part['filename'] and part['filename'].endswith('.pdf'):
                attachment_id = part['body'].get('attachmentId')
                attachment = service.users().messages().attachments().get(
                    userId='me', messageId=messages[0]['id'], id=attachment_id
                ).execute()
                
                file_data = base64.urlsafe_b64decode(attachment['data'].encode('UTF-8'))
                save_path = os.path.join("data", "raw_invoices", part['filename'])
                
                with open(save_path, 'wb') as f:
                    f.write(file_data)
                print(f"Downloaded live invoice: {save_path}")
                return save_path

    except Exception as e:
        print(f"Gmail API Error: {e}")
        return None

def parse_invoice(pdf_path):
    """
    Intelligent Parsing: Extracts Invoice ID, Vendor Name, Item Quantities, 
    Unit Pricing, Totals, and Date using regex and pdfplumber.
    """
    print(f"Parsing document: {pdf_path}")
    
    if not os.path.exists(pdf_path):
        print(f"❌ Error: Could not find PDF at {pdf_path}")
        return None

    try:
        # Extract raw text from the PDF
        with pdfplumber.open(pdf_path) as pdf:
            raw_text = ""
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    raw_text += extracted + "\n"
        
        print("\n--- Raw Text Extracted ---")
        print(raw_text)
        print("--------------------------\n")

        # Use Regex to intelligently locate data points
        invoice_id_match = re.search(r"Invoice ID:\s*([A-Z0-9-]+)", raw_text, re.IGNORECASE)
        vendor_match = re.search(r"Vendor Name:\s*(.+)", raw_text, re.IGNORECASE)
        qty_match = re.search(r"Total Items:\s*(\d+)", raw_text, re.IGNORECASE)
        price_match = re.search(r"Unit Price:\s*\$?([\d.]+)", raw_text, re.IGNORECASE)
        total_match = re.search(r"Total Amount:\s*\$?([\d.]+)", raw_text, re.IGNORECASE)
        
        # ---> DATE REGEX ADDED HERE <---
        date_match = re.search(r"Date:\s*(\d{4}-\d{2}-\d{2})", raw_text, re.IGNORECASE)

        # Structure the extracted data
        extracted_data = {
            "invoice_id": invoice_id_match.group(1).strip() if invoice_id_match else None,
            "vendor_name": vendor_match.group(1).strip() if vendor_match else None,
            "item_quantities": int(qty_match.group(1)) if qty_match else None,
            "unit_pricing": float(price_match.group(1)) if price_match else None,
            "total_amount": float(total_match.group(1)) if total_match else None,
            
            # ---> DATE DATA ADDED HERE <---
            "invoice_date": date_match.group(1).strip() if date_match else None
        }
        
        print(f"Structured transaction data: {extracted_data}")
        
        if not all(extracted_data.values()):
            print("⚠️ Warning: Some fields could not be extracted from the PDF.")
            
        return extracted_data
        
    except Exception as e:
        print(f"Error parsing PDF: {e}")
        return None