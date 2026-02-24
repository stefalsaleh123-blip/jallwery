import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime
from database import engine, SessionLocal, Base
from models.models import (
    User, Jeweler, Category, PaymentMethod, Product, ProductImage,
    Gender
)
from auth import get_password_hash

def clear_database():
    print("Clearing existing data...")
    db = SessionLocal()
    try:
        db.query(Product).delete()
        db.query(Category).delete()
        db.query(PaymentMethod).delete()
        db.query(Jeweler).delete()
        db.query(User).delete()
        db.commit()
        print("Database cleared successfully!")
    except Exception as e:
        print(f"Error clearing database: {e}")
        db.rollback()
    finally:
        db.close()

def seed_jewelers(db):
    print("Seeding jewelers...")
    jewelers = [
        Jeweler(
            name="Ahmed Al-Ghazali",
            shop_name="Golden Dreams Jewelry",
            bio="Master jeweler with 25 years of experience in handcrafted gold and diamond jewelry. Specializing in traditional Arabic designs with modern elegance.",
            address="123 Gold Street, Jewelry District, Riyadh",
            phone="+966-50-123-4567",
            email="ahmed@goldendreams.com",
            rating=4.9
        ),
        Jeweler(
            name="Fatima Al-Hassan",
            shop_name="Silver Moon Creations",
            bio="Award-winning designer specializing in contemporary silver jewelry. Known for unique gemstone combinations and minimalist aesthetics.",
            address="456 Silver Avenue, Artisan Quarter, Jeddah",
            phone="+966-55-234-5678",
            email="fatima@silvermoon.com",
            rating=4.8
        ),
        Jeweler(
            name="Omar Ibn Khalid",
            shop_name="Royal Gems Palace",
            bio="Luxury jeweler catering to elite clientele. Expert in rare gemstones, custom engagement rings, and investment-grade jewelry pieces.",
            address="789 Diamond Boulevard, Luxury Lane, Dammam",
            phone="+966-56-345-6789",
            email="omar@royalgems.com",
            rating=4.7
        )
    ]
    
    for jeweler in jewelers:
        db.add(jeweler)
    db.commit()
    print(f"Added {len(jewelers)} jewelers.")
    return jewelers

def seed_users(db):
    print("Seeding users...")
    users = [
        User(
            username="john_doe",
            email="john@example.com",
            password=get_password_hash("password123"),
            first_name="John",
            last_name="Doe",
            phone="+1-555-0101",
            dob=datetime(1990, 5, 15),
            gender=Gender.male,
            address="123 Main Street, New York, NY 10001"
        ),
        User(
            username="jane_smith",
            email="jane@example.com",
            password=get_password_hash("password123"),
            first_name="Jane",
            last_name="Smith",
            phone="+1-555-0102",
            dob=datetime(1988, 8, 22),
            gender=Gender.female,
            address="456 Oak Avenue, Los Angeles, CA 90001"
        ),
        User(
            username="mohammed_ali",
            email="mohammed@example.com",
            password=get_password_hash("password123"),
            first_name="Mohammed",
            last_name="Ali",
            phone="+966-50-111-2222",
            dob=datetime(1985, 3, 10),
            gender=Gender.male,
            address="789 Palm Street, Riyadh, Saudi Arabia"
        ),
        User(
            username="sara_ahmed",
            email="sara@example.com",
            password=get_password_hash("password123"),
            first_name="Sara",
            last_name="Ahmed",
            phone="+966-55-333-4444",
            dob=datetime(1992, 11, 28),
            gender=Gender.female,
            address="321 Desert Rose Lane, Jeddah, Saudi Arabia"
        ),
        User(
            username="khalid_hassan",
            email="khalid@example.com",
            password=get_password_hash("password123"),
            first_name="Khalid",
            last_name="Hassan",
            phone="+966-56-555-6666",
            dob=datetime(1995, 7, 4),
            gender=Gender.male,
            address="654 Oasis Boulevard, Dammam, Saudi Arabia"
        )
    ]
    
    for user in users:
        db.add(user)
    db.commit()
    print(f"Added {len(users)} users.")
    return users

