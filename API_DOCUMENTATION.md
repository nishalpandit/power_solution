# Power Solution API Documentation

Base URL: http://192.168.1.59:8000/api

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

---

### 1.2 List Categories
url : (http://192.168.1.59:8000/api/categories)
method : GET

params :- 

(None)

response :- 

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
power_supply:415 V +/- 10%, 50 Hz, 3 Phase 4 Wire
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
      "power_supply": "415 V +/- 10%, 50 Hz, 3 Phase 4 Wire"
    },
    "created_at": "2026-09-10T10:33:05.345678",
    "updated_at": "2026-09-10T10:33:05.345678"
  }
}

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

---

## 8. Category-Specific Listing APIs

### 8.1 List Lift Products
url : (http://192.168.1.59:8000/api/products/lift)
method : GET

params :- 

(None)

response :- 

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

---

### 8.2 List Generator Products
url : (http://192.168.1.59:8000/api/products/generator)
method : GET

params :- 

(None)

response :- 

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

---

### 8.3 List Panel Products
url : (http://192.168.1.59:8000/api/products/panel)
method : GET

params :- 

(None)

response :- 

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
        "power_supply": "415 V +/- 10%, 50 Hz, 3 Phase 4 Wire"
      },
      "created_at": "2026-09-10T10:33:05.345678",
      "updated_at": "2026-09-10T10:33:05.345678"
    }
  ]
}

---

