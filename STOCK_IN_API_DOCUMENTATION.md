# Stock In & Category Inventory API Documentation

## 1. Get Next Auto-Generated Stock Receipt Number & Date

url : (http://192.168.1.59:8000/api/stock-in/next-receipt-number)
method : GET

params :- 

(None)

response :- 

{
  "receipt_no": "STK-IN-260915-0001",
  "receipt_date": "15 Sep 2026"
}



## 2. Supplier Dropdown (Select Supplier)

url : (http://192.168.1.59:8000/api/stock-in/suppliers)
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
      "name": "Perfect Generators Pvt. Ltd.",
      "contact": "9876543210",
      "contact_person": "Rajesh Sharma",
      "mobile": "9876543210",
      "email": "sales@perfectgenerators.com",
      "address": "Industrial Area, Ahmedabad, Gujarat"
    },
    {
      "id": "SUP002",
      "supplier_id": 2,
      "supplier_code": "SUP002",
      "name": "ABC Electrical Pvt. Ltd.",
      "contact": "9988776655",
      "contact_person": "Amit Patel",
      "mobile": "9988776655",
      "email": "sales@abcelectrical.com",
      "address": "GIDC Estate, Vadodara, Gujarat"
    },
    {
      "id": "SUP003",
      "supplier_id": 3,
      "supplier_code": "SUP003",
      "name": "Power Equipment India",
      "contact": "9998887776",
      "contact_person": "Vikas Patel",
      "mobile": "9998887776",
      "email": "purchase@powerequipment.in",
      "address": "Industrial Estate, Surat, Gujarat"
    }
  ]
}

---

## 3. Create / Quick Add Supplier

