from datetime import datetime, timezone
from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import relationship

from core.settings import Base


def utc_now():
    return datetime.now(timezone.utc)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(80), unique=True, index=True, nullable=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, index=True, nullable=False)
    phone_number = Column(String(20), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), default="user", nullable=False)  # "admin" or "user"
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=utc_now, nullable=False)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now, nullable=False)

    def __repr__(self):
        return f"<User id={self.id} full_name='{self.full_name}' email='{self.email}' phone='{self.phone_number}' role='{self.role}'>"


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    category_name = Column(String(100), nullable=False, index=True)
    category_code = Column(String(50), unique=True, index=True, nullable=False)
    category_type = Column(String(50), nullable=False, index=True)
    category_image = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    display_order = Column(Integer, default=0, nullable=False)
    status = Column(String(20), default="active", nullable=False)
    created_at = Column(DateTime, default=utc_now, nullable=False)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now, nullable=False)

    def __repr__(self):
        return (
            f"<Category id={self.id} name='{self.category_name}' code='{self.category_code}' "
            f"type='{self.category_type}' status='{self.status}'>"
        )


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    category_type = Column(String(50), nullable=False, index=True)  # lift, generator, panel, earthing, service, other
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"), nullable=True, index=True)
    category_name = Column(String(100), nullable=True)

    # Basic Details
    product_name = Column(String(150), nullable=False, index=True)
    product_code = Column(String(100), unique=True, nullable=False, index=True)  # SKU
    brand = Column(String(100), nullable=True)
    model_number = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)

    # Pricing & Tax
    purchase_price = Column(Float, nullable=True)
    selling_price = Column(Float, nullable=True)
    discount = Column(String(50), nullable=True)
    gst_rate = Column(String(20), nullable=True)
    hsn_code = Column(String(50), nullable=True)

    # Inventory
    inventory_tracking = Column(Boolean, default=False, nullable=False)
    stock = Column(Float, default=0.0, nullable=True)
    unit = Column(String(50), nullable=True)
    min_stock = Column(Float, default=0.0, nullable=True)

    # Warranty & Terms
    warranty_period = Column(String(100), nullable=True)
    warranty_terms = Column(Text, nullable=True)
    payment_terms = Column(Text, nullable=True)

    # Media & Status
    product_image = Column(String(255), nullable=True)
    status = Column(String(20), default="active", nullable=False)

    # Dynamic Category Specifications (Stored as JSON)
    specifications = Column(JSON, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=utc_now, nullable=False)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now, nullable=False)

    # Relationship
    category = relationship("Category", backref="products")

    def __repr__(self):
        return (
            f"<Product id={self.id} name='{self.product_name}' code='{self.product_code}' "
            f"type='{self.category_type}' status='{self.status}'>"
        )


