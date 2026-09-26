import sqlite3

def migrate():
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    
    # Enable foreign keys just to be safe, then disable for migration
    cursor.execute('PRAGMA foreign_keys=OFF;')
    cursor.execute('BEGIN TRANSACTION;')
    
    try:
        # 1. Rename old table
        cursor.execute('ALTER TABLE stock_in_receipts RENAME TO old_stock_in_receipts;')
        
        # 2. Re-create the table with invoice_no allowing NULL
        cursor.execute('''
        CREATE TABLE stock_in_receipts (
            id INTEGER NOT NULL,
            receipt_no VARCHAR(60) NOT NULL,
            receipt_date VARCHAR(50) NOT NULL,
            po_number VARCHAR(60),
            invoice_no VARCHAR(60),
            invoice_date VARCHAR(50) NOT NULL,
            supplier_id INTEGER,
            supplier_code VARCHAR(50),
            supplier_name VARCHAR(150) NOT NULL,
            supplier_contact VARCHAR(50),
            product_id INTEGER,
            product_sku VARCHAR(100),
            product_type VARCHAR(50) NOT NULL,
            category VARCHAR(100) NOT NULL,
            product_name VARCHAR(150) NOT NULL,
            specifications JSON,
            quantity FLOAT NOT NULL,
            unit VARCHAR(50) NOT NULL,
            warehouse VARCHAR(100) NOT NULL,
            rack VARCHAR(100),
            batch_no VARCHAR(100),
            serial_no VARCHAR(150),
            rate FLOAT NOT NULL,
            discount FLOAT NOT NULL,
            gst FLOAT NOT NULL,
            gross_amount FLOAT NOT NULL,
            taxable_amount FLOAT NOT NULL,
            gst_amount FLOAT NOT NULL,
            total_amount FLOAT NOT NULL,
            received_by VARCHAR(100) NOT NULL,
            condition VARCHAR(50) NOT NULL,
            inspection_status VARCHAR(50) NOT NULL,
            inspection_remarks TEXT,
            notes TEXT,
            status VARCHAR(30) NOT NULL,
            created_at DATETIME NOT NULL,
            updated_at DATETIME NOT NULL,
            PRIMARY KEY (id),
            FOREIGN KEY(supplier_id) REFERENCES suppliers (id) ON DELETE SET NULL,
            FOREIGN KEY(product_id) REFERENCES products (id) ON DELETE SET NULL
        );
        ''')
        
        # 3. Copy data
        cursor.execute('INSERT INTO stock_in_receipts SELECT * FROM old_stock_in_receipts;')
        
        # 4. Drop old table
        cursor.execute('DROP TABLE old_stock_in_receipts;')
        
        # 5. Re-create indexes
        cursor.execute('CREATE UNIQUE INDEX ix_stock_in_receipts_receipt_no ON stock_in_receipts (receipt_no);')
        cursor.execute('CREATE INDEX ix_stock_in_receipts_id ON stock_in_receipts (id);')
        cursor.execute('CREATE INDEX ix_stock_in_receipts_po_number ON stock_in_receipts (po_number);')
        cursor.execute('CREATE INDEX ix_stock_in_receipts_invoice_no ON stock_in_receipts (invoice_no);')
        cursor.execute('CREATE INDEX ix_stock_in_receipts_supplier_id ON stock_in_receipts (supplier_id);')
        cursor.execute('CREATE INDEX ix_stock_in_receipts_supplier_code ON stock_in_receipts (supplier_code);')
        cursor.execute('CREATE INDEX ix_stock_in_receipts_product_id ON stock_in_receipts (product_id);')
        cursor.execute('CREATE INDEX ix_stock_in_receipts_product_sku ON stock_in_receipts (product_sku);')
        cursor.execute('CREATE INDEX ix_stock_in_receipts_product_type ON stock_in_receipts (product_type);')
        cursor.execute('CREATE INDEX ix_stock_in_receipts_category ON stock_in_receipts (category);')
        
        conn.commit()
        print("Migration successful: invoice_no is now optional.")
    except Exception as e:
        conn.rollback()
        print(f"Migration failed: {e}")
    finally:
        cursor.execute('PRAGMA foreign_keys=ON;')
        conn.close()

if __name__ == "__main__":
    migrate()
