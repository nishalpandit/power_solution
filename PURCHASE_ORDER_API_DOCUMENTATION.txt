# Purchase Order and Supplier API Documentation

Base URL: http://192.168.1.54:8000/api

---

## 1. Create Purchase Order Screen Data

Loads auto-generated PO number, dates, payment terms, status options, suppliers list, and product picker master in one request.

url : (http://192.168.1.54:8000/api/purchases/create-data)
method : GET

headers :-

Content-Type: application/json

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
      "city": null,
      "state": null,
      "pincode": null,
      "gstin": "24AAACP1234F1Z1",
      "pan_number": null,
      "payment_terms": "30 Days",
      "remarks": null,
      "notes": null
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
      "city": null,
      "state": null,
      "pincode": null,
      "gstin": "24AAACB5678K1Z2",
      "pan_number": null,
      "payment_terms": "30 Days",
      "remarks": null,
      "notes": null
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
      "city": null,
      "state": null,
      "pincode": null,
      "gstin": "24AAACP9012M1Z3",
      "pan_number": null,
      "payment_terms": "30 Days",
      "remarks": null,
      "notes": null
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
      "city": "Ahmedabad",
      "state": "Gujarat",
      "pincode": "382330",
      "gstin": "24AABCO9988C1Z4",
      "pan_number": "AABCO9988C",
      "payment_terms": "30 Days",
      "remarks": "Authorized OEM supplier for heavy duty lift components and traction motors",
      "notes": "Authorized OEM supplier for heavy duty lift components and traction motors"
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

## 2. Add New Supplier

url : (http://192.168.1.54:8000/api/purchases/suppliers)
method : POST

headers :-

Content-Type: application/json (or multipart/form-data)

params :-

supplier_name : string (Required)
contact_person : string (Optional)
mobile : string (Optional)
email : string (Optional)
address : string (Optional)
city : string (Optional)
state : string (Optional)
pincode : string (Optional)
payment_terms : string (Optional, default: 30 Days)
gstin : string (Optional)
pan_number : string (Optional)
remarks : string (Optional)
supplier_code : string (Optional, auto-generated if omitted)

body (JSON) :-

{
  "supplier_name": "Omkar Elevators & Switchgears",
  "contact_person": "Suresh Mehta",
  "mobile": "9822114455",
  "email": "suresh@omkarelevators.in",
  "address": "Plot 42, Phase II, GIDC Naroda, Ahmedabad",
  "city": "Ahmedabad",
  "state": "Gujarat",
  "pincode": "382330",
  "payment_terms": "30 Days",
  "gstin": "24AABCO9988C1Z4",
  "pan_number": "AABCO9988C",
  "remarks": "Authorized OEM supplier for heavy duty lift components and traction motors"
}

body (Multipart Form Data) :-

supplier_name: Omkar Elevators & Switchgears
contact_person: Suresh Mehta
mobile: 9822114455
email: suresh@omkarelevators.in
address: Plot 42, Phase II, GIDC Naroda, Ahmedabad
city: Ahmedabad
state: Gujarat
pincode: 382330
payment_terms: 30 Days
gstin: 24AABCO9988C1Z4
pan_number: AABCO9988C
remarks: Authorized OEM supplier for heavy duty lift components and traction motors

response :-

{
  "message": "Supplier 'Omkar Elevators & Switchgears' updated successfully",
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
    "city": "Ahmedabad",
    "state": "Gujarat",
    "pincode": "382330",
    "gstin": "24AABCO9988C1Z4",
    "pan_number": "AABCO9988C",
    "payment_terms": "30 Days",
    "remarks": "Authorized OEM supplier for heavy duty lift components and traction motors",
    "notes": "Authorized OEM supplier for heavy duty lift components and traction motors"
  }
}

---

## 3. Supplier List

url : (http://192.168.1.54:8000/api/purchases/suppliers)
method : GET

params :-

search : string (Optional)

response :-

{
  "count": 20,
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
      "city": null,
      "state": null,
      "pincode": null,
      "gstin": "24AAACP1234F1Z1",
      "pan_number": null,
      "payment_terms": "30 Days",
      "remarks": null,
      "notes": null
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
      "city": null,
      "state": null,
      "pincode": null,
      "gstin": "24AAACB5678K1Z2",
      "pan_number": null,
      "payment_terms": "30 Days",
      "remarks": null,
      "notes": null
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
      "city": null,
      "state": null,
      "pincode": null,
      "gstin": "24AAACP9012M1Z3",
      "pan_number": null,
      "payment_terms": "30 Days",
      "remarks": null,
      "notes": null
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
      "city": "Ahmedabad",
      "state": "Gujarat",
      "pincode": "382330",
      "gstin": "24AABCO9988C1Z4",
      "pan_number": "AABCO9988C",
      "payment_terms": "30 Days",
      "remarks": "Authorized OEM supplier for heavy duty lift components and traction motors",
      "notes": "Authorized OEM supplier for heavy duty lift components and traction motors"
    }
  ]
}

---

## 4. Product Picker Master

