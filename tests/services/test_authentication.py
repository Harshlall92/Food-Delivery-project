import bcrypt
import jwt
import pytest

from app.repositories.exceptions import RecordNotFoundError
from app.schemas.user import Customer
import app.services.authentication as auth
from app.services.exceptions import InvalidCredentialsError
from tests.util.builders import create_test_customer, create_test_admin, create_test_restaurant_owner, create_user_with_role
from tests.util.helpers import credentials, token_for
from tests.util.fixtures import user_repository

PASSWORD = "correct-password"

class TestVerifyPassword:

    def test_verify_password_success(self):
        user = create_test_customer(password=PASSWORD)

        assert auth.verify_password(PASSWORD, user.password)
        

    def test_verify_password_failure(self):
        password = "mysecretpassword"
        wrong_password = "wrongpassword"
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        assert not auth.verify_password(wrong_password, hashed_password)

class TestCreateAccessToken:

    @pytest.mark.anyio
    async def test_contains_subject_and_expiration(self):
        user = create_test_customer(password=PASSWORD)

        token = await auth.create_access_token(user)
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])

        assert payload.get("sub") == user.id
        assert "exp" in payload

class TestDecodeToken:

    def test_returns_subject_for_valid_token(self):
        user = create_test_customer(password=PASSWORD)

        token = token_for(user.id)
        user_id = auth.decode_token(token)

        assert user_id == user.id

    def test_raises_exception_for_invalid_token(self):
        invalid_token = "invalid.token.value"

        with pytest.raises(jwt.InvalidTokenError):
            auth.decode_token(invalid_token)

    def test_raises_exception_for_expired_token(self):
        user = create_test_customer(password=PASSWORD)

        expired_token = token_for(user.id, expires=auth.datetime.now(auth.UTC) - auth.timedelta(minutes=1))

        with pytest.raises(jwt.ExpiredSignatureError):
            auth.decode_token(expired_token)

    def test_raises_exception_for_invalid_signature(self):
        user = create_test_customer(password=PASSWORD)

        token = token_for(user.id, secret="wrong-secret")

        with pytest.raises(jwt.InvalidSignatureError):
            auth.decode_token(token)

class TestAuthenticateUser:

    @pytest.mark.anyio
    async def test_returns_token_for_valid_credentials(self, user_repository, mocker):
        user = create_test_customer(password=PASSWORD)

        mocker.patch(
            "app.services.authentication.UserRepository.get_by_email",
            return_value=user
        )

        token = await auth.authenticate_user(
            user_repository, 
            credentials(user.email, PASSWORD)
        )

        assert auth.decode_token(token) == user.id

    @pytest.mark.anyio
    async def test_rejects_unknown_email(self, mocker):
        user_repository = mocker.Mock(spec=auth.UserRepository)
        user_repository.get_by_email.side_effect = RecordNotFoundError(Customer, id="unknown@example.com")

        with pytest.raises(InvalidCredentialsError):
            await auth.authenticate_user(
                user_repository, 
                credentials("unknown@example.com", PASSWORD)
            )

    @pytest.mark.anyio
    async def test_rejects_incorrect_password(self, user_repository, mocker):
        user = create_test_customer(password=PASSWORD)

        mocker.patch(
            "app.services.authentication.UserRepository.get_by_email",
            return_value=user
        )

        mocker.patch(
            "app.services.authentication.verify_password",
            return_value=False
        )

        mocker.patch(
            "app.services.authentication.UserRepository.get_by_email",
            return_value=user
        )

        with pytest.raises(InvalidCredentialsError):
            await auth.authenticate_user(
                user_repository, 
                credentials(user.email, "wrong-password")
            )

