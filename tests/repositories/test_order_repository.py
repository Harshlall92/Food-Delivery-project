import pytest

from tests.util.builders import create_test_order
from tests.util.fixtures import order_repository


@pytest.mark.anyio
async def test_add_and_get_order_by_id(order_repository):
    order = create_test_order()
    await order_repository.add_record(order)

    assert await order_repository.get_by_id(order.id) == order

@pytest.mark.anyio
async def test_get_order_by_id_returns_none_if_not_found(order_repository):
    assert await order_repository.get_by_id("missing") is None

@pytest.mark.anyio
async def test_get_all_orders(order_repository):
    first, second = create_test_order(), create_test_order()
    await order_repository.add_record(first)
    await order_repository.add_record(second)

    assert await order_repository.get_all() == [first, second]

@pytest.mark.anyio
async def test_update_order_status(order_repository):
    order = create_test_order()
    await order_repository.add_record(order)

    updated = await order_repository.update_record(order.id, order.model_copy(update={"status": "confirmed"}))

    assert updated.status == "confirmed"
    assert (await order_repository.get_by_id(order.id)).status == "confirmed"

@pytest.mark.anyio
async def test_get_orders_by_customer_id(order_repository):
    mine = create_test_order(customer_id="c1")
    await order_repository.add_record(mine)
    await order_repository.add_record(create_test_order(customer_id="c2"))

    assert await order_repository.get_orders_by_customer_id("c1") == [mine]

@pytest.mark.anyio
async def test_get_orders_by_restaurant_id(order_repository):
    mine = create_test_order(restaurant_id="r1")
    await order_repository.add_record(mine)
    await order_repository.add_record(create_test_order(restaurant_id="r2"))

    assert await order_repository.get_orders_by_restaurant_id("r1") == [mine]

@pytest.mark.anyio
async def test_get_orders_by_status(order_repository):
    ready = create_test_order(status="ready")
    await order_repository.add_record(ready)
    await order_repository.add_record(create_test_order(status="pending"))

    assert await order_repository.get_orders_by_status("ready") == [ready]