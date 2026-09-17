# Create Invoice API Documentation

## 1. Initialize Screen Data (Single API on Screen Load)

url : (http://192.168.1.59:8000/api/invoices/create-data)
method : GET

params :- 

(None)

response :- 

{
  "invoice_no": "INV-260912-0001",
  "invoice_date": "12 Sep 2026",
  "due_date": "12 Oct 2026",
  "payment_terms": "30 Days",
  "payment_terms_options": [
    "Due on Receipt",
    "15 Days",
    "30 Days",
    "45 Days",
    "60 Days",
    "90 Days"
  ],
  "default_tax_percent": 18.0,
  "tax_rates": [0, 5, 12, 18, 28],
  "orders": [
    {
      "id": 1,
      "order_id": 1,
      "order_no": "ORD-260912-0001",
      "quotation_id": 1,
      "quotation_no": "QTN-250517-0001",
      "order_date": "12 Sep 2026",
      "customer_name": "Skyline Enterprises",
      "phone": "+91 9876543210",
      "email": "contact@skyline.com",
      "billing_address": "45 Industrial Area, Phase 2, New Delhi",
      "delivery_address": "45 Industrial Area, Phase 2, New Delhi",
      "items": [
        {
          "id": "LIFT001",
          "name": "G+2 Automatic Passenger Lift",
          "code": "LIFT001",
          "category": "Passenger Lift",
          "qty": 1,
          "rate": 450000.0,
          "discount": 25000.0,
          "tax": 18.0,
          "tax_percent": 18.0,
          "total": 450000.0,
          "specifications": {
            "Capacity": "4-6 Passenger",
            "Speed": "1 m/s"
          }
        }
      ],
      "subtotal": 450000.0,
      "discount": 25000.0,
      "tax": 76500.0,
      "grand_total": 501500.0,
      "payment_terms": "30 Days",
      "status": "Pending"
    }
  ],
  "customers": [
    {
      "customer_name": "Skyline Enterprises",
      "phone": "+91 9876543210",
      "email": "contact@skyline.com",
      "billing_address": "45 Industrial Area, Phase 2, New Delhi",
      "delivery_address": "45 Industrial Area, Phase 2, New Delhi",
      "latest_order_id": 1,
      "latest_order_no": "ORD-260912-0001",
      "orders_count": 1
    }
  ]
}

---

## 2. Create / Add Invoice (Create Invoice Screen)

url : (http://192.168.1.59:8000/api/invoices/create)
method : POST

(Also supports http://192.168.1.59:8000/api/invoices and http://192.168.1.59:8000/api/invoices/add)

params :- 

customer_name:Skyline Enterprises
phone:+91 9876543210
email:contact@skyline.com
billing_address:45 Industrial Area, Phase 2, New Delhi
invoice_no:INV-260912-0001
invoice_date:12 Sep 2026
order_no:ORD-260912-0001
payment_terms:30 Days
due_date:12 Oct 2026
reference_no:REF-INV-001
items:[{"name":"G+2 Automatic Passenger Lift","code":"LIFT001","category":"Passenger Lift","qty":1,"rate":450000.0,"discount":25000.0,"tax_percent":18.0,"total":450000.0}]
subtotal:450000.0
discount:25000.0
tax:76500.0
grand_total:501500.0
notes:
status:Unpaid

response :- 

{
  "message": "Invoice 'INV-260912-0001' created successfully",
  "invoice": {
    "id": 1,
    "invoice_no": "INV-260912-0001",
    "invoice_date": "12 Sep 2026",
    "due_date": "12 Oct 2026",
    "order_id": 1,
    "order_no": "ORD-260912-0001",
    "quotation_id": 1,
    "quotation_no": "QTN-250517-0001",
    "customer_name": "Skyline Enterprises",
    "phone": "+91 9876543210",
    "email": "contact@skyline.com",
    "billing_address": "45 Industrial Area, Phase 2, New Delhi",
    "delivery_address": "45 Industrial Area, Phase 2, New Delhi",
    "customer": {
      "name": "Skyline Enterprises",
      "phone": "+91 9876543210",
      "email": "contact@skyline.com",
      "billing_address": "45 Industrial Area, Phase 2, New Delhi",
      "delivery_address": "45 Industrial Area, Phase 2, New Delhi"
    },
    "payment_terms": "30 Days",
    "reference_no": "REF-INV-001",
    "items": [
      {
        "id": "ITEM001",
        "name": "G+2 Automatic Passenger Lift",
        "code": "LIFT001",
        "category": "Passenger Lift",
        "qty": 1.0,
        "rate": 450000.0,
        "discount": 25000.0,
        "tax_percent": 18.0,
        "tax": 76500.0,
        "total": 450000.0,
        "specifications": {}
      }
    ],
    "subtotal": 450000.0,
    "discount": 25000.0,
    "tax_percent": 18.0,
    "tax": 76500.0,
    "grand_total": 501500.0,
    "amount_paid": 0.0,
    "balance_due": 501500.0,
    "notes": "",
    "status": "Unpaid",
    "created_at": "2026-09-17T10:27:10.851043",
    "updated_at": "2026-09-17T10:27:10.851049"
  }
}

---

## 3. Next Auto-Generated Invoice Number

url : (http://192.168.1.59:8000/api/invoices/next-invoice-number)
method : GET

params :- 

(None)

response :- 

{
  "invoice_no": "INV-260912-0001"
}

---

## 4. Order Dropdown (Select Order No. to Auto-Fill Details & Items)

url : (http://192.168.1.59:8000/api/invoices/orders)
method : GET

params :- 

(None)

response :- 

{
  "count": 1,
  "results": [
    {
      "id": 1,
      "order_id": 1,
      "order_no": "ORD-260912-0001",
      "quotation_id": 1,
      "quotation_no": "QTN-250517-0001",
      "order_date": "12 Sep 2026",
      "customer_name": "Skyline Enterprises",
      "phone": "+91 9876543210",
      "email": "contact@skyline.com",
      "billing_address": "45 Industrial Area, Phase 2, New Delhi",
      "delivery_address": "45 Industrial Area, Phase 2, New Delhi",
      "items": [
        {
          "id": "LIFT001",
          "name": "G+2 Automatic Passenger Lift",
          "code": "LIFT001",
          "category": "Passenger Lift",
          "qty": 1,
          "rate": 450000.0,
          "discount": 25000.0,
          "tax": 18.0,
          "tax_percent": 18.0,
          "total": 450000.0
        }
      ],
      "subtotal": 450000.0,
      "discount": 25000.0,
      "tax": 76500.0,
      "grand_total": 501500.0,
      "payment_terms": "30 Days",
      "status": "Pending"
    }
  ]
}

---

## 5. Customer Dropdown (For Select Customer Button)

url : (http://192.168.1.59:8000/api/invoices/customers)
method : GET

params :- 

(None)

response :- 

{
  "count": 1,
  "results": [
    {
      "customer_name": "Skyline Enterprises",
      "phone": "+91 9876543210",
      "email": "contact@skyline.com",
      "billing_address": "45 Industrial Area, Phase 2, New Delhi",
      "delivery_address": "45 Industrial Area, Phase 2, New Delhi",
      "latest_order_id": 1,
      "latest_order_no": "ORD-260912-0001",
      "orders_count": 1
    }
  ]
}
