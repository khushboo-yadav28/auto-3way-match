import time
from ingestion_engine import download_invoices_from_gmail
from extraction_engine import extract_text_from_pdf, extract_invoice_data
from verification_brain import verify_three_way_match
from playwright_bot import submit_invoice_to_erp, log_exception_to_erp

def run_pipeline():
    while True:
        print("\n=== Waking Up: Checking Queue ===")
        print("Scanning Gmail for unread invoices...")
        
        # 1. Check Email
        pdf_path = download_invoices_from_gmail()
        
        if pdf_path:
            print(f"Parsing document: {pdf_path}")
            
            # 2. Extract Text
            raw_text = extract_text_from_pdf(pdf_path)
            
            # 3. Extract Data
            invoice_data = extract_invoice_data(raw_text)
            print(f"Structured transaction data: {invoice_data}")
            
            # Check if extraction was completely successful
            if None in invoice_data.values():
                print("⚠️ Warning: Some fields could not be extracted from the PDF. Skipping...")
            else:
                # 4. Verify 3-Way Match & Send Email if Failed
                print("Checking ERP Database for 3-Way Match...")
                is_match = verify_three_way_match(invoice_data)
                
                # 5. Trigger Frontend UI Automation
                if is_match:
                    print("Match successful! Triggering RPA Agent for automated UI entry...")
                    submit_invoice_to_erp(invoice_data)
                else:
                    print("Match failed! Triggering RPA Agent to flag discrepancy in UI...")
                    log_exception_to_erp(invoice_data)
                    
        else:
            print("No new invoices found.")
            
        print("\n💤 Agent resting for 30 seconds...")
        time.sleep(30)

if __name__ == "__main__":
    print("🚀 Agentic RPA Worker Started. Press Ctrl+C to stop.")
    run_pipeline()