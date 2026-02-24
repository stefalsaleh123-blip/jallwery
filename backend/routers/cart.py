from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.models import Cart, CartItem, Product, User
from schemas import CartItemCreate, CartItemUpdate, CartResponse
from auth import get_current_active_user

router = APIRouter(prefix="/api/cart", tags=["Cart"])

@router.get("/", response_model=CartResponse)
def get_cart(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if not cart:
        cart = Cart(user_id=current_user.id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    
    total = sum(item.product.price * item.quantity for item in cart.items)
    return CartResponse(
        id=cart.id,
        user_id=cart.user_id,
        updated_at=cart.updated_at,
        items=cart.items,
        total=total
    )

@router.post("/items", status_code=status.HTTP_201_CREATED)
def add_to_cart(
    item: CartItemCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    product = db.query(Product).filter(Product.id == item.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    if product.stock_quantity < item.quantity:
        raise HTTPException(status_code=400, detail="Not enough stock")
    
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if not cart:
        cart = Cart(user_id=current_user.id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    
    existing_item = db.query(CartItem).filter(
        CartItem.cart_id == cart.id,
        CartItem.product_id == item.product_id
    ).first()
    
    if existing_item:
        existing_item.quantity += item.quantity
    else:
        cart_item = CartItem(
            cart_id=cart.id,
            product_id=item.product_id,
            quantity=item.quantity
        )
        db.add(cart_item)
    
    db.commit()
    return {"message": "Item added to cart"}

@router.put("/items/{item_id}")
def update_cart_item(
    item_id: int,
    item: CartItemUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    
    cart_item = db.query(CartItem).filter(
        CartItem.id == item_id,
        CartItem.cart_id == cart.id
    ).first()
    
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    
    if cart_item.product.stock_quantity < item.quantity:
        raise HTTPException(status_code=400, detail="Not enough stock")
    
    cart_item.quantity = item.quantity
    db.commit()
    return {"message": "Cart item updated"}

@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_from_cart(
    item_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    
    cart_item = db.query(CartItem).filter(
        CartItem.id == item_id,
        CartItem.cart_id == cart.id
    ).first()
    
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    
    db.delete(cart_item)
    db.commit()
    return None

@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def clear_cart(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if cart:
        db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()
        db.commit()
    return None
