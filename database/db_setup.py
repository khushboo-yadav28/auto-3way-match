import sqlite3
import os

def init_db():
    # Ensure database directory exists
    db_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(db_dir, "rpa_database.db")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("Creating tables...")

    # 1. Create Purchase Orders Table (What was ordered)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS purchase_orders (
            po_number TEXT PRIMARY KEY,
            vendor_name TEXT NOT NULL,
            item_description TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL,
            total_amount REAL NOT NULL
        )
    ''')

    # 2. Create Goods Received Notes Table (What arrived at warehouse)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS goods_received_notes (
            grn_number TEXT PRIMARY KEY,
            po_number TEXT NOT NULL,
            vendor_name TEXT NOT NULL,
            quantity_received INTEGER NOT NULL,
            received_date TEXT NOT NULL,
            FOREIGN KEY (po_number) REFERENCES purchase_orders (po_number)
        )
    ''')

    # Seed Mock Data for Testing
    print("Seeding mock records...")

    # Clear existing records to allow re-running script cleanly
    cursor.execute("DELETE FROM purchase_orders")
    cursor.execute("DELETE FROM goods_received_notes")

    # Sample Match Scenario 1: Perfect Match (Acme Corp)
    cursor.execute('''
        INSERT INTO purchase_orders VALUES ('PO-1001', 'Acme Corp', 'Industrial Valves', 50, 120.00, 6000.00)
    ''')
    cursor.execute('''
        INSERT INTO goods_received_notes VALUES ('GRN-5001', 'PO-1001', 'Acme Corp', 50, '2026-08-01')
    ''')

    # Sample Match Scenario 2: Overbilling / Discrepancy Test (Global Tech)
    cursor.execute('''
        INSERT INTO purchase_orders VALUES ('PO-1002', 'Global Tech', 'Microcontrollers', 100, 15.00, 1500.00)
    ''')
    cursor.execute('''
        INSERT INTO goods_received_notes VALUES ('GRN-5002', 'PO-1002', 'Global Tech', 80, '2026-08-03')
    ''')

    conn.commit()
    conn.close()
    print(f"✅ Database initialized successfully at: {db_path}")

if __name__ == "__main__":
    init_db()