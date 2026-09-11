import os
import sys
import json
import io
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from core.settings import SessionLocal, ensure_database_schema
from api.models import Payment, Quotation
from main import app

def run_tests():
    ensure_database_schema()
    client = TestClient(app)

    print("--- 1. Testing Next Invoice Number API ---")
    res_next = client.get("/api/payments/next-invoice-number")
    assert res_next.status_code == 200, f"Failed: {res_next.text}"
    next_data = res_next.json()
    print("  Next Invoice No:", next_data.get("invoice_no"))
    assert "invoice_no" in next_data
    assert next_data["invoice_no"].startswith("INV-")
    print("  [OK] /api/payments/next-invoice-number works!")

    print("\n--- 2. Testing Get Customers from Quotations ---")
    res_cust = client.get("/api/payments/customers")
    assert res_cust.status_code == 200, f"Failed: {res_cust.text}"
    cust_data = res_cust.json()
    print(f"  Found {cust_data.get('count')} customers from quotations:")
    for c in cust_data.get("customers", []):
        print(f"    Customer: {c.get('customer_name')}, Phone: {c.get('phone')}, Quotations: {len(c.get('quotations', []))}")
    assert cust_data["count"] > 0
    first_customer = cust_data["customers"][0]
    cust_name = first_customer["customer_name"]
    first_q = first_customer["quotations"][0] if first_customer["quotations"] else None
    print("  [OK] /api/payments/customers works!")

    print("\n--- 3. Testing Create Payment (JSON) with Auto-Generated Invoice No ---")
    payload_json = {
        "customer_name": cust_name,
        "quotation_id": first_q["id"] if first_q else None,
        "quotation_no": first_q["quotation_no"] if first_q else None,
        "payment_date": "17 Aug 2026",
        "amount_received": 150000.0,
        "payment_mode": "Online",
        "transaction_no": "UPI-9876543210",
        "reference_no": "PAY-REF-001",
        "notes": "50% Advance received via UPI",
        "status": "Received",
    }
    res_p1 = client.post("/api/payments", json=payload_json)
    assert res_p1.status_code == 201, f"Failed: {res_p1.text}"
    p1 = res_p1.json()["payment"]
    print("  Created Payment ID:", p1["id"])
    print("  Invoice No:", p1["invoice_no"])
    print("  Customer:", p1["customer_name"])
    print("  Amount:", p1["amount_received"])
    print("  Mode:", p1["payment_mode"])
    print("  Status:", p1["status"])
    assert p1["invoice_no"].startswith("INV-")
    assert p1["amount_received"] == 150000.0
    assert p1["payment_mode"] == "Online"
    print("  [OK] JSON Payment creation passed!")

    print("\n--- 4. Testing Create Payment (Multipart Form Data with Receipt Upload) ---")
    dummy_receipt = io.BytesIO(b"%PDF-1.4 dummy payment receipt content")
    form_data = {
        "customer_name": "Skyline Enterprises",
        "payment_date": "18 Aug 2026",
        "amount_received": "75000",
        "payment_mode": "Cash",
        "transaction_no": "CASH-REC-101",
        "notes": "Cash collected by sales executive",
        "status": "Received",
    }
    files = {
        "payment_proof": ("receipt.pdf", dummy_receipt, "application/pdf")
    }
    res_p2 = client.post("/api/payment/add", data=form_data, files=files)
    assert res_p2.status_code == 201, f"Failed: {res_p2.text}"
    p2 = res_p2.json()["payment"]
    print("  Created Payment 2 ID:", p2["id"])
    print("  Invoice No:", p2["invoice_no"])
    print("  Payment Proof Path:", p2["payment_proof"])
    assert p2["payment_proof"] is not None
    assert p2["payment_proof"].startswith("/uploads/payments/")
    print("  [OK] Multipart Payment creation with receipt upload passed!")

    print("\n--- 5. Testing List Payments with Filtering ---")
    list_res = client.get("/api/payments")
    assert list_res.status_code == 200
    list_data = list_res.json()
    print(f"  Total Payments in DB: {list_data['count']}")
    assert list_data["count"] >= 2

    # Filter by mode Online
    online_res = client.get("/api/payments?payment_mode=Online").json()
    print(f"  Online Payments: {online_res['count']}")
    assert all(p["payment_mode"] == "Online" for p in online_res["payments"])

    # Filter by mode Cash
    cash_res = client.get("/api/payments?payment_mode=Cash").json()
    print(f"  Cash Payments: {cash_res['count']}")
    assert all(p["payment_mode"] == "Cash" for p in cash_res["payments"])

    # Search filter
    search_res = client.get(f"/api/payments?search={p1['invoice_no']}").json()
    assert search_res["count"] == 1
    assert search_res["payments"][0]["id"] == p1["id"]
    print("  [OK] List and filter payments passed!")

    print("\n--- 6. Testing Get Single Payment Details ---")
    get_res = client.get(f"/api/payments/{p1['id']}")
    assert get_res.status_code == 200
    assert get_res.json()["id"] == p1["id"]
    print("  [OK] GET /api/payments/{id} works!")

    print("\n--- 7. Testing Update Payment ---")
    update_res = client.put(f"/api/payments/{p1['id']}", json={"notes": "Updated note: Verified with bank", "status": "Received"})
    assert update_res.status_code == 200
    assert update_res.json()["payment"]["notes"] == "Updated note: Verified with bank"
    print("  [OK] PUT /api/payments/{id} works!")

    print("\n--- 8. Testing Delete Payment ---")
    del_res = client.delete(f"/api/payments/{p2['id']}")
    assert del_res.status_code == 200
    print("  [OK] DELETE /api/payments/{id} works!")

    print("\n>>> All Payment API tests passed successfully! <<<")

if __name__ == "__main__":
    run_tests()
