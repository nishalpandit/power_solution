# Quotation API Documentation

## 1. Create Quotation (Save Draft / Save & Send)

url : (http://192.168.1.59:8000/api/quotations)
method : POST

params :- 

quotation_no:QTN-250517-0001
quotation_date:17 May 2025
valid_till:31 May 2025
reference:REF-2025-05
customer_name:Skyline Enterprises
address:45 Industrial Area, Phase 2, New Delhi
phone:+91 9876543210
email:contact@skyline.com
items:[{"type":"Lift","category":"Passenger Lift","product":"LIFT001","product_name":"G+2 Automatic Passenger Lift","specifications":{"Capacity":"4-6 Passenger","Rated Load":"320 KG","Speed":"0.65 - 1 m/s","Floor":"G+2","Stops":"3","Door Type":"Automatic","Door Opening":"Center Opening","Drive":"VVVF / VFD","Power Supply":"415V / 3 Phase / 50Hz","Cabin Finish":"SS","Controller":"Microprocessor Based"},"quantity":1,"unit_price":450000.0,"total_price":450000.0}]
subtotal:450000.0
discount_value:25000.0
discount_type:Flat
discount_amount:25000.0
tax_type:GST 18%
tax_rate:0.18
taxable_amount:425000.0
tax_amount:76500.0
grand_total:501500.0
terms:1. 50% advance along with purchase order.\n2. Delivery within 4-6 weeks.\n3. 1 year warranty.
status:Sent

response :- 

{
  "message": "Quotation 'QTN-250517-0001' saved successfully",
  "quotation": {
    "id": 1,
    "quotation_no": "QTN-250517-0001",
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
      }
    ],
    "subtotal": 450000.0,
    "discount_type": "Flat",
    "discount_value": 25000.0,
    "discount_amount": 25000.0,
    "tax_type": "GST 18%",
    "tax_rate": 0.18,
    "taxable_amount": 425000.0,
    "tax_amount": 76500.0,
    "grand_total": 501500.0,
    "terms": "1. 50% advance along with purchase order.\n2. Delivery within 4-6 weeks.\n3. 1 year warranty.",
    "status": "Sent",
    "created_at": "2026-09-10T12:16:47.123456",
    "updated_at": "2026-09-10T12:16:47.123456"
  }
}

---

## 2. Get Next Quotation Number

url : (http://192.168.1.59:8000/api/quotations/next-number)
method : GET

params :- 

(None)

response :- 

{
  "quotation_no": "QTN-260910-0002"
}

---

## 3. List All Quotations

url : (http://192.168.1.59:8000/api/quotations)
method : GET

params :- 

status:Draft
search:Skyline

response :- 

{
  "count": 1,
  "results": [
    {
      "id": 1,
      "quotation_no": "QTN-250517-0001",
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
          "product": "LIFT001",
          "product_name": "G+2 Automatic Passenger Lift",
          "specifications": {
            "Capacity": "4-6 Passenger",
            "Rated Load": "320 KG"
          },
          "quantity": 1.0,
          "unit_price": 450000.0,
          "total_price": 450000.0
        }
      ],
      "subtotal": 450000.0,
      "discount_type": "Flat",
      "discount_value": 25000.0,
      "discount_amount": 25000.0,
      "tax_type": "GST 18%",
      "tax_rate": 0.18,
      "taxable_amount": 425000.0,
      "tax_amount": 76500.0,
      "grand_total": 501500.0,
      "terms": "1. 50% advance along with purchase order.",
      "status": "Sent",
      "created_at": "2026-09-10T12:16:47.123456",
      "updated_at": "2026-09-10T12:16:47.123456"
    }
  ]
}

---

## 4. Get Quotation by ID

url : (http://192.168.1.59:8000/api/quotations/1)
method : GET

params :- 

(None)

response :- 

{
  "id": 1,
  "quotation_no": "QTN-250517-0001",
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
    }
  ],
  "subtotal": 450000.0,
  "discount_type": "Flat",
  "discount_value": 25000.0,
  "discount_amount": 25000.0,
  "tax_type": "GST 18%",
  "tax_rate": 0.18,
  "taxable_amount": 425000.0,
  "tax_amount": 76500.0,
  "grand_total": 501500.0,
  "terms": "1. 50% advance along with purchase order.\n2. Delivery within 4-6 weeks.\n3. 1 year warranty.",
  "status": "Sent",
  "created_at": "2026-09-10T12:16:47.123456",
  "updated_at": "2026-09-10T12:16:47.123456"
}

---

## 5. Update Quotation

