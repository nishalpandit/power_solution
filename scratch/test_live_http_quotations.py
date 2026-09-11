import json
import urllib.request
import urllib.parse
import uuid

BASE_URL = "http://192.168.1.59:8000/api"

def make_request(url, method="GET", data=None, headers=None):
    if headers is None:
        headers = {}
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as response:
            status_code = response.status
            body = response.read().decode("utf-8")
            try:
                parsed = json.loads(body)
            except Exception:
                parsed = body
            return status_code, parsed
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        try:
            parsed = json.loads(error_body)
        except Exception:
            parsed = error_body
        return e.code, parsed
    except Exception as e:
        return 500, str(e)


def build_multipart_body(fields):
    boundary = f"----WebKitFormBoundary{uuid.uuid4().hex}"
    lines = []
    for key, val in fields.items():
        lines.append(f"--{boundary}".encode("utf-8"))
        lines.append(f'Content-Disposition: form-data; name="{key}"\r\n'.encode("utf-8"))
        lines.append(f"{val}".encode("utf-8"))
    lines.append(f"--{boundary}--\r\n".encode("utf-8"))
    body = b"\r\n".join(lines)
    content_type = f"multipart/form-data; boundary={boundary}"
    return body, content_type


def test_all():
    print("==================================================")
    print("TESTING ALL QUOTATION APIS LIVE ON 192.168.1.59:8000")
    print("==================================================")

    # 1. GET Next Quotation Number
    print("\n[1/7] GET /api/quotations/next-number")
    status, res = make_request(f"{BASE_URL}/quotations/next-number")
    print(f"Status: {status}")
    print(f"Response: {json.dumps(res, indent=2)}")
    assert status == 200
    assert "quotation_no" in res
    next_qtn_no = res["quotation_no"]

    # 2. POST /api/quotations with MULTIPART/FORM-DATA (Postman style)
    print("\n[2/7] POST /api/quotations (Testing with multipart/form-data as in Postman)")
    form_fields = {
        "quotation_no": next_qtn_no,
        "quotation_date": "17 May 2025",
        "valid_till": "31 May 2025",
        "reference": "REF-2025-05",
        "customer_name": "Skyline Enterprises",
        "address": "45 Industrial Area, Phase 2, New Delhi",
        "phone": "+91 9876543210",
        "email": "contact@skyline.com",
        "items": json.dumps([
            {
                "type": "Lift",
                "category": "Passenger Lift",
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
                "quantity": 1,
                "unit_price": 450000.0,
                "total_price": 450000.0
            }
        ]),
        "subtotal": "450000.0",
        "discount_value": "25000.0",
        "discount_type": "Flat",
        "discount_amount": "25000.0",
        "tax_type": "GST 18%",
        "tax_rate": "0.18",
        "taxable_amount": "425000.0",
        "tax_amount": "76500.0",
        "grand_total": "501500.0",
        "terms": "1. 50% advance along with purchase order.\n2. Delivery within 4-6 weeks.\n3. 1 year warranty.",
        "status": "Sent"
    }
    body, ct = build_multipart_body(form_fields)
    status, res = make_request(f"{BASE_URL}/quotations", method="POST", data=body, headers={"Content-Type": ct})
    print(f"Status: {status}")
    print(f"Response: {json.dumps(res, indent=2)}")
    assert status == 201, f"Expected 201, got {status}: {res}"
    form_quotation_id = res["quotation"]["id"]

    # 3. POST /api/quotations with APPLICATION/JSON
    print("\n[3/7] POST /api/quotations (Testing with application/json)")
    json_payload = {
        "quotation_no": f"QTN-JSON-{uuid.uuid4().hex[:6].upper()}",
        "quotation_date": "18 May 2025",
        "valid_till": "01 June 2025",
        "reference": "REF-JSON-TEST",
        "customer_name": "Apex Builders Group",
        "address": "77 Ring Road, Bangalore",
        "phone": "+91 9123456780",
        "email": "procurement@apexbuilders.com",
        "items": [
            {
                "type": "Generator",
                "category": "Silent Generator",
                "product": "DG001",
                "product_name": "Silent DG 60 KVA",
                "specifications": {
                    "Rating": "60 KVA / 48 KW",
                    "Voltage": "430 V"
                },
                "quantity": 1,
                "unit_price": 650000.0,
                "total_price": 650000.0
            }
        ],
        "subtotal": 650000.0,
        "discount_value": 50000.0,
        "discount_type": "Flat",
        "tax_type": "GST 18%",
        "terms": "Full payment upon delivery.",
        "status": "Draft"
    }
    json_body = json.dumps(json_payload).encode("utf-8")
    status, res = make_request(f"{BASE_URL}/quotations", method="POST", data=json_body, headers={"Content-Type": "application/json"})
    print(f"Status: {status}")
    print(f"Response: {json.dumps(res, indent=2)}")
    assert status == 201, f"Expected 201, got {status}: {res}"
    json_quotation_id = res["quotation"]["id"]

    # 4. GET /api/quotations (List All)
    print("\n[4/7] GET /api/quotations (List All & Filter/Search)")
    status, res = make_request(f"{BASE_URL}/quotations")
    print(f"Status: {status}, Total quotations count: {res.get('count', 0)}")
    assert status == 200

    # Search filter test
    status, res = make_request(f"{BASE_URL}/quotations?search=Skyline")
    print(f"Search 'Skyline' results: {res.get('count', 0)}")
    assert status == 200
    assert res["count"] >= 1

    # 5. GET /api/quotations/{id}
    print(f"\n[5/7] GET /api/quotations/{form_quotation_id} (Get single quotation)")
    status, res = make_request(f"{BASE_URL}/quotations/{form_quotation_id}")
    print(f"Status: {status}")
    print(f"Quotation: {res.get('quotation_no')} | Customer: {res.get('customer_name')} | Grand Total: {res.get('grand_total')}")
    assert status == 200

    # 6. PUT /api/quotations/{id} (Update Quotation)
    print(f"\n[6/7] PUT /api/quotations/{form_quotation_id} (Update Quotation via Form-Data)")
    form_fields["customer_name"] = "Skyline Enterprises (UPDATED)"
    form_fields["status"] = "Approved"
    body, ct = build_multipart_body(form_fields)
    status, res = make_request(f"{BASE_URL}/quotations/{form_quotation_id}", method="PUT", data=body, headers={"Content-Type": ct})
    print(f"Status: {status}")
    print(f"Updated Customer Name: {res['quotation']['customer_name']}")
    print(f"Updated Status: {res['quotation']['status']}")
    assert status == 200
    assert res["quotation"]["customer_name"] == "Skyline Enterprises (UPDATED)"

    # 7. DELETE /api/quotations/{id}
    print(f"\n[7/7] DELETE /api/quotations/{json_quotation_id} (Delete JSON test quotation)")
    status, res = make_request(f"{BASE_URL}/quotations/{json_quotation_id}", method="DELETE")
    print(f"Status: {status}")
    print(f"Response: {res}")
    assert status == 200

    print("\n==================================================")
    print("ALL 7 QUOTATION API ENDPOINTS WORKING 100% PERFECTLY!")
    print("==================================================")

if __name__ == "__main__":
    test_all()
