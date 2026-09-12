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
    print("=== TEST 1: GET Next Order Number ===")
    status, res = request_api("/api/orders/next-order-number")
    print(f"Status: {status}")
    print(res)
    assert status == 200
    assert "order_no" in res
    order_no = res["order_no"]
    print("  [OK] Next Order Number verified:", order_no)

    print("\n=== TEST 2: GET Order Quotations Dropdown ===")
    status, res = request_api("/api/orders/quotations")
    print(f"Status: {status}")
    print(f"Count: {res.get('count')}")
    assert status == 200
    assert "results" in res
    if res["results"]:
        q0 = res["results"][0]
        print(f"First quotation ID: {q0.get('id')} | Customer: {q0.get('customer')}")
        print(f"Items count: {len(q0.get('items', []))}")
    print("  [OK] Quotations dropdown endpoint verified!")

    print("\n=== TEST 3: POST Create Order (Flutter Form Payload) ===")
    order_payload = {
        "order_no": order_no,
        "quotation_id": "QTN-250517-0001",
        "order_date": "17 May 2025",
        "delivery_date": "31 May 2025",
        "order_status": "Pending",
        "customer": {
            "name": "Skyline Enterprises",
            "mobile": "9876543210",
            "email": "contact@skyline.com",
            "billing_address": "45 Industrial Area, Phase 2, New Delhi",
            "delivery_address": "45 Industrial Area, Phase 2, New Delhi",
        },
        "subtotal": 450000.0,
        "discount": 25000.0,
        "tax": 76500.0,
        "grand_total": 501500.0,
        "advance_paid": 50000.0,
        "balance_amount": 451500.0,
        "payment_status": "Partially Paid",
        "payment_mode": "Bank Transfer",
        "transaction_no": "TXN-BANK-10023",
        "payment_date": "17 May 2025",
        "special_instructions": "Handle lift components with care during transit",
        "internal_notes": "Priority VIP client",
        "terms_accepted": True,
    }
    status, res = request_api("/api/orders", data=order_payload, method="POST")
    print(f"Status: {status}")
    print(json.dumps(res, indent=2))
    assert status == 201
    assert "order" in res
    order_id = res["order"]["id"]
    print(f"  [OK] Order created with ID: {order_id}")

    print("\n=== TEST 4: GET List Orders with Filter ===")
    status, res = request_api(f"/api/orders?search={order_no}")
    print(f"Status: {status}")
    print(f"Count: {res.get('count')}")
    assert status == 200
    assert res["count"] >= 1
    print("  [OK] Order search verified!")

    print("\n=== TEST 5: GET Single Order Details ===")
    status, res = request_api(f"/api/orders/{order_id}")
    print(f"Status: {status}")
    assert status == 200
    assert res["order_no"] == order_no
    assert res["advance_paid"] == 50000.0
    print("  [OK] Single order retrieval verified!")

    print("\n=== TEST 6: PUT Update Order (Status to Confirmed) ===")
    update_payload = {
        "order_status": "Confirmed",
        "advance_paid": 150000.0,
        "payment_status": "Partially Paid",
        "internal_notes": "Updated: Client transferred 1.5L advance",
    }
    status, res = request_api(f"/api/orders/{order_id}", data=update_payload, method="PUT")
    print(f"Status: {status}")
    assert status == 200
    assert res["order"]["order_status"] == "Confirmed"
    assert res["order"]["advance_paid"] == 150000.0
    assert res["order"]["balance_amount"] == 351500.0  # 501500 - 150000
    print("  [OK] Order update and balance recalculation verified!")

    print("\n=== TEST 7: DELETE Order ===")
    status, res = request_api(f"/api/orders/{order_id}", method="DELETE")
    print(f"Status: {status}")
    assert status == 200
    print("  [OK] Order deletion verified!")

    print("\n=============================================")
    print("ALL 7 ORDER API TESTS PASSED SUCCESSFULLY!")
    print("=============================================")


if __name__ == "__main__":
    main()
