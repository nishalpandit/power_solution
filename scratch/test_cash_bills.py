import json
import urllib.request

BASE_URL = "http://192.168.1.59:8000"


def request_api(endpoint, data=None, method="GET"):
    url = f"{BASE_URL}{endpoint}"
    req = urllib.request.Request(url, method=method)
    body = None
    if data is not None:
        req.add_header("Content-Type", "application/json")
        body = json.dumps(data).encode("utf-8")

    try:
        with urllib.request.urlopen(req, data=body) as response:
            res_body = response.read().decode("utf-8")
            return response.status, json.loads(res_body) if res_body else {}
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8")
        try:
            return e.code, json.loads(err_body)
        except Exception:
            return e.code, {"error": err_body}


def main():
    print("=== TEST 1: GET Next Bill Number ===")
    status, res = request_api("/api/cash-bills/next-bill-number")
    print(f"Status: {status}")
    print(res)
    assert status == 200
    assert "bill_no" in res
    bill_no = res["bill_no"]
    print("  [OK] Next Bill Number:", bill_no)

    print("\n=== TEST 2: GET Product Picker Master ===")
    status, res = request_api("/api/cash-bills/product-picker")
    print(f"Status: {status}")
    assert status == 200
    assert "product_types" in res
    assert "categories" in res
    assert "products" in res
    assert "Lift" in res["product_types"]
    assert "Passenger Lift" in res["categories"]["Lift"]
    assert len(res["products"]["Passenger Lift"]) > 0
    print("  [OK] Product Picker hierarchy verified!")

    print("\n=== TEST 3: POST Live Calculation Preview ===")
    calc_payload = {
        "items": [
            {
                "id": "LIFT001",
                "name": "G+2 Automatic Passenger Lift",
                "price": 450000.0,
                "qty": 1,
            },
            {
                "id": "EARTH001",
                "name": "Chemical Earthing Earth Pit",
                "price": 12500.0,
                "qty": 2,
            },
        ],
        "discount": 0.0,
        "amount_paid": 500000.0,
    }
    status, res = request_api("/api/cash-bills/calculate", data=calc_payload, method="POST")
    print(f"Status: {status}")
    print(json.dumps(res, indent=2))
    assert status == 200
    # Subtotal: 450000 + 25000 = 475000.0
    assert res["subtotal"] == 475000.0
    # Taxable: 475000.0
    assert res["taxable_amount"] == 475000.0
    # GST 18%: 475000 * 0.18 = 85500.0
    assert res["gst"] == 85500.0
    # Grand Total: 475000 + 85500 = 560500.0
    assert res["grand_total"] == 560500.0
    # Amount Paid: 500000.0
    # Balance: 560500 - 500000 = 60500.0
    assert res["balance_amount"] == 60500.0
    assert res["change_returned"] == 0.0
    assert res["payment_status"] == "Partially Paid"
    print("  [OK] Accurate tax and balance calculation verified!")

    print("\n=== TEST 4: POST Generate Cash Bill (Cash Overpayment & Change Returned) ===")
    bill_payload = {
        "bill_no": bill_no,
        "bill_date": "12 Sep 2026",
        "customer_type": "Walk-in Customer",
        "customer_name": "Rohan Sharma",
        "mobile": "9876500001",
        "items": [
            {
                "id": "LIFT001",
                "name": "G+2 Automatic Passenger Lift",
                "type": "Lift",
                "category": "Passenger Lift",
                "price": 450000.0,
                "qty": 1,
                "specifications": {
                    "Capacity": "4-6 Passenger",
                    "Rated Load": "320 KG",
                },
            }
        ],
        "payment_mode": "Cash",
        "amount_paid": 550000.0,  # Grand total is 531000, overpaid by 19000
        "notes": "Delivered lift motor directly from counter",
        "status": "Generated",
    }
    status, res = request_api("/api/cash-bills", data=bill_payload, method="POST")
    print(f"Status: {status}")
    print(json.dumps(res, indent=2))
    assert status == 201
    assert "bill" in res
    bill_id = res["bill"]["id"]
    assert res["bill"]["subtotal"] == 450000.0
    assert res["bill"]["gst_amount"] == 81000.0
    assert res["bill"]["grand_total"] == 531000.0
    assert res["bill"]["change_returned"] == 19000.0
    assert res["bill"]["balance_amount"] == 0.0
    assert res["bill"]["payment_status"] == "Paid"
    print(f"  [OK] Cash bill created with ID: {bill_id} and change returned: 19000.0")

    print("\n=== TEST 5: GET List Cash Bills ===")
    status, res = request_api(f"/api/cash-bills?search={bill_no}")
    print(f"Status: {status}")
    assert status == 200
    assert res["count"] >= 1
    print("  [OK] Cash bill list and search verified!")

    print("\n=== TEST 6: GET Single Cash Bill Details ===")
    status, res = request_api(f"/api/cash-bills/{bill_id}")
    print(f"Status: {status}")
    assert status == 200
    assert res["bill_no"] == bill_no
    assert res["customer_name"] == "Rohan Sharma"
    print("  [OK] Single cash bill retrieval verified!")

    print("\n=== TEST 7: PUT Update Cash Bill ===")
    update_payload = {
        "notes": "Updated: Receipt handed over to customer",
        "customer_type": "Existing Customer",
    }
    status, res = request_api(f"/api/cash-bills/{bill_id}", data=update_payload, method="PUT")
    print(f"Status: {status}")
    assert status == 200
    assert res["bill"]["customer_type"] == "Existing Customer"
    assert "Receipt handed over" in res["bill"]["notes"]
    print("  [OK] Cash bill update verified!")

    print("\n=== TEST 8: DELETE Cash Bill ===")
    status, res = request_api(f"/api/cash-bills/{bill_id}", method="DELETE")
    print(f"Status: {status}")
    assert status == 200
    print("  [OK] Cash bill deletion verified!")

    print("\n=================================================")
    print("ALL 8 CASH BILL API TESTS PASSED SUCCESSFULLY!")
    print("=================================================")


if __name__ == "__main__":
    main()
