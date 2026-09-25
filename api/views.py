import json
import os
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Union

from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, Request, UploadFile, status
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from api.models import Category, CashBill, Invoice, Order, Payment, Product, PurchaseOrder, Quotation, StockIn, Supplier, User
from api.schemas import (
    AdminLoginRequest,
    CashBillCalculateRequest,
    CashBillCalculateResponse,
    CashBillCreateRequest,
    CashBillResponse,
    CashBillUpdateRequest,
    CategoryStockResponse,
    EarthingProductCreateRequest,
    GeneratorProductCreateRequest,
    LiftProductCreateRequest,
    OrderCreateRequest,
    OrderResponse,
    OrderUpdateRequest,
    OtherProductCreateRequest,
    PanelProductCreateRequest,
    PaymentCreateRequest,
    PaymentResponse,
    PaymentUpdateRequest,
    ProductListResponse,
    ProductResponse,
    PurchaseCalculateRequest,
    PurchaseCalculateResponse,
    PurchaseOrderCreateRequest,
    PurchaseOrderResponse,
    PurchaseOrderUpdateRequest,
    QuotationCreateRequest,
    QuotationItemSchema,
    QuotationListResponse,
    QuotationResponse,
    ServiceProductCreateRequest,
    StockInCalculateRequest,
    StockInCalculateResponse,
    StockInCreateRequest,
    StockInMetaResponse,
    StockInResponse,
    StockInUpdateRequest,
    SupplierCreateRequest,
    SupplierResponse,
    UserListResponse,
    UserLoginRequest,
    UserRegisterRequest,
    UserResponse,
)
from core.auth import create_access_token, get_current_user, hash_password, require_admin, verify_password
from core.settings import get_db

router = APIRouter()


# ==============================================================================
# AUTH & USER HELPERS
# ==============================================================================

def normalize_phone_number(value: str) -> str:
    return "".join(ch for ch in value.strip() if ch.isdigit())


def ensure_default_admin(db: Session):
    admin_username = "admin"
    admin_email = "admin@power.solution"
    admin_user = db.query(User).filter((User.username == admin_username) | (User.email == admin_email)).first()
    if admin_user:
        if not admin_user.username:
            admin_user.username = admin_username
        if admin_user.role != "admin":
            admin_user.role = "admin"
        db.commit()
        return admin_user

    default_admin = User(
        username=admin_username,
        full_name="System Administrator",
        email=admin_email,
        phone_number="0000000000",
        password_hash=hash_password("admin123"),
        role="admin",
        is_active=True,
    )
    db.add(default_admin)
    db.commit()
    db.refresh(default_admin)
    return default_admin


async def parse_json_or_form(request: Request, model):
    content_type = request.headers.get("content-type", "").lower()

    if "application/json" in content_type:
        body = await request.json()
        return model(**body)

    if "multipart/form-data" in content_type or "application/x-www-form-urlencoded" in content_type:
        form_data = await request.form()
        payload = {key: value for key, value in form_data.items()}
        return model(**payload)

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Request body must be JSON or form data",
    )


# ==============================================================================
# AUTH ENDPOINTS
# ==============================================================================

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(request: Request, db: Session = Depends(get_db)):
    payload = await parse_json_or_form(request, UserRegisterRequest)
    email = payload.email.lower().strip()
    phone_number = normalize_phone_number(payload.phone_number)

    if db.query(User).filter(User.email == email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email address is already registered",
        )

    if db.query(User).filter(User.phone_number == phone_number).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Phone number is already registered",
        )

    user = User(
        full_name=payload.full_name.strip(),
        email=email,
        phone_number=phone_number,
        password_hash=hash_password(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token({"sub": str(user.id)})
    return {
        "message": "User created successfully",
        "token": token,
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "phone_number": user.phone_number,
            "role": user.role,
            "is_active": user.is_active,
        },
    }


@router.post("/login")
async def login_user(request: Request, db: Session = Depends(get_db)):
    payload = await parse_json_or_form(request, UserLoginRequest)
    email = payload.email.lower().strip() if payload.email else None
    phone_number = normalize_phone_number(payload.phone_number) if payload.phone_number else None

    user = None
    if email:
        user = db.query(User).filter(User.email == email).first()
    if not user and phone_number:
        user = db.query(User).filter(User.phone_number == phone_number).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email/phone number or password",
        )

    if not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email/phone number or password",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )

    token = create_access_token({"sub": str(user.id)})
    return {
        "message": "Login successful",
        "token": token,
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "phone_number": user.phone_number,
            "role": user.role,
            "is_active": user.is_active,
        },
    }


@router.post("/admin/login")
async def admin_login(request: Request, db: Session = Depends(get_db)):
    payload = await parse_json_or_form(request, AdminLoginRequest)
    ensure_default_admin(db)

    username = payload.username.strip()
    user = db.query(User).filter(User.username == username).first()
    if not user:
        user = db.query(User).filter(User.full_name == username).first()
    if not user:
        user = db.query(User).filter(User.email == username.lower()).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid admin username or password",
        )

    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )

    if not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid admin username or password",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin account is inactive",
        )

    token = create_access_token({"sub": str(user.id)})
    return {
        "message": "Admin login successful",
        "token": token,
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "username": user.username,
            "full_name": user.full_name,
            "email": user.email,
            "phone_number": user.phone_number,
            "role": user.role,
            "is_active": user.is_active,
        },
    }


def format_user_response(user: User) -> dict:
    return {
        "id": user.id,
        "username": user.username,
        "full_name": user.full_name,
        "email": user.email,
        "phone_number": user.phone_number,
        "role": user.role,
        "is_active": user.is_active,
        "created_at": user.created_at.isoformat() if user.created_at else None,
        "updated_at": user.updated_at.isoformat() if user.updated_at else None,
    }


@router.get("/users")
@router.get("/users/list")
@router.get("/user/list")
def list_users(
    search: Optional[str] = Query(None, description="Search by name, email, phone number, or username"),
    role: Optional[str] = Query(None, description="Filter by role: 'admin' or 'user'"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    limit: Optional[int] = Query(None, description="Limit results"),
    offset: Optional[int] = Query(None, description="Offset results"),
    db: Session = Depends(get_db),
):
    query = db.query(User)

    if role:
        query = query.filter(User.role.ilike(role.strip()))

    if is_active is not None:
        query = query.filter(User.is_active == is_active)

    if search:
        pat = f"%{search.strip()}%"
        query = query.filter(
            or_(
                User.full_name.ilike(pat),
                User.email.ilike(pat),
                User.phone_number.like(pat),
                User.username.ilike(pat),
            )
        )

    total_count = query.count()
    query = query.order_by(User.id.asc())

    if offset is not None:
        query = query.offset(offset)
    if limit is not None:
        query = query.limit(limit)

    users = query.all()
    results = [format_user_response(u) for u in users]
    return {
        "count": total_count,
        "users": results,
        "results": results,
    }


@router.get("/users/{user_id}")
@router.get("/user/{user_id}")
def get_user_details(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found",
        )
    return {
        "message": "User details fetched successfully",
        "user": format_user_response(user),
    }


# ==============================================================================
# CATEGORY ENDPOINTS
# ==============================================================================

def save_uploaded_image(file: UploadFile) -> str:
    upload_dir = Path("uploads") / "categories"
    upload_dir.mkdir(parents=True, exist_ok=True)

    extension = Path(file.filename).suffix.lower() if file.filename else ".jpg"
    unique_name = f"{uuid.uuid4().hex}{extension}"
    destination = upload_dir / unique_name

    with destination.open("wb") as buffer:
        while True:
            chunk = file.file.read(1024 * 1024)
            if not chunk:
                break
            buffer.write(chunk)

    return f"/uploads/categories/{unique_name}"


@router.post("/categories", status_code=status.HTTP_201_CREATED)
async def create_category(
    category_name: str = Form(...),
    category_code: str = Form(...),
    category_type: str = Form(...),
    description: str = Form(default=""),
    display_order: int = Form(default=0),
    status: str = Form(default="active"),
    image: UploadFile | None = File(default=None),
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    cleaned_name = category_name.strip()
    cleaned_code = category_code.strip()
    cleaned_type = category_type.strip().lower().replace("_", " ").replace("-", " ")
    cleaned_status = status.strip().lower()

    if len(cleaned_name) < 2:
        raise HTTPException(status_code=400, detail="Category name must be at least 2 characters long")
    if len(cleaned_code) < 2:
        raise HTTPException(status_code=400, detail="Category code must be at least 2 characters long")

    allowed_types = {"lift", "generator", "panel", "earthing", "service", "other", "lift generator"}
    if cleaned_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Category type must be one of: lift, generator, panel, earthing, service, other",
        )

    if cleaned_status not in {"active", "inactive"}:
        raise HTTPException(status_code=400, detail="Status must be active or inactive")

    if display_order < 0:
        raise HTTPException(status_code=400, detail="Display order must be numeric and not negative")

    if db.query(Category).filter(Category.category_code == cleaned_code).first():
        raise HTTPException(status_code=400, detail="Category code already exists")

    image_path = None
    if image is not None and image.filename:
        image_path = save_uploaded_image(image)

    category = Category(
        category_name=cleaned_name,
        category_code=cleaned_code,
        category_type=cleaned_type,
        category_image=image_path,
        description=description.strip() if description else None,
        display_order=display_order,
        status=cleaned_status,
    )
    db.add(category)
    db.commit()
    db.refresh(category)

    return {
        "message": "Category created successfully",
        "category": {
            "id": category.id,
            "category_name": category.category_name,
            "category_code": category.category_code,
            "category_type": category.category_type,
            "category_image": category.category_image,
            "description": category.description,
            "display_order": category.display_order,
            "status": category.status,
        },
    }


@router.get("/category/list")
@router.get("/categories/list")
@router.get("/categories")
def list_categories(
    category_type_id: Optional[Union[int, str]] = Query(None),
    category_type: Optional[str] = Query(None),
    type_id: Optional[Union[int, str]] = Query(None),
    type: Optional[str] = Query(None),
    category_id: Optional[Union[int, str]] = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(Category)

    target_type = None
    raw_type_id = category_type_id or type_id
    if raw_type_id is not None and str(raw_type_id).strip().isdigit():
        tid = int(str(raw_type_id).strip())
        if tid in DOC_NUMERIC_TYPE_MAP:
            target_type = DOC_NUMERIC_TYPE_MAP[tid]

    if not target_type:
        raw_type = category_type or type
        if raw_type:
            cleaned = str(raw_type).strip().lower()
            if cleaned in CATEGORY_TYPE_MAP:
                target_type = CATEGORY_TYPE_MAP[cleaned]
            elif cleaned.isdigit() and int(cleaned) in DOC_NUMERIC_TYPE_MAP:
                target_type = DOC_NUMERIC_TYPE_MAP[int(cleaned)]
            else:
                target_type = cleaned

    if not target_type and category_id is not None:
        cid_str = str(category_id).strip().lower()
        if cid_str in CATEGORY_TYPE_MAP:
            target_type = CATEGORY_TYPE_MAP[cid_str]
        elif cid_str.isdigit() and int(cid_str) in DOC_NUMERIC_TYPE_MAP:
            target_type = DOC_NUMERIC_TYPE_MAP[int(cid_str)]

    if target_type:
        query = query.filter(Category.category_type == target_type)

    categories = query.order_by(Category.display_order.asc(), Category.id.asc()).all()
    results = [
        {
            "id": item.id,
            "category_name_id": item.id,
            "category_id": item.id,
            "category_name": item.category_name,
            "category_code": item.category_code,
            "category_type_id": CATEGORY_TYPE_TO_ID.get((item.category_type or "").lower().strip()),
            "category_type": item.category_type,
            "category_image": item.category_image,
            "description": item.description,
            "display_order": item.display_order,
            "status": item.status,
        }
        for item in categories
    ]
    resp = {
        "count": len(results),
        "categories": results,
        "results": results,
    }
    if target_type:
        resp["category_type"] = target_type
        resp["category_type_id"] = CATEGORY_TYPE_TO_ID.get(target_type)
    return resp


@router.get("/category/{category_id}")
@router.get("/categories/{category_id}")
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    return {
        "id": category.id,
        "category_name": category.category_name,
        "category_code": category.category_code,
        "category_type": category.category_type,
        "category_image": category.category_image,
        "description": category.description,
        "display_order": category.display_order,
        "status": category.status,
    }


# ==============================================================================
# PRODUCT HELPERS
# ==============================================================================

def save_product_image(file: UploadFile) -> str:
    upload_dir = Path("uploads") / "products"
    upload_dir.mkdir(parents=True, exist_ok=True)

    extension = Path(file.filename).suffix.lower() if file.filename else ".jpg"
    unique_name = f"{uuid.uuid4().hex}{extension}"
    destination = upload_dir / unique_name

    with destination.open("wb") as buffer:
        while True:
            chunk = file.file.read(1024 * 1024)
            if not chunk:
                break
            buffer.write(chunk)

    return f"/uploads/products/{unique_name}"


async def parse_product_request(request: Request, model_cls):
    """
    Parses incoming request whether it is application/json or multipart/form-data.
    Returns (validated_model_instance, optional_image_file).
    """
    content_type = request.headers.get("content-type", "").lower()

    if "application/json" in content_type:
        try:
            body = await request.json()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid JSON payload: {str(e)}",
            )
        try:
            return model_cls(**body), None
        except Exception as e:
            if hasattr(e, "errors"):
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.errors())
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))

    if "multipart/form-data" in content_type or "application/x-www-form-urlencoded" in content_type:
        try:
            form_data = await request.form()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid form data: {str(e)}",
            )

        payload = {}
        image_file = None
        for key, value in form_data.multi_items():
            if hasattr(value, "filename") and value.filename:
                image_file = value
            elif key in ("image", "product_image") and hasattr(value, "filename") and value.filename:
                image_file = value
            else:
                if key in payload:
                    if isinstance(payload[key], list):
                        payload[key].append(value)
                    else:
                        payload[key] = [payload[key], value]
                else:
                    payload[key] = value

        if "specifications" in payload and isinstance(payload["specifications"], str):
            try:
                payload["specifications"] = json.loads(payload["specifications"])
            except Exception:
                pass

        try:
            return model_cls(**payload), image_file
        except Exception as e:
            if hasattr(e, "errors"):
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.errors())
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Content-Type must be application/json or multipart/form-data",
    )


CATEGORY_TYPE_TO_ID = {
    "lift": 1,
    "generator": 2,
    "panel": 3,
    "earthing": 4,
    "service": 5,
    "other": 6,
}


def format_product_response(product: Product) -> dict:
    type_slug = (product.category_type or "").lower().strip()
    type_id = CATEGORY_TYPE_TO_ID.get(type_slug)
    return {
        "id": product.id,
        "product_id": product.id,
        "category_type_id": type_id,
        "category_type": product.category_type,
        "category_name_id": product.category_id,
        "category_id": product.category_id,
        "category_name": product.category_name,
        "product_name": product.product_name,
        "product_code": product.product_code,
        "brand": product.brand,
        "model_number": product.model_number,
        "description": product.description,
        "purchase_price": product.purchase_price,
        "selling_price": product.selling_price,
        "discount": product.discount,
        "gst_rate": product.gst_rate,
        "hsn_code": product.hsn_code,
        "inventory_tracking": product.inventory_tracking,
        "stock": product.stock,
        "unit": product.unit,
        "min_stock": product.min_stock,
        "warranty_period": product.warranty_period,
        "warranty_terms": product.warranty_terms,
        "payment_terms": product.payment_terms,
        "product_image": product.product_image,
        "status": product.status,
        "specifications": product.specifications or {},
        "created_at": product.created_at.isoformat() if product.created_at else None,
        "updated_at": product.updated_at.isoformat() if product.updated_at else None,
    }