url : (http://192.168.1.59:8000/api/stock-in/suppliers)
method : POST

params :- 

name:Reliable Power Systems Ltd
contact:9123456780
mobile:9123456780
email:info@reliablepower.com
address:GIDC Naroda, Ahmedabad

response :- 

{
  "message": "Supplier 'Reliable Power Systems Ltd' saved successfully",
  "supplier": {
    "id": "SUP004",
    "supplier_id": 4,
    "supplier_code": "SUP004",
    "name": "Reliable Power Systems Ltd",
    "contact": "9123456780",
    "mobile": "9123456780",
    "email": "info@reliablepower.com",
    "address": "GIDC Naroda, Ahmedabad"
  }
}

---

## 4. Stock for Every Category Type (Category Stock Summary)

url : (http://192.168.1.59:8000/api/stock-in/category-stock)
method : GET

params :- 

(None)

response :- 

{
  "category_types": [
    "Lift",
    "Generator",
    "LT Panel",
    "Earthing",
    "Service",
    "Other"
  ],
  "stocks_by_category_type": {
    "Lift": {
      "category_type": "Lift",
      "total_stock": 10.0,
      "total_products": 4,
      "total_valuation": 3540000.0,
      "categories": [
        {
          "category_name": "Passenger Lift",
          "product_count": 1,
          "total_stock": 4.0,
          "total_valuation": 1560000.0,
          "unit": "Nos",
          "products": [
            {
              "id": "LIFT001",
              "name": "G+2 Automatic Passenger Lift",
              "sku": "LFT-001",
              "stock": 4.0,
              "unit": "Nos",
              "purchase_price": 390000.0,
              "stock_valuation": 1560000.0,
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
        },
        {
          "category_name": "Goods Lift",
          "product_count": 1,
          "total_stock": 2.0,
          "total_valuation": 620000.0,
          "unit": "Nos",
          "products": [
            {
              "id": "LIFT002",
              "name": "Goods Lift - 1000 KG",
              "sku": "LFT-002",
              "stock": 2.0,
              "unit": "Nos",
              "purchase_price": 310000.0,
              "stock_valuation": 620000.0,
              "specifications": {
                "Capacity": "1000 KG",
                "Speed": "0.5 m/s",
                "Floor": "G+2",
                "Stops": "3",
                "Door Type": "Manual",
                "Drive": "VVVF / VFD"
              }
            }
          ]
        },
        {
          "category_name": "Hospital Lift",
          "product_count": 1,
          "total_stock": 1.0,
          "total_valuation": 520000.0,
          "unit": "Nos",
          "products": [
            {
              "id": "LIFT003",
              "name": "Hospital Bed Lift 15P",
              "sku": "LFT-003",
              "stock": 1.0,
              "unit": "Nos",
              "purchase_price": 520000.0,
              "stock_valuation": 520000.0,
              "specifications": {
                "Capacity": "15 Passenger / Bed",
                "Speed": "1.0 m/s",
                "Door Type": "Automatic Telescopic"
              }
            }
          ]
        },
        {
          "category_name": "Home Lift",
          "product_count": 1,
          "total_stock": 3.0,
          "total_valuation": 840000.0,
          "unit": "Nos",
          "products": [
            {
              "id": "LIFT004",
              "name": "Hydraulic Home Lift 4P",
              "sku": "LFT-004",
              "stock": 3.0,
              "unit": "Nos",
              "purchase_price": 280000.0,
              "stock_valuation": 840000.0,
              "specifications": {
                "Capacity": "4 Passenger / 300 KG",
                "Drive": "Hydraulic",
                "Power": "Single Phase / 3 Phase"
              }
            }
          ]
        }
      ]
    },
    "Generator": {
      "category_type": "Generator",
      "total_stock": 10.0,
      "total_products": 3,
      "total_valuation": 3050000.0,
      "categories": [
        {
          "category_name": "Silent Generator",
          "product_count": 2,
          "total_stock": 8.0,
          "total_valuation": 2700000.0,
          "unit": "Nos",
          "products": [
            {
              "id": "GEN001",
              "name": "DG Set - 25 KVA",
              "sku": "GEN-001",
              "stock": 5.0,
              "unit": "Nos",
              "purchase_price": 210000.0,
              "stock_valuation": 1050000.0,
              "specifications": {
                "Rating": "25 KVA",
                "Output Voltage": "430 V",
                "Phase": "3 Phase",
                "Frequency": "50 Hz",
                "RPM": "1500",
                "Cooling": "Liquid Cooled",
                "Voltage Control": "AVR",
                "Control Panel": "AMF"
              }
            },
            {
              "id": "GEN002",
              "name": "DG Set - 60 KVA",
              "sku": "GEN-002",
              "stock": 3.0,
              "unit": "Nos",
              "purchase_price": 550000.0,
              "stock_valuation": 1650000.0,
              "specifications": {
                "Rating": "60 KVA / 48 KW",
                "Output Voltage": "430 V",
                "Phase": "3 Phase",
                "Frequency": "50 Hz",
                "RPM": "1500",
                "Cooling": "Liquid Cooled",
                "Alternator": "Meccalte / CG",
                "Voltage Control": "AVR",
                "Control Panel": "AMF"
              }
            }
          ]
        },
        {
          "category_name": "Open Generator",
          "product_count": 1,
          "total_stock": 2.0,
          "total_valuation": 350000.0,
          "unit": "Nos",
          "products": [
            {
              "id": "GEN003",
              "name": "Open Skid DG Set 30 KVA",
              "sku": "GEN-003",
              "stock": 2.0,
              "unit": "Nos",
              "purchase_price": 175000.0,
              "stock_valuation": 350000.0,
              "specifications": {
                "Rating": "30 KVA",
                "Type": "Open Skid",
                "Cooling": "Water Cooled"
              }
            }
          ]
        }
      ]
    },
    "LT Panel": {
      "category_type": "LT Panel",
      "total_stock": 15.0,
      "total_products": 4,
      "total_valuation": 1905000.0,
      "categories": [
        {
          "category_name": "Main LT Panel",
          "product_count": 1,
          "total_stock": 6.0,
          "total_valuation": 810000.0,
          "unit": "Nos",
          "products": [
            {
              "id": "PNL001",
              "name": "Main LT Panel",
              "sku": "PNL-001",
              "stock": 6.0,
              "unit": "Nos",
              "purchase_price": 135000.0,
              "stock_valuation": 810000.0,
              "specifications": {
                "Panel Type": "Main LT Panel",
                "Construction": "Floor Mounted",
                "Sheet Thickness": "2.0 MM",
                "Busbar": "Copper",
                "Busbar Insulator": "FRP / SMC",
                "Earth Busbar": "Copper",
                "Cable Entry": "Bottom",
                "Gland Plate": "3 MM",
                "Painting": "Powder Coated"
              }
            }
          ]
        },
        {
          "category_name": "AMF Panel",
          "product_count": 1,
          "total_stock": 4.0,
          "total_valuation": 340000.0,
          "unit": "Nos",
          "products": [
            {
              "id": "PNL002",
              "name": "DG AMF Control Panel",
              "sku": "PNL-002",
              "stock": 4.0,
              "unit": "Nos",
              "purchase_price": 85000.0,
              "stock_valuation": 340000.0,
              "specifications": {
                "Panel Type": "AMF Panel",
                "Application": "DG Auto Start/Stop",
                "Sheet Thickness": "2.0 MM",
                "Cable Entry": "Bottom",
                "Painting": "Powder Coated"
              }
            }
          ]
        },
        {
          "category_name": "PCC Panel",
          "product_count": 1,
          "total_stock": 2.0,
          "total_valuation": 320000.0,
          "unit": "Nos",
          "products": [
            {
              "id": "PNL003",
              "name": "Power Control Centre (PCC) Panel",
              "sku": "PNL-003",
              "stock": 2.0,
              "unit": "Nos",
              "purchase_price": 160000.0,
              "stock_valuation": 320000.0,
              "specifications": {
                "Panel Type": "PCC Panel",
                "Current Rating": "800A",
                "Busbar": "Electrolytic Copper"
              }
            }
          ]
        },
        {
          "category_name": "MCC Panel",
          "product_count": 1,
          "total_stock": 3.0,
          "total_valuation": 435000.0,
          "unit": "Nos",
          "products": [
            {
              "id": "PNL004",
              "name": "Motor Control Centre (MCC) Panel",
              "sku": "PNL-004",
              "stock": 3.0,
              "unit": "Nos",
              "purchase_price": 145000.0,
              "stock_valuation": 435000.0,
              "specifications": {
                "Panel Type": "MCC Panel",
                "Starters": "DOL / Star-Delta",
                "Compartment": "Form 4b"
              }
            }
          ]
        }
      ]
    },
    "Earthing": {
      "category_type": "Earthing",
      "total_stock": 95.0,
      "total_products": 3,
      "total_valuation": 607500.0,
      "categories": [
        {
          "category_name": "Earth Pit",
          "product_count": 1,
          "total_stock": 25.0,
          "total_valuation": 212500.0,
          "unit": "Set",
          "products": [
            {
              "id": "EARTH001",
              "name": "Chemical Earthing Earth Pit",
              "sku": "EAR-001",
              "stock": 25.0,
              "unit": "Set",
              "purchase_price": 8500.0,
              "stock_valuation": 212500.0,
              "specifications": {
                "Earthing Type": "Chemical Earthing",
                "Electrode": "GI / Copper",
                "Earth Pit": "Maintenance Free",
                "Back Fill Compound": "Chemical Compound"
              }
            }
          ]
        },
        {
          "category_name": "Chemical Earthing",
          "product_count": 1,
          "total_stock": 40.0,
          "total_valuation": 260000.0,
          "unit": "Set",
          "products": [
            {
              "id": "EARTH002",
              "name": "Maintenance Free Chemical Earthing",
              "sku": "EAR-002",
              "stock": 40.0,
              "unit": "Set",
              "purchase_price": 6500.0,
              "stock_valuation": 260000.0,
              "specifications": {
                "Earthing Type": "Chemical Earthing",
                "Electrode": "Copper",
                "Maintenance": "Maintenance Free"
              }
            }
          ]
        },
        {
          "category_name": "GI Earthing",
          "product_count": 1,
          "total_stock": 30.0,
          "total_valuation": 135000.0,
          "unit": "Set",
          "products": [
            {
              "id": "EARTH003",
              "name": "GI Pipe & Strip Earthing Set",
              "sku": "EAR-003",
              "stock": 30.0,
              "unit": "Set",
              "purchase_price": 4500.0,
              "stock_valuation": 135000.0,
              "specifications": {
                "Earthing Type": "GI Earthing",
                "Electrode": "Hot Dip GI Pipe",
                "Plate": "600x600x6 MM"
              }
            }
          ]
        }
      ]
    },
    "Service": {
      "category_type": "Service",
      "total_stock": 50.0,
      "total_products": 4,
      "total_valuation": 274000.0,
      "categories": [
        {
          "category_name": "Lift AMC",
          "product_count": 1,
          "total_stock": 10.0,
          "total_valuation": 50000.0,
          "unit": "Year",
          "products": [
            {
              "id": "AMC001",
              "name": "Passenger Lift AMC - 1 Year",
              "sku": "AMC-LFT-001",
              "stock": 10.0,
              "unit": "Year",
              "purchase_price": 5000.0,
              "stock_valuation": 50000.0,
              "specifications": {
                "Service Type": "Lift AMC",
                "Period": "1 Year",
                "Coverage": "Preventive Maintenance"
              }
            }
          ]
        },
        {
          "category_name": "DG AMC",
          "product_count": 1,
          "total_stock": 12.0,
          "total_valuation": 96000.0,
          "unit": "Year",
          "products": [
            {
              "id": "AMC002",
              "name": "DG AMC - 1 Year",
              "sku": "AMC-DG-001",
              "stock": 12.0,
              "unit": "Year",
              "purchase_price": 8000.0,
              "stock_valuation": 96000.0,
              "specifications": {
                "Service Type": "DG AMC",
                "Period": "1 Year",
                "Coverage": "Preventive Maintenance"
              }
            }
          ]
        },
        {
          "category_name": "Electrical Service",
          "product_count": 1,
          "total_stock": 20.0,
          "total_valuation": 80000.0,
          "unit": "Job",
          "products": [
            {
              "id": "SRV001",
              "name": "Electrical Maintenance Service",
              "sku": "SRV-001",
              "stock": 20.0,
              "unit": "Job",
              "purchase_price": 4000.0,
              "stock_valuation": 80000.0,
              "specifications": {
                "Service Type": "Electrical Service",
                "Coverage": "Inspection & Maintenance"
              }
            }
          ]
        },
        {
          "category_name": "Other Service",
          "product_count": 1,
          "total_stock": 8.0,
          "total_valuation": 48000.0,
          "unit": "Job",
          "products": [
            {
              "id": "SRV002",
              "name": "Panel Testing & Calibration Service",
              "sku": "SRV-002",
              "stock": 8.0,
              "unit": "Job",
              "purchase_price": 6000.0,
              "stock_valuation": 48000.0,
              "specifications": {
                "Service Type": "Testing & Calibration"
              }
            }
          ]
        }
      ]
    },
    "Other": {
      "category_type": "Other",
      "total_stock": 15.0,
      "total_products": 1,
      "total_valuation": 150000.0,
      "categories": [
        {
          "category_name": "Other Product",
          "product_count": 1,
          "total_stock": 15.0,
          "total_valuation": 150000.0,
          "unit": "Nos",
          "products": [
            {
              "id": "OTHER001",
              "name": "Other Electrical Product",
              "sku": "OTH-001",
              "stock": 15.0,
              "unit": "Nos",
              "purchase_price": 10000.0,
              "stock_valuation": 150000.0,
              "specifications": {
                "Product Type": "Other"
              }
            }
          ]
        }
      ]
    }
  },
  "overall_total_stock": 195.0,
  "overall_total_valuation": 9526500.0
}

---

## 5. Product Picker Master (Categories & Products)

url : (http://192.168.1.59:8000/api/stock-in/product-picker)
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
        "unit": "Nos",
        "purchasePrice": 390000.0,
        "price": 390000.0,
        "gst": 18.0,
        "stock": 4.0,
        "current_stock": 4.0,
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
  },
  "stock_by_category_type": {
    "Lift": {
      "category_type": "Lift",
      "total_stock": 10.0,
      "total_valuation": 3540000.0,
      "product_count": 4
    }
  }
}

---

## 6. Calculate Stock In (Live Calculations Preview)

url : (http://192.168.1.59:8000/api/stock-in/calculate)
method : POST

params :- 

quantity:2
rate:390000.0
discount:10000.0
gst:18.0

response :- 

{
  "quantity": 2.0,
  "rate": 390000.0,
  "discount": 10000.0,
  "gross_amount": 780000.0,
  "taxable_amount": 770000.0,
  "gst_rate": 18.0,
  "gst_amount": 138600.0,
  "total_amount": 908600.0
}

---

## 7. Save Stock In (Create Receipt & Increment Stock)

url : (http://192.168.1.59:8000/api/stock-in)
method : POST

params :- 

receipt_no:STK-IN-260915-0001
receipt_date:15 Sep 2026
po_number:PO-260914-0001
invoice_no:INV-2026-0042
invoice_date:15 Sep 2026
supplier_id:SUP001
supplier_name:Perfect Generators Pvt. Ltd.
supplier_contact:9876543210
product_type:Lift
category:Passenger Lift
product:G+2 Automatic Passenger Lift
product_sku:LFT-001
quantity:2
unit:Nos
warehouse:Lift Warehouse
rack:Rack L-01
batch_no:BAT-2026-09
serial_no:LFT-SN-99881
rate:390000.0
discount:0.0
gst:18.0
received_by:Rajesh Sharma
condition:Good
inspection_status:Passed
inspection_remarks:Passed all physical and load tests.
notes:Delivered with factory guarantee certificates.
specifications:{"Capacity":"6 Passenger","Rated Load":"408 KG","Speed":"1 m/s","Floor":"G+2","Stops":"3","Door Type":"Automatic","Drive":"VVVF / VFD","Power Supply":"415V / 3 Phase / 50Hz","Cabin Finish":"SS"}

response :- 

{
  "message": "Stock In 'STK-IN-260915-0001' saved successfully. Inventory updated (+2.0 Nos).",
  "current_product_stock": 6.0,
  "stock_in": {
    "id": 1,
    "receipt_no": "STK-IN-260915-0001",
    "receipt_date": "15 Sep 2026",
    "po_number": "PO-260914-0001",
    "invoice_no": "INV-2026-0042",
    "invoice_date": "15 Sep 2026",
    "supplier_id": 1,
    "supplier_code": "SUP001",
    "supplier_name": "Perfect Generators Pvt. Ltd.",
    "supplier_contact": "9876543210",
    "product_id": 1,
    "product_sku": "LFT-001",
    "product_type": "Lift",
    "category": "Passenger Lift",
    "product_name": "G+2 Automatic Passenger Lift",
    "product": "G+2 Automatic Passenger Lift",
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
    },
    "quantity": 2.0,
    "unit": "Nos",
    "warehouse": "Lift Warehouse",
    "rack": "Rack L-01",
    "batch_no": "BAT-2026-09",
    "serial_no": "LFT-SN-99881",
    "rate": 390000.0,
    "discount": 0.0,
    "gst": 18.0,
    "gross_amount": 780000.0,
    "taxable_amount": 780000.0,
    "gst_amount": 140400.0,
    "total_amount": 920400.0,
    "received_by": "Rajesh Sharma",
    "condition": "Good",
    "inspection_status": "Passed",
    "inspection_remarks": "Passed all physical and load tests.",
    "notes": "Delivered with factory guarantee certificates.",
    "status": "Received",
    "created_at": "2026-09-15T12:00:00.000000",
    "updated_at": "2026-09-15T12:00:00.000000"
  }
}

---

## 8. Stock In Dropdown Choices / Metadata

url : (http://192.168.1.59:8000/api/stock-in/meta)
method : GET

params :- 

(None)

response :- 

{
  "warehouses": [
    "Main Warehouse",
    "Lift Warehouse",
    "DG Warehouse",
    "Panel Warehouse",
    "Service Store"
  ],
  "units": [
    "Nos",
    "Set",
    "Unit",
    "Kg",
    "Meter",
    "Feet",
    "Year",
    "Job"
  ],
  "conditions": [
    "Good",
    "Damaged",
    "Partial Damage",
    "Under Inspection"
  ],
  "inspection_statuses": [
    "Pending",
    "Passed",
    "Failed",
    "Not Required"
  ],
  "gst_rates": [
    0,
    5,
    12,
    18,
    28
  ]
}

---

## 9. List Stock In Receipts (with Search & Filters)

url : (http://192.168.1.59:8000/api/stock-in)
method : GET

params :- 

search:Lift
warehouse:Lift Warehouse
product_type:Lift
category:Passenger Lift
condition:Good
inspection_status:Passed

response :- 

{
  "count": 1,
  "receipts": [
    {
      "id": 1,
      "receipt_no": "STK-IN-260915-0001",
      "receipt_date": "15 Sep 2026",
      "supplier_name": "Perfect Generators Pvt. Ltd.",
      "product_name": "G+2 Automatic Passenger Lift",
      "quantity": 2.0,
      "unit": "Nos",
      "warehouse": "Lift Warehouse",
      "total_amount": 920400.0,
      "status": "Received"
    }
  ]
}

---

## 10. Single Stock In Detail

url : (http://192.168.1.59:8000/api/stock-in/1)
method : GET

params :- 

(None)

response :- 

{
  "id": 1,
  "receipt_no": "STK-IN-260915-0001",
  "receipt_date": "15 Sep 2026",
  "po_number": "PO-260914-0001",
  "invoice_no": "INV-2026-0042",
  "invoice_date": "15 Sep 2026",
  "supplier_id": 1,
  "supplier_code": "SUP001",
  "supplier_name": "Perfect Generators Pvt. Ltd.",
  "supplier_contact": "9876543210",
  "product_id": 1,
  "product_sku": "LFT-001",
  "product_type": "Lift",
  "category": "Passenger Lift",
  "product_name": "G+2 Automatic Passenger Lift",
  "product": "G+2 Automatic Passenger Lift",
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
  },
  "quantity": 2.0,
  "unit": "Nos",
  "warehouse": "Lift Warehouse",
  "rack": "Rack L-01",
  "batch_no": "BAT-2026-09",
  "serial_no": "LFT-SN-99881",
  "rate": 390000.0,
  "discount": 0.0,
  "gst": 18.0,
  "gross_amount": 780000.0,
  "taxable_amount": 780000.0,
  "gst_amount": 140400.0,
  "total_amount": 920400.0,
  "received_by": "Rajesh Sharma",
  "condition": "Good",
  "inspection_status": "Passed",
  "inspection_remarks": "Passed all physical and load tests.",
  "notes": "Delivered with factory guarantee certificates.",
  "status": "Received",
  "created_at": "2026-09-15T12:00:00.000000",
  "updated_at": "2026-09-15T12:00:00.000000"
}

---

## 11. Update Stock In Record

url : (http://192.168.1.59:8000/api/stock-in/1)
method : PUT

params :- 

quantity:3
rack:Rack L-02
inspection_status:Passed
notes:Verified third unit added

response :- 

{
  "message": "Stock In 'STK-IN-260915-0001' updated successfully",
  "stock_in": {
    "id": 1,
    "receipt_no": "STK-IN-260915-0001",
    "quantity": 3.0,
    "rack": "Rack L-02",
    "total_amount": 1380600.0
  }
}

---

## 12. Delete Stock In Record

url : (http://192.168.1.59:8000/api/stock-in/1)
method : DELETE

params :- 

(None)

response :- 

{
  "message": "Stock In 'STK-IN-260915-0001' deleted successfully. Reverted 3.0 units from inventory."
}
