from .auth import router as auth_router
from .products import router as products_router
from .cart import router as cart_router
from .orders import router as orders_router
from .admin import router as admin_router
from .ai import router as ai_router

__all__ = [
    'auth_router',
    'products_router',
    'cart_router',
    'orders_router',
    'admin_router',
    'ai_router'
]
