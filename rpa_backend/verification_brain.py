import sqlite3
from notification_engine import alert_manager_of_discrepancy


def verify_three_way_match(invoice_data):
  invoice_id = invoice_data.get('invoice_id')
  vendor = invoice_data.get('vendor_name')
  inv_qty = invoice_data.get('item_quantities')
  inv_price = invoice_data.get('unit_pricing')
  inv_total = invoice_data.get('total_amount')

  # Connect to the SQLite database
  conn = sqlite3.connect('database/rpa_database.db')
  cursor = conn.cursor()

  try:
    # Ensure processed_invoices table exists automatically
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS processed_invoices (
                invoice_id TEXT PRIMARY KEY,
                vendor TEXT,
                total REAL,
                processed_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
    conn.commit()

    # 0. Duplicate Invoice & Fraud Prevention Check
    cursor.execute(
        'SELECT COUNT(*) FROM processed_invoices WHERE invoice_id = ?',
        (invoice_id,),
    )
    is_duplicate = cursor.fetchone()[0] > 0

    if is_duplicate:
      print(
          f'🚨 FRAUD ALERT: Duplicate invoice detected for ID: {invoice_id}.'
          ' Blocking payment.'
      )
      alert_manager_of_discrepancy(
          invoice_data, f'Duplicate Invoice ID Detected: {invoice_id}'
      )
      return False

    # 1. Check Purchase Orders (Match by vendor name)
    cursor.execute(
        'SELECT item_qty, unit_price, total FROM purchase_orders WHERE vendor'
        ' = ?',
        (vendor,),
    )
    po_record = cursor.fetchone()

    if not po_record:
      print(f'❌ Match Failed: No Purchase Order found for vendor: {vendor}')
      alert_manager_of_discrepancy(invoice_data, 'No PO Found')
      return False

    po_qty, po_price, po_total = po_record

    # 2. Check Goods Received Notes
    cursor.execute(
        'SELECT received_qty FROM goods_received_notes WHERE vendor = ?',
        (vendor,),
    )
    grn_record = cursor.fetchone()

    if not grn_record:
      print(
          '❌ Match Failed: No Goods Received Note found for vendor:'
          f' {vendor}'
      )
      alert_manager_of_discrepancy(invoice_data, po_total)
      return False

    grn_qty = grn_record[0]

    # 3. Perform the 3-Way Match Logic
    if int(inv_qty) != int(po_qty) or int(inv_qty) != int(grn_qty):
      print(
          '❌ Match Failed: Quantity mismatch between Invoice, PO, and GRN!'
      )
      alert_manager_of_discrepancy(invoice_data, po_total)
      return False

    if float(inv_price) != float(po_price) or float(inv_total) != float(
        po_total
    ):
      print(
          '❌ Match Failed: Pricing mismatch between Invoice and Purchase'
          ' Order!'
      )
      alert_manager_of_discrepancy(invoice_data, po_total)
      return False

    # ✅ MATCH SUCCESSFUL: Record in processed_invoices to block future duplicates
    try:
      cursor.execute(
          'INSERT OR IGNORE INTO processed_invoices (invoice_id, vendor,'
          ' total) VALUES (?, ?, ?)',
          (invoice_id, vendor, inv_total),
      )
      conn.commit()
    except Exception as db_err:
      print(f'[WARNING] Could not log processed invoice to database: {db_err}')

    print('✅ Match Successful: Quantities, pricing, and vendor align.')
    return True

  finally:
    conn.close()