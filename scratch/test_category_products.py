import os
import sys
import json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from core.settings import SessionLocal, ensure_database_schema
from api.models import Category, Product, Quotation
from api.schemas import QuotationCreateRequest, QuotationItemSchema
from main import app

def run_tests():
    ensure_database_schema()
    client = TestClient(app)

    print("--- 1. Testing Category Changes on GET /api/products?category_id=X ---")
    res_cat4 = client.get("/api/products?category_id=4").json()
    res_cat5 = client.get("/api/products?category_id=5").json()
    res_cat_empty = client.get("/api/products?category_id=999999").json()

    print(f"  Category 4 ({res_cat4['category_name']}) -> {res_cat4['count']} products: {[p['product_name'] for p in res_cat4['products']]}")
    print(f"  Category 5 ({res_cat5['category_name']}) -> {res_cat5['count']} products: {[p['product_name'] for p in res_cat5['products']]}")
    print(f"  Empty Category 999999 -> {res_cat_empty['count']} products")

    assert res_cat4["category_id"] == 4
    assert res_cat5["category_id"] == 5
    assert res_cat4["products"][0]["id"] == 9
    assert res_cat5["products"][0]["id"] == 10
    assert res_cat4["products"] != res_cat5["products"], "Category 4 and 5 must return different products!"
    assert res_cat_empty["count"] == 0, "Non-existent category should return 0 products!"
    print("  [OK] Responses change accurately based on selected category!")

    print("\n--- 1b. Testing Category Name and Body Param variations ---")
    res_name4 = client.get("/api/products?category=Passenger Lift").json()
    res_name5 = client.get("/api/products?category=Silent DG").json()
    assert res_name4["products"][0]["id"] == 9
    assert res_name5["products"][0]["id"] == 10
    assert res_name4["products"] != res_name5["products"]
    print("  [OK] ?category=Passenger Lift vs ?category=Silent DG return distinct products!")

    print("\n--- 2. Testing GET /api/categories/{category_id}/products ---")
    res = client.get("/api/categories/4/products")
    assert res.status_code == 200, f"Expected 200, got {res.status_code}: {res.text}"
    data = res.json()
    print("Category ID:", data.get("category_id"))
    print("Category Name:", data.get("category_name"))
    print("Category Type:", data.get("category_type"))
    print("Total Products Found:", data.get("count"))
    assert "products" in data
    assert "results" in data
    assert data["category_id"] == 4
    assert len(data["products"]) > 0

    product0 = data["products"][0]
    print("\nFirst product details:")
    print("  ID:", product0.get("id"))
    print("  Product Name:", product0.get("product_name"))
    print("  Product Code:", product0.get("product_code"))
    print("  Category Type:", product0.get("category_type"))
    print("  Brand:", product0.get("brand"))
    print("  Model Number:", product0.get("model_number"))
    print("  Specifications count:", len(product0.get("specifications", {})))
    assert "specifications" in product0
    assert isinstance(product0["specifications"], dict)
    assert "selling_price" in product0

    print("\n--- 2. Testing Path Aliases ---")
    for path in [
        "/api/category/4/products",
        "/api/products/category/4",
        "/api/quotations/products-by-category/4",
    ]:
        alias_res = client.get(path)
        assert alias_res.status_code == 200, f"Failed for path {path}: {alias_res.status_code}"
        assert alias_res.json()["category_id"] == 4
        print(f"  [OK] {path}")

    print("\n--- 3. Testing 404 for non-existent category ---")
    res_404 = client.get("/api/categories/999999/products")
    assert res_404.status_code == 404
    print("  [OK] 404 correctly returned for non-existent category")

    print("\n--- 4. Testing Single Product Detail Aliases ---")
    prod_res = client.get("/api/quotations/product-details/9")
    assert prod_res.status_code == 200
    prod_data = prod_res.json()
    assert prod_data["id"] == 9
    assert prod_data["product_name"] == "khfk"
    print("  [OK] /api/quotations/product-details/9 works")

    prod_res2 = client.get("/api/quotations/products/9")
    assert prod_res2.status_code == 200
    print("  [OK] /api/quotations/products/9 works")

    print("\n--- 5. Testing Search & Filter on Category Products ---")
    search_res = client.get("/api/categories/4/products?search=khfk")
    assert search_res.status_code == 200
    assert search_res.json()["count"] >= 1
    print("  [OK] Search filter works")

    print("\n--- 6. Testing Quotation Creation with Auto-Enriched Product Details ---")
    db = SessionLocal()
    try:
        # Find next quotation number
        next_no_res = client.get("/api/quotations/next-number").json()
        qtn_no = next_no_res["quotation_no"]

        # Create quotation where item specifies product_id=9 but leaves specifications empty
        payload = {
            "quotation_no": qtn_no,
            "quotation_date": "11 Sep 2026",
            "valid_till": "30 Sep 2026",
            "customer_name": "Test Lift Client",
            "phone": "9876543210",
            "items": [
                {
                    "type": "lift",
                    "category": "Passenger Lift",
                    "category_id": 4,
                    "product": "khfk",
                    "product_id": 9,
                    "quantity": 2,
                    "unit_price": 500000.0,
                    # specifications not provided here, should be auto-enriched from DB
                }
            ],
            "discount_type": "Flat",
            "discount_value": 0,
            "tax_type": "GST 18%",
            "status": "Draft",
        }

        create_res = client.post("/api/quotations", json=payload)
        assert create_res.status_code == 201, f"Failed create: {create_res.text}"
        created_qtn = create_res.json()["quotation"]
        print("Quotation Created:", created_qtn["quotation_no"])
        q_item = created_qtn["items"][0]
        print("  Saved item category_id:", q_item.get("category_id"))
        print("  Saved item product_id:", q_item.get("product_id"))
        print("  Saved item specifications keys count:", len(q_item.get("specifications", {})))
        print("  Saved item total_price:", q_item.get("total_price"))

        assert q_item.get("category_id") == 4
        assert q_item.get("product_id") == 9
        assert len(q_item.get("specifications", {})) > 0, "Specifications should have been enriched from Product DB"
        assert q_item.get("total_price") == 1000000.0

        # Clean up the test quotation
        client.delete(f"/api/quotations/{created_qtn['id']}")
        print("  [OK] Test quotation cleaned up")
    finally:
        db.close()

    print("\n>>> All Category Products API and Quotation integration tests passed successfully! <<<")

if __name__ == "__main__":
    run_tests()
