from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
import os
import uuid
from database import get_db
from models.models import Order, OrderItem, Cart, CartItem, PaymentMethod, User, OrderStatus
from schemas import OrderCreate, OrderResponse, OrderUpdate
from auth import get_current_active_user

router = APIRouter(prefix="/api/orders", tags=["Orders"])

UPLOAD_DIR = "static/receipts"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.get("/", response_model=List[OrderResponse])
def get_orders(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    orders = db.query(Order).filter(Order.user_id == current_user.id).all()
    return orders

@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == current_user.id
    ).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(
    order: OrderCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if not cart or not cart.items:
        raise HTTPException(status_code=400, detail="Cart is empty")
    
    payment_method = db.query(PaymentMethod).filter(
        PaymentMethod.id == order.payment_method_id,
        PaymentMethod.is_active == True
    ).first()
    if not payment_method:
        raise HTTPException(status_code=404, detail="Payment method not found or inactive")
    
    for item in cart.items:
        if item.product.stock_quantity < item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Not enough stock for product: {item.product.name}"
            )
    
    total_amount = sum(item.product.price * item.quantity for item in cart.items)
    
    new_order = Order(
        user_id=current_user.id,
        payment_method_id=order.payment_method_id,
        total_amount=total_amount,
        shipping_address=order.shipping_address,
        transfer_receipt=order.transfer_receipt
    )
    db.add(new_order)
    db.flush()
    
    for item in cart.items:
        order_item = OrderItem(
            order_id=new_order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=item.product.price,
            subtotal=item.product.price * item.quantity
        )
        db.add(order_item)
        
        item.product.stock_quantity -= item.quantity
    
    db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()
    
    db.commit()
    db.refresh(new_order)
    return new_order

@router.put("/{order_id}", response_model=OrderResponse)
def update_order(
    order_id: int,
    order_update: OrderUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == current_user.id
    ).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    if order.status != OrderStatus.pending:
        raise HTTPException(status_code=400, detail="Cannot update order that is already processed")
    
    if order_update.transfer_receipt:
        order.transfer_receipt = order_update.transfer_receipt
    
    db.commit()
    db.refresh(order)
    return order

@router.post("/{order_id}/upload-receipt")
async def upload_receipt(
    order_id: int,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == current_user.id
    ).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    file_extension = os.path.splitext(file.filename)[1]
    file_name = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, file_name)
    
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    order.transfer_receipt = file_path
    db.commit()
    
    return {"message": "Receipt uploaded", "path": file_path}
