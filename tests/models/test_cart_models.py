from decimal import Decimal

from pydantic_core import ValidationError
import pytest

from tests.util.builders import create_test_cart_item
from app.schemas.cart import Cart, CartItem, CartItemAdd


class TestCartItemModel:

    def test_cart_item_model_valid(self):
        cart_item = CartItem(
            menu_item_id="menu_item_123",
            quantity=2,
            price=Decimal("9.99")
        )

        assert cart_item.menu_item_id == "menu_item_123"
        assert cart_item.quantity == 2
        assert cart_item.price_per_item == Decimal("9.99")

    @pytest.mark.parametrize("quantity", [0, -1, -5])
    def test_cart_item_model_invalid_quantity(self, quantity: int):
        with pytest.raises(ValidationError):
            CartItem(
                menu_item_id="menu_item_123",
                quantity=quantity,
                price=Decimal("9.99")
            )

    @pytest.mark.parametrize("price", ["-1.00", "0.00", "9.999", "10000000000.00"])
    def test_cart_item_model_invalid_price(self, price: str):
        with pytest.raises(ValidationError):
            CartItem(
                menu_item_id="menu_item_123",
                quantity=2,
                price=Decimal(price)
            )

    def test_menu_item_id_is_immutable(self):
        cart_item = create_test_cart_item()
        with pytest.raises(ValidationError):
            cart_item.menu_item_id = "new_menu_item_id"

    def test_price_per_item_is_immutable(self):
        cart_item = create_test_cart_item()
        with pytest.raises(ValidationError):
            cart_item.price_per_item = Decimal("19.99")

class TestCartModel:
    
    def test_cart_model_valid(self):
        cart = Cart(
            customer_id="customer_123",
            restaurant_id="restaurant_456",
            items=[],
            subtotal=Decimal("19.98")
        )

        assert cart.customer_id == "customer_123"
        assert cart.restaurant_id == "restaurant_456"
        assert len(cart.items) == 0
        assert cart.subtotal == Decimal("19.98")

    def test_items_parameter_defaults_to_empty_list(self):
        cart = Cart(
            customer_id="customer_123",
            restaurant_id="restaurant_456",
            subtotal=Decimal("19.98")
        )

        assert cart.customer_id == "customer_123"
        assert cart.restaurant_id == "restaurant_456"
        assert len(cart.items) == 0
        assert cart.subtotal == Decimal("19.98")

    def test_subtotal_parameter_defaults_to_zero(self):
        cart = Cart(
            customer_id="customer_123",
            restaurant_id="restaurant_456",
            items=[]
        )

        assert cart.customer_id == "customer_123"
        assert cart.restaurant_id == "restaurant_456"
        assert len(cart.items) == 0
        assert cart.subtotal == Decimal("0.00")

    @pytest.mark.parametrize("subtotal", ["-1.00", "9.999", "10000000000.00"])
    def test_cart_model_invalid_subtotal(self, subtotal: str):
        with pytest.raises(ValidationError):
            Cart(
                customer_id="customer_123",
                restaurant_id="restaurant_456",
                subtotal=Decimal(subtotal)
            )

    def test_customer_id_is_immutable(self):
        cart = Cart(
            customer_id="customer_123",
            restaurant_id="restaurant_456",
            items=[],
            subtotal=Decimal("19.98")
        )
        with pytest.raises(ValidationError):
            cart.customer_id = "new_customer_id"

    def test_restaurant_id_is_immutable(self):
        cart = Cart(
            customer_id="customer_123",
            restaurant_id="restaurant_456",
            items=[],
            subtotal=Decimal("19.98")
        )
        with pytest.raises(ValidationError):
            cart.restaurant_id = "new_restaurant_id"

class TestCartItemAddModel:

    def test_cart_item_add_model_valid(self):
        cart_item_add = CartItemAdd(
            menu_item_id="menu_item_123",
            quantity=2
        )

        assert cart_item_add.menu_item_id == "menu_item_123"
        assert cart_item_add.quantity == 2

    @pytest.mark.parametrize("quantity", [0, -1, -5])
    def test_cart_item_add_model_invalid_quantity(self, quantity: int):
        with pytest.raises(ValidationError):
            CartItemAdd(
                menu_item_id="menu_item_123",
                quantity=quantity
            )