class TestGetCurrentUser:

    @pytest.mark.anyio
    async def test_returns_user_for_valid_token(self, mocker):
        user = create_test_customer(password=PASSWORD)

        token = await auth.create_access_token(user)

        mocker.patch(
            "app.services.authentication.UserRepository.get_by_id",
            return_value=user
        )

        current_user = await auth.get_current_user(token)

        assert current_user == user

    @pytest.mark.anyio
    async def test_rejects_invalid_token(self, mocker):
        invalid_token = "invalid.token.value"

        mocker.patch(
            "app.services.authentication.decode_token",
            side_effect=jwt.InvalidTokenError
        )

        with pytest.raises(auth.HTTPException) as e:
            await auth.get_current_user(invalid_token)

        assert e.value.status_code== 401
        assert e.value.headers
        assert e.value.headers["WWW-Authenticate"] == "Bearer"
        assert e.value.detail == "Could not validate credentials"

    @pytest.mark.anyio
    async def test_rejects_nonexistent_user(self, mocker):
        user = create_test_customer(password=PASSWORD)

        token = await auth.create_access_token(user)

        mocker.patch(
            "app.services.authentication.UserRepository.get_by_id",
            return_value=None
        )

        with pytest.raises(auth.HTTPException) as e:
            await auth.get_current_user(token)

        assert e.value.status_code == 401
        assert e.value.headers
        assert e.value.headers["WWW-Authenticate"] == "Bearer"
        assert e.value.detail == "Could not validate credentials"

    @pytest.mark.anyio
    async def test_rejects_missing_user_id_in_token(self, mocker):
        user = create_test_customer(password=PASSWORD)

        mocker.patch(
            "app.services.authentication.decode_token",
            return_value=None
        )

        with pytest.raises(auth.HTTPException) as e:
            await auth.get_current_user(token_for(user.id))

        assert e.value.status_code == 401
        assert e.value.headers
        assert e.value.headers["WWW-Authenticate"] == "Bearer"
        assert e.value.detail == "Could not validate credentials"

class TestGetCurrentActiveUser:

    @pytest.mark.anyio
    async def test_returns_active_user(self, mocker):
        user = create_test_customer(password=PASSWORD, active=True)

        mocker.patch(
            "app.services.authentication.get_current_user",
            return_value=user
        )

        active_user = await auth.get_current_active_user(user)

        assert active_user == user

    @pytest.mark.anyio
    async def test_rejects_inactive_user(self, mocker):
        user = create_test_customer(password=PASSWORD, active=False)

        mocker.patch(
            "app.services.authentication.get_current_user",
            return_value=user
        )

        with pytest.raises(auth.HTTPException) as e:
            await auth.get_current_active_user(user)

        assert e.value.status_code == 400
        assert e.value.detail == "Inactive user"

    @pytest.mark.parametrize(
        ("user", "dependency"),
        [
            (create_test_customer(password=PASSWORD), auth.get_current_active_customer),
            (create_test_restaurant_owner(password=PASSWORD), auth.get_current_active_restaurant_owner),
            (create_test_admin(password=PASSWORD), auth.get_current_active_admin)
        ]
    )
    @pytest.mark.anyio
    async def test_role_dependencies_allow_matching_roles(self, mocker, user, dependency):
        mocker.patch(
            "app.services.authentication.get_current_user",
            return_value=user
        )

        result = await dependency(user)

        assert result == user

    @pytest.mark.parametrize(
        ("role", "dependency"),
        [
            ("customer", auth.get_current_active_restaurant_owner),
            ("customer", auth.get_current_active_admin),
            ("restaurant_owner", auth.get_current_active_customer),
            ("restaurant_owner", auth.get_current_active_admin),
            ("admin", auth.get_current_active_customer),
            ("admin", auth.get_current_active_restaurant_owner)
        ]
    )
    @pytest.mark.anyio
    async def test_role_dependencies_reject_non_matching_roles(self, mocker, role, dependency):
        user = create_user_with_role(role)
        mocker.patch(
            "app.services.authentication.get_current_user",
            return_value=user
        )

        with pytest.raises(auth.HTTPException) as e:
            await dependency(user)

        assert e.value.status_code == 403
        assert e.value.detail.startswith("User is not a")
