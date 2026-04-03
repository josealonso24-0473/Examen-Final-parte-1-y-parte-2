"""
test_ecommerce_mobile.py
Suite de pruebas automatizadas para la app móvil del e-commerce.
Herramienta: Appium 2.x + pytest
Plataformas: Android 13 (UIAutomator2) · iOS 17 (XCUITest)
"""

import pytest
from appium.webdriver.common.appiumby    import AppiumBy
from mobile_pages.mobile_login_page      import MobileLoginPage
from mobile_pages.mobile_product_page    import MobileProductPage

# ── Constantes de prueba ──────────────────────────────────────────────────────
VALID_USER = {
    "email":    "qa_mobile@correo.com",
    "password": "Pass@1234",
}

# ══════════════════════════════════════════════════════════════════════════════
# TC-MOB-01 / TC-MOB-02 — Módulo de Autenticación Móvil
# ══════════════════════════════════════════════════════════════════════════════

class TestLoginMobile:
    """Casos de prueba para el módulo de login en la app móvil."""

    def test_login_exitoso_movil(self, mobile_driver):
        """
        TC-MOB-01: Usuario con credenciales válidas accede a la pantalla principal.
        Aplica en: Android 13 (Galaxy S23) y iOS 17 (iPhone 15 Pro).
        """
        page = MobileLoginPage(mobile_driver)
        page.login(VALID_USER["email"], VALID_USER["password"])

        assert page.is_home_visible(), \
            "La pantalla home no cargó correctamente tras el login."

    def test_login_credenciales_invalidas_toast(self, mobile_driver):
        """
        TC-MOB-02: Credenciales incorrectas deben mostrar un toast de error nativo.
        Verifica que la UI móvil maneje errores de autenticación visualmente.
        """
        page = MobileLoginPage(mobile_driver)
        page.login("incorrecto@mail.com", "wrongpass")

        assert page.is_error_toast_visible(), \
            "El toast de error no apareció tras ingresar credenciales inválidas."


# ══════════════════════════════════════════════════════════════════════════════
# TC-MOB-03 a TC-MOB-06 — Módulo de Producto y Checkout Móvil
# ══════════════════════════════════════════════════════════════════════════════

class TestProductoMobile:
    """Casos de prueba para el flujo de producto y compra en la app móvil."""

    @pytest.fixture(autouse=True)
    def login_before_each(self, mobile_driver):
        """
        Precondición: iniciar sesión antes de cada test del módulo.
        """
        MobileLoginPage(mobile_driver).login(
            VALID_USER["email"],
            VALID_USER["password"],
        )

    def test_swipe_galeria_producto(self, mobile_driver):
        """
        TC-MOB-03: El gesto swipe hacia la izquierda debe cambiar la imagen
        activa en la galería del producto.
        Prueba exclusiva de la app móvil; no aplicable en Selenium web.
        """
        page       = MobileProductPage(mobile_driver)
        img_before = page.get_current_gallery_image_desc()
        page.swipe_product_gallery()
        img_after  = page.get_current_gallery_image_desc()

        assert img_before != img_after, \
            "La imagen de la galería no cambió después del gesto swipe."

    def test_agregar_al_carrito_movil(self, mobile_driver):
        """
        TC-MOB-04: El botón FAB 'Agregar al carrito' debe incrementar el badge
        de cantidad en la barra de navegación inferior.
        """
        page  = MobileProductPage(mobile_driver)
        count = page.add_to_cart()

        assert int(count) >= 1, \
            f"El badge del carrito debería ser >= 1, valor actual: '{count}'"

    def test_compra_completa_movil(self, mobile_driver):
        """
        TC-MOB-05: Flujo end-to-end en dispositivo móvil.
        El pago utiliza la tarjeta de prueba pre-configurada en el entorno QA.
        Resultado esperado: pantalla de orden exitosa visible.
        """
        page = MobileProductPage(mobile_driver)
        page.add_to_cart()
        page.go_to_checkout()
        # El formulario de pago en QA acepta automáticamente la tarjeta de prueba
        assert page.is_order_success_visible(), \
            "La pantalla de confirmación de orden no apareció tras el checkout."

    def test_modo_offline_muestra_banner(self, mobile_driver):
        """
        TC-MOB-06: Al perder la conexión de red, la app debe mostrar un banner
        informativo de modo offline en lugar de un error silencioso.
        Prueba exclusiva móvil usando la API de red de Appium.
        """
        # Activar modo avión (0 = sin red)
        mobile_driver.set_network_connection(0)
        page = MobileProductPage(mobile_driver)

        try:
            page.add_to_cart()
        except Exception:
            pass  # Se espera que la acción falle sin red

        assert page.is_offline_banner_visible(), \
            "El banner de modo offline no se mostró al perder la conexión."

        # Restaurar conectividad (6 = WiFi + datos móviles)
        mobile_driver.set_network_connection(6)

    def test_incrementar_cantidad_producto(self, mobile_driver):
        """
        TC-MOB-07: El botón '+' de cantidad debe incrementar el valor del campo
        numérico correctamente.
        """
        page = MobileProductPage(mobile_driver)
        page.increase_quantity(times=3)
        qty = page.get_quantity()

        assert qty == 4, \
            f"La cantidad debería ser 4 (1 inicial + 3 incrementos), valor actual: {qty}"
