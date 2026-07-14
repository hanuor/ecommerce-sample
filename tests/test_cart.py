from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def create_product():
    response = client.post(
        "/admin/products",
        json={
            "name": "Mechanical Keyboard",
            "price": 2500,
            "stock": 10,
        },
    )

    assert response.status_code == 201

    return response.json()["id"]


def test_add_item_to_cart():
    product_id = create_product()

    response = client.post(
        "/cart/items",
        json={
            "user_id": 1,
            "product_id": product_id,
            "quantity": 2,
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["user_id"] == 1
    assert len(body["items"]) == 1

    item = body["items"][0]

    assert item["product_id"] == product_id
    assert item["quantity"] == 2
    assert item["price"] == 2500
    assert item["total_price"] == 5000

    assert body["subtotal"] == 5000


def test_get_cart():
    product_id = create_product()

    client.post(
        "/cart/items",
        json={
            "user_id": 2,
            "product_id": product_id,
            "quantity": 3,
        },
    )

    response = client.get("/cart/2")

    assert response.status_code == 200

    body = response.json()

    assert body["user_id"] == 2
    assert body["subtotal"] == 7500
    assert len(body["items"]) == 1


def test_remove_item_from_cart():
    product_id = create_product()

    client.post(
        "/cart/items",
        json={
            "user_id": 3,
            "product_id": product_id,
            "quantity": 1,
        },
    )

    response = client.delete(
        f"/cart/3/items/{product_id}"
    )

    assert response.status_code == 200

    body = response.json()

    assert body["user_id"] == 3
    assert body["subtotal"] == 0
    assert body["items"] == []


def test_clear_cart():
    product_id = create_product()

    client.post(
        "/cart/items",
        json={
            "user_id": 4,
            "product_id": product_id,
            "quantity": 2,
        },
    )

    response = client.delete("/cart/4")

    assert response.status_code == 204

    response = client.get("/cart/4")

    assert response.status_code == 200

    body = response.json()

    assert body["user_id"] == 4
    assert body["subtotal"] == 0
    assert body["items"] == []


def test_add_invalid_product():
    response = client.post(
        "/cart/items",
        json={
            "user_id": 1,
            "product_id": 999,
            "quantity": 1,
        },
    )

    assert response.status_code == 404


def test_add_more_than_available_stock():
    product_id = create_product()

    response = client.post(
        "/cart/items",
        json={
            "user_id": 1,
            "product_id": product_id,
            "quantity": 100,
        },
    )

    assert response.status_code == 400