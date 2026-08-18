import os
import base64
import re
import pdfplumber
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Gmail API Scopes (Read-only access to emails)
# Change this line at the top of your file
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

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
                service.users().messages().modify(userId='me', id=messages[0]['id'], body={'removeLabelIds': ['UNREAD']}).execute()
                return save_path

    except Exception as e:
        print(f"Gmail API Error: {e}")
        return None

def parse_invoice(pdf_path):
    print(f"Parsing document: {pdf_path}\n")
    
    # --> ADDED THE MISSING 'try:' HERE <--
    try: 
        with pdfplumber.open(pdf_path) as pdf:
            text = pdf.pages[0].extract_text()
            
            print("--- Raw Text Extracted ---")
            print(text)
            print("--------------------------\n")

            # UPDATED REGEX PATTERNS to match the new PDF format
            invoice_id_match = re.search(r"Invoice Number:\s*(.*)", text)
            vendor_match = re.search(r"Vendor:\s*(.*)", text)
            qty_match = re.search(r"Item Quantities:\s*(\d+)", text)
            price_match = re.search(r"Unit Pricing:\s*\$([\d.]+)", text)
            total_match = re.search(r"Total Amount Due:\s*\$([\d.]+)", text)

            invoice_data = {
                "invoice_id": invoice_id_match.group(1).strip() if invoice_id_match else None,
                "vendor_name": vendor_match.group(1).strip() if vendor_match else None,
                "item_quantities": int(qty_match.group(1)) if qty_match else None,
                "unit_pricing": float(price_match.group(1)) if price_match else None,
                "total_amount": float(total_match.group(1)) if total_match else None
            }

            print(f"Structured transaction data: {invoice_data}")
            
            if None in invoice_data.values():
                print("⚠️ Warning: Some fields could not be extracted from the PDF.")
                return None
                
            return invoice_data
            
    except Exception as e:
        print(f"Error parsing PDF: {e}")
        return None