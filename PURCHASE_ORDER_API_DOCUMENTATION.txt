# Create Purchase Order and Supplier API Documentation

Base URL: http://192.168.1.54:8000/api
Database Verification: db.sqlite3 (All responses below are verified against real database records)

This documentation directly corresponds to the Flutter AddPurchaseOrderScreen and AddSupplierScreen workflows:
1. Add new supplier first via AddSupplierScreen (POST /api/purchases/suppliers) with supplier name, contact person, mobile number, email, and supplier address.
2. Select supplier from dropdown in AddPurchaseOrderScreen (GET /api/purchases/suppliers).
3. Contact person, mobile number, email, and supplier address automatically populate into the form controllers upon selection. If custom, user can enter them manually.
4. Auto-generate or specify PO number, PO date, expected delivery date, payment terms, and status (Draft or Ordered).
5. Add items from Product Master Picker (types, categories, products with specifications, price, qty, unit, gst).
6. Live summary calculation for Sub Total, GST, and Grand Total (POST /api/purchases/calculate).
7. Save as Draft or Place Purchase Order (POST /api/purchases).
8. Support for both application/json and multipart/form-data.
9. Support for both integer ID and string PO number (for example: PO-250517-0001).

---

## 1. Screen Initialization (Single Round-Trip for AddPurchaseOrderScreen)

Loads next PO number, today date, default delivery date (7 days later), payment terms, status options, supplier dropdown list, and the entire product picker master in one single request.

