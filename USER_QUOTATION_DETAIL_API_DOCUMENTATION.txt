# User Quotation Detail Screen API Documentation

Bearer token is compulsory for all endpoints.
The user is automatically identified from the Bearer token.
The backend returns quotations belonging to the logged-in user.

Unauthorized response without token:
HTTP 401 Unauthorized
{
  "detail": "Bearer token is compulsory. Please provide Authorization: Bearer <token>"
}

---

## 1. Get Single Quotation Details (For UserQuotationDetailScreen)

url : (http://192.168.1.54:8000/api/quotations/QTN-250517-0001)
method : GET

(Also supports http://192.168.1.54:8000/api/quotations/detail/QTN-250517-0001 and primary key ID)

headers :- 

Authorization: Bearer <user_login_token> (Required)

response (Logged in as User 11 - Rajesh Kumar / Skyline Enterprises) :- 

{
  "id": "QTN-250517-0001",
  "db_id": 8,
  "quotation_id": "QTN-250517-0001",
  "quotation_no": "QTN-250517-0001",
  "status": "Approved",
  "statusColor": "green",
  "status_color": "green",
  "status_color_hex": "#10B981",
  "icon": "elevator",
  "iconColor": "blue",
  "icon_color": "blue",
  "category": "Passenger Lift",
  "date": "17 May 2025",
  "quotation_date": "17 May 2025",
  "time": "10:30 AM",
  "quotation_time": "10:30 AM",
  "validTill": "31 May 2025",
  "valid_till": "31 May 2025",
  "amount": "Rs 4,56,000.00",
  "grand_total": 456000.0,
  "formatted_amount": "Rs 4,56,000.00",
  "company": {
    "company_name": "M/s. POWER SOLUTION.COM ENTERPRISES",
    "gstn": "20EGHPS4942E1ZH",
    "email": "POWERSOLUTIONDG3@GMAIL.COM",
    "iso_certificate": "ISO 9001:2015 QMS-25111206",
    "electric_license_no": "JH/EC/5382",
    "registered_address": "SOLANKI , SINGHMORE, HATIA ,RANCHI JHARKHAND PIN CODE 834003",
    "representative": "Mr./Ms. ________________"
  },
  "customer": {
    "name": "Rajesh Kumar",
    "phone": "+91 98765 43210",
    "email": "contact@skyline.com",
    "address": "123, Green Street, New Delhi, Delhi - 110016"
  },
  "customer_name": "Rajesh Kumar",
  "customer_phone": "+91 98765 43210",
  "customer_email": "contact@skyline.com",
  "customer_address": "123, Green Street, New Delhi, Delhi - 110016",
  "items": [
    {
      "item": "Passenger Lift",
      "description": "(6 Seater)",
      "desc": "(6 Seater)",
      "qty": "1",
      "quantity": 1.0,
      "rate": 400000.0,
      "unit_price": 400000.0,
      "formatted_rate": "Rs 4,00,000.00",
      "total": "Rs 4,00,000.00",
      "formatted_total": "Rs 4,00,000.00",
      "amount": 400000.0
    },
    {
      "item": "Installation",
      "description": "Commisioning",
      "desc": "Commisioning",
      "qty": "1",
      "quantity": 1.0,
      "rate": 40000.0,
      "unit_price": 40000.0,
      "formatted_rate": "Rs 40,000.00",
      "total": "Rs 40,000.00",
      "formatted_total": "Rs 40,000.00",
      "amount": 40000.0
    },
    {
      "item": "AMC (1 Year)",
      "description": "Maintenance",
      "desc": "Maintenance",
      "qty": "1",
      "quantity": 1.0,
      "rate": 16000.0,
      "unit_price": 16000.0,
      "formatted_rate": "Rs 16,000.00",
      "total": "Rs 16,000.00",
      "formatted_total": "Rs 16,000.00",
      "amount": 16000.0
    }
  ],
  "pricing_summary": {
    "subtotal": 456000.0,
    "formatted_subtotal": "Rs 4,56,000.00",
    "tax_type": "GST 18%",
    "tax_rate": 0.18,
    "tax_amount": 0.0,
    "formatted_tax": "Rs 0.00",
    "discount_type": "Flat",
    "discount_amount": 0.0,
    "formatted_discount": "Rs 0.00",
    "grand_total": 456000.0,
    "formatted_grand_total": "Rs 4,56,000.00"
  },
  "terms_and_conditions": [
    "This quotation is valid till the above mentioned validity date.",
    "50% advance required before installation.",
    "Delivery & Installation time: 7-10 working days.",
    "Warranty as per company policy."
  ],
  "terms": "This quotation is valid till the above mentioned validity date.\n50% advance required before installation.\nDelivery & Installation time: 7-10 working days.\nWarranty as per company policy.",
  "representation": "Represented by Mr./Ms. ________________,",
  "actions": {
    "download_pdf_url": "http://192.168.1.54:8000/api/quotations/QTN-250517-0001/pdf",
    "share_url": "http://192.168.1.54:8000/api/quotations/QTN-250517-0001/share"
  },
  "download_pdf_url": "http://192.168.1.54:8000/api/quotations/QTN-250517-0001/pdf",
  "share_url": "http://192.168.1.54:8000/api/quotations/QTN-250517-0001/share",
  "user_id": 11,
  "created_at": "2026-09-18T07:35:42.077475",
  "updated_at": "2026-09-18T07:35:42.077478"
}

---

## 2. User Isolation Example (Logged in as User 12 - Metro Builders)

When a different user logs in with their own token, they see ONLY their own quotation:

url : (http://192.168.1.54:8000/api/quotations/QTN-METRO-0001)
method : GET

headers :- 

Authorization: Bearer <user12_login_token> (Required)

response :- 

{
  "id": "QTN-METRO-0001",
  "db_id": 9,
  "quotation_id": "QTN-METRO-0001",
  "quotation_no": "QTN-METRO-0001",
  "status": "Sent",
  "statusColor": "blue",
  "status_color": "blue",
  "status_color_hex": "#3B82F6",
  "icon": "bolt",
  "iconColor": "blue",
  "icon_color": "blue",
  "category": "Generator",
  "date": "15 Sep 2026",
  "quotation_date": "15 Sep 2026",
  "time": "02:15 PM",
  "quotation_time": "02:15 PM",
  "validTill": "15 Oct 2026",
  "valid_till": "15 Oct 2026",
  "amount": "Rs 75,000.00",
  "grand_total": 75000.0,
  "formatted_amount": "Rs 75,000.00",
  "company": {
    "company_name": "M/s. POWER SOLUTION.COM ENTERPRISES",
    "gstn": "20EGHPS4942E1ZH",
    "email": "POWERSOLUTIONDG3@GMAIL.COM",
    "iso_certificate": "ISO 9001:2015 QMS-25111206",
    "electric_license_no": "JH/EC/5382",
    "registered_address": "SOLANKI , SINGHMORE, HATIA ,RANCHI JHARKHAND PIN CODE 834003",
    "representative": "Mr./Ms. ________________"
  },
  "customer": {
    "name": "Metro Builders",
    "phone": "+91 9123456780",
    "email": "user2@example.com",
    "address": "45 Construction Complex, Sector 62, Noida"
  },
  "customer_name": "Metro Builders",
  "customer_phone": "+91 9123456780",
  "customer_email": "user2@example.com",
  "customer_address": "45 Construction Complex, Sector 62, Noida",
  "items": [
    {
      "item": "Silent Diesel Generator 125 KVA",
      "description": "Heavy Duty Commercial Generator",
      "desc": "Heavy Duty Commercial Generator",
      "qty": "1",
      "quantity": 1.0,
      "rate": 75000.0,
      "unit_price": 75000.0,
      "formatted_rate": "Rs 75,000.00",
      "total": "Rs 75,000.00",
      "formatted_total": "Rs 75,000.00",
      "amount": 75000.0
    }
  ],
  "pricing_summary": {
    "subtotal": 75000.0,
    "formatted_subtotal": "Rs 75,000.00",
    "tax_type": "GST 18%",
    "tax_rate": 0.18,
    "tax_amount": 0.0,
    "formatted_tax": "Rs 0.00",
    "discount_type": "Flat",
    "discount_amount": 0.0,
    "formatted_discount": "Rs 0.00",
    "grand_total": 75000.0,
    "formatted_grand_total": "Rs 75,000.00"
  },
  "terms_and_conditions": [
    "This quotation is valid till the above mentioned validity date.",
    "Warranty 1 Year.",
    "Payment 100% on delivery."
  ],
  "terms": "This quotation is valid till the above mentioned validity date.\nWarranty 1 Year.\nPayment 100% on delivery.",
  "representation": "Represented by Mr./Ms. ________________,",
  "actions": {
    "download_pdf_url": "http://192.168.1.54:8000/api/quotations/QTN-METRO-0001/pdf",
    "share_url": "http://192.168.1.54:8000/api/quotations/QTN-METRO-0001/share"
  },
  "download_pdf_url": "http://192.168.1.54:8000/api/quotations/QTN-METRO-0001/pdf",
  "share_url": "http://192.168.1.54:8000/api/quotations/QTN-METRO-0001/share",
  "user_id": 12,
  "created_at": "2026-09-18T07:35:42.077479",
  "updated_at": "2026-09-18T07:35:42.077480"
}

---

## 3. Cross-User Security Check (HTTP 403 Forbidden)

If User 7 or User 12 attempts to access User 11 quotation (QTN-250517-0001) by ID:

url : (http://192.168.1.54:8000/api/quotations/QTN-250517-0001)
method : GET

headers :- 

Authorization: Bearer <user7_login_token> (Required)

response :- 

HTTP 403 Forbidden
{
  "detail": "You do not have permission to view this quotation"
}

---

## 4. User Quotation Dashboard / Listing (Cards + Quotations Array)

url : (http://192.168.1.54:8000/api/quotations/dashboard)
method : GET

(Also supports http://192.168.1.54:8000/api/quotations/user-dashboard)

headers :- 

Authorization: Bearer <user7_login_token> (Required)

response (Logged in as User 11 - Rajesh Kumar / Skyline Enterprises - strictly 5 quotations) :- 

{
  "summary": {
    "total_quotations": {
      "title": "Total Quotations",
      "count": "5",
      "amount": 2462000.0,
      "formatted_amount": "Rs 24,62,000.00"
    },
    "approved": {
      "title": "Approved",
      "count": "2",
      "amount": 957500.0,
      "formatted_amount": "Rs 9,57,500.00"
    },
    "sent": {
      "title": "Sent",
      "count": "3",
      "amount": 1504500.0,
      "formatted_amount": "Rs 15,04,500.00"
    },
    "pending": {
      "title": "Pending",
      "count": "0",
      "amount": 0,
      "formatted_amount": "Rs 0.00"
    }
  },
  "quotations": [
    {
      "id": "QTN-250517-0001",
      "db_id": 8,
      "quotation_id": "QTN-250517-0001",
      "quotation_no": "QTN-250517-0001",
      "status": "Approved",
      "statusColor": "green",
      "status_color": "green",
      "status_color_hex": "#10B981",
      "icon": "elevator",
      "iconColor": "blue",
      "icon_color": "blue",
      "category": "Passenger Lift",
      "date": "17 May 2025",
      "quotation_date": "17 May 2025",
      "time": "10:30 AM",
      "quotation_time": "10:30 AM",
      "validTill": "31 May 2025",
      "valid_till": "31 May 2025",
      "amount": "Rs 4,56,000.00",
      "grand_total": 456000.0,
      "formatted_amount": "Rs 4,56,000.00",
      "company": {
        "company_name": "M/s. POWER SOLUTION.COM ENTERPRISES",
        "gstn": "20EGHPS4942E1ZH",
        "email": "POWERSOLUTIONDG3@GMAIL.COM",
        "iso_certificate": "ISO 9001:2015 QMS-25111206",
        "electric_license_no": "JH/EC/5382",
        "registered_address": "SOLANKI , SINGHMORE, HATIA ,RANCHI JHARKHAND PIN CODE 834003",
        "representative": "Mr./Ms. ________________"
      },
      "customer": {
        "name": "Rajesh Kumar",
        "phone": "+91 98765 43210",
        "email": "contact@skyline.com",
        "address": "123, Green Street, New Delhi, Delhi - 110016"
      },
      "customer_name": "Rajesh Kumar",
      "customer_phone": "+91 98765 43210",
      "customer_email": "contact@skyline.com",
      "customer_address": "123, Green Street, New Delhi, Delhi - 110016",
      "items": [
        {
          "item": "Passenger Lift",
          "description": "(6 Seater)",
          "desc": "(6 Seater)",
          "qty": "1",
          "quantity": 1.0,
          "rate": 400000.0,
          "unit_price": 400000.0,
          "formatted_rate": "Rs 4,00,000.00",
          "total": "Rs 4,00,000.00",
          "formatted_total": "Rs 4,00,000.00",
          "amount": 400000.0
        },
        {
          "item": "Installation",
          "description": "Commisioning",
          "desc": "Commisioning",
          "qty": "1",
          "quantity": 1.0,
          "rate": 40000.0,
          "unit_price": 40000.0,
          "formatted_rate": "Rs 40,000.00",
          "total": "Rs 40,000.00",
          "formatted_total": "Rs 40,000.00",
          "amount": 40000.0
        },
        {
          "item": "AMC (1 Year)",
          "description": "Maintenance",
          "desc": "Maintenance",
          "qty": "1",
          "quantity": 1.0,
          "rate": 16000.0,
          "unit_price": 16000.0,
          "formatted_rate": "Rs 16,000.00",
          "total": "Rs 16,000.00",
          "formatted_total": "Rs 16,000.00",
          "amount": 16000.0
        }
      ],
      "pricing_summary": {
        "subtotal": 456000.0,
        "formatted_subtotal": "Rs 4,56,000.00",
        "tax_type": "GST 18%",
        "tax_rate": 0.18,
        "tax_amount": 0.0,
        "formatted_tax": "Rs 0.00",
        "discount_type": "Flat",
        "discount_amount": 0.0,
        "formatted_discount": "Rs 0.00",
        "grand_total": 456000.0,
        "formatted_grand_total": "Rs 4,56,000.00"
      },
      "terms_and_conditions": [
        "This quotation is valid till the above mentioned validity date.",
        "50% advance required before installation.",
        "Delivery & Installation time: 7-10 working days.",
        "Warranty as per company policy."
      ],
      "terms": "This quotation is valid till the above mentioned validity date.\n50% advance required before installation.\nDelivery & Installation time: 7-10 working days.\nWarranty as per company policy.",
      "representation": "Represented by Mr./Ms. ________________,",
      "actions": {
        "download_pdf_url": "http://192.168.1.54:8000/api/quotations/QTN-250517-0001/pdf",
        "share_url": "http://192.168.1.54:8000/api/quotations/QTN-250517-0001/share"
      },
      "download_pdf_url": "http://192.168.1.54:8000/api/quotations/QTN-250517-0001/pdf",
      "share_url": "http://192.168.1.54:8000/api/quotations/QTN-250517-0001/share",
      "user_id": 11,
      "created_at": "2026-09-18T07:35:42.077475",
      "updated_at": "2026-09-18T07:35:42.077478"
    },
    {
      "id": "QTN-260910-0002",
      "db_id": 5,
      "quotation_id": "QTN-260910-0002",
      "quotation_no": "QTN-260910-0002",
      "status": "Approved",
      "statusColor": "green",
      "status_color": "green",
      "status_color_hex": "#10B981",
      "icon": "elevator",
      "iconColor": "blue",
      "icon_color": "blue",
      "category": "Lift",
      "date": "17 May 2025",
      "quotation_date": "17 May 2025",
      "time": "10:30 AM",
      "quotation_time": "10:30 AM",
      "validTill": "31 May 2025",
      "valid_till": "31 May 2025",
      "amount": "Rs 5,01,500.00",
      "grand_total": 501500.0,
      "formatted_amount": "Rs 5,01,500.00",
      "company": {
        "company_name": "M/s. POWER SOLUTION.COM ENTERPRISES",
        "gstn": "20EGHPS4942E1ZH",
        "email": "POWERSOLUTIONDG3@GMAIL.COM",
        "iso_certificate": "ISO 9001:2015 QMS-25111206",
        "electric_license_no": "JH/EC/5382",
        "registered_address": "SOLANKI , SINGHMORE, HATIA ,RANCHI JHARKHAND PIN CODE 834003",
        "representative": "Mr./Ms. ________________"
      },
      "customer": {
        "name": "Skyline Enterprises (UPDATED)",
        "phone": "+91 9876543210",
        "email": "contact@skyline.com",
        "address": "45 Industrial Area, Phase 2, New Delhi"
      },
      "customer_name": "Skyline Enterprises (UPDATED)",
      "customer_phone": "+91 9876543210",
      "customer_email": "contact@skyline.com",
      "customer_address": "45 Industrial Area, Phase 2, New Delhi",
      "items": [
        {
          "item": "G+2 Automatic Passenger Lift",
          "description": "Passenger Lift",
          "desc": "Passenger Lift",
          "qty": "1",
          "quantity": 1.0,
          "rate": 450000.0,
          "unit_price": 450000.0,
          "formatted_rate": "Rs 4,50,000.00",
          "total": "Rs 4,50,000.00",
          "formatted_total": "Rs 4,50,000.00",
          "amount": 450000.0
        }
      ],
      "pricing_summary": {
        "subtotal": 450000.0,
        "formatted_subtotal": "Rs 4,50,000.00",
        "tax_type": "GST 18%",
        "tax_rate": 0.18,
        "tax_amount": 76500.0,
        "formatted_tax": "Rs 76,500.00",
        "discount_type": "Flat",
        "discount_amount": 25000.0,
        "formatted_discount": "Rs 25,000.00",
        "grand_total": 501500.0,
        "formatted_grand_total": "Rs 5,01,500.00"
      },
      "terms_and_conditions": [
        "1. 50% advance along with purchase order.",
        "2. Delivery within 4-6 weeks.",
        "3. 1 year warranty."
      ],
      "terms": "1. 50% advance along with purchase order.\n2. Delivery within 4-6 weeks.\n3. 1 year warranty.",
      "representation": "Represented by Mr./Ms. ________________,",
      "actions": {
        "download_pdf_url": "http://192.168.1.54:8000/api/quotations/QTN-260910-0002/pdf",
        "share_url": "http://192.168.1.54:8000/api/quotations/QTN-260910-0002/share"
      },
      "download_pdf_url": "http://192.168.1.54:8000/api/quotations/QTN-260910-0002/pdf",
      "share_url": "http://192.168.1.54:8000/api/quotations/QTN-260910-0002/share",
      "user_id": 11,
      "created_at": "2026-09-10T08:07:57.863934",
      "updated_at": "2026-09-18T07:35:42.075791"
    },
    {
      "id": "QTN-260910-0001",
      "db_id": 4,
      "quotation_id": "QTN-260910-0001",
      "quotation_no": "QTN-260910-0001",
      "status": "Sent",
      "statusColor": "blue",
      "status_color": "blue",
      "status_color_hex": "#3B82F6",
      "icon": "elevator",
      "iconColor": "blue",
      "icon_color": "blue",
      "category": "Lift",
      "date": "17 May 2025",
      "quotation_date": "17 May 2025",
      "time": "10:30 AM",
      "quotation_time": "10:30 AM",
      "validTill": "31 May 2025",
      "valid_till": "31 May 2025",
      "amount": "Rs 5,01,500.00",
      "grand_total": 501500.0,
      "formatted_amount": "Rs 5,01,500.00",
      "company": {
        "company_name": "M/s. POWER SOLUTION.COM ENTERPRISES",
        "gstn": "20EGHPS4942E1ZH",
        "email": "POWERSOLUTIONDG3@GMAIL.COM",
        "iso_certificate": "ISO 9001:2015 QMS-25111206",
        "electric_license_no": "JH/EC/5382",
        "registered_address": "SOLANKI , SINGHMORE, HATIA ,RANCHI JHARKHAND PIN CODE 834003",
        "representative": "Mr./Ms. ________________"
      },
      "customer": {
        "name": "Skyline Enterprises",
        "phone": "+91 9876543210",
        "email": "contact@skyline.com",
        "address": "45 Industrial Area, Phase 2, New Delhi"
      },
      "customer_name": "Skyline Enterprises",
      "customer_phone": "+91 9876543210",
      "customer_email": "contact@skyline.com",
      "customer_address": "45 Industrial Area, Phase 2, New Delhi",
      "items": [
        {
          "item": "G+2 Automatic Passenger Lift",
          "description": "Passenger Lift",
          "desc": "Passenger Lift",
          "qty": "1",
          "quantity": 1.0,
          "rate": 450000.0,
          "unit_price": 450000.0,
          "formatted_rate": "Rs 4,50,000.00",
          "total": "Rs 4,50,000.00",
          "formatted_total": "Rs 4,50,000.00",
          "amount": 450000.0
        }
      ],
      "pricing_summary": {
        "subtotal": 450000.0,
        "formatted_subtotal": "Rs 4,50,000.00",
        "tax_type": "GST 18%",
        "tax_rate": 0.18,
        "tax_amount": 76500.0,
        "formatted_tax": "Rs 76,500.00",
        "discount_type": "Flat",
        "discount_amount": 25000.0,
        "formatted_discount": "Rs 25,000.00",
        "grand_total": 501500.0,
        "formatted_grand_total": "Rs 5,01,500.00"
      },
      "terms_and_conditions": [
        "1. 50% advance along with purchase order.\\n2. Delivery within 4-6 weeks.\\n3. 1 year warranty."
      ],
      "terms": "1. 50% advance along with purchase order.\\n2. Delivery within 4-6 weeks.\\n3. 1 year warranty.",
      "representation": "Represented by Mr./Ms. ________________,",
      "actions": {
        "download_pdf_url": "http://192.168.1.54:8000/api/quotations/QTN-260910-0001/pdf",
        "share_url": "http://192.168.1.54:8000/api/quotations/QTN-260910-0001/share"
      },
      "download_pdf_url": "http://192.168.1.54:8000/api/quotations/QTN-260910-0001/pdf",
      "share_url": "http://192.168.1.54:8000/api/quotations/QTN-260910-0001/share",
      "user_id": 11,
      "created_at": "2026-09-10T08:04:32.558617",
      "updated_at": "2026-09-18T07:35:42.075790"
    },
    {
      "id": "QTN-250517-JSON1",
      "db_id": 3,
      "quotation_id": "QTN-250517-JSON1",
      "quotation_no": "QTN-250517-JSON1",
      "status": "Sent",
      "statusColor": "blue",
      "status_color": "blue",
      "status_color_hex": "#3B82F6",
      "icon": "elevator",
      "iconColor": "blue",
      "icon_color": "blue",
      "category": "Lift",
      "date": "17 May 2025",
      "quotation_date": "17 May 2025",
      "time": "10:30 AM",
      "quotation_time": "10:30 AM",
      "validTill": "31 May 2025",
      "valid_till": "31 May 2025",
      "amount": "Rs 5,01,500.00",
      "grand_total": 501500.0,
      "formatted_amount": "Rs 5,01,500.00",
      "company": {
        "company_name": "M/s. POWER SOLUTION.COM ENTERPRISES",
        "gstn": "20EGHPS4942E1ZH",
        "email": "POWERSOLUTIONDG3@GMAIL.COM",
        "iso_certificate": "ISO 9001:2015 QMS-25111206",
        "electric_license_no": "JH/EC/5382",
        "registered_address": "SOLANKI , SINGHMORE, HATIA ,RANCHI JHARKHAND PIN CODE 834003",
        "representative": "Mr./Ms. ________________"
      },
      "customer": {
        "name": "Skyline Enterprises (JSON)",
        "phone": "+91 9876543210",
        "email": "contact@skyline.com",
        "address": "45 Industrial Area, Phase 2, New Delhi"
      },
      "customer_name": "Skyline Enterprises (JSON)",
      "customer_phone": "+91 9876543210",
      "customer_email": "contact@skyline.com",
      "customer_address": "45 Industrial Area, Phase 2, New Delhi",
      "items": [
        {
          "item": "G+2 Automatic Passenger Lift",
          "description": "Passenger Lift",
          "desc": "Passenger Lift",
          "qty": "1",
          "quantity": 1.0,
          "rate": 450000.0,
          "unit_price": 450000.0,
          "formatted_rate": "Rs 4,50,000.00",
          "total": "Rs 4,50,000.00",
          "formatted_total": "Rs 4,50,000.00",
          "amount": 450000.0
        }
      ],
      "pricing_summary": {
        "subtotal": 450000.0,
        "formatted_subtotal": "Rs 4,50,000.00",
        "tax_type": "GST 18%",
        "tax_rate": 0.18,
        "tax_amount": 76500.0,
        "formatted_tax": "Rs 76,500.00",
        "discount_type": "Flat",
        "discount_amount": 25000.0,
        "formatted_discount": "Rs 25,000.00",
        "grand_total": 501500.0,
        "formatted_grand_total": "Rs 5,01,500.00"
      },
      "terms_and_conditions": [
        "1. 50% advance."
      ],
      "terms": "1. 50% advance.",
      "representation": "Represented by Mr./Ms. ________________,",
      "actions": {
        "download_pdf_url": "http://192.168.1.54:8000/api/quotations/QTN-250517-JSON1/pdf",
        "share_url": "http://192.168.1.54:8000/api/quotations/QTN-250517-JSON1/share"
      },
      "download_pdf_url": "http://192.168.1.54:8000/api/quotations/QTN-250517-JSON1/pdf",
      "share_url": "http://192.168.1.54:8000/api/quotations/QTN-250517-JSON1/share",
      "user_id": 11,
      "created_at": "2026-09-10T08:03:52.608691",
      "updated_at": "2026-09-18T07:35:42.075789"
    },
    {
      "id": "QTN-250517-FORM1",
      "db_id": 2,
      "quotation_id": "QTN-250517-FORM1",
      "quotation_no": "QTN-250517-FORM1",
      "status": "Sent",
      "statusColor": "blue",
      "status_color": "blue",
      "status_color_hex": "#3B82F6",
      "icon": "elevator",
      "iconColor": "blue",
      "icon_color": "blue",
      "category": "Lift",
      "date": "17 May 2025",
      "quotation_date": "17 May 2025",
      "time": "10:30 AM",
      "quotation_time": "10:30 AM",
      "validTill": "31 May 2025",
      "valid_till": "31 May 2025",
      "amount": "Rs 5,01,500.00",
      "grand_total": 501500.0,
      "formatted_amount": "Rs 5,01,500.00",
      "company": {
        "company_name": "M/s. POWER SOLUTION.COM ENTERPRISES",
        "gstn": "20EGHPS4942E1ZH",
        "email": "POWERSOLUTIONDG3@GMAIL.COM",
        "iso_certificate": "ISO 9001:2015 QMS-25111206",
        "electric_license_no": "JH/EC/5382",
        "registered_address": "SOLANKI , SINGHMORE, HATIA ,RANCHI JHARKHAND PIN CODE 834003",
        "representative": "Mr./Ms. ________________"
      },
      "customer": {
        "name": "Skyline Enterprises (Form Data)",
        "phone": "+91 9876543210",
        "email": "contact@skyline.com",
        "address": "45 Industrial Area, Phase 2, New Delhi"
      },
      "customer_name": "Skyline Enterprises (Form Data)",
      "customer_phone": "+91 9876543210",
      "customer_email": "contact@skyline.com",
      "customer_address": "45 Industrial Area, Phase 2, New Delhi",
      "items": [
        {
          "item": "G+2 Automatic Passenger Lift",
          "description": "Passenger Lift",
          "desc": "Passenger Lift",
          "qty": "1",
          "quantity": 1.0,
          "rate": 450000.0,
          "unit_price": 450000.0,
          "formatted_rate": "Rs 4,50,000.00",
          "total": "Rs 4,50,000.00",
          "formatted_total": "Rs 4,50,000.00",
          "amount": 450000.0
        }
      ],
      "pricing_summary": {
        "subtotal": 450000.0,
        "formatted_subtotal": "Rs 4,50,000.00",
        "tax_type": "GST 18%",
        "tax_rate": 0.18,
        "tax_amount": 76500.0,
        "formatted_tax": "Rs 76,500.00",
        "discount_type": "Flat",
        "discount_amount": 25000.0,
        "formatted_discount": "Rs 25,000.00",
        "grand_total": 501500.0,
        "formatted_grand_total": "Rs 5,01,500.00"
      },
      "terms_and_conditions": [
        "1. 50% advance."
      ],
      "terms": "1. 50% advance.",
      "representation": "Represented by Mr./Ms. ________________,",
      "actions": {
        "download_pdf_url": "http://192.168.1.54:8000/api/quotations/QTN-250517-FORM1/pdf",
        "share_url": "http://192.168.1.54:8000/api/quotations/QTN-250517-FORM1/share"
      },
      "download_pdf_url": "http://192.168.1.54:8000/api/quotations/QTN-250517-FORM1/pdf",
      "share_url": "http://192.168.1.54:8000/api/quotations/QTN-250517-FORM1/share",
      "user_id": 11,
      "created_at": "2026-09-10T08:03:52.601506",
      "updated_at": "2026-09-18T07:35:42.075783"
    }
  ],
  "count": 5
}

response (Logged in as User 7 - Empty State with 0 Quotations) :- 

{
  "summary": {
    "total_quotations": {
      "title": "Total Quotations",
      "count": "0",
      "amount": 0,
      "formatted_amount": "Rs 0.00"
    },
    "approved": {
      "title": "Approved",
      "count": "0",
      "amount": 0,
      "formatted_amount": "Rs 0.00"
    },
    "sent": {
      "title": "Sent",
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
  "quotations": [],
  "count": 0
}

---

## 5. Download Quotation PDF

url : (http://192.168.1.54:8000/api/quotations/QTN-250517-0001/pdf)
method : GET

headers :- 

Authorization: Bearer <user_login_token> (Required)

response :- 

{
  "quotation_id": "QTN-250517-0001",
  "file_name": "QTN-250517-0001.pdf",
  "file_size": "142 KB",
  "mime_type": "application/pdf",
  "status": "Ready",
  "download_url": "http://192.168.1.54:8000/api/quotations/QTN-250517-0001/pdf",
  "generated_at": "2026-09-18T07:35:42.077478"
}

---

## 6. Share Quotation

url : (http://192.168.1.54:8000/api/quotations/QTN-250517-0001/share)
method : GET

headers :- 

Authorization: Bearer <user_login_token> (Required)

response :- 

{
  "quotation_id": "QTN-250517-0001",
  "share_url": "http://192.168.1.54:8000/quotations/view/QTN-250517-0001",
  "share_text": "Quotation QTN-250517-0001 for Rajesh Kumar of Rs 4,56,000.00 from Power Solution Enterprises."
}

---

## 7. Missing Bearer Token Security Check (HTTP 401 Unauthorized)

If request is sent without Authorization header:

url : (http://192.168.1.54:8000/api/quotations/QTN-250517-0001)
method : GET

headers :- 

(No Authorization header provided)

response :- 

HTTP 401 Unauthorized
{
  "detail": "Bearer token is compulsory. Please provide Authorization: Bearer <token>"
}
