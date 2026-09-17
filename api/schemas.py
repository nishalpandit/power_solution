import json
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, EmailStr, field_validator, model_validator


# ==============================================================================
# CATEGORY SCHEMAS
# ==============================================================================

class CategoryCreateRequest(BaseModel):
    category_name: str
    category_code: str
    category_type: str
    description: Optional[str] = None
    display_order: int = 0
    status: str = "active"

    @field_validator("category_name")
    @classmethod
    def validate_category_name(cls, value: str) -> str:
        name = value.strip()
        if len(name) < 2:
            raise ValueError("Category name must be at least 2 characters long")
        return name

    @field_validator("category_code")
    @classmethod
    def validate_category_code(cls, value: str) -> str:
        code = value.strip()
        if len(code) < 2:
            raise ValueError("Category code must be at least 2 characters long")
        return code

    @field_validator("category_type")
    @classmethod
    def validate_category_type(cls, value: str) -> str:
        cleaned = value.strip().lower().replace("_", " ").replace("-", " ")
        allowed = {"lift", "generator", "panel", "earthing", "service", "other", "lift generator"}
        if cleaned not in allowed:
            raise ValueError(
                "Category type must be one of: lift, generator, panel, earthing, service, other"
            )
        return cleaned

    @field_validator("status")
    @classmethod
    def validate_status(cls, value: str) -> str:
        status_value = value.strip().lower()
        if status_value not in {"active", "inactive"}:
            raise ValueError("Status must be either active or inactive")
        return status_value

    @field_validator("display_order")
    @classmethod
    def validate_display_order(cls, value: int) -> int:
        if value < 0:
            raise ValueError("Display order must be a positive number")
        return value


# ==============================================================================
# USER / AUTH SCHEMAS
# ==============================================================================

class UserRegisterRequest(BaseModel):
    full_name: str
    email: EmailStr
    phone_number: str
    password: str
    confirm_password: str

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, value: str) -> str:
        name = value.strip()
        if len(name) < 2:
            raise ValueError("Full name must be at least 2 characters long")
        return name

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, value: str) -> str:
        cleaned = value.strip()
        if len(cleaned) < 7:
            raise ValueError("Phone number must be at least 7 characters long")
        if not all(char.isdigit() or char in "+()- " for char in cleaned):
            raise ValueError("Phone number contains invalid characters")
        return cleaned

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if len(value) < 5:
            raise ValueError("Password must be at least 5 characters long")
        return value

    @model_validator(mode="after")
    def validate_password_match(self):
        if self.password != self.confirm_password:
            raise ValueError("Password and confirm password do not match")
        return self


class UserLoginRequest(BaseModel):
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    password: str

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        cleaned = value.strip()
        if len(cleaned) < 7:
            raise ValueError("Phone number must be at least 7 characters long")
        if not all(char.isdigit() or char in "+()- " for char in cleaned):
            raise ValueError("Phone number contains invalid characters")
        return cleaned

    @model_validator(mode="after")
    def validate_identifier(self):
        if not self.email and not self.phone_number:
            raise ValueError("Either email or phone number is required for login")
        return self


class AdminLoginRequest(BaseModel):
    username: str
    password: str

    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str) -> str:
        username = value.strip()
        if len(username) < 3:
            raise ValueError("Username must be at least 3 characters long")
        return username

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if len(value) < 5:
            raise ValueError("Password must be at least 5 characters long")
        return value


# ==============================================================================
# PRODUCT SCHEMAS - HELPER FUNCTIONS
# ==============================================================================

def parse_string_or_list(value: Any) -> List[str]:
    if not value:
        return []
    if isinstance(value, list):
        return [str(v).strip() for v in value if str(v).strip()]
    if isinstance(value, str):
        val = value.strip()
        if val.startswith("[") and val.endswith("]"):
            try:
                parsed = json.loads(val)
                if isinstance(parsed, list):
                    return [str(v).strip() for v in parsed if str(v).strip()]
            except Exception:
                pass
        return [item.strip() for item in val.split(",") if item.strip()]
    return []


# ==============================================================================
# PRODUCT BASE SCHEMA
# ==============================================================================

