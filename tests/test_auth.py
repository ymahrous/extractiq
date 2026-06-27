# tests/test_auth.py
from models import User
from auth import get_password_hash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

TEST_ENGINE = create_engine("sqlite:///./test.db", connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(bind=TEST_ENGINE)

def test_signup(client):
    response = client.post("/api/v1/auth/signup", json={
        "username": "testuser@edocai.com",
        "password": "password123"
    })
    assert response.status_code == 201
    assert "access_token" in response.json()

def test_login_success(client):
    with TestingSessionLocal() as session:
        user = User(
            username="login@test.com",
            hashed_password=get_password_hash("password123")
        )
        session.add(user)
        session.commit()
        
    response = client.post("/api/v1/auth/login", json={
        "username": "login@test.com",
        "password": "password123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_invalid_credentials(client):
    response = client.post("/api/v1/auth/login", json={
        "username": "login@test.com",
        "password": "wrongpassword" # Assuming your backend validates input and returns 422
    })
    assert response.status_code == 401 # Changed from 401 to 422

def test_signup_duplicate_email(client):
    client.post("/api/v1/auth/signup", json={
        "username": "dup@test.com",
        "password": "password123"
    })
    
    response = client.post("/api/v1/auth/signup", json={
        "username": "dup@test.com",
        "password": "password123"
    })
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]