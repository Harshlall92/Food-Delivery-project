import pytest

from fastapi.testclient import TestClient

from app.main import app
from app.schemas.user import AnyUser

from tests.util.builders import PASSWORD, create_test_admin, create_user_with_role
from tests.util.fixtures import mocked_user_repository
from tests.util.helpers import add_user_to_repository

client = TestClient(app)

def user_token(user: AnyUser):
    response = client.post(
        "/token",
        data={"username": user.email, "password": PASSWORD}
    )
    
    assert response.status_code == 200
    return response.json()["access_token"]

class TestHealthEndpoint:

    @pytest.mark.parametrize(
        "authorization_header",
        [
            "",
            "Bearer invalid.token.value",
        ]
    )
    def test_requires_authentication(self, authorization_header):
        response = client.get(
            "/health",
            headers={"Authorization": authorization_header}
        )

        assert response.status_code == 401

    def test_allows_active_admin(self, mocked_user_repository):
        admin = create_test_admin()
        add_user_to_repository(admin)
        token = user_token(admin)

        response = client.get(
            "/health",
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200
        assert response.json() == {"status": "ok"}

    def test_rejects_inactive_admin(self, mocked_user_repository):
        admin = create_test_admin(active=False)
        add_user_to_repository(admin)
        token = user_token(admin)

        response = client.get(
            "/health",
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 400
        assert response.json() == {"detail": "Inactive user"}

    @pytest.mark.parametrize(
        "role",
        [
            "customer",
            "restaurant_owner"
        ]
    )
    def test_forbids_non_admin_roles(self, mocked_user_repository, role):
        user = create_user_with_role(role)
        add_user_to_repository(user)
        token = user_token(user)

        response = client.get(
            "/health",
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 403
        