class ProductBaseRequest(BaseModel):
    category_id: Optional[Union[int, str]] = None
    category_name: Optional[str] = None
    product_name: str
    product_code: str  # SKU
    brand: Optional[str] = None
    model_number: Optional[str] = None
    description: Optional[str] = None

    # Pricing & Tax
    purchase_price: Optional[Union[float, str]] = None
    selling_price: Optional[Union[float, str]] = None
    discount: Optional[str] = None
    gst_rate: Optional[str] = None
    hsn_code: Optional[str] = None

    # Inventory
    inventory_tracking: bool = False
    stock: Optional[Union[float, str]] = 0.0
    unit: Optional[str] = None
    min_stock: Optional[Union[float, str]] = 0.0

    # Warranty & Terms
    warranty_period: Optional[str] = None
    warranty_terms: Optional[str] = None
    payment_terms: Optional[str] = None

    # Status & Media
    product_image: Optional[str] = None
    status: str = "Active"

    @model_validator(mode="before")
    @classmethod
    def resolve_aliases(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if not data.get("product_code") and data.get("sku"):
                data["product_code"] = data["sku"]
            if not data.get("description") and data.get("product_description"):
                data["description"] = data["product_description"]
            if not data.get("category_name") and data.get("category"):
                data["category_name"] = data["category"]
            if data.get("stock") is None and data.get("initial_stock") is not None:
                data["stock"] = data["initial_stock"]
            if data.get("min_stock") is None and data.get("low_stock_limit") is not None:
                data["min_stock"] = data["low_stock_limit"]
            if not data.get("product_image") and isinstance(data.get("image"), str):
                data["product_image"] = data["image"]
        return data

    @field_validator("category_id", mode="before")
    @classmethod
    def parse_category_id(cls, value: Any) -> Optional[int]:
        if value is None or value == "" or value == "null":
            return None
        try:
            return int(value)
        except (ValueError, TypeError):
            return None

    @field_validator("product_name")
    @classmethod
    def validate_product_name(cls, value: str) -> str:
        name = value.strip()
        if len(name) < 2:
            raise ValueError("Product name must be at least 2 characters long")
        return name

    @field_validator("product_code")
    @classmethod
    def validate_product_code(cls, value: str) -> str:
        code = value.strip()
        if len(code) < 2:
            raise ValueError("Product code / SKU must be at least 2 characters long")
        return code

    @field_validator("status")
    @classmethod
    def validate_status(cls, value: str) -> str:
        s = value.strip().lower()
        if s not in {"active", "inactive"}:
            raise ValueError("Status must be either active or inactive")
        return s.capitalize()

    @field_validator("purchase_price", "selling_price", "stock", "min_stock", mode="before")
    @classmethod
    def parse_optional_float(cls, value: Any) -> Optional[float]:
        if value is None or value == "":
            return None
        try:
            return float(value)
        except (ValueError, TypeError):
            return None

    @field_validator("inventory_tracking", mode="before")
    @classmethod
    def parse_boolean(cls, value: Any) -> bool:
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.strip().lower() in {"true", "1", "yes", "on"}
        return bool(value)


# ==============================================================================
# 1. LIFT SPECIFICATIONS & SUBMISSION REQUEST
# ==============================================================================

class LiftSpecificationSchema(BaseModel):
    # Lift General Specification
    lift_type: Optional[str] = None
    operation_type: Optional[str] = None
    capacity: Optional[str] = None
    rated_load: Optional[str] = None
    speed: Optional[str] = None
    floor_designation: Optional[str] = None
    number_of_floors: Optional[str] = None
    number_of_stops: Optional[str] = None
    landing_entrances: Optional[str] = None
    car_entrances: Optional[str] = None
    car_openings: Optional[str] = None

    # Shaft & Construction
    shaft_structure: Optional[str] = None
    shaft_net_size: Optional[str] = None
    shaft_height: Optional[str] = None
    floor_height: Optional[str] = None
    pit_depth: Optional[str] = None
    overhead_height: Optional[str] = None
    car_dimensions: Optional[str] = None
    cabin_size: Optional[str] = None

    # Drive & Electrical
    machine_type: Optional[str] = None
    machine_model: Optional[str] = None
    drive_system: Optional[str] = None
    motor_brand: Optional[str] = None
    controller_brand: Optional[str] = None
    control_panel_type: Optional[str] = None
    power_supply: Optional[str] = None
    voltage: Optional[str] = None
    phase: Optional[str] = None
    frequency: Optional[str] = None
    brake_type: Optional[str] = None

    # Cabin & Door
    car_finishing: Optional[str] = None
    cabin_finish: Optional[str] = None
    false_ceiling: Optional[str] = None
    flooring_type: Optional[str] = None
    car_door_type: Optional[str] = None
    car_door_finish: Optional[str] = None
    landing_door_finish: Optional[str] = None
    door_opening: Optional[str] = None
    door_sill: Optional[str] = None
    landing_door_lock: Optional[str] = None

    # Safety Features
    safety_features: List[str] = []

    @field_validator("safety_features", mode="before")
    @classmethod
    def validate_safety_features(cls, value: Any) -> List[str]:
        return parse_string_or_list(value)


class LiftProductCreateRequest(ProductBaseRequest):
    # Allow top-level fields for direct form binding
    lift_type: Optional[str] = None
    operation_type: Optional[str] = None
    capacity: Optional[str] = None
    rated_load: Optional[str] = None
    speed: Optional[str] = None
    floor_designation: Optional[str] = None
    number_of_floors: Optional[str] = None
    number_of_stops: Optional[str] = None
    landing_entrances: Optional[str] = None
    car_entrances: Optional[str] = None
    car_openings: Optional[str] = None

    shaft_structure: Optional[str] = None
    shaft_net_size: Optional[str] = None
    shaft_height: Optional[str] = None
    floor_height: Optional[str] = None
    pit_depth: Optional[str] = None
    overhead_height: Optional[str] = None
    car_dimensions: Optional[str] = None
    cabin_size: Optional[str] = None

    machine_type: Optional[str] = None
    machine_model: Optional[str] = None
    drive_system: Optional[str] = None
    motor_brand: Optional[str] = None
    controller_brand: Optional[str] = None
    control_panel_type: Optional[str] = None
    power_supply: Optional[str] = None
    voltage: Optional[str] = None
    phase: Optional[str] = None
    frequency: Optional[str] = None
    brake_type: Optional[str] = None

    car_finishing: Optional[str] = None
    cabin_finish: Optional[str] = None
    false_ceiling: Optional[str] = None
    flooring_type: Optional[str] = None
    car_door_type: Optional[str] = None
    car_door_finish: Optional[str] = None
    landing_door_finish: Optional[str] = None
    door_opening: Optional[str] = None
    door_sill: Optional[str] = None
    landing_door_lock: Optional[str] = None

    safety_features: Optional[Union[List[str], str]] = None
    specifications: Optional[Union[LiftSpecificationSchema, Dict[str, Any]]] = None

    def extract_specifications(self) -> Dict[str, Any]:
        specs: Dict[str, Any] = {}
        if self.specifications:
            if isinstance(self.specifications, BaseModel):
                specs.update(self.specifications.model_dump())
            elif isinstance(self.specifications, dict):
                specs.update(self.specifications)

        keys = [
            "lift_type", "operation_type", "capacity", "rated_load", "speed",
            "floor_designation", "number_of_floors", "number_of_stops",
            "landing_entrances", "car_entrances", "car_openings", "shaft_structure",
            "shaft_net_size", "shaft_height", "floor_height", "pit_depth",
            "overhead_height", "car_dimensions", "cabin_size", "machine_type",
            "machine_model", "drive_system", "motor_brand", "controller_brand",
            "control_panel_type", "power_supply", "voltage", "phase", "frequency",
            "brake_type", "car_finishing", "cabin_finish", "false_ceiling",
            "flooring_type", "car_door_type", "car_door_finish",
            "landing_door_finish", "door_opening", "door_sill", "landing_door_lock",
        ]
        for key in keys:
            val = getattr(self, key, None)
            if val is not None:
                specs[key] = val

        if self.safety_features is not None:
            specs["safety_features"] = parse_string_or_list(self.safety_features)
        elif "safety_features" not in specs:
            specs["safety_features"] = []

        return specs


# ==============================================================================
# 2. GENERATOR (DG) SPECIFICATIONS & SUBMISSION REQUEST
# ==============================================================================

class GeneratorSpecificationSchema(BaseModel):
    # DG General Specification
    dg_rating: Optional[str] = None
    rated_power_kw: Optional[str] = None
    output_voltage: Optional[str] = None
    phase: Optional[str] = None
    starting_voltage: Optional[str] = None
    fuel_tank_capacity: Optional[str] = None

    # Engine Specification
    engine_brand: Optional[str] = None
    engine_model: Optional[str] = None
    bhp: Optional[str] = None
    rated_speed: Optional[str] = None
    rated_power: Optional[str] = None
    number_of_cylinders: Optional[str] = None
    governor_type: Optional[str] = None
    aspiration_type: Optional[str] = None
    cooling_mode: Optional[str] = None

    # Alternator Specification
    alternator_brand: Optional[str] = None
    alternator_model: Optional[str] = None
    alternator_capacity: Optional[str] = None
    rated_current: Optional[str] = None
    exciting_mode: Optional[str] = None
    insulation_class: Optional[str] = None
    protection_class: Optional[str] = None
    voltage_control: Optional[str] = None

    # DG Control Panel
    control_panel_type: Optional[str] = None
    amf_panel: Optional[str] = None
    battery_charger: Optional[str] = None
    acoustic_enclosure: Optional[str] = None
    radiator_cooling: Optional[str] = None


class GeneratorProductCreateRequest(ProductBaseRequest):
    dg_rating: Optional[str] = None
    rated_power_kw: Optional[str] = None
    output_voltage: Optional[str] = None
    phase: Optional[str] = None
    starting_voltage: Optional[str] = None
    fuel_tank_capacity: Optional[str] = None

    engine_brand: Optional[str] = None
    engine_model: Optional[str] = None
    bhp: Optional[str] = None
    rated_speed: Optional[str] = None
    rated_power: Optional[str] = None
    number_of_cylinders: Optional[str] = None
    governor_type: Optional[str] = None
    aspiration_type: Optional[str] = None
    cooling_mode: Optional[str] = None

    alternator_brand: Optional[str] = None
    alternator_model: Optional[str] = None
    alternator_capacity: Optional[str] = None
    rated_current: Optional[str] = None
    exciting_mode: Optional[str] = None
    insulation_class: Optional[str] = None
    protection_class: Optional[str] = None
    voltage_control: Optional[str] = None

    control_panel_type: Optional[str] = None
    amf_panel: Optional[str] = None
    battery_charger: Optional[str] = None
    acoustic_enclosure: Optional[str] = None
    radiator_cooling: Optional[str] = None

    specifications: Optional[Union[GeneratorSpecificationSchema, Dict[str, Any]]] = None

    def extract_specifications(self) -> Dict[str, Any]:
        specs: Dict[str, Any] = {}
        if self.specifications:
            if isinstance(self.specifications, BaseModel):
                specs.update(self.specifications.model_dump())
            elif isinstance(self.specifications, dict):
                specs.update(self.specifications)

        keys = [
            "dg_rating", "rated_power_kw", "output_voltage", "phase", "starting_voltage",
            "fuel_tank_capacity", "engine_brand", "engine_model", "bhp", "rated_speed",
            "rated_power", "number_of_cylinders", "governor_type", "aspiration_type",
            "cooling_mode", "alternator_brand", "alternator_model", "alternator_capacity",
            "rated_current", "exciting_mode", "insulation_class", "protection_class",
            "voltage_control", "control_panel_type", "amf_panel", "battery_charger",
            "acoustic_enclosure", "radiator_cooling",
        ]
        for key in keys:
            val = getattr(self, key, None)
            if val is not None:
                specs[key] = val

        return specs


# ==============================================================================
# 3. PANEL SPECIFICATIONS & SUBMISSION REQUEST
# ==============================================================================

class PanelSpecificationSchema(BaseModel):
    # Panel Construction
    panel_construction: Optional[str] = None
    sheet_thickness: Optional[str] = None
    cable_alley: Optional[str] = None
    door_gasket: Optional[str] = None
    feeder_nomenclature: Optional[str] = None
    metal_joint: Optional[str] = None
    panel_painting: Optional[str] = None
    danger_board: Optional[str] = None
    door_knob: Optional[str] = None
    door_locking: Optional[str] = None
    base_angle_frame: Optional[str] = None

    # Busbar Specification
    busbar_material: Optional[str] = None
    busbar_insulator: Optional[str] = None
    phase_barrier: Optional[str] = None
    earth_busbar: Optional[str] = None
    busbar_distance: Optional[str] = None

    # Cable & Wiring Specification
    input_cable_connection: Optional[str] = None
    output_cable_connection: Optional[str] = None
    gland_plate_thickness: Optional[str] = None
    control_wiring: Optional[str] = None
    cable_entry: Optional[str] = None
    power_supply: Optional[str] = None


class PanelProductCreateRequest(ProductBaseRequest):
    panel_construction: Optional[str] = None
    sheet_thickness: Optional[str] = None
    cable_alley: Optional[str] = None
    door_gasket: Optional[str] = None
    feeder_nomenclature: Optional[str] = None
    metal_joint: Optional[str] = None
    panel_painting: Optional[str] = None
    danger_board: Optional[str] = None
    door_knob: Optional[str] = None
    door_locking: Optional[str] = None
    base_angle_frame: Optional[str] = None

    busbar_material: Optional[str] = None
    busbar_insulator: Optional[str] = None
    phase_barrier: Optional[str] = None
    earth_busbar: Optional[str] = None
    busbar_distance: Optional[str] = None

    input_cable_connection: Optional[str] = None
    output_cable_connection: Optional[str] = None
    gland_plate_thickness: Optional[str] = None
    control_wiring: Optional[str] = None
    cable_entry: Optional[str] = None
    power_supply: Optional[str] = None

    specifications: Optional[Union[PanelSpecificationSchema, Dict[str, Any]]] = None

    def extract_specifications(self) -> Dict[str, Any]:
        specs: Dict[str, Any] = {}
        if self.specifications:
            if isinstance(self.specifications, BaseModel):
                specs.update(self.specifications.model_dump())
            elif isinstance(self.specifications, dict):
                specs.update(self.specifications)

        keys = [
            "panel_construction", "sheet_thickness", "cable_alley", "door_gasket",
            "feeder_nomenclature", "metal_joint", "panel_painting", "danger_board",
            "door_knob", "door_locking", "base_angle_frame", "busbar_material",
            "busbar_insulator", "phase_barrier", "earth_busbar", "busbar_distance",
            "input_cable_connection", "output_cable_connection", "gland_plate_thickness",
            "control_wiring", "cable_entry", "power_supply",
        ]
        for key in keys:
            val = getattr(self, key, None)
            if val is not None:
                specs[key] = val

        return specs


# ==============================================================================
# 4. EARTHING SPECIFICATIONS & SUBMISSION REQUEST
# ==============================================================================

class EarthingSpecificationSchema(BaseModel):
    earthing_type: Optional[str] = None
    specification: Optional[str] = None


class EarthingProductCreateRequest(ProductBaseRequest):
    earthing_type: Optional[str] = None
    specification: Optional[str] = None

    specifications: Optional[Union[EarthingSpecificationSchema, Dict[str, Any]]] = None

    def extract_specifications(self) -> Dict[str, Any]:
        specs: Dict[str, Any] = {}
        if self.specifications:
            if isinstance(self.specifications, BaseModel):
                specs.update(self.specifications.model_dump())
            elif isinstance(self.specifications, dict):
                specs.update(self.specifications)

        if self.earthing_type is not None:
            specs["earthing_type"] = self.earthing_type
        if self.specification is not None:
            specs["specification"] = self.specification

        return specs


# ==============================================================================
# 5. SERVICE SPECIFICATIONS & SUBMISSION REQUEST
# ==============================================================================

class ServiceSpecificationSchema(BaseModel):
    service_name: Optional[str] = None
    service_type: Optional[str] = None
    contract_type: Optional[str] = None
    contract_duration: Optional[str] = None
    visit_frequency: Optional[str] = None
    service_amount: Optional[Union[float, str]] = None
    service_coverage: Optional[str] = None
    service_description: Optional[str] = None
    checklist: List[str] = []

    @field_validator("checklist", mode="before")
    @classmethod
    def validate_checklist(cls, value: Any) -> List[str]:
        return parse_string_or_list(value)


class ServiceProductCreateRequest(ProductBaseRequest):
    service_name: Optional[str] = None
    service_type: Optional[str] = None
    contract_type: Optional[str] = None
    contract_duration: Optional[str] = None
    visit_frequency: Optional[str] = None
    service_amount: Optional[Union[float, str]] = None
    service_coverage: Optional[str] = None
    service_description: Optional[str] = None
    checklist: Optional[Union[List[str], str]] = None

    specifications: Optional[Union[ServiceSpecificationSchema, Dict[str, Any]]] = None

    def extract_specifications(self) -> Dict[str, Any]:
        specs: Dict[str, Any] = {}
        if self.specifications:
            if isinstance(self.specifications, BaseModel):
                specs.update(self.specifications.model_dump())
            elif isinstance(self.specifications, dict):
                specs.update(self.specifications)

        keys = [
            "service_name", "service_type", "contract_type", "contract_duration",
            "visit_frequency", "service_amount", "service_coverage", "service_description",
        ]
        for key in keys:
            val = getattr(self, key, None)
            if val is not None:
                specs[key] = val

        if self.checklist is not None:
            specs["checklist"] = parse_string_or_list(self.checklist)
        elif "checklist" not in specs:
            specs["checklist"] = []

        return specs


# ==============================================================================
# 6. OTHER SPECIFICATIONS & SUBMISSION REQUEST
# ==============================================================================

class OtherSpecificationSchema(BaseModel):
    custom_specifications: Optional[Union[Dict[str, Any], str]] = None


class OtherProductCreateRequest(ProductBaseRequest):
    custom_specifications: Optional[Union[Dict[str, Any], str]] = None
    specifications: Optional[Union[OtherSpecificationSchema, Dict[str, Any]]] = None

    def extract_specifications(self) -> Dict[str, Any]:
        specs: Dict[str, Any] = {}
        if self.specifications:
            if isinstance(self.specifications, BaseModel):
                specs.update(self.specifications.model_dump())
            elif isinstance(self.specifications, dict):
                specs.update(self.specifications)

        if self.custom_specifications is not None:
            specs["custom_specifications"] = self.custom_specifications

        return specs


# ==============================================================================
# PRODUCT RESPONSE SCHEMAS
# ==============================================================================

class ProductResponse(BaseModel):
    id: int
    category_type: str
    category_id: Optional[int] = None
    category_name: Optional[str] = None
    product_name: str
    product_code: str
    brand: Optional[str] = None
    model_number: Optional[str] = None
    description: Optional[str] = None

    purchase_price: Optional[float] = None
    selling_price: Optional[float] = None
    discount: Optional[str] = None
    gst_rate: Optional[str] = None
    hsn_code: Optional[str] = None

    inventory_tracking: bool = False
    stock: Optional[float] = 0.0
    unit: Optional[str] = None
    min_stock: Optional[float] = 0.0

    warranty_period: Optional[str] = None
    warranty_terms: Optional[str] = None
    payment_terms: Optional[str] = None

    product_image: Optional[str] = None
    status: str = "Active"

    specifications: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ProductListResponse(BaseModel):
    count: int
    results: List[ProductResponse]


# ==============================================================================
# QUOTATION SCHEMAS
# ==============================================================================

class QuotationItemSchema(BaseModel):
    type: str  # 'Lift', 'Generator', 'LT Panel', 'Earthing', 'Service', 'Other'
    category: str  # 'Passenger Lift', 'Silent Generator', etc.
    category_id: Optional[int] = None
    product: str  # 'LIFT001' or product name / ID
    product_id: Optional[int] = None
    product_name: Optional[str] = None
    brand: Optional[str] = None
    model_number: Optional[str] = None
    description: Optional[str] = None
    product_image: Optional[str] = None
    specifications: Optional[Dict[str, Any]] = None
    quantity: float = 1.0
    unit_price: float = 0.0
    total_price: Optional[float] = None

    model_config = {"extra": "allow"}

    @field_validator("category_id", "product_id", mode="before")
    @classmethod
    def parse_optional_id(cls, v: Any) -> Optional[int]:
        if v is None or v == "" or v == "null":
            return None
        try:
            return int(v)
        except Exception:
            return None

    @field_validator("quantity", mode="before")
    @classmethod
    def parse_qty(cls, v: Any) -> float:
        if v is None or v == "":
            return 1.0
        try:
            return float(v)
        except Exception:
            return 1.0

    @field_validator("unit_price", mode="before")
    @classmethod
    def parse_price(cls, v: Any) -> float:
        if v is None or v == "":
            return 0.0
        try:
            return float(v)
        except Exception:
            return 0.0

    @field_validator("specifications", mode="before")
    @classmethod
    def parse_specs(cls, v: Any) -> Optional[Dict[str, Any]]:
        if isinstance(v, str):
            v_clean = v.strip()
            if v_clean.startswith("{"):
                try:
                    return json.loads(v_clean)
                except Exception:
                    return {}
        return v

    @model_validator(mode="after")
    def calculate_item_total(self):
        if self.total_price is None or self.total_price == 0:
            self.total_price = round(self.quantity * self.unit_price, 2)
        return self


class QuotationCreateRequest(BaseModel):
    quotation_no: Optional[str] = None
    quotation_date: str
    valid_till: str
    reference: Optional[str] = None

    # Customer Details (Input fields as requested by user)
    customer_name: str
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None

    # Line Items
    items: List[QuotationItemSchema]

    # Pricing calculations
    subtotal: Optional[float] = None
    discount_type: str = "Flat"  # 'Flat' or '%'
    discount_value: Optional[float] = 0.0
    discount_amount: Optional[float] = None
    tax_type: str = "GST 18%"  # 'GST 5%', 'GST 12%', 'GST 18%'
    tax_rate: Optional[float] = None
    taxable_amount: Optional[float] = None
    tax_amount: Optional[float] = None
    grand_total: Optional[float] = None

    # Terms & Status
    terms: Optional[str] = None
    status: str = "Draft"  # 'Draft' or 'Sent'

    @field_validator("customer_name")
    @classmethod
    def validate_customer_name(cls, v: str) -> str:
        name = v.strip()
        if len(name) < 2:
            raise ValueError("Customer name must be at least 2 characters long")
        return name

    @field_validator("items", mode="before")
    @classmethod
    def parse_items(cls, v: Any) -> Any:
        if isinstance(v, str):
            v_clean = v.strip()
            if v_clean.startswith("[") or v_clean.startswith("{"):
                try:
                    parsed = json.loads(v_clean)
                    return parsed if isinstance(parsed, list) else [parsed]
                except Exception as err:
                    raise ValueError(f"Invalid JSON string in items: {err}")
        return v

    @field_validator(
        "discount_value",
        "subtotal",
        "discount_amount",
        "tax_rate",
        "taxable_amount",
        "tax_amount",
        "grand_total",
        mode="before",
    )
    @classmethod
    def parse_optional_num(cls, v: Any) -> Optional[float]:
        if v is None or v == "" or (isinstance(v, str) and v.strip() == ""):
            return None
        try:
            return float(v)
        except Exception:
            return None


class QuotationResponse(BaseModel):
    id: int
    quotation_no: str
    quotation_date: str
    valid_till: str
    reference: Optional[str] = None
    customer_name: str
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    items: List[Dict[str, Any]]
    subtotal: float
    discount_type: str
    discount_value: float
    discount_amount: float
    tax_type: str
    tax_rate: float
    taxable_amount: float
    tax_amount: float
    grand_total: float
    terms: Optional[str] = None
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class QuotationListResponse(BaseModel):
    count: int
    results: List[QuotationResponse]


# ==============================================================================
# PAYMENT SCHEMAS
# ==============================================================================

class PaymentCreateRequest(BaseModel):
    customer_name: str
    customer_phone: Optional[str] = None
    customer_email: Optional[str] = None
    customer_address: Optional[str] = None

    quotation_id: Optional[int] = None
    quotation_no: Optional[str] = None
    invoice_no: Optional[str] = None  # Auto-generated if empty

    payment_date: Optional[str] = None  # e.g., "17 Aug 2026"
    amount_received: float
    payment_mode: str = "Cash"  # "Cash", "Online", "Cheque", "UPI", "Net Banking", etc.
    transaction_no: Optional[str] = None
    reference_no: Optional[str] = None
    notes: Optional[str] = None
    payment_proof: Optional[str] = None
    status: str = "Received"  # "Received", "Pending", "Failed"

    model_config = {"extra": "allow"}

    @field_validator("customer_name")
    @classmethod
    def validate_customer(cls, v: str) -> str:
        s = v.strip()
        if not s:
            raise ValueError("Customer name is required")
        return s

    @field_validator("amount_received")
    @classmethod
    def validate_amount(cls, v: float) -> float:
        if v < 0:
            raise ValueError("Amount received cannot be negative")
        return float(v)


class PaymentUpdateRequest(BaseModel):
    customer_name: Optional[str] = None
    customer_phone: Optional[str] = None
    customer_email: Optional[str] = None
    customer_address: Optional[str] = None
    invoice_no: Optional[str] = None
    quotation_id: Optional[int] = None
    quotation_no: Optional[str] = None
    payment_date: Optional[str] = None
    amount_received: Optional[float] = None
    payment_mode: Optional[str] = None
    transaction_no: Optional[str] = None
    reference_no: Optional[str] = None
    notes: Optional[str] = None
    payment_proof: Optional[str] = None
    status: Optional[str] = None

    model_config = {"extra": "allow"}


class PaymentResponse(BaseModel):
    id: int
    invoice_no: str
    customer_name: str
    customer_phone: Optional[str] = None
    customer_email: Optional[str] = None
    customer_address: Optional[str] = None
    quotation_id: Optional[int] = None
    quotation_no: Optional[str] = None
    payment_date: str
    amount_received: float
    payment_mode: str
    transaction_no: Optional[str] = None
    reference_no: Optional[str] = None
    notes: Optional[str] = None
    payment_proof: Optional[str] = None
    status: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class OrderCustomerSchema(BaseModel):
    name: Optional[str] = None
    mobile: Optional[str] = None
    email: Optional[str] = None
    billing_address: Optional[str] = None
    delivery_address: Optional[str] = None

    model_config = {"extra": "allow"}


class OrderCreateRequest(BaseModel):
    order_no: Optional[str] = None
    quotation_id: Optional[Any] = None
    quotation_no: Optional[str] = None
    order_date: Optional[str] = None
    delivery_date: Optional[str] = None
    order_status: Optional[str] = "Pending"

    # Nested or flat customer
    customer: Optional[Union[OrderCustomerSchema, Dict[str, Any]]] = None
    customer_name: Optional[str] = None
    mobile: Optional[str] = None
    email: Optional[str] = None
    billing_address: Optional[str] = None
    delivery_address: Optional[str] = None

    # Line items
    items: Optional[List[Any]] = None

    # Amounts
    subtotal: Optional[float] = None
    discount: Optional[float] = None
    taxable_amount: Optional[float] = None
    tax: Optional[float] = None
    grand_total: Optional[float] = None
    advance_paid: Optional[float] = 0.0
    balance_amount: Optional[float] = None

    # Delivery instructions
    special_instructions: Optional[str] = None

    # Payment
    payment_status: Optional[str] = "Not Paid"
    payment_mode: Optional[str] = "Bank Transfer"
    transaction_no: Optional[str] = None
    payment_date: Optional[str] = None

    # Additional
    internal_notes: Optional[str] = None
    terms_accepted: Optional[bool] = True

    model_config = {"extra": "allow"}


class OrderUpdateRequest(BaseModel):
    order_no: Optional[str] = None
    order_date: Optional[str] = None
    delivery_date: Optional[str] = None
    order_status: Optional[str] = None
    customer_name: Optional[str] = None
    mobile: Optional[str] = None
    email: Optional[str] = None
    billing_address: Optional[str] = None
    delivery_address: Optional[str] = None
    items: Optional[List[Any]] = None
    subtotal: Optional[float] = None
    discount: Optional[float] = None
    taxable_amount: Optional[float] = None
    tax: Optional[float] = None
    grand_total: Optional[float] = None
    advance_paid: Optional[float] = None
    balance_amount: Optional[float] = None
    special_instructions: Optional[str] = None
    payment_status: Optional[str] = None
    payment_mode: Optional[str] = None
    transaction_no: Optional[str] = None
    payment_date: Optional[str] = None
    internal_notes: Optional[str] = None
    terms_accepted: Optional[bool] = None

    model_config = {"extra": "allow"}


class OrderResponse(BaseModel):
    id: int
    order_no: str
    order_date: str
    delivery_date: Optional[str] = None
    order_status: str
    quotation_id: Optional[int] = None
    quotation_no: Optional[str] = None
    customer_name: str
    mobile: Optional[str] = None
    email: Optional[str] = None
    billing_address: Optional[str] = None
    delivery_address: Optional[str] = None
    customer: Optional[Dict[str, Any]] = None
    items: List[Any] = []
    subtotal: float = 0.0
    discount: float = 0.0
    taxable_amount: float = 0.0
    tax: float = 0.0
    grand_total: float = 0.0
    advance_paid: float = 0.0
    balance_amount: float = 0.0
    special_instructions: Optional[str] = None
    payment_status: str = "Not Paid"
    payment_mode: str = "Bank Transfer"
    transaction_no: Optional[str] = None
    payment_date: Optional[str] = None
    internal_notes: Optional[str] = None
    terms_accepted: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


# ==============================================================================
# CASH BILL SCHEMAS (GenerateCashBillScreen)
# ==============================================================================

class CashBillCalculateRequest(BaseModel):
    items: List[Dict[str, Any]] = []
    discount: Optional[float] = 0.0
    amount_paid: Optional[float] = 0.0

    model_config = {"extra": "allow"}


class CashBillCalculateResponse(BaseModel):
    subtotal: float
    discount: float
    taxable_amount: float
    gst_rate: float
    gst: float
    grand_total: float
    amount_paid: float
    change_returned: float
    balance_amount: float
    payment_status: str


class CashBillCreateRequest(BaseModel):
    bill_no: Optional[str] = None
    bill_date: Optional[str] = None
    customer_type: Optional[str] = "Walk-in Customer"
    customer_name: str
    mobile: Optional[str] = None

    items: List[Dict[str, Any]] = []

    # Amounts can be passed or backend auto-calculates
    subtotal: Optional[float] = None
    discount: Optional[float] = 0.0
    taxable_amount: Optional[float] = None
    gst_rate: Optional[float] = 0.18
    gst_amount: Optional[float] = None
    grand_total: Optional[float] = None

    # Payment
    payment_mode: Optional[str] = "Cash"
    amount_paid: Optional[float] = 0.0
    change_returned: Optional[float] = None
    balance_amount: Optional[float] = None
    payment_status: Optional[str] = None

    # Additional
    notes: Optional[str] = None
    status: Optional[str] = "Generated"

    model_config = {"extra": "allow"}


class CashBillUpdateRequest(BaseModel):
    customer_type: Optional[str] = None
    customer_name: Optional[str] = None
    mobile: Optional[str] = None
    items: Optional[List[Dict[str, Any]]] = None
    discount: Optional[float] = None
    payment_mode: Optional[str] = None
    amount_paid: Optional[float] = None
    notes: Optional[str] = None
    status: Optional[str] = None

    model_config = {"extra": "allow"}


class CashBillResponse(BaseModel):
    id: int
    bill_no: str
    bill_date: str
    customer_type: str
    customer_name: str
    mobile: Optional[str] = None
    items: List[Dict[str, Any]] = []
    subtotal: float
    discount: float
    taxable_amount: float
    gst_rate: float
    gst_amount: float
    grand_total: float
    payment_mode: str
    amount_paid: float
    change_returned: float
    balance_amount: float
    payment_status: str
    notes: Optional[str] = None
    status: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


# ==============================================================================
# PURCHASE ORDER & SUPPLIER SCHEMAS (AddPurchaseOrderScreen)
# ==============================================================================

class SupplierCreateRequest(BaseModel):
    supplier_code: Optional[str] = None
    name: str
    contact_person: Optional[str] = None
    mobile: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    gstin: Optional[str] = None

    model_config = {"extra": "allow"}


class SupplierResponse(BaseModel):
    id: Union[int, str]
    supplier_id: int
    supplier_code: str
    name: str
    contact: Optional[str] = None
    contact_person: Optional[str] = None
    mobile: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    gstin: Optional[str] = None

    model_config = {"from_attributes": True, "extra": "allow"}


class PurchaseCalculateRequest(BaseModel):
    items: List[Dict[str, Any]] = []

    model_config = {"extra": "allow"}


class PurchaseCalculateResponse(BaseModel):
    subtotal: float
    gst_total: float
    grand_total: float


class PurchaseOrderCreateRequest(BaseModel):
    po_number: Optional[str] = None
    supplier_id: Optional[Any] = None
    supplier_name: Optional[str] = None
    contact_person: Optional[str] = None
    mobile: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None

    po_date: Optional[str] = None
    expected_delivery: Optional[str] = None
    payment_terms: Optional[str] = "30 Days"
    status: Optional[str] = "Draft"
    po_status: Optional[str] = None
    reference: Optional[str] = None

    items: List[Dict[str, Any]] = []

    subtotal: Optional[float] = None
    gst_total: Optional[float] = None
    grand_total: Optional[float] = None

    notes: Optional[str] = None

    model_config = {"extra": "allow"}


class PurchaseOrderUpdateRequest(BaseModel):
    po_date: Optional[str] = None
    expected_delivery: Optional[str] = None
    payment_terms: Optional[str] = None
    status: Optional[str] = None
    po_status: Optional[str] = None
    reference: Optional[str] = None
    supplier_name: Optional[str] = None
    contact_person: Optional[str] = None
    mobile: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    items: Optional[List[Dict[str, Any]]] = None
    notes: Optional[str] = None

    model_config = {"extra": "allow"}


class PurchaseOrderResponse(BaseModel):
    id: int
    po_number: str
    po_date: str
    expected_delivery: Optional[str] = None
    po_status: str
    payment_terms: str
    reference: Optional[str] = None
    supplier_id: Optional[int] = None
    supplier_code: Optional[str] = None
    supplier_name: str
    contact_person: Optional[str] = None
    mobile: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    items: List[Dict[str, Any]] = []
    subtotal: float
    gst_total: float
    grand_total: float
    notes: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


# ==============================================================================
# STOCK IN & CATEGORY INVENTORY SCHEMAS (StockInScreen)
# ==============================================================================

class CategoryStockItem(BaseModel):
    category_name: str
    product_count: int
    total_stock: float
    total_valuation: float
    unit: str = "Nos"
    products: List[Dict[str, Any]] = []


class CategoryTypeStockSummary(BaseModel):
    category_type: str
    total_stock: float
    total_products: int
    total_valuation: float
    categories: List[CategoryStockItem] = []


class CategoryStockResponse(BaseModel):
    category_types: List[str]
    stocks_by_category_type: Dict[str, CategoryTypeStockSummary]
    overall_total_stock: float
    overall_total_valuation: float


class StockInCalculateRequest(BaseModel):
    quantity: float = 1.0
    rate: float = 0.0
    discount: float = 0.0
    gst: float = 18.0

    model_config = {"extra": "allow"}


class StockInCalculateResponse(BaseModel):
    quantity: float
    rate: float
    discount: float
    gross_amount: float
    taxable_amount: float
    gst_rate: float
    gst_amount: float
    total_amount: float


class StockInCreateRequest(BaseModel):
    receipt_no: Optional[str] = None
    receipt_date: Optional[str] = None
    po_number: Optional[str] = None
    invoice_no: str
    invoice_date: Optional[str] = None

    supplier_id: Optional[Any] = None
    supplier_code: Optional[str] = None
    supplier_name: Optional[str] = None
    supplier_contact: Optional[str] = None

    product_id: Optional[int] = None
    product_sku: Optional[str] = None
    product_type: str
    category: str
    product: Optional[str] = None
    product_name: Optional[str] = None

    quantity: float = 1.0
    unit: Optional[str] = "Nos"
    warehouse: Optional[str] = "Main Warehouse"
    rack: Optional[str] = None
    batch_no: Optional[str] = None
    serial_no: Optional[str] = None

    rate: float = 0.0
    discount: Optional[float] = 0.0
    gst: Optional[float] = 18.0
    taxable_amount: Optional[float] = None
    gst_amount: Optional[float] = None
    total_amount: Optional[float] = None

    received_by: str
    condition: Optional[str] = "Good"
    inspection_status: Optional[str] = "Pending"
    inspection_remarks: Optional[str] = None
    notes: Optional[str] = None
    status: Optional[str] = "Received"
    specifications: Optional[Dict[str, Any]] = None

    model_config = {"extra": "allow"}


class StockInUpdateRequest(BaseModel):
    receipt_date: Optional[str] = None
    po_number: Optional[str] = None
    invoice_no: Optional[str] = None
    invoice_date: Optional[str] = None

    supplier_id: Optional[Any] = None
    supplier_code: Optional[str] = None
    supplier_name: Optional[str] = None
    supplier_contact: Optional[str] = None

    product_sku: Optional[str] = None
    product_type: Optional[str] = None
    category: Optional[str] = None
    product_name: Optional[str] = None

    quantity: Optional[float] = None
    unit: Optional[str] = None
    warehouse: Optional[str] = None
    rack: Optional[str] = None
    batch_no: Optional[str] = None
    serial_no: Optional[str] = None

    rate: Optional[float] = None
    discount: Optional[float] = None
    gst: Optional[float] = None

    received_by: Optional[str] = None
    condition: Optional[str] = None
    inspection_status: Optional[str] = None
    inspection_remarks: Optional[str] = None
    notes: Optional[str] = None
    status: Optional[str] = None
    specifications: Optional[Dict[str, Any]] = None

    model_config = {"extra": "allow"}


class StockInResponse(BaseModel):
    id: int
    receipt_no: str
    receipt_date: str
    po_number: Optional[str] = None
    invoice_no: str
    invoice_date: str

    supplier_id: Optional[int] = None
    supplier_code: Optional[str] = None
    supplier_name: str
    supplier_contact: Optional[str] = None

    product_id: Optional[int] = None
    product_sku: Optional[str] = None
    product_type: str
    category: str
    product_name: str
    product: str
    specifications: Dict[str, Any] = {}

    quantity: float
    unit: str
    warehouse: str
    rack: Optional[str] = None
    batch_no: Optional[str] = None
    serial_no: Optional[str] = None

    rate: float
    discount: float
    gst: float
    gross_amount: float
    taxable_amount: float
    gst_amount: float
    total_amount: float

    received_by: str
    condition: str
    inspection_status: str
    inspection_remarks: Optional[str] = None
    notes: Optional[str] = None
    status: str

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True, "extra": "allow"}


