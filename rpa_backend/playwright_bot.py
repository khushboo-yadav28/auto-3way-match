import time
from playwright.sync_api import sync_playwright

def submit_invoice_to_erp(invoice_data):
    """
    Process A (Success): Visually demonstrates the bot logging in, 
    interacting with the UI dashboard, clicking auxiliary buttons, 
    and auto-filling the verified data.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=400)
        page = browser.new_page()

        print("\nNavigating to Mock ERP System...")
        page.goto("http://localhost:5173") 

        print("Logging in hands-free...")
        page.fill("#email", "admin@nexuserp.com")
        page.fill("#password", "securepassword123")
        page.click("#authButton")

        # Wait for the dashboard to load
        page.wait_for_selector("#triggerRpaBtn")
        time.sleep(1.5)

        # --- THE AUTOMATED CLICKS ---
        print("Bot is clicking 'View PDF' to simulate an audit...")
        page.click("#viewPdfBtn")
        time.sleep(1.5)
        
        # Bring the main dashboard back into focus (since View PDF opens a new tab)
        page.bring_to_front()

        print("Bot is clicking 'Download'...")
        page.click("#downloadPdfBtn")
        time.sleep(1.5)

        print("Bot is clicking 'Trigger Agent'...")
        page.click("#triggerRpaBtn")
        time.sleep(1)
        # ----------------------------

        print("Filling invoice data into ERP fields...")
        page.fill("#invoiceId", str(invoice_data.get("invoice_id", "")))
        page.fill("#vendorName", str(invoice_data.get("vendor_name", "")))
        page.fill("#itemQuantities", str(invoice_data.get("item_quantities", "")))
        page.fill("#unitPricing", str(invoice_data.get("unit_pricing", "")))
        page.fill("#totalAmount", str(invoice_data.get("total_amount", "")))

        print("Submitting invoice entry...")
        page.click("#submitInvoice")

        print("✅ Entry confirmed on ERP Dashboard!")
        print("Demo paused for 6 seconds to view results...")
        time.sleep(6)
        
        browser.close()

def log_exception_to_erp(invoice_data):
    """
    Process B (Exception): Visually demonstrates the bot logging an error 
    into the ERP system when the Three-Way Match fails.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=400)
        page = browser.new_page()

        print("\nNavigating to Mock ERP System to report discrepancy...")
        page.goto("http://localhost:5173") 

        print("Logging in to alert human managers...")
        page.fill("#email", "admin@nexuserp.com")
        page.fill("#password", "securepassword123")
        page.click("#authButton")

        page.wait_for_selector("#logExceptionBtn")
        
        # Partially fill the form to visually show the faculty WHICH invoice failed
        print("Inputting flagged vendor data...")
        page.fill("#invoiceId", str(invoice_data.get("invoice_id", "ERROR")))
        page.fill("#vendorName", str(invoice_data.get("vendor_name", "ERROR")))
        
        time.sleep(1) # Tiny pause so the audience can read the vendor name
        
        print("Clicking 'Flag Discrepancy'...")
        page.click("#logExceptionBtn")

        print("✅ Exception successfully logged on ERP Dashboard!")
        print("Demo paused for 8 seconds to view updated Exception Metrics...")
        time.sleep(8)
        
        browser.close()