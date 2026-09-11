import urllib.request
import json

def test(name, url):
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as resp:
            r = json.loads(resp.read().decode())
            print(f"=== {name} ===")
            print("URL:", url)
            if "product" in r:
                p = r["product"]
                print(f"  Product: ID={p.get('id')}, Name={p.get('product_name')}, TypeID={p.get('category_type_id')}, CatNameID={p.get('category_name_id')}, SpecsCount={len(p.get('specifications', {}))}")
            elif "product_name" in r:
                print(f"  Single Product Object: ID={r.get('id')}, Name={r.get('product_name')}, TypeID={r.get('category_type_id')}, CatNameID={r.get('category_name_id')}, SpecsCount={len(r.get('specifications', {}))}")
            elif "products" in r:
                print(f"  Product List Count: {r.get('count')}")
                for p in r["products"][:2]:
                    print(f"    ID={p.get('id')}, Name={p.get('product_name')}, TypeID={p.get('category_type_id')}, CatNameID={p.get('category_name_id')}")
            elif "categories" in r:
                print(f"  Categories Count: {r.get('count')}")
                for c in r["categories"]:
                    print(f"    CatNameID={c.get('id')}, Name={c.get('category_name')}, TypeID={c.get('category_type_id')}")
    except Exception as e:
        print(f"=== {name} ERROR ===: {e}")

if __name__ == "__main__":
    test("1. Categories under Lift (Type ID 1)", "http://192.168.1.59:8000/api/categories?category_type_id=1")
    test("2. Categories under Generator (Type ID 2)", "http://192.168.1.59:8000/api/categories?category_type_id=2")
    test("3. Products under Category Name 4 (Passenger Lift)", "http://192.168.1.59:8000/api/products?category_type_id=1&category_name_id=4")
    test("4. Full Product Details (Lift Product 9)", "http://192.168.1.59:8000/api/products?category_type_id=1&category_name_id=4&product_id=9")
    test("5. Full Product Details (Generator Product 10)", "http://192.168.1.59:8000/api/products?category_type_id=2&category_name_id=5&product_id=10")
    test("6. Dedicated /api/products/details", "http://192.168.1.59:8000/api/products/details?category_type_id=1&category_name_id=4&product_id=9")