class Quotation(Base):
    __tablename__ = "quotations"

    id = Column(Integer, primary_key=True, index=True)
    quotation_no = Column(String(60), unique=True, index=True, nullable=False)
    quotation_date = Column(String(50), nullable=False)
    valid_till = Column(String(50), nullable=False)
    quotation_time = Column(String(50), default="10:30 AM", nullable=True)
    reference = Column(String(100), nullable=True)

    # Classification
    category = Column(String(100), default="Lift", nullable=True)

    # Linked User / Customer Account
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    user = relationship("User", backref="quotations", foreign_keys=[user_id])

    # Customer Details (Input fields as requested by user)
    customer_name = Column(String(150), nullable=False, index=True)
    address = Column(Text, nullable=True)
    phone = Column(String(50), nullable=True)
    email = Column(String(120), nullable=True)

    # Line Items (Stored as JSON array)
    items = Column(JSON, nullable=False, default=list)

    # Pricing Summary
    subtotal = Column(Float, default=0.0, nullable=False)
    discount_type = Column(String(20), default="Flat", nullable=False)  # "Flat" or "%"
    discount_value = Column(Float, default=0.0, nullable=False)
    discount_amount = Column(Float, default=0.0, nullable=False)
    tax_type = Column(String(50), default="GST 18%", nullable=False)
    tax_rate = Column(Float, default=0.18, nullable=False)
    taxable_amount = Column(Float, default=0.0, nullable=False)
    tax_amount = Column(Float, default=0.0, nullable=False)
    grand_total = Column(Float, default=0.0, nullable=False)

    # Terms & Status
    terms = Column(Text, nullable=True)
    status = Column(String(30), default="Draft", nullable=False)  # "Draft", "Sent", "Approved", "Rejected"

    # Timestamps
    created_at = Column(DateTime, default=utc_now, nullable=False)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now, nullable=False)

    def __repr__(self):
        return (
            f"<Quotation id={self.id} no='{self.quotation_no}' customer='{self.customer_name}' "
            f"total={self.grand_total} status='{self.status}'>"
        )


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    payment_no = Column(String(60), unique=True, index=True, nullable=True)  # e.g. "PAY-250517-001"
    invoice_no = Column(String(60), index=True, nullable=False)
    invoice_id = Column(Integer, ForeignKey("invoices.id", ondelete="SET NULL"), nullable=True, index=True)
    invoice_desc = Column(String(150), nullable=True)  # e.g. "Sales Invoice - Lift"
    category = Column(String(100), nullable=True)  # "Lift", "Generator", "Panel", "Earthing"

    # Linked User
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)

    customer_name = Column(String(150), nullable=False, index=True)
    customer_phone = Column(String(50), nullable=True)
    customer_email = Column(String(120), nullable=True)
    customer_address = Column(Text, nullable=True)

    quotation_id = Column(Integer, ForeignKey("quotations.id", ondelete="SET NULL"), nullable=True, index=True)
    quotation_no = Column(String(60), nullable=True, index=True)

    payment_date = Column(String(50), nullable=False)
    payment_time = Column(String(50), nullable=True)  # e.g. "10:30 AM"
    amount_received = Column(Float, nullable=False, default=0.0)
    payment_mode = Column(String(50), nullable=False)  # "Cash", "Online", "Cheque", "UPI", "Bank Transfer", "Card", "NEFT"
    transaction_no = Column(String(100), nullable=True)  # Transaction or Cheque no
    reference_no = Column(String(100), nullable=True)
    notes = Column(Text, nullable=True)
    payment_proof = Column(String(255), nullable=True)  # Image or PDF receipt path
    status = Column(String(30), default="Paid", nullable=False)  # "Paid", "Partial", "Pending"

    created_at = Column(DateTime, default=utc_now, nullable=False)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now, nullable=False)

    quotation = relationship("Quotation", backref="payments")
    invoice = relationship("Invoice", backref="payments")
    user = relationship("User", backref="payments")

    def __repr__(self):
        return (
            f"<Payment id={self.id} payment_no='{self.payment_no}' invoice='{self.invoice_no}' "
            f"customer='{self.customer_name}' amount={self.amount_received} mode='{self.payment_mode}' status='{self.status}'>"
        )


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    order_no = Column(String(60), unique=True, index=True, nullable=False)
    order_date = Column(String(50), nullable=False)
    delivery_date = Column(String(50), nullable=True)
    order_status = Column(String(30), default="Pending", nullable=False)  # Pending, Confirmed, Processing, Completed, Cancelled, Draft

    # Quotation Link
    quotation_id = Column(Integer, ForeignKey("quotations.id", ondelete="SET NULL"), nullable=True, index=True)
    quotation_no = Column(String(60), nullable=True, index=True)

    # Customer Details
    customer_name = Column(String(150), nullable=False, index=True)
    mobile = Column(String(50), nullable=True)
    email = Column(String(120), nullable=True)
    billing_address = Column(Text, nullable=True)
    delivery_address = Column(Text, nullable=True)

    # Products / Items (stored as JSON array)
    items = Column(JSON, nullable=False, default=list)

    # Pricing & Summary
    subtotal = Column(Float, default=0.0, nullable=False)
    discount = Column(Float, default=0.0, nullable=False)
    taxable_amount = Column(Float, default=0.0, nullable=False)
    tax = Column(Float, default=0.0, nullable=False)
    grand_total = Column(Float, default=0.0, nullable=False)
    advance_paid = Column(Float, default=0.0, nullable=False)
    balance_amount = Column(Float, default=0.0, nullable=False)

    # Delivery & Installation
    special_instructions = Column(Text, nullable=True)

    # Payment Details
    payment_status = Column(String(30), default="Not Paid", nullable=False)  # Not Paid, Partially Paid, Paid
    payment_mode = Column(String(50), default="Bank Transfer", nullable=False)  # Cash, Bank Transfer, UPI, Cheque, Card, Other
    transaction_no = Column(String(100), nullable=True)
    payment_date = Column(String(50), nullable=True)

    # Additional
    internal_notes = Column(Text, nullable=True)
    terms_accepted = Column(Boolean, default=True, nullable=False)

    created_at = Column(DateTime, default=utc_now, nullable=False)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now, nullable=False)

    quotation = relationship("Quotation", backref="orders")

    def __repr__(self):
        return (
            f"<Order id={self.id} no='{self.order_no}' customer='{self.customer_name}' "
            f"total={self.grand_total} status='{self.order_status}'>"
        )


