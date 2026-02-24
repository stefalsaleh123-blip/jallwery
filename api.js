const BASE_URL = "http://localhost:8000";

function getAuthToken() {
    return localStorage.getItem("access_token");
}

function setAuthToken(token) {
    localStorage.setItem("access_token", token);
}

function isLoggedIn() {
    return !!getAuthToken();
}

function logout() {
    localStorage.removeItem("access_token");
    localStorage.removeItem("user");
    window.location.href = "login.html";
}

function getCurrentUser() {
    const user = localStorage.getItem("user");
    return user ? JSON.parse(user) : null;
}

async function apiRequest(endpoint, options = {}) {
    const token = getAuthToken();
    const headers = {
        'Content-Type': 'application/json',
        ...(token && { 'Authorization': `Bearer ${token}` }),
        ...options.headers
    };

    const response = await fetch(`${BASE_URL}${endpoint}`, {
        ...options,
        headers
    });

    if (response.status === 401) {
        logout();
        return null;
    }

    return response;
}

async function login(username, password) {
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);

    const response = await fetch(`${BASE_URL}/api/auth/login`, {
        method: 'POST',
        body: formData
    });

    if (response.ok) {
        const data = await response.json();
        setAuthToken(data.access_token);
        
        const userResponse = await fetch(`${BASE_URL}/api/auth/me`, {
            headers: { 'Authorization': `Bearer ${data.access_token}` }
        });
        if (userResponse.ok) {
            const user = await userResponse.json();
            localStorage.setItem("user", JSON.stringify(user));
        }
        return { success: true };
    }
    
    const error = await response.json();
    return { success: false, error: error.detail || "Login failed" };
}

async function register(userData) {
    const response = await fetch(`${BASE_URL}/api/auth/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(userData)
    });

    if (response.ok) {
        return { success: true };
    }
    
    const error = await response.json();
    return { success: false, error: error.detail || "Registration failed" };
}

async function getProducts(filters = {}) {
    const params = new URLSearchParams();
    if (filters.category_id) params.append('category_id', filters.category_id);
    if (filters.material) params.append('material', filters.material);
    if (filters.min_price) params.append('min_price', filters.min_price);
    if (filters.max_price) params.append('max_price', filters.max_price);
    
    const response = await fetch(`${BASE_URL}/api/products/?${params.toString()}`);
    return response.json();
}

async function getProduct(productId) {
    const response = await fetch(`${BASE_URL}/api/products/${productId}`);
    return response.json();
}

async function getCategories() {
    const response = await fetch(`${BASE_URL}/api/products/categories/`);
    return response.json();
}

async function getCart() {
    if (!isLoggedIn()) return null;
    const response = await apiRequest('/api/cart/');
    return response ? response.json() : null;
}

async function addToCart(productId, quantity = 1) {
    if (!isLoggedIn()) {
        window.location.href = "login.html";
        return null;
    }
    const response = await apiRequest('/api/cart/items', {
        method: 'POST',
        body: JSON.stringify({ product_id: productId, quantity })
    });
    return response ? response.json() : null;
}

async function updateCartItem(itemId, quantity) {
    const response = await apiRequest(`/api/cart/items/${itemId}`, {
        method: 'PUT',
        body: JSON.stringify({ quantity })
    });
    return response ? response.json() : null;
}

async function removeFromCart(itemId) {
    const response = await apiRequest(`/api/cart/items/${itemId}`, {
        method: 'DELETE'
    });
    return response;
}

async function clearCart() {
    const response = await apiRequest('/api/cart/', {
        method: 'DELETE'
    });
    return response;
}

async function getOrders() {
    if (!isLoggedIn()) return [];
    const response = await apiRequest('/api/orders/');
    return response ? response.json() : [];
}

async function createOrder(orderData) {
    const response = await apiRequest('/api/orders/', {
        method: 'POST',
        body: JSON.stringify(orderData)
    });
    return response ? response.json() : null;
}

async function generateAIDesign(designData) {
    const response = await apiRequest('/api/ai/generate-design', {
        method: 'POST',
        body: JSON.stringify(designData)
    });
    return response ? response.json() : null;
}

async function getUserDesigns() {
    if (!isLoggedIn()) return [];
    const response = await apiRequest('/api/ai/designs');
    return response ? response.json() : [];
}

async function createDesignRequest(requestData) {
    const response = await apiRequest('/api/ai/design-requests', {
        method: 'POST',
        body: JSON.stringify(requestData)
    });
    return response ? response.json() : null;
}

async function getJewelers() {
    const response = await fetch(`${BASE_URL}/api/ai/jewelers`);
    return response.json();
}

function formatPrice(price) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(price);
}

function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = message;
    notification.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        padding: 15px 25px;
        border-radius: 5px;
        color: white;
        font-weight: 500;
        z-index: 9999;
        animation: slideIn 0.3s ease;
        background: ${type === 'success' ? '#2ecc71' : '#e74c3c'};
    `;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

function updateNavUI() {
    const user = getCurrentUser();
    const navIcons = document.querySelector('.nav-icons');
    
    if (navIcons) {
        if (user) {
            navIcons.innerHTML = `
                <a href="cart.html" title="Cart"><i class="fas fa-shopping-bag"></i> <span id="cart-count"></span></a>
                <a href="profile.html" title="Profile"><i class="fas fa-user"></i></a>
                <a href="#" onclick="logout(); return false;" title="Logout"><i class="fas fa-sign-out-alt"></i></a>
            `;
        } else {
            navIcons.innerHTML = `
                <a href="login.html" title="Login"><i class="fas fa-sign-in-alt"></i></a>
                <a href="cart.html" title="Cart"><i class="fas fa-shopping-bag"></i></a>
            `;
        }
    }
}

document.addEventListener('DOMContentLoaded', function() {
    updateNavUI();
});
