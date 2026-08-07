import time
from ingestion_engine import download_invoices_from_gmail, parse_invoice
from verification_brain import verify_three_way_match
from playwright_bot import submit_invoice_to_erp
from email_alert import send_exception_alert

def run_pipeline():
    print("=== Starting Intelligent Invoice Processing Pipeline ===")
    
    # Phase 1: Automated Data Ingestion & Parsing
    pdf_path = download_invoices_from_gmail()
    
    # --> ADD THIS SAFETY CHECK <--
    if not pdf_path:
        print("Pipeline on standby: No unread invoices found in Gmail.")
        return
        
    invoice_data = parse_invoice(pdf_path)
    
    if not invoice_data:
        print("Pipeline aborted: Failed to parse PDF data.")
        return

    # Phase 2: The Intelligent Verification Brain (Three-Way Matching)
    print("\n=== Initiating Three-Way Match Verification ===")
    is_valid = verify_three_way_match(invoice_data)
    
    # Phase 3: Closed-Loop Output Processing
    print("\n=== Determining Output Process ===")
    if is_valid:
        print("Executing Process A (Success): Initiating Playwright Web RPA...")
        try:
            submit_invoice_to_erp(invoice_data)
        except Exception as e:
            print(f"Playwright Automation Failed: {e}")
    else:
        print("Executing Process B (Exception): Halting automation and sending alert...")
        reason = "Mismatch detected between Invoice, Purchase Order, and Goods Received Note quantities/pricing."
        send_exception_alert(invoice_data, reason)
        
    print("\n=== Pipeline Execution Complete ===")

if __name__ == "__main__":
    # In a production environment, this would run on a scheduler or continuous loop.
    run_pipeline()