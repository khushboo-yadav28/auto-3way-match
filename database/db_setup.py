import sqlite3
import os

def setup_database():
    os.makedirs('database', exist_ok=True)
    conn = sqlite3.connect('database/rpa_database.db')
    cursor = conn.cursor()

    # 1. DROP old tables so we start with a clean slate
    cursor.execute('DROP TABLE IF EXISTS purchase_orders')
    cursor.execute('DROP TABLE IF EXISTS goods_received_notes')

    # 2. Create Tables with the exact new 5-column and 4-column schemas
    cursor.execute('''CREATE TABLE purchase_orders (id TEXT PRIMARY KEY, vendor TEXT, item_qty INTEGER, unit_price REAL, total REAL)''')
    cursor.execute('''CREATE TABLE goods_received_notes (id TEXT PRIMARY KEY, po_id TEXT, vendor TEXT, received_qty INTEGER)''')

    # 3. Seed 3 Different Companies
    companies = [
        ("PO-1001", "TechSolutions Inc.", 10, 1000.00, 10000.00, "GRN-5001", 10),
        ("PO-1002", "OfficePro Supplies", 50, 20.00, 1000.00, "GRN-5002", 50),
        ("PO-1003", "GlobalHardware Corp", 5, 500.00, 2500.00, "GRN-5003", 5)
    ]

    for po_id, vendor, qty, price, total, grn_id, rec_qty in companies:
        cursor.execute('INSERT INTO purchase_orders VALUES (?, ?, ?, ?, ?)', (po_id, vendor, qty, price, total))
        cursor.execute('INSERT INTO goods_received_notes VALUES (?, ?, ?, ?)', (grn_id, po_id, vendor, rec_qty))

    conn.commit()
    conn.close()
    print("✅ Database updated with 3 different companies!")

if __name__ == "__main__":
    setup_database()