url : (http://192.168.1.59:8000/api/quotations/1)
method : PUT

params :- 

quotation_no:QTN-250517-0001
quotation_date:18 May 2025
valid_till:05 June 2025
reference:REF-2025-05-REV1
customer_name:Skyline Towers Pvt Ltd
address:45 Industrial Area, Phase 2, New Delhi
phone:+91 9876543210
email:contact@skylinetowers.com
items:[{"type":"Lift","category":"Passenger Lift","product":"LIFT001","product_name":"G+2 Automatic Passenger Lift","specifications":{"Capacity":"4-6 Passenger","Rated Load":"320 KG"},"quantity":1,"unit_price":450000.0,"total_price":450000.0}]
subtotal:450000.0
discount_value:30000.0
discount_type:Flat
discount_amount:30000.0
tax_type:GST 18%
tax_rate:0.18
taxable_amount:420000.0
tax_amount:75600.0
grand_total:495600.0
terms:Updated terms and delivery schedule.
status:Approved

response :- 

{
  "message": "Quotation 'QTN-250517-0001' updated successfully",
  "quotation": {
    "id": 1,
    "quotation_no": "QTN-250517-0001",
    "quotation_date": "18 May 2025",
    "valid_till": "05 June 2025",
    "reference": "REF-2025-05-REV1",
    "customer_name": "Skyline Towers Pvt Ltd",
    "address": "45 Industrial Area, Phase 2, New Delhi",
    "phone": "+91 9876543210",
    "email": "contact@skylinetowers.com",
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
        "quantity": 1.0,
        "unit_price": 450000.0,
        "total_price": 450000.0
      }
    ],
    "subtotal": 450000.0,
    "discount_type": "Flat",
    "discount_value": 30000.0,
    "discount_amount": 30000.0,
    "tax_type": "GST 18%",
    "tax_rate": 0.18,
    "taxable_amount": 420000.0,
    "tax_amount": 75600.0,
    "grand_total": 495600.0,
    "terms": "Updated terms and delivery schedule.",
    "status": "Approved",
    "created_at": "2026-09-10T12:16:47.123456",
    "updated_at": "2026-09-10T12:18:10.123456"
  }
}

---

## 6. Delete Quotation

url : (http://192.168.1.59:8000/api/quotations/1)
method : DELETE

params :- 

(None)

response :- 

{
  "message": "Quotation 'QTN-250517-0001' deleted successfully"
}

## 7. Get Product Full Details (by Category Type ID, Category Name ID, and Product ID)

url : (http://192.168.1.59:8000/api/quotation/add_product)
method : GET (or POST)

params :- 

category_type_id: 1
category_name_id: 4
product_id: 9

Predefined Category Types:
- 1 = Lift
- 2 = Generator
- 3 = Panel
- 4 = Earthing
- 5 = Service
- 6 = Other

response :- 

{
  "id": 9,
  "product_id": 9,
  "category_type_id": 1,
  "category_type": "lift",
  "category_name_id": 4,
  "category_id": 4,
  "category_name": "Passenger Lift",
  "product_name": "khfk",
  "product_code": "mhmf",
  "brand": "gkhc",
  "model_number": "8987987654",
  "description": "chlclluuc",
  "purchase_price": 450000.0,
  "selling_price": 500000.0,
  "discount": "5%",
  "gst_rate": "18%",
  "hsn_code": "84281011",
  "inventory_tracking": true,
  "stock": 2.0,
  "unit": "Set",
  "min_stock": 1.0,
  "warranty_period": "2 Years",
  "warranty_terms": "Standard comprehensive warranty",
  "payment_terms": "30% Advance, 70% on delivery",
  "product_image": "/uploads/products/lift.jpg",
  "status": "Active",
  "specifications": {
    "lift_type": "Passenger",
    "operation_type": "Automatic",
    "capacity": "8 Passenger",
    "rated_load": "544 KG",
    "speed": "1.0 m/s",
    "floor_designation": "G+4",
    "number_of_floors": "5",
    "number_of_stops": "5",
    "landing_entrances": "5",
    "car_entrances": "1",
    "car_openings": "1",
    "shaft_structure": "Concrete",
    "shaft_net_size": "1800 x 1800 mm",
    "shaft_height": "18000 mm",
    "floor_height": "3000 mm",
    "pit_depth": "1500 mm",
    "overhead_height": "4200 mm",
    "car_dimensions": "1100 x 1400 mm",
    "cabin_size": "1100 x 1400 x 2200 mm",
    "machine_type": "Gearless PMSM",
    "machine_model": "GL-800",
    "drive_system": "VVVF",
    "motor_brand": "Monarch",
    "controller_brand": "Monarch Nice 3000+",
    "control_panel_type": "Integrated Microprocessor",
    "power_supply": "415 V AC, 3 Phase",
    "voltage": "415 V",
    "phase": "3 Phase",
    "frequency": "50 Hz",
    "brake_type": "Electromagnetic Disc Brake",
    "car_finishing": "Hairline SS",
    "cabin_finish": "Titanium Gold / SS Mirror",
    "false_ceiling": "LED Downlight Panel",
    "flooring_type": "Granite Finish PVC",
    "car_door_type": "Center Opening",
    "car_door_finish": "Hairline Stainless Steel",
    "landing_door_finish": "SS Hairline on Ground Floor",
    "door_opening": "800 x 2000 mm",
    "door_sill": "Hard Extruded Aluminium",
    "landing_door_lock": "Electromechanical Interlock",
    "safety_features": [
      "Over Speed Protection",
      "Infra-Red Light Curtain",
      "Automatic Rescue Device (ARD)"
    ]
  },
  "created_at": "2026-09-10T06:27:51.798573",
  "updated_at": "2026-09-10T06:27:51.798585"
}

---

## 4. Payment APIs (Add Payment / Invoices)

For the Flutter **AddPaymentScreen** where customer details come from quotations and invoices are auto-generated:
👉 Refer to **[PAYMENT_API_DOCUMENTATION.md](file:///c:/Users/PC/Desktop/power_solution/PAYMENT_API_DOCUMENTATION.md)**.



