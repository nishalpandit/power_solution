import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.settings import SessionLocal
from api.models import Category, Product

db = SessionLocal()
print('=== CATEGORIES IN DB ===')
for c in db.query(Category).all():
    print(f'ID: {c.id}, Name: "{c.category_name}", Type: "{c.category_type}"')

print('\n=== PRODUCTS IN DB ===')
for p in db.query(Product).all():
    print(f'ID: {p.id}, Name: "{p.product_name}", Category ID: {p.category_id}, Category Name: "{p.category_name}", Category Type: "{p.category_type}"')

db.close()
