from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
from models.models import (
    Jeweler, Product, Category, PaymentMethod, Order,
    DesignRequest, User, OrderStatus, DesignRequestStatus
)
from schemas import (
    JewelerCreate, JewelerUpdate, JewelerResponse,
    PaymentMethodCreate, PaymentMethodUpdate, PaymentMethodResponse,
    DesignRequestUpdate, DesignRequestResponse, OrderResponse
)

router = APIRouter(prefix="/api/admin", tags=["Admin"])

@router.post("/jewelers", response_model=JewelerResponse, status_code=status.HTTP_201_CREATED)
def create_jeweler(jeweler: JewelerCreate, db: Session = Depends(get_db)):
    existing = db.query(Jeweler).filter(Jeweler.email == jeweler.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_jeweler = Jeweler(**jeweler.dict())
    db.add(new_jeweler)
    db.commit()
    db.refresh(new_jeweler)
    return new_jeweler

@router.get("/jewelers", response_model=List[JewelerResponse])
def get_jewelers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Jeweler).offset(skip).limit(limit).all()

@router.get("/jewelers/{jeweler_id}", response_model=JewelerResponse)
def get_jeweler(jeweler_id: int, db: Session = Depends(get_db)):
    jeweler = db.query(Jeweler).filter(Jeweler.id == jeweler_id).first()
    if not jeweler:
        raise HTTPException(status_code=404, detail="Jeweler not found")
    return jeweler

@router.put("/jewelers/{jeweler_id}", response_model=JewelerResponse)
def update_jeweler(jeweler_id: int, jeweler: JewelerUpdate, db: Session = Depends(get_db)):
    db_jeweler = db.query(Jeweler).filter(Jeweler.id == jeweler_id).first()
    if not db_jeweler:
        raise HTTPException(status_code=404, detail="Jeweler not found")
    
    update_data = jeweler.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_jeweler, key, value)
    
    db.commit()
    db.refresh(db_jeweler)
    return db_jeweler

@router.delete("/jewelers/{jeweler_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_jeweler(jeweler_id: int, db: Session = Depends(get_db)):
    db_jeweler = db.query(Jeweler).filter(Jeweler.id == jeweler_id).first()
    if not db_jeweler:
        raise HTTPException(status_code=404, detail="Jeweler not found")
    db.delete(db_jeweler)
    db.commit()
    return None

@router.post("/payment-methods", response_model=PaymentMethodResponse, status_code=status.HTTP_201_CREATED)
def create_payment_method(method: PaymentMethodCreate, db: Session = Depends(get_db)):
    new_method = PaymentMethod(**method.dict())
    db.add(new_method)
    db.commit()
    db.refresh(new_method)
    return new_method

@router.get("/payment-methods", response_model=List[PaymentMethodResponse])
def get_payment_methods(db: Session = Depends(get_db)):
    return db.query(PaymentMethod).all()

@router.put("/payment-methods/{method_id}", response_model=PaymentMethodResponse)
def update_payment_method(method_id: int, method: PaymentMethodUpdate, db: Session = Depends(get_db)):
    db_method = db.query(PaymentMethod).filter(PaymentMethod.id == method_id).first()
    if not db_method:
        raise HTTPException(status_code=404, detail="Payment method not found")
    
    update_data = method.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_method, key, value)
    
    db.commit()
    db.refresh(db_method)
    return db_method

@router.delete("/payment-methods/{method_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_payment_method(method_id: int, db: Session = Depends(get_db)):
    db_method = db.query(PaymentMethod).filter(PaymentMethod.id == method_id).first()
    if not db_method:
        raise HTTPException(status_code=404, detail="Payment method not found")
    db.delete(db_method)
    db.commit()
    return None

@router.get("/orders", response_model=List[OrderResponse])
def get_all_orders(
    status_filter: OrderStatus = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(Order)
    if status_filter:
        query = query.filter(Order.status == status_filter)
    return query.offset(skip).limit(limit).all()

@router.put("/orders/{order_id}/status", response_model=OrderResponse)
def update_order_status(
    order_id: int,
    new_status: OrderStatus,
    db: Session = Depends(get_db)
):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    order.status = new_status
    db.commit()
    db.refresh(order)
    return order

@router.get("/design-requests", response_model=List[DesignRequestResponse])
def get_design_requests(
    status_filter: DesignRequestStatus = None,
    jeweler_id: int = None,
    db: Session = Depends(get_db)
):
    query = db.query(DesignRequest)
    if status_filter:
        query = query.filter(DesignRequest.status == status_filter)
    if jeweler_id:
        query = query.filter(DesignRequest.jeweler_id == jeweler_id)
    return query.all()

@router.put("/design-requests/{request_id}", response_model=DesignRequestResponse)
def update_design_request(
    request_id: int,
    update_data: DesignRequestUpdate,
    db: Session = Depends(get_db)
):
    design_request = db.query(DesignRequest).filter(DesignRequest.id == request_id).first()
    if not design_request:
        raise HTTPException(status_code=404, detail="Design request not found")
    
    update_dict = update_data.dict(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(design_request, key, value)
    
    db.commit()
    db.refresh(design_request)
    return design_request

@router.get("/users", response_model=List[dict])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    return [{"id": u.id, "username": u.username, "email": u.email, "created_at": u.created_at} for u in users]

@router.get("/dashboard/stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    total_users = db.query(User).count()
    total_jewelers = db.query(Jeweler).count()
    total_products = db.query(Product).count()
    total_orders = db.query(Order).count()
    total_revenue = db.query(Order).filter(Order.status != OrderStatus.cancelled).with_entities(
        func.sum(Order.total_amount)
    ).scalar() or 0
    
    return {
        "total_users": total_users,
        "total_jewelers": total_jewelers,
        "total_products": total_products,
        "total_orders": total_orders,
        "total_revenue": total_revenue
    }
