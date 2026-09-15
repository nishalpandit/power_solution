# Purchase Order API Documentation

## 1. Get Next Auto-Generated PO Number

url : (http://192.168.1.59:8000/api/purchases/next-po-number)
method : GET

params :- 

(None)

response :- 

{
  "po_number": "PO-260914-0001"
}

---

## 2. Supplier Dropdown (Select Supplier)

url : (http://192.168.1.59:8000/api/purchases/suppliers)
method : GET

params :- 

(None)

response :- 

{
  "count": 3,
  "suppliers": [
    {
      "id": "SUP001",
      "supplier_id": 1,
      "supplier_code": "SUP001",
      "name": "ABC Electrical Pvt. Ltd.",
      "contact": "Rajesh Kumar",
      "mobile": "9876543210",
      "email": "sales@abcelectrical.com",
      "address": "Industrial Area, Ahmedabad, Gujarat"
    },
    {
      "id": "SUP002",
      "supplier_id": 2,
      "supplier_code": "SUP002",
      "name": "XYZ Power Systems",
      "contact": "Amit Sharma",
      "mobile": "9988776655",
      "email": "info@xyzpower.com",
      "address": "GIDC Estate, Vadodara, Gujarat"
    },
    {
      "id": "SUP003",
      "supplier_id": 3,
      "supplier_code": "SUP003",
      "name": "Power Equipment India",
      "contact": "Vikas Patel",
      "mobile": "9998887776",
      "email": "purchase@powerequipment.in",
      "address": "Industrial Estate, Surat, Gujarat"
    }
  ]
}

---

## 3. Create New Supplier (Add Supplier Screen)

url : (http://192.168.1.59:8000/api/purchases/suppliers)
method : POST

params :- 

name:Metro Electricals Ltd
supplier_code:SUP004
contact_person:Sunil Verma
mobile:9811223344
email:contact@metroelec.in
address:Sector 18, Noida, UP

response :- 

{
  "message": "Supplier 'Metro Electricals Ltd' created successfully",
  "supplier": {
    "id": "SUP004",
    "supplier_id": 4,
    "supplier_code": "SUP004",
    "name": "Metro Electricals Ltd",
    "contact": "Sunil Verma",
    "mobile": "9811223344",
    "email": "contact@metroelec.in",
    "address": "Sector 18, Noida, UP"
  }
}

---

## 4. Purchase Product Picker Master

url : (http://192.168.1.59:8000/api/purchases/product-picker)
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
        "sku": "LFT-001",
        "purchasePrice": 390000.0,
        "price": 390000.0,
        "unit": "Nos",
        "gst": 18.0,
        "type": "Lift",
        "category": "Passenger Lift",
        "specifications": {
          "Capacity": "6 Passenger",
          "Rated Load": "408 KG",
          "Speed": "1 m/s",
          "Floor": "G+2",
          "Stops": "3",
          "Door Type": "Automatic",
          "Drive": "VVVF / VFD",
          "Power Supply": "415V / 3 Phase / 50Hz",
          "Cabin Finish": "SS"
        }
      }
    ]
  }
}

---

## 5. Calculate Purchase Order (Live Calculations Preview)