url : (http://192.168.1.54:8000/api/purchases/product-picker)
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

## 5. Calculate Purchase Order

url : (http://192.168.1.54:8000/api/purchases/calculate)
method : POST

headers :-

Content-Type: application/json

params :-

items : array of objects (Required)
- id : string (Required)
- name : string (Required)
- price : float (Required)
- qty : integer (Required)
- gst : float (Optional, default: 18.0)
- unit : string (Optional, default: Nos)
- sku : string (Optional)
- type : string (Optional)
- category : string (Optional)

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

url : (http://192.168.1.54:8000/api/purchases)
method : POST

headers :-

Content-Type: application/json (or multipart/form-data)

params :-

supplier_name : string (Required)
items : array of objects (Required)
supplier_id : string or integer (Optional)
contact_person : string (Optional)
mobile : string (Optional)
email : string (Optional)
address : string (Optional)
po_number : string (Optional, auto-generated if omitted)
po_date : string (Optional, default: today)
expected_delivery : string (Optional, default: today + 7 days)
payment_terms : string (Optional, default: 30 Days)
status : string (Optional, default: Draft)
reference : string (Optional)
subtotal : float (Optional)
gst_total : float (Optional)
grand_total : float (Optional)
notes : string (Optional)

body (Save as Draft Example) :-

{
  "po_number": "PO-250517-0001",
  "supplier_id": "SUP001",
  "supplier_name": "ABC Electrical Pvt. Ltd.",
  "contact_person": "Rajesh Kumar",
  "mobile": "9876543210",
  "email": "sales@abcelectrical.com",
  "address": "Industrial Area, Ahmedabad, Gujarat",
  "payment_terms": "30 Days",
  "po_date": "17 May 2025",
  "expected_delivery": "24 May 2025",
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

body (Place Purchase Order Example) :-

{
  "po_number": "PO-250517-0002",
  "supplier_id": "SUP018",
  "supplier_name": "Omkar Elevators & Switchgears",
  "contact_person": "Suresh Mehta",
  "mobile": "9822114455",
  "email": "suresh@omkarelevators.in",
  "address": "Plot 42, Phase II, GIDC Naroda, Ahmedabad",
  "payment_terms": "30 Days",
  "po_date": "18 May 2025",
  "expected_delivery": "25 May 2025",
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

body (Multipart Form Data Example) :-

po_number: PO-250517-0002
supplier_id: SUP018
supplier_name: Omkar Elevators & Switchgears
contact_person: Suresh Mehta
mobile: 9822114455
email: suresh@omkarelevators.in
address: Plot 42, Phase II, GIDC Naroda, Ahmedabad
payment_terms: 30 Days
po_date: 18 May 2025
expected_delivery: 25 May 2025
status: Ordered
reference: REF-OCT-2025
items: [{"id":"LIFT001","name":"G+2 Automatic Passenger Lift","sku":"LFT-001","type":"Lift","category":"Passenger Lift","price":390000.0,"purchasePrice":390000.0,"qty":1,"unit":"Nos","gst":18.0,"total":460200.0}]
subtotal: 390000.0
gst_total: 70200.0
grand_total: 460200.0
notes: Urgent requirement for Site A

response :-

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
    "remarks": "Urgent requirement for Site A",
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
    "remarks": "Urgent requirement for Site A",
    "created_at": "2026-09-18T11:28:29.824349",
    "updated_at": "2026-09-18T11:28:29.824352"
  }
}

---

## 7. Get Purchase Order Details

url : (http://192.168.1.54:8000/api/purchases/PO-250517-0001)
method : GET

params :-

po_id : string or integer (In URL path)

response :-

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
  "remarks": "",
  "created_at": "2026-09-18T11:25:02.972451",
  "updated_at": "2026-09-18T11:25:02.972454"
}

---

## 8. List Purchase Orders

url : (http://192.168.1.54:8000/api/purchases)
method : GET

params :-

search : string (Optional)
po_status : string (Optional)
supplier_name : string (Optional)

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
      "notes": "Approved by GM",
      "remarks": "Approved by GM"
    }
  ]
}

---

## 9. Update Purchase Order

url : (http://192.168.1.54:8000/api/purchases/PO-250517-0002)
method : PUT

headers :-

Content-Type: application/json (or multipart/form-data)

params :-

po_id : string or integer (In URL path)
po_status : string (Optional)
expected_delivery : string (Optional)
payment_terms : string (Optional)
reference : string (Optional)
contact_person : string (Optional)
mobile : string (Optional)
email : string (Optional)
address : string (Optional)
notes : string (Optional)
items : array of objects (Optional)

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
    "notes": "Approved by GM",
    "remarks": "Approved by GM"
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
    "notes": "Approved by GM",
    "remarks": "Approved by GM"
  }
}

---

## 10. Delete Purchase Order

url : (http://192.168.1.54:8000/api/purchases/PO-250517-0002)
method : DELETE

params :-

po_id : string or integer (In URL path)

response :-

{
  "message": "Purchase order 'PO-250517-0002' deleted successfully"
}