def seed_categories(db):
    print("Seeding categories...")
    
    rings = Category(name="Rings", parent_id=None)
    db.add(rings)
    db.flush()
    
    rings_subcats = [
        Category(name="Engagement Rings", parent_id=rings.id),
        Category(name="Wedding Bands", parent_id=rings.id),
        Category(name="Fashion Rings", parent_id=rings.id),
        Category(name="Statement Rings", parent_id=rings.id)
    ]
    for cat in rings_subcats:
        db.add(cat)
    
    necklaces = Category(name="Necklaces", parent_id=None)
    db.add(necklaces)
    db.flush()
    
    necklaces_subcats = [
        Category(name="Pendant Necklaces", parent_id=necklaces.id),
        Category(name="Chain Necklaces", parent_id=necklaces.id),
        Category(name="Chokers", parent_id=necklaces.id),
        Category(name="Statement Necklaces", parent_id=necklaces.id)
    ]
    for cat in necklaces_subcats:
        db.add(cat)
    
    bracelets = Category(name="Bracelets", parent_id=None)
    db.add(bracelets)
    db.flush()
    
    bracelets_subcats = [
        Category(name="Tennis Bracelets", parent_id=bracelets.id),
        Category(name="Bangles", parent_id=bracelets.id),
        Category(name="Charm Bracelets", parent_id=bracelets.id),
        Category(name="Cuff Bracelets", parent_id=bracelets.id)
    ]
    for cat in bracelets_subcats:
        db.add(cat)
    
    db.commit()
    print("Added categories with subcategories.")
    
    all_categories = db.query(Category).all()
    return all_categories

def seed_payment_methods(db):
    print("Seeding payment methods...")
    payment_methods = [
        PaymentMethod(
            method_name="Bank Transfer",
            qr_code_image="static/qrcodes/bank_transfer_qr.png",
            is_active=True,
            notes="Transfer to our bank account. Please include your order number in the reference."
        ),
        PaymentMethod(
            method_name="Cash on Delivery",
            qr_code_image=None,
            is_active=True,
            notes="Pay with cash upon delivery. Available in select areas only."
        )
    ]
    
    for method in payment_methods:
        db.add(method)
    db.commit()
    print(f"Added {len(payment_methods)} payment methods.")
    return payment_methods

