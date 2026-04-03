"""
checkout_page.py
Page Object para las pantallas de Producto y Checkout (web).
Cubre el flujo: agregar al carrito → pagar → confirmación.
"""

from selenium.webdriver.common.by import By
from .base_page import BasePage


class CheckoutPage(BasePage):
    """Page Object que cubre el flujo de compra en la aplicación web."""

    # ── Locators — Ficha de producto ─────────────────────────────────────────
    PRODUCT_TITLE   = (By.CSS_SELECTOR, ".product-name")
    PRODUCT_PRICE   = (By.CSS_SELECTOR, ".product-price")
    ADD_TO_CART_BTN = (By.ID,           "add-to-cart")
    CART_COUNT      = (By.CSS_SELECTOR, ".cart-badge")
    OUT_OF_STOCK    = (By.CSS_SELECTOR, ".out-of-stock-label")

    # ── Locators — Carrito ────────────────────────────────────────────────────
    CHECKOUT_BTN    = (By.ID,           "go-to-checkout")
    CART_ITEMS      = (By.CSS_SELECTOR, ".cart-item")

    # ── Locators — Formulario de pago ─────────────────────────────────────────
    CARD_NUMBER     = (By.ID,           "card-number")
    CARD_EXPIRY     = (By.ID,           "card-expiry")
    CARD_CVV        = (By.ID,           "card-cvv")
    CONFIRM_BTN     = (By.ID,           "confirm-order")

    # ── Locators — Confirmación ───────────────────────────────────────────────
    SUCCESS_MSG     = (By.CSS_SELECTOR, ".order-success")
    ORDER_ID        = (By.CSS_SELECTOR, ".order-id-value")

    # ── Acciones ──────────────────────────────────────────────────────────────

    def open_product(self, product_url: str):
        """Navega directamente a la URL de un producto."""
        self.driver.get(product_url)

    def add_product_to_cart(self, product_url: str) -> str:
        """
        Navega al producto y lo agrega al carrito.
        Retorna el texto actual del badge del carrito.
        """
        self.open_product(product_url)
        self.click(self.ADD_TO_CART_BTN)
        return self.get_text(self.CART_COUNT)

    def is_add_to_cart_disabled(self) -> bool:
        """Retorna True si el botón 'Agregar' está deshabilitado (stock = 0)."""
        btn = self.find(self.ADD_TO_CART_BTN)
        return not btn.is_enabled()

    def go_to_checkout(self):
        """Navega a la pantalla de pago desde el carrito."""
        self.click(self.CHECKOUT_BTN)

    def fill_payment_form(self, card_number: str, expiry: str, cvv: str):
        """Rellena los campos del formulario de pago con tarjeta."""
        self.type_text(self.CARD_NUMBER, card_number)
        self.type_text(self.CARD_EXPIRY, expiry)
        self.type_text(self.CARD_CVV,    cvv)

    def complete_order(self) -> str:
        """
        Confirma la orden y espera la pantalla de éxito.
        Retorna el Order ID generado.
        """
        self.click(self.CONFIRM_BTN)
        self.find(self.SUCCESS_MSG)  # espera implícita a la confirmación
        return self.get_text(self.ORDER_ID)

    def get_cart_item_count(self) -> int:
        """Retorna la cantidad de ítems distintos en el carrito."""
        return len(self.driver.find_elements(*self.CART_ITEMS))
