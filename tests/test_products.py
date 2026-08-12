# from fastapi.testclient import TestClient

# from main import app

# client = TestClient(app)

def test_get_products(client):
    response = client.get("/products")

    assert response.status_code == 200


def test_get_product_by_id(client):
    response = client.get("/products/1")

    assert response.status_code == 404


def test_create_product(client):
    product = {
        "id": 100,
        "name": "Test Phone",
        "description": "Test description",
        "price": 99.2,
        "quantity": 5
    }

    response = client.post("/products", json=product)

    assert response.status_code == 200
    assert response.json()["name"] == "Test Phone"


def test_update_product(client):
    product = {
        "id": 100,
        "name": "Updated Phone",
        "description": "Updated testing product",
        "price": 199.99,
        "quantity": 10
    }

    client.post("/products", json={
        "id": 100,
        "name": "Test Phone",
        "description": "Test description",
        "price": 99.2,
        "quantity": 5
    })

    response = client.put(
        "/products/100",
        json=product
    )

    assert response.status_code == 200


def test_delete_product(client):
    client.post("/products", json={
        "id": 100,
        "name": "Test Phone",
        "description": "Test description",
        "price": 99.2,
        "quantity": 5
    })

    response = client.delete("/products/100")

    assert response.status_code == 200





















# Haan bhai. Upar jo `test_products.py` diya tha, usko **line by line simple way mein** samajh:

# ## 1. FastAPI ka testing client

# ```python
# from fastapi.testclient import TestClient
# ```

# `TestClient` ek fake client hai jo browser/Postman/React ki tarah API ko request bhej sakta hai.

# Normally:

# ```text
# React/Postman
#      ↓
#    FastAPI
# ```

# Testing mein:

# ```text
# TestClient
#      ↓
#    FastAPI
# ```

# ---

# ## 2. Apni FastAPI app import ki

# ```python
# from main import app
# ```

# Tere `main.py` mein:

# ```python
# app = FastAPI()
# ```

# hai.

# Hum wahi `app` testing ke liye use kar rahe hain.

# ---

# ## 3. Test client banaya

# ```python
# client = TestClient(app)
# ```

# Ab `client` se hum API endpoints ko call kar sakte hain.

# Example:

# ```python
# client.get("/products")
# ```

# Matlab:

# > `/products` par GET request bhejo.

# ---

# # 4. GET all products test

# ```python
# def test_get_products():
#     response = client.get("/products")

#     assert response.status_code == 200
# ```

# Yahan:

# ```python
# client.get("/products")
# ```

# ye request bhejta hai:

# ```text
# GET /products
# ```

# Tere `main.py` mein:

# ```python
# @app.get("/products")
# def get_all_product(...):
# ```

# hai.

# Agar API successfully response deti hai:

# ```text
# 200 OK
# ```

# To:

# ```python
# assert response.status_code == 200
# ```

# check karega.

# ### `assert` kya hai?

# Simple:

# > "Mujhe expect hai ki ye condition true honi chahiye."

# Agar:

# ```text
# 200 == 200
# ```

# → Test PASS ✅

# Agar:

# ```text
# 500 == 200
# ```

# → Test FAIL ❌

# ---

# # 5. GET product by ID

# ```python
# def test_get_product_by_id():
#     response = client.get("/products/1")

#     assert response.status_code in [200, 404]
# ```

# Request:

# ```text
# GET /products/1
# ```

# Tere code mein:

# ```python
# @app.get("/products/{id}")
# ```

# hai.

# Agar product `1` mil gaya:

# ```text
# 200
# ```

# Agar nahi mila:

# ```text
# 404
# ```

# Isliye:

# ```python
# in [200, 404]
# ```

# bola hai.

# Matlab:

# > 200 ya 404 mein se koi bhi aaya to test pass.

# **Lekin industry-style test mein hum usually exact expected result check karenge.** Ye basic example tha.

# ---

# # 6. POST test

# ```python
# def test_create_product():
# ```

# Hum ek product ka data banate hain:

# ```python
# product = {
#     "id": 100,
#     "name": "Test Phone",
#     "description": "Testing product",
#     "price": 99.99,
#     "quantity": 5
# }
# ```

# Ye exactly request body jaisa hai:

# ```json
# {
#   "id": 100,
#   "name": "Test Phone",
#   "description": "Testing product",
#   "price": 99.99,
#   "quantity": 5
# }
# ```

# Phir:

# ```python
# response = client.post("/products", json=product)
# ```

# Matlab:

# ```text
# POST /products
#        ↓
# JSON body
#        ↓
# FastAPI
# ```

# Tere endpoint mein:

# ```python
# @app.post("/products")
# def add_product(product: Product, ...):
# ```

# FastAPI JSON ko `Product` Pydantic model mein convert karega.

# Phir:

# ```python
# assert response.status_code == 200
# ```

# check karega ki creation successful hui.

# ---

# # 7. PUT test

# ```python
# def test_update_product():
# ```

# Update ke liye data:

# ```python
# product = {
#     "id": 100,
#     "name": "Updated Phone",
#     "description": "Updated testing product",
#     "price": 199.99,
#     "quantity": 10
# }
# ```

# Phir:

# ```python
# response = client.put("/products/100", json=product)
# ```

# Matlab:

# ```text
# PUT /products/100
# ```

# Tere endpoint:

# ```python
# @app.put("/products/{id}")
# ```

# mein `id = 100` jayega.

# Aur body mein updated product jayega.

# Phir:

# ```python
# assert response.status_code == 200
# ```

# ---

# # 8. DELETE test

# ```python
# def test_delete_product():
#     response = client.delete("/products/100")

#     assert response.status_code == 200
# ```

# Request:

# ```text
# DELETE /products/100
# ```

# Tere endpoint:

# ```python
# @app.delete("/products/{id}")
# ```

# ko hit karega.

# Agar deletion successful:

# ```text
# 200 OK
# ```

# to test pass.

# ---

# # Overall kya ho raha hai?

# Tere 5 API operations:

# ```text
#                 TestClient
#                     │
#         ┌───────────┼────────────┐
#         ▼           ▼            ▼
#        GET         POST         PUT
#         │           │            │
#         ▼           ▼            ▼
#    /products    /products   /products/100
#         │
#         ▼
#       DELETE
#         │
#         ▼
#    /products/100
# ```

# `pytest` in functions ko automatically discover karega because functions ka naam:

# ```text
# test_...
# ```

# se start ho raha hai.

# Phir:

# ```powershell
# pytest
# ```

# run karoge.

# Output roughly:

# ```text
# 5 passed
# ```

# Matlab:

# ```text
# GET       ✅
# GET ID    ✅
# POST      ✅
# PUT       ✅
# DELETE    ✅
# ```

# ### Aur GitHub Actions mein

# Local:

# ```text
# pytest
#    ↓
# 5 tests
#    ↓
# PASS
# ```

# GitHub:

# ```text
# git push
#    ↓
# GitHub Actions
#    ↓
# Runner
#    ↓
# pytest
#    ↓
# 5 tests
#    ↓
# ✅ PASS
# ```

# **Bas ek important correction:** jo test code maine diya tha woh samajhne ke liye basic tha. Tere current PostgreSQL setup ke saath directly GitHub Actions mein nahi chalega. Ab next hum **test database + dependency override** samjhenge, taaki actual CRUD tests safely run hon.
