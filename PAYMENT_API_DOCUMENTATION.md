# Payment API Documentation (Admin and Management)

Note: This document covers the Admin Payment Management APIs for back-office operations.
For the customer-facing mobile dashboard with compulsory Bearer token and strict user isolation, please see USER_PAYMENT_DASHBOARD_API_DOCUMENTATION.md.

---

## 1. Get Next Auto-Generated Invoice / Order Number

url : (http://192.168.1.59:8000/api/payments/next-invoice-number)
method : GET

params :- 

(None)

response :- 

{
  "invoice_no": "INV-260917-0001",
  "order_no": "INV-260917-0001"
}

---

## 2. Customer Dropdown (From Quotation)

url : (http://192.168.1.59:8000/api/payments/customers)
method : GET

params :- 

(None)

response :- 

{
  "count": 5,
  "customers": [
    {
      "customer_name": "Customer A",
      "phone": "799797979859",
      "email": "grrvrrv",
      "address": "rbr",
      "quotations": [
        {
          "id": 7,
          "quotation_no": "QTN-260911-0002",
          "quotation_date": "2026-09-11",
          "grand_total": 13322.2,
          "status": "Sent"
        },
        {
          "id": 6,
          "quotation_no": "QTN-260911-0001",
          "quotation_date": "17 May 2025",
          "grand_total": 7186.2,
          "status": "Sent"
        }
      ]
    },
    {
      "customer_name": "Skyline Enterprises (UPDATED)",
      "phone": "+91 9876543210",
      "email": "contact@skyline.com",
      "address": "45 Industrial Area, Phase 2, New Delhi",
      "quotations": [
        {
          "id": 5,
          "quotation_no": "QTN-260910-0002",
          "quotation_date": "17 May 2025",
          "grand_total": 501500.0,
          "status": "Approved"
        }
      ]
    },
    {
      "customer_name": "Skyline Enterprises",
      "phone": "+91 9876543210",
      "email": "contact@skyline.com",
      "address": "45 Industrial Area, Phase 2, New Delhi",
      "quotations": [
        {
          "id": 4,
          "quotation_no": "QTN-260910-0001",
          "quotation_date": "17 May 2025",
          "grand_total": 501500.0,
          "status": "Sent"
        }
      ]
    },
    {
      "customer_name": "Skyline Enterprises (JSON)",
      "phone": "+91 9876543210",
      "email": "contact@skyline.com",
      "address": "45 Industrial Area, Phase 2, New Delhi",
      "quotations": [
        {
          "id": 3,
          "quotation_no": "QTN-250517-JSON1",
          "quotation_date": "17 May 2025",
          "grand_total": 501500.0,
          "status": "Sent"
        }
      ]
    },
    {
      "customer_name": "Skyline Enterprises (Form Data)",
      "phone": "+91 9876543210",
      "email": "contact@skyline.com",
      "address": "45 Industrial Area, Phase 2, New Delhi",
      "quotations": [
        {
          "id": 2,
          "quotation_no": "QTN-250517-FORM1",
          "quotation_date": "17 May 2025",
          "grand_total": 501500.0,
          "status": "Sent"
        }
      ]
    }
  ],
  "results": [
    {
      "customer_name": "Customer A",
      "phone": "799797979859",
      "email": "grrvrrv",
      "address": "rbr",
      "quotations": [
        {
          "id": 7,
          "quotation_no": "QTN-260911-0002",
          "quotation_date": "2026-09-11",
          "grand_total": 13322.2,
          "status": "Sent"
        },
        {
          "id": 6,
          "quotation_no": "QTN-260911-0001",
          "quotation_date": "17 May 2025",
          "grand_total": 7186.2,
          "status": "Sent"
        }
      ]
    },
    {
      "customer_name": "Skyline Enterprises (UPDATED)",
      "phone": "+91 9876543210",
      "email": "contact@skyline.com",
      "address": "45 Industrial Area, Phase 2, New Delhi",
      "quotations": [
        {
          "id": 5,
          "quotation_no": "QTN-260910-0002",
          "quotation_date": "17 May 2025",
          "grand_total": 501500.0,
          "status": "Approved"
        }
      ]
    },
    {
      "customer_name": "Skyline Enterprises",
      "phone": "+91 9876543210",
      "email": "contact@skyline.com",
      "address": "45 Industrial Area, Phase 2, New Delhi",
      "quotations": [
        {
          "id": 4,
          "quotation_no": "QTN-260910-0001",
          "quotation_date": "17 May 2025",
          "grand_total": 501500.0,
          "status": "Sent"
        }
      ]
    },
    {
      "customer_name": "Skyline Enterprises (JSON)",
      "phone": "+91 9876543210",
      "email": "contact@skyline.com",
      "address": "45 Industrial Area, Phase 2, New Delhi",
      "quotations": [
        {
          "id": 3,
          "quotation_no": "QTN-250517-JSON1",
          "quotation_date": "17 May 2025",
          "grand_total": 501500.0,
          "status": "Sent"
        }
      ]
    },
    {
      "customer_name": "Skyline Enterprises (Form Data)",
      "phone": "+91 9876543210",
      "email": "contact@skyline.com",
      "address": "45 Industrial Area, Phase 2, New Delhi",
      "quotations": [
        {
          "id": 2,
          "quotation_no": "QTN-250517-FORM1",
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

(Also supports http://192.168.1.59:8000/api/payment/add and http://192.168.1.59:8000/api/payments)

params :- 

invoice_no:INV-260917-0001
customer_name:Skyline Enterprises
quotation_id:1
quotation_no:QTN-250517-0001
customer_phone:+91 9876543210
customer_email:contact@skyline.com
customer_address:45 Industrial Area, Phase 2, New Delhi
payment_date:17 Sep 2026
amount_received:150000.0
payment_mode:Online
transaction_no:TXN-UPI-98234123
reference_no:REF-PAY-001
notes:30% advance payment received via PhonePe UPI
status:Received
payment_proof:upload (File: JPG, PNG, PDF)

response :- 

{
  "message": "Payment 'INV-260917-0001' saved successfully",
  "payment": {
    "id": 19,
    "payment_no": "PAY-260917-0001",
    "invoice_no": "INV-260917-0001",
    "order_no": "INV-260917-0001",
    "customer_name": "Skyline Enterprises",
    "customer_phone": "+91 9876543210",
    "customer_email": "contact@skyline.com",
    "customer_address": "45 Industrial Area, Phase 2, New Delhi",
    "quotation_id": 1,
    "quotation_no": "QTN-250517-0001",
    "payment_date": "17 Sep 2026",
    "amount_received": 150000.0,
    "payment_mode": "Online",
    "transaction_no": "TXN-UPI-98234123",
    "reference_no": "REF-PAY-001",
    "notes": "30% advance payment received via PhonePe UPI",
    "payment_proof": "/uploads/payments/sample_proof.png",
    "status": "Received",
    "created_at": "2026-09-17T18:00:00.000000",
    "updated_at": "2026-09-17T18:00:00.000000"
  }
}

---

## 4. List All Payments (Admin View - All Customers)

url : (http://192.168.1.59:8000/api/payments)
method : GET

params :- 

(None)

response :- 

{
  "count": 14,
  "payments": [
    {
      "id": 18,
      "payment_id": "PAY-METRO-001",
      "payment_no": "PAY-METRO-001",
      "method": "Bank Transfer",
      "payment_mode": "Bank Transfer",
      "method_icon": "bank",
      "invoice_no": "INV-METRO-001",
      "order_no": "INV-METRO-001",
      "invoice_id": null,
      "invoice_desc": "Sales Invoice - Generator",
      "category": "Generator",
      "amount": 50000.0,
      "amount_received": 50000.0,
      "formatted_amount": "Rs 50,000.00",
      "date": "15 Sep 2026",
      "payment_date": "15 Sep 2026",
      "time": "03:45 PM",
      "payment_time": "03:45 PM",
      "status": "Paid",
      "status_color": "green",
      "customer_name": "Metro Builders",
      "customer_phone": "+91 9123456780",
      "customer_email": "user2@example.com",
      "customer_address": null,
      "quotation_id": null,
      "quotation_no": null,
      "transaction_no": "TXN-METRO-001",
      "reference_no": "",
      "notes": "",
      "payment_proof": "",
      "user_id": 12,
      "created_at": "2026-09-17T12:13:51.609128",
      "updated_at": "2026-09-17T12:13:51.609129"
    },
    {
      "id": 17,
      "payment_id": "PAY-250517-007",
      "payment_no": "PAY-250517-007",
      "method": "UPI",
      "payment_mode": "UPI",
      "method_icon": "wallet",
      "invoice_no": "INV-250517-008",
      "order_no": "INV-250517-008",
      "invoice_id": null,
      "invoice_desc": "Service Invoice - Earthing",
      "category": "Earthing",
      "amount": 2510.0,
      "amount_received": 2510.0,
      "formatted_amount": "Rs 2,510.00",
      "date": "10 May 2025",
      "payment_date": "10 May 2025",
      "time": "12:05 PM",
      "payment_time": "12:05 PM",
      "status": "Paid",
      "status_color": "green",
      "customer_name": "Skyline Enterprises",
      "customer_phone": "+91 9876543210",
      "customer_email": "contact@skyline.com",
      "customer_address": null,
      "quotation_id": null,
      "quotation_no": null,
      "transaction_no": "TXN-UPI-33221100",
      "reference_no": "",
      "notes": "",
      "payment_proof": "",
      "user_id": 11,
      "created_at": "2026-09-17T12:13:51.609127",
      "updated_at": "2026-09-17T12:13:51.609127"
    },
    {
      "id": 16,
      "payment_id": "PAY-250517-006",
      "payment_no": "PAY-250517-006",
      "method": "NEFT",
      "payment_mode": "NEFT",
      "method_icon": "bank",
      "invoice_no": "INV-250517-007",
      "order_no": "INV-250517-007",
      "invoice_id": null,
      "invoice_desc": "Service Invoice - Panel",
      "category": "Panel",
      "amount": 4120.0,
      "amount_received": 4120.0,
      "formatted_amount": "Rs 4,120.00",
      "date": "11 May 2025",
      "payment_date": "11 May 2025",
      "time": "01:10 PM",
      "payment_time": "01:10 PM",
      "status": "Pending",
      "status_color": "red",
      "customer_name": "Skyline Enterprises",
      "customer_phone": "+91 9876543210",
      "customer_email": "contact@skyline.com",
      "customer_address": null,
      "quotation_id": null,
      "quotation_no": null,
      "transaction_no": "TXN-NEFT-554433",
      "reference_no": "",
      "notes": "",
      "payment_proof": "",
      "user_id": 11,
      "created_at": "2026-09-17T12:13:51.609125",
      "updated_at": "2026-09-17T12:13:51.609126"
    },
    {
      "id": 15,
      "payment_id": "PAY-250517-005",
      "payment_no": "PAY-250517-005",
      "method": "Bank Transfer",
      "payment_mode": "Bank Transfer",
      "method_icon": "bank",
      "invoice_no": "INV-250517-006",
      "order_no": "INV-250517-006",
      "invoice_id": null,
      "invoice_desc": "Service Invoice - Generator",
      "category": "Generator",
      "amount": 7890.0,
      "amount_received": 7890.0,
      "formatted_amount": "Rs 7,890.00",
      "date": "12 May 2025",
      "payment_date": "12 May 2025",
      "time": "04:30 PM",
      "payment_time": "04:30 PM",
      "status": "Partial",
      "status_color": "orange",
      "customer_name": "Skyline Enterprises",
      "customer_phone": "+91 9876543210",
      "customer_email": "contact@skyline.com",
      "customer_address": null,
      "quotation_id": null,
      "quotation_no": null,
      "transaction_no": "TXN-BT-99887766",
      "reference_no": "",
      "notes": "",
      "payment_proof": "",
      "user_id": 11,
      "created_at": "2026-09-17T12:13:51.609123",
      "updated_at": "2026-09-17T12:13:51.609124"
    },
    {
      "id": 14,
      "payment_id": "PAY-250517-004",
      "payment_no": "PAY-250517-004",
      "method": "Card",
      "payment_mode": "Card",
      "method_icon": "card",
      "invoice_no": "INV-250517-004",
      "order_no": "INV-250517-004",
      "invoice_id": null,
      "invoice_desc": "Service Invoice - Lift",
      "category": "Lift",
      "amount": 3250.0,
      "amount_received": 3250.0,
      "formatted_amount": "Rs 3,250.00",
      "date": "13 May 2025",
      "payment_date": "13 May 2025",
      "time": "09:20 AM",
      "payment_time": "09:20 AM",
      "status": "Paid",
      "status_color": "green",
      "customer_name": "Skyline Enterprises",
      "customer_phone": "+91 9876543210",
      "customer_email": "contact@skyline.com",
      "customer_address": null,
      "quotation_id": null,
      "quotation_no": null,
      "transaction_no": "TXN-CARD-445566",
      "reference_no": "",
      "notes": "",
      "payment_proof": "",
      "user_id": 11,
      "created_at": "2026-09-17T12:13:51.609122",
      "updated_at": "2026-09-17T12:13:51.609122"
    },
    {
      "id": 13,
      "payment_id": "PAY-250517-003",
      "payment_no": "PAY-250517-003",
      "method": "UPI",
      "payment_mode": "UPI",
      "method_icon": "wallet",
      "invoice_no": "INV-250517-003",
      "order_no": "INV-250517-003",
      "invoice_id": null,
      "invoice_desc": "Sales Invoice - Panel",
      "category": "Panel",
      "amount": 6350.0,
      "amount_received": 6350.0,
      "formatted_amount": "Rs 6,350.00",
      "date": "15 May 2025",
      "payment_date": "15 May 2025",
      "time": "11:45 AM",
      "payment_time": "11:45 AM",
      "status": "Paid",
      "status_color": "green",
      "customer_name": "Skyline Enterprises",
      "customer_phone": "+91 9876543210",
      "customer_email": "contact@skyline.com",
      "customer_address": null,
      "quotation_id": null,
      "quotation_no": null,
      "transaction_no": "TXN-UPI-88776655",
      "reference_no": "",
      "notes": "",
      "payment_proof": "",
      "user_id": 11,
      "created_at": "2026-09-17T12:13:51.609120",
      "updated_at": "2026-09-17T12:13:51.609121"
    },
    {
      "id": 12,
      "payment_id": "PAY-250517-002",
      "payment_no": "PAY-250517-002",
      "method": "Bank Transfer",
      "payment_mode": "Bank Transfer",
      "method_icon": "bank",
      "invoice_no": "INV-250517-002",
      "order_no": "INV-250517-002",
      "invoice_id": null,
      "invoice_desc": "Sales Invoice - Generator",
      "category": "Generator",
      "amount": 5000.0,
      "amount_received": 5000.0,
      "formatted_amount": "Rs 5,000.00",
      "date": "16 May 2025",
      "payment_date": "16 May 2025",
      "time": "02:15 PM",
      "payment_time": "02:15 PM",
      "status": "Partial",
      "status_color": "orange",
      "customer_name": "Skyline Enterprises",
      "customer_phone": "+91 9876543210",
      "customer_email": "contact@skyline.com",
      "customer_address": null,
      "quotation_id": null,
      "quotation_no": null,
      "transaction_no": "TXN-BT-11223344",
      "reference_no": "",
      "notes": "",
      "payment_proof": "",
      "user_id": 11,
      "created_at": "2026-09-17T12:13:51.609118",
      "updated_at": "2026-09-17T12:13:51.609119"
    },
    {
      "id": 11,
      "payment_id": "PAY-250517-001",
      "payment_no": "PAY-250517-001",
      "method": "UPI",
      "payment_mode": "UPI",
      "method_icon": "wallet",
      "invoice_no": "INV-250517-001",
      "order_no": "INV-250517-001",
      "invoice_id": null,
      "invoice_desc": "Sales Invoice - Lift",
      "category": "Lift",
      "amount": 4560.0,
      "amount_received": 4560.0,
      "formatted_amount": "Rs 4,560.00",
      "date": "17 May 2025",
      "payment_date": "17 May 2025",
      "time": "10:30 AM",
      "payment_time": "10:30 AM",
      "status": "Paid",
      "status_color": "green",
      "customer_name": "Skyline Enterprises",
      "customer_phone": "+91 9876543210",
      "customer_email": "contact@skyline.com",
      "customer_address": null,
      "quotation_id": null,
      "quotation_no": null,
      "transaction_no": "TXN-UPI-98234123",
      "reference_no": "",
      "notes": "",
      "payment_proof": "",
      "user_id": 11,
      "created_at": "2026-09-17T12:13:51.609110",
      "updated_at": "2026-09-17T12:13:51.609116"
    },
    {
      "id": 8,
      "payment_id": "PAY-000008",
      "payment_no": "PAY-000008",
      "method": "UPI",
      "payment_mode": "UPI",
      "method_icon": "wallet",
      "invoice_no": "INV-260914-0006",
      "order_no": "INV-260914-0006",
      "invoice_id": null,
      "invoice_desc": "Invoice",
      "category": "",
      "amount": 25000.0,
      "amount_received": 25000.0,
      "formatted_amount": "Rs 25,000.00",
      "date": "14 Sep 2026",
      "payment_date": "14 Sep 2026",
      "time": "10:30 AM",
      "payment_time": "10:30 AM",
      "status": "Paid",
      "status_color": "green",
      "customer_name": "Test Customer Sharma",
      "customer_phone": null,
      "customer_email": null,
      "customer_address": null,
      "quotation_id": null,
      "quotation_no": null,
      "transaction_no": "",
      "reference_no": "",
      "notes": "Advance payment via UPI",
      "payment_proof": "",
      "user_id": null,
      "created_at": "2026-09-14T10:09:59.834476",
      "updated_at": "2026-09-14T10:09:59.834482"
    },
    {
      "id": 7,
      "payment_id": "PAY-000007",
      "payment_no": "PAY-000007",
      "method": "UPI",
      "payment_mode": "UPI",
      "method_icon": "wallet",
      "invoice_no": "INV-260914-0005",
      "order_no": "INV-260914-0005",
      "invoice_id": null,
      "invoice_desc": "Invoice",
      "category": "",
      "amount": 25000.0,
      "amount_received": 25000.0,
      "formatted_amount": "Rs 25,000.00",
      "date": "14 Sep 2026",
      "payment_date": "14 Sep 2026",
      "time": "10:30 AM",
      "payment_time": "10:30 AM",
      "status": "Paid",
      "status_color": "green",
      "customer_name": "Test Customer Sharma",
      "customer_phone": null,
      "customer_email": null,
      "customer_address": null,
      "quotation_id": null,
      "quotation_no": null,
      "transaction_no": "",
      "reference_no": "",
      "notes": "Advance payment via UPI",
      "payment_proof": "",
      "user_id": null,
      "created_at": "2026-09-14T10:06:53.936788",
      "updated_at": "2026-09-14T10:06:53.936793"
    },
    {
      "id": 6,
      "payment_id": "PAY-000006",
      "payment_no": "PAY-000006",
      "method": "UPI",
      "payment_mode": "UPI",
      "method_icon": "wallet",
      "invoice_no": "INV-260914-0004",
      "order_no": "INV-260914-0004",
      "invoice_id": null,
      "invoice_desc": "Invoice",
      "category": "",
      "amount": 25000.0,
      "amount_received": 25000.0,
      "formatted_amount": "Rs 25,000.00",
      "date": "14 Sep 2026",
      "payment_date": "14 Sep 2026",
      "time": "10:30 AM",
      "payment_time": "10:30 AM",
      "status": "Paid",
      "status_color": "green",
      "customer_name": "Test Customer Sharma",
      "customer_phone": null,
      "customer_email": null,
      "customer_address": null,
      "quotation_id": null,
      "quotation_no": null,
      "transaction_no": "",
      "reference_no": "",
      "notes": "Advance payment via UPI",
      "payment_proof": "",
      "user_id": null,
      "created_at": "2026-09-14T10:04:19.597791",
      "updated_at": "2026-09-14T10:04:19.597795"
    },
    {
      "id": 5,
      "payment_id": "PAY-000005",
      "payment_no": "PAY-000005",
      "method": "UPI",
      "payment_mode": "UPI",
      "method_icon": "wallet",
      "invoice_no": "INV-260914-0003",
      "order_no": "INV-260914-0003",
      "invoice_id": null,
      "invoice_desc": "Invoice",
      "category": "",
      "amount": 25000.0,
      "amount_received": 25000.0,
      "formatted_amount": "Rs 25,000.00",
      "date": "14 Sep 2026",
      "payment_date": "14 Sep 2026",
      "time": "10:30 AM",
      "payment_time": "10:30 AM",
      "status": "Paid",
      "status_color": "green",
      "customer_name": "Test Customer Sharma",
      "customer_phone": null,
      "customer_email": null,
      "customer_address": null,
      "quotation_id": null,
      "quotation_no": null,
      "transaction_no": "",
      "reference_no": "",
      "notes": "Advance payment via UPI",
      "payment_proof": "",
      "user_id": null,
      "created_at": "2026-09-14T10:01:28.164059",
      "updated_at": "2026-09-14T10:01:28.164066"
    },
    {
      "id": 4,
      "payment_id": "PAY-000004",
      "payment_no": "PAY-000004",
      "method": "UPI",
      "payment_mode": "UPI",
      "method_icon": "wallet",
      "invoice_no": "INV-260914-0002",
      "order_no": "INV-260914-0002",
      "invoice_id": null,
      "invoice_desc": "Invoice",
      "category": "",
      "amount": 25000.0,
      "amount_received": 25000.0,
      "formatted_amount": "Rs 25,000.00",
      "date": "14 Sep 2026",
      "payment_date": "14 Sep 2026",
      "time": "10:30 AM",
      "payment_time": "10:30 AM",
      "status": "Paid",
      "status_color": "green",
      "customer_name": "Test Customer Sharma",
      "customer_phone": null,
      "customer_email": null,
      "customer_address": null,
      "quotation_id": null,
      "quotation_no": null,
      "transaction_no": "",
      "reference_no": "",
      "notes": "Advance payment via UPI",
      "payment_proof": "",
      "user_id": null,
      "created_at": "2026-09-14T09:43:17.921532",
      "updated_at": "2026-09-14T09:43:17.921538"
    },
    {
      "id": 3,
      "payment_id": "PAY-000003",
      "payment_no": "PAY-000003",
      "method": "UPI",
      "payment_mode": "UPI",
      "method_icon": "wallet",
      "invoice_no": "INV-260914-0001",
      "order_no": "INV-260914-0001",
      "invoice_id": null,
      "invoice_desc": "Invoice",
      "category": "",
      "amount": 25000.0,
      "amount_received": 25000.0,
      "formatted_amount": "Rs 25,000.00",
      "date": "14 Sep 2026",
      "payment_date": "14 Sep 2026",
      "time": "10:30 AM",
      "payment_time": "10:30 AM",
      "status": "Paid",
      "status_color": "green",
      "customer_name": "Test Customer Sharma",
      "customer_phone": null,
      "customer_email": null,
      "customer_address": null,
      "quotation_id": null,
      "quotation_no": null,
      "transaction_no": "",
      "reference_no": "",
      "notes": "Advance payment via UPI",
      "payment_proof": "",
      "user_id": null,
      "created_at": "2026-09-14T09:42:37.038419",
      "updated_at": "2026-09-14T09:42:37.038426"
    }
  ],
  "results": [
    {
      "id": 18,
      "payment_id": "PAY-METRO-001",
      "payment_no": "PAY-METRO-001",
      "method": "Bank Transfer",
      "payment_mode": "Bank Transfer",
      "method_icon": "bank",
      "invoice_no": "INV-METRO-001",
      "order_no": "INV-METRO-001",
      "invoice_id": null,
      "invoice_desc": "Sales Invoice - Generator",
      "category": "Generator",
      "amount": 50000.0,
      "amount_received": 50000.0,
      "formatted_amount": "Rs 50,000.00",
      "date": "15 Sep 2026",
      "payment_date": "15 Sep 2026",
      "time": "03:45 PM",
      "payment_time": "03:45 PM",
      "status": "Paid",
      "status_color": "green",
      "customer_name": "Metro Builders",
      "customer_phone": "+91 9123456780",
      "customer_email": "user2@example.com",
      "customer_address": null,
      "quotation_id": null,
      "quotation_no": null,
      "transaction_no": "TXN-METRO-001",
      "reference_no": "",
      "notes": "",
      "payment_proof": "",
      "user_id": 12,
      "created_at": "2026-09-17T12:13:51.609128",
      "updated_at": "2026-09-17T12:13:51.609129"
    },
    {
      "id": 17,
      "payment_id": "PAY-250517-007",
      "payment_no": "PAY-250517-007",
      "method": "UPI",
      "payment_mode": "UPI",
      "method_icon": "wallet",
      "invoice_no": "INV-250517-008",
      "order_no": "INV-250517-008",
      "invoice_id": null,
      "invoice_desc": "Service Invoice - Earthing",
      "category": "Earthing",
      "amount": 2510.0,
      "amount_received": 2510.0,
      "formatted_amount": "Rs 2,510.00",
      "date": "10 May 2025",
      "payment_date": "10 May 2025",
      "time": "12:05 PM",
      "payment_time": "12:05 PM",
      "status": "Paid",
      "status_color": "green",
      "customer_name": "Skyline Enterprises",
      "customer_phone": "+91 9876543210",
      "customer_email": "contact@skyline.com",
      "customer_address": null,
      "quotation_id": null,
      "quotation_no": null,
      "transaction_no": "TXN-UPI-33221100",
      "reference_no": "",
      "notes": "",
      "payment_proof": "",
      "user_id": 11,
      "created_at": "2026-09-17T12:13:51.609127",
      "updated_at": "2026-09-17T12:13:51.609127"
    },
    {
      "id": 16,
      "payment_id": "PAY-250517-006",
      "payment_no": "PAY-250517-006",
      "method": "NEFT",
      "payment_mode": "NEFT",
      "method_icon": "bank",
      "invoice_no": "INV-250517-007",
      "order_no": "INV-250517-007",
      "invoice_id": null,
      "invoice_desc": "Service Invoice - Panel",
      "category": "Panel",
      "amount": 4120.0,
      "amount_received": 4120.0,
      "formatted_amount": "Rs 4,120.00",
      "date": "11 May 2025",
      "payment_date": "11 May 2025",
      "time": "01:10 PM",
      "payment_time": "01:10 PM",
      "status": "Pending",
      "status_color": "red",
      "customer_name": "Skyline Enterprises",
      "customer_phone": "+91 9876543210",
      "customer_email": "contact@skyline.com",
      "customer_address": null,
      "quotation_id": null,
      "quotation_no": null,
      "transaction_no": "TXN-NEFT-554433",
      "reference_no": "",
      "notes": "",
      "payment_proof": "",
      "user_id": 11,
      "created_at": "2026-09-17T12:13:51.609125",
      "updated_at": "2026-09-17T12:13:51.609126"
    },
    {
      "id": 15,
      "payment_id": "PAY-250517-005",
      "payment_no": "PAY-250517-005",
      "method": "Bank Transfer",
      "payment_mode": "Bank Transfer",
      "method_icon": "bank",
      "invoice_no": "INV-250517-006",
      "order_no": "INV-250517-006",
      "invoice_id": null,
      "invoice_desc": "Service Invoice - Generator",
      "category": "Generator",
      "amount": 7890.0,
      "amount_received": 7890.0,
      "formatted_amount": "Rs 7,890.00",
      "date": "12 May 2025",
      "payment_date": "12 May 2025",
      "time": "04:30 PM",
      "payment_time": "04:30 PM",
      "status": "Partial",
      "status_color": "orange",
      "customer_name": "Skyline Enterprises",
      "customer_phone": "+91 9876543210",
      "customer_email": "contact@skyline.com",
      "customer_address": null,
      "quotation_id": null,
      "quotation_no": null,
      "transaction_no": "TXN-BT-99887766",
      "reference_no": "",
      "notes": "",
      "payment_proof": "",
      "user_id": 11,
      "created_at": "2026-09-17T12:13:51.609123",
      "updated_at": "2026-09-17T12:13:51.609124"
    },
    {
      "id": 14,
      "payment_id": "PAY-250517-004",
      "payment_no": "PAY-250517-004",
      "method": "Card",
      "payment_mode": "Card",
      "method_icon": "card",
      "invoice_no": "INV-250517-004",
      "order_no": "INV-250517-004",
      "invoice_id": null,
      "invoice_desc": "Service Invoice - Lift",
      "category": "Lift",
      "amount": 3250.0,
      "amount_received": 3250.0,
      "formatted_amount": "Rs 3,250.00",
      "date": "13 May 2025",
      "payment_date": "13 May 2025",
      "time": "09:20 AM",
      "payment_time": "09:20 AM",
      "status": "Paid",
      "status_color": "green",
      "customer_name": "Skyline Enterprises",
      "customer_phone": "+91 9876543210",
      "customer_email": "contact@skyline.com",
      "customer_address": null,
      "quotation_id": null,
      "quotation_no": null,
      "transaction_no": "TXN-CARD-445566",
      "reference_no": "",
      "notes": "",
      "payment_proof": "",
      "user_id": 11,
      "created_at": "2026-09-17T12:13:51.609122",
      "updated_at": "2026-09-17T12:13:51.609122"
    },
    {
      "id": 13,
      "payment_id": "PAY-250517-003",
      "payment_no": "PAY-250517-003",
      "method": "UPI",
      "payment_mode": "UPI",
      "method_icon": "wallet",
      "invoice_no": "INV-250517-003",
      "order_no": "INV-250517-003",
      "invoice_id": null,
      "invoice_desc": "Sales Invoice - Panel",
      "category": "Panel",
      "amount": 6350.0,
      "amount_received": 6350.0,
      "formatted_amount": "Rs 6,350.00",
      "date": "15 May 2025",
      "payment_date": "15 May 2025",
      "time": "11:45 AM",
      "payment_time": "11:45 AM",
      "status": "Paid",
      "status_color": "green",
      "customer_name": "Skyline Enterprises",
      "customer_phone": "+91 9876543210",
      "customer_email": "contact@skyline.com",
      "customer_address": null,
      "quotation_id": null,
      "quotation_no": null,
      "transaction_no": "TXN-UPI-88776655",
      "reference_no": "",
      "notes": "",
      "payment_proof": "",
      "user_id": 11,
      "created_at": "2026-09-17T12:13:51.609120",
      "updated_at": "2026-09-17T12:13:51.609121"
    },
    {
      "id": 12,
      "payment_id": "PAY-250517-002",
      "payment_no": "PAY-250517-002",
      "method": "Bank Transfer",
      "payment_mode": "Bank Transfer",
      "method_icon": "bank",
      "invoice_no": "INV-250517-002",
      "order_no": "INV-250517-002",
      "invoice_id": null,
      "invoice_desc": "Sales Invoice - Generator",
      "category": "Generator",
      "amount": 5000.0,
      "amount_received": 5000.0,
      "formatted_amount": "Rs 5,000.00",
      "date": "16 May 2025",
      "payment_date": "16 May 2025",
      "time": "02:15 PM",
      "payment_time": "02:15 PM",
      "status": "Partial",
      "status_color": "orange",
      "customer_name": "Skyline Enterprises",
      "customer_phone": "+91 9876543210",
      "customer_email": "contact@skyline.com",
      "customer_address": null,
      "quotation_id": null,
      "quotation_no": null,
      "transaction_no": "TXN-BT-11223344",
      "reference_no": "",
      "notes": "",
      "payment_proof": "",
      "user_id": 11,
      "created_at": "2026-09-17T12:13:51.609118",
      "updated_at": "2026-09-17T12:13:51.609119"
    },
    {
      "id": 11,
      "payment_id": "PAY-250517-001",
      "payment_no": "PAY-250517-001",
      "method": "UPI",
      "payment_mode": "UPI",
      "method_icon": "wallet",
      "invoice_no": "INV-250517-001",
      "order_no": "INV-250517-001",
      "invoice_id": null,
      "invoice_desc": "Sales Invoice - Lift",
      "category": "Lift",
      "amount": 4560.0,
      "amount_received": 4560.0,
      "formatted_amount": "Rs 4,560.00",
      "date": "17 May 2025",
      "payment_date": "17 May 2025",
      "time": "10:30 AM",
      "payment_time": "10:30 AM",
      "status": "Paid",
      "status_color": "green",
      "customer_name": "Skyline Enterprises",
      "customer_phone": "+91 9876543210",
      "customer_email": "contact@skyline.com",
      "customer_address": null,
      "quotation_id": null,
      "quotation_no": null,
      "transaction_no": "TXN-UPI-98234123",
      "reference_no": "",
      "notes": "",
      "payment_proof": "",
      "user_id": 11,
      "created_at": "2026-09-17T12:13:51.609110",
      "updated_at": "2026-09-17T12:13:51.609116"
    },
    {
      "id": 8,
      "payment_id": "PAY-000008",
      "payment_no": "PAY-000008",
      "method": "UPI",
      "payment_mode": "UPI",
      "method_icon": "wallet",
      "invoice_no": "INV-260914-0006",
      "order_no": "INV-260914-0006",
      "invoice_id": null,
      "invoice_desc": "Invoice",
      "category": "",
      "amount": 25000.0,
      "amount_received": 25000.0,
      "formatted_amount": "Rs 25,000.00",
      "date": "14 Sep 2026",
      "payment_date": "14 Sep 2026",
      "time": "10:30 AM",
      "payment_time": "10:30 AM",
      "status": "Paid",
      "status_color": "green",
      "customer_name": "Test Customer Sharma",
      "customer_phone": null,
      "customer_email": null,
      "customer_address": null,
      "quotation_id": null,
      "quotation_no": null,
      "transaction_no": "",
      "reference_no": "",
      "notes": "Advance payment via UPI",
      "payment_proof": "",
      "user_id": null,
      "created_at": "2026-09-14T10:09:59.834476",
      "updated_at": "2026-09-14T10:09:59.834482"
    },
    {
      "id": 7,
      "payment_id": "PAY-000007",
      "payment_no": "PAY-000007",
      "method": "UPI",
      "payment_mode": "UPI",
      "method_icon": "wallet",
      "invoice_no": "INV-260914-0005",
      "order_no": "INV-260914-0005",
      "invoice_id": null,
      "invoice_desc": "Invoice",
      "category": "",
      "amount": 25000.0,
      "amount_received": 25000.0,
      "formatted_amount": "Rs 25,000.00",
      "date": "14 Sep 2026",
      "payment_date": "14 Sep 2026",
      "time": "10:30 AM",
      "payment_time": "10:30 AM",
      "status": "Paid",
      "status_color": "green",
      "customer_name": "Test Customer Sharma",
      "customer_phone": null,
      "customer_email": null,
      "customer_address": null,
      "quotation_id": null,
      "quotation_no": null,
      "transaction_no": "",
      "reference_no": "",
      "notes": "Advance payment via UPI",
      "payment_proof": "",
      "user_id": null,
      "created_at": "2026-09-14T10:06:53.936788",
      "updated_at": "2026-09-14T10:06:53.936793"
    },
    {
      "id": 6,
      "payment_id": "PAY-000006",
      "payment_no": "PAY-000006",
      "method": "UPI",
      "payment_mode": "UPI",
      "method_icon": "wallet",
      "invoice_no": "INV-260914-0004",
      "order_no": "INV-260914-0004",
      "invoice_id": null,
      "invoice_desc": "Invoice",
      "category": "",
      "amount": 25000.0,
      "amount_received": 25000.0,
      "formatted_amount": "Rs 25,000.00",
      "date": "14 Sep 2026",
      "payment_date": "14 Sep 2026",
      "time": "10:30 AM",
      "payment_time": "10:30 AM",
      "status": "Paid",
      "status_color": "green",
      "customer_name": "Test Customer Sharma",
      "customer_phone": null,
      "customer_email": null,
      "customer_address": null,
      "quotation_id": null,
      "quotation_no": null,
      "transaction_no": "",
      "reference_no": "",
      "notes": "Advance payment via UPI",
      "payment_proof": "",
      "user_id": null,
      "created_at": "2026-09-14T10:04:19.597791",
      "updated_at": "2026-09-14T10:04:19.597795"
    },
    {
      "id": 5,
      "payment_id": "PAY-000005",
      "payment_no": "PAY-000005",
      "method": "UPI",
      "payment_mode": "UPI",
      "method_icon": "wallet",
      "invoice_no": "INV-260914-0003",
      "order_no": "INV-260914-0003",
      "invoice_id": null,
      "invoice_desc": "Invoice",
      "category": "",
      "amount": 25000.0,
      "amount_received": 25000.0,
      "formatted_amount": "Rs 25,000.00",
      "date": "14 Sep 2026",
      "payment_date": "14 Sep 2026",
      "time": "10:30 AM",
      "payment_time": "10:30 AM",
      "status": "Paid",
      "status_color": "green",
      "customer_name": "Test Customer Sharma",
      "customer_phone": null,
      "customer_email": null,
      "customer_address": null,
      "quotation_id": null,
      "quotation_no": null,
      "transaction_no": "",
      "reference_no": "",
      "notes": "Advance payment via UPI",
      "payment_proof": "",
      "user_id": null,
      "created_at": "2026-09-14T10:01:28.164059",
      "updated_at": "2026-09-14T10:01:28.164066"
    },
    {
      "id": 4,
      "payment_id": "PAY-000004",
      "payment_no": "PAY-000004",
      "method": "UPI",
      "payment_mode": "UPI",
      "method_icon": "wallet",
      "invoice_no": "INV-260914-0002",
      "order_no": "INV-260914-0002",
      "invoice_id": null,
      "invoice_desc": "Invoice",
      "category": "",
      "amount": 25000.0,
      "amount_received": 25000.0,
      "formatted_amount": "Rs 25,000.00",
      "date": "14 Sep 2026",
      "payment_date": "14 Sep 2026",
      "time": "10:30 AM",
      "payment_time": "10:30 AM",
      "status": "Paid",
      "status_color": "green",
      "customer_name": "Test Customer Sharma",
      "customer_phone": null,
      "customer_email": null,
      "customer_address": null,
      "quotation_id": null,
      "quotation_no": null,
      "transaction_no": "",
      "reference_no": "",
      "notes": "Advance payment via UPI",
      "payment_proof": "",
      "user_id": null,
      "created_at": "2026-09-14T09:43:17.921532",
      "updated_at": "2026-09-14T09:43:17.921538"
    },
    {
      "id": 3,
      "payment_id": "PAY-000003",
      "payment_no": "PAY-000003",
      "method": "UPI",
      "payment_mode": "UPI",
      "method_icon": "wallet",
      "invoice_no": "INV-260914-0001",
      "order_no": "INV-260914-0001",
      "invoice_id": null,
      "invoice_desc": "Invoice",
      "category": "",
      "amount": 25000.0,
      "amount_received": 25000.0,
      "formatted_amount": "Rs 25,000.00",
      "date": "14 Sep 2026",
      "payment_date": "14 Sep 2026",
      "time": "10:30 AM",
      "payment_time": "10:30 AM",
      "status": "Paid",
      "status_color": "green",
      "customer_name": "Test Customer Sharma",
      "customer_phone": null,
      "customer_email": null,
      "customer_address": null,
      "quotation_id": null,
      "quotation_no": null,
      "transaction_no": "",
      "reference_no": "",
      "notes": "Advance payment via UPI",
      "payment_proof": "",
      "user_id": null,
      "created_at": "2026-09-14T09:42:37.038419",
      "updated_at": "2026-09-14T09:42:37.038426"
    }
  ]
}

---

## 5. Get Single Payment Details

url : (http://192.168.1.59:8000/api/payments/18)
method : GET

params :- 

(None)

response :- 

{
  "detail": "Bearer token is compulsory. Please provide Authorization: Bearer <token>"
}

---

## 6. Update Payment Record

url : (http://192.168.1.59:8000/api/payments/18)
method : PUT

params :- 

status:Received
transaction_no:CHQ-882194
notes:Cheque cleared

response :- 

{
  "message": "Payment 'INV-METRO-001' updated successfully",
  "payment": {
    "id": 18,
    "payment_no": "PAY-METRO-001",
    "invoice_no": "INV-METRO-001",
    "order_no": "INV-METRO-001",
    "customer_name": "Metro Builders",
    "customer_phone": "+91 9123456780",
    "customer_email": "user2@example.com",
    "customer_address": null,
    "quotation_id": null,
    "quotation_no": null,
    "payment_date": "15 Sep 2026",
    "amount_received": 50000.0,
    "payment_mode": "Bank Transfer",
    "transaction_no": "CHQ-882194",
    "reference_no": "",
    "notes": "Cheque cleared",
    "payment_proof": "",
    "status": "Received",
    "created_at": "2026-09-17T12:13:51.609128",
    "updated_at": "2026-09-17T18:00:00.000000"
  }
}

---

## 7. Delete Payment Record

url : (http://192.168.1.59:8000/api/payments/18)
method : DELETE

params :- 

(None)

response :- 

{
  "message": "Payment record 'INV-METRO-001' deleted successfully"
}
