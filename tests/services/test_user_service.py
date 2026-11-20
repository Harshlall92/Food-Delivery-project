import pytest

from app.schemas.restaurant import Restaurant
from app.services.exceptions import UserNotFoundError, DuplicateItemError, RestaurantNotFoundError, ItemNotFoundError
from app.schemas.user import Customer, UserCreate, UserUpdate
from app.services.user_service import *
from tests.util.helpers import create_test_customer, create_test_restaurant_owner
from tests.util.fixtures import *

class TestUserService:

    class TestCreateCustomerAccount:

        @pytest.mark.anyio
        async def test_create_customer_account(self, user_repository):
            data = UserCreate(
                email="test@example.com",
                password="password123",
                confirm_password="password123",
                first_name="John",
                last_name="Doe"
            )

            result = await create_customer(user_repository, data)

            assert isinstance(result, Customer)
            assert result.email == data.email
            assert result.first_name == data.first_name
            assert result.last_name == data.last_name

            contents = await user_repository._read_file()

            assert len(contents) == 1

        @pytest.mark.anyio
        async def test_create_customer_raises_duplicate_error(self, user_repository):
            existing_customer = create_test_customer()
            await user_repository.add_record(existing_customer)

            data = UserCreate(
                email=existing_customer.email,
                password="password123",
                confirm_password="password123",
                first_name="Jane",
                last_name="Smith"
            )

            with pytest.raises(DuplicateItemError, match=f"Customer with email {existing_customer.email} already exists."):
                await create_customer(user_repository, data)

    class TestUpdateCustomerAccount:

        @pytest.mark.anyio
        async def test_update_customer_account(self, user_repository):
            customer = create_test_customer()
            await user_repository.add_record(customer)

            customer_id = customer.id

            update_data = UserUpdate(
                email="new_email@test.com",
                password="newpassword",
                confirm_password="newpassword",
                first_name="Tim",
                last_name="Apple",
                active=False
            )

            result = await update_customer(user_repository, customer_id, update_data)

            assert isinstance(result, Customer)
            assert result.email == update_data.email
            assert result.first_name == update_data.first_name
            assert result.last_name == update_data.last_name
            assert result.active == update_data.active

            updated = await user_repository.get_by_id(customer_id)

            assert updated is not None
            assert updated.email == update_data.email
            assert updated.password != customer.password  # Password should be hashed and different
            assert updated.first_name == update_data.first_name
            assert updated.last_name == update_data.last_name
            assert updated.active == update_data.active

        @pytest.mark.anyio
        async def test_update_customer_raises_user_not_found_error_on_nonexistent_user(self, user_repository):

            non_existent_id = "non-existent-id"

            update_data = UserUpdate(
                email="new_email@test.com",
                password="newpassword",
                confirm_password="newpassword",
                first_name="Tim",
                last_name="Apple",
                active=False
            )

            with pytest.raises(UserNotFoundError, match=f"Customer with ID {non_existent_id} not found."):
                await update_customer(user_repository, non_existent_id, update_data)

        @pytest.mark.anyio
        async def test_update_raises_duplicate_error_on_email_conflict(self, user_repository):
            customer = create_test_customer()
            other_customer = create_test_customer(email="other@example.com")

            await user_repository.add_record(customer)
            await user_repository.add_record(other_customer)

            with pytest.raises(DuplicateItemError, match=f"Customer with email {other_customer.email} already exists."):
                await update_customer(user_repository, customer.id, UserUpdate(email=other_customer.email))

    class TestCreateRestaurantOwnerAccount:

        @pytest.mark.anyio
        async def test_create_restaurant_owner_account(self, user_repository):
            data = UserCreate(
                email="restaurant_owner@example.com",
                password="password123",
                confirm_password="password123",
                first_name="Alice",
                last_name="Smith"
            )

            result = await create_restaurant_owner(user_repository, data)

            assert isinstance(result, RestaurantOwner)
            assert result.email == data.email
            assert result.first_name == data.first_name
            assert result.last_name == data.last_name
            assert result.restaurant_id is None  # Since restaurant_id is optional and not provided

            contents = await user_repository._read_file()

            assert len(contents) == 1

        @pytest.mark.anyio
        async def test_create_restaurant_owner_raises_duplicate_error(self, user_repository):
            existing_owner = create_test_restaurant_owner() 
            await user_repository.add_record(existing_owner)

            data = UserCreate(
                email=existing_owner.email,
                password="password123",
                confirm_password="password123",
                first_name="Bob",
                last_name="Johnson"
            )

            with pytest.raises(DuplicateItemError, match=f"Restaurant owner with email {existing_owner.email} already exists."):
                await create_restaurant_owner(user_repository, data)

    class TestUpdateRestaurantOwnerAccount:

        @pytest.mark.anyio
        async def test_update_restaurant_owner_account(self, user_repository, restaurant_repository):

            owner = create_test_restaurant_owner()
            await user_repository.add_record(owner)

            restaurant = Restaurant(
                name="Test Restaurant",
                address="123 Test St",
                cuisine="test",
            )
            await restaurant_repository.add_record(restaurant)

            update_data = RestaurantOwnerUpdate(
                restaurant_id=restaurant.id,
            )

            result = await update_restaurant_owner(user_repository, restaurant_repository, owner.id, update_data)

            assert isinstance(result, RestaurantOwner)
            assert result.email == owner.email
            assert result.restaurant_id == restaurant.id

            contents = await user_repository._read_file()

            assert contents[0]["restaurant_id"] == restaurant.id

        @pytest.mark.anyio
        async def test_update_restaurant_owner_raises_user_not_found_error_on_nonexistent_user(self, user_repository, restaurant_repository):

            non_existent_id = "non-existent-id"

            update_data = RestaurantOwnerUpdate(
                restaurant_id="some-restaurant-id"
            )

            with pytest.raises(UserNotFoundError, match=f"Restaurant owner with ID {non_existent_id} not found."):
                await update_restaurant_owner(user_repository, restaurant_repository, non_existent_id, update_data)

        @pytest.mark.anyio
        async def test_update_restaurant_owner_raises_restaurant_not_found_error_on_nonexistent_restaurant(self, user_repository, restaurant_repository):

            owner = create_test_restaurant_owner()
            await user_repository.add_record(owner)

            non_existent_restaurant_id = "nonexistent-restaurant-id"

            update_data = RestaurantOwnerUpdate(
                restaurant_id=non_existent_restaurant_id
            )

            with pytest.raises(RestaurantNotFoundError, match=f"Restaurant with ID {non_existent_restaurant_id} does not exist."):
                await update_restaurant_owner(user_repository, restaurant_repository, owner.id, update_data)    

    class TestAddCustomerAddress:

        @pytest.mark.anyio
        async def test_add_customer_address(self, user_repository):
            customer = create_test_customer()
            await user_repository.add_record(customer)

            address = CustomerAddress(
                label="Home",
                address_line_1="123 Main St",
                city="Anytown",
                province="BC",
                postal_code="A1B 2C3",
            )

            result = await add_customer_address(user_repository, customer.id, address)

            assert isinstance(result, Customer)
            assert len(result.addresses) == 1
            assert result.addresses[0].label == address.label

            contents = await user_repository._read_file()

            assert len(contents[0]["addresses"]) == 1
            assert contents[0]["addresses"][0]["label"] == address.label

        @pytest.mark.anyio
        async def test_add_customer_address_raises_user_not_found_error_on_nonexistent_user(self, user_repository):
            non_existent_id = "non-existent-id"

            address = CustomerAddress(
                label="Home",
                address_line_1="123 Main St",
                city="Anytown",
                province="BC",
                postal_code="A1B 2C3",
            )

            with pytest.raises(UserNotFoundError, match=f"Customer with ID {non_existent_id} not found."):
                await add_customer_address(user_repository, non_existent_id, address)

        @pytest.mark.anyio
        async def test_add_customer_address_raises_value_error_on_non_customer(self, user_repository):
            non_customer = create_test_restaurant_owner()
            await user_repository.add_record(non_customer)

            address = CustomerAddress(
                label="Home",
                address_line_1="123 Main St",
                city="Anytown",
                province="BC",
                postal_code="A1B 2C3",
            )

            with pytest.raises(ValueError, match=f"User with ID {non_customer.id} is not a customer."):
                await add_customer_address(user_repository, non_customer.id, address)

        @pytest.mark.anyio
        async def test_add_customer_address_raises_duplicate_error_on_duplicate_label(self, user_repository):
            customer = create_test_customer()
            await user_repository.add_record(customer)

            address1 = CustomerAddress(
                label="Home",
                address_line_1="123 Main St",
                city="Anytown",
                province="BC",
                postal_code="A1B 2C3",
            )

            await add_customer_address(user_repository, customer.id, address1)

            address2 = CustomerAddress(
                label="Home",  # Same label as address1
                address_line_1="456 Elm St",
                city="Othertown",
                province="BC",
                postal_code="D4E 5F6",
            )

            with pytest.raises(DuplicateItemError, match=f"Address with label {address2.label} already exists for this customer."):
                await add_customer_address(user_repository, customer.id, address2)

    class TestUpdateCustomerAddress:

        @pytest.mark.anyio
        async def test_update_customer_address(self, user_repository):
            customer = create_test_customer()
            await user_repository.add_record(customer)

            address1 = CustomerAddress(
                label="Home",
                address_line_1="123 Main St",
                city="Anytown",
                province="BC",
                postal_code="A1B 2C3",
            )

            await add_customer_address(user_repository, customer.id, address1)

            new_address = CustomerAddress(
                label="Work",  # Same label to update
                address_line_1="456 Elm St",
                city="Othertown",
                province="BC",
                postal_code="D4E 5F6",
            )

            result = await update_customer_address(user_repository, customer.id, "Home", new_address)

            assert isinstance(result, Customer)
            assert len(result.addresses) == 1
            assert result.addresses[0].label == new_address.label
            assert result.addresses[0].address_line_1 == new_address.address_line_1

            contents = await user_repository._read_file()

            assert len(contents[0]["addresses"]) == 1
            assert contents[0]["addresses"][0]["label"] == new_address.label
            assert contents[0]["addresses"][0]["address_line_1"] == new_address.address_line_1

        @pytest.mark.anyio
        async def test_update_customer_address_raises_not_found_error_on_nonexistent_address(self, user_repository):
            customer = create_test_customer()
            await user_repository.add_record(customer)

            new_address = CustomerAddress(
                label="Work",
                address_line_1="456 Elm St",
                city="Othertown",
                province="BC",
                postal_code="D4E 5F6",
            )

            with pytest.raises(ItemNotFoundError, match=f"Address with label {new_address.label} not found for this customer."):
                await update_customer_address(user_repository, customer.id, "Work", new_address)

        @pytest.mark.anyio
        async def test_update_customer_address_raises_user_not_found_error_on_nonexistent_user(self, user_repository):
            non_existent_id = "non-existent-id"

            new_address = CustomerAddress(
                label="Work",
                address_line_1="456 Elm St",
                city="Othertown",
                province="BC",
                postal_code="D4E 5F6",
            )

            with pytest.raises(UserNotFoundError, match=f"Customer with ID {non_existent_id} not found."):
                await update_customer_address(user_repository, non_existent_id, "Work", new_address)

        @pytest.mark.anyio
        async def test_update_customer_address_raises_value_error_on_non_customer(self, user_repository):
            non_customer = create_test_restaurant_owner()
            await user_repository.add_record(non_customer)

            new_address = CustomerAddress(
                label="Work",
                address_line_1="456 Elm St",
                city="Othertown",
                province="BC",
                postal_code="D4E 5F6",
            )

            with pytest.raises(ValueError, match=f"User with ID {non_customer.id} is not a customer."):
                await update_customer_address(user_repository, non_customer.id, "Work", new_address)