class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    invoice_no = Column(String(60), unique=True, index=True, nullable=False)
    invoice_date = Column(String(50), nullable=False)
    due_date = Column(String(50), nullable=True)

    # Linked Order / Quotation
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="SET NULL"), nullable=True, index=True)
    order_no = Column(String(60), nullable=True, index=True)
    quotation_id = Column(Integer, ForeignKey("quotations.id", ondelete="SET NULL"), nullable=True, index=True)
    quotation_no = Column(String(60), nullable=True, index=True)

    # Linked User / Customer Account
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)

    # Customer Details
    customer_name = Column(String(150), nullable=False, index=True)
    phone = Column(String(50), nullable=True)
    email = Column(String(120), nullable=True)
    billing_address = Column(Text, nullable=True)
    delivery_address = Column(Text, nullable=True)

    # Terms & References
    payment_terms = Column(String(50), default="30 Days", nullable=False)
    reference_no = Column(String(100), nullable=True)

    # Classification for Dashboard (Sales / Service, Category)
    category = Column(String(100), default="Lift", nullable=True)  # "Lift", "Generator", "Panel", "Earthing"
    invoice_type = Column(String(50), default="Sales", nullable=False)  # "Sales" or "Service"

    # Line Items (stored as JSON array: [{id, name, code, category, qty, rate, discount, tax, total, specifications}])
    items = Column(JSON, nullable=False, default=list)

    # Pricing & Summary
    subtotal = Column(Float, default=0.0, nullable=False)
    discount = Column(Float, default=0.0, nullable=False)
    tax_percent = Column(Float, default=18.0, nullable=False)
    tax = Column(Float, default=0.0, nullable=False)
    grand_total = Column(Float, default=0.0, nullable=False)
    amount_paid = Column(Float, default=0.0, nullable=False)
    balance_due = Column(Float, default=0.0, nullable=False)

    # Notes & Status
    notes = Column(Text, nullable=True)
    status = Column(String(30), default="Unpaid", nullable=False)  # Unpaid, Paid, Partially Paid, Overdue, Draft, Cancelled

    created_at = Column(DateTime, default=utc_now, nullable=False)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now, nullable=False)

    order = relationship("Order", backref="invoices")
    quotation = relationship("Quotation", backref="invoices")
    user = relationship("User", backref="invoices")

    def __repr__(self):
        return (
            f"<Invoice id={self.id} no='{self.invoice_no}' customer='{self.customer_name}' "
            f"total={self.grand_total} status='{self.status}'>"
        )


class CashBill(Base):
    __tablename__ = "cash_bills"

    id = Column(Integer, primary_key=True, index=True)
    bill_no = Column(String(60), unique=True, index=True, nullable=False)
    bill_date = Column(String(50), nullable=False)
    customer_type = Column(String(50), default="Walk-in Customer", nullable=False)  # "Walk-in Customer" or "Existing Customer"
    customer_name = Column(String(150), nullable=False, index=True)
    mobile = Column(String(50), nullable=True)

    # Line items with specifications, price, qty, total
    items = Column(JSON, nullable=False, default=list)

    # Calculations
    subtotal = Column(Float, default=0.0, nullable=False)
    discount = Column(Float, default=0.0, nullable=False)
    taxable_amount = Column(Float, default=0.0, nullable=False)
    gst_rate = Column(Float, default=0.18, nullable=False)
    gst_amount = Column(Float, default=0.0, nullable=False)
    grand_total = Column(Float, default=0.0, nullable=False)

    # Payment settlement
    payment_mode = Column(String(50), default="Cash", nullable=False)  # "Cash", "UPI", "Card", "Bank Transfer"
    amount_paid = Column(Float, default=0.0, nullable=False)
    change_returned = Column(Float, default=0.0, nullable=False)
    balance_amount = Column(Float, default=0.0, nullable=False)
    payment_status = Column(String(30), default="Paid", nullable=False)  # "Paid", "Partially Paid", "Unpaid"

    # Additional
    notes = Column(Text, nullable=True)
    status = Column(String(30), default="Generated", nullable=False)  # "Generated", "Draft", "Cancelled"

    created_at = Column(DateTime, default=utc_now, nullable=False)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now, nullable=False)

    def __repr__(self):
        return (
            f"<CashBill id={self.id} no='{self.bill_no}' customer='{self.customer_name}' "
            f"total={self.grand_total} status='{self.status}'>"
        )


class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True)
    supplier_code = Column(String(50), unique=True, index=True, nullable=False)  # e.g. "SUP001"
    name = Column(String(150), nullable=False, index=True)
    contact_person = Column(String(100), nullable=True)
    mobile = Column(String(50), nullable=True)
    email = Column(String(120), nullable=True)
    address = Column(Text, nullable=True)
    gstin = Column(String(50), nullable=True)
    payment_terms = Column(String(50), default="30 Days", nullable=True)

    created_at = Column(DateTime, default=utc_now, nullable=False)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now, nullable=False)

    def __repr__(self):
        return f"<Supplier id={self.id} code='{self.supplier_code}' name='{self.name}'>"


