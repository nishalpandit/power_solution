import json
import os
import uuid
from pathlib import Path
from typing import Optional, Union

from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, Request, UploadFile, status
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from api.models import Category, CashBill, Order, Payment, Product, Quotation, User
from api.schemas import (
    AdminLoginRequest,
    CashBillCalculateRequest,
    CashBillCalculateResponse,
    CashBillCreateRequest,
    CashBillResponse,
    CashBillUpdateRequest,
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
    QuotationCreateRequest,
    QuotationItemSchema,
    QuotationListResponse,
    QuotationResponse,
    ServiceProductCreateRequest,
    UserLoginRequest,
    UserRegisterRequest,
)
from core.auth import create_access_token, hash_password, require_admin, verify_password
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
    return f"{prefix}{new_seq:04d}"


@router.get("/quotations/next-number")
def get_next_quotation_number(db: Session = Depends(get_db)):
    """Generate the next sequential quotation number in QTN-YYMMDD-XXXX format."""
    next_no = generate_quotation_no(db)
    return {"quotation_no": next_no}


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


@router.get("/quotations/{quotation_id}")
def get_quotation(quotation_id: int, db: Session = Depends(get_db)):
    quotation = db.query(Quotation).filter(Quotation.id == quotation_id).first()
    if not quotation:
        raise HTTPException(status_code=404, detail="Quotation not found")
    return format_quotation_response(quotation)


@router.put("/quotations/{quotation_id}")
async def update_quotation(
    quotation_id: int,
    request: Request,
    db: Session = Depends(get_db),
):
    """Update an existing quotation. Supports BOTH multipart/form-data and application/json."""
    quotation = db.query(Quotation).filter(Quotation.id == quotation_id).first()
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

    status_val = (payload.status or quotation.status).strip().capitalize()

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
    quotation.terms = payload.terms.strip() if payload.terms else None
    quotation.status = status_val

    db.commit()
    db.refresh(quotation)

    return {
        "message": f"Quotation '{quotation.quotation_no}' updated successfully",
        "quotation": format_quotation_response(quotation),
    }


@router.delete("/quotations/{quotation_id}")
def delete_quotation(quotation_id: int, db: Session = Depends(get_db)):
    quotation = db.query(Quotation).filter(Quotation.id == quotation_id).first()
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
    return {
        "id": payment.id,
        "invoice_no": payment.invoice_no,
        "order_no": payment.invoice_no,
        "customer_name": payment.customer_name,
        "customer_phone": payment.customer_phone,
        "customer_email": payment.customer_email,
        "customer_address": payment.customer_address,
        "quotation_id": payment.quotation_id,
        "quotation_no": payment.quotation_no,
        "payment_date": payment.payment_date,
        "amount_received": payment.amount_received,
        "payment_mode": payment.payment_mode,
        "transaction_no": payment.transaction_no,
        "reference_no": payment.reference_no,
        "notes": payment.notes,
        "payment_proof": payment.payment_proof,
        "status": payment.status,
        "created_at": payment.created_at.isoformat() if payment.created_at else None,
        "updated_at": payment.updated_at.isoformat() if payment.updated_at else None,
    }


def generate_invoice_no(db: Session) -> str:
    from datetime import datetime
    date_str = datetime.now().strftime("%y%m%d")
    prefix = f"INV-{date_str}-"
    last_p = (
        db.query(Payment)
        .filter(Payment.invoice_no.like(f"{prefix}%"))
        .order_by(Payment.id.desc())
        .first()
    )
    if last_p and last_p.invoice_no:
        try:
            last_seq = int(last_p.invoice_no.split("-")[-1])
            new_seq = last_seq + 1
        except Exception:
            new_seq = 1
    else:
        new_seq = 1
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


@router.post("/payments", status_code=status.HTTP_201_CREATED)
@router.post("/payment/add", status_code=status.HTTP_201_CREATED)
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

    customer_name = str(payload.get("customer_name") or "").strip()
    if not customer_name:
        raise HTTPException(status_code=400, detail="Customer name is required")

    amount_received = payload.get("amount_received")
    if amount_received is None or str(amount_received).strip() == "":
        raise HTTPException(status_code=400, detail="Amount received is required")
    try:
        amount_received = float(amount_received)
        if amount_received < 0:
            raise ValueError()
    except Exception:
        raise HTTPException(status_code=400, detail="Amount received must be a valid positive number")

    # Resolve invoice / order number
    invoice_no = str(payload.get("invoice_no") or payload.get("order_no") or "").strip()
    if not invoice_no:
        invoice_no = generate_invoice_no(db)
    else:
        existing_p = db.query(Payment).filter(Payment.invoice_no == invoice_no).first()
        if existing_p:
            raise HTTPException(status_code=400, detail=f"Invoice/Order number '{invoice_no}' already exists")

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
    quotation_id = payload.get("quotation_id")
    quotation_no = str(payload.get("quotation_no") or "").strip() or None
    customer_phone = str(payload.get("customer_phone") or payload.get("phone") or "").strip() or None
    customer_email = str(payload.get("customer_email") or payload.get("email") or "").strip() or None
    customer_address = str(payload.get("customer_address") or payload.get("address") or "").strip() or None

    if quotation_id and str(quotation_id).isdigit():
        q_obj = db.query(Quotation).filter(Quotation.id == int(quotation_id)).first()
        if q_obj:
            quotation_no = q_obj.quotation_no
            if not customer_phone:
                customer_phone = q_obj.phone
            if not customer_email:
                customer_email = q_obj.email
            if not customer_address:
                customer_address = q_obj.address
    elif quotation_no:
        q_obj = db.query(Quotation).filter(Quotation.quotation_no == quotation_no).first()
        if q_obj:
            quotation_id = q_obj.id
            if not customer_phone:
                customer_phone = q_obj.phone
            if not customer_email:
                customer_email = q_obj.email
            if not customer_address:
                customer_address = q_obj.address

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


@router.get("/payments/{payment_id}")
def get_payment(payment_id: int, db: Session = Depends(get_db)):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
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
    if not order_no:
        order_no = generate_order_no(db)

    # Check order_no uniqueness
    existing_order = db.query(Order).filter(Order.order_no == order_no).first()
    if existing_order:
        raise HTTPException(status_code=400, detail=f"Order number '{order_no}' already exists")

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
    if not bill_no:
        bill_no = generate_bill_no(db)

    # Check bill_no uniqueness
    existing_bill = db.query(CashBill).filter(CashBill.bill_no == bill_no).first()
    if existing_bill:
        raise HTTPException(status_code=400, detail=f"Bill number '{bill_no}' already exists")

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




