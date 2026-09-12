# Cash Bill API Documentation

## 1. Get Next Auto-Generated Cash Bill Number

url : (http://192.168.1.59:8000/api/cash-bills/next-bill-number)
method : GET

params :- 

(None)

response :- 

{
  "bill_no": "CB-260912-0001"
}

---

## 2. Product Picker Master (Categories & Products)

url : (http://192.168.1.59:8000/api/cash-bills/product-picker)
method : GET

params :- 

(None)

response :- 

{
  "product_types": [
    "Lift",
    "Generator",
    "LT Panel",
    "Earthing",
    "Service",
    "Other"
  ],
  "categories": {
    "Lift": [
      "Passenger Lift",
      "Goods Lift",
      "Hospital Lift",
      "Home Lift"
    ],
    "Generator": [
      "Silent Generator",
      "Open Generator"
    ],
    "LT Panel": [
      "Main LT Panel",
      "AMF Panel",
      "PCC Panel",
      "MCC Panel"
    ],
    "Earthing": [
      "Earth Pit",
      "Chemical Earthing",
      "GI Earthing"
    ],
    "Service": [
      "Lift AMC",
      "DG AMC",
      "Electrical Service",
      "Other Service"
    ],
    "Other": [
      "Other Product"
    ]
  },
  "products": {
    "Passenger Lift": [
      {
        "id": "LIFT001",
        "name": "G+2 Automatic Passenger Lift",
        "price": 450000.0,
        "type": "Lift",
        "category": "Passenger Lift",
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
          "Cabin Finish": "SS"
        }
      }
    ]
  }
}

---

## 3. Calculate Bill (Live Calculation Preview)

url : (http://192.168.1.59:8000/api/cash-bills/calculate)
method : POST

params :- 

items:[{"id":"LIFT001","name":"G+2 Automatic Passenger Lift","price":450000.0,"qty":1},{"id":"EARTH001","name":"Chemical Earthing Earth Pit","price":12500.0,"qty":2}]
discount:0.0
amount_paid:500000.0

response :- 

{
  "subtotal": 475000.0,
  "discount": 0.0,
  "taxable_amount": 475000.0,
  "gst_rate": 0.18,
  "gst": 85500.0,
  "grand_total": 560500.0,
  "amount_paid": 500000.0,
  "change_returned": 0.0,
  "balance_amount": 60500.0,
  "payment_status": "Partially Paid"
}

---

## 4. Generate Cash Bill / Save Draft

url : (http://192.168.1.59:8000/api/cash-bills)
method : POST

params :- 

bill_no:CB-260912-0001
bill_date:12 Sep 2026
customer_type:Walk-in Customer
customer_name:Rohan Sharma
mobile:9876500001
items:[{"id":"LIFT001","name":"G+2 Automatic Passenger Lift","type":"Lift","category":"Passenger Lift","price":450000.0,"qty":1,"specifications":{"Capacity":"4-6 Passenger","Rated Load":"320 KG"}}]
discount:0.0
payment_mode:Cash
amount_paid:550000.0
notes:Delivered lift motor directly from counter
status:Generated

response :- 

{
  "message": "Cash bill 'CB-260912-0001' generated successfully",
  "bill": {
    "id": 1,
    "bill_no": "CB-260912-0001",
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
        "total": 450000.0,
        "specifications": {
          "Capacity": "4-6 Passenger",
          "Rated Load": "320 KG"
        }
      }
    ],
    "subtotal": 450000.0,
    "discount": 0.0,
    "taxable_amount": 450000.0,
    "gst_rate": 0.18,
    "gst_amount": 81000.0,
    "gst": 81000.0,
    "grand_total": 531000.0,
    "payment_mode": "Cash",
    "amount_paid": 550000.0,
    "change_returned": 19000.0,
    "balance_amount": 0.0,
    "payment_status": "Paid",
    "notes": "Delivered lift motor directly from counter",
    "status": "Generated",
    "created_at": "2026-09-12T10:39:23.374476",
    "updated_at": "2026-09-12T10:39:23.374481"
  }
}

---

## 5. List All Cash Bills

url : (http://192.168.1.59:8000/api/cash-bills)
method : GET

params :- 

(None)

response :- 

{
  "count": 1,
  "results": [
    {
      "id": 1,
      "bill_no": "CB-260912-0001",
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
          "total": 450000.0
        }
      ],
      "subtotal": 450000.0,
      "discount": 0.0,
      "taxable_amount": 450000.0,
      "gst_rate": 0.18,
      "gst_amount": 81000.0,
      "gst": 81000.0,
      "grand_total": 531000.0,
      "payment_mode": "Cash",
      "amount_paid": 550000.0,
      "change_returned": 19000.0,
      "balance_amount": 0.0,
      "payment_status": "Paid",
      "notes": "Delivered lift motor directly from counter",
      "status": "Generated",
      "created_at": "2026-09-12T10:39:23.374476",
      "updated_at": "2026-09-12T10:39:23.374481"
    }
  ]
}

---

## 6. Get Single Cash Bill Details

url : (http://192.168.1.59:8000/api/cash-bills/1)
method : GET

params :- 

(None)

response :- 

{
  "id": 1,
  "bill_no": "CB-260912-0001",
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
      "total": 450000.0,
      "specifications": {
        "Capacity": "4-6 Passenger",
        "Rated Load": "320 KG"
      }
    }
  ],
  "subtotal": 450000.0,
  "discount": 0.0,
  "taxable_amount": 450000.0,
  "gst_rate": 0.18,
  "gst_amount": 81000.0,
  "gst": 81000.0,
  "grand_total": 531000.0,
  "payment_mode": "Cash",
  "amount_paid": 550000.0,
  "change_returned": 19000.0,
  "balance_amount": 0.0,
  "payment_status": "Paid",
  "notes": "Delivered lift motor directly from counter",
  "status": "Generated",
  "created_at": "2026-09-12T10:39:23.374476",
  "updated_at": "2026-09-12T10:39:23.374481"
}

---

## 7. Update Cash Bill

url : (http://192.168.1.59:8000/api/cash-bills/1)
method : PUT

params :- 

notes:Updated: Receipt handed over to customer
customer_type:Existing Customer

response :- 

{
  "message": "Cash bill 'CB-260912-0001' updated successfully",
  "bill": {
    "id": 1,
    "bill_no": "CB-260912-0001",
    "customer_type": "Existing Customer",
    "customer_name": "Rohan Sharma",
    "notes": "Updated: Receipt handed over to customer",
    "updated_at": "2026-09-12T10:45:00.000000"
  }
}

---

## 8. Delete Cash Bill

url : (http://192.168.1.59:8000/api/cash-bills/1)
method : DELETE

params :- 

(None)

response :- 

{
  "message": "Cash bill 'CB-260912-0001' deleted successfully"
}