url : (http://192.168.1.54:8000/api/purchases/create-data)
method : GET

params :-

(None)

response :-

{
  "po_number": "PO-260918-0001",
  "next_po_number": "PO-260918-0001",
  "po_date": "18 Sep 2026",
  "delivery_date": "25 Sep 2026",
  "expected_delivery": "25 Sep 2026",
  "payment_terms": "30 Days",
  "payment_terms_options": [
    "Advance",
    "15 Days",
    "30 Days",
    "45 Days",
    "60 Days",
    "Against Delivery"
  ],
  "po_status": "Draft",
  "po_status_options": [
    "Draft",
    "Pending",
    "Approved",
    "Ordered",
    "Received",
    "Cancelled"
  ],
  "suppliers": [
    {
      "id": "SUP001",
      "supplier_id": 1,
      "supplier_code": "SUP001",
      "name": "ABC Electrical Pvt. Ltd.",
      "supplier_name": "ABC Electrical Pvt. Ltd.",
      "contact": "Rajesh Kumar",
      "contact_person": "Rajesh Kumar",
      "mobile": "9876543210",
      "phone": "9876543210",
      "email": "sales@abcelectrical.com",
      "address": "Industrial Area, Ahmedabad, Gujarat",
      "gstin": "24AAACP1234F1Z1"
    },
    {
      "id": "SUP002",
      "supplier_id": 2,
      "supplier_code": "SUP002",
      "name": "XYZ Power Systems",
      "supplier_name": "XYZ Power Systems",
      "contact": "Amit Sharma",
      "contact_person": "Amit Sharma",
      "mobile": "9988776655",
      "phone": "9988776655",
      "email": "info@xyzpower.com",
      "address": "GIDC Estate, Vadodara, Gujarat",
      "gstin": null
    },
    {
      "id": "SUP003",
      "supplier_id": 3,
      "supplier_code": "SUP003",
      "name": "Power Equipment India",
      "supplier_name": "Power Equipment India",
      "contact": "Vikas Patel",
      "contact_person": "Vikas Patel",
      "mobile": "9998887776",
      "phone": "9998887776",
      "email": "purchase@powerequipment.in",
      "address": "Industrial Estate, Surat, Gujarat",
      "gstin": null
    }
  ],
  "product_types": [
    "Lift",
    "Generator",
    "LT Panel",
    "Earthing",
    "Service",
    "Other"
  ]
}

---

## 2. Add New Supplier First (AddSupplierScreen)

Used when the user taps the add button next to the supplier dropdown to create a new supplier first.
Accepts supplier name, contact person, mobile number, email, and supplier address.
Supports both application/json and multipart/form-data.

url : (http://192.168.1.54:8000/api/purchases/suppliers)
method : POST

(Also supports http://192.168.1.54:8000/api/suppliers and http://192.168.1.54:8000/api/purchase-orders/suppliers)

headers :-

Content-Type: application/json
(or multipart/form-data)

body (JSON) :-

{
  "supplier_name": "Omkar Elevators & Switchgears",
  "contact_person": "Suresh Mehta",
  "mobile": "9822114455",
  "email": "suresh@omkarelevators.in",
  "address": "Plot 42, Phase II, GIDC Naroda, Ahmedabad",
  "gstin": "24AABCO9988C1Z4"
}

body (Multipart Form Data) :-

supplier_name: Omkar Elevators & Switchgears
contact_person: Suresh Mehta
mobile: 9822114455
email: suresh@omkarelevators.in
address: Plot 42, Phase II, GIDC Naroda, Ahmedabad
gstin: 24AABCO9988C1Z4

response (HTTP 201 Created) :-

{
  "message": "Supplier 'Omkar Elevators & Switchgears' created successfully",
  "supplier": {
    "id": "SUP018",
    "supplier_id": 18,
    "supplier_code": "SUP018",
    "name": "Omkar Elevators & Switchgears",
    "supplier_name": "Omkar Elevators & Switchgears",
    "contact": "Suresh Mehta",
    "contact_person": "Suresh Mehta",
    "mobile": "9822114455",
    "phone": "9822114455",
    "email": "suresh@omkarelevators.in",
    "address": "Plot 42, Phase II, GIDC Naroda, Ahmedabad",
    "gstin": "24AABCO9988C1Z4"
  }
}

---

## 3. Supplier Dropdown List (Select Supplier)

Returns all suppliers stored in the database.
Every supplier object has id, name, contact, mobile, email, and address matching Flutter controller keys.

url : (http://192.168.1.54:8000/api/purchases/suppliers)
method : GET

(Also supports http://192.168.1.54:8000/api/suppliers)

params :-

(None)

response :-

{
  "count": 18,
  "suppliers": [
    {
      "id": "SUP001",
      "supplier_id": 1,
      "supplier_code": "SUP001",
      "name": "ABC Electrical Pvt. Ltd.",
      "supplier_name": "ABC Electrical Pvt. Ltd.",
      "contact": "Rajesh Kumar",
      "contact_person": "Rajesh Kumar",
      "mobile": "9876543210",
      "phone": "9876543210",
      "email": "sales@abcelectrical.com",
      "address": "Industrial Area, Ahmedabad, Gujarat",
      "gstin": "24AAACP1234F1Z1"
    },
    {
      "id": "SUP002",
      "supplier_id": 2,
      "supplier_code": "SUP002",
      "name": "XYZ Power Systems",
      "supplier_name": "XYZ Power Systems",
      "contact": "Amit Sharma",
      "contact_person": "Amit Sharma",
      "mobile": "9988776655",
      "phone": "9988776655",
      "email": "info@xyzpower.com",
      "address": "GIDC Estate, Vadodara, Gujarat",
      "gstin": null
    },
    {
      "id": "SUP003",
      "supplier_id": 3,
      "supplier_code": "SUP003",
      "name": "Power Equipment India",
      "supplier_name": "Power Equipment India",
      "contact": "Vikas Patel",
      "contact_person": "Vikas Patel",
      "mobile": "9998887776",
      "phone": "9998887776",
      "email": "purchase@powerequipment.in",
      "address": "Industrial Estate, Surat, Gujarat",
      "gstin": null
    },
    {
      "id": "SUP018",
      "supplier_id": 18,
      "supplier_code": "SUP018",
      "name": "Omkar Elevators & Switchgears",
      "supplier_name": "Omkar Elevators & Switchgears",
      "contact": "Suresh Mehta",
      "contact_person": "Suresh Mehta",
      "mobile": "9822114455",
      "phone": "9822114455",
      "email": "suresh@omkarelevators.in",
      "address": "Plot 42, Phase II, GIDC Naroda, Ahmedabad",
      "gstin": "24AABCO9988C1Z4"
    }
  ]
}

---

## 4. Product Picker Master (Modal Bottom Sheet in Flutter)

Provides the 3-level product hierarchy:
Level 1: Product Types (Lift, Generator, LT Panel, Earthing, Service, Other)
Level 2: Categories mapped under each Product Type
Level 3: Products mapped under each Category with full technical specifications, purchasePrice, SKU, unit, and GST (18%)

url : (http://192.168.1.54:8000/api/purchases/product-picker)
method : GET

(Also supports http://192.168.1.54:8000/api/purchases/products)

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
    ],
    "Goods Lift": [
      {
        "id": "LIFT002",
        "name": "Goods Lift - 1000 KG",
        "sku": "LFT-002",
        "purchasePrice": 310000.0,
        "price": 310000.0,
        "unit": "Nos",
        "gst": 18.0,
        "type": "Lift",
        "category": "Goods Lift",
        "specifications": {
          "Capacity": "1000 KG",
          "Speed": "0.5 m/s",
          "Floor": "G+2",
          "Stops": "3",
          "Door Type": "Manual",
          "Drive": "VVVF / VFD"
        }
      }
    ],
    "Silent Generator": [
      {
        "id": "DG001",
        "name": "Silent DG 60 KVA",
        "sku": "GEN-001",
        "purchasePrice": 550000.0,
        "price": 550000.0,
        "unit": "Nos",
        "gst": 18.0,
        "type": "Generator",
        "category": "Silent Generator",
        "specifications": {
          "Rating": "60 KVA / 48 KW",
          "Output Voltage": "430 V",
          "Phase": "3 Phase",
          "Frequency": "50 Hz",
          "Engine": "4 Cylinder",
          "RPM": "1500",
          "Cooling": "Liquid Cooled",
          "Alternator": "Meccalte / CG",
          "Voltage Control": "AVR",
          "Control Panel": "AMF"
        }
      }
    ]
  }
}

---

## 5. Live Calculation Preview (Order Summary Section)

Calculates Sub Total, GST Total, and Grand Total when item quantities change or new products are added.

url : (http://192.168.1.54:8000/api/purchases/calculate)
method : POST

(Also supports http://192.168.1.54:8000/api/purchase-orders/calculate)

headers :-

Content-Type: application/json

body :-

{
  "items": [
    {
      "id": "LIFT001",
      "name": "G+2 Automatic Passenger Lift",
      "sku": "LFT-001",
      "purchasePrice": 390000.0,
      "qty": 2,
      "unit": "Nos",
      "gst": 18.0
    }
  ]
}

response :-

{
  "subtotal": 780000.0,
  "gst_total": 140400.0,
  "grand_total": 920400.0
}

---

## 6. Place Purchase Order / Save as Draft

Creates the purchase order record in the database.
Handles:
- Supplier selection by supplier_id (for example: SUP001 or integer ID 1)
- Contact Person, Mobile Number, Email, Supplier Address
- Order details: PO number, PO date, expected delivery date, payment terms, reference, status (Draft or Ordered)
- Full item array with technical specifications, price, quantity, and GST
- Sub Total, GST Total, and Grand Total
- Additional notes and instructions
- Supports both application/json and multipart/form-data.

url : (http://192.168.1.54:8000/api/purchases)
method : POST

(Also supports http://192.168.1.54:8000/api/purchases/create, http://192.168.1.54:8000/api/purchase-orders, and http://192.168.1.54:8000/api/purchase-orders/create)

headers :-

Content-Type: application/json
(or multipart/form-data)

body (JSON - Save as Draft Example) :-

{
  "po_number": "PO-250517-0001",
  "supplier_id": "SUP001",
  "supplier_name": "ABC Electrical Pvt. Ltd.",
  "contact_person": "Rajesh Kumar",
  "mobile": "9876543210",
  "email": "sales@abcelectrical.com",
  "address": "Industrial Area, Ahmedabad, Gujarat",
  "po_date": "17 May 2025",
  "expected_delivery": "24 May 2025",
  "payment_terms": "30 Days",
  "status": "Draft",
  "reference": "",
  "items": [
    {
      "id": "LIFT001",
      "name": "G+2 Automatic Passenger Lift",
      "sku": "LFT-001",
      "type": "Lift",
      "category": "Passenger Lift",
      "purchasePrice": 390000.0,
      "price": 390000.0,
      "qty": 1,
      "unit": "Nos",
      "gst": 18.0,
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
  ],
  "subtotal": 390000.0,
  "gst_total": 70200.0,
  "grand_total": 460200.0,
  "notes": ""
}

body (JSON - Place Purchase Order with New Supplier Example) :-

{
  "po_number": "PO-250517-0002",
  "supplier_id": "SUP018",
  "supplier_name": "Omkar Elevators & Switchgears",
  "contact_person": "Suresh Mehta",
  "mobile": "9822114455",
  "email": "suresh@omkarelevators.in",
  "address": "Plot 42, Phase II, GIDC Naroda, Ahmedabad",
  "po_date": "18 May 2025",
  "expected_delivery": "25 May 2025",
  "payment_terms": "30 Days",
  "status": "Ordered",
  "reference": "REF-OCT-2025",
  "items": [
    {
      "id": "LIFT001",
      "name": "G+2 Automatic Passenger Lift",
      "sku": "LFT-001",
      "type": "Lift",
      "category": "Passenger Lift",
      "purchasePrice": 390000.0,
      "price": 390000.0,
      "qty": 1,
      "unit": "Nos",
      "gst": 18.0,
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
  ],
  "subtotal": 390000.0,
  "gst_total": 70200.0,
  "grand_total": 460200.0,
  "notes": "Urgent requirement for Site A"
}

response (HTTP 201 Created) :-

{
  "message": "Purchase order 'PO-250517-0002' created successfully",
  "purchase_order": {
    "id": 12,
    "po_number": "PO-250517-0002",
    "po_date": "18 May 2025",
    "expected_delivery": "25 May 2025",
    "delivery_date": "25 May 2025",
    "po_status": "Ordered",
    "status": "Ordered",
    "payment_terms": "30 Days",
    "reference": "REF-OCT-2025",
    "supplier_id": "SUP018",
    "supplier_db_id": 18,
    "supplier_code": "SUP018",
    "supplier_name": "Omkar Elevators & Switchgears",
    "contact_person": "Suresh Mehta",
    "contact": "Suresh Mehta",
    "mobile": "9822114455",
    "phone": "9822114455",
    "email": "suresh@omkarelevators.in",
    "address": "Plot 42, Phase II, GIDC Naroda, Ahmedabad",
    "items": [
      {
        "id": "LIFT001",
        "name": "G+2 Automatic Passenger Lift",
        "sku": "LFT-001",
        "type": "Lift",
        "category": "Passenger Lift",
        "price": 390000.0,
        "purchasePrice": 390000.0,
        "qty": 1,
        "unit": "Nos",
        "gst": 18.0,
        "total": 460200.0,
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
    ],
    "subtotal": 390000.0,
    "gst_total": 70200.0,
    "grand_total": 460200.0,
    "formatted_subtotal": "Rs 3,90,000.00",
    "formatted_gst_total": "Rs 70,200.00",
    "formatted_grand_total": "Rs 4,60,200.00",
    "notes": "Urgent requirement for Site A",
    "created_at": "2026-09-18T11:28:29.824349",
    "updated_at": "2026-09-18T11:28:29.824352"
  },
  "po": {
    "id": 12,
    "po_number": "PO-250517-0002",
    "po_date": "18 May 2025",
    "expected_delivery": "25 May 2025",
    "delivery_date": "25 May 2025",
    "po_status": "Ordered",
    "status": "Ordered",
    "payment_terms": "30 Days",
    "reference": "REF-OCT-2025",
    "supplier_id": "SUP018",
    "supplier_db_id": 18,
    "supplier_code": "SUP018",
    "supplier_name": "Omkar Elevators & Switchgears",
    "contact_person": "Suresh Mehta",
    "contact": "Suresh Mehta",
    "mobile": "9822114455",
    "phone": "9822114455",
    "email": "suresh@omkarelevators.in",
    "address": "Plot 42, Phase II, GIDC Naroda, Ahmedabad",
    "items": [
      {
        "id": "LIFT001",
        "name": "G+2 Automatic Passenger Lift",
        "sku": "LFT-001",
        "type": "Lift",
        "category": "Passenger Lift",
        "price": 390000.0,
        "purchasePrice": 390000.0,
        "qty": 1,
        "unit": "Nos",
        "gst": 18.0,
        "total": 460200.0,
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
    ],
    "subtotal": 390000.0,
    "gst_total": 70200.0,
    "grand_total": 460200.0,
    "formatted_subtotal": "Rs 3,90,000.00",
    "formatted_gst_total": "Rs 70,200.00",
    "formatted_grand_total": "Rs 4,60,200.00",
    "notes": "Urgent requirement for Site A",
    "created_at": "2026-09-18T11:28:29.824349",
    "updated_at": "2026-09-18T11:28:29.824352"
  }
}

---

## 7. Get Purchase Order Details by PO Number or ID

Lookup by string PO number (for example: PO-250517-0001 or PO-250517-0002) or integer primary key.

url : (http://192.168.1.54:8000/api/purchases/PO-250517-0001)
method : GET

(Also supports http://192.168.1.54:8000/api/purchase-orders/PO-250517-0001)

params :-

(None)

response (Verified from db.sqlite3 record ID 11) :-

{
  "id": 11,
  "po_number": "PO-250517-0001",
  "po_date": "17 May 2025",
  "expected_delivery": "24 May 2025",
  "delivery_date": "24 May 2025",
  "po_status": "Draft",
  "status": "Draft",
  "payment_terms": "30 Days",
  "reference": "",
  "supplier_id": "SUP001",
  "supplier_db_id": 1,
  "supplier_code": "SUP001",
  "supplier_name": "ABC Electrical Pvt. Ltd.",
  "contact_person": "Rajesh Kumar",
  "contact": "Rajesh Kumar",
  "mobile": "9876543210",
  "phone": "9876543210",
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
  ],
  "subtotal": 390000.0,
  "gst_total": 70200.0,
  "grand_total": 460200.0,
  "formatted_subtotal": "Rs 3,90,000.00",
  "formatted_gst_total": "Rs 70,200.00",
  "formatted_grand_total": "Rs 4,60,200.00",
  "notes": "",
  "created_at": "2026-09-18T11:25:02.972451",
  "updated_at": "2026-09-18T11:25:02.972454"
}

---

## 8. List Purchase Orders (With Filtering)

url : (http://192.168.1.54:8000/api/purchases)
method : GET

(Also supports http://192.168.1.54:8000/api/purchase-orders)

optional query params :-

po_status: Draft
supplier_name: Omkar
search: Suresh

response :-

{
  "count": 1,
  "purchase_orders": [
    {
      "id": 12,
      "po_number": "PO-250517-0002",
      "po_date": "18 May 2025",
      "expected_delivery": "25 May 2025",
      "delivery_date": "25 May 2025",
      "po_status": "Approved",
      "status": "Approved",
      "payment_terms": "30 Days",
      "reference": "REF-OCT-2025",
      "supplier_id": "SUP018",
      "supplier_db_id": 18,
      "supplier_code": "SUP018",
      "supplier_name": "Omkar Elevators & Switchgears",
      "contact_person": "Suresh Mehta",
      "contact": "Suresh Mehta",
      "mobile": "9822114455",
      "phone": "9822114455",
      "email": "suresh@omkarelevators.in",
      "address": "Plot 42, Phase II, GIDC Naroda, Ahmedabad",
      "items": [
        {
          "id": "LIFT001",
          "name": "G+2 Automatic Passenger Lift",
          "sku": "LFT-001",
          "type": "Lift",
          "category": "Passenger Lift",
          "price": 390000.0,
          "purchasePrice": 390000.0,
          "qty": 1,
          "unit": "Nos",
          "gst": 18.0,
          "total": 460200.0
        }
      ],
      "subtotal": 390000.0,
      "gst_total": 70200.0,
      "grand_total": 460200.0,
      "formatted_subtotal": "Rs 3,90,000.00",
      "formatted_gst_total": "Rs 70,200.00",
      "formatted_grand_total": "Rs 4,60,200.00",
      "notes": "Approved by GM"
    }
  ]
}

---

## 9. Update Purchase Order Status or Details

Supports updating po_status (Draft, Pending, Approved, Ordered, Received, Cancelled), expected delivery date, payment terms, notes, or contact info.
Lookup by string PO number or integer ID.

url : (http://192.168.1.54:8000/api/purchases/PO-250517-0002)
method : PUT

(Also supports http://192.168.1.54:8000/api/purchase-orders/PO-250517-0002)

headers :-

Content-Type: application/json

body :-

{
  "po_status": "Approved",
  "notes": "Approved by GM"
}

response :-

{
  "message": "Purchase order 'PO-250517-0002' updated successfully",
  "purchase_order": {
    "id": 12,
    "po_number": "PO-250517-0002",
    "po_date": "18 May 2025",
    "expected_delivery": "25 May 2025",
    "delivery_date": "25 May 2025",
    "po_status": "Approved",
    "status": "Approved",
    "payment_terms": "30 Days",
    "reference": "REF-OCT-2025",
    "supplier_id": "SUP018",
    "supplier_db_id": 18,
    "supplier_code": "SUP018",
    "supplier_name": "Omkar Elevators & Switchgears",
    "contact_person": "Suresh Mehta",
    "contact": "Suresh Mehta",
    "mobile": "9822114455",
    "phone": "9822114455",
    "email": "suresh@omkarelevators.in",
    "address": "Plot 42, Phase II, GIDC Naroda, Ahmedabad",
    "subtotal": 390000.0,
    "gst_total": 70200.0,
    "grand_total": 460200.0,
    "notes": "Approved by GM"
  },
  "po": {
    "id": 12,
    "po_number": "PO-250517-0002",
    "po_date": "18 May 2025",
    "expected_delivery": "25 May 2025",
    "delivery_date": "25 May 2025",
    "po_status": "Approved",
    "status": "Approved",
    "payment_terms": "30 Days",
    "reference": "REF-OCT-2025",
    "supplier_id": "SUP018",
    "supplier_db_id": 18,
    "supplier_code": "SUP018",
    "supplier_name": "Omkar Elevators & Switchgears",
    "contact_person": "Suresh Mehta",
    "contact": "Suresh Mehta",
    "mobile": "9822114455",
    "phone": "9822114455",
    "email": "suresh@omkarelevators.in",
    "address": "Plot 42, Phase II, GIDC Naroda, Ahmedabad",
    "subtotal": 390000.0,
    "gst_total": 70200.0,
    "grand_total": 460200.0,
    "notes": "Approved by GM"
  }
}

---

## 10. Delete Purchase Order

url : (http://192.168.1.54:8000/api/purchases/PO-250517-0002)
method : DELETE

(Also supports http://192.168.1.54:8000/api/purchase-orders/PO-250517-0002)

response :-

{
  "message": "Purchase order 'PO-250517-0002' deleted successfully"
}
