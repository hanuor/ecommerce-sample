from fastapi.testclient import TestClient

from app.main import app
from .conftest import client
# client = TestClient(app)


def test_create_product():
    response = client.post(
        "/admin/products",
        json={
            "name": "Mechanical Keyboard",
            "price": 2500,
            "stock": 10,
        },
    )

    assert response.status_code == 201

    body = response.json()

    assert body["id"] == 1
    assert body["name"] == "Mechanical Keyboard"
    assert body["price"] == 2500
    assert body["stock"] == 10

def test_list_products():

    client.post(
        "/admin/products",
        json={
            "name": "Keyboard",
            "price": 2500,
            "stock": 10,
        },
    )

    client.post(
        "/admin/products",
        json={
            "name": "Mouse",
            "price": 1000,
            "stock": 20,
        },
    )

    response = client.get("/admin/products")

    assert response.status_code == 200

    body = response.json()

    assert len(body) == 2

    names = {product["name"] for product in body}

    assert names == {"Keyboard", "Mouse"}


def test_generate_discount_coupon():

    response = client.post(
        "/admin/generate-discount"
    )

    assert response.status_code == 200

    body = response.json()

    assert "code" in body
    assert body["percentage"] == 10
    assert body["used"] is False


def test_list_coupons():

    client.post("/admin/generate-discount")
    client.post("/admin/generate-discount")

    response = client.get("/admin/coupons")

    assert response.status_code == 200

    body = response.json()

    assert len(body) == 2

    for coupon in body:
        assert "code" in coupon
        assert "percentage" in coupon
        assert "used" in coupon


def test_stats_initially_empty():

    response = client.get("/admin/stats")

    assert response.status_code == 200

    body = response.json()

    assert body["total_orders"] == 0
    assert body["total_items_purchased"] == 0
    assert body["total_revenue"] == 0
    assert body["total_discount_given"] == 0
    assert body["total_discount_codes"] == 0


def test_stats_after_coupon_generation():

    client.post("/admin/generate-discount")
    client.post("/admin/generate-discount")

    response = client.get("/admin/stats")

    assert response.status_code == 200

    body = response.json()

    assert body["total_discount_codes"] == 2