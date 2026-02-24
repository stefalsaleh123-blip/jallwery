from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from models.models import OrderStatus, DesignRequestStatus

class JewelerBase(BaseModel):
    name: str
    shop_name: str
    bio: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: str

class JewelerCreate(JewelerBase):
    pass

class JewelerUpdate(BaseModel):
    name: Optional[str] = None
    shop_name: Optional[str] = None
    bio: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    rating: Optional[float] = None

class JewelerResponse(JewelerBase):
    id: int
    rating: float
    created_at: datetime
    
    class Config:
        from_attributes = True

class PaymentMethodBase(BaseModel):
    method_name: str
    qr_code_image: Optional[str] = None
    is_active: bool = True
    notes: Optional[str] = None

class PaymentMethodCreate(PaymentMethodBase):
    pass

class PaymentMethodUpdate(BaseModel):
    method_name: Optional[str] = None
    qr_code_image: Optional[str] = None
    is_active: Optional[bool] = None
    notes: Optional[str] = None

class PaymentMethodResponse(PaymentMethodBase):
    id: int
    
    class Config:
        from_attributes = True

class CategoryBase(BaseModel):
    name: str
    parent_id: Optional[int] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    parent_id: Optional[int] = None

class CategoryResponse(CategoryBase):
    id: int
    
    class Config:
        from_attributes = True

class CategoryWithSubcategories(CategoryResponse):
    subcategories: List['CategoryResponse'] = []

class ProductImageBase(BaseModel):
    image_path: str
    display_order: int = 0

class ProductImageCreate(ProductImageBase):
    pass

class ProductImageResponse(ProductImageBase):
    id: int
    product_id: int
    
    class Config:
        from_attributes = True

class ProductBase(BaseModel):
    name: str
    material: Optional[str] = None
    karat: Optional[str] = None
    weight: Optional[float] = None
    price: float
    stock_quantity: int = 0
    description: Optional[str] = None
    image_path: Optional[str] = None
    jeweler_id: int

class ProductCreate(ProductBase):
    category_ids: List[int] = []

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    material: Optional[str] = None
    karat: Optional[str] = None
    weight: Optional[float] = None
    price: Optional[float] = None
    stock_quantity: Optional[int] = None
    description: Optional[str] = None
    image_path: Optional[str] = None
    category_ids: Optional[List[int]] = None

class ProductResponse(ProductBase):
    id: int
    images: List[ProductImageResponse] = []
    categories: List[CategoryResponse] = []
    
    class Config:
        from_attributes = True

class CartItemBase(BaseModel):
    product_id: int
    quantity: int = 1

class CartItemCreate(CartItemBase):
    pass

class CartItemUpdate(BaseModel):
    quantity: int

class CartItemResponse(CartItemBase):
    id: int
    cart_id: int
    product: ProductResponse
    
    class Config:
        from_attributes = True

class CartResponse(BaseModel):
    id: int
    user_id: int
    updated_at: datetime
    items: List[CartItemResponse] = []
    total: float = 0
    
    class Config:
        from_attributes = True

class OrderItemBase(BaseModel):
    product_id: int
    quantity: int = 1
    unit_price: float
    subtotal: float

class OrderItemResponse(OrderItemBase):
    id: int
    order_id: int
    
    class Config:
        from_attributes = True

class OrderBase(BaseModel):
    payment_method_id: int
    shipping_address: str
    transfer_receipt: Optional[str] = None

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    status: Optional[OrderStatus] = None
    transfer_receipt: Optional[str] = None

class OrderResponse(OrderBase):
    id: int
    user_id: int
    order_date: datetime
    status: OrderStatus
    total_amount: float
    items: List[OrderItemResponse] = []
    
    class Config:
        from_attributes = True

class UserGeneratedDesignBase(BaseModel):
    selected_options: dict
    generated_image_url: Optional[str] = None
    user_id: Optional[int] = None

class UserGeneratedDesignCreate(BaseModel):
    type: str
    color: str
    shape: str
    material: str
    karat: str
    gemstone_type: str
    gemstone_color: str

class UserGeneratedDesignResponse(BaseModel):
    id: int
    selected_options: dict
    generated_image_url: Optional[str] = None
    created_at: datetime
    user_id: Optional[int] = None
    
    class Config:
        from_attributes = True

class DesignRequestBase(BaseModel):
    jeweler_id: Optional[int] = None
    generated_design_id: Optional[int] = None
    description: str
    attachment_url: Optional[str] = None
    estimated_budget: Optional[float] = None

class DesignRequestCreate(DesignRequestBase):
    pass

class DesignRequestUpdate(BaseModel):
    jeweler_id: Optional[int] = None
    description: Optional[str] = None
    attachment_url: Optional[str] = None
    estimated_budget: Optional[float] = None
    jeweler_price_offer: Optional[float] = None
    status: Optional[DesignRequestStatus] = None

class DesignRequestResponse(DesignRequestBase):
    id: int
    user_id: int
    request_date: datetime
    jeweler_price_offer: Optional[float] = None
    status: DesignRequestStatus
    
    class Config:
        from_attributes = True
