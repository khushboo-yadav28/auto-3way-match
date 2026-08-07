from reportlab.pdfgen import canvas
import os

os.makedirs("data/raw_invoices", exist_ok=True)
pdf_path = "data/raw_invoices/sample_invoice.pdf"

c = canvas.Canvas(pdf_path)
c.setFont("Helvetica-Bold", 24)
c.drawString(50, 800, "INVOICE")

c.setFont("Helvetica", 12)
c.drawString(50, 750, "Invoice ID: INV-2026-001")
c.drawString(50, 730, "Vendor Name: Acme Corp")
c.drawString(50, 710, "Date: 2026-08-05")  # <-- Added Date Field
c.drawString(50, 690, "Description: Industrial Valves")
c.drawString(50, 670, "Total Items: 50")
c.drawString(50, 650, "Unit Price: $120.00")
c.drawString(50, 610, "Total Amount: $6000.00")

c.save()
print(f"Test PDF generated at: {pdf_path}")