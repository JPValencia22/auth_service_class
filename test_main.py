# test_main.py
from fastapi.testclient import TestClient


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.db import Base
from main import app
from config.db import  get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_create_item():
    response = client.post("/users/", json={"username": "JPDev", "email": "jpdev@gmail.com",  "name": "JP",  "password": "admin123",  "role": "admin",  "cel": "3216549870"})
    assert response.status_code == 201