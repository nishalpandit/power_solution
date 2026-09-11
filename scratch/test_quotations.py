import os
import sys
import json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from core.settings import SessionLocal, ensure_database_schema
from main import app

def run_tests():
    ensure_database_schema()
    client = TestClient(app)

    print("1. Testing get_next_quotation_number...")
    next_res = client.get("/api/quotations/next-number")
    assert next_res.status_code == 200
    next_no_res = next_res.json()
    print("Next quotation number:", next_no_res)
    assert "quotation_no" in next_no_res
    qtn_no = next_no_res["quotation_no"]

    print("\n2. Testing create_quotation (Save & Send)...")
    payload = {
        "quotation_no": qtn_no,
        "quotation_date": "17 May 2025",
        "valid_till": "31 May 2025",
        "reference": "REF-2025-05",
        "customer_name": "Skyline Enterprises",
        "address": "45 Industrial Area, Phase 2, New Delhi",
        "phone": "+91 9876543210",
        "email": "contact@skyline.com",
        "items": [
            {
                "type": "Lift",
                "category": "Passenger Lift",
                "category_id": 4,
                "product": "LIFT001",
                "product_name": "G+2 Automatic Passenger Lift",
                "specifications": {
                    "Capacity": "4-6 Passenger",
                    "Rated Load": "320 KG",
                    "Speed": "0.65 - 1 m/s",
                    "Floor": "G+2",
                    "Stops": "3",
                    "Door Type": "Automatic",
                    "Door Opening": "Center Opening",
                    "Drive": "VVVF / VFD",
                    "Power Supply": "415V / 3 Phase / 50Hz",
                    "Cabin Finish": "SS",
                    "Controller": "Microprocessor Based"
                },
                "quantity": 1.0,
                "unit_price": 450000.0,
                "total_price": 450000.0
            },
            {
                "type": "Earthing",
                "category": "Earth Pit",
                "product": "EARTH001",
                "product_name": "Chemical Earthing Earth Pit",
                "specifications": {
                    "Earthing Type": "Chemical Earthing",
                    "Electrode": "GI / Copper",
                    "Earth Pit": "Maintenance Free",
                    "Back Fill Compound": "Chemical Compound",
                    "Connection": "Heavy Duty"
                },
                "quantity": 2.0,
                "unit_price": 12500.0,
                "total_price": 25000.0
            }
        ],
        "subtotal": 475000.0,
        "discount_type": "Flat",
        "discount_value": 25000.0,
        "discount_amount": 25000.0,
        "tax_type": "GST 18%",
        "tax_rate": 0.18,
        "taxable_amount": 450000.0,
        "tax_amount": 81000.0,
        "grand_total": 531000.0,
        "terms": "1. 50% advance along with purchase order.\n2. Delivery within 4-6 weeks.\n3. 1 year warranty.",
        "status": "Sent"
    }

    create_res = client.post("/api/quotations", json=payload)
    assert create_res.status_code == 201, f"Failed create: {create_res.text}"
    create_data = create_res.json()
    print("Create response message:", create_data["message"])
    q_data = create_data["quotation"]
    print("Created Quotation:", {
        "id": q_data["id"],
        "no": q_data["quotation_no"],
        "customer": q_data["customer_name"],
        "grand_total": q_data["grand_total"],
        "status": q_data["status"],
        "items_count": len(q_data["items"])
    })
    assert q_data["customer_name"] == "Skyline Enterprises"
    assert q_data["grand_total"] == 531000.0
    q_id = q_data["id"]

    print("\n3. Testing list_quotations...")
    list_res = client.get("/api/quotations")
    assert list_res.status_code == 200
    list_data = list_res.json()
    print(f"Total quotations in DB: {list_data['count']}")
    assert list_data["count"] >= 1

    print("\n4. Testing list_quotations with search (Skyline)...")
    search_res = client.get("/api/quotations?search=Skyline")
    assert search_res.status_code == 200
    search_data = search_res.json()
    print(f"Search results count: {search_data['count']}")
    assert search_data["count"] >= 1
    assert any(q["customer_name"] == "Skyline Enterprises" for q in search_data["results"])

    print(f"\n5. Testing get_quotation (ID={q_id})...")
    get_res = client.get(f"/api/quotations/{q_id}")
    assert get_res.status_code == 200
    get_data = get_res.json()
    print(f"Retrieved: {get_data['quotation_no']} - {get_data['customer_name']}")
    assert get_data["id"] == q_id

    print(f"\n6. Testing update_quotation (ID={q_id})...")
    payload["customer_name"] = "Apex Skyline Towers Pvt Ltd"
    payload["status"] = "Approved"
    update_res = client.put(f"/api/quotations/{q_id}", json=payload)
    assert update_res.status_code == 200
    update_data = update_res.json()
    print(f"Updated message: {update_data['message']}")
    assert update_data["quotation"]["customer_name"] == "Apex Skyline Towers Pvt Ltd"
    assert update_data["quotation"]["status"] == "Approved"

    print(f"\n7. Testing delete_quotation (ID={q_id})...")
    del_res = client.delete(f"/api/quotations/{q_id}")
    assert del_res.status_code == 200
    print(f"Delete response: {del_res.json()['message']}")

    print("\nAll quotation view functions tested and passed with 100% success!")

if __name__ == "__main__":
    run_tests()
