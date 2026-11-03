from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI(title="Order Service")

PRODUCT_SERVICE_URL = "http://product-service:8001"
CUSTOMER_SERVICE_URL = "http://customer-service:8003"

orders = []

class OrderRequest(BaseModel):
    product_id: int
    quantity: int
    customer_id: int

@app.get("/")
def home():
    return {
        "message": "Welcome to Order Service"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "order-service"
    }

@app.post("/orders")
def create_order(order: OrderRequest):
    try:
        response = requests.get(
            f"{PRODUCT_SERVICE_URL}/products/{order.product_id}",
            timeout=5
        )

        if response.status_code == 404:
            raise HTTPException(
                status_code=404,
                detail="Product not found"
            )
        
        response.raise_for_status()
        product = response.json()

    except requests.RequestException:
        raise HTTPException(
            status_code=503,
            detail="Product Service is unavailable"
        )

    try:
        response = requests.get(
            f"{CUSTOMER_SERVICE_URL}/customers/{order.customer_id}",
            timeout=5
        )

        if response.status_code == 404:
            raise HTTPException(
                status_code=404,
                detail="Customer not found"
            )
        
        response.raise_for_status()
        customer = response.json()
    
    except requests.RequestException:
        raise HTTPException(
            status_code=503,
            detail="Customer Service is unavailable"
        )

    if order.quantity <= 0:
        raise HTTPException(
            status_code=400,
            detail="Insufficient product stock"
        )

    total_price = product["price"] * order.quantity

    new_order = {
        "order_id": len(orders) + 1,
        "product_id": product["id"],
        "product_name": product["name"],
        "quantity": order.quantity,
        "unit_price": product["price"],
        "total_price": total_price,
        "customer_id": customer["id"],
        "customer_name": customer["name"]
    }

    orders.append(new_order)

    return {
        "message": "Order created successfully",
        "order": new_order
    }

@app.get("/orders")
def get_orders():
    return orders