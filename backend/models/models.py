from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey, Enum, JSON, Boolean, Table
from sqlalchemy.orm import relationship
from database import Base
import enum

class OrderStatus(enum.Enum):
    pending = "pending"
    confirmed = "confirmed"
    processing = "processing"
    shipped = "shipped"
    delivered = "delivered"
    cancelled = "cancelled"

class DesignRequestStatus(enum.Enum):
    pending = "pending"
    reviewed = "reviewed"
    quoted = "quoted"
    accepted = "accepted"
    rejected = "rejected"
    completed = "completed"

class Gender(enum.Enum):
    male = "male"
    female = "female"
    other = "other"

product_categories = Table(
    'product_categories',
    Base.metadata,
    Column('product_id', Integer, ForeignKey('products.id'), primary_key=True),
    Column('category_id', Integer, ForeignKey('categories.id'), primary_key=True)
)

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    first_name = Column(String(50))
    last_name = Column(String(50))
    phone = Column(String(20))
    dob = Column(DateTime, nullable=True)
    gender = Column(Enum(Gender), nullable=True)
    address = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    cart = relationship("Cart", back_populates="user", uselist=False)
    orders = relationship("Order", back_populates="user")
    generated_designs = relationship("UserGeneratedDesign", back_populates="user")
    design_requests = relationship("DesignRequest", back_populates="user")

class Jeweler(Base):
    __tablename__ = "jewelers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    shop_name = Column(String(100), nullable=False)
    bio = Column(Text)
    address = Column(Text)
    phone = Column(String(20))
    email = Column(String(100), unique=True, index=True)
    rating = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    products = relationship("Product", back_populates="jeweler")
    design_requests = relationship("DesignRequest", back_populates="jeweler")

class PaymentMethod(Base):
    __tablename__ = "payment_methods"
    
    id = Column(Integer, primary_key=True, index=True)
    method_name = Column(String(100), nullable=False)
    qr_code_image = Column(String(255))
    is_active = Column(Boolean, default=True)
    notes = Column(Text)
    
    orders = relationship("Order", back_populates="payment_method")

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    parent_id = Column(Integer, ForeignKey('categories.id'), nullable=True)
    
    parent = relationship("Category", remote_side=[id], backref="subcategories")
    products = relationship("Product", secondary=product_categories, back_populates="categories")

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    jeweler_id = Column(Integer, ForeignKey('jewelers.id'), nullable=False)
    name = Column(String(200), nullable=False)
    material = Column(String(50))
    karat = Column(String(10))
    weight = Column(Float)
    price = Column(Float, nullable=False)
    stock_quantity = Column(Integer, default=0)
    description = Column(Text)
    image_path = Column(String(255))
    
    jeweler = relationship("Jeweler", back_populates="products")
    categories = relationship("Category", secondary=product_categories, back_populates="products")
    images = relationship("ProductImage", back_populates="product", cascade="all, delete-orphan")
    cart_items = relationship("CartItem", back_populates="product")
    order_items = relationship("OrderItem", back_populates="product")

class ProductImage(Base):
    __tablename__ = "product_images"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    image_path = Column(String(255), nullable=False)
    display_order = Column(Integer, default=0)
    
    product = relationship("Product", back_populates="images")

class Cart(Base):
    __tablename__ = "carts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", back_populates="cart")
    items = relationship("CartItem", back_populates="cart", cascade="all, delete-orphan")

class CartItem(Base):
    __tablename__ = "cart_items"
    
    id = Column(Integer, primary_key=True, index=True)
    cart_id = Column(Integer, ForeignKey('carts.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, default=1)
    
    cart = relationship("Cart", back_populates="items")
    product = relationship("Product", back_populates="cart_items")

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    payment_method_id = Column(Integer, ForeignKey('payment_methods.id'), nullable=False)
    order_date = Column(DateTime, default=datetime.utcnow)
    status = Column(Enum(OrderStatus), default=OrderStatus.pending)
    total_amount = Column(Float, nullable=False)
    shipping_address = Column(Text)
    transfer_receipt = Column(String(255))
    
    user = relationship("User", back_populates="orders")
    payment_method = relationship("PaymentMethod", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

class OrderItem(Base):
    __tablename__ = "order_items"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, default=1)
    unit_price = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)
    
    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")

class UserGeneratedDesign(Base):
    __tablename__ = "user_generated_designs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    selected_options = Column(JSON)
    generated_image_url = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="generated_designs")
    design_requests = relationship("DesignRequest", back_populates="generated_design")

class DesignRequest(Base):
    __tablename__ = "design_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    jeweler_id = Column(Integer, ForeignKey('jewelers.id'), nullable=True)
    generated_design_id = Column(Integer, ForeignKey('user_generated_designs.id'), nullable=True)
    request_date = Column(DateTime, default=datetime.utcnow)
    description = Column(Text)
    attachment_url = Column(String(255))
    estimated_budget = Column(Float)
    jeweler_price_offer = Column(Float, nullable=True)
    status = Column(Enum(DesignRequestStatus), default=DesignRequestStatus.pending)
    
    user = relationship("User", back_populates="design_requests")
    jeweler = relationship("Jeweler", back_populates="design_requests")
    generated_design = relationship("UserGeneratedDesign", back_populates="design_requests")