def seed_products(db, jewelers, categories):
    print("Seeding products...")
    
    rings_cat = db.query(Category).filter(Category.name == "Rings").first()
    engagement_cat = db.query(Category).filter(Category.name == "Engagement Rings").first()
    necklaces_cat = db.query(Category).filter(Category.name == "Necklaces").first()
    pendant_cat = db.query(Category).filter(Category.name == "Pendant Necklaces").first()
    bracelets_cat = db.query(Category).filter(Category.name == "Bracelets").first()
    tennis_cat = db.query(Category).filter(Category.name == "Tennis Bracelets").first()
    bangles_cat = db.query(Category).filter(Category.name == "Bangles").first()
    fashion_cat = db.query(Category).filter(Category.name == "Fashion Rings").first()
    chain_cat = db.query(Category).filter(Category.name == "Chain Necklaces").first()
    
    products = [
        Product(
            jeweler_id=jewelers[0].id,
            name="Royal Diamond Engagement Ring",
            material="Gold",
            karat="18k",
            weight=5.2,
            price=4999.99,
            stock_quantity=5,
            description="A stunning 18k gold engagement ring featuring a brilliant 1.5 carat diamond center stone surrounded by smaller accent diamonds. Perfect for the special moment.",
            image_path="static/products/ring1.jpg"
        ),
        Product(
            jeweler_id=jewelers[0].id,
            name="Classic Wedding Band Set",
            material="Gold",
            karat="21k",
            weight=12.5,
            price=2499.99,
            stock_quantity=10,
            description="Traditional 21k gold wedding band set with elegant brushed finish. His and hers matching design symbolizing eternal love.",
            image_path="static/products/ring2.jpg"
        ),
        Product(
            jeweler_id=jewelers[1].id,
            name="Moonlight Silver Pendant",
            material="Silver",
            karat="925",
            weight=8.3,
            price=349.99,
            stock_quantity=25,
            description="Handcrafted sterling silver pendant featuring a crescent moon design with tiny sapphire accents. Comes with a 20-inch silver chain.",
            image_path="static/products/pendant1.jpg"
        ),
        Product(
            jeweler_id=jewelers[1].id,
            name="Minimalist Silver Chain",
            material="Silver",
            karat="925",
            weight=15.0,
            price=199.99,
            stock_quantity=30,
            description="Elegant sterling silver rope chain, perfect for everyday wear. 24 inches length with secure lobster clasp.",
            image_path="static/products/chain1.jpg"
        ),
        Product(
            jeweler_id=jewelers[2].id,
            name="Diamond Tennis Bracelet",
            material="Gold",
            karat="18k",
            weight=18.5,
            price=8999.99,
            stock_quantity=3,
            description="Luxurious 18k white gold tennis bracelet featuring 50 round-cut diamonds totaling 5 carats. Certified quality with exceptional brilliance.",
            image_path="static/products/bracelet1.jpg"
        ),
        Product(
            jeweler_id=jewelers[2].id,
            name="Ruby Statement Ring",
            material="Gold",
            karat="18k",
            weight=7.8,
            price=3499.99,
            stock_quantity=4,
            description="Bold 18k rose gold statement ring featuring a 2-carat Burmese ruby surrounded by brilliant cut diamonds. A true conversation piece.",
            image_path="static/products/ring3.jpg"
        ),
        Product(
            jeweler_id=jewelers[0].id,
            name="Emerald Drop Necklace",
            material="Gold",
            karat="21k",
            weight=22.0,
            price=7499.99,
            stock_quantity=2,
            description="Exquisite 21k yellow gold necklace featuring three graduated Colombian emeralds totaling 3 carats, accented with diamond halos.",
            image_path="static/products/necklace1.jpg"
        ),
        Product(
            jeweler_id=jewelers[1].id,
            name="Silver Infinity Bangle",
            material="Silver",
            karat="925",
            weight=25.0,
            price=279.99,
            stock_quantity=20,
            description="Beautiful sterling silver infinity bangle with polished finish. Adjustable size to fit most wrists. Perfect gift for loved ones.",
            image_path="static/products/bangle1.jpg"
        ),
        Product(
            jeweler_id=jewelers[2].id,
            name="Sapphire Halo Ring",
            material="Gold",
            karat="18k",
            weight=4.5,
            price=2999.99,
            stock_quantity=6,
            description="Elegant 18k white gold ring featuring a 1-carat Ceylon sapphire surrounded by a halo of brilliant diamonds. Timeless beauty.",
            image_path="static/products/ring4.jpg"
        ),
        Product(
            jeweler_id=jewelers[0].id,
            name="Pearl Strand Necklace",
            material="Gold",
            karat="14k",
            weight=35.0,
            price=1999.99,
            stock_quantity=8,
            description="Classic 18-inch strand of AA grade freshwater pearls with 14k yellow gold clasp. Perfect for formal occasions and bridal wear.",
            image_path="static/products/necklace2.jpg"
        )
    ]
    
    for product in products:
        db.add(product)
    db.flush()
    
    products[0].categories = [rings_cat, engagement_cat]
    products[1].categories = [rings_cat]
    products[2].categories = [necklaces_cat, pendant_cat]
    products[3].categories = [necklaces_cat, chain_cat]
    products[4].categories = [bracelets_cat, tennis_cat]
    products[5].categories = [rings_cat, fashion_cat]
    products[6].categories = [necklaces_cat, pendant_cat]
    products[7].categories = [bracelets_cat, bangles_cat]
    products[8].categories = [rings_cat, fashion_cat]
    products[9].categories = [necklaces_cat]
    
    db.commit()
    print(f"Added {len(products)} products.")
    return products

def main():
    print("=" * 50)
    print("Jewelry E-commerce Database Seeder")
    print("=" * 50)
    
    Base.metadata.create_all(bind=engine)
    
    clear_database()
    
    db = SessionLocal()
    
    try:
        jewelers = seed_jewelers(db)
        users = seed_users(db)
        categories = seed_categories(db)
        payment_methods = seed_payment_methods(db)
        products = seed_products(db, jewelers, categories)
        
        print("\n" + "=" * 50)
        print("Database seeding completed successfully!")
        print("=" * 50)
        print("\nSummary:")
        print(f"- Jewelers: 3")
        print(f"- Users: 5")
        print(f"- Categories: 3 main + subcategories")
        print(f"- Payment Methods: 2")
        print(f"- Products: 10")
        print("\nTest User Credentials:")
        print("- Username: john_doe, Password: password123")
        print("- Username: jane_smith, Password: password123")
        print("=" * 50)
        
    except Exception as e:
        print(f"Error during seeding: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()