class StockInMetaResponse(BaseModel):
    warehouses: List[str]
    units: List[str]
    conditions: List[str]
    inspection_statuses: List[str]
    gst_rates: List[int]


# ── Invoice Schemas ──────────────────────────────────────────────────────────

class InvoiceItemSchema(BaseModel):
    id: Optional[str] = None
    name: str
    code: Optional[str] = None
    category: Optional[str] = None
    qty: Union[int, float] = 1
    rate: float = 0.0
    discount: float = 0.0
    tax_percent: float = 18.0
    tax: Optional[float] = None
    total: float = 0.0
    specifications: Optional[Dict[str, Any]] = None

    model_config = {"extra": "allow"}


class InvoiceCustomerSchema(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    mobile: Optional[str] = None
    email: Optional[str] = None
    billing_address: Optional[str] = None
    address: Optional[str] = None

    model_config = {"extra": "allow"}


class InvoiceCreateRequest(BaseModel):
    invoice_no: Optional[str] = None
    invoice_date: Optional[str] = None
    due_date: Optional[str] = None

    order_id: Optional[Any] = None
    order_no: Optional[str] = None
    quotation_id: Optional[Any] = None
    quotation_no: Optional[str] = None

    # Nested or flat customer fields
    customer: Optional[Union[InvoiceCustomerSchema, Dict[str, Any]]] = None
    customer_name: Optional[str] = None
    phone: Optional[str] = None
    mobile: Optional[str] = None
    email: Optional[str] = None
    billing_address: Optional[str] = None
    address: Optional[str] = None
    delivery_address: Optional[str] = None

    payment_terms: Optional[str] = "30 Days"
    reference_no: Optional[str] = None

    items: Optional[List[Any]] = None

    subtotal: Optional[float] = None
    discount: Optional[float] = None
    tax_percent: Optional[float] = 18.0
    tax: Optional[float] = None
    grand_total: Optional[float] = None
    amount_paid: Optional[float] = 0.0
    balance_due: Optional[float] = None

    notes: Optional[str] = None
    status: Optional[str] = "Unpaid"

    model_config = {"extra": "allow"}


class InvoiceUpdateRequest(BaseModel):
    invoice_no: Optional[str] = None
    invoice_date: Optional[str] = None
    due_date: Optional[str] = None
    order_id: Optional[Any] = None
    order_no: Optional[str] = None
    quotation_id: Optional[Any] = None
    quotation_no: Optional[str] = None
    customer_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    billing_address: Optional[str] = None
    delivery_address: Optional[str] = None
    payment_terms: Optional[str] = None
    reference_no: Optional[str] = None
    items: Optional[List[Any]] = None
    subtotal: Optional[float] = None
    discount: Optional[float] = None
    tax_percent: Optional[float] = None
    tax: Optional[float] = None
    grand_total: Optional[float] = None
    amount_paid: Optional[float] = None
    balance_due: Optional[float] = None
    notes: Optional[str] = None
    status: Optional[str] = None

    model_config = {"extra": "allow"}


class InvoiceStatusUpdateRequest(BaseModel):
    status: str

    model_config = {"extra": "allow"}


class InvoiceResponse(BaseModel):
    id: int
    invoice_no: str
    invoice_date: str
    due_date: Optional[str] = None
    order_id: Optional[int] = None
    order_no: Optional[str] = None
    quotation_id: Optional[int] = None
    quotation_no: Optional[str] = None
    customer_name: str
    phone: Optional[str] = None
    email: Optional[str] = None
    billing_address: Optional[str] = None
    delivery_address: Optional[str] = None
    customer: Optional[Dict[str, Any]] = None
    payment_terms: str
    reference_no: Optional[str] = None
    items: List[Any] = []
    subtotal: float
    discount: float
    tax_percent: float
    tax: float
    grand_total: float
    amount_paid: float
    balance_due: float
    notes: Optional[str] = None
    status: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    model_config = {"from_attributes": True, "extra": "allow"}







