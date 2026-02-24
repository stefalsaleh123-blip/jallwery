from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from database import engine, Base
from routers import (
    auth_router, products_router, cart_router,
    orders_router, admin_router, ai_router
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Jewelry E-commerce & AI Design Platform",
    description="A complete backend API for jewelry e-commerce with AI-powered design generation",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

static_dir = "static"
if not os.path.exists(static_dir):
    os.makedirs(static_dir)
    os.makedirs(os.path.join(static_dir, "generated_designs"))
    os.makedirs(os.path.join(static_dir, "products"))
    os.makedirs(os.path.join(static_dir, "qrcodes"))
    os.makedirs(os.path.join(static_dir, "receipts"))

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(auth_router)
app.include_router(products_router)
app.include_router(cart_router)
app.include_router(orders_router)
app.include_router(admin_router)
app.include_router(ai_router)

@app.get("/")
def root():
    return {
        "message": "Welcome to Jewelry E-commerce & AI Design Platform API",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
