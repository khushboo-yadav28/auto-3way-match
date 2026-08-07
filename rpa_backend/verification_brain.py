import sqlite3
import os
from datetime import datetime

def verify_three_way_match(invoice_data):
    """
    Performs an automated Three-Way Match against local databases, 
    including advanced date validation logic[cite: 2].
    """
    db_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(db_dir, "database", "rpa_database.db")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('SELECT quantity, unit_price FROM purchase_orders WHERE vendor_name = ?', (invoice_data['vendor_name'],))
    po_record = cursor.fetchone()
    
    cursor.execute('SELECT quantity_received, received_date FROM goods_received_notes WHERE vendor_name = ?', (invoice_data['vendor_name'],))
    grn_record = cursor.fetchone()
    conn.close()
    
    if po_record and grn_record:
        po_qty, po_price = po_record
        grn_qty, grn_date_str = grn_record
        
        # 1. Standard Match Verification (Quantities & Pricing)
        if not (invoice_data['item_quantities'] == po_qty == grn_qty and invoice_data['unit_pricing'] == po_price):
            print("❌ Discrepancy Detected: Mismatch in expected quantities or pricing.")
            return False
            
        # 2. Complex Date Validation
        try:
            invoice_date = datetime.strptime(invoice_data['invoice_date'], "%Y-%m-%d")
            grn_date = datetime.strptime(grn_date_str, "%Y-%m-%d")
            
            if invoice_date < grn_date:
                print("❌ Temporal Discrepancy: Invoice is dated BEFORE goods were received.")
                return False
                
        except ValueError:
            print("❌ Validation Error: Invalid date format detected.")
            return False
            
        print("✅ Match Successful: Quantities, pricing, vendor, and dates align.")
        return True
        
    print("❌ Exception: Missing PO or GRN records.")
    return False