def save_new_product(
    db: Session,
    category_type: str,
    payload,
    image_file: Optional[UploadFile] = None,
) -> Product:
    code = payload.product_code.strip()
    if db.query(Product).filter(Product.product_code == code).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Product with code '{code}' already exists",
        )

    cat_id = payload.category_id
    cat_name = payload.category_name
    if cat_id:
        category = db.query(Category).filter(Category.id == cat_id).first()
        if category and not cat_name:
            cat_name = category.category_name

    image_path = payload.product_image
    if image_file and image_file.filename:
        image_path = save_product_image(image_file)

    specs = payload.extract_specifications()

    product = Product(
        category_type=category_type.lower().strip(),
        category_id=cat_id,
        category_name=cat_name,
        product_name=payload.product_name.strip(),
        product_code=code,
        brand=payload.brand.strip() if payload.brand else None,
        model_number=payload.model_number.strip() if payload.model_number else None,
        description=payload.description.strip() if payload.description else None,
        purchase_price=payload.purchase_price,
        selling_price=payload.selling_price,
        discount=payload.discount.strip() if payload.discount else None,
        gst_rate=payload.gst_rate.strip() if payload.gst_rate else None,
        hsn_code=payload.hsn_code.strip() if payload.hsn_code else None,
        inventory_tracking=payload.inventory_tracking,
        stock=payload.stock if payload.stock is not None else 0.0,
        unit=payload.unit.strip() if payload.unit else None,
        min_stock=payload.min_stock if payload.min_stock is not None else 0.0,
        warranty_period=payload.warranty_period.strip() if payload.warranty_period else None,
        warranty_terms=payload.warranty_terms.strip() if payload.warranty_terms else None,
        payment_terms=payload.payment_terms.strip() if payload.payment_terms else None,
        product_image=image_path,
        status=payload.status,
        specifications=specs,
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


# ==============================================================================
# 6 CATEGORY TYPE PRODUCT SUBMISSION APIS
# ==============================================================================

# 1. LIFT PRODUCT SUBMISSION API
@router.post("/products/lift", status_code=status.HTTP_201_CREATED)
async def create_lift_product(
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Submit a Lift product with complete general, shaft, electrical, cabin/door specifications and safety features.
    Accepts JSON or multipart/form-data (with optional image file).
    """
    payload, image_file = await parse_product_request(request, LiftProductCreateRequest)
    product = save_new_product(db, "lift", payload, image_file)
    return {
        "message": "Lift product created successfully",
        "product": format_product_response(product),
    }


# 2. GENERATOR (DG) PRODUCT SUBMISSION API
@router.post("/products/generator", status_code=status.HTTP_201_CREATED)
async def create_generator_product(
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Submit a Generator (DG) product with general rating, engine, alternator, and control panel specifications.
    Accepts JSON or multipart/form-data (with optional image file).
    """
    payload, image_file = await parse_product_request(request, GeneratorProductCreateRequest)
    product = save_new_product(db, "generator", payload, image_file)
    return {
        "message": "Generator product created successfully",
        "product": format_product_response(product),
    }


# 3. PANEL PRODUCT SUBMISSION API
@router.post("/products/panel", status_code=status.HTTP_201_CREATED)
async def create_panel_product(
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Submit an Electrical Panel product with construction, busbar, and cable/wiring specifications.
    Accepts JSON or multipart/form-data (with optional image file).
    """
    payload, image_file = await parse_product_request(request, PanelProductCreateRequest)
    product = save_new_product(db, "panel", payload, image_file)
    return {
        "message": "Panel product created successfully",
        "product": format_product_response(product),
    }


# 4. EARTHING PRODUCT SUBMISSION API
@router.post("/products/earthing", status_code=status.HTTP_201_CREATED)
async def create_earthing_product(
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Submit an Earthing product with earthing type and specification details.
    Accepts JSON or multipart/form-data (with optional image file).
    """
    payload, image_file = await parse_product_request(request, EarthingProductCreateRequest)
    product = save_new_product(db, "earthing", payload, image_file)
    return {
        "message": "Earthing product created successfully",
        "product": format_product_response(product),
    }


# 5. SERVICE PRODUCT SUBMISSION API
@router.post("/products/service", status_code=status.HTTP_201_CREATED)
async def create_service_product(
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Submit a Service product (AMC/CMC/Repair/Installation) with contract terms, coverage, and service checklist.
    Accepts JSON or multipart/form-data (with optional image file).
    """
    payload, image_file = await parse_product_request(request, ServiceProductCreateRequest)
    product = save_new_product(db, "service", payload, image_file)
    return {
        "message": "Service product created successfully",
        "product": format_product_response(product),
    }


# 6. OTHER PRODUCT SUBMISSION API
@router.post("/products/other", status_code=status.HTTP_201_CREATED)
async def create_other_product(
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Submit an Other product with custom specifications.
    Accepts JSON or multipart/form-data (with optional image file).
    """
    payload, image_file = await parse_product_request(request, OtherProductCreateRequest)
    product = save_new_product(db, "other", payload, image_file)
    return {
        "message": "Other product created successfully",
        "product": format_product_response(product),
    }


# ==============================================================================
# CATEGORY-SPECIFIC LISTING ENDPOINTS
# ==============================================================================

@router.get("/products/lift")
def list_lift_products(db: Session = Depends(get_db)):
    products = db.query(Product).filter(Product.category_type == "lift").order_by(Product.id.desc()).all()
    formatted = [format_product_response(p) for p in products]
    return {
        "count": len(formatted),
        "category_type": "lift",
        "products": formatted,
        "results": formatted,
    }


@router.get("/products/generator")
def list_generator_products(db: Session = Depends(get_db)):
    products = db.query(Product).filter(Product.category_type == "generator").order_by(Product.id.desc()).all()
    formatted = [format_product_response(p) for p in products]
    return {
        "count": len(formatted),
        "category_type": "generator",
        "products": formatted,
        "results": formatted,
    }


@router.get("/products/panel")
def list_panel_products(db: Session = Depends(get_db)):
    products = db.query(Product).filter(Product.category_type == "panel").order_by(Product.id.desc()).all()
    formatted = [format_product_response(p) for p in products]
    return {
        "count": len(formatted),
        "category_type": "panel",
        "products": formatted,
        "results": formatted,
    }


@router.get("/products/earthing")
def list_earthing_products(db: Session = Depends(get_db)):
    products = db.query(Product).filter(Product.category_type == "earthing").order_by(Product.id.desc()).all()
    formatted = [format_product_response(p) for p in products]
    return {
        "count": len(formatted),
        "category_type": "earthing",
        "products": formatted,
        "results": formatted,
    }


@router.get("/products/service")
def list_service_products(db: Session = Depends(get_db)):
    products = db.query(Product).filter(Product.category_type == "service").order_by(Product.id.desc()).all()
    formatted = [format_product_response(p) for p in products]
    return {
        "count": len(formatted),
        "category_type": "service",
        "products": formatted,
        "results": formatted,
    }


@router.get("/products/other")
def list_other_products(db: Session = Depends(get_db)):
    products = db.query(Product).filter(Product.category_type == "other").order_by(Product.id.desc()).all()
    formatted = [format_product_response(p) for p in products]
    return {
        "count": len(formatted),
        "category_type": "other",
        "products": formatted,
        "results": formatted,
    }


# ==============================================================================
# GENERAL PRODUCT ENDPOINTS
# ==============================================================================

CATEGORY_TYPE_MAP = {
    "lift": "lift",
    "lifts": "lift",
    "elevator": "lift",
    "elevators": "lift",
    "passenger lift": "lift",
    "generator": "generator",
    "generators": "generator",
    "dg": "generator",
    "dg set": "generator",
    "silent dg": "generator",
    "diesel generator": "generator",
    "silent generator": "generator",
    "panel": "panel",
    "panels": "panel",
    "lt panel": "panel",
    "lt panels": "panel",
    "distribution panel": "panel",
    "earthing": "earthing",
    "earth": "earthing",
    "service": "service",
    "services": "service",
    "amc": "service",
    "maintenance": "service",
    "other": "other",
    "others": "other",
}

# Fallback for 1-6 only if numeric ID is not found in the categories table
DOC_NUMERIC_TYPE_MAP = {
    1: "lift",
    2: "generator",
    3: "panel",
    4: "earthing",
    5: "service",
    6: "other",
}


@router.get("/products")
@router.get("/products/details")
@router.get("/product/details")
@router.get("/quotations/product-details")
@router.get("/quotation/add_product")
@router.post("/quotation/add_product")
@router.get("/quotations/add_product")
@router.post("/quotations/add_product")
@router.get("/quotation/add-product")
@router.post("/quotation/add-product")
@router.get("/quotations/add-product")
@router.post("/quotations/add-product")
async def list_products(
    request: Request,
    category_type_id: Optional[Union[int, str]] = Query(None),
    category_type: Optional[str] = Query(None),
    category_name_id: Optional[Union[int, str]] = Query(None),
    category_id: Optional[Union[int, str]] = Query(None),
    category: Optional[Union[int, str]] = Query(None),
    category_name: Optional[str] = Query(None),
    product_id: Optional[Union[int, str]] = Query(None),
    id: Optional[Union[int, str]] = Query(None),
    type_id: Optional[Union[int, str]] = Query(None),
    type: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    body_data = {}
    content_type = request.headers.get("content-type", "").lower()
    try:
        if "application/json" in content_type:
            body_data = await request.json()
        elif "multipart/form-data" in content_type or "application/x-www-form-urlencoded" in content_type:
            form_data = await request.form()
            body_data = dict(form_data)
    except Exception:
        body_data = {}

    raw_prod_id = (
        product_id
        or id
        or request.query_params.get("product_id")
        or request.query_params.get("id")
        or body_data.get("product_id")
        or body_data.get("id")
    )

    # If a specific product_id is requested, return that product's full details as a single clean object
    if raw_prod_id is not None and str(raw_prod_id).strip().isdigit():
        prod_id_int = int(str(raw_prod_id).strip())
        product = db.query(Product).filter(Product.id == prod_id_int).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product with ID {raw_prod_id} not found")

        return format_product_response(product)

    raw_cat_type = (
        category_type_id
        or type_id
        or category_type
        or type
        or request.query_params.get("category_type_id")
        or request.query_params.get("type_id")
        or request.query_params.get("category_type")
        or request.query_params.get("type")
        or body_data.get("category_type_id")
        or body_data.get("type_id")
        or body_data.get("category_type")
        or body_data.get("type")
    )
    raw_cat_id = (
        category_name_id
        or category_id
        or request.query_params.get("category_name_id")
        or request.query_params.get("category_id")
        or body_data.get("category_name_id")
        or body_data.get("category_id")
    )
    raw_category = (
        category
        or category_name
        or request.query_params.get("category")
        or request.query_params.get("category_name")
        or body_data.get("category")
        or body_data.get("category_name")
    )

    query = db.query(Product)
    matched_category_type = None
    category_obj = None

    # Check if category_type_id was provided as a numeric ID (1-6)
    if raw_cat_type is not None and str(raw_cat_type).strip().isdigit():
        tid = int(str(raw_cat_type).strip())
        if tid in DOC_NUMERIC_TYPE_MAP:
            matched_category_type = DOC_NUMERIC_TYPE_MAP[tid]

    # Determine if a numeric category ID was provided for category name
    numeric_cat_id = None
    if raw_cat_id is not None and str(raw_cat_id).strip().isdigit():
        numeric_cat_id = int(str(raw_cat_id).strip())
    elif raw_category is not None and str(raw_category).strip().isdigit():
        numeric_cat_id = int(str(raw_category).strip())

    if numeric_cat_id is not None:
        # Priority 1: Check database Category table by primary key
        category_obj = db.query(Category).filter(Category.id == numeric_cat_id).first()
        if category_obj:
            matched_category_type = category_obj.category_type
            query = query.filter(
                or_(
                    Product.category_id == category_obj.id,
                    Product.category_name.ilike(category_obj.category_name.strip()),
                    and_(
                        Product.category_id.is_(None),
                        Product.category_type == category_obj.category_type,
                    ),
                )
            )
        elif numeric_cat_id in DOC_NUMERIC_TYPE_MAP:
            # Fallback to canonical type 1-6 if ID doesn't exist in DB
            matched_category_type = DOC_NUMERIC_TYPE_MAP[numeric_cat_id]
            query = query.filter(Product.category_type == matched_category_type)
        else:
            query = query.filter(Product.category_id == numeric_cat_id)
    else:
        # Priority 2: Match string category name or category type
        if matched_category_type:
            query = query.filter(Product.category_type == matched_category_type)
        else:
            str_val = None
            for candidate in [raw_cat_type, raw_cat_id, raw_category]:
                if candidate is not None and str(candidate).strip():
                    str_val = str(candidate).strip()
                    break

            if str_val:
                cleaned = str_val.lower()
                if cleaned in CATEGORY_TYPE_MAP:
                    matched_category_type = CATEGORY_TYPE_MAP[cleaned]
                    query = query.filter(Product.category_type == matched_category_type)
                else:
                    # Check dynamic category table by name or type
                    category_obj = (
                        db.query(Category)
                        .filter(
                            or_(
                                Category.category_name.ilike(str_val),
                                Category.category_type.ilike(cleaned),
                            )
                        )
                        .first()
                    )
                    if category_obj:
                        matched_category_type = category_obj.category_type
                        query = query.filter(
                            or_(
                                Product.category_id == category_obj.id,
                                Product.category_name.ilike(category_obj.category_name.strip()),
                                and_(
                                    Product.category_id.is_(None),
                                    Product.category_type == category_obj.category_type,
                                ),
                            )
                        )
                    else:
                        query = query.filter(
                            or_(
                                Product.category_type.ilike(cleaned),
                                Product.category_name.ilike(f"%{str_val}%"),
                            )
                        )

    # Optional status filter
    resolved_status = status or request.query_params.get("status") or body_data.get("status")
    if resolved_status:
        query = query.filter(Product.status.ilike(str(resolved_status).strip()))

    # Optional search filter
    resolved_search = search or request.query_params.get("search") or body_data.get("search")
    if resolved_search:
        search_pattern = f"%{str(resolved_search).strip()}%"
        query = query.filter(
            or_(
                Product.product_name.ilike(search_pattern),
                Product.product_code.ilike(search_pattern),
                Product.brand.ilike(search_pattern),
                Product.model_number.ilike(search_pattern),
            )
        )

    products = query.order_by(Product.id.desc()).all()
    formatted_products = [format_product_response(p) for p in products]

    response_data = {
        "count": len(formatted_products),
        "products": formatted_products,
        "results": formatted_products,
    }
    if matched_category_type:
        response_data["category_type"] = matched_category_type
        response_data["category_type_id"] = CATEGORY_TYPE_TO_ID.get((matched_category_type or "").lower().strip())
    if category_obj:
        response_data["category_name_id"] = category_obj.id
        response_data["category_id"] = category_obj.id
        response_data["category_name"] = category_obj.category_name

    return response_data


@router.get("/categories/{category_id}/products")
@router.get("/category/{category_id}/products")
@router.get("/products/category/{category_id}")
@router.get("/quotations/products-by-category/{category_id}")
def get_products_by_category(
    category_id: str,
    status: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    """
    Fetch all products with full details (specifications, price, brand, etc.)
    by Category ID (e.g. 4, 5) or Category Type (e.g. lift, generator).
    """
    cleaned_id = str(category_id).strip().lower()
    category_obj = None
    target_type = None
    category_name = None

    if cleaned_id.isdigit():
        cat_id_int = int(cleaned_id)
        category_obj = db.query(Category).filter(Category.id == cat_id_int).first()
        if category_obj:
            target_type = category_obj.category_type
            category_name = category_obj.category_name
            query = db.query(Product).filter(
                or_(
                    Product.category_id == cat_id_int,
                    Product.category_name.ilike(category_obj.category_name.strip()),
                    and_(
                        Product.category_id.is_(None),
                        Product.category_type == category_obj.category_type,
                    ),
                )
            )
        elif cat_id_int in DOC_NUMERIC_TYPE_MAP:
            target_type = DOC_NUMERIC_TYPE_MAP[cat_id_int]
            category_name = target_type.capitalize()
            query = db.query(Product).filter(Product.category_type == target_type)
        else:
            raise HTTPException(status_code=404, detail=f"Category with ID {category_id} not found")
    elif cleaned_id in CATEGORY_TYPE_MAP:
        target_type = CATEGORY_TYPE_MAP[cleaned_id]
        category_name = target_type.capitalize()
        query = db.query(Product).filter(Product.category_type == target_type)
    else:
        category_obj = (
            db.query(Category)
            .filter(
                or_(
                    Category.category_name.ilike(category_id.strip()),
                    Category.category_type.ilike(cleaned_id),
                )
            )
            .first()
        )
        if category_obj:
            target_type = category_obj.category_type
            category_name = category_obj.category_name
            query = db.query(Product).filter(
                or_(
                    Product.category_id == category_obj.id,
                    Product.category_name.ilike(category_obj.category_name.strip()),
                    and_(
                        Product.category_id.is_(None),
                        Product.category_type == category_obj.category_type,
                    ),
                )
            )
        else:
            query = db.query(Product).filter(
                or_(
                    Product.category_type.ilike(cleaned_id),
                    Product.category_name.ilike(f"%{category_id.strip()}%"),
                )
            )
            target_type = cleaned_id
            category_name = cleaned_id.capitalize()

    if status:
        query = query.filter(Product.status.ilike(status.strip()))

    if search:
        search_pat = f"%{search.strip()}%"
        query = query.filter(
            or_(
                Product.product_name.ilike(search_pat),
                Product.product_code.ilike(search_pat),
                Product.brand.ilike(search_pat),
                Product.model_number.ilike(search_pat),
            )
        )

    products = query.order_by(Product.id.desc()).all()
    formatted_products = [format_product_response(p) for p in products]

    resp = {
        "count": len(formatted_products),
        "products": formatted_products,
        "results": formatted_products,
    }
    if target_type:
        resp["category_type"] = target_type
    if category_name:
        resp["category_name"] = category_name
    if category_obj:
        resp["category_id"] = category_obj.id

    return resp


@router.get("/products/{product_id}")
@router.get("/quotations/product-details/{product_id}")
@router.get("/quotations/products/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return format_product_response(product)


@router.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()
    return {"message": f"Product '{product.product_name}' deleted successfully"}


# ==============================================================================
# QUOTATION HELPERS & ENDPOINTS
# ==============================================================================

def format_quotation_response(quotation: Quotation) -> dict:
    return {
        "id": quotation.id,
        "quotation_no": quotation.quotation_no,
        "quotation_date": quotation.quotation_date,
        "valid_till": quotation.valid_till,
        "reference": quotation.reference,
        "customer_name": quotation.customer_name,
        "address": quotation.address,
        "phone": quotation.phone,
        "email": quotation.email,
        "items": quotation.items or [],
        "subtotal": quotation.subtotal,
        "discount_type": quotation.discount_type,
        "discount_value": quotation.discount_value,
        "discount_amount": quotation.discount_amount,
        "tax_type": quotation.tax_type,
        "tax_rate": quotation.tax_rate,
        "taxable_amount": quotation.taxable_amount,
        "tax_amount": quotation.tax_amount,
        "grand_total": quotation.grand_total,
        "terms": quotation.terms,
        "status": quotation.status,
        "created_at": quotation.created_at.isoformat() if quotation.created_at else None,
        "updated_at": quotation.updated_at.isoformat() if quotation.updated_at else None,
    }


def format_user_quotation_detail_response(quotation: Quotation) -> dict:
    """
    Formats quotation data to directly power UserQuotationDetailScreen in Flutter.
    Provides:
    - Top-level keys for direct Flutter indexing (id, status, statusColor, category, icon, iconColor, date, time, validTill, amount)
    - company object (M/s. POWER SOLUTION.COM ENTERPRISES official details)
    - customer object (name, phone, email, address)
    - items array (item, description, qty, rate, total)
    - pricing_summary (subtotal, GST 18%, grand_total)
    - terms_and_conditions list
    - actions (download_pdf_url, share_url)
    """
    st = (quotation.status or "Draft").strip()
    if st.lower() in ["approved", "accepted", "confirmed"]:
        status_color = "green"
        status_color_hex = "#10B981"
    elif st.lower() in ["sent", "submitted"]:
        status_color = "blue"
        status_color_hex = "#3B82F6"
    elif st.lower() in ["pending", "draft", "in review"]:
        status_color = "orange"
        status_color_hex = "#F59E0B"
    elif st.lower() in ["rejected", "cancelled", "declined"]:
        status_color = "red"
        status_color_hex = "#EF4444"
    else:
        status_color = "blue"
        status_color_hex = "#3B82F6"

    cat = (quotation.category or "Lift").strip()
    if "lift" in cat.lower():
        icon_name = "elevator"
    elif "generator" in cat.lower():
        icon_name = "bolt"
    elif "panel" in cat.lower():
        icon_name = "dashboard"
    elif "earthing" in cat.lower():
        icon_name = "shield"
    else:
        icon_name = "receipt_long"

    formatted_amount = format_currency_inr(quotation.grand_total or 0.0)

    # Process items table
    raw_items = quotation.items or []
    if isinstance(raw_items, str):
        try:
            import json
            raw_items = json.loads(raw_items)
        except Exception:
            raw_items = []

    formatted_items = []
    for item in raw_items:
        if isinstance(item, dict):
            item_title = (
                item.get("item")
                or item.get("name")
                or item.get("product_name")
                or item.get("product")
                or "Quotation Item"
            )
            item_desc = (
                item.get("description")
                or item.get("desc")
                or item.get("specification")
                or item.get("category")
                or ""
            )
            qty_val = item.get("qty") if item.get("qty") is not None else item.get("quantity", 1)
            try:
                qty_num = float(qty_val)
                qty_str = str(int(qty_num)) if qty_num.is_integer() else str(qty_num)
            except Exception:
                qty_str = str(qty_val)
                qty_num = 1.0

            rate_val = float(item.get("rate") or item.get("unit_price") or item.get("price") or 0.0)
            tot_val = float(
                item.get("total")
                or item.get("total_price")
                or item.get("amount")
                or (rate_val * qty_num)
            )

            formatted_items.append({
                "item": str(item_title),
                "description": str(item_desc),
                "desc": str(item_desc),
                "qty": qty_str,
                "quantity": qty_num,
                "rate": rate_val,
                "unit_price": rate_val,
                "formatted_rate": format_currency_inr(rate_val),
                "total": format_currency_inr(tot_val),
                "formatted_total": format_currency_inr(tot_val),
                "amount": tot_val,
            })

    # Terms and conditions
    default_terms = [
        "This quotation is valid till the above mentioned validity date.",
        "50% advance required before installation.",
        "Delivery & Installation time: 7-10 working days.",
        "Warranty as per company policy.",
    ]
    if quotation.terms and quotation.terms.strip():
        parsed_terms = [
            t.strip().lstrip("•*- ").strip()
            for t in quotation.terms.splitlines()
            if t.strip()
        ]
        terms_list = parsed_terms if parsed_terms else default_terms
    else:
        terms_list = default_terms

    subtotal = float(quotation.subtotal or quotation.grand_total or 0.0)
    tax_amount = float(quotation.tax_amount or 0.0)
    grand_total = float(quotation.grand_total or subtotal)

    server_base = "http://192.168.1.54:8000"
    q_no = quotation.quotation_no

    return {
        "id": q_no,
        "db_id": quotation.id,
        "quotation_id": q_no,
        "quotation_no": q_no,
        "status": st,
        "statusColor": status_color,
        "status_color": status_color,
        "status_color_hex": status_color_hex,
        "icon": icon_name,
        "iconColor": "blue",
        "icon_color": "blue",
        "category": cat,
        "date": quotation.quotation_date or "",
        "quotation_date": quotation.quotation_date or "",
        "time": quotation.quotation_time or "10:30 AM",
        "quotation_time": quotation.quotation_time or "10:30 AM",
        "validTill": quotation.valid_till or "",
        "valid_till": quotation.valid_till or "",
        "amount": formatted_amount,
        "grand_total": grand_total,
        "formatted_amount": formatted_amount,
        "company": {
            "company_name": "M/s. POWER SOLUTION.COM ENTERPRISES",
            "gstn": "20EGHPS4942E1ZH",
            "email": "POWERSOLUTIONDG3@GMAIL.COM",
            "iso_certificate": "ISO 9001:2015 QMS-25111206",
            "electric_license_no": "JH/EC/5382",
            "registered_address": "SOLANKI , SINGHMORE, HATIA ,RANCHI JHARKHAND PIN CODE 834003",
            "representative": "Mr./Ms. ________________",
        },
        "customer": {
            "name": quotation.customer_name or "",
            "phone": quotation.phone or "",
            "email": quotation.email or "",
            "address": quotation.address or "",
        },
        "customer_name": quotation.customer_name or "",
        "customer_phone": quotation.phone or "",
        "customer_email": quotation.email or "",
        "customer_address": quotation.address or "",
        "items": formatted_items,
        "pricing_summary": {
            "subtotal": subtotal,
            "formatted_subtotal": format_currency_inr(subtotal),
            "tax_type": quotation.tax_type or "GST (18%)",
            "tax_rate": float(quotation.tax_rate or 0.18),
            "tax_amount": tax_amount,
            "formatted_tax": format_currency_inr(tax_amount),
            "discount_type": quotation.discount_type or "Flat",
            "discount_amount": float(quotation.discount_amount or 0.0),
            "formatted_discount": format_currency_inr(float(quotation.discount_amount or 0.0)),
            "grand_total": grand_total,
            "formatted_grand_total": formatted_amount,
        },
        "terms_and_conditions": terms_list,
        "terms": "\n".join(terms_list),
        "representation": "Represented by Mr./Ms. ________________,",
        "actions": {
            "download_pdf_url": f"{server_base}/api/quotations/{q_no}/pdf",
            "share_url": f"{server_base}/api/quotations/{q_no}/share",
        },
        "download_pdf_url": f"{server_base}/api/quotations/{q_no}/pdf",
        "share_url": f"{server_base}/api/quotations/{q_no}/share",
        "user_id": quotation.user_id,
        "created_at": quotation.created_at.isoformat() if quotation.created_at else None,
        "updated_at": quotation.updated_at.isoformat() if quotation.updated_at else None,
    }


def generate_quotation_no(db: Session) -> str:
    from datetime import datetime
    date_str = datetime.now().strftime("%y%m%d")
    prefix = f"QTN-{date_str}-"
    last_q = (
        db.query(Quotation)
        .filter(Quotation.quotation_no.like(f"{prefix}%"))
        .order_by(Quotation.id.desc())
        .first()
    )
    if last_q and last_q.quotation_no:
        try:
            last_seq = int(last_q.quotation_no.split("-")[-1])
            new_seq = last_seq + 1
        except Exception:
            new_seq = 1
    else:
        new_seq = 1

    while db.query(Quotation).filter(Quotation.quotation_no == f"{prefix}{new_seq:04d}").first():
        new_seq += 1

    return f"{prefix}{new_seq:04d}"


@router.get("/quotations/next-number")
@router.get("/quotations/next-quotation-number")
def get_next_quotation_number(db: Session = Depends(get_db)):
    """Generate the next sequential quotation number in QTN-YYMMDD-XXXX format."""
    next_no = generate_quotation_no(db)
    return {"quotation_no": next_no}


@router.post("/quotations/calculate")
async def calculate_quotation(
    request: Request,
    db: Session = Depends(get_db),
):
    """Live calculation preview for quotation items, discount, tax, and grand total."""
    try:
        payload = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON body")

    raw_items = payload.get("items") or []
    subtotal = 0.0
    for item in raw_items:
        if isinstance(item, dict):
            qty = float(item.get("quantity") or item.get("qty") or 1)
            price = float(item.get("unit_price") or item.get("price") or 0.0)
            subtotal += qty * price

    subtotal = round(subtotal, 2)
    discount_type = str(payload.get("discount_type") or "Flat").strip()
    discount_value = float(payload.get("discount_value") or 0.0)
    if discount_type == "%":
        discount_amount = round(subtotal * discount_value / 100.0, 2)
    else:
        discount_amount = round(discount_value, 2)
    discount_amount = min(subtotal, discount_amount)

    taxable_amount = max(0.0, round(subtotal - discount_amount, 2))
    tax_rate = float(payload.get("tax_rate") or 18.0)
    if tax_rate > 1:
        tax_rate = tax_rate / 100.0
    tax_amount = round(taxable_amount * tax_rate, 2)
    grand_total = round(taxable_amount + tax_amount, 2)

    return {
        "subtotal": subtotal,
        "discount_amount": discount_amount,
        "taxable_amount": taxable_amount,
        "tax_rate": tax_rate,
        "tax_amount": tax_amount,
        "grand_total": grand_total,
    }


async def extract_quotation_payload(request: Request) -> QuotationCreateRequest:
    content_type = request.headers.get("content-type", "").lower()
    data: dict = {}

    if "application/json" in content_type:
        try:
            data = await request.json()
        except Exception as e:
            raise HTTPException(status_code=422, detail=f"Invalid JSON body: {str(e)}")
    elif "multipart/form-data" in content_type or "application/x-www-form-urlencoded" in content_type:
        form = await request.form()
        data = dict(form)
    else:
        # Fallback: try JSON first, then Form
        try:
            data = await request.json()
        except Exception:
            try:
                form = await request.form()
                data = dict(form)
            except Exception:
                data = {}

    if not data:
        raise HTTPException(status_code=422, detail="Request body cannot be empty")

    if isinstance(data.get("items"), str):
        try:
            data["items"] = json.loads(data["items"])
        except Exception as e:
            raise HTTPException(status_code=422, detail=f"Invalid JSON in 'items': {str(e)}")

    try:
        return QuotationCreateRequest.model_validate(data)
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))


def process_quotation_items(items, db: Session):
    formatted_items = []
    computed_subtotal = 0.0

    for item in items:
        qty = float(item.quantity)
        u_price = float(item.unit_price)

        # Attempt auto-enrichment from product database if product_id or product is provided
        prod_obj = None
        item_prod_id = getattr(item, "product_id", None)
        if item_prod_id:
            prod_obj = db.query(Product).filter(Product.id == item_prod_id).first()
        elif getattr(item, "product", None):
            prod_candidate = str(item.product).strip()
            prod_obj = db.query(Product).filter(
                or_(
                    Product.product_code == prod_candidate,
                    Product.product_name.ilike(prod_candidate),
                )
            ).first()
            if not prod_obj and prod_candidate.isdigit():
                prod_obj = db.query(Product).filter(Product.id == int(prod_candidate)).first()

        item_specs = getattr(item, "specifications", None) or {}
        item_prod_name = getattr(item, "product_name", None) or item.product
        item_brand = getattr(item, "brand", None)
        item_model = getattr(item, "model_number", None)
        item_desc = getattr(item, "description", None)
        item_image = getattr(item, "product_image", None)
        item_cat_id = getattr(item, "category_id", None)

        if prod_obj:
            if not item_specs and prod_obj.specifications:
                item_specs = prod_obj.specifications
            if (not getattr(item, "product_name", None) or item.product_name == item.product) and prod_obj.product_name:
                item_prod_name = prod_obj.product_name
            if u_price == 0.0 and prod_obj.selling_price:
                u_price = float(prod_obj.selling_price)
            if not item_brand and prod_obj.brand:
                item_brand = prod_obj.brand
            if not item_model and prod_obj.model_number:
                item_model = prod_obj.model_number
            if not item_desc and prod_obj.description:
                item_desc = prod_obj.description
            if not item_image and prod_obj.product_image:
                item_image = prod_obj.product_image
            if not item_cat_id and prod_obj.category_id:
                item_cat_id = prod_obj.category_id
            if not item_prod_id:
                item_prod_id = prod_obj.id

        t_price = round(qty * u_price, 2)
        computed_subtotal += t_price

        formatted_items.append({
            "type": item.type,
            "category": item.category,
            "category_id": item_cat_id,
            "product": item.product,
            "product_id": item_prod_id,
            "product_name": item_prod_name,
            "brand": item_brand,
            "model_number": item_model,
            "description": item_desc,
            "product_image": item_image,
            "specifications": item_specs,
            "quantity": qty,
            "unit_price": u_price,
            "total_price": t_price,
        })

    return formatted_items, computed_subtotal


@router.post("/quotations", status_code=status.HTTP_201_CREATED)
async def create_quotation(request: Request, db: Session = Depends(get_db)):
    """
    Create a new quotation (Draft or Sent).
    Supports BOTH multipart/form-data and application/json.
    - customer_name is a freeform text input field.
    - All pricing (subtotal, discount, taxable amount, tax amount, grand total) is computed reliably.
    """
    payload = await extract_quotation_payload(request)

    # Quotation Number: Use provided or auto-generate
    qtn_no = (payload.quotation_no or "").strip()
    if not qtn_no:
        qtn_no = generate_quotation_no(db)
    else:
        existing = db.query(Quotation).filter(Quotation.quotation_no == qtn_no).first()
        if existing:
            qtn_no = generate_quotation_no(db)

    # Process items and compute subtotal
    formatted_items, computed_subtotal = process_quotation_items(payload.items, db)

    # Subtotal
    subtotal = (
        round(payload.subtotal, 2)
        if (payload.subtotal is not None and payload.subtotal > 0)
        else round(computed_subtotal, 2)
    )

    # Discount
    discount_type = payload.discount_type.strip() if payload.discount_type else "Flat"
    if discount_type not in ["Flat", "%"]:
        discount_type = "Flat"
    discount_value = round(float(payload.discount_value or 0.0), 2)

    if discount_type == "%":
        discount_amount = round(subtotal * discount_value / 100.0, 2)
    else:
        discount_amount = round(discount_value, 2)

    if discount_amount > subtotal:
        discount_amount = subtotal

    # Taxable Amount
    taxable_amount = max(0.0, round(subtotal - discount_amount, 2))

    # Tax calculation
    tax_type = (payload.tax_type or "GST 18%").strip()
    tax_rates = {
        "GST 5%": 0.05,
        "GST 12%": 0.12,
        "GST 18%": 0.18,
        "GST 28%": 0.28,
    }
    tax_rate = (
        payload.tax_rate
        if (payload.tax_rate is not None and payload.tax_rate > 0)
        else tax_rates.get(tax_type, 0.18)
    )
    tax_amount = round(taxable_amount * tax_rate, 2)

    # Grand Total
    grand_total = round(taxable_amount + tax_amount, 2)

    # Status
    status_val = (payload.status or "Draft").strip().capitalize()
    if status_val not in ["Draft", "Sent", "Approved", "Rejected"]:
        status_val = "Draft"

    quotation = Quotation(
        quotation_no=qtn_no,
        quotation_date=payload.quotation_date.strip(),
        valid_till=payload.valid_till.strip(),
        reference=payload.reference.strip() if payload.reference else None,
        customer_name=payload.customer_name.strip(),
        address=payload.address.strip() if payload.address else None,
        phone=payload.phone.strip() if payload.phone else None,
        email=payload.email.strip() if payload.email else None,
        items=formatted_items,
        subtotal=subtotal,
        discount_type=discount_type,
        discount_value=discount_value,
        discount_amount=discount_amount,
        tax_type=tax_type,
        tax_rate=tax_rate,
        taxable_amount=taxable_amount,
        tax_amount=tax_amount,
        grand_total=grand_total,
        terms=payload.terms.strip() if payload.terms else None,
        status=status_val,
    )

    db.add(quotation)
    db.commit()
    db.refresh(quotation)

    return {
        "message": f"Quotation '{quotation.quotation_no}' saved successfully",
        "quotation": format_quotation_response(quotation),
    }


@router.get("/quotations")
def list_quotations(
    status: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    """
    List quotations with optional status filter and text search.
    Search matches quotation_no, customer_name, reference, or phone.
    """
    query = db.query(Quotation)

    if status:
        query = query.filter(Quotation.status.ilike(status.strip()))

    if search:
        search_pat = f"%{search.strip()}%"
        query = query.filter(
            or_(
                Quotation.quotation_no.ilike(search_pat),
                Quotation.customer_name.ilike(search_pat),
                Quotation.reference.ilike(search_pat),
                Quotation.phone.ilike(search_pat),
            )
        )

    quotations = query.order_by(Quotation.id.desc()).all()
    return {
        "count": len(quotations),
        "results": [format_quotation_response(q) for q in quotations],
    }


# ──────────────────────────────────────────────────────────────────────────────
# USER QUOTATION DASHBOARD & DETAIL ENDPOINTS (UserQuotationDetailScreen)
# ──────────────────────────────────────────────────────────────────────────────

@router.get("/quotations/dashboard")
@router.get("/quotations/user-dashboard")
def get_user_quotation_dashboard(
    search: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Dedicated endpoint for User Quotation Dashboard in Flutter.
    Bearer token is compulsory (Authorization: Bearer <token>).
    Strictly calculates summary analytics cards and returns quotation records ONLY for the authenticated user.
    """
    query = db.query(Quotation)

    if getattr(current_user, "role", "") != "admin":
        clean_phone = "".join(ch for ch in (current_user.phone_number or "") if ch.isdigit())
        user_filters = [Quotation.user_id == current_user.id]
        legacy_conditions = []
        if current_user.email:
            legacy_conditions.append(Quotation.email.ilike(current_user.email.strip()))
        if clean_phone and len(clean_phone) >= 10:
            legacy_conditions.append(Quotation.phone.like(f"%{clean_phone[-10:]}%"))
        if current_user.full_name:
            legacy_conditions.append(Quotation.customer_name.ilike(current_user.full_name.strip()))
        if legacy_conditions:
            user_filters.append(and_(Quotation.user_id.is_(None), or_(*legacy_conditions)))

        query = query.filter(or_(*user_filters))

    if status:
        st = status.strip().lower()
        if st in ["approved", "accepted"]:
            query = query.filter(or_(Quotation.status.ilike("Approved"), Quotation.status.ilike("Accepted")))
        elif st in ["sent", "submitted"]:
            query = query.filter(or_(Quotation.status.ilike("Sent"), Quotation.status.ilike("Submitted")))
        elif st in ["pending", "draft"]:
            query = query.filter(or_(Quotation.status.ilike("Pending"), Quotation.status.ilike("Draft")))
        elif st in ["rejected", "declined"]:
            query = query.filter(or_(Quotation.status.ilike("Rejected"), Quotation.status.ilike("Declined")))
        else:
            query = query.filter(Quotation.status.ilike(f"%{status.strip()}%"))

    if category:
        query = query.filter(Quotation.category.ilike(f"%{category.strip()}%"))

    if search:
        pat = f"%{search.strip()}%"
        query = query.filter(
            or_(
                Quotation.quotation_no.ilike(pat),
                Quotation.customer_name.ilike(pat),
                Quotation.category.ilike(pat),
                Quotation.status.ilike(pat),
                Quotation.quotation_date.ilike(pat),
            )
        )

    all_quotations = query.order_by(Quotation.id.desc()).all()

    total_count = len(all_quotations)
    total_amount = sum(float(q.grand_total or 0.0) for q in all_quotations)

    approved_list = [q for q in all_quotations if (q.status or "").lower() in ["approved", "accepted"]]
    approved_count = len(approved_list)
    approved_amount = sum(float(q.grand_total or 0.0) for q in approved_list)

    sent_list = [q for q in all_quotations if (q.status or "").lower() in ["sent", "submitted"]]
    sent_count = len(sent_list)
    sent_amount = sum(float(q.grand_total or 0.0) for q in sent_list)

    pending_list = [q for q in all_quotations if (q.status or "").lower() in ["pending", "draft", "in review"]]
    pending_count = len(pending_list)
    pending_amount = sum(float(q.grand_total or 0.0) for q in pending_list)

    formatted_quotations = [format_user_quotation_detail_response(q) for q in all_quotations]

    return {
        "summary": {
            "total_quotations": {
                "title": "Total Quotations",
                "count": str(total_count),
                "amount": total_amount,
                "formatted_amount": format_currency_inr(total_amount),
            },
            "approved": {
                "title": "Approved",
                "count": str(approved_count),
                "amount": approved_amount,
                "formatted_amount": format_currency_inr(approved_amount),
            },
            "sent": {
                "title": "Sent",
                "count": str(sent_count),
                "amount": sent_amount,
                "formatted_amount": format_currency_inr(sent_amount),
            },
            "pending": {
                "title": "Pending",
                "count": str(pending_count),
                "amount": pending_amount,
                "formatted_amount": format_currency_inr(pending_amount),
            },
        },
        "quotations": formatted_quotations,
        "count": total_count,
    }


@router.get("/quotations/detail/{quotation_id}")
@router.get("/quotations/{quotation_id}")
def get_user_quotation_detail(
    quotation_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Dedicated endpoint for UserQuotationDetailScreen in Flutter.
    Bearer token is compulsory (Authorization: Bearer <token>).
    Fetches full quotation details by alphanumeric quotation_no (e.g., QTN-250517-0001) or database integer ID.
    Strictly verifies ownership: users can only view their own quotations.
    """
    q = None
    if quotation_id.isdigit():
        q = db.query(Quotation).filter(Quotation.id == int(quotation_id)).first()
    if not q:
        q = db.query(Quotation).filter(Quotation.quotation_no.ilike(quotation_id.strip())).first()

    if not q:
        raise HTTPException(status_code=404, detail="Quotation not found")

    if getattr(current_user, "role", "") != "admin":
        clean_phone = "".join(ch for ch in (current_user.phone_number or "") if ch.isdigit())
        user_name = (current_user.full_name or "").strip().lower()
        q_name = (q.customer_name or "").strip().lower()
        user_email = (current_user.email or "").strip().lower()
        q_email = (q.email or "").strip().lower()

        belongs = (
            q.user_id == current_user.id
            or (user_name and user_name == q_name)
            or (user_email and user_email == q_email)
            or (clean_phone and clean_phone[-10:] in (q.phone or ""))
        )
        if not belongs:
            raise HTTPException(status_code=403, detail="You do not have permission to view this quotation")

    return format_user_quotation_detail_response(q)


@router.get("/quotations/{quotation_id}/pdf")
def get_quotation_pdf(
    quotation_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Returns PDF download metadata / link for the quotation.
    Bearer token is compulsory.
    """
    q = None
    if quotation_id.isdigit():
        q = db.query(Quotation).filter(Quotation.id == int(quotation_id)).first()
    if not q:
        q = db.query(Quotation).filter(Quotation.quotation_no.ilike(quotation_id.strip())).first()

    if not q:
        raise HTTPException(status_code=404, detail="Quotation not found")

    if getattr(current_user, "role", "") != "admin":
        clean_phone = "".join(ch for ch in (current_user.phone_number or "") if ch.isdigit())
        user_name = (current_user.full_name or "").strip().lower()
        q_name = (q.customer_name or "").strip().lower()
        user_email = (current_user.email or "").strip().lower()
        q_email = (q.email or "").strip().lower()

        belongs = (
            q.user_id == current_user.id
            or (user_name and user_name == q_name)
            or (user_email and user_email == q_email)
            or (clean_phone and clean_phone[-10:] in (q.phone or ""))
        )
        if not belongs:
            raise HTTPException(status_code=403, detail="You do not have permission to view this quotation")

    return {
        "quotation_id": q.quotation_no,
        "file_name": f"{q.quotation_no}.pdf",
        "file_size": "142 KB",
        "mime_type": "application/pdf",
        "status": "Ready",
        "download_url": f"http://192.168.1.54:8000/api/quotations/{q.quotation_no}/pdf",
        "generated_at": q.updated_at.isoformat() if q.updated_at else datetime.now().isoformat(),
    }


@router.get("/quotations/{quotation_id}/share")
def share_quotation(
    quotation_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Returns shareable link and text summary for the quotation.
    Bearer token is compulsory.
    """
    q = None
    if quotation_id.isdigit():
        q = db.query(Quotation).filter(Quotation.id == int(quotation_id)).first()
    if not q:
        q = db.query(Quotation).filter(Quotation.quotation_no.ilike(quotation_id.strip())).first()

    if not q:
        raise HTTPException(status_code=404, detail="Quotation not found")

    if getattr(current_user, "role", "") != "admin":
        clean_phone = "".join(ch for ch in (current_user.phone_number or "") if ch.isdigit())
        user_name = (current_user.full_name or "").strip().lower()
        q_name = (q.customer_name or "").strip().lower()
        user_email = (current_user.email or "").strip().lower()
        q_email = (q.email or "").strip().lower()

        belongs = (
            q.user_id == current_user.id
            or (user_name and user_name == q_name)
            or (user_email and user_email == q_email)
            or (clean_phone and clean_phone[-10:] in (q.phone or ""))
        )
        if not belongs:
            raise HTTPException(status_code=403, detail="You do not have permission to view this quotation")

    formatted_tot = format_currency_inr(q.grand_total)
    return {
        "quotation_id": q.quotation_no,
        "share_url": f"http://192.168.1.54:8000/quotations/view/{q.quotation_no}",
        "share_text": f"Quotation {q.quotation_no} for {q.customer_name} of {formatted_tot} from Power Solution Enterprises.",
    }


@router.put("/quotations/{quotation_id}")
async def update_quotation(
    quotation_id: str,
    request: Request,
    db: Session = Depends(get_db),
):
    """Update an existing quotation. Supports BOTH multipart/form-data and application/json."""
    quotation = None
    if quotation_id.isdigit():
        quotation = db.query(Quotation).filter(Quotation.id == int(quotation_id)).first()
    if not quotation:
        quotation = db.query(Quotation).filter(Quotation.quotation_no.ilike(quotation_id.strip())).first()

    if not quotation:
        raise HTTPException(status_code=404, detail="Quotation not found")

    payload = await extract_quotation_payload(request)

    # Process items and compute subtotal
    formatted_items, computed_subtotal = process_quotation_items(payload.items, db)

    subtotal = (
        round(payload.subtotal, 2)
        if (payload.subtotal is not None and payload.subtotal > 0)
        else round(computed_subtotal, 2)
    )

    discount_type = payload.discount_type.strip() if payload.discount_type else "Flat"
    if discount_type not in ["Flat", "%"]:
        discount_type = "Flat"
    discount_value = round(float(payload.discount_value or 0.0), 2)

    if discount_type == "%":
        discount_amount = round(subtotal * discount_value / 100.0, 2)
    else:
        discount_amount = round(discount_value, 2)

    if discount_amount > subtotal:
        discount_amount = subtotal

    taxable_amount = max(0.0, round(subtotal - discount_amount, 2))

    tax_type = (payload.tax_type or "GST 18%").strip()
    tax_rates = {
        "GST 5%": 0.05,
        "GST 12%": 0.12,
        "GST 18%": 0.18,
        "GST 28%": 0.28,
    }
    tax_rate = (
        payload.tax_rate
        if (payload.tax_rate is not None and payload.tax_rate > 0)
        else tax_rates.get(tax_type, 0.18)
    )
    tax_amount = round(taxable_amount * tax_rate, 2)
    grand_total = round(taxable_amount + tax_amount, 2)

    # Update fields
    quotation.quotation_date = payload.quotation_date.strip()
    quotation.valid_till = payload.valid_till.strip()
    quotation.reference = payload.reference.strip() if payload.reference else None
    quotation.customer_name = payload.customer_name.strip()
    quotation.address = payload.address.strip() if payload.address else None
    quotation.phone = payload.phone.strip() if payload.phone else None
    quotation.email = payload.email.strip() if payload.email else None
    quotation.items = formatted_items
    quotation.subtotal = subtotal
    quotation.discount_type = discount_type
    quotation.discount_value = discount_value
    quotation.discount_amount = discount_amount
    quotation.tax_type = tax_type
    quotation.tax_rate = tax_rate
    quotation.taxable_amount = taxable_amount
    quotation.tax_amount = tax_amount
    quotation.grand_total = grand_total
    quotation.terms = payload.terms.strip() if payload.terms else quotation.terms
    quotation.status = payload.status.strip() if payload.status else quotation.status

    db.commit()
    db.refresh(quotation)

    return {
        "message": f"Quotation '{quotation.quotation_no}' updated successfully",
        "quotation": format_user_quotation_detail_response(quotation),
    }


@router.delete("/quotations/{quotation_id}")
def delete_quotation(quotation_id: str, db: Session = Depends(get_db)):
    quotation = None
    if quotation_id.isdigit():
        quotation = db.query(Quotation).filter(Quotation.id == int(quotation_id)).first()
    if not quotation:
        quotation = db.query(Quotation).filter(Quotation.quotation_no.ilike(quotation_id.strip())).first()

    if not quotation:
        raise HTTPException(status_code=404, detail="Quotation not found")

    qtn_no = quotation.quotation_no
    db.delete(quotation)
    db.commit()
    return {"message": f"Quotation '{qtn_no}' deleted successfully"}


# ==============================================================================
# PAYMENT HELPERS & ENDPOINTS (FLUTTER ADD PAYMENT SCREEN)
# ==============================================================================

def save_payment_proof(file: UploadFile) -> str:
    upload_dir = Path("uploads") / "payments"
    upload_dir.mkdir(parents=True, exist_ok=True)

    file_extension = Path(file.filename).suffix
    unique_name = f"{uuid.uuid4().hex}{file_extension}"
    destination = upload_dir / unique_name

    with destination.open("wb") as buffer:
        while True:
            chunk = file.file.read(1024 * 1024)
            if not chunk:
                break
            buffer.write(chunk)

    return f"/uploads/payments/{unique_name}"


def format_payment_response(payment: Payment) -> dict:
    mode = payment.payment_mode or "Cash"
    mode_lower = mode.lower()
    if "upi" in mode_lower or "wallet" in mode_lower:
        method_icon = "wallet"
    elif any(k in mode_lower for k in ["bank", "neft", "rtgs", "transfer"]):
        method_icon = "bank"
    elif "card" in mode_lower:
        method_icon = "card"
    else:
        method_icon = "cash"

    st_raw = (payment.status or "Paid").strip()
    st_lower = st_raw.lower()
    if any(k in st_lower for k in ["paid", "received", "success", "completed"]):
        status_text = "Paid"
        status_color = "green"
    elif "partial" in st_lower:
        status_text = "Partial"
        status_color = "orange"
    else:
        status_text = "Pending"
        status_color = "red"

    amt = float(payment.amount_received or 0.0)
    pay_id = payment.payment_no or f"PAY-{payment.id:06d}"
    inv_desc = payment.invoice_desc or (f"Invoice - {payment.category}" if payment.category else "Invoice")

    return {
        "id": payment.id,
        "payment_id": pay_id,
        "payment_no": pay_id,
        "method": mode,
        "payment_mode": mode,
        "method_icon": method_icon,
        "invoice_no": payment.invoice_no,
        "order_no": payment.invoice_no,
        "invoice_id": payment.invoice_id,
        "invoice_desc": inv_desc,
        "category": payment.category or "",
        "amount": amt,
        "amount_received": amt,
        "formatted_amount": format_currency_inr(amt),
        "date": payment.payment_date,
        "payment_date": payment.payment_date,
        "time": payment.payment_time or "10:30 AM",
        "payment_time": payment.payment_time or "10:30 AM",
        "status": status_text,
        "status_color": status_color,
        "customer_name": payment.customer_name,
        "customer_phone": payment.customer_phone,
        "customer_email": payment.customer_email,
        "customer_address": payment.customer_address,
        "quotation_id": payment.quotation_id,
        "quotation_no": payment.quotation_no,
        "transaction_no": payment.transaction_no or "",
        "reference_no": payment.reference_no or "",
        "notes": payment.notes or "",
        "payment_proof": payment.payment_proof or "",
        "user_id": payment.user_id,
        "created_at": payment.created_at.isoformat() if payment.created_at else None,
        "updated_at": payment.updated_at.isoformat() if payment.updated_at else None,
    }


def generate_payment_no(db: Session) -> str:
    from datetime import datetime
    date_str = datetime.now().strftime("%y%m%d")
    prefix = f"PAY-{date_str}-"

    max_seq = 0
    last_p = (
        db.query(Payment)
        .filter(Payment.payment_no.like(f"{prefix}%"))
        .order_by(Payment.id.desc())
        .first()
    )
    if last_p and last_p.payment_no:
        try:
            max_seq = max(max_seq, int(last_p.payment_no.split("-")[-1]))
        except Exception:
            pass

    new_seq = max_seq + 1
    while db.query(Payment).filter(Payment.payment_no == f"{prefix}{new_seq:03d}").first():
        new_seq += 1

    return f"{prefix}{new_seq:03d}"


def generate_invoice_no(db: Session) -> str:
    from datetime import datetime
    date_str = datetime.now().strftime("%y%m%d")
    prefix = f"INV-{date_str}-"

    # Find highest sequence across both invoices and payments
    max_seq = 0
    last_inv = (
        db.query(Invoice)
        .filter(Invoice.invoice_no.like(f"{prefix}%"))
        .order_by(Invoice.id.desc())
        .first()
    )
    if last_inv and last_inv.invoice_no:
        try:
            max_seq = max(max_seq, int(last_inv.invoice_no.split("-")[-1]))
        except Exception:
            pass

    last_p = (
        db.query(Payment)
        .filter(Payment.invoice_no.like(f"{prefix}%"))
        .order_by(Payment.id.desc())
        .first()
    )
    if last_p and last_p.invoice_no:
        try:
            max_seq = max(max_seq, int(last_p.invoice_no.split("-")[-1]))
        except Exception:
            pass

    new_seq = max_seq + 1

    while (
        db.query(Invoice).filter(Invoice.invoice_no == f"{prefix}{new_seq:04d}").first()
        or db.query(Payment).filter(Payment.invoice_no == f"{prefix}{new_seq:04d}").first()
    ):
        new_seq += 1

    return f"{prefix}{new_seq:04d}"


@router.get("/payments/next-invoice-number")
@router.get("/payments/next-number")
@router.get("/payment/next-number")
def get_next_invoice_number(db: Session = Depends(get_db)):
    """Generate next sequential invoice/order number in INV-YYMMDD-XXXX format."""
    inv_no = generate_invoice_no(db)
    return {"invoice_no": inv_no, "order_no": inv_no}


@router.get("/payments/customers")
@router.get("/quotations/customers")
def get_customers_from_quotations(db: Session = Depends(get_db)):
    """
    Fetch distinct customers from Quotations along with their details
    and associated quotation/order references to populate the 'Select Customer' dropdown.
    """
    quotations = db.query(Quotation).order_by(Quotation.id.desc()).all()
    customers_map = {}
    for q in quotations:
        c_name = q.customer_name.strip()
        if c_name not in customers_map:
            customers_map[c_name] = {
                "customer_name": c_name,
                "phone": q.phone,
                "email": q.email,
                "address": q.address,
                "quotations": [],
            }
        customers_map[c_name]["quotations"].append({
            "id": q.id,
            "quotation_no": q.quotation_no,
            "quotation_date": q.quotation_date,
            "grand_total": q.grand_total,
            "status": q.status,
        })

    return {
        "count": len(customers_map),
        "customers": list(customers_map.values()),
        "results": list(customers_map.values()),
    }


@router.post("/payments/add", status_code=status.HTTP_201_CREATED)
@router.post("/payment/add", status_code=status.HTTP_201_CREATED)
@router.post("/payments/create", status_code=status.HTTP_201_CREATED)
@router.post("/payment/create", status_code=status.HTTP_201_CREATED)
@router.post("/payments", status_code=status.HTTP_201_CREATED)
@router.post("/payment", status_code=status.HTTP_201_CREATED)
@router.post("/add-payment", status_code=status.HTTP_201_CREATED)
async def create_payment(
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Add a new payment record from the Flutter AddPaymentScreen.
    Accepts JSON or multipart/form-data (with optional receipt file).
    Auto-generates invoice/order number if not supplied.
    Links customer details from quotation if quotation_id or quotation_no is provided.
    """
    content_type = request.headers.get("content-type", "").lower()
    payload = {}
    proof_file = None

    if "multipart/form-data" in content_type or "application/x-www-form-urlencoded" in content_type:
        form_data = await request.form()
        for key, value in form_data.items():
            if hasattr(value, "filename") and value.filename:
                proof_file = value
            else:
                payload[key] = value
    elif "application/json" in content_type:
        payload = await request.json()
    else:
        try:
            payload = await request.json()
        except Exception:
            payload = {}

    customer_name = str(
        payload.get("customer_name")
        or (payload.get("customer") if isinstance(payload.get("customer"), str) else (payload.get("customer", {}).get("name") if isinstance(payload.get("customer"), dict) else ""))
        or ""
    ).strip()

    amount_received = payload.get("amount_received")
    if amount_received is None or str(amount_received).strip() == "":
        raise HTTPException(status_code=400, detail="Amount received is required")
    try:
        amount_received = float(amount_received)
        if amount_received < 0:
            raise ValueError()
    except Exception:
        raise HTTPException(status_code=400, detail="Amount received must be a valid positive number")

    invoice_no = str(payload.get("invoice_no") or payload.get("order_no") or "").strip()
    if not invoice_no or db.query(Payment).filter(Payment.invoice_no == invoice_no).first():
        invoice_no = generate_invoice_no(db)

    # Payment date
    payment_date = str(payload.get("payment_date") or "").strip()
    if not payment_date:
        from datetime import datetime
        payment_date = datetime.now().strftime("%d %b %Y")

    payment_mode = str(payload.get("payment_mode") or "Cash").strip()
    transaction_no = str(payload.get("transaction_no") or payload.get("cheque_no") or "").strip() or None
    reference_no = str(payload.get("reference_no") or "").strip() or None
    notes = str(payload.get("notes") or "").strip() or None
    status_val = str(payload.get("status") or "Received").strip().capitalize()

    # Link quotation details if provided
    quotation_id_val = payload.get("quotation_id")
    quotation_no = str(payload.get("quotation_no") or "").strip() or None
    customer_phone = str(payload.get("customer_phone") or payload.get("phone") or payload.get("mobile") or "").strip() or None
    customer_email = str(payload.get("customer_email") or payload.get("email") or "").strip() or None
    customer_address = str(payload.get("customer_address") or payload.get("address") or payload.get("billing_address") or "").strip() or None

    q_obj = None
    if quotation_id_val is not None:
        if str(quotation_id_val).isdigit():
            q_obj = db.query(Quotation).filter(Quotation.id == int(quotation_id_val)).first()
        else:
            q_obj = db.query(Quotation).filter(Quotation.quotation_no == str(quotation_id_val).strip()).first()
    if not q_obj and quotation_no:
        q_obj = db.query(Quotation).filter(Quotation.quotation_no == quotation_no).first()

    if q_obj:
        quotation_id = q_obj.id
        quotation_no = q_obj.quotation_no
        if not customer_name:
            customer_name = q_obj.customer_name
        if not customer_phone:
            customer_phone = q_obj.phone
        if not customer_email:
            customer_email = q_obj.email
        if not customer_address:
            customer_address = q_obj.address
    else:
        quotation_id = int(quotation_id_val) if quotation_id_val and str(quotation_id_val).isdigit() else None

    if not customer_name:
        raise HTTPException(status_code=400, detail="Customer name is required")

    # Payment proof
    proof_path = str(payload.get("payment_proof") or "").strip() or None
    if proof_file and proof_file.filename:
        proof_path = save_payment_proof(proof_file)

    payment = Payment(
        invoice_no=invoice_no,
        customer_name=customer_name,
        customer_phone=customer_phone,
        customer_email=customer_email,
        customer_address=customer_address,
        quotation_id=int(quotation_id) if quotation_id and str(quotation_id).isdigit() else None,
        quotation_no=quotation_no,
        payment_date=payment_date,
        amount_received=amount_received,
        payment_mode=payment_mode,
        transaction_no=transaction_no,
        reference_no=reference_no,
        notes=notes,
        payment_proof=proof_path,
        status=status_val,
    )
    db.add(payment)
    db.commit()
    db.refresh(payment)

    return {
        "message": f"Payment '{payment.invoice_no}' saved successfully",
        "payment": format_payment_response(payment),
    }


@router.get("/payments")
def list_payments(
    search: Optional[str] = Query(None),
    customer_name: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    payment_mode: Optional[str] = Query(None),
    invoice_no: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(Payment)

    if customer_name:
        query = query.filter(Payment.customer_name.ilike(f"%{customer_name.strip()}%"))

    if status:
        query = query.filter(Payment.status.ilike(status.strip()))

    if payment_mode:
        query = query.filter(Payment.payment_mode.ilike(payment_mode.strip()))

    if invoice_no:
        query = query.filter(Payment.invoice_no.ilike(f"%{invoice_no.strip()}%"))

    if search:
        pat = f"%{search.strip()}%"
        query = query.filter(
            or_(
                Payment.customer_name.ilike(pat),
                Payment.invoice_no.ilike(pat),
                Payment.quotation_no.ilike(pat),
                Payment.transaction_no.ilike(pat),
                Payment.reference_no.ilike(pat),
            )
        )

    payments = query.order_by(Payment.id.desc()).all()
    results = [format_payment_response(p) for p in payments]
    return {
        "count": len(results),
        "payments": results,
        "results": results,
    }


# ──────────────────────────────────────────────────────────────────────────────
# User Payment Dashboard API (For UserPaymentDashboardScreen in Flutter)
# ──────────────────────────────────────────────────────────────────────────────

@router.get("/payments/dashboard")
@router.get("/payments/user-dashboard")
def get_user_payment_dashboard(
    search: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    payment_mode: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Dedicated endpoint for UserPaymentDashboardScreen in Flutter:
    Bearer token is COMPULSORY (Authorization: Bearer <token>).
    Strictly calculates summary analytics cards and returns payment transactions ONLY for the authenticated user.
    """
    query = db.query(Payment)

    # 1. Strictly isolate to the authenticated user
    clean_phone = "".join(ch for ch in (current_user.phone_number or "") if ch.isdigit())
    user_filters = [Payment.user_id == current_user.id]
    legacy_conditions = []
    if current_user.email:
        legacy_conditions.append(Payment.customer_email.ilike(current_user.email.strip()))
    if clean_phone and len(clean_phone) >= 10:
        legacy_conditions.append(Payment.customer_phone.like(f"%{clean_phone[-10:]}%"))
    if legacy_conditions:
        user_filters.append(and_(Payment.user_id.is_(None), or_(*legacy_conditions)))

    query = query.filter(or_(*user_filters))

    # 2. General Filters (Status, Payment Mode, Category)
    if status:
        st = status.strip().lower()
        if st == "paid":
            query = query.filter(or_(Payment.status.ilike("Paid"), Payment.status.ilike("Received"), Payment.status.ilike("Success"), Payment.status.ilike("Completed")))
        elif st == "partial":
            query = query.filter(Payment.status.ilike("%Partial%"))
        elif st == "pending":
            query = query.filter(or_(Payment.status.ilike("%Pending%"), Payment.status.ilike("%Failed%"), Payment.status.ilike("%Unpaid%")))
        else:
            query = query.filter(Payment.status.ilike(f"%{status.strip()}%"))

    if payment_mode:
        query = query.filter(Payment.payment_mode.ilike(f"%{payment_mode.strip()}%"))

    if category:
        query = query.filter(or_(Payment.category.ilike(f"%{category.strip()}%"), Payment.invoice_desc.ilike(f"%{category.strip()}%")))

    # 3. Global Search (Search within this user's payments)
    if search:
        pat = f"%{search.strip()}%"
        query = query.filter(
            or_(
                Payment.payment_no.ilike(pat),
                Payment.invoice_no.ilike(pat),
                Payment.transaction_no.ilike(pat),
                Payment.reference_no.ilike(pat),
                Payment.invoice_desc.ilike(pat),
                Payment.category.ilike(pat),
                Payment.payment_mode.ilike(pat),
                Payment.status.ilike(pat),
                Payment.payment_date.ilike(pat),
            )
        )

    all_payments = query.order_by(Payment.id.desc()).all()

    # Compute Summary Analytics Cards ONLY for this user's payments
    total_count = len(all_payments)
    total_amount = sum(float(p.amount_received or 0.0) for p in all_payments)

    paid_count = sum(1 for p in all_payments if (p.status or "").lower() in ["paid", "received", "success", "completed"])
    paid_amount = sum(float(p.amount_received or 0.0) for p in all_payments if (p.status or "").lower() in ["paid", "received", "success", "completed"])

    partial_count = sum(1 for p in all_payments if "partial" in (p.status or "").lower())
    partial_amount = sum(float(p.amount_received or 0.0) for p in all_payments if "partial" in (p.status or "").lower())

    pending_count = sum(1 for p in all_payments if "pending" in (p.status or "").lower() or (p.status or "").lower() in ["failed", "unpaid"])
    pending_amount = sum(float(p.amount_received or 0.0) for p in all_payments if "pending" in (p.status or "").lower() or (p.status or "").lower() in ["failed", "unpaid"])

    formatted_payments = [format_payment_response(p) for p in all_payments]

    return {
        "summary": {
            "total_payments": {
                "title": "Total Payments",
                "count": str(total_count),
                "amount": total_amount,
                "formatted_amount": format_currency_inr(total_amount),
            },
            "paid": {
                "title": "Paid",
                "count": str(paid_count),
                "amount": paid_amount,
                "formatted_amount": format_currency_inr(paid_amount),
            },
            "partial": {
                "title": "Partial",
                "count": str(partial_count),
                "amount": partial_amount,
                "formatted_amount": format_currency_inr(partial_amount),
            },
            "pending": {
                "title": "Pending",
                "count": str(pending_count),
                "amount": pending_amount,
                "formatted_amount": format_currency_inr(pending_amount),
            },
        },
        "payments": formatted_payments,
        "count": total_count,
    }


@router.get("/payments/{payment_id}")
def get_payment(
    payment_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Retrieves full details of a single payment by ID or payment_no.
    Bearer token is compulsory.
    Regular users can only view their own payments; admins can view any.
    """
    payment = None
    if payment_id.isdigit():
        payment = db.query(Payment).filter(Payment.id == int(payment_id)).first()
    if not payment:
        payment = db.query(Payment).filter(Payment.payment_no == payment_id.strip()).first()
    if not payment:
        payment = db.query(Payment).filter(Payment.invoice_no == payment_id.strip()).first()
    if not payment:
        payment = db.query(Payment).filter(Payment.transaction_no == payment_id.strip()).first()

    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    if getattr(current_user, "role", "") != "admin":
        clean_phone = "".join(ch for ch in (current_user.phone_number or "") if ch.isdigit())
        user_name = (current_user.full_name or "").strip().lower()
        p_name = (payment.customer_name or "").strip().lower()
        user_email = (current_user.email or "").strip().lower()
        p_email = (payment.customer_email or "").strip().lower()

        belongs = (
            payment.user_id == current_user.id
            or (user_name and user_name == p_name)
            or (user_email and user_email == p_email)
            or (clean_phone and clean_phone[-10:] in (payment.customer_phone or ""))
        )
        if not belongs:
            raise HTTPException(status_code=403, detail="You do not have permission to view this payment")

    return format_payment_response(payment)


@router.put("/payments/{payment_id}")
async def update_payment(
    payment_id: int,
    request: Request,
    db: Session = Depends(get_db),
):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    content_type = request.headers.get("content-type", "").lower()
    payload = {}
    proof_file = None

    if "multipart/form-data" in content_type or "application/x-www-form-urlencoded" in content_type:
        form_data = await request.form()
        for key, value in form_data.items():
            if hasattr(value, "filename") and value.filename:
                proof_file = value
            else:
                payload[key] = value
    else:
        try:
            payload = await request.json()
        except Exception:
            payload = {}

    if "customer_name" in payload and payload["customer_name"]:
        payment.customer_name = str(payload["customer_name"]).strip()
    if "customer_phone" in payload:
        payment.customer_phone = str(payload["customer_phone"]).strip() or None
    if "customer_email" in payload:
        payment.customer_email = str(payload["customer_email"]).strip() or None
    if "customer_address" in payload:
        payment.customer_address = str(payload["customer_address"]).strip() or None
    if "payment_date" in payload and payload["payment_date"]:
        payment.payment_date = str(payload["payment_date"]).strip()
    if "amount_received" in payload and payload["amount_received"] is not None:
        try:
            payment.amount_received = float(payload["amount_received"])
        except Exception:
            pass
    if "payment_mode" in payload and payload["payment_mode"]:
        payment.payment_mode = str(payload["payment_mode"]).strip()
    if "transaction_no" in payload:
        payment.transaction_no = str(payload["transaction_no"]).strip() or None
    if "reference_no" in payload:
        payment.reference_no = str(payload["reference_no"]).strip() or None
    if "notes" in payload:
        payment.notes = str(payload["notes"]).strip() or None
    if "status" in payload and payload["status"]:
        payment.status = str(payload["status"]).strip().capitalize()

    if proof_file and proof_file.filename:
        payment.payment_proof = save_payment_proof(proof_file)
    elif "payment_proof" in payload and payload["payment_proof"]:
        payment.payment_proof = str(payload["payment_proof"]).strip()

    db.commit()
    db.refresh(payment)

    return {
        "message": f"Payment '{payment.invoice_no}' updated successfully",
        "payment": format_payment_response(payment),
    }


@router.delete("/payments/{payment_id}")
def delete_payment(payment_id: int, db: Session = Depends(get_db)):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    inv_no = payment.invoice_no
    db.delete(payment)
    db.commit()
    return {"message": f"Payment '{inv_no}' deleted successfully"}


# ==============================================================================
# ORDER HELPERS & ENDPOINTS (CreateOrderScreen)
# ==============================================================================

def generate_order_no(db: Session) -> str:
    """Auto-generate sequential order number ORD-YYMMDD-XXXX"""
    from datetime import datetime
    today_prefix = f"ORD-{datetime.now().strftime('%y%m%d')}-"
    latest_order = (
        db.query(Order)
        .filter(Order.order_no.like(f"{today_prefix}%"))
        .order_by(Order.id.desc())
        .first()
    )
    if latest_order and latest_order.order_no:
        try:
            last_seq = int(latest_order.order_no.split("-")[-1])
            next_seq = last_seq + 1
        except Exception:
            next_seq = 1
    else:
        next_seq = 1

    while db.query(Order).filter(Order.order_no == f"{today_prefix}{next_seq:04d}").first():
        next_seq += 1

    return f"{today_prefix}{next_seq:04d}"


def format_order_response(order: Order) -> dict:
    customer_obj = {
        "name": order.customer_name,
        "mobile": order.mobile,
        "email": order.email,
        "billing_address": order.billing_address,
        "delivery_address": order.delivery_address,
    }
    return {
        "id": order.id,
        "order_no": order.order_no,
        "order_date": order.order_date,
        "delivery_date": order.delivery_date,
        "order_status": order.order_status,
        "quotation_id": order.quotation_id,
        "quotation_no": order.quotation_no,
        "customer_name": order.customer_name,
        "mobile": order.mobile,
        "email": order.email,
        "billing_address": order.billing_address,
        "delivery_address": order.delivery_address,
        "customer": customer_obj,
        "items": order.items or [],
        "subtotal": float(order.subtotal or 0.0),
        "discount": float(order.discount or 0.0),
        "taxable_amount": float(order.taxable_amount or 0.0),
        "tax": float(order.tax or 0.0),
        "grand_total": float(order.grand_total or 0.0),
        "advance_paid": float(order.advance_paid or 0.0),
        "balance_amount": float(order.balance_amount or 0.0),
        "special_instructions": order.special_instructions,
        "payment_status": order.payment_status,
        "payment_mode": order.payment_mode,
        "transaction_no": order.transaction_no,
        "payment_date": order.payment_date,
        "internal_notes": order.internal_notes,
        "terms_accepted": bool(order.terms_accepted),
        "created_at": order.created_at.isoformat() if order.created_at else None,
        "updated_at": order.updated_at.isoformat() if order.updated_at else None,
    }


@router.get("/orders/next-order-number")
@router.get("/orders/next-number")
def get_next_order_number(db: Session = Depends(get_db)):
    return {
        "order_no": generate_order_no(db)
    }


@router.get("/orders/quotations")
def get_order_quotations(
    status: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    """
    Returns quotations formatted to cleanly plug into the Flutter CreateOrderScreen
    dropdown and auto-fill customer, address, products with specifications, and totals.
    """
    query = db.query(Quotation)
    if status:
        query = query.filter(Quotation.status.ilike(status.strip()))
    if search:
        pat = f"%{search.strip()}%"
        query = query.filter(
            or_(
                Quotation.quotation_no.ilike(pat),
                Quotation.customer_name.ilike(pat),
                Quotation.phone.ilike(pat),
            )
        )

    quotations = query.order_by(Quotation.id.desc()).all()
    results = []
    for q in quotations:
        formatted_items = []
        for idx, it in enumerate(q.items or []):
            if isinstance(it, dict):
                formatted_items.append({
                    "id": it.get("product") or it.get("id") or f"ITEM{idx+1:03d}",
                    "name": it.get("product_name") or it.get("name") or "Product",
                    "type": it.get("type") or "Product",
                    "category": it.get("category") or "",
                    "qty": int(it.get("quantity") or it.get("qty") or 1),
                    "price": float(it.get("unit_price") or it.get("price") or 0.0),
                    "total": float(it.get("total_price") or it.get("total") or 0.0),
                    "specifications": it.get("specifications") or {},
                })

        results.append({
            "id": q.quotation_no,  # Matches Flutter's quotation['id'] for DropdownMenuItem
            "quotation_id": q.id,
            "quotation_no": q.quotation_no,
            "date": q.quotation_date,
            "customer": q.customer_name,
            "mobile": q.phone or "",
            "email": q.email or "",
            "billingAddress": q.address or "",
            "deliveryAddress": q.address or "",
            "subtotal": float(q.subtotal or 0.0),
            "discount": float(q.discount_amount or q.discount_value or 0.0),
            "tax": float(q.tax_amount or 0.0),
            "taxable_amount": float(q.taxable_amount or 0.0),
            "grandTotal": float(q.grand_total or 0.0),
            "status": q.status,
            "items": formatted_items,
        })

    return {
        "count": len(results),
        "quotations": results,
        "results": results,
    }


@router.post("/orders", status_code=status.HTTP_201_CREATED)
@router.post("/order/create", status_code=status.HTTP_201_CREATED)
async def create_order(
    request: Request,
    db: Session = Depends(get_db),
):
    try:
        payload = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON body")

    order_no = str(payload.get("order_no") or "").strip()
    if not order_no or db.query(Order).filter(Order.order_no == order_no).first():
        order_no = generate_order_no(db)

    from datetime import datetime
    order_date = str(payload.get("order_date") or datetime.now().strftime("%d %b %Y")).strip()
    delivery_date = str(payload.get("delivery_date") or "").strip() or None
    order_status_val = str(payload.get("order_status") or "Pending").strip().capitalize()

    # Quotation linkage
    quotation_id_val = payload.get("quotation_id")
    quotation_no_val = str(payload.get("quotation_no") or "").strip() or None
    q_obj = None

    if quotation_id_val is not None:
        if str(quotation_id_val).isdigit():
            q_obj = db.query(Quotation).filter(Quotation.id == int(quotation_id_val)).first()
        else:
            q_obj = db.query(Quotation).filter(Quotation.quotation_no == str(quotation_id_val).strip()).first()
    elif quotation_no_val:
        q_obj = db.query(Quotation).filter(Quotation.quotation_no == quotation_no_val).first()

    quotation_id = q_obj.id if q_obj else None
    quotation_no = q_obj.quotation_no if q_obj else (quotation_no_val or (str(quotation_id_val) if quotation_id_val and not str(quotation_id_val).isdigit() else None))

    # Customer details (nested 'customer' object or flat fields)
    customer_dict = payload.get("customer") if isinstance(payload.get("customer"), dict) else {}
    customer_name = str(customer_dict.get("name") or payload.get("customer_name") or (q_obj.customer_name if q_obj else "")).strip()
    if not customer_name:
        raise HTTPException(status_code=422, detail="Customer / Company name is required")

    mobile = str(customer_dict.get("mobile") or payload.get("mobile") or payload.get("phone") or (q_obj.phone if q_obj else "")).strip() or None
    email = str(customer_dict.get("email") or payload.get("email") or (q_obj.email if q_obj else "")).strip() or None
    billing_address = str(customer_dict.get("billing_address") or payload.get("billing_address") or payload.get("address") or (q_obj.address if q_obj else "")).strip() or None
    delivery_address = str(customer_dict.get("delivery_address") or payload.get("delivery_address") or billing_address or "").strip() or None

    # Line items
    items = payload.get("items")
    if not items and q_obj and q_obj.items:
        items = q_obj.items
    elif not items:
        items = []

    # Amounts
    subtotal = float(payload.get("subtotal") if payload.get("subtotal") is not None else (q_obj.subtotal if q_obj else 0.0))
    discount = float(payload.get("discount") if payload.get("discount") is not None else ((q_obj.discount_amount or q_obj.discount_value) if q_obj else 0.0))
    taxable_amount = float(payload.get("taxable_amount") if payload.get("taxable_amount") is not None else (max(0.0, subtotal - discount)))
    tax = float(payload.get("tax") if payload.get("tax") is not None else (q_obj.tax_amount if q_obj else 0.0))
    grand_total = float(payload.get("grand_total") if payload.get("grand_total") is not None else (q_obj.grand_total if q_obj else (taxable_amount + tax)))
    advance_paid = float(payload.get("advance_paid") or 0.0)
    balance_amount = float(payload.get("balance_amount") if payload.get("balance_amount") is not None else max(0.0, grand_total - advance_paid))

    special_instructions = str(payload.get("special_instructions") or "").strip() or None
    payment_status_val = str(payload.get("payment_status") or "Not Paid").strip()
    payment_mode_val = str(payload.get("payment_mode") or "Bank Transfer").strip()
    transaction_no = str(payload.get("transaction_no") or "").strip() or None
    payment_date = str(payload.get("payment_date") or order_date).strip() or None
    internal_notes = str(payload.get("internal_notes") or "").strip() or None
    terms_accepted = bool(payload.get("terms_accepted", True))

    order = Order(
        order_no=order_no,
        order_date=order_date,
        delivery_date=delivery_date,
        order_status=order_status_val,
        quotation_id=quotation_id,
        quotation_no=quotation_no,
        customer_name=customer_name,
        mobile=mobile,
        email=email,
        billing_address=billing_address,
        delivery_address=delivery_address,
        items=items,
        subtotal=subtotal,
        discount=discount,
        taxable_amount=taxable_amount,
        tax=tax,
        grand_total=grand_total,
        advance_paid=advance_paid,
        balance_amount=balance_amount,
        special_instructions=special_instructions,
        payment_status=payment_status_val,
        payment_mode=payment_mode_val,
        transaction_no=transaction_no,
        payment_date=payment_date,
        internal_notes=internal_notes,
        terms_accepted=terms_accepted,
    )

    db.add(order)
    db.commit()
    db.refresh(order)

    return {
        "message": f"Order '{order.order_no}' created successfully",
        "order": format_order_response(order),
    }


@router.get("/orders")
def list_orders(
    search: Optional[str] = Query(None),
    order_status: Optional[str] = Query(None),
    payment_status: Optional[str] = Query(None),
    customer_name: Optional[str] = Query(None),
    quotation_no: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(Order)

    if customer_name:
        query = query.filter(Order.customer_name.ilike(f"%{customer_name.strip()}%"))

    if order_status:
        query = query.filter(Order.order_status.ilike(order_status.strip()))

    if payment_status:
        query = query.filter(Order.payment_status.ilike(payment_status.strip()))

    if quotation_no:
        query = query.filter(Order.quotation_no.ilike(f"%{quotation_no.strip()}%"))

    if search:
        pat = f"%{search.strip()}%"
        query = query.filter(
            or_(
                Order.order_no.ilike(pat),
                Order.customer_name.ilike(pat),
                Order.quotation_no.ilike(pat),
                Order.mobile.ilike(pat),
                Order.transaction_no.ilike(pat),
            )
        )

    orders = query.order_by(Order.id.desc()).all()
    results = [format_order_response(o) for o in orders]
    return {
        "count": len(results),
        "orders": results,
        "results": results,
    }


@router.get("/orders/{order_id}")
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return format_order_response(order)


@router.put("/orders/{order_id}")
async def update_order(
    order_id: int,
    request: Request,
    db: Session = Depends(get_db),
):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    try:
        payload = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON body")

    if "order_status" in payload and payload["order_status"]:
        order.order_status = str(payload["order_status"]).strip().capitalize()
    if "delivery_date" in payload:
        order.delivery_date = str(payload["delivery_date"]).strip() or None
    if "delivery_address" in payload:
        order.delivery_address = str(payload["delivery_address"]).strip() or None
    if "advance_paid" in payload and payload["advance_paid"] is not None:
        order.advance_paid = float(payload["advance_paid"])
        order.balance_amount = max(0.0, order.grand_total - order.advance_paid)
    if "payment_status" in payload and payload["payment_status"]:
        order.payment_status = str(payload["payment_status"]).strip()
    if "payment_mode" in payload and payload["payment_mode"]:
        order.payment_mode = str(payload["payment_mode"]).strip()
    if "transaction_no" in payload:
        order.transaction_no = str(payload["transaction_no"]).strip() or None
    if "payment_date" in payload:
        order.payment_date = str(payload["payment_date"]).strip() or None
    if "special_instructions" in payload:
        order.special_instructions = str(payload["special_instructions"]).strip() or None
    if "internal_notes" in payload:
        order.internal_notes = str(payload["internal_notes"]).strip() or None
    if "terms_accepted" in payload:
        order.terms_accepted = bool(payload["terms_accepted"])

    db.commit()
    db.refresh(order)

    return {
        "message": f"Order '{order.order_no}' updated successfully",
        "order": format_order_response(order),
    }


@router.delete("/orders/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    ord_no = order.order_no
    db.delete(order)
    db.commit()
    return {"message": f"Order '{ord_no}' deleted successfully"}


# ==============================================================================
# CASH BILL HELPERS & ENDPOINTS (GenerateCashBillScreen)
# ==============================================================================

def generate_bill_no(db: Session) -> str:
    """Auto-generate sequential cash bill number CB-YYMMDD-XXXX"""
    from datetime import datetime
    today_prefix = f"CB-{datetime.now().strftime('%y%m%d')}-"
    latest_bill = (
        db.query(CashBill)
        .filter(CashBill.bill_no.like(f"{today_prefix}%"))
        .order_by(CashBill.id.desc())
        .first()
    )
    if latest_bill and latest_bill.bill_no:
        try:
            last_seq = int(latest_bill.bill_no.split("-")[-1])
            next_seq = last_seq + 1
        except Exception:
            next_seq = 1
    else:
        next_seq = 1

    while db.query(CashBill).filter(CashBill.bill_no == f"{today_prefix}{next_seq:04d}").first():
        next_seq += 1

    return f"{today_prefix}{next_seq:04d}"


def compute_cash_bill_totals(items: list, discount: float = 0.0, amount_paid: float = 0.0) -> dict:
    """
    Computes exact cash bill math:
    Subtotal = sum(qty * price)
    Taxable Amount = max(0, Subtotal - Discount)
    GST (18%) = Taxable Amount * 0.18
    Grand Total = Taxable Amount + GST
    Change Returned = max(0, Amount Paid - Grand Total)
    Balance Amount = max(0, Grand Total - Amount Paid)
    """
    subtotal = 0.0
    formatted_items = []

    for idx, item in enumerate(items or []):
        if not isinstance(item, dict):
            continue
        qty = float(item.get("qty") or item.get("quantity") or 1)
        price = float(item.get("price") or item.get("unit_price") or 0.0)
        item_total = round(qty * price, 2)
        subtotal += item_total

        formatted_items.append({
            "id": str(item.get("id") or f"ITEM{idx+1:03d}"),
            "name": str(item.get("name") or item.get("product_name") or "Product"),
            "type": str(item.get("type") or "Other"),
            "category": str(item.get("category") or ""),
            "price": price,
            "qty": int(qty),
            "total": item_total,
            "specifications": item.get("specifications") if isinstance(item.get("specifications"), dict) else {},
        })

    subtotal = round(subtotal, 2)
    discount_val = max(0.0, float(discount or 0.0))
    taxable_amount = max(0.0, round(subtotal - discount_val, 2))
    gst_rate = 0.18
    gst_amount = round(taxable_amount * gst_rate, 2)
    grand_total = round(taxable_amount + gst_amount, 2)
    paid = max(0.0, float(amount_paid or 0.0))

    if paid >= grand_total:
        change_returned = round(paid - grand_total, 2)
        balance_amount = 0.0
        payment_status = "Paid"
    else:
        change_returned = 0.0
        balance_amount = round(grand_total - paid, 2)
        payment_status = "Partially Paid" if paid > 0 else "Unpaid"

    return {
        "items": formatted_items,
        "subtotal": subtotal,
        "discount": discount_val,
        "taxable_amount": taxable_amount,
        "gst_rate": gst_rate,
        "gst_amount": gst_amount,
        "gst": gst_amount,
        "grand_total": grand_total,
        "amount_paid": paid,
        "change_returned": change_returned,
        "balance_amount": balance_amount,
        "payment_status": payment_status,
    }


def format_cash_bill_response(bill: CashBill) -> dict:
    return {
        "id": bill.id,
        "bill_no": bill.bill_no,
        "bill_date": bill.bill_date,
        "customer_type": bill.customer_type,
        "customer_name": bill.customer_name,
        "mobile": bill.mobile,
        "items": bill.items or [],
        "subtotal": float(bill.subtotal or 0.0),
        "discount": float(bill.discount or 0.0),
        "taxable_amount": float(bill.taxable_amount or 0.0),
        "gst_rate": float(bill.gst_rate or 0.18),
        "gst_amount": float(bill.gst_amount or 0.0),
        "gst": float(bill.gst_amount or 0.0),
        "grand_total": float(bill.grand_total or 0.0),
        "payment_mode": bill.payment_mode,
        "amount_paid": float(bill.amount_paid or 0.0),
        "change_returned": float(bill.change_returned or 0.0),
        "balance_amount": float(bill.balance_amount or 0.0),
        "payment_status": bill.payment_status,
        "notes": bill.notes,
        "status": bill.status,
        "created_at": bill.created_at.isoformat() if bill.created_at else None,
        "updated_at": bill.updated_at.isoformat() if bill.updated_at else None,
    }


@router.get("/cash-bills/next-bill-number")
@router.get("/cash-bills/next-number")
def get_next_cash_bill_number(db: Session = Depends(get_db)):
    return {
        "bill_no": generate_bill_no(db)
    }


@router.get("/cash-bills/product-picker")
@router.get("/cash-bills/products")
def get_cash_bill_product_picker(db: Session = Depends(get_db)):
    """
    Returns the exact hierarchical product master required by the
    GenerateCashBillScreen modal bottom sheet:
    - product_types
    - categories (grouped by product_type)
    - products (grouped by category_name)
    """
    default_types = ["Lift", "Generator", "LT Panel", "Earthing", "Service", "Other"]

    default_categories = {
        "Lift": ["Passenger Lift", "Goods Lift", "Hospital Lift", "Home Lift"],
        "Generator": ["Silent Generator", "Open Generator"],
        "LT Panel": ["Main LT Panel", "AMF Panel", "PCC Panel", "MCC Panel"],
        "Earthing": ["Earth Pit", "Chemical Earthing", "GI Earthing"],
        "Service": ["Lift AMC", "DG AMC", "Electrical Service", "Other Service"],
        "Other": ["Other Product"],
    }

    # Query all active products from DB
    db_products = db.query(Product).filter(Product.status == "active").all()

    # Pre-populate products dictionary with categories
    products_by_category = {}
    for cat_list in default_categories.values():
        for cat in cat_list:
            products_by_category[cat] = []

    # Map DB products to their respective categories
    for p in db_products:
        cat_name = p.category_name or "Other Product"
        type_name = str(p.category_type or "Other").capitalize()
        if type_name == "Lt panel" or type_name == "Panel":
            type_name = "LT Panel"

        if cat_name not in products_by_category:
            products_by_category[cat_name] = []

        products_by_category[cat_name].append({
            "id": p.product_code or f"PROD{p.id:03d}",
            "name": p.product_name,
            "price": float(p.selling_price or 0.0),
            "type": type_name,
            "category": cat_name,
            "specifications": p.specifications or {},
        })

    # Fallback/standard items if DB category is empty
    defaults = {
        "Passenger Lift": [{
            "id": "LIFT001",
            "name": "G+2 Automatic Passenger Lift",
            "price": 450000.0,
            "type": "Lift",
            "category": "Passenger Lift",
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
            }
        }],
        "Silent Generator": [{
            "id": "DG001",
            "name": "Silent DG 60 KVA",
            "price": 650000.0,
            "type": "Generator",
            "category": "Silent Generator",
            "specifications": {
                "Rating": "60 KVA / 48 KW",
                "Output Voltage": "430 V",
                "Phase": "3 Phase",
                "Frequency": "50 Hz",
                "Engine": "4 Cylinder",
                "RPM": "1500",
                "Cooling": "Liquid Cooled",
                "Alternator": "Meccalte / CG",
                "Voltage Control": "AVR",
                "Control Panel": "AMF",
            }
        }],
        "Main LT Panel": [{
            "id": "PANEL001",
            "name": "Main LT Panel",
            "price": 185000.0,
            "type": "LT Panel",
            "category": "Main LT Panel",
            "specifications": {
                "Panel Type": "Main LT Panel",
                "Construction": "Floor Mounted",
                "Sheet Thickness": "2.0 MM",
                "Busbar": "Copper",
                "Busbar Insulator": "FRP / SMC",
                "Earth Busbar": "Copper",
                "Cable Entry": "Bottom",
                "Gland Plate": "3 MM",
                "Painting": "Powder Coated",
            }
        }],
        "Earth Pit": [{
            "id": "EARTH001",
            "name": "Chemical Earthing Earth Pit",
            "price": 12500.0,
            "type": "Earthing",
            "category": "Earth Pit",
            "specifications": {
                "Earthing Type": "Chemical Earthing",
                "Electrode": "GI / Copper",
                "Earth Pit": "Maintenance Free",
                "Back Fill Compound": "Chemical Compound",
                "Connection": "Heavy Duty",
            }
        }],
        "Lift AMC": [{
            "id": "AMC001",
            "name": "Passenger Lift AMC - 1 Year",
            "price": 7500.0,
            "type": "Service",
            "category": "Lift AMC",
            "specifications": {
                "Service Type": "Lift AMC",
                "Period": "1 Year",
                "Coverage": "Preventive Maintenance",
                "Equipment": "Passenger Lift",
            }
        }],
        "DG AMC": [{
            "id": "AMC002",
            "name": "DG AMC - 1 Year",
            "price": 12000.0,
            "type": "Service",
            "category": "DG AMC",
            "specifications": {
                "Service Type": "DG AMC",
                "Period": "1 Year",
                "Coverage": "Preventive Maintenance",
                "Equipment": "Diesel Generator",
            }
        }],
        "Electrical Service": [{
            "id": "SRV001",
            "name": "Electrical Maintenance Service",
            "price": 5000.0,
            "type": "Service",
            "category": "Electrical Service",
            "specifications": {
                "Service Type": "Electrical Service",
                "Period": "As Per Requirement",
                "Coverage": "Electrical Inspection & Maintenance",
            }
        }],
        "Other Product": [{
            "id": "OTHER001",
            "name": "Other Electrical Product",
            "price": 10000.0,
            "type": "Other",
            "category": "Other Product",
            "specifications": {
                "Product Type": "Other",
                "Description": "Electrical Product",
            }
        }]
    }

    for cat, sample_items in defaults.items():
        if cat not in products_by_category or not products_by_category[cat]:
            products_by_category[cat] = sample_items

    return {
        "product_types": default_types,
        "categories": default_categories,
        "products": products_by_category,
    }


@router.post("/cash-bills/calculate")
async def calculate_cash_bill(
    request: Request,
):
    """
    Live calculation endpoint for GenerateCashBillScreen:
    Calculates Subtotal, Taxable Amount, GST (18%), Grand Total,
    Change Returned, and Balance Amount.
    """
    try:
        payload = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON body")

    items = payload.get("items") or []
    discount = float(payload.get("discount") or 0.0)
    amount_paid = float(payload.get("amount_paid") or 0.0)

    computed = compute_cash_bill_totals(items=items, discount=discount, amount_paid=amount_paid)

    return {
        "subtotal": computed["subtotal"],
        "discount": computed["discount"],
        "taxable_amount": computed["taxable_amount"],
        "gst_rate": computed["gst_rate"],
        "gst": computed["gst_amount"],
        "grand_total": computed["grand_total"],
        "amount_paid": computed["amount_paid"],
        "change_returned": computed["change_returned"],
        "balance_amount": computed["balance_amount"],
        "payment_status": computed["payment_status"],
    }


@router.post("/cash-bills", status_code=status.HTTP_201_CREATED)
@router.post("/cash-bills/generate", status_code=status.HTTP_201_CREATED)
async def generate_cash_bill(
    request: Request,
    db: Session = Depends(get_db),
):
    try:
        payload = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON body")

    customer_name = str(payload.get("customer_name") or "").strip()
    if not customer_name:
        raise HTTPException(status_code=422, detail="Customer name is required")

    items = payload.get("items") or []
    if not items:
        raise HTTPException(status_code=422, detail="Please add at least one product")

    bill_no = str(payload.get("bill_no") or "").strip()
    if not bill_no or db.query(CashBill).filter(CashBill.bill_no == bill_no).first():
        bill_no = generate_bill_no(db)

    from datetime import datetime
    bill_date = str(payload.get("bill_date") or datetime.now().strftime("%d %b %Y")).strip()
    customer_type = str(payload.get("customer_type") or "Walk-in Customer").strip()
    mobile = str(payload.get("mobile") or "").strip() or None
    payment_mode = str(payload.get("payment_mode") or "Cash").strip()
    notes = str(payload.get("notes") or "").strip() or None
    status_val = str(payload.get("status") or "Generated").strip().capitalize()

    discount = float(payload.get("discount") or 0.0)
    amount_paid = float(payload.get("amount_paid") or 0.0)

    # Compute calculations automatically
    computed = compute_cash_bill_totals(items=items, discount=discount, amount_paid=amount_paid)

    cash_bill = CashBill(
        bill_no=bill_no,
        bill_date=bill_date,
        customer_type=customer_type,
        customer_name=customer_name,
        mobile=mobile,
        items=computed["items"],
        subtotal=computed["subtotal"],
        discount=computed["discount"],
        taxable_amount=computed["taxable_amount"],
        gst_rate=computed["gst_rate"],
        gst_amount=computed["gst_amount"],
        grand_total=computed["grand_total"],
        payment_mode=payment_mode,
        amount_paid=computed["amount_paid"],
        change_returned=computed["change_returned"],
        balance_amount=computed["balance_amount"],
        payment_status=computed["payment_status"],
        notes=notes,
        status=status_val,
    )

    db.add(cash_bill)
    db.commit()
    db.refresh(cash_bill)

    return {
        "message": f"Cash bill '{cash_bill.bill_no}' generated successfully",
        "bill": format_cash_bill_response(cash_bill),
    }


@router.get("/cash-bills")
def list_cash_bills(
    search: Optional[str] = Query(None),
    customer_name: Optional[str] = Query(None),
    customer_type: Optional[str] = Query(None),
    payment_mode: Optional[str] = Query(None),
    payment_status: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(CashBill)

    if customer_name:
        query = query.filter(CashBill.customer_name.ilike(f"%{customer_name.strip()}%"))

    if customer_type:
        query = query.filter(CashBill.customer_type.ilike(customer_type.strip()))

    if payment_mode:
        query = query.filter(CashBill.payment_mode.ilike(payment_mode.strip()))

    if payment_status:
        query = query.filter(CashBill.payment_status.ilike(payment_status.strip()))

    if status:
        query = query.filter(CashBill.status.ilike(status.strip()))

    if search:
        pat = f"%{search.strip()}%"
        query = query.filter(
            or_(
                CashBill.bill_no.ilike(pat),
                CashBill.customer_name.ilike(pat),
                CashBill.mobile.ilike(pat),
            )
        )

    bills = query.order_by(CashBill.id.desc()).all()
    results = [format_cash_bill_response(b) for b in bills]
    return {
        "count": len(results),
        "bills": results,
        "results": results,
    }


@router.get("/cash-bills/{bill_id}")
def get_cash_bill(bill_id: int, db: Session = Depends(get_db)):
    bill = db.query(CashBill).filter(CashBill.id == bill_id).first()
    if not bill:
        raise HTTPException(status_code=404, detail="Cash bill not found")
    return format_cash_bill_response(bill)


@router.put("/cash-bills/{bill_id}")
async def update_cash_bill(
    bill_id: int,
    request: Request,
    db: Session = Depends(get_db),
):
    bill = db.query(CashBill).filter(CashBill.id == bill_id).first()
    if not bill:
        raise HTTPException(status_code=404, detail="Cash bill not found")

    try:
        payload = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON body")

    if "customer_type" in payload:
        bill.customer_type = str(payload["customer_type"]).strip()
    if "customer_name" in payload and payload["customer_name"]:
        bill.customer_name = str(payload["customer_name"]).strip()
    if "mobile" in payload:
        bill.mobile = str(payload["mobile"]).strip() or None
    if "payment_mode" in payload:
        bill.payment_mode = str(payload["payment_mode"]).strip()
    if "notes" in payload:
        bill.notes = str(payload["notes"]).strip() or None
    if "status" in payload:
        bill.status = str(payload["status"]).strip().capitalize()

    # If items, discount, or amount_paid updated, recalculate everything
    items_to_use = payload.get("items") if "items" in payload else bill.items
    discount_to_use = float(payload.get("discount") if "discount" in payload else bill.discount)
    paid_to_use = float(payload.get("amount_paid") if "amount_paid" in payload else bill.amount_paid)

    computed = compute_cash_bill_totals(items=items_to_use, discount=discount_to_use, amount_paid=paid_to_use)

    bill.items = computed["items"]
    bill.subtotal = computed["subtotal"]
    bill.discount = computed["discount"]
    bill.taxable_amount = computed["taxable_amount"]
    bill.gst_rate = computed["gst_rate"]
    bill.gst_amount = computed["gst_amount"]
    bill.grand_total = computed["grand_total"]
    bill.amount_paid = computed["amount_paid"]
    bill.change_returned = computed["change_returned"]
    bill.balance_amount = computed["balance_amount"]
    bill.payment_status = computed["payment_status"]

    db.commit()
    db.refresh(bill)

    return {
        "message": f"Cash bill '{bill.bill_no}' updated successfully",
        "bill": format_cash_bill_response(bill),
    }


@router.delete("/cash-bills/{bill_id}")
def delete_cash_bill(bill_id: int, db: Session = Depends(get_db)):
    bill = db.query(CashBill).filter(CashBill.id == bill_id).first()
    if not bill:
        raise HTTPException(status_code=404, detail="Cash bill not found")

    bill_no = bill.bill_no
    db.delete(bill)
    db.commit()
    return {"message": f"Cash bill '{bill_no}' deleted successfully"}


# ==============================================================================
# PURCHASE ORDER & SUPPLIER ENDPOINTS (AddPurchaseOrderScreen)
# ==============================================================================

async def extract_request_payload(request: Request) -> dict:
    content_type = request.headers.get("content-type", "").lower()
    if "application/json" in content_type:
        try:
            return await request.json()
        except Exception:
            pass
    elif "multipart/form-data" in content_type or "application/x-www-form-urlencoded" in content_type:
        try:
            form = await request.form()
            return dict(form)
        except Exception:
            pass
    try:
        return await request.json()
    except Exception:
        try:
            form = await request.form()
            return dict(form)
        except Exception:
            return {}


def ensure_default_suppliers(db: Session):
    defaults = [
        {
            "supplier_code": "SUP001",
            "name": "ABC Electrical Pvt. Ltd.",
            "contact_person": "Rajesh Kumar",
            "mobile": "9876543210",
            "email": "sales@abcelectrical.com",
            "address": "Industrial Area, Ahmedabad, Gujarat",
        },
        {
            "supplier_code": "SUP002",
            "name": "XYZ Power Systems",
            "contact_person": "Amit Sharma",
            "mobile": "9988776655",
            "email": "info@xyzpower.com",
            "address": "GIDC Estate, Vadodara, Gujarat",
        },
        {
            "supplier_code": "SUP003",
            "name": "Power Equipment India",
            "contact_person": "Vikas Patel",
            "mobile": "9998887776",
            "email": "purchase@powerequipment.in",
            "address": "Industrial Estate, Surat, Gujarat",
        },
    ]
    for s_data in defaults:
        existing = db.query(Supplier).filter(Supplier.supplier_code == s_data["supplier_code"]).first()
        if existing:
            existing.name = s_data["name"]
            existing.contact_person = s_data["contact_person"]
            existing.mobile = s_data["mobile"]
            existing.email = s_data["email"]
            existing.address = s_data["address"]
        else:
            s = Supplier(**s_data)
            db.add(s)
    db.commit()


def generate_po_no(db: Session) -> str:
    """Auto-generate sequential purchase order number PO-YYMMDD-XXXX"""
    from datetime import datetime
    today_prefix = f"PO-{datetime.now().strftime('%y%m%d')}-"
    latest_po = (
        db.query(PurchaseOrder)
        .filter(PurchaseOrder.po_number.like(f"{today_prefix}%"))
        .order_by(PurchaseOrder.id.desc())
        .first()
    )
    if latest_po and latest_po.po_number:
        try:
            last_seq = int(latest_po.po_number.split("-")[-1])
            next_seq = last_seq + 1
        except Exception:
            next_seq = 1
    else:
        next_seq = 1

    while db.query(PurchaseOrder).filter(PurchaseOrder.po_number == f"{today_prefix}{next_seq:04d}").first():
        next_seq += 1

    return f"{today_prefix}{next_seq:04d}"


def compute_po_totals(items: list) -> dict:
    """
    Computes exact purchase order math:
    Subtotal = sum(price * qty)
    GST Total = sum(price * qty * (gst / 100))
    Grand Total = Subtotal + GST Total
    """
    subtotal = 0.0
    gst_total = 0.0
    formatted_items = []

    for idx, item in enumerate(items or []):
        if not isinstance(item, dict):
            continue
        qty = int(item.get("qty") or item.get("quantity") or 1)
        price = float(item.get("price") or item.get("purchasePrice") or item.get("unit_price") or 0.0)
        gst_rate = float(item.get("gst") or item.get("gst_rate") or 18.0)
        item_subtotal = round(price * qty, 2)
        item_gst = round(item_subtotal * (gst_rate / 100.0), 2)
        item_total = round(item_subtotal + item_gst, 2)

        subtotal += item_subtotal
        gst_total += item_gst

        formatted_items.append({
            "id": str(item.get("id") or f"ITEM{idx+1:03d}"),
            "name": str(item.get("name") or item.get("product_name") or "Product"),
            "sku": str(item.get("sku") or ""),
            "type": str(item.get("type") or "Other"),
            "category": str(item.get("category") or ""),
            "price": price,
            "purchasePrice": price,
            "qty": qty,
            "unit": str(item.get("unit") or "Nos"),
            "gst": gst_rate,
            "total": item_total,
            "specifications": item.get("specifications") if isinstance(item.get("specifications"), dict) else {},
        })

    subtotal = round(subtotal, 2)
    gst_total = round(gst_total, 2)
    grand_total = round(subtotal + gst_total, 2)

    return {
        "items": formatted_items,
        "subtotal": subtotal,
        "gst_total": gst_total,
        "grand_total": grand_total,
    }


def format_supplier_response(supplier: Supplier) -> dict:
    return {
        "id": supplier.supplier_code,  # Matches Flutter's supplier['id']
        "supplier_id": supplier.id,
        "supplier_code": supplier.supplier_code,
        "name": supplier.name,
        "supplier_name": supplier.name,
        "contact": supplier.contact_person,
        "contact_person": supplier.contact_person,
        "mobile": supplier.mobile,
        "phone": supplier.mobile,
        "email": supplier.email,
        "address": supplier.address,
        "city": getattr(supplier, "city", None),
        "state": getattr(supplier, "state", None),
        "pincode": getattr(supplier, "pincode", None),
        "gstin": supplier.gstin,
        "pan_number": getattr(supplier, "pan_number", None),
        "payment_terms": getattr(supplier, "payment_terms", None) or "30 Days",
        "remarks": getattr(supplier, "remarks", None),
        "notes": getattr(supplier, "remarks", None),
    }


def format_po_response(po: PurchaseOrder) -> dict:
    return {
        "id": po.id,
        "po_number": po.po_number,
        "po_date": po.po_date,
        "expected_delivery": po.expected_delivery,
        "delivery_date": po.expected_delivery,
        "po_status": po.po_status,
        "status": po.po_status,
        "payment_terms": po.payment_terms,
        "reference": po.reference,
        "supplier_id": po.supplier_code or str(po.supplier_id),
        "supplier_db_id": po.supplier_id,
        "supplier_code": po.supplier_code,
        "supplier_name": po.supplier_name,
        "contact_person": po.contact_person,
        "contact": po.contact_person,
        "mobile": po.mobile,
        "phone": po.mobile,
        "email": po.email,
        "address": po.address,
        "items": po.items or [],
        "subtotal": float(po.subtotal or 0.0),
        "gst_total": float(po.gst_total or 0.0),
        "grand_total": float(po.grand_total or 0.0),
        "formatted_subtotal": format_currency_inr(po.subtotal or 0.0),
        "formatted_gst_total": format_currency_inr(po.gst_total or 0.0),
        "formatted_grand_total": format_currency_inr(po.grand_total or 0.0),
        "notes": po.notes,
        "remarks": po.notes,
        "created_at": po.created_at.isoformat() if po.created_at else None,
        "updated_at": po.updated_at.isoformat() if po.updated_at else None,
    }


@router.get("/purchases/next-po-number")
@router.get("/purchases/next-number")
@router.get("/purchase-orders/next-number")
def get_next_po_number(db: Session = Depends(get_db)):
    return {
        "po_number": generate_po_no(db)
    }


@router.get("/purchases/suppliers")
@router.get("/suppliers")
@router.get("/purchase-orders/suppliers")
def list_suppliers(
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    ensure_default_suppliers(db)
    query = db.query(Supplier)
    if search:
        pat = f"%{search.strip()}%"
        query = query.filter(
            or_(
                Supplier.name.ilike(pat),
                Supplier.supplier_code.ilike(pat),
                Supplier.contact_person.ilike(pat),
                Supplier.mobile.ilike(pat),
                Supplier.city.ilike(pat),
                Supplier.state.ilike(pat),
            )
        )
    suppliers = query.order_by(Supplier.id.asc()).all()
    results = [format_supplier_response(s) for s in suppliers]
    return {
        "count": len(results),
        "suppliers": results,
        "results": results,
    }


@router.post("/purchases/suppliers", status_code=status.HTTP_201_CREATED)
@router.post("/suppliers", status_code=status.HTTP_201_CREATED)
@router.post("/purchase-orders/suppliers", status_code=status.HTTP_201_CREATED)
async def create_supplier(
    request: Request,
    db: Session = Depends(get_db),
):
    payload = await extract_request_payload(request)
    name = str(payload.get("name") or payload.get("supplier_name") or "").strip()
    if not name:
        raise HTTPException(status_code=422, detail="Supplier name is required")

    contact = str(payload.get("contact") or payload.get("contact_person") or "").strip() or None
    mobile = str(payload.get("mobile") or payload.get("phone") or "").strip() or None
    email = str(payload.get("email") or "").strip() or None
    address = str(payload.get("address") or payload.get("supplier_address") or "").strip() or None
    city = str(payload.get("city") or "").strip() or None
    state_val = str(payload.get("state") or "").strip() or None
    pincode = str(payload.get("pincode") or payload.get("pin") or "").strip() or None
    gstin = str(payload.get("gstin") or "").strip() or None
    pan_number = str(payload.get("pan_number") or payload.get("pan") or "").strip() or None
    payment_terms = str(payload.get("payment_terms") or "30 Days").strip()
    remarks = str(payload.get("remarks") or payload.get("notes") or "").strip() or None

    supplier_code = str(payload.get("supplier_code") or "").strip()
    if not supplier_code:
        last_sup = db.query(Supplier).order_by(Supplier.id.desc()).first()
        next_num = (last_sup.id + 1) if last_sup else 1
        supplier_code = f"SUP{next_num:03d}"
        while db.query(Supplier).filter(Supplier.supplier_code == supplier_code).first():
            next_num += 1
            supplier_code = f"SUP{next_num:03d}"
    else:
        existing = db.query(Supplier).filter(Supplier.supplier_code == supplier_code).first()
        if existing:
            existing.name = name
            if contact:
                existing.contact_person = contact
            if mobile:
                existing.mobile = mobile
            if email:
                existing.email = email
            if address:
                existing.address = address
            if city:
                existing.city = city
            if state_val:
                existing.state = state_val
            if pincode:
                existing.pincode = pincode
            if gstin:
                existing.gstin = gstin
            if pan_number:
                existing.pan_number = pan_number
            if payment_terms:
                existing.payment_terms = payment_terms
            if remarks:
                existing.remarks = remarks
            db.commit()
            db.refresh(existing)
            return {
                "message": f"Supplier '{existing.name}' updated successfully",
                "supplier": format_supplier_response(existing),
            }

    supplier = Supplier(
        supplier_code=supplier_code,
        name=name,
        contact_person=contact,
        mobile=mobile,
        email=email,
        address=address,
        city=city,
        state=state_val,
        pincode=pincode,
        gstin=gstin,
        pan_number=pan_number,
        payment_terms=payment_terms,
        remarks=remarks,
    )
    db.add(supplier)
    db.commit()
    db.refresh(supplier)

    return {
        "message": f"Supplier '{supplier.name}' created successfully",
        "supplier": format_supplier_response(supplier),
    }


@router.get("/purchases/create-data")
@router.get("/purchase-orders/create-data")
def get_purchase_create_data(db: Session = Depends(get_db)):
    """
    Initializes AddPurchaseOrderScreen in a single round-trip:
    - Auto-generated PO Number & dates
    - Preloaded suppliers
    - Product Picker hierarchies (types, categories, products)
    - Payment terms and PO status options
    """
    ensure_default_suppliers(db)
    from datetime import datetime, timedelta
    now = datetime.now()
    po_number = generate_po_no(db)
    po_date = now.strftime("%d %b %Y")
    expected_delivery = (now + timedelta(days=7)).strftime("%d %b %Y")

    suppliers = [format_supplier_response(s) for s in db.query(Supplier).order_by(Supplier.id.asc()).all()]
    picker = get_purchase_product_picker(db)

    return {
        "po_number": po_number,
        "next_po_number": po_number,
        "po_date": po_date,
        "delivery_date": expected_delivery,
        "expected_delivery": expected_delivery,
        "payment_terms": "30 Days",
        "payment_terms_options": [
            "Advance",
            "15 Days",
            "30 Days",
            "45 Days",
            "60 Days",
            "Against Delivery",
        ],
        "po_status": "Draft",
        "po_status_options": [
            "Draft",
            "Pending",
            "Approved",
            "Ordered",
            "Received",
            "Cancelled",
        ],
        "suppliers": suppliers,
        "product_types": picker.get("product_types", []),
        "categories": picker.get("categories", {}),
        "products": picker.get("products", {}),
    }


@router.get("/purchases/product-picker")
@router.get("/purchases/products")
def get_purchase_product_picker(db: Session = Depends(get_db)):
    """
    Returns the exact hierarchical product master required by the
    AddPurchaseOrderScreen modal bottom sheet:
    - product_types
    - categories (grouped by product_type)
    - products (grouped by category_name) with purchasePrice, sku, unit, gst (18%), specifications
    """
    default_types = ["Lift", "Generator", "LT Panel", "Earthing", "Service", "Other"]

    default_categories = {
        "Lift": ["Passenger Lift", "Goods Lift", "Hospital Lift", "Home Lift"],
        "Generator": ["Silent Generator", "Open Generator"],
        "LT Panel": ["Main LT Panel", "AMF Panel", "PCC Panel", "MCC Panel"],
        "Earthing": ["Earth Pit", "Chemical Earthing", "GI Earthing"],
        "Service": ["Lift AMC", "DG AMC", "Electrical Service", "Other Service"],
        "Other": ["Other Product"],
    }

    # Query DB products
    db_products = db.query(Product).filter(Product.status == "active").all()
    products_by_category = {}
    for cat_list in default_categories.values():
        for cat in cat_list:
            products_by_category[cat] = []

    for p in db_products:
        cat_name = p.category_name or "Other Product"
        type_name = str(p.category_type or "Other").capitalize()
        if type_name == "Lt panel" or type_name == "Panel":
            type_name = "LT Panel"

        if cat_name not in products_by_category:
            products_by_category[cat_name] = []

        products_by_category[cat_name].append({
            "id": p.product_code or f"PROD{p.id:03d}",
            "name": p.product_name,
            "sku": p.model_number or p.product_code or f"SKU-{p.id:03d}",
            "purchasePrice": float(p.purchase_price or p.selling_price or 0.0),
            "price": float(p.purchase_price or p.selling_price or 0.0),
            "unit": p.unit or "Nos",
            "gst": 18.0,
            "type": type_name,
            "category": cat_name,
            "specifications": p.specifications or {},
        })

    # Standard fallback items from Flutter screen
    defaults = {
        "Passenger Lift": [{
            "id": "LIFT001",
            "name": "G+2 Automatic Passenger Lift",
            "sku": "LFT-001",
            "purchasePrice": 390000.0,
            "price": 390000.0,
            "unit": "Nos",
            "gst": 18.0,
            "type": "Lift",
            "category": "Passenger Lift",
            "specifications": {
                "Capacity": "6 Passenger",
                "Rated Load": "408 KG",
                "Speed": "1 m/s",
                "Floor": "G+2",
                "Stops": "3",
                "Door Type": "Automatic",
                "Drive": "VVVF / VFD",
                "Power Supply": "415V / 3 Phase / 50Hz",
                "Cabin Finish": "SS",
            }
        }],
        "Goods Lift": [{
            "id": "LIFT002",
            "name": "Goods Lift - 1000 KG",
            "sku": "LFT-002",
            "purchasePrice": 310000.0,
            "price": 310000.0,
            "unit": "Nos",
            "gst": 18.0,
            "type": "Lift",
            "category": "Goods Lift",
            "specifications": {
                "Capacity": "1000 KG",
                "Speed": "0.5 m/s",
                "Floor": "G+2",
                "Stops": "3",
                "Door Type": "Manual",
                "Drive": "VVVF / VFD",
            }
        }],
        "Silent Generator": [
            {
                "id": "DG001",
                "name": "Silent DG 60 KVA",
                "sku": "GEN-001",
                "purchasePrice": 550000.0,
                "price": 550000.0,
                "unit": "Nos",
                "gst": 18.0,
                "type": "Generator",
                "category": "Silent Generator",
                "specifications": {
                    "Rating": "60 KVA / 48 KW",
                    "Output Voltage": "430 V",
                    "Phase": "3 Phase",
                    "Frequency": "50 Hz",
                    "Engine": "4 Cylinder",
                    "RPM": "1500",
                    "Cooling": "Liquid Cooled",
                    "Alternator": "Meccalte / CG",
                    "Voltage Control": "AVR",
                    "Control Panel": "AMF",
                }
            },
            {
                "id": "DG002",
                "name": "Silent DG 25 KVA",
                "sku": "GEN-002",
                "purchasePrice": 185000.0,
                "price": 185000.0,
                "unit": "Nos",
                "gst": 18.0,
                "type": "Generator",
                "category": "Silent Generator",
                "specifications": {
                    "Rating": "25 KVA",
                    "Output Voltage": "430 V",
                    "Phase": "3 Phase",
                    "Frequency": "50 Hz",
                    "Engine": "4 Cylinder",
                    "RPM": "1500",
                    "Cooling": "Liquid Cooled",
                    "Voltage Control": "AVR",
                }
            }
        ],
        "Main LT Panel": [{
            "id": "PANEL001",
            "name": "Main LT Control Panel",
            "sku": "PNL-001",
            "purchasePrice": 135000.0,
            "price": 135000.0,
            "unit": "Nos",
            "gst": 18.0,
            "type": "LT Panel",
            "category": "Main LT Panel",
            "specifications": {
                "Panel Type": "Main LT Panel",
                "Construction": "Floor Mounted",
                "Sheet Thickness": "2.0 MM",
                "Busbar": "Copper",
                "Busbar Insulator": "FRP / SMC",
                "Earth Busbar": "Copper",
                "Cable Entry": "Bottom",
                "Gland Plate": "3 MM",
                "Painting": "Powder Coated",
            }
        }],
        "AMF Panel": [{
            "id": "PANEL002",
            "name": "DG AMF Control Panel",
            "sku": "PNL-002",
            "purchasePrice": 85000.0,
            "price": 85000.0,
            "unit": "Nos",
            "gst": 18.0,
            "type": "LT Panel",
            "category": "AMF Panel",
            "specifications": {
                "Panel Type": "AMF Panel",
                "Application": "DG Auto Start/Stop",
                "Sheet Thickness": "2.0 MM",
                "Controller": "AMF Controller",
                "Cable Entry": "Bottom",
                "Painting": "Powder Coated",
            }
        }],
        "Earth Pit": [{
            "id": "EARTH001",
            "name": "Chemical Earthing Earth Pit",
            "sku": "EAR-001",
            "purchasePrice": 8500.0,
            "price": 8500.0,
            "unit": "Set",
            "gst": 18.0,
            "type": "Earthing",
            "category": "Earth Pit",
            "specifications": {
                "Earthing Type": "Chemical Earthing",
                "Electrode": "GI / Copper",
                "Earth Pit": "Maintenance Free",
                "Back Fill Compound": "Chemical Compound",
                "Connection": "Heavy Duty",
            }
        }],
        "Chemical Earthing": [{
            "id": "EARTH002",
            "name": "Maintenance Free Chemical Earthing",
            "sku": "EAR-002",
            "purchasePrice": 6500.0,
            "price": 6500.0,
            "unit": "Set",
            "gst": 18.0,
            "type": "Earthing",
            "category": "Chemical Earthing",
            "specifications": {
                "Earthing Type": "Chemical Earthing",
                "Electrode": "Copper",
                "Maintenance": "Maintenance Free",
                "Back Fill": "Chemical Compound",
            }
        }],
        "Lift AMC": [{
            "id": "AMC001",
            "name": "Passenger Lift AMC - 1 Year",
            "sku": "AMC-LFT-001",
            "purchasePrice": 5000.0,
            "price": 5000.0,
            "unit": "Year",
            "gst": 18.0,
            "type": "Service",
            "category": "Lift AMC",
            "specifications": {
                "Service Type": "Lift AMC",
                "Period": "1 Year",
                "Coverage": "Preventive Maintenance",
            }
        }],
        "DG AMC": [{
            "id": "AMC002",
            "name": "DG AMC - 1 Year",
            "sku": "AMC-DG-001",
            "purchasePrice": 8000.0,
            "price": 8000.0,
            "unit": "Year",
            "gst": 18.0,
            "type": "Service",
            "category": "DG AMC",
            "specifications": {
                "Service Type": "DG AMC",
                "Period": "1 Year",
                "Coverage": "Preventive Maintenance",
            }
        }],
        "Other Service": [{
            "id": "SRV001",
            "name": "Electrical Maintenance Service",
            "sku": "SRV-001",
            "purchasePrice": 4000.0,
            "price": 4000.0,
            "unit": "Job",
            "gst": 18.0,
            "type": "Service",
            "category": "Other Service",
            "specifications": {
                "Service Type": "Electrical Service",
                "Coverage": "Inspection & Maintenance",
            }
        }],
        "Other Product": [{
            "id": "OTHER001",
            "name": "Other Electrical Product",
            "sku": "OTH-001",
            "purchasePrice": 10000.0,
            "price": 10000.0,
            "unit": "Nos",
            "gst": 18.0,
            "type": "Other",
            "category": "Other Product",
            "specifications": {
                "Product Type": "Other",
            }
        }],
    }

    for cat, sample_items in defaults.items():
        if cat not in products_by_category or not products_by_category[cat]:
            products_by_category[cat] = sample_items

    return {
        "product_types": default_types,
        "categories": default_categories,
        "products": products_by_category,
    }


@router.post("/purchases/calculate")
@router.post("/purchase-orders/calculate")
async def calculate_purchase_order(
    request: Request,
):
    """
    Live calculation endpoint for AddPurchaseOrderScreen:
    Calculates Sub Total, GST Total, and Grand Total.
    """
    payload = await extract_request_payload(request)
    items = payload.get("items") or []
    if isinstance(items, str):
        try:
            import json
            items = json.loads(items)
        except Exception:
            items = []

    computed = compute_po_totals(items)

    return {
        "subtotal": computed["subtotal"],
        "gst_total": computed["gst_total"],
        "grand_total": computed["grand_total"],
    }


@router.post("/purchases", status_code=status.HTTP_201_CREATED)
@router.post("/purchases/create", status_code=status.HTTP_201_CREATED)
@router.post("/purchase-orders", status_code=status.HTTP_201_CREATED)
@router.post("/purchase-orders/create", status_code=status.HTTP_201_CREATED)
async def create_purchase_order(
    request: Request,
    db: Session = Depends(get_db),
):
    payload = await extract_request_payload(request)
    if not payload:
        raise HTTPException(status_code=400, detail="Invalid request body")

    items = payload.get("items") or []
    if isinstance(items, str):
        try:
            import json
            items = json.loads(items)
        except Exception:
            items = []

    if not items:
        raise HTTPException(status_code=422, detail="Please add at least one product")

    po_number = str(payload.get("po_number") or "").strip()
    if not po_number or db.query(PurchaseOrder).filter(PurchaseOrder.po_number == po_number).first():
        po_number = generate_po_no(db)

    # Supplier linkage: match by id (int), supplier_code (SUP001), or name
    supplier_id_val = payload.get("supplier_id") or payload.get("supplierId")
    sup_obj = None
    if supplier_id_val is not None:
        val_str = str(supplier_id_val).strip()
        if val_str.isdigit():
            sup_obj = db.query(Supplier).filter(Supplier.id == int(val_str)).first()
        if not sup_obj:
            sup_obj = db.query(Supplier).filter(Supplier.supplier_code == val_str).first()
        if not sup_obj:
            sup_obj = db.query(Supplier).filter(Supplier.name.ilike(val_str)).first()

    supplier_name = str(payload.get("supplier_name") or payload.get("supplier") or payload.get("name") or (sup_obj.name if sup_obj else "")).strip()
    if not sup_obj and supplier_name:
        sup_obj = db.query(Supplier).filter(Supplier.name.ilike(supplier_name)).first()

    if not supplier_name and sup_obj:
        supplier_name = sup_obj.name

    if not supplier_name:
        raise HTTPException(status_code=422, detail="Please select or provide supplier name")

    supplier_id = sup_obj.id if sup_obj else None
    supplier_code = sup_obj.supplier_code if sup_obj else (str(supplier_id_val) if supplier_id_val and not str(supplier_id_val).isdigit() else None)

    # Contact Person, Mobile, Email, Address: prioritize what the user entered in Flutter controllers
    contact_person = str(payload.get("contact_person") or payload.get("contact") or (sup_obj.contact_person if sup_obj else "")).strip() or None
    mobile = str(payload.get("mobile") or payload.get("phone") or (sup_obj.mobile if sup_obj else "")).strip() or None
    email = str(payload.get("email") or (sup_obj.email if sup_obj else "")).strip() or None
    address = str(payload.get("address") or payload.get("supplier_address") or (sup_obj.address if sup_obj else "")).strip() or None

    from datetime import datetime
    po_date = str(payload.get("po_date") or datetime.now().strftime("%d %b %Y")).strip()
    expected_delivery = str(payload.get("expected_delivery") or payload.get("delivery_date") or "").strip() or None
    payment_terms = str(payload.get("payment_terms") or "30 Days").strip()
    status_val = str(payload.get("status") or payload.get("po_status") or "Draft").strip().capitalize()
    reference = str(payload.get("reference") or "").strip() or None
    notes = str(payload.get("notes") or "").strip() or None

    computed = compute_po_totals(items)

    po = PurchaseOrder(
        po_number=po_number,
        po_date=po_date,
        expected_delivery=expected_delivery,
        po_status=status_val,
        payment_terms=payment_terms,
        reference=reference,
        supplier_id=supplier_id,
        supplier_code=supplier_code,
        supplier_name=supplier_name,
        contact_person=contact_person,
        mobile=mobile,
        email=email,
        address=address,
        items=computed["items"],
        subtotal=computed["subtotal"],
        gst_total=computed["gst_total"],
        grand_total=computed["grand_total"],
        notes=notes,
    )

    db.add(po)
    db.commit()
    db.refresh(po)

    formatted = format_po_response(po)
    return {
        "message": f"Purchase order '{po.po_number}' created successfully",
        "purchase_order": formatted,
        "po": formatted,
    }


@router.get("/purchases")
@router.get("/purchase-orders")
def list_purchase_orders(
    search: Optional[str] = Query(None),
    po_status: Optional[str] = Query(None),
    supplier_name: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(PurchaseOrder)

    if po_status:
        query = query.filter(PurchaseOrder.po_status.ilike(po_status.strip()))

    if supplier_name:
        query = query.filter(PurchaseOrder.supplier_name.ilike(f"%{supplier_name.strip()}%"))

    if search:
        pat = f"%{search.strip()}%"
        query = query.filter(
            or_(
                PurchaseOrder.po_number.ilike(pat),
                PurchaseOrder.supplier_name.ilike(pat),
                PurchaseOrder.supplier_code.ilike(pat),
                PurchaseOrder.reference.ilike(pat),
                PurchaseOrder.contact_person.ilike(pat),
            )
        )

    orders = query.order_by(PurchaseOrder.id.desc()).all()
    results = [format_po_response(p) for p in orders]
    return {
        "count": len(results),
        "purchase_orders": results,
        "results": results,
    }


def find_purchase_order(po_id: str, db: Session) -> Optional[PurchaseOrder]:
    val = str(po_id).strip()
    if val.isdigit():
        po = db.query(PurchaseOrder).filter(PurchaseOrder.id == int(val)).first()
        if po:
            return po
    return db.query(PurchaseOrder).filter(PurchaseOrder.po_number.ilike(val)).first()


@router.get("/purchases/{po_id}")
@router.get("/purchase-orders/{po_id}")
def get_purchase_order(po_id: str, db: Session = Depends(get_db)):
    po = find_purchase_order(po_id, db)
    if not po:
        raise HTTPException(status_code=404, detail="Purchase order not found")
    return format_po_response(po)


@router.put("/purchases/{po_id}")
@router.put("/purchase-orders/{po_id}")
async def update_purchase_order(
    po_id: str,
    request: Request,
    db: Session = Depends(get_db),
):
    po = find_purchase_order(po_id, db)
    if not po:
        raise HTTPException(status_code=404, detail="Purchase order not found")

    payload = await extract_request_payload(request)
    if not payload:
        raise HTTPException(status_code=400, detail="Invalid request body")

    if "po_status" in payload and payload["po_status"]:
        po.po_status = str(payload["po_status"]).strip().capitalize()
    elif "status" in payload and payload["status"]:
        po.po_status = str(payload["status"]).strip().capitalize()

    if "expected_delivery" in payload:
        po.expected_delivery = str(payload["expected_delivery"]).strip() or None
    elif "delivery_date" in payload:
        po.expected_delivery = str(payload["delivery_date"]).strip() or None

    if "payment_terms" in payload and payload["payment_terms"]:
        po.payment_terms = str(payload["payment_terms"]).strip()
    if "reference" in payload:
        po.reference = str(payload["reference"]).strip() or None
    if "notes" in payload:
        po.notes = str(payload["notes"]).strip() or None

    if "contact_person" in payload:
        po.contact_person = str(payload["contact_person"]).strip() or None
    elif "contact" in payload:
        po.contact_person = str(payload["contact"]).strip() or None

    if "mobile" in payload:
        po.mobile = str(payload["mobile"]).strip() or None
    elif "phone" in payload:
        po.mobile = str(payload["phone"]).strip() or None

    if "email" in payload:
        po.email = str(payload["email"]).strip() or None

    if "address" in payload:
        po.address = str(payload["address"]).strip() or None

    if "items" in payload and payload["items"]:
        items = payload["items"]
        if isinstance(items, str):
            try:
                import json
                items = json.loads(items)
            except Exception:
                items = []
        if items:
            computed = compute_po_totals(items)
            po.items = computed["items"]
            po.subtotal = computed["subtotal"]
            po.gst_total = computed["gst_total"]
            po.grand_total = computed["grand_total"]

    db.commit()
    db.refresh(po)

    formatted = format_po_response(po)
    return {
        "message": f"Purchase order '{po.po_number}' updated successfully",
        "purchase_order": formatted,
        "po": formatted,
    }


@router.delete("/purchases/{po_id}")
@router.delete("/purchase-orders/{po_id}")
def delete_purchase_order(po_id: str, db: Session = Depends(get_db)):
    po = find_purchase_order(po_id, db)
    if not po:
        raise HTTPException(status_code=404, detail="Purchase order not found")

    po_num = po.po_number
    db.delete(po)
    db.commit()
    return {"message": f"Purchase order '{po_num}' deleted successfully"}


# ==============================================================================
# STOCK IN & CATEGORY INVENTORY ENDPOINTS (StockInScreen)
# ==============================================================================

def generate_receipt_no(db: Session) -> str:
    """Auto-generate sequential stock in receipt number STK-IN-YYMMDD-XXXX"""
    from datetime import datetime
    today_prefix = f"STK-IN-{datetime.now().strftime('%y%m%d')}-"
    latest_stk = (
        db.query(StockIn)
        .filter(StockIn.receipt_no.like(f"{today_prefix}%"))
        .order_by(StockIn.id.desc())
        .first()
    )
    if latest_stk and latest_stk.receipt_no:
        try:
            last_seq = int(latest_stk.receipt_no.split("-")[-1])
            next_seq = last_seq + 1
        except Exception:
            next_seq = 1
    else:
        next_seq = 1

    while db.query(StockIn).filter(StockIn.receipt_no == f"{today_prefix}{next_seq:04d}").first():
        next_seq += 1

    return f"{today_prefix}{next_seq:04d}"


def compute_stock_in_totals(
    quantity: float,
    rate: float,
    discount: float = 0.0,
    gst: float = 18.0,
) -> dict:
    """
    Computes exact math matching StockInScreen:
    gross_amount = quantity * rate
    taxable_amount = max(0, gross_amount - discount)
    gst_amount = taxable_amount * (gst / 100)
    total_amount = taxable_amount + gst_amount
    """
    qty = max(0.0, float(quantity or 0.0))
    unit_rate = max(0.0, float(rate or 0.0))
    disc = max(0.0, float(discount or 0.0))
    gst_rate = max(0.0, float(gst if gst is not None else 18.0))

    gross_amount = round(qty * unit_rate, 2)
    taxable_amount = max(0.0, round(gross_amount - disc, 2))
    gst_amount = round(taxable_amount * (gst_rate / 100.0), 2)
    total_amount = round(taxable_amount + gst_amount, 2)

    return {
        "quantity": qty,
        "rate": unit_rate,
        "discount": disc,
        "gst_rate": gst_rate,
        "gross_amount": gross_amount,
        "taxable_amount": taxable_amount,
        "gst_amount": gst_amount,
        "total_amount": total_amount,
    }


def format_stock_in_response(stk: StockIn) -> dict:
    sku_val = stk.product_sku or ""
    qty_val = float(stk.quantity or 0.0)
    rate_val = float(stk.rate or 0.0)
    return {
        "id": stk.id,
        "stock_id": stk.id,
        "stock_in_id": stk.id,
        "receipt_no": stk.receipt_no,
        "receipt_date": stk.receipt_date,
        "po_number": stk.po_number,
        "invoice_no": stk.invoice_no,
        "invoice_date": stk.invoice_date,
        "supplier_id": stk.supplier_id,
        "supplier_code": stk.supplier_code,
        "supplier_name": stk.supplier_name,
        "supplier_contact": stk.supplier_contact,
        "product_id": stk.product_id,
        "product_sku": sku_val,
        "product_code": sku_val,
        "sku": sku_val,
        "product_type": stk.product_type,
        "category": stk.category,
        "product_name": stk.product_name,
        "product": stk.product_name,
        "specifications": stk.specifications if isinstance(stk.specifications, dict) else {},
        "quantity": qty_val,
        "stock": qty_val,
        "current_stock": qty_val,
        "unit": stk.unit or "Nos",
        "warehouse": stk.warehouse or "Main Warehouse",
        "rack": stk.rack,
        "batch_no": stk.batch_no,
        "serial_no": stk.serial_no,
        "rate": rate_val,
        "price": rate_val,
        "purchase_price": rate_val,
        "discount": float(stk.discount or 0.0),
        "gst": float(stk.gst or 18.0),
        "gross_amount": float(stk.gross_amount or 0.0),
        "taxable_amount": float(stk.taxable_amount or 0.0),
        "gst_amount": float(stk.gst_amount or 0.0),
        "total_amount": float(stk.total_amount or 0.0),
        "received_by": stk.received_by,
        "condition": stk.condition,
        "inspection_status": stk.inspection_status,
        "inspection_remarks": stk.inspection_remarks,
        "notes": stk.notes,
        "status": stk.status,
        "created_at": stk.created_at.isoformat() if stk.created_at else None,
        "updated_at": stk.updated_at.isoformat() if stk.updated_at else None,
    }


def get_default_stock_master():
    """Hierarchy and master data with initial stock for products."""
    product_types = [
        "Lift",
        "Generator",
        "LT Panel",
        "Earthing",
        "Service",
        "Other",
    ]

    categories = {
        "Lift": [
            "Passenger Lift",
            "Goods Lift",
            "Hospital Lift",
            "Home Lift",
        ],
        "Generator": [
            "Silent Generator",
            "Open Generator",
        ],
        "LT Panel": [
            "Main LT Panel",
            "AMF Panel",
            "PCC Panel",
            "MCC Panel",
        ],
        "Earthing": [
            "Earth Pit",
            "Chemical Earthing",
            "GI Earthing",
        ],
        "Service": [
            "Lift AMC",
            "DG AMC",
            "Electrical Service",
            "Other Service",
        ],
        "Other": [
            "Other Product",
        ],
    }

    products = {
        "Passenger Lift": [
            {
                "id": "LIFT001",
                "name": "G+2 Automatic Passenger Lift",
                "sku": "LFT-001",
                "unit": "Nos",
                "purchasePrice": 390000.0,
                "price": 390000.0,
                "gst": 18.0,
                "stock": 4.0,
                "specifications": {
                    "Capacity": "6 Passenger",
                    "Rated Load": "408 KG",
                    "Speed": "1 m/s",
                    "Floor": "G+2",
                    "Stops": "3",
                    "Door Type": "Automatic",
                    "Drive": "VVVF / VFD",
                    "Power Supply": "415V / 3 Phase / 50Hz",
                    "Cabin Finish": "SS",
                },
            },
        ],
        "Goods Lift": [
            {
                "id": "LIFT002",
                "name": "Goods Lift - 1000 KG",
                "sku": "LFT-002",
                "unit": "Nos",
                "purchasePrice": 310000.0,
                "price": 310000.0,
                "gst": 18.0,
                "stock": 2.0,
                "specifications": {
                    "Capacity": "1000 KG",
                    "Speed": "0.5 m/s",
                    "Floor": "G+2",
                    "Stops": "3",
                    "Door Type": "Manual",
                    "Drive": "VVVF / VFD",
                },
            },
        ],
        "Hospital Lift": [
            {
                "id": "LIFT003",
                "name": "Hospital Bed Lift 15P",
                "sku": "LFT-003",
                "unit": "Nos",
                "purchasePrice": 520000.0,
                "price": 520000.0,
                "gst": 18.0,
                "stock": 1.0,
                "specifications": {
                    "Capacity": "15 Passenger / Bed",
                    "Speed": "1.0 m/s",
                    "Door Type": "Automatic Telescopic",
                },
            },
        ],
        "Home Lift": [
            {
                "id": "LIFT004",
                "name": "Hydraulic Home Lift 4P",
                "sku": "LFT-004",
                "unit": "Nos",
                "purchasePrice": 280000.0,
                "price": 280000.0,
                "gst": 18.0,
                "stock": 3.0,
                "specifications": {
                    "Capacity": "4 Passenger / 300 KG",
                    "Drive": "Hydraulic",
                    "Power": "Single Phase / 3 Phase",
                },
            },
        ],
        "Silent Generator": [
            {
                "id": "GEN001",
                "name": "DG Set - 25 KVA",
                "sku": "GEN-001",
                "unit": "Nos",
                "purchasePrice": 210000.0,
                "price": 210000.0,
                "gst": 18.0,
                "stock": 5.0,
                "specifications": {
                    "Rating": "25 KVA",
                    "Output Voltage": "430 V",
                    "Phase": "3 Phase",
                    "Frequency": "50 Hz",
                    "RPM": "1500",
                    "Cooling": "Liquid Cooled",
                    "Voltage Control": "AVR",
                    "Control Panel": "AMF",
                },
            },
            {
                "id": "GEN002",
                "name": "DG Set - 60 KVA",
                "sku": "GEN-002",
                "unit": "Nos",
                "purchasePrice": 550000.0,
                "price": 550000.0,
                "gst": 18.0,
                "stock": 3.0,
                "specifications": {
                    "Rating": "60 KVA / 48 KW",
                    "Output Voltage": "430 V",
                    "Phase": "3 Phase",
                    "Frequency": "50 Hz",
                    "RPM": "1500",
                    "Cooling": "Liquid Cooled",
                    "Alternator": "Meccalte / CG",
                    "Voltage Control": "AVR",
                    "Control Panel": "AMF",
                },
            },
        ],
        "Open Generator": [
            {
                "id": "GEN003",
                "name": "Open Skid DG Set 30 KVA",
                "sku": "GEN-003",
                "unit": "Nos",
                "purchasePrice": 175000.0,
                "price": 175000.0,
                "gst": 18.0,
                "stock": 2.0,
                "specifications": {
                    "Rating": "30 KVA",
                    "Type": "Open Skid",
                    "Cooling": "Water Cooled",
                },
            },
        ],
        "Main LT Panel": [
            {
                "id": "PNL001",
                "name": "Main LT Panel",
                "sku": "PNL-001",
                "unit": "Nos",
                "purchasePrice": 135000.0,
                "price": 135000.0,
                "gst": 18.0,
                "stock": 6.0,
                "specifications": {
                    "Panel Type": "Main LT Panel",
                    "Construction": "Floor Mounted",
                    "Sheet Thickness": "2.0 MM",
                    "Busbar": "Copper",
                    "Busbar Insulator": "FRP / SMC",
                    "Earth Busbar": "Copper",
                    "Cable Entry": "Bottom",
                    "Gland Plate": "3 MM",
                    "Painting": "Powder Coated",
                },
            },
        ],
        "AMF Panel": [
            {
                "id": "PNL002",
                "name": "DG AMF Control Panel",
                "sku": "PNL-002",
                "unit": "Nos",
                "purchasePrice": 85000.0,
                "price": 85000.0,
                "gst": 18.0,
                "stock": 4.0,
                "specifications": {
                    "Panel Type": "AMF Panel",
                    "Application": "DG Auto Start/Stop",
                    "Sheet Thickness": "2.0 MM",
                    "Cable Entry": "Bottom",
                    "Painting": "Powder Coated",
                },
            },
        ],
        "PCC Panel": [
            {
                "id": "PNL003",
                "name": "Power Control Centre (PCC) Panel",
                "sku": "PNL-003",
                "unit": "Nos",
                "purchasePrice": 160000.0,
                "price": 160000.0,
                "gst": 18.0,
                "stock": 2.0,
                "specifications": {
                    "Panel Type": "PCC Panel",
                    "Current Rating": "800A",
                    "Busbar": "Electrolytic Copper",
                },
            },
        ],
        "MCC Panel": [
            {
                "id": "PNL004",
                "name": "Motor Control Centre (MCC) Panel",
                "sku": "PNL-004",
                "unit": "Nos",
                "purchasePrice": 145000.0,
                "price": 145000.0,
                "gst": 18.0,
                "stock": 3.0,
                "specifications": {
                    "Panel Type": "MCC Panel",
                    "Starters": "DOL / Star-Delta",
                    "Compartment": "Form 4b",
                },
            },
        ],
        "Earth Pit": [
            {
                "id": "EARTH001",
                "name": "Chemical Earthing Earth Pit",
                "sku": "EAR-001",
                "unit": "Set",
                "purchasePrice": 8500.0,
                "price": 8500.0,
                "gst": 18.0,
                "stock": 25.0,
                "specifications": {
                    "Earthing Type": "Chemical Earthing",
                    "Electrode": "GI / Copper",
                    "Earth Pit": "Maintenance Free",
                    "Back Fill Compound": "Chemical Compound",
                },
            },
        ],
        "Chemical Earthing": [
            {
                "id": "EARTH002",
                "name": "Maintenance Free Chemical Earthing",
                "sku": "EAR-002",
                "unit": "Set",
                "purchasePrice": 6500.0,
                "price": 6500.0,
                "gst": 18.0,
                "stock": 40.0,
                "specifications": {
                    "Earthing Type": "Chemical Earthing",
                    "Electrode": "Copper",
                    "Maintenance": "Maintenance Free",
                },
            },
        ],
        "GI Earthing": [
            {
                "id": "EARTH003",
                "name": "GI Pipe & Strip Earthing Set",
                "sku": "EAR-003",
                "unit": "Set",
                "purchasePrice": 4500.0,
                "price": 4500.0,
                "gst": 18.0,
                "stock": 30.0,
                "specifications": {
                    "Earthing Type": "GI Earthing",
                    "Electrode": "Hot Dip GI Pipe",
                    "Plate": "600x600x6 MM",
                },
            },
        ],
        "Lift AMC": [
            {
                "id": "AMC001",
                "name": "Passenger Lift AMC - 1 Year",
                "sku": "AMC-LFT-001",
                "unit": "Year",
                "purchasePrice": 5000.0,
                "price": 5000.0,
                "gst": 18.0,
                "stock": 10.0,
                "specifications": {
                    "Service Type": "Lift AMC",
                    "Period": "1 Year",
                    "Coverage": "Preventive Maintenance",
                },
            },
        ],
        "DG AMC": [
            {
                "id": "AMC002",
                "name": "DG AMC - 1 Year",
                "sku": "AMC-DG-001",
                "unit": "Year",
                "purchasePrice": 8000.0,
                "price": 8000.0,
                "gst": 18.0,
                "stock": 12.0,
                "specifications": {
                    "Service Type": "DG AMC",
                    "Period": "1 Year",
                    "Coverage": "Preventive Maintenance",
                },
            },
        ],
        "Electrical Service": [
            {
                "id": "SRV001",
                "name": "Electrical Maintenance Service",
                "sku": "SRV-001",
                "unit": "Job",
                "purchasePrice": 4000.0,
                "price": 4000.0,
                "gst": 18.0,
                "stock": 20.0,
                "specifications": {
                    "Service Type": "Electrical Service",
                    "Coverage": "Inspection & Maintenance",
                },
            },
        ],
        "Other Service": [
            {
                "id": "SRV002",
                "name": "Panel Testing & Calibration Service",
                "sku": "SRV-002",
                "unit": "Job",
                "purchasePrice": 6000.0,
                "price": 6000.0,
                "gst": 18.0,
                "stock": 8.0,
                "specifications": {
                    "Service Type": "Testing & Calibration",
                },
            },
        ],
        "Other Product": [
            {
                "id": "OTHER001",
                "name": "Other Electrical Product",
                "sku": "OTH-001",
                "unit": "Nos",
                "purchasePrice": 10000.0,
                "price": 10000.0,
                "gst": 18.0,
                "stock": 15.0,
                "specifications": {
                    "Product Type": "Other",
                },
            },
        ],
    }

    return product_types, categories, products


# ──────────────────────────────────────────────────────────────────────────────
# 1. Next Auto-Generated Stock In Receipt Number
# ──────────────────────────────────────────────────────────────────────────────

@router.get("/stock-in/next-receipt-number")
@router.get("/stock-in/next-number")
@router.get("/stock-ins/next-receipt-number")
def get_next_stock_in_receipt_number(db: Session = Depends(get_db)):
    from datetime import datetime
    return {
        "receipt_no": generate_receipt_no(db),
        "receipt_date": datetime.now().strftime("%d %b %Y"),
    }


# ──────────────────────────────────────────────────────────────────────────────
# 2. Supplier Dropdown for Stock In
# ──────────────────────────────────────────────────────────────────────────────

@router.get("/stock-in/suppliers")
@router.get("/stock-ins/suppliers")
def get_stock_in_suppliers(
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    ensure_default_suppliers(db)
    query = db.query(Supplier)
    if search:
        pat = f"%{search.strip()}%"
        query = query.filter(
            or_(
                Supplier.name.ilike(pat),
                Supplier.supplier_code.ilike(pat),
                Supplier.contact_person.ilike(pat),
                Supplier.mobile.ilike(pat),
            )
        )
    suppliers = query.order_by(Supplier.id.asc()).all()

    results = []
    for s in suppliers:
        contact_val = s.mobile or s.contact_person or ""
        results.append({
            "id": s.supplier_code,  # Matches Flutter's supplier['id']
            "supplier_id": s.id,
            "supplier_code": s.supplier_code,
            "name": s.name,
            "contact": contact_val,  # Matches Flutter's supplier['contact']
            "contact_person": s.contact_person,
            "mobile": s.mobile,
            "email": s.email,
            "address": s.address,
            "gstin": s.gstin,
        })

    return {
        "count": len(results),
        "suppliers": results,
        "results": results,
    }


@router.post("/stock-in/suppliers")
@router.post("/stock-ins/suppliers")
async def create_stock_in_supplier(
    request: Request,
    db: Session = Depends(get_db),
):
    try:
        payload = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON body")

    name = str(payload.get("name") or "").strip()
    if not name:
        raise HTTPException(status_code=422, detail="Supplier name is required")

    supplier_code = str(payload.get("supplier_code") or payload.get("id") or "").strip()
    if not supplier_code:
        last_sup = db.query(Supplier).order_by(Supplier.id.desc()).first()
        next_num = (last_sup.id + 1) if last_sup else 1
        supplier_code = f"SUP{next_num:03d}"
        while db.query(Supplier).filter(Supplier.supplier_code == supplier_code).first():
            next_num += 1
            supplier_code = f"SUP{next_num:03d}"

    supplier = db.query(Supplier).filter(Supplier.supplier_code == supplier_code).first()
    contact_val = str(payload.get("contact") or payload.get("contact_person") or payload.get("mobile") or "").strip() or None

    if supplier:
        supplier.name = name
        supplier.contact_person = contact_val
        supplier.mobile = str(payload.get("mobile") or contact_val or "").strip() or None
        if payload.get("email"):
            supplier.email = str(payload["email"]).strip()
        if payload.get("address"):
            supplier.address = str(payload["address"]).strip()
        if payload.get("gstin"):
            supplier.gstin = str(payload["gstin"]).strip()
        db.commit()
        db.refresh(supplier)
    else:
        supplier = Supplier(
            supplier_code=supplier_code,
            name=name,
            contact_person=contact_val,
            mobile=str(payload.get("mobile") or contact_val or "").strip() or None,
            email=str(payload.get("email") or "").strip() or None,
            address=str(payload.get("address") or "").strip() or None,
            gstin=str(payload.get("gstin") or "").strip() or None,
        )
        db.add(supplier)
        db.commit()
        db.refresh(supplier)

    return {
        "message": f"Supplier '{supplier.name}' saved successfully",
        "supplier": {
            "id": supplier.supplier_code,
            "supplier_id": supplier.id,
            "supplier_code": supplier.supplier_code,
            "name": supplier.name,
            "contact": supplier.mobile or supplier.contact_person or "",
            "mobile": supplier.mobile,
            "email": supplier.email,
            "address": supplier.address,
        },
    }


# ──────────────────────────────────────────────────────────────────────────────
# 3. Stock for Every Category Type (Direct user requirement)
# ──────────────────────────────────────────────────────────────────────────────

@router.get("/stock-in/category-stock")
@router.get("/stock-in/stock-by-category")
@router.get("/inventory/category-stock")
def get_stock_by_category_type(db: Session = Depends(get_db)):
    """
    Returns total stock and valuation grouped by every category type:
    - Lift
    - Generator
    - LT Panel
    - Earthing
    - Service
    - Other
    Includes sub-category breakdowns and active product stocks.
    """
    product_types, categories_map, default_products = get_default_stock_master()

    # Query all active products in DB
    db_products = db.query(Product).filter(Product.status == "active").all()

    # Map DB products by lowercase normalized category_type
    # and also track DB products by category_name
    type_alias_map = {
        "lift": "Lift",
        "generator": "Generator",
        "panel": "LT Panel",
        "lt panel": "LT Panel",
        "earthing": "Earthing",
        "service": "Service",
        "other": "Other",
    }

    stocks_by_type = {}
    for p_type in product_types:
        stocks_by_type[p_type] = {
            "category_type": p_type,
            "total_stock": 0.0,
            "total_products": 0,
            "total_valuation": 0.0,
            "categories": [],
        }

    overall_total_stock = 0.0
    overall_total_valuation = 0.0

    # Index existing Stock In receipts by product_id and sku for instant relation
    all_stock_ins = db.query(StockIn).order_by(StockIn.id.desc()).all()
    stock_in_by_prod_id = {}
    stock_in_by_sku = {}
    for si in all_stock_ins:
        if si.product_id and si.product_id not in stock_in_by_prod_id:
            stock_in_by_prod_id[si.product_id] = si
        if si.product_sku and si.product_sku.lower() not in stock_in_by_sku:
            stock_in_by_sku[si.product_sku.lower()] = si

    # Process each category type and its categories
    for p_type in product_types:
        cat_list = categories_map.get(p_type, [])
        type_stock = 0.0
        type_valuation = 0.0
        type_product_count = 0
        categories_data = []

        for cat_name in cat_list:
            # Find DB products matching this category
            matched_db_prods = [
                p for p in db_products
                if (p.category_name and p.category_name.strip().lower() == cat_name.lower())
                or (
                    p.category_type
                    and type_alias_map.get(p.category_type.lower(), "Other") == p_type
                    and p.category_name == cat_name
                )
            ]

            # If no DB products exist for this category, populate with default products
            cat_products_list = []
            if matched_db_prods:
                for p in matched_db_prods:
                    stk_val = float(p.stock or 0.0)
                    price_val = float(p.purchase_price or p.selling_price or 0.0)
                    item_valuation = round(stk_val * price_val, 2)
                    p_code = p.product_code or f"PROD{p.id:03d}"
                    p_sku = p.model_number or p_code
                    si = (
                        stock_in_by_prod_id.get(p.id)
                        or stock_in_by_sku.get(str(p.product_code or "").lower())
                        or stock_in_by_sku.get(str(p.model_number or "").lower())
                    )
                    cat_products_list.append({
                        "id": p_code,
                        "product_id": p.id,
                        "product_code": p_code,
                        "stock_id": si.id if si else p.id,
                        "stock_in_id": si.id if si else None,
                        "receipt_no": si.receipt_no if si else None,
                        "name": p.product_name,
                        "sku": p_sku,
                        "stock": stk_val,
                        "current_stock": stk_val,
                        "unit": p.unit or "Nos",
                        "purchase_price": price_val,
                        "price": price_val,
                        "stock_valuation": item_valuation,
                        "specifications": p.specifications or {},
                    })
            else:
                for p in default_products.get(cat_name, []):
                    stk_val = float(p.get("stock") or 0.0)
                    price_val = float(p.get("purchasePrice") or p.get("price") or 0.0)
                    item_valuation = round(stk_val * price_val, 2)
                    p_id = p["id"]
                    p_sku = p.get("sku") or p_id
                    si = stock_in_by_sku.get(str(p_sku).lower()) or stock_in_by_sku.get(str(p_id).lower())
                    cat_products_list.append({
                        "id": p_id,
                        "product_id": si.product_id if si else None,
                        "product_code": p_sku,
                        "stock_id": si.id if si else p_id,
                        "stock_in_id": si.id if si else None,
                        "receipt_no": si.receipt_no if si else None,
                        "name": p["name"],
                        "sku": p_sku,
                        "stock": stk_val,
                        "current_stock": stk_val,
                        "unit": p.get("unit") or "Nos",
                        "purchase_price": price_val,
                        "price": price_val,
                        "stock_valuation": item_valuation,
                        "specifications": p.get("specifications") or {},
                    })

            cat_stock = sum(item["stock"] for item in cat_products_list)
            cat_valuation = sum(item["stock_valuation"] for item in cat_products_list)
            cat_count = len(cat_products_list)

            categories_data.append({
                "category_name": cat_name,
                "product_count": cat_count,
                "total_stock": round(cat_stock, 2),
                "total_valuation": round(cat_valuation, 2),
                "unit": cat_products_list[0]["unit"] if cat_products_list else "Nos",
                "products": cat_products_list,
            })

            type_stock += cat_stock
            type_valuation += cat_valuation
            type_product_count += cat_count

        stocks_by_type[p_type]["total_stock"] = round(type_stock, 2)
        stocks_by_type[p_type]["total_valuation"] = round(type_valuation, 2)
        stocks_by_type[p_type]["total_products"] = type_product_count
        stocks_by_type[p_type]["categories"] = categories_data

        overall_total_stock += type_stock
        overall_total_valuation += type_valuation

    return {
        "category_types": product_types,
        "stocks_by_category_type": stocks_by_type,
        "overall_total_stock": round(overall_total_stock, 2),
        "overall_total_valuation": round(overall_total_valuation, 2),
    }


# ──────────────────────────────────────────────────────────────────────────────
# 4. Product Picker Master with Stock per Product & Category
# ──────────────────────────────────────────────────────────────────────────────

@router.get("/stock-in/product-picker")
@router.get("/stock-in/products")
@router.get("/stock-ins/product-picker")
def get_stock_in_product_picker(db: Session = Depends(get_db)):
    """
    Returns the exact hierarchical product master required by Flutter StockInScreen:
    - product_types (List[String])
    - categories (Map<String, List<String>>)
    - products (Map<String, List<Map<String, dynamic>>>) with specs, rates, and stock
    - stock_by_category_type (Map with total stock and valuation for each category type)
    """
    product_types, categories, default_products = get_default_stock_master()

    # Fetch all DB products to ensure live stock reflection
    db_products = db.query(Product).filter(Product.status == "active").all()

    type_alias_map = {
        "lift": "Lift",
        "generator": "Generator",
        "panel": "LT Panel",
        "lt panel": "LT Panel",
        "earthing": "Earthing",
        "service": "Service",
        "other": "Other",
    }

    products_by_category = {}
    for cat_list in categories.values():
        for cat in cat_list:
            products_by_category[cat] = []

    # Index existing Stock In receipts
    all_stock_ins = db.query(StockIn).order_by(StockIn.id.desc()).all()
    stock_in_by_prod_id = {}
    stock_in_by_sku = {}
    for si in all_stock_ins:
        if si.product_id and si.product_id not in stock_in_by_prod_id:
            stock_in_by_prod_id[si.product_id] = si
        if si.product_sku and si.product_sku.lower() not in stock_in_by_sku:
            stock_in_by_sku[si.product_sku.lower()] = si

    # Map DB products
    for p in db_products:
        cat_name = p.category_name or "Other Product"
        type_name = type_alias_map.get(str(p.category_type or "").lower(), "Other")

        if cat_name not in products_by_category:
            products_by_category[cat_name] = []

        p_code = p.product_code or f"PROD{p.id:03d}"
        p_sku = p.model_number or p_code
        si = (
            stock_in_by_prod_id.get(p.id)
            or stock_in_by_sku.get(str(p.product_code or "").lower())
            or stock_in_by_sku.get(str(p.model_number or "").lower())
        )

        products_by_category[cat_name].append({
            "id": p_code,
            "product_id": p.id,
            "product_code": p_code,
            "stock_id": si.id if si else p.id,
            "stock_in_id": si.id if si else None,
            "receipt_no": si.receipt_no if si else None,
            "name": p.product_name,
            "sku": p_sku,
            "unit": p.unit or "Nos",
            "purchasePrice": float(p.purchase_price or p.selling_price or 0.0),
            "price": float(p.purchase_price or p.selling_price or 0.0),
            "gst": 18.0,
            "stock": float(p.stock or 0.0),
            "current_stock": float(p.stock or 0.0),
            "type": type_name,
            "category": cat_name,
            "specifications": p.specifications or {},
        })

    # Fill defaults for categories that are empty
    for cat, items in default_products.items():
        if cat not in products_by_category or not products_by_category[cat]:
            def_items = []
            for it in items:
                p_id = it.get("id")
                p_sku = it.get("sku") or p_id
                si = stock_in_by_sku.get(str(p_sku).lower()) or stock_in_by_sku.get(str(p_id).lower())
                def_items.append({
                    **it,
                    "product_id": si.product_id if si else None,
                    "product_code": p_sku,
                    "stock_id": si.id if si else p_id,
                    "stock_in_id": si.id if si else None,
                    "receipt_no": si.receipt_no if si else None,
                    "current_stock": it.get("stock", 0.0),
                })
            products_by_category[cat] = def_items

    # Calculate stock summary per category type
    stock_by_category_type = {}
    for p_type in product_types:
        cat_list = categories.get(p_type, [])
        cat_type_stock = 0.0
        cat_type_valuation = 0.0
        cat_type_count = 0
        for cat in cat_list:
            items = products_by_category.get(cat, [])
            for it in items:
                stk = float(it.get("stock", 0.0))
                price = float(it.get("purchasePrice", 0.0))
                cat_type_stock += stk
                cat_type_valuation += stk * price
                cat_type_count += 1

        stock_by_category_type[p_type] = {
            "category_type": p_type,
            "total_stock": round(cat_type_stock, 2),
            "total_valuation": round(cat_type_valuation, 2),
            "product_count": cat_type_count,
        }

    return {
        "product_types": product_types,
        "categories": categories,
        "products": products_by_category,
        "stock_by_category_type": stock_by_category_type,
    }


# ──────────────────────────────────────────────────────────────────────────────
# 5. Live Calculation Preview
# ──────────────────────────────────────────────────────────────────────────────

@router.post("/stock-in/calculate")
@router.post("/stock-ins/calculate")
async def calculate_stock_in(request: Request):
    """
    Live calculation preview for StockInScreen:
    Calculates Gross Amount, Discount, Taxable Amount, GST Amount, and Total Stock Value.
    """
    try:
        payload = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON body")

    quantity = float(payload.get("quantity") or payload.get("qty") or 1.0)
    rate = float(payload.get("rate") or payload.get("purchasePrice") or payload.get("price") or 0.0)
    discount = float(payload.get("discount") or 0.0)
    gst = float(payload.get("gst") if payload.get("gst") is not None else 18.0)

    computed = compute_stock_in_totals(quantity=quantity, rate=rate, discount=discount, gst=gst)

    return {
        "quantity": computed["quantity"],
        "rate": computed["rate"],
        "discount": computed["discount"],
        "gross_amount": computed["gross_amount"],
        "taxable_amount": computed["taxable_amount"],
        "gst_rate": computed["gst_rate"],
        "gst_amount": computed["gst_amount"],
        "total_amount": computed["total_amount"],
    }


# ──────────────────────────────────────────────────────────────────────────────
# 6. Create / Save Stock In (and Increment Product Inventory)
# ──────────────────────────────────────────────────────────────────────────────

@router.post("/stock-in")
@router.post("/stock-in/create")
@router.post("/stock-ins")
async def create_stock_in(
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Creates a new Stock In entry from StockInScreen payload and automatically
    increments the product's inventory stock in the database.
    """
    try:
        payload = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON body")

    # Required field validations matching Flutter UI
    supplier_val = payload.get("supplier_id") or payload.get("supplier")
    if not supplier_val:
        raise HTTPException(status_code=422, detail="Please select supplier.")

    product_type = str(payload.get("product_type") or "").strip()
    if not product_type:
        raise HTTPException(status_code=422, detail="Please select product type.")

    category = str(payload.get("category") or "").strip()
    if not category:
        raise HTTPException(status_code=422, detail="Please select category.")

    product_name = str(payload.get("product") or payload.get("product_name") or "").strip()
    if not product_name:
        raise HTTPException(status_code=422, detail="Please select product.")

    quantity = float(payload.get("quantity") or 0.0)
    if quantity <= 0:
        raise HTTPException(status_code=422, detail="Please enter valid quantity.")

    rate = float(payload.get("rate") or 0.0)
    if rate <= 0:
        raise HTTPException(status_code=422, detail="Please enter valid rate.")

    invoice_no = str(payload.get("invoice_no") or "").strip()
    if not invoice_no:
        raise HTTPException(status_code=422, detail="Invoice No. is required.")

    # Receipt Number
    receipt_no = str(payload.get("receipt_no") or "").strip()
    if not receipt_no or db.query(StockIn).filter(StockIn.receipt_no == receipt_no).first():
        receipt_no = generate_receipt_no(db)

    from datetime import datetime
    receipt_date = str(payload.get("receipt_date") or datetime.now().strftime("%d %b %Y")).strip()
    invoice_date = str(payload.get("invoice_date") or receipt_date).strip()
    po_number = str(payload.get("po_number") or "").strip() or None

    # Resolve Supplier
    sup_obj = None
    if str(supplier_val).isdigit():
        sup_obj = db.query(Supplier).filter(Supplier.id == int(supplier_val)).first()
    else:
        sup_obj = db.query(Supplier).filter(Supplier.supplier_code == str(supplier_val).strip()).first()

    supplier_id = sup_obj.id if sup_obj else None
    supplier_code = sup_obj.supplier_code if sup_obj else (str(supplier_val) if not str(supplier_val).isdigit() else None)
    supplier_name = str(payload.get("supplier_name") or (sup_obj.name if sup_obj else supplier_val)).strip()
    supplier_contact = str(payload.get("supplier_contact") or (sup_obj.mobile if sup_obj else "")).strip() or None

    # Stock & Storage
    unit = str(payload.get("unit") or "Nos").strip()
    warehouse = str(payload.get("warehouse") or "Main Warehouse").strip()
    rack = str(payload.get("rack") or "").strip() or None
    batch_no = str(payload.get("batch_no") or "").strip() or None
    serial_no = str(payload.get("serial_no") or "").strip() or None

    # Pricing calculations
    discount = float(payload.get("discount") or 0.0)
    gst = float(payload.get("gst") if payload.get("gst") is not None else 18.0)
    computed = compute_stock_in_totals(quantity=quantity, rate=rate, discount=discount, gst=gst)

    received_by = str(payload.get("received_by") or "Admin").strip()
    condition = str(payload.get("condition") or "Good").strip()
    inspection_status = str(payload.get("inspection_status") or "Pending").strip()
    inspection_remarks = str(payload.get("inspection_remarks") or "").strip() or None
    notes = str(payload.get("notes") or "").strip() or None
    status_val = str(payload.get("status") or "Received").strip()

    # Product linkage & specifications
    specs = payload.get("specifications") if isinstance(payload.get("specifications"), dict) else {}
    product_sku = str(payload.get("product_sku") or payload.get("sku") or "").strip() or None

    # Look for matching product in DB to link and update inventory stock
    product_obj = None
    if payload.get("product_id") and str(payload.get("product_id")).isdigit():
        product_obj = db.query(Product).filter(Product.id == int(payload.get("product_id"))).first()

    if not product_obj and product_sku:
        product_obj = db.query(Product).filter(Product.product_code == product_sku).first()

    if not product_obj and product_name:
        product_obj = db.query(Product).filter(Product.product_name == product_name).first()

    # Update or create product stock in DB
    if product_obj:
        product_obj.stock = float(product_obj.stock or 0.0) + quantity
        product_obj.inventory_tracking = True
        product_obj.purchase_price = rate
        if specs and not product_obj.specifications:
            product_obj.specifications = specs
        db.flush()
        product_id = product_obj.id
        if not product_sku:
            product_sku = product_obj.product_code
        if not specs and product_obj.specifications:
            specs = product_obj.specifications
    else:
        # Create product in DB to ensure stock is permanently tracked
        new_prod_code = product_sku or f"PRD-{receipt_no.split('-')[-1]}"
        product_obj = Product(
            category_type=product_type.lower(),
            category_name=category,
            product_name=product_name,
            product_code=new_prod_code,
            purchase_price=rate,
            selling_price=round(rate * 1.25, 2),
            stock=quantity,
            unit=unit,
            inventory_tracking=True,
            specifications=specs,
            status="active",
        )
        db.add(product_obj)
        db.flush()
        product_id = product_obj.id
        product_sku = product_obj.product_code

    stock_in = StockIn(
        receipt_no=receipt_no,
        receipt_date=receipt_date,
        po_number=po_number,
        invoice_no=invoice_no,
        invoice_date=invoice_date,
        supplier_id=supplier_id,
        supplier_code=supplier_code,
        supplier_name=supplier_name,
        supplier_contact=supplier_contact,
        product_id=product_id,
        product_sku=product_sku,
        product_type=product_type,
        category=category,
        product_name=product_name,
        specifications=specs,
        quantity=quantity,
        unit=unit,
        warehouse=warehouse,
        rack=rack,
        batch_no=batch_no,
        serial_no=serial_no,
        rate=rate,
        discount=discount,
        gst=gst,
        gross_amount=computed["gross_amount"],
        taxable_amount=computed["taxable_amount"],
        gst_amount=computed["gst_amount"],
        total_amount=computed["total_amount"],
        received_by=received_by,
        condition=condition,
        inspection_status=inspection_status,
        inspection_remarks=inspection_remarks,
        notes=notes,
        status=status_val,
    )

    db.add(stock_in)
    db.commit()
    db.refresh(stock_in)

    return {
        "message": f"Stock In '{stock_in.receipt_no}' saved successfully. Inventory updated (+{quantity} {unit}).",
        "stock_in": format_stock_in_response(stock_in),
        "receipt": format_stock_in_response(stock_in),
        "current_product_stock": float(product_obj.stock or 0.0) if product_obj else quantity,
    }


# ──────────────────────────────────────────────────────────────────────────────
# 7. List Stock In Receipts (with Search, Filters, and Sorting)
# ──────────────────────────────────────────────────────────────────────────────

@router.get("/stock-in")
@router.get("/stock-ins")
def list_stock_in_receipts(
    search: Optional[str] = Query(None),
    product_type: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    warehouse: Optional[str] = Query(None),
    condition: Optional[str] = Query(None),
    inspection_status: Optional[str] = Query(None),
    supplier_name: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    product_id: Optional[Union[int, str]] = Query(None),
    product_sku: Optional[str] = Query(None),
    receipt_no: Optional[str] = Query(None),
    id: Optional[Union[int, str]] = Query(None),
    stock_id: Optional[Union[int, str]] = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(StockIn)

    if product_type:
        query = query.filter(StockIn.product_type.ilike(product_type.strip()))
    if category:
        query = query.filter(StockIn.category.ilike(category.strip()))
    if warehouse:
        query = query.filter(StockIn.warehouse.ilike(warehouse.strip()))
    if condition:
        query = query.filter(StockIn.condition.ilike(condition.strip()))
    if inspection_status:
        query = query.filter(StockIn.inspection_status.ilike(inspection_status.strip()))
    if supplier_name:
        query = query.filter(StockIn.supplier_name.ilike(f"%{supplier_name.strip()}%"))
    if status:
        query = query.filter(StockIn.status.ilike(status.strip()))

    if product_id is not None and str(product_id).strip():
        val = str(product_id).strip()
        if val.isdigit():
            query = query.filter(StockIn.product_id == int(val))
        else:
            query = query.filter(StockIn.product_sku.ilike(val))

    if product_sku:
        query = query.filter(StockIn.product_sku.ilike(product_sku.strip()))

    if receipt_no:
        query = query.filter(StockIn.receipt_no.ilike(receipt_no.strip()))

    rec_id = id if id is not None else stock_id
    if rec_id is not None and str(rec_id).strip():
        val = str(rec_id).strip()
        if val.isdigit():
            query = query.filter(or_(StockIn.id == int(val), StockIn.product_id == int(val)))
        else:
            query = query.filter(or_(StockIn.receipt_no.ilike(val), StockIn.product_sku.ilike(val)))

    if search:
        pat = f"%{search.strip()}%"
        query = query.filter(
            or_(
                StockIn.receipt_no.ilike(pat),
                StockIn.invoice_no.ilike(pat),
                StockIn.po_number.ilike(pat),
                StockIn.supplier_name.ilike(pat),
                StockIn.product_name.ilike(pat),
                StockIn.product_sku.ilike(pat),
                StockIn.serial_no.ilike(pat),
                StockIn.batch_no.ilike(pat),
                StockIn.warehouse.ilike(pat),
                StockIn.received_by.ilike(pat),
            )
        )

    receipts = query.order_by(StockIn.id.desc()).all()
    results = [format_stock_in_response(r) for r in receipts]

    return {
        "count": len(results),
        "receipts": results,
        "stock_ins": results,
        "results": results,
    }


# ──────────────────────────────────────────────────────────────────────────────
# 8. Dropdown Choices / Metadata Endpoint
# ──────────────────────────────────────────────────────────────────────────────

@router.get("/stock-in/meta")
@router.get("/stock-ins/meta")
def get_stock_in_metadata():
    """
    Returns static configuration dropdown choices used in StockInScreen:
    - warehouses
    - units
    - conditions
    - inspection_statuses
    - gst_rates
    """
    return {
        "warehouses": [
            "Main Warehouse",
            "Lift Warehouse",
            "DG Warehouse",
            "Panel Warehouse",
            "Service Store",
        ],
        "units": [
            "Nos",
            "Set",
            "Unit",
            "Kg",
            "Meter",
            "Feet",
            "Year",
            "Job",
        ],
        "conditions": [
            "Good",
            "Damaged",
            "Partial Damage",
            "Under Inspection",
        ],
        "inspection_statuses": [
            "Pending",
            "Passed",
            "Failed",
            "Not Required",
        ],
        "gst_rates": [
            0,
            5,
            12,
            18,
            28,
        ],
    }


# ──────────────────────────────────────────────────────────────────────────────
# 9. Intelligent Stock In / Inventory Detail Resolvers
# ──────────────────────────────────────────────────────────────────────────────

def format_product_as_stock_in_response(prod: Product) -> dict:
    """Formats an inventory Product as a Stock In response when no receipt exists yet."""
    price = float(prod.purchase_price or prod.selling_price or 0.0)
    stk_val = float(prod.stock or 0.0)
    sku = prod.model_number or prod.product_code or f"SKU-{prod.id:03d}"
    cat_type = (prod.category_type or "General").capitalize()
    cat_name = prod.category_name or cat_type
    gross = round(stk_val * price, 2)
    taxable = gross
    gst_amt = round(taxable * 0.18, 2)
    total = round(taxable + gst_amt, 2)
    return {
        "id": prod.id,
        "stock_id": prod.id,
        "stock_in_id": None,
        "receipt_no": f"STK-PROD-{prod.id:04d}",
        "receipt_date": datetime.now().strftime("%d %b %Y"),
        "po_number": None,
        "invoice_no": None,
        "invoice_date": None,
        "supplier_id": 1,
        "supplier_code": "SUP001",
        "supplier_name": "In-House Stock",
        "supplier_contact": "",
        "product_id": prod.id,
        "product_sku": sku,
        "product_code": prod.product_code or sku,
        "sku": sku,
        "product_type": cat_type,
        "category": cat_name,
        "product_name": prod.product_name,
        "product": prod.product_name,
        "specifications": prod.specifications if isinstance(prod.specifications, dict) else {},
        "quantity": stk_val,
        "stock": stk_val,
        "current_stock": stk_val,
        "unit": prod.unit or "Nos",
        "warehouse": "Main Warehouse",
        "rack": "General Store",
        "batch_no": None,
        "serial_no": None,
        "rate": price,
        "price": price,
        "purchase_price": price,
        "discount": 0.0,
        "gst": 18.0,
        "gross_amount": gross,
        "taxable_amount": taxable,
        "gst_amount": gst_amt,
        "total_amount": total,
        "received_by": "Inventory Manager",
        "condition": "Good",
        "inspection_status": "Passed",
        "inspection_remarks": "Product inventory on hand",
        "notes": "Current inventory stock",
        "status": "In Stock",
        "created_at": prod.created_at.isoformat() if prod.created_at else None,
        "updated_at": prod.updated_at.isoformat() if prod.updated_at else None,
    }


def format_default_item_as_stock_in(item: dict, category_name: str) -> dict:
    """Formats a static default product master item as a Stock In response."""
    price = float(item.get("purchasePrice") or item.get("price") or 0.0)
    stk_val = float(item.get("stock") or 0.0)
    item_id = item.get("id") or "ITEM001"
    sku = item.get("sku") or item_id
    gross = round(stk_val * price, 2)
    taxable = gross
    gst_amt = round(taxable * 0.18, 2)
    total = round(taxable + gst_amt, 2)
    return {
        "id": item_id,
        "stock_id": item_id,
        "stock_in_id": None,
        "receipt_no": f"STK-DEF-{item_id}",
        "receipt_date": datetime.now().strftime("%d %b %Y"),
        "po_number": None,
        "invoice_no": None,
        "invoice_date": None,
        "supplier_id": 1,
        "supplier_code": "SUP001",
        "supplier_name": "Default Master Supplier",
        "supplier_contact": "",
        "product_id": None,
        "product_sku": sku,
        "product_code": sku,
        "sku": sku,
        "product_type": item.get("type") or "General",
        "category": category_name,
        "product_name": item.get("name") or item_id,
        "product": item.get("name") or item_id,
        "specifications": item.get("specifications") if isinstance(item.get("specifications"), dict) else {},
        "quantity": stk_val,
        "stock": stk_val,
        "current_stock": stk_val,
        "unit": item.get("unit") or "Nos",
        "warehouse": "Main Warehouse",
        "rack": "Rack-01",
        "batch_no": None,
        "serial_no": None,
        "rate": price,
        "price": price,
        "purchase_price": price,
        "discount": 0.0,
        "gst": 18.0,
        "gross_amount": gross,
        "taxable_amount": taxable,
        "gst_amount": gst_amt,
        "total_amount": total,
        "received_by": "Store Admin",
        "condition": "Good",
        "inspection_status": "Passed",
        "inspection_remarks": "Master inventory item",
        "notes": "Master item",
        "status": "In Stock",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
    }


def find_stock_in_entity(identifier: Union[int, str], db: Session) -> Optional[StockIn]:
    """
    Finds the underlying StockIn database model instance by any identifier:
    - Integer StockIn ID (e.g. 1)
    - Product ID in StockIn (e.g. 11, 15, 28)
    - Receipt Number (e.g. STK-IN-260915-0001)
    - Product SKU / Code (e.g. LFT-001, GEN-002, PNL-001)
    - Invoice Number
    - PO Number
    - Serial Number or Batch Number
    - Product ID / Code from products table that has a StockIn receipt
    """
    if identifier is None:
        return None
    val = str(identifier).strip()
    if not val or val.lower() in ("next-receipt-number", "suppliers", "category-stock", "stock-by-category", "product-picker", "products", "calculate", "meta"):
        return None

    if val.isdigit():
        int_id = int(val)
        # 1. Exact StockIn primary key id
        stk = db.query(StockIn).filter(StockIn.id == int_id).first()
        if stk:
            return stk
        # 2. Exact StockIn.product_id
        stk = db.query(StockIn).filter(StockIn.product_id == int_id).order_by(StockIn.id.desc()).first()
        if stk:
            return stk

    # 3. Exact receipt_no (case-insensitive)
    stk = db.query(StockIn).filter(StockIn.receipt_no.ilike(val)).first()
    if stk:
        return stk

    # 4. Product SKU or Code
    stk = db.query(StockIn).filter(StockIn.product_sku.ilike(val)).order_by(StockIn.id.desc()).first()
    if stk:
        return stk

    # 5. Invoice No
    stk = db.query(StockIn).filter(StockIn.invoice_no.ilike(val)).order_by(StockIn.id.desc()).first()
    if stk:
        return stk

    # 6. PO Number
    stk = db.query(StockIn).filter(StockIn.po_number.ilike(val)).order_by(StockIn.id.desc()).first()
    if stk:
        return stk

    # 7. Serial No or Batch No
    stk = db.query(StockIn).filter(or_(StockIn.serial_no.ilike(val), StockIn.batch_no.ilike(val))).first()
    if stk:
        return stk

    # 8. Check if identifier matches a Product (by code, SKU, or name) that has a StockIn receipt
    prod = None
    if val.isdigit():
        prod = db.query(Product).filter(Product.id == int(val)).first()
    if not prod:
        prod = db.query(Product).filter(
            or_(
                Product.product_code.ilike(val),
                Product.model_number.ilike(val),
                Product.product_name.ilike(val),
            )
        ).first()

    if prod:
        stk = db.query(StockIn).filter(StockIn.product_id == prod.id).order_by(StockIn.id.desc()).first()
        if stk:
            return stk

    return None


def find_stock_in_record(identifier: Union[int, str], db: Session) -> Optional[dict]:
    """
    Unified resolver that returns the complete formatted stock in / inventory detail dictionary.
    First checks StockIn database table; if not present as a receipt, checks Product table and master defaults.
    """
    stk = find_stock_in_entity(identifier, db)
    if stk:
        return format_stock_in_response(stk)

    if identifier is None:
        return None
    val = str(identifier).strip()
    if not val or val.lower() in ("next-receipt-number", "suppliers", "category-stock", "stock-by-category", "product-picker", "products", "calculate", "meta"):
        return None

    # Check if a Product exists in DB for this identifier
    prod = None
    if val.isdigit():
        prod = db.query(Product).filter(Product.id == int(val)).first()
    if not prod:
        prod = db.query(Product).filter(
            or_(
                Product.product_code.ilike(val),
                Product.model_number.ilike(val),
                Product.product_name.ilike(val),
            )
        ).first()

    if prod:
        return format_product_as_stock_in_response(prod)

    # Check default products master
    _, _, default_prods = get_default_stock_master()
    for cat_name, items in default_prods.items():
        for it in items:
            if (
                str(it.get("id", "")).strip().lower() == val.lower()
                or str(it.get("sku", "")).strip().lower() == val.lower()
                or str(it.get("name", "")).strip().lower() == val.lower()
            ):
                return format_default_item_as_stock_in(it, cat_name)

    return None


# ──────────────────────────────────────────────────────────────────────────────
# 10. Single Stock In Detail (Accepts ANY ID: StockIn ID, Receipt No, Product ID, SKU)
# ──────────────────────────────────────────────────────────────────────────────

@router.get("/stock-in/product/{product_id}")
@router.get("/stock-ins/product/{product_id}")
@router.get("/stock-in/by-product/{product_id}")
def get_stock_in_by_product(product_id: str, db: Session = Depends(get_db)):
    detail = find_stock_in_record(product_id, db)
    if not detail:
        raise HTTPException(status_code=404, detail=f"Stock In detail not found for product '{product_id}'")
    return detail


@router.get("/stock-in/receipt/{receipt_no}")
@router.get("/stock-ins/receipt/{receipt_no}")
def get_stock_in_by_receipt(receipt_no: str, db: Session = Depends(get_db)):
    detail = find_stock_in_record(receipt_no, db)
    if not detail:
        raise HTTPException(status_code=404, detail=f"Stock In detail not found for receipt '{receipt_no}'")
    return detail


@router.get("/stock-in/{stock_id:path}")
@router.get("/stock-ins/{stock_id:path}")
def get_stock_in_detail(stock_id: str, db: Session = Depends(get_db)):
    detail = find_stock_in_record(stock_id, db)
    if not detail:
        raise HTTPException(status_code=404, detail=f"Stock In receipt not found for identifier '{stock_id}'")
    return detail


# ──────────────────────────────────────────────────────────────────────────────
# 11. Update Stock In Record (Accepts ANY identifier)
# ──────────────────────────────────────────────────────────────────────────────

@router.put("/stock-in/{stock_id:path}")
@router.put("/stock-ins/{stock_id:path}")
async def update_stock_in(
    stock_id: str,
    request: Request,
    db: Session = Depends(get_db),
):
    stk = find_stock_in_entity(stock_id, db)
    if not stk:
        raise HTTPException(status_code=404, detail=f"Stock In receipt not found for identifier '{stock_id}'")

    try:
        payload = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON body")

    old_quantity = float(stk.quantity or 0.0)

    # Update basic fields if present
    if "receipt_date" in payload:
        stk.receipt_date = str(payload["receipt_date"]).strip()
    if "po_number" in payload:
        stk.po_number = str(payload["po_number"]).strip() or None
    if "invoice_no" in payload and payload["invoice_no"]:
        stk.invoice_no = str(payload["invoice_no"]).strip()
    if "invoice_date" in payload:
        stk.invoice_date = str(payload["invoice_date"]).strip()

    if "supplier_name" in payload and payload["supplier_name"]:
        stk.supplier_name = str(payload["supplier_name"]).strip()
    if "supplier_contact" in payload:
        stk.supplier_contact = str(payload["supplier_contact"]).strip() or None

    if "warehouse" in payload:
        stk.warehouse = str(payload["warehouse"]).strip()
    if "rack" in payload:
        stk.rack = str(payload["rack"]).strip() or None
    if "batch_no" in payload:
        stk.batch_no = str(payload["batch_no"]).strip() or None
    if "serial_no" in payload:
        stk.serial_no = str(payload["serial_no"]).strip() or None

    if "received_by" in payload and payload["received_by"]:
        stk.received_by = str(payload["received_by"]).strip()
    if "condition" in payload:
        stk.condition = str(payload["condition"]).strip()
    if "inspection_status" in payload:
        stk.inspection_status = str(payload["inspection_status"]).strip()
    if "inspection_remarks" in payload:
        stk.inspection_remarks = str(payload["inspection_remarks"]).strip() or None
    if "notes" in payload:
        stk.notes = str(payload["notes"]).strip() or None
    if "status" in payload:
        stk.status = str(payload["status"]).strip()

    # Recalculate if pricing or quantity changed
    new_quantity = float(payload["quantity"]) if "quantity" in payload and payload["quantity"] is not None else old_quantity
    new_rate = float(payload["rate"]) if "rate" in payload and payload["rate"] is not None else float(stk.rate or 0.0)
    new_discount = float(payload["discount"]) if "discount" in payload and payload["discount"] is not None else float(stk.discount or 0.0)
    new_gst = float(payload["gst"]) if "gst" in payload and payload["gst"] is not None else float(stk.gst or 18.0)

    computed = compute_stock_in_totals(quantity=new_quantity, rate=new_rate, discount=new_discount, gst=new_gst)

    stk.quantity = new_quantity
    stk.rate = new_rate
    stk.discount = new_discount
    stk.gst = new_gst
    stk.gross_amount = computed["gross_amount"]
    stk.taxable_amount = computed["taxable_amount"]
    stk.gst_amount = computed["gst_amount"]
    stk.total_amount = computed["total_amount"]

    # Adjust product stock if quantity changed
    qty_diff = new_quantity - old_quantity
    if qty_diff != 0 and stk.product_id:
        prod = db.query(Product).filter(Product.id == stk.product_id).first()
        if prod:
            prod.stock = max(0.0, float(prod.stock or 0.0) + qty_diff)

    db.commit()
    db.refresh(stk)

    return {
        "message": f"Stock In '{stk.receipt_no}' updated successfully",
        "stock_in": format_stock_in_response(stk),
    }


# ──────────────────────────────────────────────────────────────────────────────
# 12. Delete Stock In Record (Rolls back Product Stock, accepts ANY identifier)
# ──────────────────────────────────────────────────────────────────────────────

@router.delete("/stock-in/{stock_id:path}")
@router.delete("/stock-ins/{stock_id:path}")
def delete_stock_in(stock_id: str, db: Session = Depends(get_db)):
    stk = find_stock_in_entity(stock_id, db)
    if not stk:
        raise HTTPException(status_code=404, detail=f"Stock In receipt not found for identifier '{stock_id}'")

    receipt_num = stk.receipt_no
    qty_to_revert = float(stk.quantity or 0.0)

    # Roll back product inventory stock
    if stk.product_id and qty_to_revert > 0:
        prod = db.query(Product).filter(Product.id == stk.product_id).first()
        if prod:
            prod.stock = max(0.0, float(prod.stock or 0.0) - qty_to_revert)

    db.delete(stk)
    db.commit()

    return {"message": f"Stock In '{receipt_num}' deleted successfully. Reverted {qty_to_revert} units from inventory."}


# ==============================================================================
# SECTION 12: INVOICE MANAGEMENT APIS (Create Invoice Screen)
# ==============================================================================

def compute_due_date(invoice_date_str: str, payment_terms: str) -> str:
    """Calculates due date based on invoice date and payment terms."""
    from datetime import datetime, timedelta
    dt = None
    for fmt in ("%d %b %Y", "%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"):
        try:
            dt = datetime.strptime(invoice_date_str.strip(), fmt)
            break
        except Exception:
            pass
    if not dt:
        dt = datetime.now()

    terms_lower = (payment_terms or "").lower()
    days = 30
    if "15" in terms_lower:
        days = 15
    elif "45" in terms_lower:
        days = 45
    elif "60" in terms_lower:
        days = 60
    elif "90" in terms_lower:
        days = 90
    elif "due on receipt" in terms_lower or "immediate" in terms_lower:
        days = 0

    due_dt = dt + timedelta(days=days)
    return due_dt.strftime("%d %b %Y")


def format_currency_inr(value: float) -> str:
    """Formats a float as Indian Rupee string: e.g. 125600.0 -> 'Rs 1,25,600.00'."""
    try:
        val = round(float(value), 2)
        s = f"{val:.2f}"
        int_part, dec_part = s.split(".")
        if len(int_part) > 3:
            last_three = int_part[-3:]
            rest = int_part[:-3]
            groups = []
            while len(rest) > 2:
                groups.insert(0, rest[-2:])
                rest = rest[:-2]
            if rest:
                groups.insert(0, rest)
            groups.append(last_three)
            int_formatted = ",".join(groups)
        else:
            int_formatted = int_part
        return f"Rs {int_formatted}.{dec_part}"
    except Exception:
        return f"Rs {value:.2f}"


def format_invoice_response(invoice: Invoice) -> dict:
    """Standardized dictionary representation of an invoice matching Flutter Invoice Dashboard Screen."""
    status_val = invoice.status or "Unpaid"
    status_color = "red"
    if status_val.lower() == "paid":
        status_color = "green"
    elif "partial" in status_val.lower():
        status_color = "orange"

    category_val = getattr(invoice, "category", None) or "Lift"
    if not category_val and invoice.items and len(invoice.items) > 0 and isinstance(invoice.items[0], dict):
        category_val = invoice.items[0].get("category") or "Lift"

    inv_type = getattr(invoice, "invoice_type", None) or "Sales"
    if invoice.invoice_no and invoice.invoice_no.upper().startswith("SV-"):
        inv_type = "Service"

    amt = float(invoice.grand_total or 0.0)

    return {
        "id": invoice.id,
        "invoice_no": invoice.invoice_no,
        "category": category_val,
        "invoice_type": inv_type,
        "invoice_date": invoice.invoice_date,
        "date": invoice.invoice_date,
        "due_date": invoice.due_date or "",
        "due": invoice.due_date or "",
        "amount": amt,
        "formatted_amount": format_currency_inr(amt),
        "status": status_val,
        "status_color": status_color,
        "user_id": invoice.user_id,
        "order_id": invoice.order_id,
        "order_no": invoice.order_no,
        "quotation_id": invoice.quotation_id,
        "quotation_no": invoice.quotation_no,
        "customer_name": invoice.customer_name,
        "phone": invoice.phone or "",
        "email": invoice.email or "",
        "billing_address": invoice.billing_address or "",
        "delivery_address": invoice.delivery_address or "",
        "customer": {
            "name": invoice.customer_name,
            "phone": invoice.phone or "",
            "email": invoice.email or "",
            "billing_address": invoice.billing_address or "",
            "delivery_address": invoice.delivery_address or "",
        },
        "payment_terms": invoice.payment_terms or "30 Days",
        "reference_no": invoice.reference_no or "",
        "items": invoice.items or [],
        "subtotal": float(invoice.subtotal or 0.0),
        "discount": float(invoice.discount or 0.0),
        "tax_percent": float(invoice.tax_percent or 18.0),
        "tax": float(invoice.tax or 0.0),
        "grand_total": amt,
        "amount_paid": float(invoice.amount_paid or 0.0),
        "balance_due": float(invoice.balance_due or 0.0),
        "notes": invoice.notes or "",
        "created_at": invoice.created_at.isoformat() if invoice.created_at else None,
        "updated_at": invoice.updated_at.isoformat() if invoice.updated_at else None,
    }


# ──────────────────────────────────────────────────────────────────────────────
# 0. Single Screen Data Endpoint (Initial Screen Bootstrap)
# ──────────────────────────────────────────────────────────────────────────────

@router.get("/invoices/create-data")
@router.get("/invoices/create-screen-data")
@router.get("/invoices/meta")
def get_create_invoice_screen_data(db: Session = Depends(get_db)):
    """
    SINGLE UNIFIED API FOR THE CREATE INVOICE SCREEN:
    Returns everything needed to render the Create Invoice screen in 1 single HTTP request:
    - invoice_no (next auto-generated)
    - invoice_date (today's date)
    - due_date (default 30 days)
    - payment_terms & payment_terms_options dropdown
    - orders dropdown list (with items and customer details for 1-tap auto-fill)
    - customers list (for [Select Customer] modal)
    - default_tax_percent
    """
    from datetime import datetime, timedelta

    inv_no = generate_invoice_no(db)
    today = datetime.now()
    invoice_date = today.strftime("%d %b %Y")
    due_date = (today + timedelta(days=30)).strftime("%d %b %Y")

    orders = db.query(Order).order_by(Order.id.desc()).all()
    orders_list = []
    for ord_obj in orders:
        formatted_items = []
        for idx, it in enumerate(ord_obj.items or []):
            if isinstance(it, dict):
                qty = float(it.get("qty") or it.get("quantity") or 1)
                rate = float(it.get("rate") or it.get("price") or it.get("unit_price") or 0.0)
                disc = float(it.get("discount") or 0.0)
                tax_pct = float(it.get("tax_percent") or it.get("tax") or 18.0)
                tot = float(it.get("total") or it.get("total_price") or (qty * rate))
                formatted_items.append({
                    "id": it.get("id") or it.get("product") or f"ITEM{idx+1:03d}",
                    "name": it.get("name") or it.get("product_name") or "Product",
                    "code": it.get("code") or it.get("product_code") or it.get("id") or "",
                    "category": it.get("category") or "",
                    "qty": qty,
                    "rate": rate,
                    "discount": disc,
                    "tax": tax_pct,
                    "tax_percent": tax_pct,
                    "total": tot,
                    "specifications": it.get("specifications") or {},
                })

        orders_list.append({
            "id": ord_obj.id,
            "order_id": ord_obj.id,
            "order_no": ord_obj.order_no,
            "quotation_id": ord_obj.quotation_id,
            "quotation_no": ord_obj.quotation_no,
            "order_date": ord_obj.order_date,
            "customer_name": ord_obj.customer_name,
            "phone": ord_obj.mobile or "",
            "email": ord_obj.email or "",
            "billing_address": ord_obj.billing_address or "",
            "delivery_address": ord_obj.delivery_address or "",
            "items": formatted_items,
            "subtotal": float(ord_obj.subtotal or 0.0),
            "discount": float(ord_obj.discount or 0.0),
            "tax": float(ord_obj.tax or 0.0),
            "grand_total": float(ord_obj.grand_total or 0.0),
            "payment_terms": "30 Days",
            "status": ord_obj.order_status,
        })

    customers_map = {}
    for ord_obj in orders:
        name = (ord_obj.customer_name or "").strip()
        if not name:
            continue
        key = name.lower()
        if key not in customers_map:
            customers_map[key] = {
                "customer_name": name,
                "phone": ord_obj.mobile or "",
                "email": ord_obj.email or "",
                "billing_address": ord_obj.billing_address or "",
                "delivery_address": ord_obj.delivery_address or "",
                "latest_order_id": ord_obj.id,
                "latest_order_no": ord_obj.order_no,
                "orders_count": 0,
            }
        customers_map[key]["orders_count"] += 1

    for q in db.query(Quotation).order_by(Quotation.id.desc()).all():
        name = (q.customer_name or "").strip()
        if not name:
            continue
        key = name.lower()
        if key not in customers_map:
            customers_map[key] = {
                "customer_name": name,
                "phone": q.phone or "",
                "email": q.email or "",
                "billing_address": q.address or "",
                "delivery_address": q.address or "",
                "latest_order_id": None,
                "latest_order_no": None,
                "orders_count": 0,
            }
        else:
            if not customers_map[key]["phone"] and q.phone:
                customers_map[key]["phone"] = q.phone
            if not customers_map[key]["email"] and q.email:
                customers_map[key]["email"] = q.email
            if not customers_map[key]["billing_address"] and q.address:
                customers_map[key]["billing_address"] = q.address

    customers_list = list(customers_map.values())

    return {
        "invoice_no": inv_no,
        "invoice_date": invoice_date,
        "due_date": due_date,
        "payment_terms": "30 Days",
        "payment_terms_options": [
            "Due on Receipt",
            "15 Days",
            "30 Days",
            "45 Days",
            "60 Days",
            "90 Days",
        ],
        "default_tax_percent": 18.0,
        "tax_rates": [0, 5, 12, 18, 28],
        "orders": orders_list,
        "customers": customers_list,
    }


# ──────────────────────────────────────────────────────────────────────────────
# 1. Next Auto-Generated Invoice Number
# ──────────────────────────────────────────────────────────────────────────────

@router.get("/invoices/next-invoice-number")
@router.get("/invoices/next-number")
def get_next_invoice_number_endpoint(db: Session = Depends(get_db)):
    """Generate next sequential invoice number in INV-YYMMDD-XXXX format."""
    inv_no = generate_invoice_no(db)
    return {
        "invoice_no": inv_no
    }


# ──────────────────────────────────────────────────────────────────────────────
# 2. Orders Dropdown (Auto-fills Customer Details & Items)
# ──────────────────────────────────────────────────────────────────────────────

@router.get("/invoices/orders")
def get_invoice_orders_dropdown(
    search: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    """
    Returns existing orders formatted to populate the 'Order No.' dropdown 
    in the Create Invoice screen. Enables 1-tap autofill of Customer Details & Line Items.
    """
    query = db.query(Order)
    if status:
        query = query.filter(Order.order_status.ilike(status.strip()))
    if search:
        pat = f"%{search.strip()}%"
        query = query.filter(
            or_(
                Order.order_no.ilike(pat),
                Order.customer_name.ilike(pat),
                Order.mobile.ilike(pat),
            )
        )

    orders = query.order_by(Order.id.desc()).all()
    results = []
    for ord_obj in orders:
        formatted_items = []
        for idx, it in enumerate(ord_obj.items or []):
            if isinstance(it, dict):
                qty = float(it.get("qty") or it.get("quantity") or 1)
                rate = float(it.get("rate") or it.get("price") or it.get("unit_price") or 0.0)
                disc = float(it.get("discount") or 0.0)
                tax_pct = float(it.get("tax_percent") or it.get("tax") or 18.0)
                tot = float(it.get("total") or it.get("total_price") or (qty * rate))
                formatted_items.append({
                    "id": it.get("id") or it.get("product") or f"ITEM{idx+1:03d}",
                    "name": it.get("name") or it.get("product_name") or "Product",
                    "code": it.get("code") or it.get("product_code") or it.get("id") or "",
                    "category": it.get("category") or "",
                    "qty": qty,
                    "rate": rate,
                    "discount": disc,
                    "tax": tax_pct,
                    "tax_percent": tax_pct,
                    "total": tot,
                    "specifications": it.get("specifications") or {},
                })

        results.append({
            "id": ord_obj.id,
            "order_id": ord_obj.id,
            "order_no": ord_obj.order_no,
            "quotation_id": ord_obj.quotation_id,
            "quotation_no": ord_obj.quotation_no,
            "order_date": ord_obj.order_date,
            "customer_name": ord_obj.customer_name,
            "phone": ord_obj.mobile or "",
            "email": ord_obj.email or "",
            "billing_address": ord_obj.billing_address or "",
            "delivery_address": ord_obj.delivery_address or "",
            "items": formatted_items,
            "subtotal": float(ord_obj.subtotal or 0.0),
            "discount": float(ord_obj.discount or 0.0),
            "tax": float(ord_obj.tax or 0.0),
            "grand_total": float(ord_obj.grand_total or 0.0),
            "payment_terms": "30 Days",
            "status": ord_obj.order_status,
        })

    return {
        "count": len(results),
        "orders": results,
        "results": results,
    }


# ──────────────────────────────────────────────────────────────────────────────
# 3. Customer List (Select Customer Modal)
# ──────────────────────────────────────────────────────────────────────────────

@router.get("/invoices/customers")
def get_invoice_customers(
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    """
    Returns customer list for the [Select Customer] picker in Create Invoice screen.
    Aggregates customers from Orders and Quotations with their contact information.
    """
    customers_map = {}

    # Gather from Orders
    for ord_obj in db.query(Order).order_by(Order.id.desc()).all():
        name = (ord_obj.customer_name or "").strip()
        if not name:
            continue
        key = name.lower()
        if key not in customers_map:
            customers_map[key] = {
                "customer_name": name,
                "phone": ord_obj.mobile or "",
                "email": ord_obj.email or "",
                "billing_address": ord_obj.billing_address or "",
                "delivery_address": ord_obj.delivery_address or "",
                "latest_order_id": ord_obj.id,
                "latest_order_no": ord_obj.order_no,
                "orders_count": 0,
            }
        customers_map[key]["orders_count"] += 1

    # Gather from Quotations
    for q in db.query(Quotation).order_by(Quotation.id.desc()).all():
        name = (q.customer_name or "").strip()
        if not name:
            continue
        key = name.lower()
        if key not in customers_map:
            customers_map[key] = {
                "customer_name": name,
                "phone": q.phone or "",
                "email": q.email or "",
                "billing_address": q.address or "",
                "delivery_address": q.address or "",
                "latest_order_id": None,
                "latest_order_no": None,
                "orders_count": 0,
            }
        else:
            if not customers_map[key]["phone"] and q.phone:
                customers_map[key]["phone"] = q.phone
            if not customers_map[key]["email"] and q.email:
                customers_map[key]["email"] = q.email
            if not customers_map[key]["billing_address"] and q.address:
                customers_map[key]["billing_address"] = q.address

    results = list(customers_map.values())
    if search:
        pat = search.strip().lower()
        results = [
            c for c in results
            if pat in c["customer_name"].lower()
            or pat in c["phone"].lower()
            or pat in c["email"].lower()
        ]

    return {
        "count": len(results),
        "customers": results,
        "results": results,
    }


# ──────────────────────────────────────────────────────────────────────────────
# 4. Create Invoice
# ──────────────────────────────────────────────────────────────────────────────

@router.post("/invoices", status_code=status.HTTP_201_CREATED)
@router.post("/invoices/create", status_code=status.HTTP_201_CREATED)
@router.post("/invoices/add", status_code=status.HTTP_201_CREATED)
async def create_invoice(
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Creates a new Invoice record. Accepts JSON or multipart/form-data.
    Supports auto-calculation of subtotal, tax, grand total from items if not supplied.
    """
    from datetime import datetime

    content_type = request.headers.get("content-type", "").lower()
    if "application/json" in content_type:
        try:
            payload = await request.json()
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid JSON body")
    else:
        try:
            form = await request.form()
            payload = dict(form)
            # Parse items if passed as stringified JSON
            if "items" in payload and isinstance(payload["items"], str):
                try:
                    payload["items"] = json.loads(payload["items"])
                except Exception:
                    payload["items"] = []
            if "customer" in payload and isinstance(payload["customer"], str):
                try:
                    payload["customer"] = json.loads(payload["customer"])
                except Exception:
                    payload["customer"] = {}
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid form data")

    # 1. Invoice Number
    invoice_no = str(payload.get("invoice_no") or "").strip()
    if not invoice_no:
        invoice_no = generate_invoice_no(db)
    else:
        existing = db.query(Invoice).filter(Invoice.invoice_no == invoice_no).first()
        if existing:
            invoice_no = generate_invoice_no(db)

    # 2. Date & Terms
    invoice_date = str(payload.get("invoice_date") or datetime.now().strftime("%d %b %Y")).strip()
    payment_terms = str(payload.get("payment_terms") or "30 Days").strip()
    due_date = str(payload.get("due_date") or "").strip()
    if not due_date:
        due_date = compute_due_date(invoice_date, payment_terms)

    reference_no = str(payload.get("reference_no") or "").strip() or None

    # 3. Order linkage
    order_id_val = payload.get("order_id")
    order_no_val = str(payload.get("order_no") or "").strip()
    ord_obj = None

    if order_id_val is not None and str(order_id_val).isdigit():
        ord_obj = db.query(Order).filter(Order.id == int(order_id_val)).first()
    elif order_no_val:
        ord_obj = db.query(Order).filter(Order.order_no == order_no_val).first()

    order_id = ord_obj.id if ord_obj else None
    order_no = ord_obj.order_no if ord_obj else (order_no_val or None)
    quotation_id = ord_obj.quotation_id if ord_obj else payload.get("quotation_id")
    quotation_no = ord_obj.quotation_no if ord_obj else payload.get("quotation_no")

    # 4. Customer details
    cust_data = payload.get("customer") if isinstance(payload.get("customer"), dict) else {}
    customer_name = str(
        payload.get("customer_name")
        or cust_data.get("name")
        or (ord_obj.customer_name if ord_obj else "")
    ).strip()

    if not customer_name:
        raise HTTPException(status_code=422, detail="Customer Name is required")

    phone = str(
        payload.get("phone")
        or payload.get("mobile")
        or cust_data.get("phone")
        or cust_data.get("mobile")
        or (ord_obj.mobile if ord_obj else "")
    ).strip() or None

    email = str(
        payload.get("email")
        or cust_data.get("email")
        or (ord_obj.email if ord_obj else "")
    ).strip() or None

    billing_address = str(
        payload.get("billing_address")
        or payload.get("address")
        or cust_data.get("billing_address")
        or cust_data.get("address")
        or (ord_obj.billing_address if ord_obj else "")
    ).strip() or None

    delivery_address = str(
        payload.get("delivery_address")
        or cust_data.get("delivery_address")
        or (ord_obj.delivery_address if ord_obj else "")
        or billing_address
        or ""
    ).strip() or None

    # 5. Items
    items = payload.get("items")
    if not items and ord_obj and ord_obj.items:
        items = ord_obj.items
    elif not items:
        items = []

    # Clean & format items
    formatted_items = []
    items_subtotal = 0.0
    items_discount = 0.0

    for idx, it in enumerate(items):
        if isinstance(it, dict):
            qty = float(it.get("qty") or it.get("quantity") or 1)
            rate = float(it.get("rate") or it.get("price") or it.get("unit_price") or 0.0)
            disc = float(it.get("discount") or 0.0)
            tax_pct = float(it.get("tax_percent") or it.get("tax") or 18.0)
            line_tot = float(it.get("total") or it.get("total_price") or (qty * rate))

            items_subtotal += (qty * rate)
            items_discount += disc

            formatted_items.append({
                "id": it.get("id") or f"ITEM{idx+1:03d}",
                "name": str(it.get("name") or it.get("product_name") or f"Item {idx+1}").strip(),
                "code": str(it.get("code") or it.get("product_code") or "").strip(),
                "category": str(it.get("category") or "").strip(),
                "qty": qty,
                "rate": rate,
                "discount": disc,
                "tax_percent": tax_pct,
                "tax": float(it.get("tax_amount") or round((max(0.0, (qty * rate) - disc)) * (tax_pct / 100.0), 2)),
                "total": line_tot,
                "specifications": it.get("specifications") or {},
            })

    # 6. Pricing calculations
    subtotal = float(payload.get("subtotal") if payload.get("subtotal") is not None else items_subtotal)
    discount = float(payload.get("discount") if payload.get("discount") is not None else items_discount)
    tax_percent = float(payload.get("tax_percent") if payload.get("tax_percent") is not None else 18.0)
    taxable = max(0.0, subtotal - discount)

    if payload.get("tax") is not None:
        tax = float(payload.get("tax"))
    else:
        tax = round(taxable * (tax_percent / 100.0), 2)

    if payload.get("grand_total") is not None:
        grand_total = float(payload.get("grand_total"))
    else:
        grand_total = round(taxable + tax, 2)

    amount_paid = float(payload.get("amount_paid") or 0.0)
    balance_due = float(payload.get("balance_due") if payload.get("balance_due") is not None else max(0.0, grand_total - amount_paid))

    # 7. Status & Notes
    status_val = str(payload.get("status") or "").strip().capitalize()
    if not status_val:
        if amount_paid >= grand_total and grand_total > 0:
            status_val = "Paid"
        elif amount_paid > 0:
            status_val = "Partially Paid"
        else:
            status_val = "Unpaid"

    notes = str(payload.get("notes") or "").strip() or None

    first_item_cat = formatted_items[0].get("category") if formatted_items else "Lift"
    category_val = str(payload.get("category") or first_item_cat or "Lift").strip()
    inv_type_val = str(payload.get("invoice_type") or payload.get("type") or "").strip().capitalize()
    if not inv_type_val:
        if invoice_no.upper().startswith("SV-") or "service" in category_val.lower():
            inv_type_val = "Service"
        else:
            inv_type_val = "Sales"

    # Match user account to associate invoice with specific user
    user_id_val = payload.get("user_id")
    matched_user = None
    if user_id_val and str(user_id_val).isdigit():
        matched_user = db.query(User).filter(User.id == int(user_id_val)).first()
    if not matched_user and email:
        matched_user = db.query(User).filter(User.email.ilike(email.strip())).first()
    if not matched_user and phone:
        clean_p = "".join(ch for ch in phone if ch.isdigit())
        if clean_p:
            matched_user = db.query(User).filter(User.phone_number.like(f"%{clean_p[-10:]}%")).first()
    if not matched_user and customer_name:
        matched_user = db.query(User).filter(User.full_name.ilike(customer_name.strip())).first()

    matched_user_id = matched_user.id if matched_user else (int(user_id_val) if user_id_val and str(user_id_val).isdigit() else None)

    invoice = Invoice(
        invoice_no=invoice_no,
        invoice_date=invoice_date,
        due_date=due_date,
        order_id=order_id,
        order_no=order_no,
        quotation_id=quotation_id,
        quotation_no=quotation_no,
        user_id=matched_user_id,
        customer_name=customer_name,
        phone=phone,
        email=email,
        billing_address=billing_address,
        delivery_address=delivery_address,
        payment_terms=payment_terms,
        reference_no=reference_no,
        category=category_val,
        invoice_type=inv_type_val,
        items=formatted_items,
        subtotal=subtotal,
        discount=discount,
        tax_percent=tax_percent,
        tax=tax,
        grand_total=grand_total,
        amount_paid=amount_paid,
        balance_due=balance_due,
        notes=notes,
        status=status_val,
    )

    db.add(invoice)
    db.commit()
    db.refresh(invoice)

    return {
        "message": f"Invoice '{invoice.invoice_no}' created successfully",
        "invoice": format_invoice_response(invoice),
    }


# ──────────────────────────────────────────────────────────────────────────────
# 5. List Invoices
# ──────────────────────────────────────────────────────────────────────────────

@router.get("/invoices")
def list_invoices(
    search: Optional[str] = Query(None),
    customer_name: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    order_no: Optional[str] = Query(None),
    payment_terms: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    """
    Returns list of invoices in reverse chronological order with optional filtering.
    """
    query = db.query(Invoice)

    if customer_name:
        query = query.filter(Invoice.customer_name.ilike(f"%{customer_name.strip()}%"))

    if status:
        query = query.filter(Invoice.status.ilike(status.strip()))

    if order_no:
        query = query.filter(Invoice.order_no.ilike(f"%{order_no.strip()}%"))

    if payment_terms:
        query = query.filter(Invoice.payment_terms.ilike(f"%{payment_terms.strip()}%"))

    if search:
        pat = f"%{search.strip()}%"
        query = query.filter(
            or_(
                Invoice.invoice_no.ilike(pat),
                Invoice.customer_name.ilike(pat),
                Invoice.order_no.ilike(pat),
                Invoice.reference_no.ilike(pat),
                Invoice.phone.ilike(pat),
            )
        )

    invoices = query.order_by(Invoice.id.desc()).all()
    results = [format_invoice_response(inv) for inv in invoices]

    return {
        "count": len(results),
        "invoices": results,
        "results": results,
    }


# ──────────────────────────────────────────────────────────────────────────────
# 6. User Invoice Dashboard API (For UserInvoiceDashboardScreen in Flutter)
# ──────────────────────────────────────────────────────────────────────────────

@router.get("/invoices/dashboard")
@router.get("/invoices/user-dashboard")
def get_user_invoice_dashboard(
    search: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    invoice_type: Optional[str] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Dedicated endpoint for UserInvoiceDashboardScreen:
    Bearer token is COMPULSORY (Authorization: Bearer <token>).
    Strictly calculates summary analytics cards and returns invoices ONLY for the authenticated user.
    """
    query = db.query(Invoice)

    # 1. Strictly isolate to the authenticated user
    clean_phone = "".join(ch for ch in (current_user.phone_number or "") if ch.isdigit())
    user_filters = [Invoice.user_id == current_user.id]
    legacy_conditions = []
    if current_user.email:
        legacy_conditions.append(Invoice.email.ilike(current_user.email.strip()))
    if clean_phone and len(clean_phone) >= 10:
        legacy_conditions.append(Invoice.phone.like(f"%{clean_phone[-10:]}%"))
    if legacy_conditions:
        user_filters.append(and_(Invoice.user_id.is_(None), or_(*legacy_conditions)))

    query = query.filter(or_(*user_filters))

    # 2. General Filters (Status, Category, Invoice Type)
    if status:
        query = query.filter(Invoice.status.ilike(status.strip()))
    if category:
        query = query.filter(Invoice.category.ilike(f"%{category.strip()}%"))
    if invoice_type:
        query = query.filter(Invoice.invoice_type.ilike(invoice_type.strip()))

    # 3. Global Search (Search within this user's invoices)
    if search:
        pat = f"%{search.strip()}%"
        query = query.filter(
            or_(
                Invoice.invoice_no.ilike(pat),
                Invoice.category.ilike(pat),
                Invoice.invoice_date.ilike(pat),
                Invoice.customer_name.ilike(pat),
                Invoice.status.ilike(pat),
            )
        )

    all_invoices = query.order_by(Invoice.id.desc()).all()

    # Compute Summary Analytics Cards ONLY for this user's invoices
    total_count = len(all_invoices)
    total_amount = sum(float(inv.grand_total or 0.0) for inv in all_invoices)

    paid_count = sum(1 for inv in all_invoices if (inv.status or "").lower() == "paid")
    paid_amount = sum(float(inv.grand_total or 0.0) for inv in all_invoices if (inv.status or "").lower() == "paid")

    partially_paid_count = sum(1 for inv in all_invoices if "partial" in (inv.status or "").lower())
    partially_paid_amount = sum(float(inv.grand_total or 0.0) for inv in all_invoices if "partial" in (inv.status or "").lower())

    unpaid_count = sum(1 for inv in all_invoices if (inv.status or "").lower() == "unpaid")
    unpaid_amount = sum(float(inv.grand_total or 0.0) for inv in all_invoices if (inv.status or "").lower() == "unpaid")

    formatted_all = [format_invoice_response(inv) for inv in all_invoices]
    sales_list = [inv for inv in formatted_all if inv["invoice_type"].lower() == "sales"]
    service_list = [inv for inv in formatted_all if inv["invoice_type"].lower() == "service"]

    return {
        "summary": {
            "total_invoices": {
                "title": "Total Invoice",
                "count": str(total_count),
                "amount": total_amount,
                "formatted_amount": format_currency_inr(total_amount),
            },
            "paid": {
                "title": "Paid",
                "count": str(paid_count),
                "amount": paid_amount,
                "formatted_amount": format_currency_inr(paid_amount),
            },
            "partially_paid": {
                "title": "Partially Paid",
                "count": str(partially_paid_count),
                "amount": partially_paid_amount,
                "formatted_amount": format_currency_inr(partially_paid_amount),
            },
            "unpaid": {
                "title": "Unpaid",
                "count": str(unpaid_count),
                "amount": unpaid_amount,
                "formatted_amount": format_currency_inr(unpaid_amount),
            },
        },
        "sales_invoices": sales_list,
        "service_invoices": service_list,
        "all_invoices": formatted_all,
        "count": total_count,
    }


@router.get("/invoices/sales")
def get_sales_invoices(
    search: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Returns Sales Invoices for Tab 2 (Sales Invoice) - strictly for authenticated user."""
    return get_user_invoice_dashboard(
        search=search,
        status=status,
        category=category,
        invoice_type="Sales",
        current_user=current_user,
        db=db,
    )


@router.get("/invoices/service")
def get_service_invoices(
    search: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Returns Service Invoices for Tab 3 (Service Invoice) - strictly for authenticated user."""
    return get_user_invoice_dashboard(
        search=search,
        status=status,
        category=category,
        invoice_type="Service",
        current_user=current_user,
        db=db,
    )


# ──────────────────────────────────────────────────────────────────────────────
# 7. Get Single Invoice Details
# ──────────────────────────────────────────────────────────────────────────────

@router.get("/invoices/{invoice_id}")
def get_invoice(
    invoice_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Retrieves full details of a single invoice by ID or by invoice_no (e.g., INV-260912-0001).
    Bearer token is compulsory.
    Regular users can only view their own invoice; admins can view any.
    """
    inv = None
    if invoice_id.isdigit():
        inv = db.query(Invoice).filter(Invoice.id == int(invoice_id)).first()
    if not inv:
        inv = db.query(Invoice).filter(Invoice.invoice_no == invoice_id.strip()).first()

    if not inv:
        raise HTTPException(status_code=404, detail="Invoice not found")

    # If regular user, check if invoice belongs to them
    if getattr(current_user, "role", "") != "admin":
        clean_phone = "".join(ch for ch in (current_user.phone_number or "") if ch.isdigit())
        user_name = (current_user.full_name or "").strip().lower()
        inv_name = (inv.customer_name or "").strip().lower()
        user_email = (current_user.email or "").strip().lower()
        inv_email = (inv.email or "").strip().lower()

        belongs = (
            inv.user_id == current_user.id
            or (user_name and user_name == inv_name)
            or (user_email and user_email == inv_email)
            or (clean_phone and clean_phone[-10:] in (inv.phone or ""))
        )
        if not belongs:
            raise HTTPException(status_code=403, detail="You do not have permission to view this invoice")

    return format_invoice_response(inv)


# ──────────────────────────────────────────────────────────────────────────────
# 7. Update Invoice
# ──────────────────────────────────────────────────────────────────────────────

@router.put("/invoices/{invoice_id}")
@router.patch("/invoices/{invoice_id}")
async def update_invoice(
    invoice_id: str,
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Updates an existing invoice.
    """
    inv = None
    if invoice_id.isdigit():
        inv = db.query(Invoice).filter(Invoice.id == int(invoice_id)).first()
    if not inv:
        inv = db.query(Invoice).filter(Invoice.invoice_no == invoice_id.strip()).first()

    if not inv:
        raise HTTPException(status_code=404, detail="Invoice not found")

    try:
        content_type = request.headers.get("content-type", "").lower()
        if "application/json" in content_type:
            payload = await request.json()
        else:
            form = await request.form()
            payload = dict(form)
            if "items" in payload and isinstance(payload["items"], str):
                try:
                    payload["items"] = json.loads(payload["items"])
                except Exception:
                    pass
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid payload")

    if "customer_name" in payload and payload["customer_name"]:
        inv.customer_name = str(payload["customer_name"]).strip()
    if "phone" in payload:
        inv.phone = str(payload["phone"] or "").strip() or None
    if "email" in payload:
        inv.email = str(payload["email"] or "").strip() or None
    if "billing_address" in payload:
        inv.billing_address = str(payload["billing_address"] or "").strip() or None
    if "delivery_address" in payload:
        inv.delivery_address = str(payload["delivery_address"] or "").strip() or None
    if "invoice_date" in payload and payload["invoice_date"]:
        inv.invoice_date = str(payload["invoice_date"]).strip()
    if "due_date" in payload and payload["due_date"]:
        inv.due_date = str(payload["due_date"]).strip()
    if "payment_terms" in payload and payload["payment_terms"]:
        inv.payment_terms = str(payload["payment_terms"]).strip()
    if "reference_no" in payload:
        inv.reference_no = str(payload["reference_no"] or "").strip() or None
    if "notes" in payload:
        inv.notes = str(payload["notes"] or "").strip() or None
    if "status" in payload and payload["status"]:
        inv.status = str(payload["status"]).strip().capitalize()

    if "items" in payload and isinstance(payload["items"], list):
        formatted_items = []
        calc_subtotal = 0.0
        calc_discount = 0.0
        for idx, it in enumerate(payload["items"]):
            if isinstance(it, dict):
                qty = float(it.get("qty") or it.get("quantity") or 1)
                rate = float(it.get("rate") or it.get("price") or 0.0)
                disc = float(it.get("discount") or 0.0)
                tax_pct = float(it.get("tax_percent") or 18.0)
                tot = float(it.get("total") or (qty * rate))
                calc_subtotal += (qty * rate)
                calc_discount += disc
                formatted_items.append({
                    "id": it.get("id") or f"ITEM{idx+1:03d}",
                    "name": str(it.get("name") or "Item").strip(),
                    "code": str(it.get("code") or "").strip(),
                    "category": str(it.get("category") or "").strip(),
                    "qty": qty,
                    "rate": rate,
                    "discount": disc,
                    "tax_percent": tax_pct,
                    "tax": float(it.get("tax") or round(max(0.0, (qty * rate) - disc) * (tax_pct / 100.0), 2)),
                    "total": tot,
                    "specifications": it.get("specifications") or {},
                })
        inv.items = formatted_items
        if "subtotal" not in payload:
            inv.subtotal = calc_subtotal
        if "discount" not in payload:
            inv.discount = calc_discount

    if "subtotal" in payload:
        inv.subtotal = float(payload["subtotal"])
    if "discount" in payload:
        inv.discount = float(payload["discount"])
    if "tax_percent" in payload:
        inv.tax_percent = float(payload["tax_percent"])
    if "tax" in payload:
        inv.tax = float(payload["tax"])
    elif "subtotal" in payload or "discount" in payload or "items" in payload:
        inv.tax = round(max(0.0, inv.subtotal - inv.discount) * (inv.tax_percent / 100.0), 2)

    if "grand_total" in payload:
        inv.grand_total = float(payload["grand_total"])
    elif "subtotal" in payload or "tax" in payload or "items" in payload:
        inv.grand_total = round(max(0.0, inv.subtotal - inv.discount) + inv.tax, 2)

    if "amount_paid" in payload:
        inv.amount_paid = float(payload["amount_paid"])
    if "balance_due" in payload:
        inv.balance_due = float(payload["balance_due"])
    else:
        inv.balance_due = max(0.0, inv.grand_total - inv.amount_paid)

    db.commit()
    db.refresh(inv)

    return {
        "message": f"Invoice '{inv.invoice_no}' updated successfully",
        "invoice": format_invoice_response(inv),
    }


# ──────────────────────────────────────────────────────────────────────────────
# 8. Quick Status Update
# ──────────────────────────────────────────────────────────────────────────────

@router.patch("/invoices/{invoice_id}/status")
@router.put("/invoices/{invoice_id}/status")
async def update_invoice_status(
    invoice_id: str,
    request: Request,
    db: Session = Depends(get_db),
):
    """Quickly update invoice status (Unpaid, Paid, Partially Paid, Overdue, Cancelled)."""
    inv = None
    if invoice_id.isdigit():
        inv = db.query(Invoice).filter(Invoice.id == int(invoice_id)).first()
    if not inv:
        inv = db.query(Invoice).filter(Invoice.invoice_no == invoice_id.strip()).first()

    if not inv:
        raise HTTPException(status_code=404, detail="Invoice not found")

    try:
        payload = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON body")

    new_status = str(payload.get("status") or "").strip().capitalize()
    if not new_status:
        raise HTTPException(status_code=422, detail="'status' is required")

    inv.status = new_status
    if new_status == "Paid":
        inv.amount_paid = inv.grand_total
        inv.balance_due = 0.0
    elif new_status == "Unpaid":
        inv.amount_paid = 0.0
        inv.balance_due = inv.grand_total

    db.commit()
    db.refresh(inv)

    return {
        "message": f"Invoice '{inv.invoice_no}' status updated to '{inv.status}'",
        "invoice": format_invoice_response(inv),
    }


# ──────────────────────────────────────────────────────────────────────────────
# 9. Delete Invoice
# ──────────────────────────────────────────────────────────────────────────────

@router.delete("/invoices/{invoice_id}")
def delete_invoice(invoice_id: str, db: Session = Depends(get_db)):
    """Deletes an invoice record."""
    inv = None
    if invoice_id.isdigit():
        inv = db.query(Invoice).filter(Invoice.id == int(invoice_id)).first()
    if not inv:
        inv = db.query(Invoice).filter(Invoice.invoice_no == invoice_id.strip()).first()

    if not inv:
        raise HTTPException(status_code=404, detail="Invoice not found")

    num = inv.invoice_no
    db.delete(inv)
    db.commit()

    return {"message": f"Invoice '{num}' deleted successfully"}