class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"

    id = Column(Integer, primary_key=True, index=True)
    po_number = Column(String(60), unique=True, index=True, nullable=False)  # e.g. "PO-260914-0001"
    po_date = Column(String(50), nullable=False)
    expected_delivery = Column(String(50), nullable=True)
    po_status = Column(String(30), default="Draft", nullable=False)  # Draft, Pending, Approved, Ordered, Received, Cancelled
    payment_terms = Column(String(50), default="30 Days", nullable=False)
    reference = Column(String(100), nullable=True)

    # Supplier info
    supplier_id = Column(Integer, ForeignKey("suppliers.id", ondelete="SET NULL"), nullable=True, index=True)
    supplier_code = Column(String(50), nullable=True)
    supplier_name = Column(String(150), nullable=False)
    contact_person = Column(String(100), nullable=True)
    mobile = Column(String(50), nullable=True)
    email = Column(String(120), nullable=True)
    address = Column(Text, nullable=True)

    # Items
    items = Column(JSON, nullable=False, default=list)

    # Totals
    subtotal = Column(Float, default=0.0, nullable=False)
    gst_total = Column(Float, default=0.0, nullable=False)
    grand_total = Column(Float, default=0.0, nullable=False)

    # Additional
    notes = Column(Text, nullable=True)

    created_at = Column(DateTime, default=utc_now, nullable=False)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now, nullable=False)

    supplier = relationship("Supplier", backref="purchase_orders")

    def __repr__(self):
        return (
            f"<PurchaseOrder id={self.id} no='{self.po_number}' supplier='{self.supplier_name}' "
            f"total={self.grand_total} status='{self.po_status}'>"
        )


class StockIn(Base):
    __tablename__ = "stock_in_receipts"

    id = Column(Integer, primary_key=True, index=True)
    receipt_no = Column(String(60), unique=True, index=True, nullable=False)
    receipt_date = Column(String(50), nullable=False)
    po_number = Column(String(60), nullable=True, index=True)
    invoice_no = Column(String(60), nullable=False, index=True)
    invoice_date = Column(String(50), nullable=False)

    # Supplier Details
    supplier_id = Column(Integer, ForeignKey("suppliers.id", ondelete="SET NULL"), nullable=True, index=True)
    supplier_code = Column(String(50), nullable=True, index=True)
    supplier_name = Column(String(150), nullable=False)
    supplier_contact = Column(String(50), nullable=True)

    # Product Details
    product_id = Column(Integer, ForeignKey("products.id", ondelete="SET NULL"), nullable=True, index=True)
    product_sku = Column(String(100), nullable=True, index=True)
    product_type = Column(String(50), nullable=False, index=True)
    category = Column(String(100), nullable=False, index=True)
    product_name = Column(String(150), nullable=False, index=True)
    specifications = Column(JSON, nullable=True, default=dict)

    # Stock Details
    quantity = Column(Float, default=1.0, nullable=False)
    unit = Column(String(50), default="Nos", nullable=False)
    warehouse = Column(String(100), default="Main Warehouse", nullable=False)
    rack = Column(String(100), nullable=True)
    batch_no = Column(String(100), nullable=True)
    serial_no = Column(String(150), nullable=True)

    # Pricing & Tax
    rate = Column(Float, default=0.0, nullable=False)
    discount = Column(Float, default=0.0, nullable=False)
    gst = Column(Float, default=18.0, nullable=False)
    gross_amount = Column(Float, default=0.0, nullable=False)
    taxable_amount = Column(Float, default=0.0, nullable=False)
    gst_amount = Column(Float, default=0.0, nullable=False)
    total_amount = Column(Float, default=0.0, nullable=False)

    # Receiving & Inspection
    received_by = Column(String(100), nullable=False)
    condition = Column(String(50), default="Good", nullable=False)
    inspection_status = Column(String(50), default="Pending", nullable=False)
    inspection_remarks = Column(Text, nullable=True)

    # Notes & Status
    notes = Column(Text, nullable=True)
    status = Column(String(30), default="Received", nullable=False)

    # Timestamps
    created_at = Column(DateTime, default=utc_now, nullable=False)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now, nullable=False)

    supplier = relationship("Supplier", backref="stock_ins")
    product = relationship("Product", backref="stock_ins")

    def __repr__(self):
        return (
            f"<StockIn id={self.id} receipt='{self.receipt_no}' product='{self.product_name}' "
            f"qty={self.quantity} total={self.total_amount}>"
        )







