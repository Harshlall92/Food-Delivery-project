import pytest

from app.schemas.user import User, UserUpdate

class TestUserModel:

    @pytest.mark.parametrize("email", [
        "plainaddress",
        "@missingusername.com",
        "username@.com",
        "username@com",
        "username@domain..com",
        "username@domain,com",
        "username@"
    ])
    def test_user_must_have_valid_email(self, email: str):
        with pytest.raises(ValueError):
            User(
                email=email,
                password="password123",
                first_name="John",
                last_name="Doe"
            )

    def test_user_email_is_normalized(self):
        user = User(
            email="    JOHN@DOE.COM     ",
            password="password123",
            first_name="John",
            last_name="Doe"
        )
        assert user.email == "john@doe.com"

    def test_user_names_are_normalized(self):
        user = User(
            email="john@doe.com",
            password="password123",
            first_name="  john   ",
            last_name="   doe    "
        )
        assert user.first_name == "John"
        assert user.last_name == "Doe"

    def test_user_names_cannot_be_empty(self):
        with pytest.raises(ValueError):
            User(
                email="john@doe.com",
                password="password123",
                first_name="   ",
                last_name="Doe"
            )

        with pytest.raises(ValueError):
            User(
                email="john@doe.com",
                password="password123",
                first_name="John",
                last_name="   "
            )

    def test_user_password_cannot_be_empty(self):
        with pytest.raises(ValueError):
            User(
                email="john@doe.com",
                password="   ",
                first_name="John",
                last_name="Doe"
            )

    def test_user_password_cannot_contain_whitespace(self):
        with pytest.raises(ValueError):
            User(
                email="john@doe.com",
                password="pass word",
                first_name="John",
                last_name="Doe"
            )

    def test_user_password_is_hashed(self):
        user = User(
            email="john@doe.com",
            password="password123",
            first_name="John",
            last_name="Doe"
        )
        assert user.password != "password123"

class TestUserUpdateModel:

    def test_user_update_passwords_must_match(self):
        with pytest.raises(ValueError):
            UserUpdate(
                password="password123",
                confirm_password="differentpassword"
            )

    def test_user_update_passwords_did_not_confirm(self):
        with pytest.raises(ValueError):
            UserUpdate(
                password="password123"
            )
