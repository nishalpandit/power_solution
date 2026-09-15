# Power Solution API Documentation

This document lists all APIs with their exact URLs, HTTP methods, every single parameter (both required and optional) sorted in the exact ascending order of the Flutter form fields from top to bottom, including all dropdown choices and sample responses.

---

## 1. Category APIs

### 1.1 Create Category
url : (http://192.168.1.59:8000/api/categories)
method : POST

params :- 

category_name:test
category_code:0001
category_type:earthing
description:hii this is test
display_order:1
status:active
image:upload (File: JPG, PNG)

response :- 

```json
{
  "message": "Category created successfully",
  "category": {
    "id": 1,
    "category_name": "test",
    "category_code": "0001",
    "category_type": "earthing",
    "category_image": "/uploads/categories/98c440a840a64f3bbac7bba198c82f4d.png",
    "description": "hii this is test",
    "display_order": 1,
    "status": "active"
  }
}
```

---

### 1.2 List Categories
url : (http://192.168.1.59:8000/api/categories)
method : GET

params :- 

(None)

response :- 

```json
{
  "count": 1,
  "results": [
    {
      "id": 1,
      "category_name": "test",
      "category_code": "0001",
      "category_type": "earthing",
      "category_image": "/uploads/categories/98c440a840a64f3bbac7bba198c82f4d.png",
      "description": "hii this is test",
      "display_order": 1,
      "status": "active"
    }
  ]
}
```

---

### 1.3 Get Product Details by Category Type ID, Category Name ID, and Product ID
url : (http://192.168.1.59:8000/api/quotation/add_product)
method : GET (or POST)

params :- 

category_type_id: 1
category_name_id: 4
product_id: 9

Predefined Category Types:
- 1 = Lift
- 2 = Generator
- 3 = Panel
- 4 = Earthing
- 5 = Service
- 6 = Other

response :-

```json
{
  "id": 9,
  "product_id": 9,
  "category_type_id": 1,
  "category_type": "lift",
  "category_name_id": 4,
  "category_id": 4,
  "category_name": "Passenger Lift",
  "product_name": "khfk",
  "product_code": "mhmf",
  "brand": "gkhc",
  "model_number": "8987987654",
  "description": "chlclluuc",
  "purchase_price": 450000.0,
  "selling_price": 500000.0,
  "discount": "5%",
  "gst_rate": "18%",
  "hsn_code": "84281011",
  "inventory_tracking": true,
  "stock": 2.0,
  "unit": "Set",
  "min_stock": 1.0,
  "warranty_period": "2 Years",
  "warranty_terms": "Standard comprehensive warranty",
  "payment_terms": "30% Advance, 70% on delivery",
  "product_image": "/uploads/products/lift.jpg",
  "status": "Active",
  "specifications": {
    "lift_type": "Passenger",
    "operation_type": "Automatic",
    "capacity": "8 Passenger",
    "rated_load": "544 KG",
    "speed": "1.0 m/s",
    "floor_designation": "G+4",
    "number_of_floors": "5",
    "number_of_stops": "5",
    "landing_entrances": "5",
    "car_entrances": "1",
    "car_openings": "1",
    "shaft_structure": "Concrete",
    "shaft_net_size": "1800 x 1800 mm",
    "shaft_height": "18000 mm",
    "floor_height": "3000 mm",
    "pit_depth": "1500 mm",
    "overhead_height": "4200 mm",
    "car_dimensions": "1100 x 1400 mm",
    "cabin_size": "1100 x 1400 x 2200 mm",
    "machine_type": "Gearless PMSM",
    "machine_model": "GL-800",
    "drive_system": "VVVF",
    "motor_brand": "Monarch",
    "controller_brand": "Monarch Nice 3000+",
    "control_panel_type": "Integrated Microprocessor",
    "power_supply": "415 V AC, 3 Phase",
    "voltage": "415 V",
    "phase": "3 Phase",
    "frequency": "50 Hz",
    "brake_type": "Electromagnetic Disc Brake",
    "car_finishing": "Hairline SS",
    "cabin_finish": "Titanium Gold / SS Mirror",
    "false_ceiling": "LED Downlight Panel",
    "flooring_type": "Granite Finish PVC",
    "car_door_type": "Center Opening",
    "car_door_finish": "Hairline Stainless Steel",
    "landing_door_finish": "SS Hairline on Ground Floor",
    "door_opening": "800 x 2000 mm",
    "door_sill": "Hard Extruded Aluminium",
    "landing_door_lock": "Electromechanical Interlock",
    "safety_features": [
      "Over Speed Protection",
      "Infra-Red Light Curtain",
      "Automatic Rescue Device (ARD)"
    ]
  },
  "created_at": "2026-09-10T06:27:51.798573",
  "updated_at": "2026-09-10T06:27:51.798585"
}
```

---

## 2. Category 1: Lift Product Submission API

url : (http://192.168.1.59:8000/api/products/lift)
method : POST

params :- 

category_type:Lift
category_name:Passenger Lift
category_id:1
product_name:Passenger Traction Lift 8P
product_code:LIFT-TR-001
brand:Schindler / Custom
model_number:TR-800
description:High speed traction lift for commercial buildings
lift_type:Passenger
operation_type:Automatic
capacity:8 Passenger
rated_load:544 KG
speed:1.0 m/s
floor_designation:G+4
number_of_floors:5
number_of_stops:5
landing_entrances:5
car_entrances:1
car_openings:1
shaft_structure:Concrete
shaft_net_size:1800 x 1800 mm
shaft_height:18000 mm
floor_height:3000 mm
pit_depth:1500 mm
overhead_height:4200 mm
car_dimensions:1100 x 1400 mm
cabin_size:1100 x 1400 x 2200 mm
machine_type:Gearless PMSM
machine_model:GL-800
drive_system:VVVF
motor_brand:Monarch
controller_brand:Monarch Nice 3000+
control_panel_type:Integrated Microprocessor
power_supply:415 V AC, 3 Phase
voltage:415 V
phase:3 Phase
frequency:50 Hz
brake_type:Electromagnetic Disc Brake
car_finishing:Hairline SS
cabin_finish:Titanium Gold / SS Mirror
false_ceiling:LED Downlight Panel
flooring_type:Granite Finish PVC
car_door_type:Center Opening
car_door_finish:Hairline Stainless Steel
landing_door_finish:SS Hairline on Ground Floor
door_opening:800 x 2000 mm
door_sill:Hard Extruded Aluminium
landing_door_lock:Electromechanical Interlock
safety_features:Over Speed Protection,Infra-Red Light Curtain,Fire Alarm System,Emergency Stop Button,Battery Operated Emergency Light,Battery Operated Emergency Alarm,Battery Operated Emergency Blower,Automatic Rescue Device (ARD),Single Phasing Preventer,Overload Safety Device,Limit Switches,Motor Thermal Overload Protection,Car Gate Switches,Safe Voltage Protection,Locked Rotor Protection,Door Lock Protection
purchase_price:1200000.00
selling_price:1500000.00
discount:5%
gst_rate:18%
hsn_code:84281011
inventory_tracking:true
stock:2
unit:Set
min_stock:1
warranty_period:2 Years
warranty_terms:Comprehensive warranty including all mechanical parts
payment_terms:30% advance, 60% on delivery, 10% on handover
image:upload (File: JPG, PNG up to 2MB)
status:Active

response :- 

```json
{
  "message": "Lift product created successfully",
  "product": {
    "id": 1,
    "category_type": "lift",
    "category_id": 1,
    "category_name": "Passenger Lift",
    "product_name": "Passenger Traction Lift 8P",
    "product_code": "LIFT-TR-001",
    "brand": "Schindler / Custom",
    "model_number": "TR-800",
    "description": "High speed traction lift for commercial buildings",
    "purchase_price": 1200000.0,
    "selling_price": 1500000.0,
    "discount": "5%",
    "gst_rate": "18%",
    "hsn_code": "84281011",
    "inventory_tracking": true,
    "stock": 2.0,
    "unit": "Set",
    "min_stock": 1.0,
    "warranty_period": "2 Years",
    "warranty_terms": "Comprehensive warranty including all mechanical parts",
    "payment_terms": "30% advance, 60% on delivery, 10% on handover",
    "product_image": "/uploads/products/39ec6f35383d4e99b205a2590b42a3e8.jpg",
    "status": "Active",
    "specifications": {
      "lift_type": "Passenger",
      "operation_type": "Automatic",
      "capacity": "8 Passenger",
      "rated_load": "544 KG",
      "speed": "1.0 m/s",
      "floor_designation": "G+4",
      "number_of_floors": "5",
      "number_of_stops": "5",
      "landing_entrances": "5",
      "car_entrances": "1",
      "car_openings": "1",
      "shaft_structure": "Concrete",
      "shaft_net_size": "1800 x 1800 mm",
      "shaft_height": "18000 mm",
      "floor_height": "3000 mm",
      "pit_depth": "1500 mm",
      "overhead_height": "4200 mm",
      "car_dimensions": "1100 x 1400 mm",
      "cabin_size": "1100 x 1400 x 2200 mm",
      "machine_type": "Gearless PMSM",
      "machine_model": "GL-800",
      "drive_system": "VVVF",
      "motor_brand": "Monarch",
      "controller_brand": "Monarch Nice 3000+",
      "control_panel_type": "Integrated Microprocessor",
      "power_supply": "415 V AC, 3 Phase",
      "voltage": "415 V",
      "phase": "3 Phase",
      "frequency": "50 Hz",
      "brake_type": "Electromagnetic Disc Brake",
      "car_finishing": "Hairline SS",
      "cabin_finish": "Titanium Gold / SS Mirror",
      "false_ceiling": "LED Downlight Panel",
      "flooring_type": "Granite Finish PVC",
      "car_door_type": "Center Opening",
      "car_door_finish": "Hairline Stainless Steel",
      "landing_door_finish": "SS Hairline on Ground Floor",
      "door_opening": "800 x 2000 mm",
      "door_sill": "Hard Extruded Aluminium",
      "landing_door_lock": "Electromechanical Interlock",
      "safety_features": [
        "Over Speed Protection",
        "Infra-Red Light Curtain",
        "Fire Alarm System",
        "Emergency Stop Button",
        "Battery Operated Emergency Light",
        "Battery Operated Emergency Alarm",
        "Battery Operated Emergency Blower",
        "Automatic Rescue Device (ARD)",
        "Single Phasing Preventer",
        "Overload Safety Device",
        "Limit Switches",
        "Motor Thermal Overload Protection",
        "Car Gate Switches",
        "Safe Voltage Protection",
        "Locked Rotor Protection",
        "Door Lock Protection"
      ]
    },
    "created_at": "2026-09-10T10:33:05.123456",
    "updated_at": "2026-09-10T10:33:05.123456"
  }
}
```

---

## 3. Category 2: Generator (DG) Product Submission API

url : (http://192.168.1.59:8000/api/products/generator)
method : POST

params :- 

category_type:Generator
category_name:Silent DG
category_id:2
product_name:62.5 KVA Silent Diesel Generator
product_code:DG-62K-001
brand:Cummins / Kirloskar
model_number:CP62D5
description:Water-cooled silent diesel generator set with AMF panel
dg_rating:62.5 KVA
rated_power_kw:50 KW
output_voltage:415 V
phase:3 Phase
starting_voltage:12 V
fuel_tank_capacity:150 LTRS
engine_brand:Cummins
engine_model:4BTA3.9-G2
bhp:78 BHP
rated_speed:1500 RPM
rated_power:50 KW
number_of_cylinders:4
governor_type:Mechanical / CRDI
aspiration_type:Turbocharged
cooling_mode:Liquid Cooled
alternator_brand:Stamford
alternator_model:UCI224E
alternator_capacity:62.5 KVA
rated_current:87 Ampere
exciting_mode:Brushless Self Excited
insulation_class:Class H
protection_class:IP23
voltage_control:AVR
control_panel_type:Digital Control Panel with AMF
amf_panel:Yes
battery_charger:SMPS Auto Battery Charger
acoustic_enclosure:Yes
radiator_cooling:Heavy Duty 50 Deg C Radiator
purchase_price:450000.00
selling_price:520000.00
discount:0%
gst_rate:18%
hsn_code:85021100
inventory_tracking:true
stock:3
unit:Set
min_stock:1
warranty_period:2 Years / 5000 Hours
warranty_terms:Standard manufacturer warranty on engine and alternator
payment_terms:50% Advance, 50% against delivery
image:upload (File: JPG, PNG up to 2MB)
status:Active

response :- 

```json
{
  "message": "Generator product created successfully",
  "product": {
    "id": 2,
    "category_type": "generator",
    "category_id": 2,
    "category_name": "Silent DG",
    "product_name": "62.5 KVA Silent Diesel Generator",
    "product_code": "DG-62K-001",
    "brand": "Cummins / Kirloskar",
    "model_number": "CP62D5",
    "description": "Water-cooled silent diesel generator set with AMF panel",
    "purchase_price": 450000.0,
    "selling_price": 520000.0,
    "discount": "0%",
    "gst_rate": "18%",
    "hsn_code": "85021100",
    "inventory_tracking": true,
    "stock": 3.0,
    "unit": "Set",
    "min_stock": 1.0,
    "warranty_period": "2 Years / 5000 Hours",
    "warranty_terms": "Standard manufacturer warranty on engine and alternator",
    "payment_terms": "50% Advance, 50% against delivery",
    "product_image": null,
    "status": "Active",
    "specifications": {
      "dg_rating": "62.5 KVA",
      "rated_power_kw": "50 KW",
      "output_voltage": "415 V",
      "phase": "3 Phase",
      "starting_voltage": "12 V",
      "fuel_tank_capacity": "150 LTRS",
      "engine_brand": "Cummins",
      "engine_model": "4BTA3.9-G2",
      "bhp": "78 BHP",
      "rated_speed": "1500 RPM",
      "rated_power": "50 KW",
      "number_of_cylinders": "4",
      "governor_type": "Mechanical / CRDI",
      "aspiration_type": "Turbocharged",
      "cooling_mode": "Liquid Cooled",
      "alternator_brand": "Stamford",
      "alternator_model": "UCI224E",
      "alternator_capacity": "62.5 KVA",
      "rated_current": "87 Ampere",
      "exciting_mode": "Brushless Self Excited",
      "insulation_class": "Class H",
      "protection_class": "IP23",
      "voltage_control": "AVR",
      "control_panel_type": "Digital Control Panel with AMF",
      "amf_panel": "Yes",
      "battery_charger": "SMPS Auto Battery Charger",
      "acoustic_enclosure": "Yes",
      "radiator_cooling": "Heavy Duty 50 Deg C Radiator"
    },
    "created_at": "2026-09-10T10:33:05.234567",
    "updated_at": "2026-09-10T10:33:05.234567"
  }
}
```

---

## 4. Category 3: Panel Product Submission API

url : (http://192.168.1.59:8000/api/products/panel)
method : POST

params :- 

category_type:Panel
category_name:LT Panel
category_id:3
product_name:400A Main LT Electrical Distribution Panel
product_code:PNL-LT-400
brand:PowerSolution Panels
model_number:LT-400A-01
description:Floor mounted compartmentalized LT distribution panel
panel_construction:CRCA Sheet Steel, Fully Compartmentalized
sheet_thickness:14/16 SWG (2.0/1.6 mm)
cable_alley:Dedicated Vertical Cable Alley with Doors
door_gasket:Neoprene Continuous Gasket
feeder_nomenclature:Screen Printed Acrylic Labels
metal_joint:Continuous CO2 / Arc Welding
panel_painting:7-Tank Process Powder Coated RAL 7035
danger_board:Enamelled Danger Caution Plate 415V
door_knob:Heavy Duty Quarter Turn Handle
door_locking:Keyed Cam Lock System
base_angle_frame:ISMC 75 x 40 x 5 mm Channel Base
busbar_material:EC Grade Aluminium with Heat Shrinkable PVC Sleeves
busbar_insulator:DMC/SMC Finger Type High Grade Support Insulators
phase_barrier:FRP/Polycarbonate Phase Barriers between Buses
earth_busbar:25 x 5 mm Copper/GI Earth Busbar along panel length
busbar_distance:Phase to Phase > 25 mm, Phase to Earth > 19 mm
input_cable_connection:Top/Bottom Entry with Brass Cable Glands
output_cable_connection:Bottom Cable Chamber with Terminal Blocks
gland_plate_thickness:3.0 mm Removable Aluminium/CRCA Plate
control_wiring:1.5 SQ MM 1100V Grade FRLS Flexible Copper Wire
cable_entry:Bottom Entry
power_supply:415 V ±10%, 50 Hz, 3 Phase 4 Wire
purchase_price:180000.00
selling_price:240000.00
discount:0%
gst_rate:18%
hsn_code:85371000
inventory_tracking:false
stock:0
unit:Set
min_stock:0
warranty_period:1 Year
warranty_terms:12 months warranty against manufacturing defects
payment_terms:40% Advance, 60% on dispatch
image:upload (File: JPG, PNG up to 2MB)
status:Active

response :- 

```json
{
  "message": "Panel product created successfully",
  "product": {
    "id": 3,
    "category_type": "panel",
    "category_id": 3,
    "category_name": "LT Panel",
    "product_name": "400A Main LT Electrical Distribution Panel",
    "product_code": "PNL-LT-400",
    "brand": "PowerSolution Panels",
    "model_number": "LT-400A-01",
    "description": "Floor mounted compartmentalized LT distribution panel",
    "purchase_price": 180000.0,
    "selling_price": 240000.0,
    "discount": "0%",
    "gst_rate": "18%",
    "hsn_code": "85371000",
    "inventory_tracking": false,
    "stock": 0.0,
    "unit": "Set",
    "min_stock": 0.0,
    "warranty_period": "1 Year",
    "warranty_terms": "12 months warranty against manufacturing defects",
    "payment_terms": "40% Advance, 60% on dispatch",
    "product_image": null,
    "status": "Active",
    "specifications": {
      "panel_construction": "CRCA Sheet Steel, Fully Compartmentalized",
      "sheet_thickness": "14/16 SWG (2.0/1.6 mm)",
      "cable_alley": "Dedicated Vertical Cable Alley with Doors",
      "door_gasket": "Neoprene Continuous Gasket",
      "feeder_nomenclature": "Screen Printed Acrylic Labels",
      "metal_joint": "Continuous CO2 / Arc Welding",
      "panel_painting": "7-Tank Process Powder Coated RAL 7035",
      "danger_board": "Enamelled Danger Caution Plate 415V",
      "door_knob": "Heavy Duty Quarter Turn Handle",
      "door_locking": "Keyed Cam Lock System",
      "base_angle_frame": "ISMC 75 x 40 x 5 mm Channel Base",
      "busbar_material": "EC Grade Aluminium with Heat Shrinkable PVC Sleeves",
      "busbar_insulator": "DMC/SMC Finger Type High Grade Support Insulators",
      "phase_barrier": "FRP/Polycarbonate Phase Barriers between Buses",
      "earth_busbar": "25 x 5 mm Copper/GI Earth Busbar along panel length",
      "busbar_distance": "Phase to Phase > 25 mm, Phase to Earth > 19 mm",
      "input_cable_connection": "Top/Bottom Entry with Brass Cable Glands",
      "output_cable_connection": "Bottom Cable Chamber with Terminal Blocks",
      "gland_plate_thickness": "3.0 mm Removable Aluminium/CRCA Plate",
      "control_wiring": "1.5 SQ MM 1100V Grade FRLS Flexible Copper Wire",
      "cable_entry": "Bottom Entry",
      "power_supply": "415 V ±10%, 50 Hz, 3 Phase 4 Wire"
    },
    "created_at": "2026-09-10T10:33:05.345678",
    "updated_at": "2026-09-10T10:33:05.345678"
  }
}
```

---

## 5. Category 4: Earthing Product Submission API

url : (http://192.168.1.59:8000/api/products/earthing)
method : POST

params :- 

category_type:Earthing
category_name:Earth Pit
category_id:4
product_name:Chemical Maintenance-Free Earth Electrode
product_code:EARTH-CU-3M
brand:PowerShield Earth
model_number:PE-50-3000
description:Pure copper bonded earth electrode with carbon ground enhancing compound
earthing_type:Copper Bonded Chemical Earth Pit
specification:3 Meter Length, 50mm Diameter, 250 Micron Copper Coating, tested as per IEEE 80 / IS 3043
purchase_price:3500.00
selling_price:5200.00
discount:10%
gst_rate:18%
hsn_code:85359090
inventory_tracking:true
stock:50
unit:Nos
min_stock:10
warranty_period:5 Years
warranty_terms:5 years replacement warranty against corrosion
payment_terms:100% Advance
image:upload (File: JPG, PNG up to 2MB)
status:Active

response :- 

```json
{
  "message": "Earthing product created successfully",
  "product": {
    "id": 4,
    "category_type": "earthing",
    "category_id": 4,
    "category_name": "Earth Pit",
    "product_name": "Chemical Maintenance-Free Earth Electrode",
    "product_code": "EARTH-CU-3M",
    "brand": "PowerShield Earth",
    "model_number": "PE-50-3000",
    "description": "Pure copper bonded earth electrode with carbon ground enhancing compound",
    "purchase_price": 3500.0,
    "selling_price": 5200.0,
    "discount": "10%",
    "gst_rate": "18%",
    "hsn_code": "85359090",
    "inventory_tracking": true,
    "stock": 50.0,
    "unit": "Nos",
    "min_stock": 10.0,
    "warranty_period": "5 Years",
    "warranty_terms": "5 years replacement warranty against corrosion",
    "payment_terms": "100% Advance",
    "product_image": null,
    "status": "Active",
    "specifications": {
      "earthing_type": "Copper Bonded Chemical Earth Pit",
      "specification": "3 Meter Length, 50mm Diameter, 250 Micron Copper Coating, tested as per IEEE 80 / IS 3043"
    },
    "created_at": "2026-09-10T10:33:05.456789",
    "updated_at": "2026-09-10T10:33:05.456789"
  }
}
```

---

## 6. Category 5: Service Product Submission API

url : (http://192.168.1.59:8000/api/products/service)
method : POST

params :- 

category_type:Service
category_name:AMC
category_id:5
product_name:Annual Maintenance Contract - Commercial Passenger Lift
product_code:SRV-AMC-LIFT-01
brand:PowerSolution Services
model_number:AMC-COMM-01
description:Comprehensive annual maintenance contract with 24x7 breakdown response
service_name:Comprehensive Elevator AMC
service_type:AMC
contract_type:Annual
contract_duration:12 Months
visit_frequency:Monthly
service_amount:36000.00
service_coverage:Full electrical, mechanical, door drives, lubrication, emergency response
service_description:Monthly routine checkup plus unlimited emergency breakdown calls within 2 hours
checklist:Inspection / Checking,Cleaning,Battery Check,Electrical Check,Safety Check,Load Test,Wiring Inspection,Lubrication,Repair / Replacement
purchase_price:20000.00
selling_price:36000.00
discount:0%
gst_rate:18%
hsn_code:998719
inventory_tracking:false
stock:0
unit:Year
min_stock:0
warranty_period:1 Year Service Agreement
warranty_terms:Service guarantee with 2 hours breakdown response time
payment_terms:Quarterly Advance
image:upload (File: JPG, PNG up to 2MB)
status:Active

response :- 

```json
{
  "message": "Service product created successfully",
  "product": {
    "id": 5,
    "category_type": "service",
    "category_id": 5,
    "category_name": "AMC",
    "product_name": "Annual Maintenance Contract - Commercial Passenger Lift",
    "product_code": "SRV-AMC-LIFT-01",
    "brand": "PowerSolution Services",
    "model_number": "AMC-COMM-01",
    "description": "Comprehensive annual maintenance contract with 24x7 breakdown response",
    "purchase_price": 20000.0,
    "selling_price": 36000.0,
    "discount": "0%",
    "gst_rate": "18%",
    "hsn_code": "998719",
    "inventory_tracking": false,
    "stock": 0.0,
    "unit": "Year",
    "min_stock": 0.0,
    "warranty_period": "1 Year Service Agreement",
    "warranty_terms": "Service guarantee with 2 hours breakdown response time",
    "payment_terms": "Quarterly Advance",
    "product_image": null,
    "status": "Active",
    "specifications": {
      "service_name": "Comprehensive Elevator AMC",
      "service_type": "AMC",
      "contract_type": "Annual",
      "contract_duration": "12 Months",
      "visit_frequency": "Monthly",
      "service_amount": 36000.0,
      "service_coverage": "Full electrical, mechanical, door drives, lubrication, emergency response",
      "service_description": "Monthly routine checkup plus unlimited emergency breakdown calls within 2 hours",
      "checklist": [
        "Inspection / Checking",
        "Cleaning",
        "Battery Check",
        "Electrical Check",
        "Safety Check",
        "Load Test",
        "Wiring Inspection",
        "Lubrication",
        "Repair / Replacement"
      ]
    },
    "created_at": "2026-09-10T10:33:05.567890",
    "updated_at": "2026-09-10T10:33:05.567890"
  }
}
```

---

## 7. Category 6: Other Product Submission API

url : (http://192.168.1.59:8000/api/products/other)
method : POST

params :- 

category_type:Other
category_name:Other Product
category_id:6
product_name:Automatic Transfer Switch (ATS) 250A
product_code:OTH-ATS-250
brand:Socomec / ABB
model_number:ATyS-dM
description:Motorised changeover switch for mains and generator synchronization
custom_specifications:{"pole_count": 4, "current_rating": "250A", "operation_time_ms": 180}
purchase_price:35000.00
selling_price:48000.00
discount:2000
gst_rate:18%
hsn_code:85365090
inventory_tracking:true
stock:5
unit:Nos
min_stock:1
warranty_period:2 Years
warranty_terms:Standard warranty
payment_terms:100% Advance
image:upload (File: JPG, PNG up to 2MB)
status:Active

response :- 

```json
{
  "message": "Other product created successfully",
  "product": {
    "id": 6,
    "category_type": "other",
    "category_id": 6,
    "category_name": "Other Product",
    "product_name": "Automatic Transfer Switch (ATS) 250A",
    "product_code": "OTH-ATS-250",
    "brand": "Socomec / ABB",
    "model_number": "ATyS-dM",
    "description": "Motorised changeover switch for mains and generator synchronization",
    "purchase_price": 35000.0,
    "selling_price": 48000.0,
    "discount": "2000",
    "gst_rate": "18%",
    "hsn_code": "85365090",
    "inventory_tracking": true,
    "stock": 5.0,
    "unit": "Nos",
    "min_stock": 1.0,
    "warranty_period": "2 Years",
    "warranty_terms": "Standard warranty",
    "payment_terms": "100% Advance",
    "product_image": null,
    "status": "Active",
    "specifications": {
      "custom_specifications": {
        "pole_count": 4,
        "current_rating": "250A",
        "operation_time_ms": 180
      }
    },
    "created_at": "2026-09-10T10:33:05.678901",
    "updated_at": "2026-09-10T10:33:05.678901"
  }
}
```

---

## 8. Category-Specific Listing APIs

### 8.1 List Lift Products
url : (http://192.168.1.59:8000/api/products/lift)
method : GET

params :- 

(None)

response :- 

```json
{
  "count": 1,
  "category_type": "lift",
  "results": [
    {
      "id": 1,
      "category_type": "lift",
      "category_id": 1,
      "category_name": "Passenger Lift",
      "product_name": "Passenger Traction Lift 8P",
      "product_code": "LIFT-TR-001",
      "brand": "Schindler / Custom",
      "model_number": "TR-800",
      "description": "High speed traction lift for commercial buildings",
      "purchase_price": 1200000.0,
      "selling_price": 1500000.0,
      "discount": "5%",
      "gst_rate": "18%",
      "hsn_code": "84281011",
      "inventory_tracking": true,
      "stock": 2.0,
      "unit": "Set",
      "min_stock": 1.0,
      "warranty_period": "2 Years",
      "warranty_terms": "Comprehensive warranty including all mechanical parts",
      "payment_terms": "30% advance, 60% on delivery, 10% on handover",
      "product_image": "/uploads/products/39ec6f35383d4e99b205a2590b42a3e8.jpg",
      "status": "Active",
      "specifications": {
        "lift_type": "Passenger",
        "operation_type": "Automatic",
        "capacity": "8 Passenger",
        "rated_load": "544 KG",
        "speed": "1.0 m/s",
        "floor_designation": "G+4",
        "number_of_floors": "5",
        "number_of_stops": "5",
        "landing_entrances": "5",
        "car_entrances": "1",
        "car_openings": "1",
        "shaft_structure": "Concrete",
        "shaft_net_size": "1800 x 1800 mm",
        "shaft_height": "18000 mm",
        "floor_height": "3000 mm",
        "pit_depth": "1500 mm",
        "overhead_height": "4200 mm",
        "car_dimensions": "1100 x 1400 mm",
        "cabin_size": "1100 x 1400 x 2200 mm",
        "machine_type": "Gearless PMSM",
        "machine_model": "GL-800",
        "drive_system": "VVVF",
        "motor_brand": "Monarch",
        "controller_brand": "Monarch Nice 3000+",
        "control_panel_type": "Integrated Microprocessor",
        "power_supply": "415 V AC, 3 Phase",
        "voltage": "415 V",
        "phase": "3 Phase",
        "frequency": "50 Hz",
        "brake_type": "Electromagnetic Disc Brake",
        "car_finishing": "Hairline SS",
        "cabin_finish": "Titanium Gold / SS Mirror",
        "false_ceiling": "LED Downlight Panel",
        "flooring_type": "Granite Finish PVC",
        "car_door_type": "Center Opening",
        "car_door_finish": "Hairline Stainless Steel",
        "landing_door_finish": "SS Hairline on Ground Floor",
        "door_opening": "800 x 2000 mm",
        "door_sill": "Hard Extruded Aluminium",
        "landing_door_lock": "Electromechanical Interlock",
        "safety_features": [
          "Over Speed Protection",
          "Infra-Red Light Curtain",
          "Automatic Rescue Device (ARD)",
          "Single Phasing Preventer",
          "Emergency Stop Button"
        ]
      },
      "created_at": "2026-09-10T10:33:05.123456",
      "updated_at": "2026-09-10T10:33:05.123456"
    }
  ]
}
```

---

### 8.2 List Generator Products
url : (http://192.168.1.59:8000/api/products/generator)
method : GET

params :- 

(None)

response :- 

```json
{
  "count": 1,
  "category_type": "generator",
  "results": [
    {
      "id": 2,
      "category_type": "generator",
      "category_id": 2,
      "category_name": "Silent DG",
      "product_name": "62.5 KVA Silent Diesel Generator",
      "product_code": "DG-62K-001",
      "brand": "Cummins / Kirloskar",
      "model_number": "CP62D5",
      "description": "Water-cooled silent diesel generator set with AMF panel",
      "purchase_price": 450000.0,
      "selling_price": 520000.0,
      "discount": "0%",
      "gst_rate": "18%",
      "hsn_code": "85021100",
      "inventory_tracking": true,
      "stock": 3.0,
      "unit": "Set",
      "min_stock": 1.0,
      "warranty_period": "2 Years / 5000 Hours",
      "warranty_terms": "Standard manufacturer warranty on engine and alternator",
      "payment_terms": "50% Advance, 50% against delivery",
      "product_image": null,
      "status": "Active",
      "specifications": {
        "dg_rating": "62.5 KVA",
        "rated_power_kw": "50 KW",
        "output_voltage": "415 V",
        "phase": "3 Phase",
        "starting_voltage": "12 V",
        "fuel_tank_capacity": "150 LTRS",
        "engine_brand": "Cummins",
        "engine_model": "4BTA3.9-G2",
        "bhp": "78 BHP",
        "rated_speed": "1500 RPM",
        "rated_power": "50 KW",
        "number_of_cylinders": "4",
        "governor_type": "Mechanical / CRDI",
        "aspiration_type": "Turbocharged",
        "cooling_mode": "Liquid Cooled",
        "alternator_brand": "Stamford",
        "alternator_model": "UCI224E",
        "alternator_capacity": "62.5 KVA",
        "rated_current": "87 Ampere",
        "exciting_mode": "Brushless Self Excited",
        "insulation_class": "Class H",
        "protection_class": "IP23",
        "voltage_control": "AVR",
        "control_panel_type": "Digital Control Panel with AMF",
        "amf_panel": "Yes",
        "battery_charger": "SMPS Auto Battery Charger",
        "acoustic_enclosure": "Yes",
        "radiator_cooling": "Heavy Duty 50 Deg C Radiator"
      },
      "created_at": "2026-09-10T10:33:05.234567",
      "updated_at": "2026-09-10T10:33:05.234567"
    }
  ]
}
```

---

### 8.3 List Panel Products
url : (http://192.168.1.59:8000/api/products/panel)
method : GET

params :- 

(None)

response :- 

```json
{
  "count": 1,
  "category_type": "panel",
  "results": [
    {
      "id": 3,
      "category_type": "panel",
      "category_id": 3,
      "category_name": "LT Panel",
      "product_name": "400A Main LT Electrical Distribution Panel",
      "product_code": "PNL-LT-400",
      "brand": "PowerSolution Panels",
      "model_number": "LT-400A-01",
      "description": "Floor mounted compartmentalized LT distribution panel",
      "purchase_price": 180000.0,
      "selling_price": 240000.0,
      "discount": "0%",
      "gst_rate": "18%",
      "hsn_code": "85371000",
      "inventory_tracking": false,
      "stock": 0.0,
      "unit": "Set",
      "min_stock": 0.0,
      "warranty_period": "1 Year",
      "warranty_terms": "12 months warranty against manufacturing defects",
      "payment_terms": "40% Advance, 60% on dispatch",
      "product_image": null,
      "status": "Active",
      "specifications": {
        "panel_construction": "CRCA Sheet Steel, Fully Compartmentalized",
        "sheet_thickness": "14/16 SWG (2.0/1.6 mm)",
        "cable_alley": "Dedicated Vertical Cable Alley with Doors",
        "door_gasket": "Neoprene Continuous Gasket",
        "feeder_nomenclature": "Screen Printed Acrylic Labels",
        "metal_joint": "Continuous CO2 / Arc Welding",
        "panel_painting": "7-Tank Process Powder Coated RAL 7035",
        "danger_board": "Enamelled Danger Caution Plate 415V",
        "door_knob": "Heavy Duty Quarter Turn Handle",
        "door_locking": "Keyed Cam Lock System",
        "base_angle_frame": "ISMC 75 x 40 x 5 mm Channel Base",
        "busbar_material": "EC Grade Aluminium with Heat Shrinkable PVC Sleeves",
        "busbar_insulator": "DMC/SMC Finger Type High Grade Support Insulators",
        "phase_barrier": "FRP/Polycarbonate Phase Barriers between Buses",
        "earth_busbar": "25 x 5 mm Copper/GI Earth Busbar along panel length",
        "busbar_distance": "Phase to Phase > 25 mm, Phase to Earth > 19 mm",
        "input_cable_connection": "Top/Bottom Entry with Brass Cable Glands",
        "output_cable_connection": "Bottom Cable Chamber with Terminal Blocks",
        "gland_plate_thickness": "3.0 mm Removable Aluminium/CRCA Plate",
        "control_wiring": "1.5 SQ MM 1100V Grade FRLS Flexible Copper Wire",
        "cable_entry": "Bottom Entry",
        "power_supply": "415 V ±10%, 50 Hz, 3 Phase 4 Wire"
      },
      "created_at": "2026-09-10T10:33:05.345678",
      "updated_at": "2026-09-10T10:33:05.345678"
    }
  ]
}
```

---

### 8.4 List Earthing Products
url : (http://192.168.1.59:8000/api/products/earthing)
method : GET

params :- 

(None)

response :- 

```json
{
  "count": 1,
  "category_type": "earthing",
  "results": [
    {
      "id": 4,
      "category_type": "earthing",
      "category_id": 4,
      "category_name": "Earth Pit",
      "product_name": "Chemical Maintenance-Free Earth Electrode",
      "product_code": "EARTH-CU-3M",
      "brand": "PowerShield Earth",
      "model_number": "PE-50-3000",
      "description": "Pure copper bonded earth electrode with carbon ground enhancing compound",
      "purchase_price": 3500.0,
      "selling_price": 5200.0,
      "discount": "10%",
      "gst_rate": "18%",
      "hsn_code": "85359090",
      "inventory_tracking": true,
      "stock": 50.0,
      "unit": "Nos",
      "min_stock": 10.0,
      "warranty_period": "5 Years",
      "warranty_terms": "5 years replacement warranty against corrosion",
      "payment_terms": "100% Advance",
      "product_image": null,
      "status": "Active",
      "specifications": {
        "earthing_type": "Copper Bonded Chemical Earth Pit",
        "specification": "3 Meter Length, 50mm Diameter, 250 Micron Copper Coating, tested as per IEEE 80 / IS 3043"
      },
      "created_at": "2026-09-10T10:33:05.456789",
      "updated_at": "2026-09-10T10:33:05.456789"
    }
  ]
}
```

---

### 8.5 List Service Products
url : (http://192.168.1.59:8000/api/products/service)
method : GET

params :- 

(None)

response :- 

```json
{
  "count": 1,
  "category_type": "service",
  "results": [
    {
      "id": 5,
      "category_type": "service",
      "category_id": 5,
      "category_name": "AMC",
      "product_name": "Annual Maintenance Contract - Commercial Passenger Lift",
      "product_code": "SRV-AMC-LIFT-01",
      "brand": "PowerSolution Services",
      "model_number": "AMC-COMM-01",
      "description": "Comprehensive annual maintenance contract with 24x7 breakdown response",
      "purchase_price": 20000.0,
      "selling_price": 36000.0,
      "discount": "0%",
      "gst_rate": "18%",
      "hsn_code": "998719",
      "inventory_tracking": false,
      "stock": 0.0,
      "unit": "Year",
      "min_stock": 0.0,
      "warranty_period": "1 Year Service Agreement",
      "warranty_terms": "Service guarantee with 2 hours breakdown response time",
      "payment_terms": "Quarterly Advance",
      "product_image": null,
      "status": "Active",
      "specifications": {
        "service_name": "Comprehensive Elevator AMC",
        "service_type": "AMC",
        "contract_type": "Annual",
        "contract_duration": "12 Months",
        "visit_frequency": "Monthly",
        "service_amount": 36000.0,
        "service_coverage": "Full electrical, mechanical, door drives, lubrication, emergency response",
        "service_description": "Monthly routine checkup plus unlimited emergency breakdown calls within 2 hours",
        "checklist": [
          "Inspection / Checking",
          "Cleaning",
          "Battery Check",
          "Electrical Check",
          "Safety Check",
          "Load Test",
          "Wiring Inspection",
          "Lubrication",
          "Repair / Replacement"
        ]
      },
      "created_at": "2026-09-10T10:33:05.567890",
      "updated_at": "2026-09-10T10:33:05.567890"
    }
  ]
}
```

---

### 8.6 List Other Products
url : (http://192.168.1.59:8000/api/products/other)
method : GET

params :- 

(None)

response :- 

```json
{
  "count": 1,
  "category_type": "other",
  "results": [
    {
      "id": 6,
      "category_type": "other",
      "category_id": 6,
      "category_name": "Other Product",
      "product_name": "Automatic Transfer Switch (ATS) 250A",
      "product_code": "OTH-ATS-250",
      "brand": "Socomec / ABB",
      "model_number": "ATyS-dM",
      "description": "Motorised changeover switch for mains and generator synchronization",
      "purchase_price": 35000.0,
      "selling_price": 48000.0,
      "discount": "2000",
      "gst_rate": "18%",
      "hsn_code": "85365090",
      "inventory_tracking": true,
      "stock": 5.0,
      "unit": "Nos",
      "min_stock": 1.0,
      "warranty_period": "2 Years",
      "warranty_terms": "Standard warranty",
      "payment_terms": "100% Advance",
      "product_image": null,
      "status": "Active",
      "specifications": {
        "custom_specifications": {
          "pole_count": 4,
          "current_rating": "250A",
          "operation_time_ms": 180
        }
      },
      "created_at": "2026-09-10T10:33:05.678901",
      "updated_at": "2026-09-10T10:33:05.678901"
    }
  ]
}
```

---

## 9. General Product Listing & Filtering API

url : (http://192.168.1.59:8000/api/products)
method : GET

params :- 

category_type:lift (Optional: lift, generator, panel, earthing, service, other)
category_id:1 (Optional: ID of category)
status:Active (Optional: Active, Inactive)
search:Schindler (Optional: searches across name, code, brand, model)

response :- 

```json
{
  "count": 1,
  "results": [
    {
      "id": 1,
      "category_type": "lift",
      "category_id": 1,
      "category_name": "Passenger Lift",
      "product_name": "Passenger Traction Lift 8P",
      "product_code": "LIFT-TR-001",
      "brand": "Schindler / Custom",
      "model_number": "TR-800",
      "description": "High speed traction lift for commercial buildings",
      "purchase_price": 1200000.0,
      "selling_price": 1500000.0,
      "discount": "5%",
      "gst_rate": "18%",
      "hsn_code": "84281011",
      "inventory_tracking": true,
      "stock": 2.0,
      "unit": "Set",
      "min_stock": 1.0,
      "warranty_period": "2 Years",
      "warranty_terms": "Comprehensive warranty including all mechanical parts",
      "payment_terms": "30% advance, 60% on delivery, 10% on handover",
      "product_image": "/uploads/products/39ec6f35383d4e99b205a2590b42a3e8.jpg",
      "status": "Active",
      "specifications": {
        "lift_type": "Passenger",
        "operation_type": "Automatic",
        "capacity": "8 Passenger",
        "rated_load": "544 KG",
        "speed": "1.0 m/s",
        "floor_designation": "G+4",
        "number_of_floors": "5",
        "number_of_stops": "5",
        "landing_entrances": "5",
        "car_entrances": "1",
        "car_openings": "1",
        "shaft_structure": "Concrete",
        "shaft_net_size": "1800 x 1800 mm",
        "shaft_height": "18000 mm",
        "floor_height": "3000 mm",
        "pit_depth": "1500 mm",
        "overhead_height": "4200 mm",
        "car_dimensions": "1100 x 1400 mm",
        "cabin_size": "1100 x 1400 x 2200 mm",
        "machine_type": "Gearless PMSM",
        "machine_model": "GL-800",
        "drive_system": "VVVF",
        "motor_brand": "Monarch",
        "controller_brand": "Monarch Nice 3000+",
        "control_panel_type": "Integrated Microprocessor",
        "power_supply": "415 V AC, 3 Phase",
        "voltage": "415 V",
        "phase": "3 Phase",
        "frequency": "50 Hz",
        "brake_type": "Electromagnetic Disc Brake",
        "car_finishing": "Hairline SS",
        "cabin_finish": "Titanium Gold / SS Mirror",
        "false_ceiling": "LED Downlight Panel",
        "flooring_type": "Granite Finish PVC",
        "car_door_type": "Center Opening",
        "car_door_finish": "Hairline Stainless Steel",
        "landing_door_finish": "SS Hairline on Ground Floor",
        "door_opening": "800 x 2000 mm",
        "door_sill": "Hard Extruded Aluminium",
        "landing_door_lock": "Electromechanical Interlock",
        "safety_features": [
          "Over Speed Protection",
          "Infra-Red Light Curtain",
          "Automatic Rescue Device (ARD)",
          "Single Phasing Preventer",
          "Emergency Stop Button"
        ]
      },
      "created_at": "2026-09-10T10:33:05.123456",
      "updated_at": "2026-09-10T10:33:05.123456"
    }
  ]
}
```

---

## 10. Single Product Details & Delete APIs

### 10.1 Get Single Product Details
url : (http://192.168.1.59:8000/api/products/1)
method : GET

params :- 

(None - product ID is passed in the URL path)

response :- 

```json
{
  "id": 1,
  "category_type": "lift",
  "category_id": 1,
  "category_name": "Passenger Lift",
  "product_name": "Passenger Traction Lift 8P",
  "product_code": "LIFT-TR-001",
  "brand": "Schindler / Custom",
  "model_number": "TR-800",
  "description": "High speed traction lift for commercial buildings",
  "purchase_price": 1200000.0,
  "selling_price": 1500000.0,
  "discount": "5%",
  "gst_rate": "18%",
  "hsn_code": "84281011",
  "inventory_tracking": true,
  "stock": 2.0,
  "unit": "Set",
  "min_stock": 1.0,
  "warranty_period": "2 Years",
  "warranty_terms": "Comprehensive warranty including all mechanical parts",
  "payment_terms": "30% advance, 60% on delivery, 10% on handover",
  "product_image": "/uploads/products/39ec6f35383d4e99b205a2590b42a3e8.jpg",
  "status": "Active",
  "specifications": {
    "lift_type": "Passenger",
    "operation_type": "Automatic",
    "capacity": "8 Passenger",
    "rated_load": "544 KG",
    "speed": "1.0 m/s",
    "floor_designation": "G+4",
    "number_of_floors": "5",
    "number_of_stops": "5",
    "landing_entrances": "5",
    "car_entrances": "1",
    "car_openings": "1",
    "shaft_structure": "Concrete",
    "shaft_net_size": "1800 x 1800 mm",
    "shaft_height": "18000 mm",
    "floor_height": "3000 mm",
    "pit_depth": "1500 mm",
    "overhead_height": "4200 mm",
    "car_dimensions": "1100 x 1400 mm",
    "cabin_size": "1100 x 1400 x 2200 mm",
    "machine_type": "Gearless PMSM",
    "machine_model": "GL-800",
    "drive_system": "VVVF",
    "motor_brand": "Monarch",
    "controller_brand": "Monarch Nice 3000+",
    "control_panel_type": "Integrated Microprocessor",
    "power_supply": "415 V AC, 3 Phase",
    "voltage": "415 V",
    "phase": "3 Phase",
    "frequency": "50 Hz",
    "brake_type": "Electromagnetic Disc Brake",
    "car_finishing": "Hairline SS",
    "cabin_finish": "Titanium Gold / SS Mirror",
    "false_ceiling": "LED Downlight Panel",
    "flooring_type": "Granite Finish PVC",
    "car_door_type": "Center Opening",
    "car_door_finish": "Hairline Stainless Steel",
    "landing_door_finish": "SS Hairline on Ground Floor",
    "door_opening": "800 x 2000 mm",
    "door_sill": "Hard Extruded Aluminium",
    "landing_door_lock": "Electromechanical Interlock",
    "safety_features": [
      "Over Speed Protection",
      "Infra-Red Light Curtain",
      "Automatic Rescue Device (ARD)",
      "Single Phasing Preventer",
      "Emergency Stop Button"
    ]
  },
  "created_at": "2026-09-10T10:33:05.123456",
  "updated_at": "2026-09-10T10:33:05.123456"
}
```

---

### 10.2 Delete Product
url : (http://192.168.1.59:8000/api/products/1)
method : DELETE

params :- 

(None - product ID is passed in the URL path)

response :- 

```json
{
  "message": "Product 'Passenger Traction Lift 8P' deleted successfully"
}
```

---

## 11. Payment APIs (Add Payment Screen)

> **Full Documentation:** See [PAYMENT_API_DOCUMENTATION.md](file:///c:/Users/PC/Desktop/power_solution/PAYMENT_API_DOCUMENTATION.md) for complete details, request examples, and Flutter integration snippets.

### 11.1 Auto-Generate Next Invoice / Order Number
- **URL:** `http://192.168.1.59:8000/api/payments/next-invoice-number`
- **Method:** `GET`
- **Response:** `{"invoice_no": "INV-260911-0001", "order_no": "INV-260911-0001"}`

### 11.2 Customer Dropdown (From Quotations)
- **URL:** `http://192.168.1.59:8000/api/payments/customers`
- **Method:** `GET`
- **Response:** List of customers with phone, email, address, and quotation details.

### 11.3 Add Payment
- **URL:** `http://192.168.1.59:8000/api/payments`
- **Method:** `POST`
- **Content-Type:** `multipart/form-data` or `application/json`
- **Params:** `invoice_no`, `customer_name`, `quotation_id`, `quotation_no`, `customer_phone`, `customer_email`, `customer_address`, `payment_date`, `amount_received`, `payment_mode` (`Cash`, `Online`, `Cheque`, `UPI`), `transaction_no`, `reference_no`, `notes`, `status`, `payment_proof` (file)
- **Response:** Created payment object with `invoice_no` and all details.

---

## 12. Order APIs (Create Order Screen)

> **Full Documentation:** See [ORDER_API_DOCUMENTATION.md](file:///c:/Users/PC/Desktop/power_solution/ORDER_API_DOCUMENTATION.md) for complete details and request examples.

### 12.1 Auto-Generate Next Order Number
- **URL:** `http://192.168.1.59:8000/api/orders/next-order-number`
- **Method:** `GET`
- **Response:** `{"order_no": "ORD-260912-0001"}`

### 12.2 Quotation Dropdown (For Select Quotation)
- **URL:** `http://192.168.1.59:8000/api/orders/quotations`
- **Method:** `GET`
- **Response:** List of approved quotations with customer info, line items, and amount calculations formatted for Flutter.

### 12.3 Create Order / Save Draft
- **URL:** `http://192.168.1.59:8000/api/orders`
- **Method:** `POST`
- **Content-Type:** `application/json`
- **Params:** `order_no`, `quotation_id`, `order_date`, `delivery_date`, `order_status`, `customer`, `subtotal`, `discount`, `tax`, `grand_total`, `advance_paid`, `balance_amount`, `payment_status`, `payment_mode`, `transaction_no`, `payment_date`, `special_instructions`, `internal_notes`, `terms_accepted`
- **Response:** Created order object with status 201.

---

## 13. Cash Bill APIs (Generate Cash Bill Screen)

> **Full Documentation:** See [CASH_BILL_API_DOCUMENTATION.md](file:///c:/Users/PC/Desktop/power_solution/CASH_BILL_API_DOCUMENTATION.md) for complete details, request examples, and calculation breakdowns.

### 13.1 Auto-Generate Next Bill Number
- **URL:** `http://192.168.1.59:8000/api/cash-bills/next-bill-number`
- **Method:** `GET`
- **Response:** `{"bill_no": "CB-260912-0001"}`

### 13.2 Product Picker Master (Categories & Products)
- **URL:** `http://192.168.1.59:8000/api/cash-bills/product-picker`
- **Method:** `GET`
- **Response:** Hierarchical master `product_types`, `categories`, and `products` matching Flutter bottom sheet.

### 13.3 Calculate Bill (Live Calculations Preview)
- **URL:** `http://192.168.1.59:8000/api/cash-bills/calculate`
- **Method:** `POST`
- **Params:** `items`, `discount`, `amount_paid`
- **Response:** Computed `subtotal`, `taxable_amount`, `gst` (18%), `grand_total`, `change_returned`, `balance_amount`.

### 13.4 Generate Cash Bill / Save Draft
- **URL:** `http://192.168.1.59:8000/api/cash-bills`
- **Method:** `POST`
- **Content-Type:** `application/json`
- **Params:** `bill_no`, `bill_date`, `customer_type`, `customer_name`, `mobile`, `items`, `discount`, `payment_mode`, `amount_paid`, `notes`, `status`
- **Response:** Generated cash bill object with calculated totals.

---

## 14. Purchase Order APIs (Add Purchase Order Screen)

> **Full Documentation:** See [PURCHASE_API_DOCUMENTATION.md](file:///c:/Users/PC/Desktop/power_solution/PURCHASE_API_DOCUMENTATION.md) for complete details, request examples, and calculation breakdowns.

### 14.1 Auto-Generate Next PO Number
- **URL:** `http://192.168.1.59:8000/api/purchases/next-po-number`
- **Method:** `GET`
- **Params:** `(None)`
- **Response:** `{"po_number": "PO-260914-0001"}`

### 14.2 Supplier Dropdown (Select Supplier)
- **URL:** `http://192.168.1.59:8000/api/purchases/suppliers`
- **Method:** `GET`
- **Params:** `(None)`
- **Response:** List of suppliers with code, name, contact person, mobile, email, and address.

### 14.3 Add New Supplier
- **URL:** `http://192.168.1.59:8000/api/purchases/suppliers`
- **Method:** `POST`
- **Params:** `name`, `supplier_code` (optional), `contact_person`, `mobile`, `email`, `address`, `gstin`
- **Response:** Created supplier object with assigned code.

### 14.4 Purchase Product Picker Master
- **URL:** `http://192.168.1.59:8000/api/purchases/product-picker`
- **Method:** `GET`
- **Params:** `(None)`
- **Response:** Hierarchical master with `purchasePrice`, `sku`, `unit`, `gst` (18%), and technical specifications.

### 14.5 Calculate Purchase Order (Live Preview)
- **URL:** `http://192.168.1.59:8000/api/purchases/calculate`
- **Method:** `POST`
- **Params:** `items`
- **Response:** Computed `subtotal`, `gst_total` (18%), and `grand_total`.

### 14.6 Place Purchase Order / Save Draft
- **URL:** `http://192.168.1.59:8000/api/purchases`
- **Method:** `POST`
- **Content-Type:** `application/json`
- **Params:** `po_number`, `supplier_id`, `po_date`, `expected_delivery`, `payment_terms`, `status`, `reference`, `items`, `notes`
- **Response:** Created purchase order object with computed totals.

### 14.7 List All Purchase Orders
- **URL:** `http://192.168.1.59:8000/api/purchases`
- **Method:** `GET`
- **Params:** `(None)`
- **Response:** List of purchase orders with summary counts and totals.






