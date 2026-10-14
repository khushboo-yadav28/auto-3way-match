import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Ensure the output directory exists
os.makedirs('data/raw_invoices', exist_ok=True)


def create_invoice_pdf(filename, text_lines):
  filepath = os.path.join('data/raw_invoices', filename)
  c = canvas.Canvas(filepath, pagesize=letter)
  width, height = letter

  # Header
  c.setFont('Helvetica-Bold', 16)
  c.drawString(50, height - 50, 'KINETIX ERP - OFFICIAL VENDOR INVOICE')

  # Body Content
  c.setFont('Helvetica', 12)
  y = height - 100
  for line in text_lines:
    c.drawString(50, y, line)
    y -= 30

  c.save()
  print(f'✅ Generated Test PDF: {filepath}')


# 1. Verified Invoice (Matches PO & GRN perfectly)
create_invoice_pdf(
    'invoice_verified.pdf',
    [
        'Vendor: TechSolutions Inc.',
        'Invoice ID: INV-2026-001',
        'Quantity: 10',
        'Unit Price: $1000.00',
        'Total Amount Due: $10000.00',
    ],
)

# 2. Mismatched Invoice (Triggers 3-way match price/qty exception)
create_invoice_pdf(
    'invoice_mismatched.pdf',
    [
        'Vendor: TechSolutions Inc.',
        'Invoice ID: INV-9999',
        'Quantity: 10',
        'Unit Price: $100.00',
        'Total Amount Due: $1000.00',
    ],
)

# 3. Duplicate Invoice (Shares ID INV-2026-001 to test fraud block after first run)
create_invoice_pdf(
    'invoice_duplicate.pdf',
    [
        'Vendor: TechSolutions Inc.',
        'Invoice ID: INV-2026-001',
        'Quantity: 10',
        'Unit Price: $1000.00',
        'Total Amount Due: $10000.00',
    ],
)

# 4. Multilingual Invoice (Hindi/English mixed format for translation/regex fallback)
create_invoice_pdf(
    'invoice_multilingual.pdf',
    [
        'चालान संख्या (Invoice ID): INV-2026-HI99',
        'विक्रेता (Vendor): TechSolutions Corp',
        'मात्रा (Quantity): 5',
        'यूनिट कीमत (Unit Price): $150.00',
        'कुल राशि (Total Amount): $750.00',
    ],
)

print(
    '\n🚀 All 4 test invoice PDFs are ready inside data/raw_invoices/!'
)