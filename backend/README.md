# Jewelry E-commerce & AI Design Platform - Backend

A complete FastAPI backend for a Jewelry E-commerce platform with AI-powered jewelry design generation using Google Gemini API.

## Table of Contents

1. [Technology Stack](#technology-stack)
2. [Project Structure](#project-structure)
3. [Setup Instructions](#setup-instructions)
4. [Running the Application](#running-the-application)
5. [API Endpoints](#api-endpoints)
6. [Frontend Integration Guide](#frontend-integration-guide)
7. [Database Schema](#database-schema)

## Technology Stack

- **Framework**: FastAPI (Python 3.8+)
- **Database**: MySQL (XAMPP)
- **ORM**: SQLAlchemy with Pydantic
- **Authentication**: JWT (python-jose)
- **AI Integration**: Google Gemini API
- **Password Hashing**: bcrypt (passlib)

## Project Structure

```
backend/
├── main.py                 # FastAPI application entry point
├── config.py               # Configuration settings
├── database.py             # Database connection and session
├── auth.py                 # Authentication utilities
├── seeder.py               # Database seeder
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variables template
├── models/
│   ├── __init__.py
│   └── models.py           # SQLAlchemy database models
├── schemas/
│   ├── __init__.py
│   ├── user.py             # User Pydantic schemas
│   └── schemas.py          # All other schemas
├── routers/
│   ├── __init__.py
│   ├── auth.py             # Authentication routes
│   ├── products.py         # Products and categories routes
│   ├── cart.py             # Shopping cart routes
│   ├── orders.py           # Order management routes
│   ├── admin.py            # Admin dashboard routes
│   └── ai.py               # AI design generation routes
└── static/
    ├── generated_designs/  # AI-generated jewelry images
    ├── products/           # Product images
    ├── qrcodes/            # Payment QR codes
    └── receipts/           # Payment receipts
```

## Setup Instructions

### 1. Install XAMPP and Setup MySQL

1. Download and install XAMPP from [https://www.apachefriends.org/](https://www.apachefriends.org/)
2. Open XAMPP Control Panel
3. Start the **Apache** and **MySQL** modules
4. Click on "Admin" for MySQL or go to [http://localhost/phpmyadmin](http://localhost/phpmyadmin)
5. Create a new database named `jewelry_db`:
   - Click on "New" in the left sidebar
   - Enter database name: `jewelry_db`
   - Click "Create"

### 2. Clone and Setup the Project

```bash
# Navigate to the backend directory
cd backend

# Create a virtual environment (optional but recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment Variables

1. Copy the `.env.example` file to `.env`:
   ```bash
   copy .env.example .env
   ```

2. Edit the `.env` file with your configuration:
   ```env
   DATABASE_URL=mysql+pymysql://root:@localhost:3306/jewelry_db
   GEMINI_API_KEY=your_actual_gemini_api_key_here
   SECRET_KEY=your_super_secret_key_change_in_production
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

   **To get a Gemini API Key:**
   - Go to [https://makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)
   - Sign in with your Google account
   - Click "Create API key"
   - Copy the key and paste it in your `.env` file

### 4. Run the Database Seeder

```bash
python seeder.py
```

This will create all tables and populate them with sample data:
- 3 Jewelers
- 5 Users
- 3 Main Categories with subcategories
- 2 Payment Methods
- 10 Products

## Running the Application

### Start the FastAPI Server

```bash
# Development mode with auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Or simply run
python main.py
```

The API will be available at: [http://localhost:8000](http://localhost:8000)

### Access API Documentation

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## API Endpoints

### Authentication (`/api/auth`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/register` | Register a new user |
| POST | `/login` | Login and get JWT token |
| GET | `/me` | Get current user info |
| PUT | `/me` | Update current user info |

### Products (`/api/products`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Get all products (with filters) |
| GET | `/{product_id}` | Get single product |
| POST | `/` | Create new product |
| PUT | `/{product_id}` | Update product |
| DELETE | `/{product_id}` | Delete product |
| POST | `/{product_id}/images` | Upload product image |
| GET | `/categories/` | Get all categories |
| POST | `/categories/` | Create category |
| PUT | `/categories/{category_id}` | Update category |
| DELETE | `/categories/{category_id}` | Delete category |

### Cart (`/api/cart`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Get user's cart |
| POST | `/items` | Add item to cart |
| PUT | `/items/{item_id}` | Update cart item |
| DELETE | `/items/{item_id}` | Remove item from cart |
| DELETE | `/` | Clear cart |

### Orders (`/api/orders`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Get user's orders |
| GET | `/{order_id}` | Get single order |
| POST | `/` | Create order from cart |
| PUT | `/{order_id}` | Update order |
| POST | `/{order_id}/upload-receipt` | Upload payment receipt |

### Admin (`/api/admin`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/jewelers` | Create jeweler |
| GET | `/jewelers` | Get all jewelers |
| PUT | `/jewelers/{id}` | Update jeweler |
| DELETE | `/jewelers/{id}` | Delete jeweler |
| POST | `/payment-methods` | Create payment method |
| GET | `/payment-methods` | Get all payment methods |
| PUT | `/payment-methods/{id}` | Update payment method |
| GET | `/orders` | Get all orders |
| PUT | `/orders/{id}/status` | Update order status |
| GET | `/design-requests` | Get design requests |
| PUT | `/design-requests/{id}` | Update design request |

### AI Design (`/api/ai`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/generate-design` | Generate AI jewelry design |
| GET | `/designs` | Get user's generated designs |
| GET | `/designs/{design_id}` | Get single design |
| POST | `/design-requests` | Create design request |
| GET | `/design-requests` | Get user's design requests |
| GET | `/jewelers` | Get jewelers for design requests |

## Frontend Integration Guide

### Authentication with JWT

```javascript
// Register a new user
async function register(userData) {
    const response = await fetch('http://localhost:8000/api/auth/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData)
    });
    return await response.json();
}

// Login and get token
async function login(username, password) {
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);
    
    const response = await fetch('http://localhost:8000/api/auth/login', {
        method: 'POST',
        body: formData
    });
    const data = await response.json();
    
    // Store token in localStorage
    localStorage.setItem('access_token', data.access_token);
    return data;
}

// Get current user (requires authentication)
async function getCurrentUser() {
    const token = localStorage.getItem('access_token');
    
    const response = await fetch('http://localhost:8000/api/auth/me', {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });
    return await response.json();
}
```

### AI Design Generation

```javascript
// Generate AI Jewelry Design
async function generateDesign(designParams) {
    const token = localStorage.getItem('access_token');
    
    const response = await fetch('http://localhost:8000/api/ai/generate-design', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': token ? `Bearer ${token}` : ''
        },
        body: JSON.stringify({
            type: designParams.type,           // e.g., "Ring", "Necklace", "Bracelet"
            color: designParams.color,         // e.g., "Gold", "Silver", "Rose Gold"
            shape: designParams.shape,         // e.g., "Round", "Oval", "Heart"
            material: designParams.material,   // e.g., "Gold", "Silver"
            karat: designParams.karat,         // e.g., "18k", "21k", "24k"
            gemstone_type: designParams.gemstone,  // e.g., "Diamond", "Ruby", "None"
            gemstone_color: designParams.gemColor  // e.g., "White", "Red", "Blue"
        })
    });
    
    const result = await response.json();
    
    // result.generated_image_url contains the path to the generated image
    // result.id is the design ID for future reference
    return result;
}

// Example usage
const design = await generateDesign({
    type: "Ring",
    color: "Rose Gold",
    shape: "Heart",
    material: "Gold",
    karat: "18k",
    gemstone: "Ruby",
    gemColor: "Red"
});

// Display the generated image
const img = document.createElement('img');
img.src = `http://localhost:8000/${design.generated_image_url}`;
document.body.appendChild(img);
```

### Cart Management

```javascript
// Add item to cart
async function addToCart(productId, quantity = 1) {
    const token = localStorage.getItem('access_token');
    
    const response = await fetch('http://localhost:8000/api/cart/items', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
            product_id: productId,
            quantity: quantity
        })
    });
    return await response.json();
}

// Get cart
async function getCart() {
    const token = localStorage.getItem('access_token');
    
    const response = await fetch('http://localhost:8000/api/cart/', {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });
    return await response.json();
}

// Remove item from cart
async function removeFromCart(itemId) {
    const token = localStorage.getItem('access_token');
    
    const response = await fetch(`http://localhost:8000/api/cart/items/${itemId}`, {
        method: 'DELETE',
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });
    return response;
}
```

### Get Products with Filters

```javascript
async function getProducts(filters = {}) {
    const params = new URLSearchParams();
    
    if (filters.category_id) params.append('category_id', filters.category_id);
    if (filters.material) params.append('material', filters.material);
    if (filters.min_price) params.append('min_price', filters.min_price);
    if (filters.max_price) params.append('max_price', filters.max_price);
    if (filters.jeweler_id) params.append('jeweler_id', filters.jeweler_id);
    
    const response = await fetch(`http://localhost:8000/api/products/?${params.toString()}`);
    return await response.json();
}

// Example: Get all gold rings under $5000
const goldRings = await getProducts({
    material: 'Gold',
    max_price: 5000
});
```

### Create an Order

```javascript
async function createOrder(orderData) {
    const token = localStorage.getItem('access_token');
    
    const response = await fetch('http://localhost:8000/api/orders/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
            payment_method_id: orderData.payment_method_id,
            shipping_address: orderData.shipping_address,
            transfer_receipt: orderData.receipt_url // optional
        })
    });
    return await response.json();
}
```

## Database Schema

### Tables Overview

1. **Users**: Customer accounts with personal information
2. **Jewelers**: Jewelry shop/seller profiles
3. **Payment_Methods**: Available payment options
4. **Categories**: Product categories with hierarchical structure
5. **Products**: Jewelry items for sale
6. **Product_Images**: Multiple images per product
7. **Product_Categories**: Many-to-many relationship between products and categories
8. **Carts**: Shopping carts linked to users
9. **Cart_Items**: Items in shopping carts
10. **Orders**: Customer orders
11. **Order_Items**: Items in orders
12. **User_Generated_Designs**: AI-generated jewelry designs
13. **Design_Requests**: Custom design requests to jewelers

### Enums

**OrderStatus**: pending, confirmed, processing, shipped, delivered, cancelled

**DesignRequestStatus**: pending, reviewed, quoted, accepted, rejected, completed

**Gender**: male, female, other

## Test Credentials

After running the seeder, you can test with these accounts:

- **Username**: `john_doe` | **Password**: `password123`
- **Username**: `jane_smith` | **Password**: `password123`
- **Username**: `mohammed_ali` | **Password**: `password123`

## License

MIT License