url : (http://192.168.1.59:8000/api/purchases/calculate)
method : POST

params :- 

items:[{"id":"LIFT001","name":"G+2 Automatic Passenger Lift","price":390000.0,"qty":1,"gst":18.0},{"id":"EARTH001","name":"Chemical Earthing Earth Pit","price":8500.0,"qty":2,"gst":18.0}]

response :- 

{
  "subtotal": 407000.0,
  "gst_total": 73260.0,
  "grand_total": 480260.0
}

---

## 6. Place Purchase Order / Save as Draft

url : (http://192.168.1.59:8000/api/purchases)
method : POST

params :- 

po_number:PO-260914-0001
supplier_id:SUP001
po_date:17 May 2025
expected_delivery:24 May 2025
payment_terms:30 Days
status:Draft
reference:REF-PO-2025-01
items:[{"id":"LIFT001","name":"G+2 Automatic Passenger Lift","sku":"LFT-001","type":"Lift","category":"Passenger Lift","price":390000.0,"qty":1,"unit":"Nos","gst":18.0,"specifications":{"Capacity":"6 Passenger","Rated Load":"408 KG"}}]
notes:Ensure heavy duty wooden packing for lift motor.

response :- 

{
  "message": "Purchase order 'PO-260914-0001' created successfully",
  "purchase_order": {
    "id": 1,
    "po_number": "PO-260914-0001",
    "po_date": "17 May 2025",
    "expected_delivery": "24 May 2025",
    "po_status": "Draft",
    "status": "Draft",
    "payment_terms": "30 Days",
    "reference": "REF-PO-2025-01",
    "supplier_id": 1,
    "supplier_code": "SUP001",
    "supplier_name": "ABC Electrical Pvt. Ltd.",
    "contact_person": "Rajesh Kumar",
    "mobile": "9876543210",
    "email": "sales@abcelectrical.com",
    "address": "Industrial Area, Ahmedabad, Gujarat",
    "items": [
      {
        "id": "LIFT001",
        "name": "G+2 Automatic Passenger Lift",
        "sku": "LFT-001",
        "type": "Lift",
        "category": "Passenger Lift",
        "price": 390000.0,
        "qty": 1,
        "unit": "Nos",
        "gst": 18.0,
        "total": 460200.0,
        "specifications": {
          "Capacity": "6 Passenger",
          "Rated Load": "408 KG"
        }
      }
    ],
    "subtotal": 390000.0,
    "gst_total": 70200.0,
    "grand_total": 460200.0,
    "notes": "Ensure heavy duty wooden packing for lift motor.",
    "created_at": "2026-09-14T09:26:14.766490",
    "updated_at": "2026-09-14T09:26:14.766499"
  }
}

---

## 7. List All Purchase Orders

url : (http://192.168.1.59:8000/api/purchases)
method : GET

params :- 

(None)

response :- 

{
  "count": 1,
  "results": [
    {
      "id": 1,
      "po_number": "PO-260914-0001",
      "po_date": "17 May 2025",
      "expected_delivery": "24 May 2025",
      "po_status": "Draft",
      "status": "Draft",
      "payment_terms": "30 Days",
      "reference": "REF-PO-2025-01",
      "supplier_id": 1,
      "supplier_code": "SUP001",
      "supplier_name": "ABC Electrical Pvt. Ltd.",
      "contact_person": "Rajesh Kumar",
      "mobile": "9876543210",
      "email": "sales@abcelectrical.com",
      "address": "Industrial Area, Ahmedabad, Gujarat",
      "items": [
        {
          "id": "LIFT001",
          "name": "G+2 Automatic Passenger Lift",
          "sku": "LFT-001",
          "type": "Lift",
          "category": "Passenger Lift",
          "price": 390000.0,
          "qty": 1,
          "unit": "Nos",
          "gst": 18.0,
          "total": 460200.0
        }
      ],
      "subtotal": 390000.0,
      "gst_total": 70200.0,
      "grand_total": 460200.0,
      "notes": "Ensure heavy duty wooden packing for lift motor.",
      "created_at": "2026-09-14T09:26:14.766490",
      "updated_at": "2026-09-14T09:26:14.766499"
    }
  ]
}

---

## 8. Get Single Purchase Order Details

url : (http://192.168.1.59:8000/api/purchases/1)
method : GET

params :- 

(None)

response :- 

{
  "id": 1,
  "po_number": "PO-260914-0001",
  "po_date": "17 May 2025",
  "expected_delivery": "24 May 2025",
  "po_status": "Draft",
  "status": "Draft",
  "payment_terms": "30 Days",
  "reference": "REF-PO-2025-01",
  "supplier_id": 1,
  "supplier_code": "SUP001",
  "supplier_name": "ABC Electrical Pvt. Ltd.",
  "contact_person": "Rajesh Kumar",
  "mobile": "9876543210",
  "email": "sales@abcelectrical.com",
  "address": "Industrial Area, Ahmedabad, Gujarat",
  "items": [
    {
      "id": "LIFT001",
      "name": "G+2 Automatic Passenger Lift",
      "sku": "LFT-001",
      "type": "Lift",
      "category": "Passenger Lift",
      "price": 390000.0,
      "qty": 1,
      "unit": "Nos",
      "gst": 18.0,
      "total": 460200.0,
      "specifications": {
        "Capacity": "6 Passenger",
        "Rated Load": "408 KG"
      }
    }
  ],
  "subtotal": 390000.0,
  "gst_total": 70200.0,
  "grand_total": 460200.0,
  "notes": "Ensure heavy duty wooden packing for lift motor.",
  "created_at": "2026-09-14T09:26:14.766490",
  "updated_at": "2026-09-14T09:26:14.766499"
}

---

## 9. Update Purchase Order

url : (http://192.168.1.59:8000/api/purchases/1)
method : PUT

params :- 

status:Ordered
notes:Updated: Vendor confirmed delivery date for 24 May

response :- 

{
  "message": "Purchase order 'PO-260914-0001' updated successfully",
  "purchase_order": {
    "id": 1,
    "po_number": "PO-260914-0001",
    "po_status": "Ordered",
    "status": "Ordered",
    "notes": "Updated: Vendor confirmed delivery date for 24 May",
    "updated_at": "2026-09-14T09:30:00.000000"
  }
}

---

## 10. Delete Purchase Order

url : (http://192.168.1.59:8000/api/purchases/1)
method : DELETE

params :- 

(None)

response :- 

{
  "message": "Purchase order 'PO-260914-0001' deleted successfully"
}
