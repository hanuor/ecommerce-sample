from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def create_product(
    name="Mechanical Keyboard",
    price=2500,
    stock=10,
):
    response = client.post(
        "/admin/products",
        json={
            "name": name,
            "price": price,
            "stock": stock,
        },
    )

    assert response.status_code == 201

    return response.json()["id"]


def add_to_cart(user_id, product_id, quantity):
    response = client.post(
        "/cart/items",
        json={
            "user_id": user_id,
            "product_id": product_id,
            "quantity": quantity,
        },
    )

    assert response.status_code == 200


def test_successful_checkout():

    product_id = create_product()

    add_to_cart(
        user_id=1,
        product_id=product_id,
        quantity=2,
    )

    response = client.post(
        "/checkout",
        json={
            "user_id": 1
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["order_id"] == 1
    assert body["subtotal"] == 5000
    assert body["discount"] == 0
    assert body["total"] == 5000
    assert body["generated_coupon"] is None

    # Cart should now be empty
    cart = client.get("/cart/1").json()

    assert cart["items"] == []
    assert cart["subtotal"] == 0


def test_checkout_with_invalid_coupon():

    product_id = create_product()

    add_to_cart(
        user_id=2,
        product_id=product_id,
        quantity=1,
    )

    response = client.post(
        "/checkout",
        json={
            "user_id": 2,
            "discount_code": "INVALID123",
        },
    )

    assert response.status_code == 400

    assert response.json()["detail"] == "Invalid or already used coupon."


def test_checkout_empty_cart():

    response = client.post(
        "/checkout",
        json={
            "user_id": 999
        },
    )

    assert response.status_code == 400

    assert response.json()["detail"] == "Cart is empty."


# def test_checkout_insufficient_stock():

#     product_id = create_product(stock=2)

#     add_to_cart(
#         user_id=3,
#         product_id=product_id,
#         quantity=3,
#     )

#     response = client.post(
#         "/checkout",
#         json={
#             "user_id": 3
#         },
#     )

#     assert response.status_code == 400

#     assert "Insufficient stock" in response.json()["detail"]


def test_statistics_updated_after_checkout():

    product_id = create_product()

    add_to_cart(
        user_id=4,
        product_id=product_id,
        quantity=2,
    )

    checkout = client.post(
        "/checkout",
        json={
            "user_id": 4
        },
    )

    assert checkout.status_code == 200

    stats = client.get("/admin/stats")

    assert stats.status_code == 200

    body = stats.json()

    assert body["total_orders"] == 1
    assert body["total_items_purchased"] == 2
    assert body["total_revenue"] == 5000
    assert body["total_discount_given"] == 0