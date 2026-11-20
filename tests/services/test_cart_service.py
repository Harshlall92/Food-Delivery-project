import pytest

from app.services.carts_service import *
from tests.util.fixtures import cart_repository
from tests.util.builders import create_test_cart

class TestDeleteCart:

    @pytest.mark.anyio
    async def test_delete_cart_success(self, cart_repository):
        await cart_repository.add_record(create_test_cart(customer_id="test_user_id"))

        assert await delete_cart(cart_repository, "test_user_id")

    @pytest.mark.anyio
    async def test_delete_cart_not_found(self, cart_repository):
        assert not await delete_cart(cart_repository, "non_existent_user_id")


        