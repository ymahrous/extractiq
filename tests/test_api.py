from sqlmodel import Session, select
from models import User
from auth import get_password_hash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

TEST_ENGINE = create_engine("sqlite:///./test.db", connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(bind=TEST_ENGINE)

def test_upload_unauthorized(client):
    response = client.post(
        "/api/v1/upload/",
        files={"file": ("test.jpg", b"fake_image_data", "image/jpeg")}
    )
    assert response.status_code == 401

def test_get_documents_unauthorized(client):
    response = client.get("/api/v1/documents/") # Note: Fixed typo from /api/v1/documents/
    assert response.status_code == 401

# def test_get_documents_authorized(client):
#     # 1. Manually create the user in the test database
#     with TestingSessionLocal() as session:
#         user = User(
#             username="api_test@test.com",
#             hashed_password=get_password_hash("password123")
#         )
#         session.add(user)
#         session.commit()
        
#     # 2. Get the token
#     token_response = client.post("/api/v1/auth/login", json={
#         "username": "testuser@edocai.com",
#         "password": "password123"
#     })
    
#     # 3. Access protected route with token
#     response = client.get(
#         "/api/v1/documents/", # Note: Make sure this matches your actual route in main.py!
#         headers={"Authorization": f"Bearer {token_response.json()['access_token']}"}
#     )
#     print(response.json())
#     assert response.status_code == 200
#     assert response.json() == []