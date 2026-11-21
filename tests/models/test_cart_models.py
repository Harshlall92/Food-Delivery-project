from decimal import Decimal

from pydantic_core import ValidationError
import pytest

from tests.util.builders import create_test_cart_item
from app.schemas.cart import Cart, CartItem, CartItemAdd

from app.schemas.cart import CartItemResponse, CartResponse, CartCreate


class TestCartItemModel:

    def test_cart_item_model_valid(self):
        cart_item = CartItem(
            menu_item_id="menu_item_123",
            quantity=2,
            price=Decimal("9.99")
        )

        assert cart_item.menu_item_id == "menu_item_123"
        assert cart_item.quantity == 2
        assert cart_item.price == Decimal("9.99")

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

    def test_price_is_immutable(self):
        cart_item = create_test_cart_item()
        with pytest.raises(ValidationError):
            cart_item.price = Decimal("19.99")

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

class TestCartResponseModels:

    def test_cart_item_response_valid(self):
        item = CartItemResponse(menu_item_name="Pizza", quantity=2, price=Decimal("5.00"))
        assert item.menu_item_name == "Pizza"
        assert item.price == Decimal("5.00")

    @pytest.mark.parametrize("quantity", [0, -1])
    def test_cart_item_response_invalid_quantity(self, quantity):
        with pytest.raises(ValidationError):
            CartItemResponse(menu_item_name="Pizza", quantity=quantity, price=Decimal("5.00"))

    def test_cart_response_allows_empty_cart(self):
        cart = CartResponse(restaurant_name="R", items=[], total_quantity=0, sub_total=Decimal("0.00"))
        assert cart.total_quantity == 0

class TestCartCreateModel:

    def test_cart_create_valid(self):
        cart_create = CartCreate(customer_id="customer_123", menu_item_id="menu_item_123", quantity=2)

        assert isinstance(cart_create, CartItemAdd)
        assert cart_create.customer_id == "customer_123"
        assert cart_create.menu_item_id == "menu_item_123"
        assert cart_create.quantity == 2

    def test_cart_create_quantity_defaults_to_one(self):
        cart_create = CartCreate(customer_id="customer_123", menu_item_id="menu_item_123")
        assert cart_create.quantity == 1

    @pytest.mark.parametrize("quantity", [0, -1])
    def test_cart_create_invalid_quantity(self, quantity: int):
        with pytest.raises(ValidationError):
            CartCreate(customer_id="customer_123", menu_item_id="menu_item_123", quantity=quantity)

    def test_cart_create_missing_customer_id(self):
        with pytest.raises(ValidationError):
            CartCreate(menu_item_id="menu_item_123")

    def test_cart_create_empty_customer_id(self):
        with pytest.raises(ValidationError):
            CartCreate(customer_id="", menu_item_id="menu_item_123")