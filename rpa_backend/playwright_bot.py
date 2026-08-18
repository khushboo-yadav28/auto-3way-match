import time
from playwright.sync_api import sync_playwright

def submit_invoice_to_erp(invoice_data):
    """
    Process A (Success): Applies Playwright browser automation tools to 
    automatically log in, wait for human trigger, and fill the target web ERP.
    """
    with sync_playwright() as p:
        # Launch browser (slow_mo=600 adds a 0.6 second delay between keystrokes for dramatic effect)
        browser = p.chromium.launch(headless=False, slow_mo=600)
        page = browser.new_page()

        print("Navigating to Mock ERP System...")
        page.goto("http://localhost:5173")  # Target React app URL

        # 1. Automatic Login
        print("Logging in hands-free...")
        page.fill("#email", "admin@nexuserp.com")
        page.fill("#password", "securepassword123")
        page.click("#authButton")

        # 2. Wait for Dashboard & The New Trigger Button to Load
        page.wait_for_selector("#triggerRpaBtn")

        # 3. HUMAN-IN-THE-LOOP PAUSE
        print("--------------------------------------------------")
        print("⏸️ DEMO PAUSED: Waiting for human to click 'Trigger Auto-Fill' on the React dashboard...")
        print("--------------------------------------------------")
        
        # This freezes the Python script infinitely (timeout=0) until the React button is clicked
        page.wait_for_function("window.startRpaTyping === true", timeout=0)
        
        print("▶️ Button clicked! Bot is now typing the data...")
        time.sleep(1) # Tiny pause for dramatic effect

        # 4. Enter Invoice Data Extracted during Ingestion Phase
        print("Filling invoice data into ERP fields...")
        page.fill("#invoiceId", str(invoice_data.get("invoice_id", "")))
        page.fill("#vendorName", str(invoice_data.get("vendor_name", "")))
        page.fill("#itemQuantities", str(invoice_data.get("item_quantities", "")))
        page.fill("#unitPricing", str(invoice_data.get("unit_pricing", "")))
        page.fill("#totalAmount", str(invoice_data.get("total_amount", "")))

        # 5. Submit Form
        print("Submitting invoice entry...")
        page.click("#submitInvoice")

        # 6. Confirm Successful Entry
        page.wait_for_selector("#successBanner")
        print("✅ Entry confirmed on ERP Dashboard!")
        print("Demo paused for 10 seconds to view results...")
        time.sleep(10)
        
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