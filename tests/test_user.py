from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

users = [
    {
        'id': 1,
        'name': 'Ivan Ivanov',
        'email': 'i.i.ivanov@mail.com',
    },
    {
        'id': 2,
        'name': 'Petr Petrov',
        'email': 'p.p.petrov@mail.com',
    }
]

def test_get_existed_user():
    '''Получение существующего пользователя'''
    response = client.get("/api/v1/user", params={'email': users[0]['email']})
    assert response.status_code == 200
    assert response.json() == users[0]

def test_get_unexisted_user():
    '''Получение несуществующего пользователя'''
    response = client.get("/api/v1/user", params={'email': 'fake@test.com'})
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

def test_create_user_with_valid_email():
    '''Создание пользователя с уникальной почтой'''
    new_user = {"name": "New Guy", "email": "newguy@mail.com"}
    response = client.post("/api/v1/user", json=new_user)
    assert response.status_code == 201
    assert isinstance(response.json(), int)

def test_create_user_with_invalid_email():
    '''Создание пользователя с почтой, которую использует другой пользователь'''
    existing_user = {"name": "Ivan Ivanov", "email": users[0]['email']}
    response = client.post("/api/v1/user", json=existing_user)
    assert response.status_code == 409
    assert response.json() == {"detail": "User with this email already exists"}

def test_delete_user():
    '''Удаление пользователя'''
    new_user = {"name": "Temp User", "email": "temp.delete@mail.com"}
    create_resp = client.post("/api/v1/user", json=new_user)
    assert create_resp.status_code == 201

    response = client.delete("/api/v1/user", params={'email': 'temp.delete@mail.com'})
    assert response.status_code == 204

    response_get = client.get("/api/v1/user", params={'email': 'temp.delete@mail.com'})
    assert response_get.status_code == 404
