"""
Seed script — iSpace uchun 15 ta namunaviy mahsulot qo'shadi.
"""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_tennis_club.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from members.models import Category, Product

# ─── Kategoriyalar ────────────────────────────────────────────────────────────
cats_data = [
    {'name': 'iPhone',   'slug': 'iphone'},
    {'name': 'Mac',      'slug': 'mac'},
    {'name': 'iPad',     'slug': 'ipad'},
    {'name': 'Samsung',  'slug': 'samsung'},
    {'name': 'TV',       'slug': 'tv'},
]

cats = {}
for c in cats_data:
    obj, created = Category.objects.get_or_create(slug=c['slug'], defaults={'name': c['name']})
    cats[c['slug']] = obj
    if created:
        print(f"  Category created: {c['name']}")
    else:
        print(f"  Category exists:  {c['name']}")

# ─── Mahsulotlar ──────────────────────────────────────────────────────────────
products_data = [
    # --- iPhone ---
    {
        'category': 'iphone', 'title': 'iPhone 15 Pro Max',
        'vendor': 'APPLE', 'price': 18_254_000, 'old_price': None,
        'display_size': '6.7"', 'processor': 'A17 Pro', 'internal_memory': '256 GB',
        'camera': '48MP + 12MP + 12MP', 'battery_info': '4422 mAh',
        'color': 'Natural Titanium', 'is_trending': True,
    },
    {
        'category': 'iphone', 'title': 'iPhone 15 Pro',
        'vendor': 'APPLE', 'price': 15_800_000, 'old_price': 16_500_000,
        'display_size': '6.1"', 'processor': 'A17 Pro', 'internal_memory': '128 GB',
        'camera': '48MP + 12MP + 12MP', 'battery_info': '3274 mAh',
        'color': 'Black Titanium', 'is_trending': True,
    },
    {
        'category': 'iphone', 'title': 'iPhone 15',
        'vendor': 'APPLE', 'price': 12_300_000, 'old_price': None,
        'display_size': '6.1"', 'processor': 'A16 Bionic', 'internal_memory': '128 GB',
        'camera': '48MP + 12MP', 'battery_info': '3349 mAh',
        'color': 'Pink', 'is_trending': True,
    },
    {
        'category': 'iphone', 'title': 'iPhone 14',
        'vendor': 'APPLE', 'price': 9_800_000, 'old_price': 11_000_000,
        'display_size': '6.1"', 'processor': 'A15 Bionic', 'internal_memory': '128 GB',
        'camera': '12MP + 12MP', 'battery_info': '3279 mAh',
        'color': 'Midnight', 'is_trending': True,
    },

    # --- Mac ---
    {
        'category': 'mac', 'title': 'MacBook Air M2',
        'vendor': 'APPLE', 'price': 22_500_000, 'old_price': None,
        'display_size': '13.6"', 'processor': 'Apple M2', 'internal_memory': '256 GB SSD',
        'camera': '1080p FaceTime HD', 'battery_info': '52.6 Wh',
        'color': 'Midnight', 'is_trending': True,
    },
    {
        'category': 'mac', 'title': 'MacBook Pro 14" M3',
        'vendor': 'APPLE', 'price': 38_900_000, 'old_price': None,
        'display_size': '14.2"', 'processor': 'Apple M3 Pro', 'internal_memory': '512 GB SSD',
        'camera': '12MP Center Stage', 'battery_info': '70 Wh',
        'color': 'Space Black', 'is_trending': True,
    },
    {
        'category': 'mac', 'title': 'iMac 24" M3',
        'vendor': 'APPLE', 'price': 35_000_000, 'old_price': None,
        'display_size': '24" Retina 4.5K', 'processor': 'Apple M3', 'internal_memory': '256 GB SSD',
        'camera': '12MP Center Stage', 'battery_info': 'Powered',
        'color': 'Blue', 'is_trending': False,
    },

    # --- iPad ---
    {
        'category': 'ipad', 'title': 'iPad Pro 12.9" M2',
        'vendor': 'APPLE', 'price': 28_000_000, 'old_price': None,
        'display_size': '12.9" Liquid Retina XDR', 'processor': 'Apple M2',
        'internal_memory': '256 GB', 'camera': '12MP Wide + 10MP Ultra Wide',
        'battery_info': '40.88 Wh', 'color': 'Space Gray', 'is_trending': True,
    },
    {
        'category': 'ipad', 'title': 'iPad Air M1',
        'vendor': 'APPLE', 'price': 14_500_000, 'old_price': 15_800_000,
        'display_size': '10.9" Liquid Retina', 'processor': 'Apple M1',
        'internal_memory': '64 GB', 'camera': '12MP Wide',
        'battery_info': '28.65 Wh', 'color': 'Starlight', 'is_trending': True,
    },

    # --- Samsung ---
    {
        'category': 'samsung', 'title': 'Samsung Galaxy S24 Ultra',
        'vendor': 'SAMSUNG', 'price': 16_500_000, 'old_price': 18_000_000,
        'display_size': '6.8" Dynamic AMOLED 2X', 'processor': 'Snapdragon 8 Gen 3',
        'internal_memory': '256 GB', 'camera': '200MP + 50MP + 12MP + 10MP',
        'battery_info': '5000 mAh', 'color': 'Titanium Black', 'is_trending': True,
    },
    {
        'category': 'samsung', 'title': 'Samsung Galaxy S23',
        'vendor': 'SAMSUNG', 'price': 11_200_000, 'old_price': 13_000_000,
        'display_size': '6.1" Dynamic AMOLED 2X', 'processor': 'Snapdragon 8 Gen 2',
        'internal_memory': '128 GB', 'camera': '50MP + 12MP + 10MP',
        'battery_info': '3900 mAh', 'color': 'Phantom Black', 'is_trending': True,
    },
    {
        'category': 'samsung', 'title': 'Samsung Galaxy Z Fold 5',
        'vendor': 'SAMSUNG', 'price': 24_800_000, 'old_price': None,
        'display_size': '7.6" Foldable AMOLED', 'processor': 'Snapdragon 8 Gen 2',
        'internal_memory': '512 GB', 'camera': '50MP + 10MP + 12MP',
        'battery_info': '4400 mAh', 'color': 'Icy Blue', 'is_trending': True,
    },

    # --- TV ---
    {
        'category': 'tv', 'title': 'Samsung 55" QLED 4K Q80C',
        'vendor': 'SAMSUNG', 'price': 13_400_000, 'old_price': 15_000_000,
        'display_size': '55" QLED 4K', 'processor': 'NQ4 AI Gen2',
        'internal_memory': None, 'camera': None,
        'battery_info': None, 'color': 'Black', 'is_trending': False,
    },
    {
        'category': 'tv', 'title': 'Apple TV 4K (3rd gen)',
        'vendor': 'APPLE', 'price': 3_800_000, 'old_price': None,
        'display_size': '4K HDR', 'processor': 'A15 Bionic',
        'internal_memory': '64 GB', 'camera': None,
        'battery_info': None, 'color': 'Black', 'is_trending': False,
    },
    {
        'category': 'tv', 'title': 'LG OLED C3 65"',
        'vendor': 'LG', 'price': 24_000_000, 'old_price': 27_000_000,
        'display_size': '65" OLED 4K', 'processor': 'α9 Gen6 AI',
        'internal_memory': None, 'camera': None,
        'battery_info': None, 'color': 'Black', 'is_trending': False,
    },
]

created_count = 0
for p in products_data:
    cat = cats[p['category']]
    exists = Product.objects.filter(title=p['title'], category=cat).exists()
    if exists:
        print(f"  [exists]  {p['title']}")
        continue
    Product.objects.create(
        category=cat,
        title=p['title'],
        vendor=p.get('vendor', ''),
        price=p['price'],
        old_price=p.get('old_price'),
        display_size=p.get('display_size', ''),
        processor=p.get('processor', ''),
        internal_memory=p.get('internal_memory', ''),
        camera=p.get('camera', ''),
        battery_info=p.get('battery_info', ''),
        color=p.get('color', ''),
        is_trending=p.get('is_trending', True),
        image=f"products/placeholder_{p['category']}.jpg",
    )
    created_count += 1
    print(f"  [created] {p['title']}")

print(f"\nOK! Done! {created_count} products added.")
print(f"  Total products: {Product.objects.count()}")
print(f"  Total categories: {Category.objects.count()}")
