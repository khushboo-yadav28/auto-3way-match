import sqlite3

def verify_three_way_match(invoice_data):
    vendor = invoice_data.get('vendor_name')
    inv_qty = invoice_data.get('item_quantities')
    inv_price = invoice_data.get('unit_pricing')
    inv_total = invoice_data.get('total_amount')

    # Connect to the updated database
    conn = sqlite3.connect('database/rpa_database.db')
    cursor = conn.cursor()

    try:
        # 1. Check Purchase Orders (Match by vendor name)
        cursor.execute("SELECT item_qty, unit_price, total FROM purchase_orders WHERE vendor = ?", (vendor,))
        po_record = cursor.fetchone()

        if not po_record:
            print(f"❌ Match Failed: No Purchase Order found for vendor: {vendor}")
            return False

        po_qty, po_price, po_total = po_record

        # 2. Check Goods Received Notes
        cursor.execute("SELECT received_qty FROM goods_received_notes WHERE vendor = ?", (vendor,))
        grn_record = cursor.fetchone()

        if not grn_record:
            print(f"❌ Match Failed: No Goods Received Note found for vendor: {vendor}")
            return False

        grn_qty = grn_record[0]

        # 3. Perform the 3-Way Match Logic
        if int(inv_qty) != int(po_qty) or int(inv_qty) != int(grn_qty):
            print("❌ Match Failed: Quantity mismatch between Invoice, PO, and GRN!")
            return False

        if float(inv_price) != float(po_price) or float(inv_total) != float(po_total):
            print("❌ Match Failed: Pricing mismatch between Invoice and Purchase Order!")
            return False

        print("✅ Match Successful: Quantities, pricing, and vendor align.")
        return True

    finally:
        conn.close()