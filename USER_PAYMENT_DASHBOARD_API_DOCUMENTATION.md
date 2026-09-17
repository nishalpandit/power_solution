# User Payment Dashboard API Documentation

Bearer token is compulsory for all endpoints.
The user is automatically identified from the Bearer token.
The backend returns ONLY payments belonging to that logged-in user.
No user_id, phone, email, or customer_name parameters are needed.

Important: This API does NOT return payments for all users combined.
Each user sees strictly their own payments.

Database Verification Proof Across All Users in db.sqlite3:
- User 11 (Skyline Enterprises): 7 payments, Total Rs 33,680.00 (PAY-250517-001 to PAY-250517-007)
- User 12 (Metro Builders): 1 payment, Total Rs 50,000.00 (PAY-METRO-001)
- User 7 (Aman): 0 payments, Total Rs 0.00
- User 8 (Deep Amam): 0 payments, Total Rs 0.00
- User 4 (Nihal): 0 payments, Total Rs 0.00
- User 1 (Test User): 0 payments, Total Rs 0.00
- Admin All Payments API (GET /api/payments): 14 payments total across all customers

If request is sent without Bearer token or with invalid token, API returns:
HTTP 401 Unauthorized
{
  "detail": "Bearer token is compulsory. Please provide Authorization: Bearer <token>"
}

---

## 1. User Payment Dashboard (Summary Cards + Payment Transactions List)

url : (http://192.168.1.59:8000/api/payments/dashboard)
method : GET

(Also supports http://192.168.1.59:8000/api/payments/user-dashboard)

headers :- 

Authorization: Bearer <user_login_token> (Required)

response (Logged in as User 11 - Skyline Enterprises - strictly 7 payments) :- 

{
  "summary": {
    "total_payments": {
      "title": "Total Payments",
      "count": "7",
      "amount": 33680.0,
      "formatted_amount": "Rs 33,680.00"
    },
    "paid": {
      "title": "Paid",
      "count": "4",
      "amount": 16670.0,
      "formatted_amount": "Rs 16,670.00"
    },
    "partial": {
      "title": "Partial",
      "count": "2",
      "amount": 12890.0,
      "formatted_amount": "Rs 12,890.00"
    },
    "pending": {
      "title": "Pending",
      "count": "1",
      "amount": 4120.0,
      "formatted_amount": "Rs 4,120.00"
    }
  },
  "payments": [
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
    }
  ],
  "count": 7
}

---

## 2. User Isolation Example 1 (Logged in as User 12 - Metro Builders)

When User 12 logs in with their token, they see strictly their 1 payment:

url : (http://192.168.1.59:8000/api/payments/dashboard)
method : GET

headers :- 

Authorization: Bearer <user12_login_token> (Required)

response :- 

{
  "summary": {
    "total_payments": {
      "title": "Total Payments",
      "count": "1",
      "amount": 50000.0,
      "formatted_amount": "Rs 50,000.00"
    },
    "paid": {
      "title": "Paid",
      "count": "1",
      "amount": 50000.0,
      "formatted_amount": "Rs 50,000.00"
    },
    "partial": {
      "title": "Partial",
      "count": "0",
      "amount": 0,
      "formatted_amount": "Rs 0.00"
    },
    "pending": {
      "title": "Pending",
      "count": "0",
      "amount": 0,
      "formatted_amount": "Rs 0.00"
    }
  },
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
    }
  ],
  "count": 1
}

---

## 3. User Isolation Example 2 - Empty State (Logged in as User with 0 Payments, e.g. User 7 - Aman)

When a user with no payments logs in, the API returns count 0, Rs 0.00, and an empty payments array:

url : (http://192.168.1.59:8000/api/payments/dashboard)
method : GET

headers :- 

Authorization: Bearer <user7_login_token> (Required)

response :- 

{
  "summary": {
    "total_payments": {
      "title": "Total Payments",
      "count": "0",
      "amount": 0,
      "formatted_amount": "Rs 0.00"
    },
    "paid": {
      "title": "Paid",
      "count": "0",
      "amount": 0,
      "formatted_amount": "Rs 0.00"
    },
    "partial": {
      "title": "Partial",
      "count": "0",
      "amount": 0,
      "formatted_amount": "Rs 0.00"
    },
    "pending": {
      "title": "Pending",
      "count": "0",
      "amount": 0,
      "formatted_amount": "Rs 0.00"
    }
  },
  "payments": [],
  "count": 0
}

---

## 4. Single Payment Details (On Tapping Payment Item / Action Arrow)

url : (http://192.168.1.59:8000/api/payments/PAY-250517-001)
method : GET

(Also supports ID like http://192.168.1.59:8000/api/payments/11)

headers :- 

Authorization: Bearer <user_login_token> (Required)

response :- 

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
}

---

## 5. Cross-User Security Check (HTTP 403 Forbidden)

If User 7 or User 12 attempts to access User 11 payment (PAY-250517-001) by ID:

url : (http://192.168.1.59:8000/api/payments/PAY-250517-001)
method : GET

headers :- 

Authorization: Bearer <user7_login_token> (Required)

response :- 

HTTP 403 Forbidden
{
  "detail": "You do not have permission to view this payment"
}

---

## 6. Missing Bearer Token Security Check (HTTP 401 Unauthorized)

If request is sent without Authorization header:

url : (http://192.168.1.59:8000/api/payments/dashboard)
method : GET

headers :- 

(No Authorization header)

response :- 

HTTP 401 Unauthorized
{
  "detail": "Bearer token is compulsory. Please provide Authorization: Bearer <token>"
}

---

## 7. Difference Between User Payment Dashboard and Admin Payments API

1. User Payment Dashboard: GET /api/payments/dashboard
- Requires Bearer token.
- Strictly filtered to logged-in user.
- Returns summary analytics cards (Total Payments, Paid, Partial, Pending) formatted for Flutter.
- User 11 sees only their 7 payments. User 12 sees only their 1 payment.

2. Admin All Payments List: GET /api/payments
- Used by admin / back-office portal.
- Lists all 14 payments across all customers and users.
