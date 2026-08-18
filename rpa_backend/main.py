import time
from ingestion_engine import download_invoices_from_gmail, parse_invoice
from verification_brain import verify_three_way_match
from playwright_bot import submit_invoice_to_erp, log_exception_to_erp

def run_pipeline():
    print("\n=== Waking Up: Checking Queue ===")
    pdf_path = download_invoices_from_gmail()
    
    # If no email is found, the function quietly ends and the bot goes back to sleep
    if not pdf_path:
        return 

    invoice_data = parse_invoice(pdf_path)
    
    if not invoice_data:
        return

    print("\n=== Initiating Three-Way Match Verification ===")
    is_valid = verify_three_way_match(invoice_data)

    print("\n=== Determining Output Process ===")
    if is_valid:
        print("Executing Process A (Success): Initiating Playwright Web RPA...")
        try:
            submit_invoice_to_erp(invoice_data)
        except Exception as e:
            print(f"Playwright Automation Failed: {e}")
    else:
        print("Executing Process B (Exception): Three-Way Match Failed!")
        print("Initiating UI alert protocol...")
        try:
            log_exception_to_erp(invoice_data)
        except Exception as e:
            print(f"Playwright Automation Failed: {e}")
            
    print("=== Pipeline Cycle Complete ===")

if __name__ == "__main__":
    print("🚀 Agentic RPA Worker Started. Press Ctrl+C to stop.")
    
    try:
        # The Infinite Loop: This keeps the script running continuously
        while True:
            run_pipeline()
            
            # Polling Interval: Wait 30 seconds before checking Gmail again
            print("\n💤 Agent resting for 30 seconds...")
            time.sleep(30)
            
    except KeyboardInterrupt:
        # Allows you to smoothly kill the script in the terminal using Ctrl + C
        print("\n🛑 Agent shutdown gracefully by human manager.")