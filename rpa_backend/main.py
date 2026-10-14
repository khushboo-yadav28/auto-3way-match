import time
from extraction_engine import (
    extract_invoice_data,
    extract_text_from_pdf,
)
from ingestion_engine import download_invoices_from_gmail
from playwright_bot import log_exception_to_erp, submit_invoice_to_erp
from verification_brain import verify_three_way_match


def run_pipeline():
  while True:
    print('\n=== Waking Up: Checking Queue ===')
    print('Scanning Gmail for unread invoices (Multilingual Engine Active)...')

    # 1. Check Email for Unread Invoices
    pdf_path = download_invoices_from_gmail()

    if pdf_path:
      print(f'📄 Parsing document: {pdf_path}')

      # 2. Extract Text (Automatically handles translation & hybrid bilingual regex fallback)
      raw_text = extract_text_from_pdf(pdf_path)

      # 3. Extract Structured Data
      invoice_data = extract_invoice_data(raw_text)
      print(f'📊 Structured transaction data extracted: {invoice_data}')

      # Check if extraction was completely successful
      if None in invoice_data.values():
        print(
            '⚠️ Warning: Some essential fields could not be extracted from the'
            ' PDF. Skipping submission...'
        )
      else:
        # 4. Verify 3-Way Match against SQLite Database
        print('🔍 Checking ERP Database for 3-Way Match (PO = GRN = Invoice)...')
        is_match = verify_three_way_match(invoice_data)

        # 5. Trigger Frontend Playwright UI Automation
        if is_match:
          print(
              '✅ Match successful! Triggering Playwright RPA Agent for'
              ' automated UI entry...'
          )
          submit_invoice_to_erp(invoice_data)
        else:
          print(
              '❌ Match failed! Triggering Playwright RPA Agent to flag anomaly'
              ' in UI Command Center...'
          )
          log_exception_to_erp(invoice_data)

    else:
      print('📭 No new invoices found in inbox.')

    print('\n💤 Agent resting for 30 seconds before next polling cycle...')
    time.sleep(30)


if __name__ == '__main__':
  print('🚀 Kinetix ERP Agentic RPA Worker Started. Press Ctrl+C to stop.')
  run_pipeline()