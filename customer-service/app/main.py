from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI (title="Customer Service")

class customerDetails(BaseModel):
    name: str

customers = []

@app.get("/")
def home():
    return {
        "message": "Welcome to Customer Service"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "customer-service"
    }

@app.get("/customers")
def get_customers():
    return customers

@app.get("/customers/{customer_id}")
def get_customer(customer_id: int):
    for customer in customers:
        if customer["id"] == customer_id:
            return customer

    raise HTTPException(
        status_code=404,
        detail="Product not found"
    )

@app.post("/customer")
def create_customer(customer: customerDetails):
    new_customer = {
        "id": len(customers) + 1,
        "name": customer.name
    }

    customers.append(new_customer)

    return {
        "message": "customer created successfully",
        "customer": new_customer
    }