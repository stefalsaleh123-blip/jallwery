from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
import os
import uuid
from database import get_db
from models.models import Product, ProductImage, Category, Jeweler
from schemas import (
    ProductCreate, ProductUpdate, ProductResponse,
    CategoryCreate, CategoryUpdate, CategoryResponse, CategoryWithSubcategories,
    ProductImageCreate, ProductImageResponse
)

router = APIRouter(prefix="/api/products", tags=["Products"])

UPLOAD_DIR = "static/products"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.get("/", response_model=List[ProductResponse])
def get_products(
    skip: int = 0,
    limit: int = 100,
    category_id: Optional[int] = None,
    material: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    jeweler_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Product)
    
    if category_id:
        query = query.join(Product.categories).filter(Category.id == category_id)
    if material:
        query = query.filter(Product.material.ilike(f"%{material}%"))
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)
    if jeweler_id:
        query = query.filter(Product.jeweler_id == jeweler_id)
    
    products = query.offset(skip).limit(limit).all()
    return products

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    jeweler = db.query(Jeweler).filter(Jeweler.id == product.jeweler_id).first()
    if not jeweler:
        raise HTTPException(status_code=404, detail="Jeweler not found")
    
    new_product = Product(
        name=product.name,
        material=product.material,
        karat=product.karat,
        weight=product.weight,
        price=product.price,
        stock_quantity=product.stock_quantity,
        description=product.description,
        image_path=product.image_path,
        jeweler_id=product.jeweler_id
    )
    
    if product.category_ids:
        categories = db.query(Category).filter(Category.id.in_(product.category_ids)).all()
        new_product.categories = categories
    
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product: ProductUpdate,
    db: Session = Depends(get_db)
):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    update_data = product.dict(exclude_unset=True, exclude={"category_ids"})
    for key, value in update_data.items():
        setattr(db_product, key, value)
    
    if product.category_ids is not None:
        categories = db.query(Category).filter(Category.id.in_(product.category_ids)).all()
        db_product.categories = categories
    
    db.commit()
    db.refresh(db_product)
    return db_product

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(db_product)
    db.commit()
    return None

@router.post("/{product_id}/images", response_model=ProductImageResponse, status_code=status.HTTP_201_CREATED)
async def upload_product_image(
    product_id: int,
    file: UploadFile = File(...),
    display_order: int = 0,
    db: Session = Depends(get_db)
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    file_extension = os.path.splitext(file.filename)[1]
    file_name = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, file_name)
    
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    image = ProductImage(
        product_id=product_id,
        image_path=file_path,
        display_order=display_order
    )
    db.add(image)
    db.commit()
    db.refresh(image)
    return image

@router.get("/categories/", response_model=List[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()

@router.get("/categories/{category_id}", response_model=CategoryWithSubcategories)
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.post("/categories/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    if category.parent_id:
        parent = db.query(Category).filter(Category.id == category.parent_id).first()
        if not parent:
            raise HTTPException(status_code=404, detail="Parent category not found")
    
    new_category = Category(
        name=category.name,
        parent_id=category.parent_id
    )
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

@router.put("/categories/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int,
    category: CategoryUpdate,
    db: Session = Depends(get_db)
):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    update_data = category.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_category, key, value)
    
    db.commit()
    db.refresh(db_category)
    return db_category

@router.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(db_category)
    db.commit()
    return None
