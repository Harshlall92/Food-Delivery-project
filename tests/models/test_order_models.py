from datetime import datetime
from decimal import Decimal

from pydantic_core import ValidationError
import pytest

from tests.util.builders import create_test_order, create_test_order_item
from app.schemas.order import Order, OrderCreate, OrderItem, OrderStatusUpdate


class TestOrderStatus:

    @pytest.mark.parametrize("status", ["pending", "confirmed", "preparing", "ready", "picked up", "delivered", "cancelled"])
    def test_valid_status(self, status: str):
        assert create_test_order(status=status).status == status
        assert OrderStatusUpdate(status=status).status == status

    @pytest.mark.parametrize("status", ["shipped", "Pending", "picked_up", ""])
    def test_invalid_status(self, status: str):
        with pytest.raises(ValidationError):
            create_test_order(status=status)
        with pytest.raises(ValidationError):
            OrderStatusUpdate(status=status)

    def test_status_defaults_to_pending(self):
        order = Order(customer_id="customer_123", restaurant_id="restaurant_456", total=Decimal("0.00"))
        assert order.status == "pending"


class TestOrderModel:

    def test_order_model_valid(self):
        order = create_test_order(customer_id="customer_123", restaurant_id="restaurant_456", total="19.98")

        assert order.id
        assert order.customer_id == "customer_123"
        assert order.restaurant_id == "restaurant_456"
        assert isinstance(order.order_date, datetime)
        assert order.total == Decimal("19.98")

    @pytest.mark.parametrize("total", ["-1.00", "9.999", "10000000000.00"])
    def test_order_model_invalid_total(self, total: str):
        with pytest.raises(ValidationError):
            create_test_order(total=total)

    def test_order_model_missing_customer_id(self):
        with pytest.raises(ValidationError):
            Order(restaurant_id="restaurant_456", total=Decimal("10.00"))

    def test_order_id_is_immutable(self):
        order = create_test_order()
        with pytest.raises(ValidationError):
            order.id = "new_id"


class TestOrderItemModel:

    def test_order_item_model_valid(self):
        item = create_test_order_item(order_id="order_123", menu_item_id="menu_item_123", quantity=2, price_per_item="9.99")

        assert item.id
        assert item.order_id == "order_123"
        assert item.menu_item_id == "menu_item_123"
        assert item.quantity == 2
        assert item.price_per_item == Decimal("9.99")

    @pytest.mark.parametrize("quantity", [0, -1])
    def test_order_item_invalid_quantity(self, quantity: int):
        with pytest.raises(ValidationError):
            create_test_order_item(quantity=quantity)

    @pytest.mark.parametrize("price", ["-1.00", "9.999"])
    def test_order_item_invalid_price(self, price: str):
        with pytest.raises(ValidationError):
            create_test_order_item(price_per_item=price)

    def test_order_item_missing_order_id(self):
        with pytest.raises(ValidationError):
            OrderItem(menu_item_id="menu_item_123", quantity=1, price_per_item=Decimal("9.99"))


class TestOrderCreateModel:

    def test_order_create_valid(self):
        assert OrderCreate(customer_id="customer_123").customer_id == "customer_123"

    def test_order_create_missing_customer_id(self):
        with pytest.raises(ValidationError):
            OrderCreate()