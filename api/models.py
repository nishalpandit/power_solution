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
    reference = Column(String(100), nullable=True)

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
    invoice_no = Column(String(60), unique=True, index=True, nullable=False)
    customer_name = Column(String(150), nullable=False, index=True)
    customer_phone = Column(String(50), nullable=True)
    customer_email = Column(String(120), nullable=True)
    customer_address = Column(Text, nullable=True)

    quotation_id = Column(Integer, ForeignKey("quotations.id", ondelete="SET NULL"), nullable=True, index=True)
    quotation_no = Column(String(60), nullable=True, index=True)

    payment_date = Column(String(50), nullable=False)
    amount_received = Column(Float, nullable=False, default=0.0)
    payment_mode = Column(String(50), nullable=False)  # "Cash", "Online", "Cheque", "UPI", etc.
    transaction_no = Column(String(100), nullable=True)  # Transaction or Cheque no
    reference_no = Column(String(100), nullable=True)
    notes = Column(Text, nullable=True)
    payment_proof = Column(String(255), nullable=True)  # Image or PDF receipt path
    status = Column(String(30), default="Received", nullable=False)  # "Received", "Pending", "Failed"

    created_at = Column(DateTime, default=utc_now, nullable=False)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now, nullable=False)

    quotation = relationship("Quotation", backref="payments")

    def __repr__(self):
        return (
            f"<Payment id={self.id} invoice='{self.invoice_no}' customer='{self.customer_name}' "
            f"amount={self.amount_received} mode='{self.payment_mode}' status='{self.status}'>"
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





