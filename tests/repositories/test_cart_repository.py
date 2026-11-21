import pytest

from tests.util.builders import create_test_cart
from tests.util.fixtures import cart_repository

@pytest.mark.anyio
async def test_has_cart_for_existing_user(cart_repository):
    user_id = "test_customer_001"
    await cart_repository.add_record(create_test_cart(customer_id=user_id))

    assert await cart_repository.has_cart_for_user(user_id)

@pytest.mark.anyio
async def test_has_cart_for_non_existing_user_returns_false(cart_repository):
    user_id = "non_existing_user"

    assert not await cart_repository.has_cart_for_user(user_id)

@pytest.mark.anyio
async def test_get_cart_by_customer_id_returns_cart(cart_repository):
    await cart_repository.add_record(create_test_cart(customer_id="c1"))
    cart = await cart_repository.get_cart_by_customer_id("c1")
    assert cart.customer_id == "c1"

@pytest.mark.anyio
async def test_get_cart_by_customer_id_returns_none(cart_repository):
    assert await cart_repository.get_cart_by_customer_id("nobody") is None