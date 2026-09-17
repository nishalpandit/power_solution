# User Invoice Dashboard API Documentation

Bearer token is compulsory for all endpoints.
The user is automatically identified from the Bearer token.
The backend returns ONLY invoices belonging to that logged-in user.
No user_id, phone, email, or customer_name parameters are needed.

If request is sent without Bearer token or with invalid token, API returns:
HTTP 401 Unauthorized
{
  "detail": "Bearer token is compulsory. Please provide Authorization: Bearer <token>"
}

---

## 1. User Invoice Dashboard (Summary Cards + Sales & Service Invoices)

url : (http://192.168.1.59:8000/api/invoices/dashboard)
method : GET

(Also supports http://192.168.1.59:8000/api/invoices/user-dashboard)

headers :- 

Authorization: Bearer <user_login_token> (Required)

response (Logged in as User 11 - Skyline Enterprises) :- 

{
  "summary": {
    "total_invoices": {
      "title": "Total Invoice",
      "count": "3",
      "amount": 509310.0,
      "formatted_amount": "Rs 5,09,310.00"
    },
    "paid": {
      "title": "Paid",
      "count": "2",
      "amount": 7810.0,
      "formatted_amount": "Rs 7,810.00"
    },
    "partially_paid": {
      "title": "Partially Paid",
      "count": "0",
      "amount": 0,
      "formatted_amount": "Rs 0.00"
    },
    "unpaid": {
      "title": "Unpaid",
      "count": "1",
      "amount": 501500.0,
      "formatted_amount": "Rs 5,01,500.00"
    }
  },
  "sales_invoices": [
    {
      "id": 4,
      "invoice_no": "SI-250517-001",
      "category": "Lift",
      "invoice_type": "Sales",
      "invoice_date": "17 May 2025",
      "date": "17 May 2025",
      "due_date": "27 May 2025",
      "due": "27 May 2025",
      "amount": 4560.0,
      "formatted_amount": "Rs 4,560.00",
      "status": "Paid",
      "status_color": "green",
      "user_id": 11,
      "order_id": null,
      "order_no": null,
      "quotation_id": null,
      "quotation_no": null,
      "customer_name": "Demo Customer",
      "phone": "",
      "email": "",
      "billing_address": "",
      "delivery_address": "",
      "customer": {
        "name": "Demo Customer",
        "phone": "",
        "email": "",
        "billing_address": "",
        "delivery_address": ""
      },
      "payment_terms": "30 Days",
      "reference_no": "",
      "items": [
        {
          "name": "Lift Item",
          "category": "Lift",
          "total": 4560.0
        }
      ],
      "subtotal": 4560.0,
      "discount": 0.0,
      "tax_percent": 18.0,
      "tax": 0.0,
      "grand_total": 4560.0,
      "amount_paid": 0.0,
      "balance_due": 0.0,
      "notes": "",
      "created_at": "2026-09-17T11:33:50.107760",
      "updated_at": "2026-09-17T11:51:40.930547"
    },
    {
      "id": 1,
      "invoice_no": "INV-260912-0001",
      "category": "Lift",
      "invoice_type": "Sales",
      "invoice_date": "12 Sep 2026",
      "date": "12 Sep 2026",
      "due_date": "12 Oct 2026",
      "due": "12 Oct 2026",
      "amount": 501500.0,
      "formatted_amount": "Rs 5,01,500.00",
      "status": "Unpaid",
      "status_color": "red",
      "user_id": 11,
      "order_id": 1,
      "order_no": "ORD-260912-0001",
      "quotation_id": null,
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
      "reference_no": "REF-SKY-001",
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
      "notes": "Original invoice generated from mobile Create Invoice screen",
      "created_at": "2026-09-17T10:42:28.735129",
      "updated_at": "2026-09-17T12:24:51.557369"
    }
  ],
  "service_invoices": [
    {
      "id": 8,
      "invoice_no": "SV-250517-001",
      "category": "Lift",
      "invoice_type": "Service",
      "invoice_date": "17 May 2025",
      "date": "17 May 2025",
      "due_date": "27 May 2025",
      "due": "27 May 2025",
      "amount": 3250.0,
      "formatted_amount": "Rs 3,250.00",
      "status": "Paid",
      "status_color": "green",
      "user_id": 11,
      "order_id": null,
      "order_no": null,
      "quotation_id": null,
      "quotation_no": null,
      "customer_name": "Demo Customer",
      "phone": "",
      "email": "",
      "billing_address": "",
      "delivery_address": "",
      "customer": {
        "name": "Demo Customer",
        "phone": "",
        "email": "",
        "billing_address": "",
        "delivery_address": ""
      },
      "payment_terms": "30 Days",
      "reference_no": "",
      "items": [
        {
          "name": "Lift Item",
          "category": "Lift",
          "total": 3250.0
        }
      ],
      "subtotal": 3250.0,
      "discount": 0.0,
      "tax_percent": 18.0,
      "tax": 0.0,
      "grand_total": 3250.0,
      "amount_paid": 0.0,
      "balance_due": 0.0,
      "notes": "",
      "created_at": "2026-09-17T11:33:50.107775",
      "updated_at": "2026-09-17T11:51:40.937100"
    }
  ],
  "all_invoices": [
    {
      "id": 8,
      "invoice_no": "SV-250517-001",
      "category": "Lift",
      "invoice_type": "Service",
      "invoice_date": "17 May 2025",
      "date": "17 May 2025",
      "due_date": "27 May 2025",
      "due": "27 May 2025",
      "amount": 3250.0,
      "formatted_amount": "Rs 3,250.00",
      "status": "Paid",
      "status_color": "green",
      "user_id": 11,
      "order_id": null,
      "order_no": null,
      "quotation_id": null,
      "quotation_no": null,
      "customer_name": "Demo Customer",
      "phone": "",
      "email": "",
      "billing_address": "",
      "delivery_address": "",
      "customer": {
        "name": "Demo Customer",
        "phone": "",
        "email": "",
        "billing_address": "",
        "delivery_address": ""
      },
      "payment_terms": "30 Days",
      "reference_no": "",
      "items": [
        {
          "name": "Lift Item",
          "category": "Lift",
          "total": 3250.0
        }
      ],
      "subtotal": 3250.0,
      "discount": 0.0,
      "tax_percent": 18.0,
      "tax": 0.0,
      "grand_total": 3250.0,
      "amount_paid": 0.0,
      "balance_due": 0.0,
      "notes": "",
      "created_at": "2026-09-17T11:33:50.107775",
      "updated_at": "2026-09-17T11:51:40.937100"
    },
    {
      "id": 4,
      "invoice_no": "SI-250517-001",
      "category": "Lift",
      "invoice_type": "Sales",
      "invoice_date": "17 May 2025",
      "date": "17 May 2025",
      "due_date": "27 May 2025",
      "due": "27 May 2025",
      "amount": 4560.0,
      "formatted_amount": "Rs 4,560.00",
      "status": "Paid",
      "status_color": "green",
      "user_id": 11,
      "order_id": null,
      "order_no": null,
      "quotation_id": null,
      "quotation_no": null,
      "customer_name": "Demo Customer",
      "phone": "",
      "email": "",
      "billing_address": "",
      "delivery_address": "",
      "customer": {
        "name": "Demo Customer",
        "phone": "",
        "email": "",
        "billing_address": "",
        "delivery_address": ""
      },
      "payment_terms": "30 Days",
      "reference_no": "",
      "items": [
        {
          "name": "Lift Item",
          "category": "Lift",
          "total": 4560.0
        }
      ],
      "subtotal": 4560.0,
      "discount": 0.0,
      "tax_percent": 18.0,
      "tax": 0.0,
      "grand_total": 4560.0,
      "amount_paid": 0.0,
      "balance_due": 0.0,
      "notes": "",
      "created_at": "2026-09-17T11:33:50.107760",
      "updated_at": "2026-09-17T11:51:40.930547"
    },
    {
      "id": 1,
      "invoice_no": "INV-260912-0001",
      "category": "Lift",
      "invoice_type": "Sales",
      "invoice_date": "12 Sep 2026",
      "date": "12 Sep 2026",
      "due_date": "12 Oct 2026",
      "due": "12 Oct 2026",
      "amount": 501500.0,
      "formatted_amount": "Rs 5,01,500.00",
      "status": "Unpaid",
      "status_color": "red",
      "user_id": 11,
      "order_id": 1,
      "order_no": "ORD-260912-0001",
      "quotation_id": null,
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
      "reference_no": "REF-SKY-001",
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
      "notes": "Original invoice generated from mobile Create Invoice screen",
      "created_at": "2026-09-17T10:42:28.735129",
      "updated_at": "2026-09-17T12:24:51.557369"
    }
  ],
  "count": 3
}

---

## 2. User Sales Invoices (Tab 2: Sales Invoice)

url : (http://192.168.1.59:8000/api/invoices/sales)
method : GET

headers :- 

Authorization: Bearer <user_login_token> (Required)

response :- 

{
  "summary": {
    "total_invoices": {
      "title": "Total Invoice",
      "count": "2",
      "amount": 506060.0,
      "formatted_amount": "Rs 5,06,060.00"
    },
    "paid": {
      "title": "Paid",
      "count": "1",
      "amount": 4560.0,
      "formatted_amount": "Rs 4,560.00"
    },
    "partially_paid": {
      "title": "Partially Paid",
      "count": "0",
      "amount": 0,
      "formatted_amount": "Rs 0.00"
    },
    "unpaid": {
      "title": "Unpaid",
      "count": "1",
      "amount": 501500.0,
      "formatted_amount": "Rs 5,01,500.00"
    }
  },
  "sales_invoices": [
    {
      "id": 4,
      "invoice_no": "SI-250517-001",
      "category": "Lift",
      "invoice_type": "Sales",
      "invoice_date": "17 May 2025",
      "date": "17 May 2025",
      "due_date": "27 May 2025",
      "due": "27 May 2025",
      "amount": 4560.0,
      "formatted_amount": "Rs 4,560.00",
      "status": "Paid",
      "status_color": "green",
      "user_id": 11,
      "order_id": null,
      "order_no": null,
      "quotation_id": null,
      "quotation_no": null,
      "customer_name": "Demo Customer",
      "phone": "",
      "email": "",
      "billing_address": "",
      "delivery_address": "",
      "customer": {
        "name": "Demo Customer",
        "phone": "",
        "email": "",
        "billing_address": "",
        "delivery_address": ""
      },
      "payment_terms": "30 Days",
      "reference_no": "",
      "items": [
        {
          "name": "Lift Item",
          "category": "Lift",
          "total": 4560.0
        }
      ],
      "subtotal": 4560.0,
      "discount": 0.0,
      "tax_percent": 18.0,
      "tax": 0.0,
      "grand_total": 4560.0,
      "amount_paid": 0.0,
      "balance_due": 0.0,
      "notes": "",
      "created_at": "2026-09-17T11:33:50.107760",
      "updated_at": "2026-09-17T11:51:40.930547"
    },
    {
      "id": 1,
      "invoice_no": "INV-260912-0001",
      "category": "Lift",
      "invoice_type": "Sales",
      "invoice_date": "12 Sep 2026",
      "date": "12 Sep 2026",
      "due_date": "12 Oct 2026",
      "due": "12 Oct 2026",
      "amount": 501500.0,
      "formatted_amount": "Rs 5,01,500.00",
      "status": "Unpaid",
      "status_color": "red",
      "user_id": 11,
      "order_id": 1,
      "order_no": "ORD-260912-0001",
      "quotation_id": null,
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
      "reference_no": "REF-SKY-001",
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
      "notes": "Original invoice generated from mobile Create Invoice screen",
      "created_at": "2026-09-17T10:42:28.735129",
      "updated_at": "2026-09-17T12:24:51.557369"
    }
  ],
  "service_invoices": [],
  "all_invoices": [
    {
      "id": 4,
      "invoice_no": "SI-250517-001",
      "category": "Lift",
      "invoice_type": "Sales",
      "invoice_date": "17 May 2025",
      "date": "17 May 2025",
      "due_date": "27 May 2025",
      "due": "27 May 2025",
      "amount": 4560.0,
      "formatted_amount": "Rs 4,560.00",
      "status": "Paid",
      "status_color": "green",
      "user_id": 11,
      "order_id": null,
      "order_no": null,
      "quotation_id": null,
      "quotation_no": null,
      "customer_name": "Demo Customer",
      "phone": "",
      "email": "",
      "billing_address": "",
      "delivery_address": "",
      "customer": {
        "name": "Demo Customer",
        "phone": "",
        "email": "",
        "billing_address": "",
        "delivery_address": ""
      },
      "payment_terms": "30 Days",
      "reference_no": "",
      "items": [
        {
          "name": "Lift Item",
          "category": "Lift",
          "total": 4560.0
        }
      ],
      "subtotal": 4560.0,
      "discount": 0.0,
      "tax_percent": 18.0,
      "tax": 0.0,
      "grand_total": 4560.0,
      "amount_paid": 0.0,
      "balance_due": 0.0,
      "notes": "",
      "created_at": "2026-09-17T11:33:50.107760",
      "updated_at": "2026-09-17T11:51:40.930547"
    },
    {
      "id": 1,
      "invoice_no": "INV-260912-0001",
      "category": "Lift",
      "invoice_type": "Sales",
      "invoice_date": "12 Sep 2026",
      "date": "12 Sep 2026",
      "due_date": "12 Oct 2026",
      "due": "12 Oct 2026",
      "amount": 501500.0,
      "formatted_amount": "Rs 5,01,500.00",
      "status": "Unpaid",
      "status_color": "red",
      "user_id": 11,
      "order_id": 1,
      "order_no": "ORD-260912-0001",
      "quotation_id": null,
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
      "reference_no": "REF-SKY-001",
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
      "notes": "Original invoice generated from mobile Create Invoice screen",
      "created_at": "2026-09-17T10:42:28.735129",
      "updated_at": "2026-09-17T12:24:51.557369"
    }
  ],
  "count": 2
}

---

## 3. User Service Invoices (Tab 3: Service Invoice)

url : (http://192.168.1.59:8000/api/invoices/service)
method : GET

headers :- 

Authorization: Bearer <user_login_token> (Required)

response :- 

{
  "summary": {
    "total_invoices": {
      "title": "Total Invoice",
      "count": "1",
      "amount": 3250.0,
      "formatted_amount": "Rs 3,250.00"
    },
    "paid": {
      "title": "Paid",
      "count": "1",
      "amount": 3250.0,
      "formatted_amount": "Rs 3,250.00"
    },
    "partially_paid": {
      "title": "Partially Paid",
      "count": "0",
      "amount": 0,
      "formatted_amount": "Rs 0.00"
    },
    "unpaid": {
      "title": "Unpaid",
      "count": "0",
      "amount": 0,
      "formatted_amount": "Rs 0.00"
    }
  },
  "sales_invoices": [],
  "service_invoices": [
    {
      "id": 8,
      "invoice_no": "SV-250517-001",
      "category": "Lift",
      "invoice_type": "Service",
      "invoice_date": "17 May 2025",
      "date": "17 May 2025",
      "due_date": "27 May 2025",
      "due": "27 May 2025",
      "amount": 3250.0,
      "formatted_amount": "Rs 3,250.00",
      "status": "Paid",
      "status_color": "green",
      "user_id": 11,
      "order_id": null,
      "order_no": null,
      "quotation_id": null,
      "quotation_no": null,
      "customer_name": "Demo Customer",
      "phone": "",
      "email": "",
      "billing_address": "",
      "delivery_address": "",
      "customer": {
        "name": "Demo Customer",
        "phone": "",
        "email": "",
        "billing_address": "",
        "delivery_address": ""
      },
      "payment_terms": "30 Days",
      "reference_no": "",
      "items": [
        {
          "name": "Lift Item",
          "category": "Lift",
          "total": 3250.0
        }
      ],
      "subtotal": 3250.0,
      "discount": 0.0,
      "tax_percent": 18.0,
      "tax": 0.0,
      "grand_total": 3250.0,
      "amount_paid": 0.0,
      "balance_due": 0.0,
      "notes": "",
      "created_at": "2026-09-17T11:33:50.107775",
      "updated_at": "2026-09-17T11:51:40.937100"
    }
  ],
  "all_invoices": [
    {
      "id": 8,
      "invoice_no": "SV-250517-001",
      "category": "Lift",
      "invoice_type": "Service",
      "invoice_date": "17 May 2025",
      "date": "17 May 2025",
      "due_date": "27 May 2025",
      "due": "27 May 2025",
      "amount": 3250.0,
      "formatted_amount": "Rs 3,250.00",
      "status": "Paid",
      "status_color": "green",
      "user_id": 11,
      "order_id": null,
      "order_no": null,
      "quotation_id": null,
      "quotation_no": null,
      "customer_name": "Demo Customer",
      "phone": "",
      "email": "",
      "billing_address": "",
      "delivery_address": "",
      "customer": {
        "name": "Demo Customer",
        "phone": "",
        "email": "",
        "billing_address": "",
        "delivery_address": ""
      },
      "payment_terms": "30 Days",
      "reference_no": "",
      "items": [
        {
          "name": "Lift Item",
          "category": "Lift",
          "total": 3250.0
        }
      ],
      "subtotal": 3250.0,
      "discount": 0.0,
      "tax_percent": 18.0,
      "tax": 0.0,
      "grand_total": 3250.0,
      "amount_paid": 0.0,
      "balance_due": 0.0,
      "notes": "",
      "created_at": "2026-09-17T11:33:50.107775",
      "updated_at": "2026-09-17T11:51:40.937100"
    }
  ],
  "count": 1
}

---

## 4. Single Invoice Details (On Tapping Invoice / Action Icon)

url : (http://192.168.1.59:8000/api/invoices/SI-250517-001)
method : GET

(Also supports ID like http://192.168.1.59:8000/api/invoices/4)

headers :- 

Authorization: Bearer <user_login_token> (Required)

response :- 

{
  "id": 4,
  "invoice_no": "SI-250517-001",
  "category": "Lift",
  "invoice_type": "Sales",
  "invoice_date": "17 May 2025",
  "date": "17 May 2025",
  "due_date": "27 May 2025",
  "due": "27 May 2025",
  "amount": 4560.0,
  "formatted_amount": "Rs 4,560.00",
  "status": "Paid",
  "status_color": "green",
  "user_id": 11,
  "order_id": null,
  "order_no": null,
  "quotation_id": null,
  "quotation_no": null,
  "customer_name": "Demo Customer",
  "phone": "",
  "email": "",
  "billing_address": "",
  "delivery_address": "",
  "customer": {
    "name": "Demo Customer",
    "phone": "",
    "email": "",
    "billing_address": "",
    "delivery_address": ""
  },
  "payment_terms": "30 Days",
  "reference_no": "",
  "items": [
    {
      "name": "Lift Item",
      "category": "Lift",
      "total": 4560.0
    }
  ],
  "subtotal": 4560.0,
  "discount": 0.0,
  "tax_percent": 18.0,
  "tax": 0.0,
  "grand_total": 4560.0,
  "amount_paid": 0.0,
  "balance_due": 0.0,
  "notes": "",
  "created_at": "2026-09-17T11:33:50.107760",
  "updated_at": "2026-09-17T11:51:40.930547"
}
