from playwright.sync_api import sync_playwright

def submit_invoice_to_erp(invoice_data):
    """
    Process A (Success): Applies Playwright browser automation tools to 
    automatically fill the target web ERP by logging into it completely hands-free[cite: 2].
    """
    with sync_playwright() as p:
        # Launch browser (set headless=False so you can watch Playwright fill the form)
        browser = p.chromium.launch(headless=False, slow_mo=500)
        page = browser.new_page()

        print("Navigating to Mock ERP System...")
        page.goto("http://localhost:5173")  # Target React app URL

        # 1. Automatic Login
        print("Logging in hands-free...")
        page.fill("#email", "admin@nexuserp.com")
        page.fill("#password", "securepassword123")
        page.click("#authButton")

        # 2. Wait for Dashboard & Form to Load
        page.wait_for_selector("#invoiceForm")

        # 3. Enter Invoice Data Extracted during Ingestion Phase
        print("Filling invoice data into ERP fields...")
        page.fill("#invoiceId", str(invoice_data.get("invoice_id", "")))
        page.fill("#vendorName", str(invoice_data.get("vendor_name", "")))
        page.fill("#itemQuantities", str(invoice_data.get("item_quantities", "")))
        page.fill("#unitPricing", str(invoice_data.get("unit_pricing", "")))
        page.fill("#totalAmount", str(invoice_data.get("total_amount", "")))

        # 4. Submit Form
        print("Submitting invoice entry...")
        page.click("#submitInvoice")

        # 5. Confirm Successful Entry
        page.wait_for_selector("#successBanner")
        print("✅ Entry confirmed on ERP Dashboard!")

        browser.close()