# Payment API Documentation

## 1. Get Next Auto-Generated Invoice / Order Number

url : (http://192.168.1.59:8000/api/payments/next-invoice-number)
method : GET

params :- 

(None)

response :- 

{
  "invoice_no": "INV-260911-0001",
  "order_no": "INV-260911-0001"
}

---

## 2. Customer Dropdown (From Quotation)

url : (http://192.168.1.59:8000/api/payments/customers)
method : GET

params :- 

(None)

response :- 

{
  "count": 2,
  "results": [
    {
      "customer_name": "Skyline Enterprises",
      "phone": "+91 9876543210",
      "email": "contact@skyline.com",
      "address": "45 Industrial Area, Phase 2, New Delhi",
      "latest_quotation_id": 1,
      "latest_quotation_no": "QTN-250517-0001",
      "quotations": [
        {
          "id": 1,
          "quotation_no": "QTN-250517-0001",
          "quotation_date": "17 May 2025",
          "grand_total": 501500.0,
          "status": "Sent"
        }
      ]
    }
  ]
}

---

## 3. Create / Add Payment

url : (http://192.168.1.59:8000/api/payments/add)
method : POST

*(Also supports `http://192.168.1.59:8000/api/payment/add` and `http://192.168.1.59:8000/api/payments`)*

params :- 

invoice_no:INV-260911-0001
customer_name:Skyline Enterprises
quotation_id:1
quotation_no:QTN-250517-0001
customer_phone:+91 9876543210
customer_email:contact@skyline.com
customer_address:45 Industrial Area, Phase 2, New Delhi
payment_date:11 Sep 2026
amount_received:150000.0
payment_mode:Online
transaction_no:TXN-UPI-98234123
reference_no:REF-PAY-001
notes:30% advance payment received via PhonePe UPI
status:Received
payment_proof:upload (File: JPG, PNG, PDF)

response :- 

{
  "message": "Payment 'INV-260911-0001' saved successfully",
  "payment": {
    "id": 1,
    "invoice_no": "INV-260911-0001",
    "order_no": "INV-260911-0001",
    "customer_name": "Skyline Enterprises",
    "customer_phone": "+91 9876543210",
    "customer_email": "contact@skyline.com",
    "customer_address": "45 Industrial Area, Phase 2, New Delhi",
    "quotation_id": 1,
    "quotation_no": "QTN-250517-0001",
    "payment_date": "11 Sep 2026",
    "amount_received": 150000.0,
    "payment_mode": "Online",
    "transaction_no": "TXN-UPI-98234123",
    "reference_no": "REF-PAY-001",
    "notes": "30% advance payment received via PhonePe UPI",
    "payment_proof": "/uploads/payments/3f6a2b8e91cd4a229a4309cde87612f0.png",
    "status": "Received",
    "created_at": "2026-09-11T12:35:10.123456",
    "updated_at": "2026-09-11T12:35:10.123456"
  }
}

---

## 4. List All Payments

url : (http://192.168.1.59:8000/api/payments)
method : GET

params :- 

(None)

response :- 

{
  "count": 1,
  "results": [
    {
      "id": 1,
      "invoice_no": "INV-260911-0001",
      "order_no": "INV-260911-0001",
      "customer_name": "Skyline Enterprises",
      "customer_phone": "+91 9876543210",
      "customer_email": "contact@skyline.com",
      "customer_address": "45 Industrial Area, Phase 2, New Delhi",
      "quotation_id": 1,
      "quotation_no": "QTN-250517-0001",
      "payment_date": "11 Sep 2026",
      "amount_received": 150000.0,
      "payment_mode": "Online",
      "transaction_no": "TXN-UPI-98234123",
      "reference_no": "REF-PAY-001",
      "notes": "30% advance payment received via PhonePe UPI",
      "payment_proof": "/uploads/payments/3f6a2b8e91cd4a229a4309cde87612f0.png",
      "status": "Received",
      "created_at": "2026-09-11T12:35:10.123456",
      "updated_at": "2026-09-11T12:35:10.123456"
    }
  ]
}

---

## 5. Get Single Payment Details

url : (http://192.168.1.59:8000/api/payments/1)
method : GET

params :- 

(None)

response :- 

{
  "id": 1,
  "invoice_no": "INV-260911-0001",
  "order_no": "INV-260911-0001",
  "customer_name": "Skyline Enterprises",
  "customer_phone": "+91 9876543210",
  "customer_email": "contact@skyline.com",
  "customer_address": "45 Industrial Area, Phase 2, New Delhi",
  "quotation_id": 1,
  "quotation_no": "QTN-250517-0001",
  "payment_date": "11 Sep 2026",
  "amount_received": 150000.0,
  "payment_mode": "Online",
  "transaction_no": "TXN-UPI-98234123",
  "reference_no": "REF-PAY-001",
  "notes": "30% advance payment received via PhonePe UPI",
  "payment_proof": "/uploads/payments/3f6a2b8e91cd4a229a4309cde87612f0.png",
  "status": "Received",
  "created_at": "2026-09-11T12:35:10.123456",
  "updated_at": "2026-09-11T12:35:10.123456"
}

---

## 6. Update Payment Record

url : (http://192.168.1.59:8000/api/payments/1)
method : PUT

params :- 

status:Received
transaction_no:CHQ-882194
notes:Cheque cleared on 12 Sep 2026

response :- 

{
  "message": "Payment 'INV-260911-0001' updated successfully",
  "payment": {
    "id": 1,
    "invoice_no": "INV-260911-0001",
    "order_no": "INV-260911-0001",
    "customer_name": "Skyline Enterprises",
    "customer_phone": "+91 9876543210",
    "customer_email": "contact@skyline.com",
    "customer_address": "45 Industrial Area, Phase 2, New Delhi",
    "quotation_id": 1,
    "quotation_no": "QTN-250517-0001",
    "payment_date": "11 Sep 2026",
    "amount_received": 150000.0,
    "payment_mode": "Cheque",
    "transaction_no": "CHQ-882194",
    "reference_no": "REF-PAY-001",
    "notes": "Cheque cleared on 12 Sep 2026",
    "payment_proof": "/uploads/payments/3f6a2b8e91cd4a229a4309cde87612f0.png",
    "status": "Received",
    "created_at": "2026-09-11T12:35:10.123456",
    "updated_at": "2026-09-11T12:38:00.000000"
  }
}

---

## 7. Delete Payment Record

url : (http://192.168.1.59:8000/api/payments/1)
method : DELETE

params :- 

(None)

response :- 

{
  "message": "Payment record 'INV-260911-0001' deleted successfully"
}
