import pytest

from app.repositories.exceptions import DuplicateRecordError
from tests.util.builders import create_test_order_item
from tests.util.fixtures import order_item_repository


@pytest.mark.anyio
async def test_add_order_items_persists_all_items(order_item_repository):
    items = [create_test_order_item(order_id="o1"), create_test_order_item(order_id="o1", quantity=2)]

    assert await order_item_repository.add_order_items(items) == items
    assert await order_item_repository.get_all() == items

@pytest.mark.anyio
async def test_get_items_by_order_id(order_item_repository):
    mine = create_test_order_item(order_id="o1")
    await order_item_repository.add_order_items([mine, create_test_order_item(order_id="o2")])

    assert await order_item_repository.get_items_by_order_id("o1") == [mine]

@pytest.mark.anyio
async def test_get_items_by_order_id_returns_empty_list(order_item_repository):
    assert await order_item_repository.get_items_by_order_id("missing") == []

@pytest.mark.anyio
async def test_add_order_items_rejects_duplicate_id(order_item_repository):
    item = create_test_order_item()
    await order_item_repository.add_order_items([item])

    with pytest.raises(DuplicateRecordError):
        await order_item_repository.add_order_items([item])