import json
import asyncio
from api.views import create_quotation
from core.settings import SessionLocal, ensure_database_schema

async def run_tests():
    ensure_database_schema()
    db = SessionLocal()

    # 1. Test multipart/form-data
    form_data = {
        "quotation_no": "QTN-250517-FORM1",
        "quotation_date": "17 May 2025",
        "valid_till": "31 May 2025",
        "reference": "REF-2025-05",
        "customer_name": "Skyline Enterprises (Form Data)",
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
                    "Rated Load": "320 KG"
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
        "terms": "1. 50% advance.",
        "status": "Sent"
    }

    class MockFormRequest:
        def __init__(self, data):
            self.headers = {"content-type": "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW"}
            self._data = data

        async def form(self):
            return self._data

        async def json(self):
            return self._data

    print("1. Testing multipart/form-data...")
    res_form = await create_quotation(request=MockFormRequest(form_data), db=db)
    print("Form-data success:", res_form["message"])
    assert res_form["quotation"]["customer_name"] == "Skyline Enterprises (Form Data)"

    # 2. Test application/json
    json_data = {
        "quotation_no": "QTN-250517-JSON1",
        "quotation_date": "17 May 2025",
        "valid_till": "31 May 2025",
        "reference": "REF-2025-05",
        "customer_name": "Skyline Enterprises (JSON)",
        "address": "45 Industrial Area, Phase 2, New Delhi",
        "phone": "+91 9876543210",
        "email": "contact@skyline.com",
        "items": [
            {
                "type": "Lift",
                "category": "Passenger Lift",
                "product": "LIFT001",
                "product_name": "G+2 Automatic Passenger Lift",
                "specifications": {
                    "Capacity": "4-6 Passenger",
                    "Rated Load": "320 KG"
                },
                "quantity": 1,
                "unit_price": 450000.0,
                "total_price": 450000.0
            }
        ],
        "subtotal": 450000.0,
        "discount_value": 25000.0,
        "discount_type": "Flat",
        "discount_amount": 25000.0,
        "tax_type": "GST 18%",
        "tax_rate": 0.18,
        "taxable_amount": 425000.0,
        "tax_amount": 76500.0,
        "grand_total": 501500.0,
        "terms": "1. 50% advance.",
        "status": "Sent"
    }

    class MockJsonRequest:
        def __init__(self, data):
            self.headers = {"content-type": "application/json"}
            self._data = data

        async def form(self):
            return self._data

        async def json(self):
            return self._data

    print("\n2. Testing application/json...")
    res_json = await create_quotation(request=MockJsonRequest(json_data), db=db)
    print("JSON success:", res_json["message"])
    assert res_json["quotation"]["customer_name"] == "Skyline Enterprises (JSON)"

    print("\nBoth multipart/form-data and application/json passed seamlessly!")

    db.close()

if __name__ == "__main__":
    asyncio.run(run_tests())
