# Invoice API Documentation (Create Invoice Screen)

## 1. Get Next Auto-Generated Invoice Number

url : (http://192.168.1.59:8000/api/invoices/next-invoice-number)
method : GET

*(Also supports `http://192.168.1.59:8000/api/invoices/next-number`)*

params :- 

(None)

response :- 

```json
{
  "invoice_no": "INV-260912-0001"
}
```

---

## 2. Order Dropdown (Select Order No. to Auto-Fill Details & Items)

url : (http://192.168.1.59:8000/api/invoices/orders)
method : GET

params :- 

- `search` (optional): Filter by order no, customer name, mobile
- `status` (optional): Filter by status (e.g. `Pending`, `Confirmed`, etc.)

response :- 

```json
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
  ]
}
```

---

## 3. Customer List (Select Customer Modal)

url : (http://192.168.1.59:8000/api/invoices/customers)
method : GET

params :- 

- `search` (optional): Search by customer name, phone, email

response :- 

```json
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
```

---

## 4. Create / Save Invoice

url : (http://192.168.1.59:8000/api/invoices/create)
method : POST

*(Also supports `http://192.168.1.59:8000/api/invoices` and `http://192.168.1.59:8000/api/invoices/add`)*

### JSON Body (Matches the Mobile App Screen Exactly):

```json
{
  "invoice_no": "INV-260912-0001",
  "invoice_date": "12 Sep 2026",
  "due_date": "12 Oct 2026",
  "order_no": "ORD-260912-0001",
  "payment_terms": "30 Days",
  "reference_no": "REF-INV-001",
  "customer_name": "Skyline Enterprises",
  "phone": "+91 9876543210",
  "email": "contact@skyline.com",
  "billing_address": "45 Industrial Area, Phase 2, New Delhi",
  "items": [
    {
      "name": "G+2 Automatic Passenger Lift",
      "category": "Passenger Lift",
      "code": "LIFT001",
      "qty": 1,
      "rate": 450000.0,
      "discount": 25000.0,
      "tax_percent": 18.0,
      "total": 450000.0
    }
  ],
  "subtotal": 450000.0,
  "discount": 25000.0,
  "tax": 76500.0,
  "grand_total": 501500.0,
  "notes": "Generated from mobile Create Invoice screen",
  "status": "Unpaid"
}
```

*(Note: `subtotal`, `discount`, `tax`, and `grand_total` are auto-computed if omitted)*

response :- 

```json
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
    "notes": "Generated from mobile Create Invoice screen",
    "status": "Unpaid",
    "created_at": "2026-09-17T10:27:10.851043",
    "updated_at": "2026-09-17T10:27:10.851049"
  }
}
```

---

## 5. List All Invoices

url : (http://192.168.1.59:8000/api/invoices)
method : GET

params :- 

- `search` (optional): Global search across invoice no, customer name, order no, reference no, phone
- `customer_name` (optional): Filter by customer name
- `status` (optional): Filter by status (`Unpaid`, `Paid`, `Partially Paid`, `Overdue`, `Cancelled`)
- `order_no` (optional): Filter by order no
- `payment_terms` (optional): Filter by payment terms

response :- 

```json
{
  "count": 1,
  "results": [
    {
      "id": 1,
      "invoice_no": "INV-260912-0001",
      "invoice_date": "12 Sep 2026",
      "due_date": "12 Oct 2026",
      "order_no": "ORD-260912-0001",
      "customer_name": "Skyline Enterprises",
      "phone": "+91 9876543210",
      "email": "contact@skyline.com",
      "billing_address": "45 Industrial Area, Phase 2, New Delhi",
      "payment_terms": "30 Days",
      "reference_no": "REF-INV-001",
      "items": [
        {
          "name": "G+2 Automatic Passenger Lift",
          "qty": 1.0,
          "rate": 450000.0,
          "discount": 25000.0,
          "tax_percent": 18.0,
          "total": 450000.0
        }
      ],
      "subtotal": 450000.0,
      "discount": 25000.0,
      "tax": 76500.0,
      "grand_total": 501500.0,
      "amount_paid": 0.0,
      "balance_due": 501500.0,
      "status": "Unpaid",
      "created_at": "2026-09-17T10:27:10.851043",
      "updated_at": "2026-09-17T10:27:10.851049"
    }
  ]
}
```

---

## 6. Get Single Invoice Details

url : (http://192.168.1.59:8000/api/invoices/1)
method : GET

*(Also supports lookup by string `invoice_no`: `http://192.168.1.59:8000/api/invoices/INV-260912-0001`)*

params :- 

(None)

response :- 

```json
{
  "id": 1,
  "invoice_no": "INV-260912-0001",
  "invoice_date": "12 Sep 2026",
  "due_date": "12 Oct 2026",
  "order_id": 1,
  "order_no": "ORD-260912-0001",
  "customer_name": "Skyline Enterprises",
  "phone": "+91 9876543210",
  "email": "contact@skyline.com",
  "billing_address": "45 Industrial Area, Phase 2, New Delhi",
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
      "total": 450000.0
    }
  ],
  "subtotal": 450000.0,
  "discount": 25000.0,
  "tax_percent": 18.0,
  "tax": 76500.0,
  "grand_total": 501500.0,
  "amount_paid": 0.0,
  "balance_due": 501500.0,
  "notes": "Generated from mobile Create Invoice screen",
  "status": "Unpaid"
}
```

---

## 7. Update Invoice

url : (http://192.168.1.59:8000/api/invoices/1)
method : PUT

*(Also supports `PATCH`)*

params :- 

```json
{
  "notes": "Payment expected by 12 Oct 2026",
  "reference_no": "REF-INV-001-MODIFIED"
}
```

response :- 

```json
{
  "message": "Invoice 'INV-260912-0001' updated successfully",
  "invoice": {
    "id": 1,
    "invoice_no": "INV-260912-0001",
    "reference_no": "REF-INV-001-MODIFIED",
    "notes": "Payment expected by 12 Oct 2026"
  }
}
```

---

## 8. Quick Status Update

url : (http://192.168.1.59:8000/api/invoices/1/status)
method : PATCH

params :- 

```json
{
  "status": "Paid"
}
```

response :- 

```json
{
  "message": "Invoice 'INV-260912-0001' status updated to 'Paid'",
  "invoice": {
    "id": 1,
    "invoice_no": "INV-260912-0001",
    "status": "Paid",
    "amount_paid": 501500.0,
    "balance_due": 0.0
  }
}
```

---

## 9. Delete Invoice

url : (http://192.168.1.59:8000/api/invoices/1)
method : DELETE

params :- 

(None)

response :- 

```json
{
  "message": "Invoice 'INV-260912-0001' deleted successfully"
}
```
