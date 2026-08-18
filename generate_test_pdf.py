from reportlab.pdfgen import canvas
import os

def create_invoice(filename, invoice_id, vendor, qty, price, total):
    os.makedirs('data/raw_invoices', exist_ok=True)
    filepath = f"data/raw_invoices/{filename}"
    c = canvas.Canvas(filepath)
    
    c.setFont("Helvetica-Bold", 24)
    c.drawString(50, 800, "INVOICE")
    
    c.setFont("Helvetica", 14)
    c.drawString(50, 750, f"Invoice Number: {invoice_id}")
    c.drawString(50, 720, f"Vendor: {vendor}")
    c.drawString(50, 690, f"Item Quantities: {qty}")
    c.drawString(50, 660, f"Unit Pricing: ${price:.2f}")
    
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 600, f"Total Amount Due: ${total:.2f}")
    
    c.save()
    print(f"✅ Generated: {filepath}")

if __name__ == "__main__":
    create_invoice("invoice_techsolutions.pdf", "INV-2026-001", "TechSolutions Inc.", 10, 1000.00, 10000.00)
    create_invoice("invoice_officepro.pdf", "INV-2026-002", "OfficePro Supplies", 50, 20.00, 1000.00)
    create_invoice("invoice_globalhardware.pdf", "INV-2026-003", "GlobalHardware Corp", 5, 500.00, 2500.00)