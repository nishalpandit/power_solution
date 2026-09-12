# Order API Documentation

## 1. Get Next Auto-Generated Order Number

url : (http://192.168.1.59:8000/api/orders/next-order-number)
method : GET

params :- 

(None)

response :- 

{
  "order_no": "ORD-260912-0001"
}

---

## 2. Quotation Dropdown (Select Quotation)

url : (http://192.168.1.59:8000/api/orders/quotations)
method : GET

params :- 

(None)

response :- 

{
  "count": 1,
  "results": [
    {
      "id": "QTN-250517-0001",
      "quotation_id": 1,
      "quotation_no": "QTN-250517-0001",
      "date": "17 May 2025",
      "customer": "Skyline Enterprises",
      "mobile": "+91 9876543210",
      "email": "contact@skyline.com",
      "billingAddress": "45 Industrial Area, Phase 2, New Delhi",
      "deliveryAddress": "45 Industrial Area, Phase 2, New Delhi",
      "subtotal": 450000.0,
      "discount": 25000.0,
      "tax": 76500.0,
      "taxable_amount": 425000.0,
      "grandTotal": 501500.0,
      "status": "Sent",
      "items": [
        {
          "id": "LIFT001",
          "name": "G+2 Automatic Passenger Lift",
          "type": "Lift",
          "category": "Passenger Lift",
          "qty": 1,
          "price": 450000.0,
          "total": 450000.0,
          "specifications": {
            "Capacity": "4-6 Passenger",
            "Rated Load": "320 KG",
            "Speed": "0.65 - 1 m/s",
            "Floor": "G+2",
            "Stops": "3",
            "Door Type": "Automatic",
            "Drive": "VVVF / VFD",
            "Power Supply": "415V / 3 Phase / 50Hz",
            "Cabin Finish": "SS"
          }
        }
      ]
    }
  ]
}

---

## 3. Create Order / Save Draft

url : (http://192.168.1.59:8000/api/orders)
method : POST

params :- 

order_no:ORD-260912-0001
quotation_id:QTN-250517-0001
order_date:17 May 2025
delivery_date:31 May 2025
order_status:Pending
customer:{"name":"Skyline Enterprises","mobile":"9876543210","email":"contact@skyline.com","billing_address":"45 Industrial Area, Phase 2, New Delhi","delivery_address":"45 Industrial Area, Phase 2, New Delhi"}
subtotal:450000.0
discount:25000.0
tax:76500.0
grand_total:501500.0
advance_paid:50000.0
balance_amount:451500.0
payment_status:Partially Paid
payment_mode:Bank Transfer
transaction_no:TXN-BANK-10023
payment_date:17 May 2025
special_instructions:Handle lift components with care during transit
internal_notes:Priority VIP client
terms_accepted:true

response :- 

{
  "message": "Order 'ORD-260912-0001' created successfully",
  "order": {
    "id": 1,
    "order_no": "ORD-260912-0001",
    "order_date": "17 May 2025",
    "delivery_date": "31 May 2025",
    "order_status": "Pending",
    "quotation_id": 1,
    "quotation_no": "QTN-250517-0001",
    "customer_name": "Skyline Enterprises",
    "mobile": "9876543210",
    "email": "contact@skyline.com",
    "billing_address": "45 Industrial Area, Phase 2, New Delhi",
    "delivery_address": "45 Industrial Area, Phase 2, New Delhi",
    "customer": {
      "name": "Skyline Enterprises",
      "mobile": "9876543210",
      "email": "contact@skyline.com",
      "billing_address": "45 Industrial Area, Phase 2, New Delhi",
      "delivery_address": "45 Industrial Area, Phase 2, New Delhi"
    },
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
    "discount": 25000.0,
    "taxable_amount": 425000.0,
    "tax": 76500.0,
    "grand_total": 501500.0,
    "advance_paid": 50000.0,
    "balance_amount": 451500.0,
    "special_instructions": "Handle lift components with care during transit",
    "payment_status": "Partially Paid",
    "payment_mode": "Bank Transfer",
    "transaction_no": "TXN-BANK-10023",
    "payment_date": "17 May 2025",
    "internal_notes": "Priority VIP client",
    "terms_accepted": true,
    "created_at": "2026-09-12T08:32:12.331495",
    "updated_at": "2026-09-12T08:32:12.331500"
  }
}

---

## 4. List All Orders

url : (http://192.168.1.59:8000/api/orders)
method : GET

params :- 

(None)

response :- 

{
  "count": 1,
  "results": [
    {
      "id": 1,
      "order_no": "ORD-260912-0001",
      "order_date": "17 May 2025",
      "delivery_date": "31 May 2025",
      "order_status": "Pending",
      "quotation_id": 1,
      "quotation_no": "QTN-250517-0001",
      "customer_name": "Skyline Enterprises",
      "mobile": "9876543210",
      "email": "contact@skyline.com",
      "billing_address": "45 Industrial Area, Phase 2, New Delhi",
      "delivery_address": "45 Industrial Area, Phase 2, New Delhi",
      "subtotal": 450000.0,
      "discount": 25000.0,
      "taxable_amount": 425000.0,
      "tax": 76500.0,
      "grand_total": 501500.0,
      "advance_paid": 50000.0,
      "balance_amount": 451500.0,
      "payment_status": "Partially Paid",
      "payment_mode": "Bank Transfer",
      "transaction_no": "TXN-BANK-10023",
      "payment_date": "17 May 2025",
      "internal_notes": "Priority VIP client",
      "terms_accepted": true,
      "created_at": "2026-09-12T08:32:12.331495",
      "updated_at": "2026-09-12T08:32:12.331500"
    }
  ]
}

---

## 5. Get Single Order Details

url : (http://192.168.1.59:8000/api/orders/1)
method : GET

params :- 

(None)

response :- 

{
  "id": 1,
  "order_no": "ORD-260912-0001",
  "order_date": "17 May 2025",
  "delivery_date": "31 May 2025",
  "order_status": "Pending",
  "quotation_id": 1,
  "quotation_no": "QTN-250517-0001",
  "customer_name": "Skyline Enterprises",
  "mobile": "9876543210",
  "email": "contact@skyline.com",
  "billing_address": "45 Industrial Area, Phase 2, New Delhi",
  "delivery_address": "45 Industrial Area, Phase 2, New Delhi",
  "customer": {
    "name": "Skyline Enterprises",
    "mobile": "9876543210",
    "email": "contact@skyline.com",
    "billing_address": "45 Industrial Area, Phase 2, New Delhi",
    "delivery_address": "45 Industrial Area, Phase 2, New Delhi"
  },
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
        "Drive": "VVVF / VFD",
        "Power Supply": "415V / 3 Phase / 50Hz",
        "Cabin Finish": "SS"
      },
      "quantity": 1.0,
      "unit_price": 450000.0,
      "total_price": 450000.0
    }
  ],
  "subtotal": 450000.0,
  "discount": 25000.0,
  "taxable_amount": 425000.0,
  "tax": 76500.0,
  "grand_total": 501500.0,
  "advance_paid": 50000.0,
  "balance_amount": 451500.0,
  "special_instructions": "Handle lift components with care during transit",
  "payment_status": "Partially Paid",
  "payment_mode": "Bank Transfer",
  "transaction_no": "TXN-BANK-10023",
  "payment_date": "17 May 2025",
  "internal_notes": "Priority VIP client",
  "terms_accepted": true,
  "created_at": "2026-09-12T08:32:12.331495",
  "updated_at": "2026-09-12T08:32:12.331500"
}

---

## 6. Update Order Record

url : (http://192.168.1.59:8000/api/orders/1)
method : PUT

params :- 

order_status:Confirmed
advance_paid:150000.0
payment_status:Partially Paid
internal_notes:Client transferred 1.5L advance via RTGS

response :- 

{
  "message": "Order 'ORD-260912-0001' updated successfully",
  "order": {
    "id": 1,
    "order_no": "ORD-260912-0001",
    "order_status": "Confirmed",
    "advance_paid": 150000.0,
    "balance_amount": 351500.0,
    "payment_status": "Partially Paid",
    "internal_notes": "Client transferred 1.5L advance via RTGS",
    "updated_at": "2026-09-12T08:35:00.000000"
  }
}

---

## 7. Delete Order Record

url : (http://192.168.1.59:8000/api/orders/1)
method : DELETE

params :- 

(None)

response :- 

{
  "message": "Order 'ORD-260912-0001' deleted successfully"
}
