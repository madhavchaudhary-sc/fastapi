import sys   #Python ke kisi existing module/library ko apni file mein use karne ke liye lana.  , sys Python ka built-in module hai.Isme Python ke system/interpreter se related information hoti hai.
from pathlib import Path  #Ye ek list hoti hai jisme Python dekhta hai ki modules/files kahan search karne hain. Ye path ko properly handle karne mein help karta hai.

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool  #SQLite ka ye temporary database ek hi connection ko maintain kare, isliye StaticPool use kiya.
from fastapi.testclient import TestClient

from database import Base   #Python database.py ko sys.path mein available locations mein search karta hai.
from main import app, get_db



#Ye temporary SQLite database create karta hai.
SQLALCHEMY_DATABASE_URL = "sqlite://"


#Ye SQLite database ka connection/engine banata hai.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool, #"Test ke dauran isi temporary database ko use karte raho."
)

#Ye testing database ke liye database session factory hai.
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

@pytest.fixture
def db():
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db):

    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    return TestClient(app)


# Normal App
# SessionLocal
#      ↓
# PostgreSQL


# Tests
# TestingSessionLocal
#      ↓
# SQLite


#! Sabse important: @pytest.fixture

#?Test ko jo cheez chahiye, woh ready karke dena.
# @pytest.fixture
# def db():


# Test ko database chahiye
#         ↓
# fixture database banata hai
#         ↓
# test ko database milta hai

#? Table create
# Base.metadata.create_all(bind=engine)    #Ye test database ke andar tables banata hai.

# Tere database_model.py mein:   ==> class Product(Base):  hai.
# To test database mein: ==> product ==>table create ho jayegi.

#? Database session
# db = TestingSessionLocal()   #Ab actual database session mil gaya.


# SQLite Test DB
#       ↓
# TestingSessionLocal()
#       ↓
# db



#? yield db

# yield db

# Iska matlab: "Ye database session test ko de do."

# For example:

# def test_create_product(client):

# aur client ke andar API ko database chahiye.
# Fixture usko database provide karega.

#? finally 
# finally:
#     db.close()

#? drop_all
# Base.metadata.drop_all(bind=engine)

# Ye test ke baad tables hata deta hai.


# Test start
#    ↓
# DB open
#    ↓
# CRUD test
#    ↓
# Test finish
#    ↓
# DB close
# Test finish
#    ↓
# Table delete


#? Ab second fixture

# @pytest.fixture
# def client(db):

# yahan client fixture ko db fixture chahiye.

# Pytest automatically:

# client
#   ↓
# db
#   ↓
# Test database



#? 12. Dependency Override

# Ye sabse important FastAPI concept hai:

# app.dependency_overrides[get_db] = override_get_db

#* Tere main.py mein:

# @app.get("/products")
# def get_all_product(
#     db: Session = Depends(get_db)
# ):

#* FastAPI normally:

# Depends(get_db)
#        ↓
# PostgreSQL

# use karega.

#* Lekin test mein hum bol rahe hain:

# Depends(get_db)
#        ↓
# WAIT!
#        ↓
# override_get_db use karo
#        ↓
# SQLite Test DB

# That's called dependency override.




#? override_get_db
# def override_get_db():
#     try:
#         yield db
#     finally:
#         pass

#? Normal:

# get_db()

# PostgreSQL session deta hai.

#? Test:

# override_get_db()

# SQLite session deta hai.

# So:

#                  get_db()
#                     │
#             ┌───────┴────────┐
#             │                │
#        Normal App           Tests
#             │                │
#       PostgreSQL          SQLite




#? TestClient

#? Finally:

# return TestClient(app)

# Testing client ready.

#? Ab test_products.py mein:

# def test_get_products(client):

# Pytest automatically client fixture ko inject karega.

# Then:

# response = client.get("/products")

#? request jayegi:

# TestClient
#     ↓
# FastAPI
#     ↓
# Depends(get_db)
#     ↓
# override_get_db
#     ↓
# SQLite
# Pura conftest.py ek line mein

#? conftest.py bolta hai:

# "Jab tests chalenge, real PostgreSQL ko mat use karo; temporary SQLite database banao, FastAPI ke get_db() ko us test database se replace karo, test ko client do, aur test ke baad database clean kar do."


# conftest.py
#     ↓
# "Test chalane ke liye environment ready karo"
#     ↓
# test_products.py
#     ↓
# "Ab CRUD test karo"