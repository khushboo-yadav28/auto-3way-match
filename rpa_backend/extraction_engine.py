import re
import PyPDF2 

def extract_text_from_pdf(pdf_path):
    """
    Reads the raw text out of the downloaded PDF.
    """
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() + "\n"
            print("--- RAW PDF TEXT ---")
            print(text)
            print("--------------------")
    
        return text
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return ""

def extract_invoice_data(text):
    """
    Extracts structured data using flexible regex patterns.
    """
    data = {
        'invoice_id': None,
        'vendor_name': None,
        'item_quantities': None,
        'unit_pricing': None,
        'total_amount': None
    }

    # Matches "Vendor: Name" or "From: Name"
    vendor_match = re.search(r'(?:Vendor|From):\s*(.+)', text, re.IGNORECASE)
    if vendor_match: data['vendor_name'] = vendor_match.group(1).strip()

    # Matches "Invoice ID: 123", "Invoice #: 123", or "Invoice: 123"
    id_match = re.search(r'Invoice\s*(?:ID|#|Number)?\s*:\s*([\w-]+)', text, re.IGNORECASE)
    if id_match: data['invoice_id'] = id_match.group(1).strip()

    # Matches "10 x", "Qty: 10", or "Quantity: 10"
    # Matches "Item Quantities: 5", "Quantity: 10", "Qty: 10", or "10 x"
    qty_match = re.search(r'(?:Qty|Quantity|Quantities)\s*:\s*(\d+)|(\d+)\s*x', text, re.IGNORECASE)
    if qty_match: 
        data['item_quantities'] = int(qty_match.group(1) or qty_match.group(2))

    # Matches "Unit Pricing: $500.00", "Unit Price: $500", "Price: $500", or "at $500"
    price_match = re.search(r'(?:at|Price|Unit Price|Unit Pricing)\s*:?\s*\$?\s*([\d,\.]+)', text, re.IGNORECASE)
    if price_match: 
        data['unit_pricing'] = float(price_match.group(1).replace(',', ''))
    # Matches "Total: $1000", "Amount Due: $1000", or "Total Amount: $1000"
    total_match = re.search(r'(?:Total(?: Amount)?|Amount Due)\s*:?\s*\$?\s*([\d,\.]+)', text, re.IGNORECASE)
    if total_match: data['total_amount'] = float(total_match.group(1).replace(',', ''))

    return data