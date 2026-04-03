"""
test_ecommerce_web.py
Suite de pruebas automatizadas para la aplicación web del e-commerce.
Herramienta: Selenium 4 + pytest
Navegadores: Chrome, Firefox, Edge (parametrizados en conftest.py)
"""

import pytest
from pages.login_page    import LoginPage
from pages.checkout_page import CheckoutPage

# ── Constantes de prueba ──────────────────────────────────────────────────────
BASE_URL     = "https://www.mitienda.com"
PRODUCT_URL  = f"{BASE_URL}/products/camiseta-premium"
OOS_URL      = f"{BASE_URL}/products/agotado-test"  # producto sin stock

VALID_USER = {
    "email":    "qa_test@correo.com",
    "password": "Pass@1234",
}
TEST_CARD = {
    "number": "4111111111111111",  # Tarjeta Visa de prueba (Stripe)
    "expiry": "12/26",
    "cvv":    "123",
}

# ══════════════════════════════════════════════════════════════════════════════
# TC-WEB-01 a TC-WEB-04 — Módulo de Autenticación
# ══════════════════════════════════════════════════════════════════════════════

class TestLoginWeb:
    """Casos de prueba para el módulo de login en la aplicación web."""

    def test_login_exitoso(self, driver):
        """
        TC-WEB-01: Usuario con credenciales válidas inicia sesión correctamente.
        Precondición: usuario registrado en la base de datos.
        Resultado esperado: banner de bienvenida visible tras el login.
        """
        driver.get(f"{BASE_URL}/login")
        page = LoginPage(driver)
        page.login(VALID_USER["email"], VALID_USER["password"])

        assert page.is_logged_in(), \
            "El banner de bienvenida no apareció: el login falló con credenciales válidas."

    @pytest.mark.parametrize("email, pwd, expected_error", [
        ("noexiste@mail.com",   "Pass@1234",  "Credenciales incorrectas"),
        ("qa_test@correo.com",  "wrongpass",  "Credenciales incorrectas"),
        ("",                    "",           "El email es requerido"),
    ])
    def test_login_credenciales_invalidas(self, driver, email, pwd, expected_error):
        """
        TC-WEB-02/03/04: Credenciales inválidas deben mostrar el mensaje de error correcto.
        Cubre: usuario inexistente, contraseña incorrecta, campos vacíos.
        """
        driver.get(f"{BASE_URL}/login")
        page = LoginPage(driver)
        page.login(email, pwd)

        actual_error = page.get_error_message()
        assert expected_error in actual_error, \
            f"Error esperado: '{expected_error}' | Error obtenido: '{actual_error}'"


# ══════════════════════════════════════════════════════════════════════════════
# TC-WEB-05 a TC-WEB-07 — Módulo de Checkout
# ══════════════════════════════════════════════════════════════════════════════

class TestCheckoutWeb:
    """Casos de prueba para el flujo de compra en la aplicación web."""

    @pytest.fixture(autouse=True)
    def login_before_each(self, driver):
        """
        Precondición: autenticar al usuario antes de cada test del módulo.
        Se ejecuta automáticamente gracias a autouse=True.
        """
        driver.get(f"{BASE_URL}/login")
        LoginPage(driver).login(VALID_USER["email"], VALID_USER["password"])

    def test_agregar_producto_al_carrito(self, driver):
        """
        TC-WEB-05: Al agregar un producto, el badge del carrito debe incrementar.
        Resultado esperado: cart_badge >= 1.
        """
        page  = CheckoutPage(driver)
        count = page.add_product_to_cart(PRODUCT_URL)

        assert int(count) >= 1, \
            f"El carrito debería tener al menos 1 ítem, pero muestra: {count}"

    def test_compra_exitosa_end_to_end(self, driver):
        """
        TC-WEB-06: Flujo completo de compra genera un Order ID con prefijo 'ORD-'.
        Cubre: agregar al carrito → checkout → pago → confirmación.
        """
        page = CheckoutPage(driver)
        page.add_product_to_cart(PRODUCT_URL)
        page.go_to_checkout()
        page.fill_payment_form(
            TEST_CARD["number"],
            TEST_CARD["expiry"],
            TEST_CARD["cvv"],
        )
        order_id = page.complete_order()

        assert order_id.startswith("ORD-"), \
            f"El Order ID generado no tiene el formato esperado: '{order_id}'"

    def test_producto_fuera_de_stock_deshabilitado(self, driver):
        """
        TC-WEB-07: El botón 'Agregar al carrito' debe estar deshabilitado
        cuando el producto no tiene stock disponible.
        """
        driver.get(OOS_URL)
        page = CheckoutPage(driver)

        assert page.is_add_to_cart_disabled(), \
            "El botón 'Agregar' debería estar deshabilitado para productos sin stock."
