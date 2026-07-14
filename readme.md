# E-Commerce Store

A lightweight e-commerce backend built with **FastAPI** and **Redis**.

## Features

- Product management
- Shopping cart
- Checkout
- Coupon validation
- Automatic reward coupon generation (every Nth order)
- Store analytics

---

## Tech Stack

- FastAPI
- Redis
- Pydantic
- Python 3.9+

---

## Project Structure

```text
app/
├── api/
├── core/
├── repositories/
├── schemas/
├── services/
└── main.py
```

---

## Prerequisites

- Python 3.9+
- Redis
- pip

---

## Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd ecommerce-store
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

**macOS / Linux**

```bash
source venv/bin/activate
```

**Windows**

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root.

```env
REDIS_HOST=localhost
REDIS_PORT=6379

NTH_ORDER=5
DISCOUNT_PERCENTAGE=10
```

### 5. Start Redis

If Redis is installed locally:

```bash
redis-server
```

Verify it's running:

```bash
redis-cli ping
```

Expected response:

```text
PONG
```

### 6. Run the application

```bash
uvicorn app.main:app --reload
```

---

## API Documentation

Swagger UI:

```
http://localhost:8000/docs
```

ReDoc:

```
http://localhost:8000/redoc
```

---

## API Endpoints

### Cart

| Method | Endpoint |
|---------|----------|
| POST | `/cart/items` |
| GET | `/cart/{user_id}` |
| DELETE | `/cart/{user_id}/items/{product_id}` |
| DELETE | `/cart/{user_id}` |

### Checkout

| Method | Endpoint |
|---------|----------|
| POST | `/checkout` |

### Admin

| Method | Endpoint |
|---------|----------|
| POST | `/admin/products` |
| GET | `/admin/products` |
| POST | `/admin/generate-discount` |
| GET | `/admin/coupons` |
| GET | `/admin/stats` |

---

## Assumptions

- Product inventory is managed within the application.
- Coupons can only be used once.
- Every Nth successful checkout generates a reward coupon.
- Shopping carts are stored in Redis.
- Store analytics are updated during checkout.

---

## Production Considerations

For the purpose of this project, Redis is used as the primary datastore.

In a production system, orders and payment-related data would typically be stored in a relational database such as PostgreSQL to provide stronger durability, transactional guarantees, and auditing, while Redis would continue to be used for carts, caching, counters, and distributed locking.




---

# Sample API Flow

## 1. Create a Product

**POST** `/admin/products`

Request

```json
{
  "name": "Mechanical Keyboard",
  "price": 2500,
  "stock": 10
}
```

Response

```json
{
  "id": 1,
  "name": "Mechanical Keyboard",
  "price": 2500,
  "stock": 10
}
```

---

## 2. Add Product to Cart

**POST** `/cart/items`

Request

```json
{
  "user_id": 1,
  "product_id": 1,
  "quantity": 2
}
```

Response

```json
{
  "user_id": 1,
  "items": [
    {
      "product_id": 1,
      "quantity": 2,
      "price": 2500,
      "total_price": 5000
    }
  ],
  "subtotal": 5000
}
```

---

## 3. View Cart

**GET** `/cart/1`

Response

```json
{
  "user_id": 1,
  "items": [
    {
      "product_id": 1,
      "quantity": 2,
      "price": 2500,
      "total_price": 5000
    }
  ],
  "subtotal": 5000
}
```

---

## 4. Checkout

**POST** `/checkout`

Request

```json
{
  "user_id": 1
}
```

Response

```json
{
  "order_id": 1,
  "items": [
    {
      "product_id": 1,
      "quantity": 2,
      "price": 2500
    }
  ],
  "subtotal": 5000,
  "discount": 0,
  "total": 5000,
  "generated_coupon": null
}
```

---

## 5. Checkout Using a Coupon

**POST** `/checkout`

Request

```json
{
  "user_id": 2,
  "discount_code": "SAVE10AB"
}
```

Response

```json
{
  "order_id": 2,
  "items": [
    {
      "product_id": 1,
      "quantity": 1,
      "price": 2500
    }
  ],
  "subtotal": 2500,
  "discount": 250,
  "total": 2250,
  "generated_coupon": null
}
```

---

## 6. View Store Statistics

**GET** `/admin/stats`

Response

```json
{
  "total_orders": 2,
  "total_items_purchased": 3,
  "total_revenue": 7250,
  "total_discount_codes": 0,
  "total_discount_given": 250
}
```

---

## 7. List Coupons

**GET** `/admin/coupons`

Response

```json
[
  {
    "code": "SAVE10AB",
    "percentage": 10,
    "used": true
  },
  {
    "code": "X7P2K9QM",
    "percentage": 10,
    "used": false
  }
]
```

> **Note:** Every `N`th successful checkout generates a new reward coupon. The value of `N` is configurable using the `NTH_ORDER` environment variable.