### 8.4 List Earthing Products
url : (http://192.168.1.59:8000/api/products/earthing)
method : GET

params :- 

(None)

response :- 

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

---

### 8.5 List Service Products
url : (http://192.168.1.59:8000/api/products/service)
method : GET

params :- 

(None)

response :- 

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

---

### 8.6 List Other Products
url : (http://192.168.1.59:8000/api/products/other)
method : GET

params :- 

(None)

response :- 

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

---

## 10. Single Product Details & Delete APIs

### 10.1 Get Single Product Details
url : (http://192.168.1.59:8000/api/products/1)
method : GET

params :- 

(None - product ID is passed in the URL path)

response :- 

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

---

### 10.2 Delete Product
url : (http://192.168.1.59:8000/api/products/1)
method : DELETE

params :- 

(None - product ID is passed in the URL path)

response :- 

{
  "message": "Product 'Passenger Traction Lift 8P' deleted successfully"
}

---

---

## 11. Payment APIs

### 11.1 Auto-Generate Next Invoice / Order Number
url : (http://192.168.1.59:8000/api/payments/next-invoice-number)
method : GET

(Also supports http://192.168.1.59:8000/api/payments/next-number)

params :- 

(None)

response :- 

{
  "invoice_no": "INV-260911-0001",
  "order_no": "INV-260911-0001"
}

---

### 11.2 Customer Dropdown (From Quotation)
url : (http://192.168.1.59:8000/api/payments/customers)
method : GET

(Also supports http://192.168.1.59:8000/api/quotations/customers)

params :- 

(None)

response :- 

{
  "count": 2,
  "results": [
    {
      "customer_name": "Skyline Enterprises",
      "phone": "+91 9876543210",
      "email": "contact@skyline.com",
      "address": "45 Industrial Area, Phase 2, New Delhi",
      "latest_quotation_id": 1,
      "latest_quotation_no": "QTN-250517-0001",
      "quotations": [
        {
          "id": 1,
          "quotation_no": "QTN-250517-0001",
          "quotation_date": "17 May 2025",
          "grand_total": 501500.0,
          "status": "Sent"
        }
      ]
    }
  ]
}

---

### 11.3 Create / Add Payment
url : (http://192.168.1.59:8000/api/payments/add)
method : POST

(Also supports http://192.168.1.59:8000/api/payment/add and http://192.168.1.59:8000/api/payments)

params :- 

invoice_no:INV-260911-0001
customer_name:Skyline Enterprises
quotation_id:1
quotation_no:QTN-250517-0001
customer_phone:+91 9876543210
customer_email:contact@skyline.com
customer_address:45 Industrial Area, Phase 2, New Delhi
payment_date:2026-09-11
amount_received:50000.00
payment_mode:Cash (Options: Cash, Online, Cheque, UPI)
transaction_no:TRX-987654321
reference_no:REF-001
notes:Payment received
status:Received
payment_proof:upload (File: JPG, PNG, PDF)

response :- 

{
  "message": "Payment created successfully",
  "payment": {
    "id": 1,
    "invoice_no": "INV-260911-0001",
    "customer_name": "Skyline Enterprises",
    "amount_received": 50000.0,
    "payment_mode": "Cash",
    "status": "Received"
  }
}

---

### 11.4 List All Payments
url : (http://192.168.1.59:8000/api/payments)
method : GET

params :- 

(None)

response :- 

{
  "count": 1,
  "payments": [
    {
      "id": 1,
      "payment_no": "INV-260911-0001",
      "customer_name": "Skyline Enterprises",
      "amount_received": 50000.0,
      "payment_mode": "Cash",
      "status": "Received"
    }
  ]
}

---

### 11.5 Get Single Payment Details
url : (http://192.168.1.59:8000/api/payments/1)
method : GET

params :- 

(None)

response :- 

{
  "id": 1,
  "payment_no": "INV-260911-0001",
  "customer_name": "Skyline Enterprises",
  "amount_received": 50000.0,
  "status": "Received"
}

---

### 11.6 Delete Payment
url : (http://192.168.1.59:8000/api/payments/1)
method : DELETE

params :- 

(None)

response :- 

{
  "message": "Payment 1 deleted successfully"
}

---

## 12. Order APIs

### 12.1 Auto-Generate Next Order Number
url : (http://192.168.1.59:8000/api/orders/next-order-number)
method : GET

params :- 

(None)

response :- 

{
  "order_no": "ORD-260912-0001"
}

---

### 12.2 Quotation Dropdown (Select Quotation)
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
      "grandTotal": 501500.0,
      "status": "Sent"
    }
  ]
}

---

### 12.3 Create Order / Save Draft
url : (http://192.168.1.59:8000/api/orders)
method : POST

params :- 

order_no:ORD-260912-0001
quotation_id:1
order_date:12 Sep 2026
delivery_date:20 Sep 2026
order_status:Confirmed
customer:Skyline Enterprises
subtotal:450000.00
discount:25000.00
tax:76500.00
grand_total:501500.00
advance_paid:100000.00
balance_amount:401500.00
payment_status:Partially Paid
payment_mode:Online / Bank Transfer
transaction_no:TXN-20260912-001
payment_date:12 Sep 2026
special_instructions:Handle with care
internal_notes:Priority delivery
terms_accepted:true

response :- 

{
  "message": "Order created successfully",
  "order": {
    "id": 1,
    "order_no": "ORD-260912-0001",
    "customer": "Skyline Enterprises",
    "grand_total": 501500.0,
    "order_status": "Confirmed"
  }
}

---

### 12.4 List All Orders
url : (http://192.168.1.59:8000/api/orders)
method : GET

params :- 

(None)

response :- 

{
  "count": 1,
  "orders": [
    {
      "id": 1,
      "order_no": "ORD-260912-0001",
      "customer": "Skyline Enterprises",
      "grand_total": 501500.0,
      "order_status": "Confirmed"
    }
  ]
}

---

### 12.5 Single Order Details
url : (http://192.168.1.59:8000/api/orders/1)
method : GET

params :- 

(None)

response :- 

{
  "id": 1,
  "order_no": "ORD-260912-0001",
  "customer": "Skyline Enterprises",
  "grand_total": 501500.0,
  "order_status": "Confirmed"
}

---

### 12.6 Delete Order
url : (http://192.168.1.59:8000/api/orders/1)
method : DELETE

params :- 

(None)

response :- 

{
  "message": "Order ORD-260912-0001 deleted successfully"
}

---

## 13. Cash Bill APIs

### 13.1 Auto-Generate Next Bill Number
url : (http://192.168.1.59:8000/api/cash-bills/next-bill-number)
method : GET

params :- 

(None)

response :- 

{
  "bill_no": "CB-260912-0001"
}

---

### 13.2 Product Picker Master (Categories & Products)
url : (http://192.168.1.59:8000/api/cash-bills/product-picker)
method : GET

params :- 

(None)

response :- 

{
  "product_types": [
    "Lift",
    "Generator",
    "LT Panel",
    "Earthing",
    "Service",
    "Other"
  ]
}

---

### 13.3 Calculate Bill (Live Calculation Preview)
url : (http://192.168.1.59:8000/api/cash-bills/calculate)
method : POST

params :- 

items:[{"id":"LIFT001","name":"G+2 Automatic Passenger Lift","price":450000.0,"qty":1}]
discount:0.0
amount_paid:500000.0

response :- 

{
  "subtotal": 450000.0,
  "discount": 0.0,
  "taxable_amount": 450000.0,
  "gst": 81000.0,
  "grand_total": 531000.0,
  "amount_paid": 500000.0,
  "change_returned": 0.0,
  "balance_amount": 31000.0
}

---

### 13.4 Generate Cash Bill / Save Draft
url : (http://192.168.1.59:8000/api/cash-bills)
method : POST

params :- 

bill_no:CB-260912-0001
bill_date:12 Sep 2026
customer_type:Walk-in Customer
customer_name:Rohan Sharma
mobile:9876500001
items:[{"name":"G+2 Automatic Passenger Lift","price":450000.0,"qty":1}]
discount:0.0
payment_mode:Cash
amount_paid:531000.0
notes:Delivered directly from counter
status:Generated

response :- 

{
  "message": "Cash bill 'CB-260912-0001' generated successfully",
  "bill": {
    "id": 1,
    "bill_no": "CB-260912-0001",
    "customer_name": "Rohan Sharma",
    "grand_total": 531000.0,
    "status": "Generated"
  }
}

---

### 13.5 List All Cash Bills
url : (http://192.168.1.59:8000/api/cash-bills)
method : GET

params :- 

(None)

response :- 

{
  "count": 1,
  "results": [
    {
      "id": 1,
      "bill_no": "CB-260912-0001",
      "customer_name": "Rohan Sharma",
      "grand_total": 531000.0,
      "status": "Generated"
    }
  ]
}

---

### 13.6 Single Cash Bill Details
url : (http://192.168.1.59:8000/api/cash-bills/1)
method : GET

params :- 

(None)

response :- 

{
  "id": 1,
  "bill_no": "CB-260912-0001",
  "customer_name": "Rohan Sharma",
  "grand_total": 531000.0,
  "status": "Generated"
}

---

### 13.7 Delete Cash Bill
url : (http://192.168.1.59:8000/api/cash-bills/1)
method : DELETE

params :- 

(None)

response :- 

{
  "message": "Cash bill 'CB-260912-0001' deleted successfully"
}

---

## 14. Purchase Order APIs

### 14.1 Auto-Generate Next PO Number
url : (http://192.168.1.59:8000/api/purchases/next-po-number)
method : GET

(Also supports http://192.168.1.59:8000/api/purchases/next-number and http://192.168.1.59:8000/api/purchase-orders/next-number)

params :- 

(None)

response :- 

{
  "po_number": "PO-260914-0001"
}

---

### 14.2 Supplier Dropdown (Select Supplier)
url : (http://192.168.1.59:8000/api/purchases/suppliers)
method : GET

(Also supports http://192.168.1.59:8000/api/suppliers and http://192.168.1.59:8000/api/purchase-orders/suppliers)

params :- 

(None)

response :- 

{
  "count": 2,
  "suppliers": [
    {
      "id": 1,
      "supplier_code": "SUP-001",
      "supplier_name": "Kirloskar Oil Engines Ltd",
      "contact_person": "Amit Sharma",
      "mobile": "9876543210",
      "email": "amit@kirloskar.com",
      "address": "Pune, Maharashtra"
    }
  ]
}

---

### 14.3 Add New Supplier
url : (http://192.168.1.59:8000/api/purchases/suppliers)
method : POST

(Also supports http://192.168.1.59:8000/api/suppliers and http://192.168.1.59:8000/api/purchase-orders/suppliers)

params :- 

name:Kirloskar Oil Engines Ltd
supplier_code:SUP-001
contact_person:Amit Sharma
mobile:9876543210
email:amit@kirloskar.com
address:Pune, Maharashtra
city:Pune
state:Maharashtra
pincode:411001
payment_terms:30 Days Net
gstin:27AAACK1234F1Z5
pan_number:AAACK1234F
remarks:Main DG engine supplier

response :- 

{
  "message": "Supplier created successfully",
  "supplier": {
    "id": 1,
    "supplier_code": "SUP-001",
    "name": "Kirloskar Oil Engines Ltd"
  }
}

---

### 14.4 Purchase Product Picker Master
url : (http://192.168.1.59:8000/api/purchases/product-picker)
method : GET

params :- 

(None)

response :- 

{
  "product_types": [
    "Lift",
    "Generator",
    "LT Panel",
    "Earthing",
    "Service",
    "Other"
  ]
}

---

### 14.5 Calculate Purchase Order (Live Preview)
url : (http://192.168.1.59:8000/api/purchases/calculate)
method : POST

(Also supports http://192.168.1.59:8000/api/purchase-orders/calculate)

params :- 

items:[{"product_name":"15 kVA Silent DG Set","purchase_price":210000,"qty":1,"unit":"Set","gst":18}]

response :- 

{
  "subtotal": 210000.0,
  "gst_total": 37800.0,
  "grand_total": 247800.0
}

---

### 14.6 Place Purchase Order / Save Draft
url : (http://192.168.1.59:8000/api/purchases)
method : POST

(Also supports http://192.168.1.59:8000/api/purchases/create, http://192.168.1.59:8000/api/purchase-orders, and http://192.168.1.59:8000/api/purchase-orders/create)

params :- 

po_number:PO-260914-0001
supplier_id:1
po_date:14 Sep 2026
expected_delivery:21 Sep 2026
payment_terms:30% Advance, 70% Against Delivery
status:Ordered
reference:REF-PO-001
items:[{"product_name":"15 kVA Silent DG Set","purchase_price":210000,"qty":1,"unit":"Set","gst":18}]
notes:Urgent delivery required

response :- 

{
  "message": "Purchase order created successfully",
  "purchase_order": {
    "id": 1,
    "po_number": "PO-260914-0001",
    "supplier_name": "Kirloskar Oil Engines Ltd",
    "grand_total": 247800.0,
    "status": "Ordered"
  }
}

---

### 14.7 List All Purchase Orders
url : (http://192.168.1.59:8000/api/purchases)
method : GET

(Also supports http://192.168.1.59:8000/api/purchase-orders)

params :- 

(None)

response :- 

{
  "count": 1,
  "purchase_orders": [
    {
      "id": 1,
      "po_number": "PO-260914-0001",
      "supplier_name": "Kirloskar Oil Engines Ltd",
      "grand_total": 247800.0,
      "status": "Ordered"
    }
  ]
}

---

### 14.8 Single Purchase Order Details
url : (http://192.168.1.59:8000/api/purchases/1)
method : GET

(Also supports http://192.168.1.59:8000/api/purchase-orders/1 and PO string e.g. PO-260914-0001)

params :- 

(None)

response :- 

{
  "id": 1,
  "po_number": "PO-260914-0001",
  "supplier_name": "Kirloskar Oil Engines Ltd",
  "grand_total": 247800.0,
  "status": "Ordered"
}

---

### 14.9 Delete Purchase Order
url : (http://192.168.1.59:8000/api/purchases/1)
method : DELETE

(Also supports http://192.168.1.59:8000/api/purchase-orders/1)

params :- 

(None)

response :- 

{
  "message": "Purchase order PO-260914-0001 deleted successfully"
}

---

## 15. Invoice APIs

### 15.1 Auto-Generate Next Invoice Number
url : (http://192.168.1.59:8000/api/invoices/next-invoice-number)
method : GET

(Also supports http://192.168.1.59:8000/api/invoices/next-number)

params :- 

(None)

response :- 

{
  "invoice_no": "INV-260912-0001"
}

---

### 15.2 Order Dropdown (Auto-fills Customer Details & Items)
url : (http://192.168.1.59:8000/api/invoices/orders)
method : GET

params :- 

(None)

response :- 

{
  "count": 1,
  "orders": [
    {
      "order_no": "ORD-260912-0001",
      "customer_name": "Skyline Enterprises",
      "phone": "+91 9876543210",
      "email": "contact@skyline.com",
      "billing_address": "45 Industrial Area, Phase 2, New Delhi",
      "grand_total": 501500.0
    }
  ]
}

---

### 15.3 Customer List (Select Customer Modal)
url : (http://192.168.1.59:8000/api/invoices/customers)
method : GET

params :- 

(None)

response :- 

{
  "count": 2,
  "customers": [
    {
      "customer_name": "Skyline Enterprises",
      "phone": "+91 9876543210",
      "email": "contact@skyline.com",
      "billing_address": "45 Industrial Area, Phase 2, New Delhi"
    }
  ]
}

---

### 15.4 Create Invoice
url : (http://192.168.1.59:8000/api/invoices)
method : POST

(Also supports http://192.168.1.59:8000/api/invoices/create and http://192.168.1.59:8000/api/invoices/add)

params :- 

invoice_no:INV-260912-0001
invoice_date:12 Sep 2026
due_date:26 Sep 2026
order_no:ORD-260912-0001
payment_terms:Net 15
reference_no:REF-INV-001
customer_name:Skyline Enterprises
phone:+91 9876543210
email:contact@skyline.com
billing_address:45 Industrial Area, Phase 2, New Delhi
delivery_address:45 Industrial Area, Phase 2, New Delhi
items:[{"item_name":"G+2 Automatic Passenger Lift","price":450000,"qty":1,"total":450000}]
subtotal:450000.00
discount:25000.00
tax:76500.00
tax_percent:18.00
grand_total:501500.00
notes:Thank you for your business
status:Pending

response :- 

{
  "message": "Invoice created successfully",
  "invoice": {
    "id": 1,
    "invoice_no": "INV-260912-0001",
    "customer_name": "Skyline Enterprises",
    "grand_total": 501500.0,
    "status": "Pending"
  }
}

---

### 15.5 List All Invoices
url : (http://192.168.1.59:8000/api/invoices)
method : GET

params :- 

search: (Optional) Search by invoice no, customer name, order no, or phone
customer_name: (Optional) Filter by customer name
status: (Optional) Filter by status (Paid, Pending, Partial, Overdue)
order_no: (Optional) Filter by order no
payment_terms: (Optional) Filter by payment terms

response :- 

{
  "count": 1,
  "invoices": [
    {
      "id": 1,
      "invoice_no": "INV-260912-0001",
      "customer_name": "Skyline Enterprises",
      "grand_total": 501500.0,
      "status": "Pending"
    }
  ]
}

---

### 15.6 Single Invoice Details
url : (http://192.168.1.59:8000/api/invoices/1)
method : GET

(Also supports invoice number e.g. http://192.168.1.59:8000/api/invoices/INV-260912-0001)

params :- 

(None)

response :- 

{
  "id": 1,
  "invoice_no": "INV-260912-0001",
  "customer_name": "Skyline Enterprises",
  "grand_total": 501500.0,
  "status": "Pending"
}

---

### 15.7 Update Invoice Status
url : (http://192.168.1.59:8000/api/invoices/1/status)
method : PATCH

(Also supports PUT http://192.168.1.59:8000/api/invoices/1/status)

params :- 

status:Paid

response :- 

{
  "message": "Invoice status updated successfully",
  "invoice_no": "INV-260912-0001",
  "status": "Paid"
}

---

### 15.8 Delete Invoice
url : (http://192.168.1.59:8000/api/invoices/1)
method : DELETE

params :- 

(None)

response :- 

{
  "message": "Invoice INV-260912-0001 deleted successfully"
}

---

## 16. User APIs

### 16.1 List All Users
url : (http://192.168.1.59:8000/api/users)
method : GET

(Also supports http://192.168.1.59:8000/api/users/list and http://192.168.1.59:8000/api/user/list)

params :- 

search: (Optional) Search text matching user's full name, email, phone number, or username
role: (Optional) Filter by role (user or admin)
is_active: (Optional) Filter by active status (true or false)
limit: (Optional) Integer to limit number of records
offset: (Optional) Integer to offset results for pagination

response :- 

{
  "count": 12,
  "users": [
    {
      "id": 1,
      "username": null,
      "full_name": "Test User",
      "email": "test88190241@example.com",
      "phone_number": "15558819024",
      "role": "user",
      "is_active": true,
      "created_at": "2026-09-09T04:43:59.992396",
      "updated_at": "2026-09-09T04:43:59.992405"
    },
    {
      "id": 6,
      "username": "admin",
      "full_name": "System Administrator",
      "email": "admin@power.solution",
      "phone_number": "0000000000",
      "role": "admin",
      "is_active": true,
      "created_at": "2026-09-09T05:19:42.523953",
      "updated_at": "2026-09-09T05:19:42.523959"
    }
  ],
  "results": [
    {
      "id": 1,
      "username": null,
      "full_name": "Test User",
      "email": "test88190241@example.com",
      "phone_number": "15558819024",
      "role": "user",
      "is_active": true,
      "created_at": "2026-09-09T04:43:59.992396",
      "updated_at": "2026-09-09T04:43:59.992405"
    },
    {
      "id": 6,
      "username": "admin",
      "full_name": "System Administrator",
      "email": "admin@power.solution",
      "phone_number": "0000000000",
      "role": "admin",
      "is_active": true,
      "created_at": "2026-09-09T05:19:42.523953",
      "updated_at": "2026-09-09T05:19:42.523959"
    }
  ]
}

---

### 16.2 Get Single User Details
url : (http://192.168.1.59:8000/api/users/6)
method : GET

(Also supports http://192.168.1.59:8000/api/user/6)

params :- 

(None)

response :- 

{
  "message": "User details fetched successfully",
  "user": {
    "id": 6,
    "username": "admin",
    "full_name": "System Administrator",
    "email": "admin@power.solution",
    "phone_number": "0000000000",
    "role": "admin",
    "is_active": true,
    "created_at": "2026-09-09T05:19:42.523953",
    "updated_at": "2026-09-09T05:19:42.523959"
  }
}
