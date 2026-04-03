"""
mobile_product_page.py
Page Object para la pantalla de Producto y Checkout en la app móvil.
Incluye implementación de gestos táctiles (swipe) con la API de Appium 2.
"""

from appium.webdriver.common.appiumby    import AppiumBy
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.support.ui       import WebDriverWait
from selenium.webdriver.support          import expected_conditions as EC
from selenium.common.exceptions          import TimeoutException


class MobileProductPage:
    """Page Object que cubre el flujo de producto y checkout en la app móvil."""

    # ── Locators ──────────────────────────────────────────────────────────────
    PRODUCT_IMAGE   = (AppiumBy.ACCESSIBILITY_ID, "product_gallery_image")
    ADD_TO_CART_BTN = (AppiumBy.ACCESSIBILITY_ID, "add_to_cart_fab")
    CART_BADGE      = (AppiumBy.ACCESSIBILITY_ID, "cart_item_count")
    CHECKOUT_BTN    = (AppiumBy.ACCESSIBILITY_ID, "proceed_checkout_button")
    SUCCESS_SCREEN  = (AppiumBy.ACCESSIBILITY_ID, "order_success_screen")
    OFFLINE_BANNER  = (AppiumBy.ACCESSIBILITY_ID, "offline_banner")
    QUANTITY_PLUS   = (AppiumBy.ACCESSIBILITY_ID, "quantity_increase_button")
    QUANTITY_VALUE  = (AppiumBy.ACCESSIBILITY_ID, "quantity_display")

    def __init__(self, driver):
        self.driver = driver
        self.wait   = WebDriverWait(driver, timeout=12)

    def swipe_product_gallery(self):
        """
        Desliza la galería de imágenes del producto hacia la izquierda
        para mostrar la siguiente imagen.
        Implementado con TouchAction (compatible con Android e iOS).
        """
        size    = self.driver.get_window_size()
        width   = size['width']
        height  = size['height']
        start_x = int(width  * 0.80)
        end_x   = int(width  * 0.20)
        mid_y   = int(height * 0.35)

        TouchAction(self.driver) \
            .press(x=start_x, y=mid_y) \
            .wait(500) \
            .move_to(x=end_x, y=mid_y) \
            .release() \
            .perform()

    def get_current_gallery_image_desc(self) -> str:
        """Retorna el content-desc de la imagen actual de la galería."""
        return self.driver \
            .find_element(*self.PRODUCT_IMAGE) \
            .get_attribute("content-desc")

    def add_to_cart(self) -> str:
        """
        Pulsa el botón FAB de 'Agregar al carrito'.
        Retorna el texto del badge (número de ítems en carrito).
        """
        self.wait.until(EC.element_to_be_clickable(self.ADD_TO_CART_BTN)).click()
        return self.driver.find_element(*self.CART_BADGE).text

    def increase_quantity(self, times: int = 1):
        """Incrementa la cantidad del producto el número de veces indicado."""
        for _ in range(times):
            self.driver.find_element(*self.QUANTITY_PLUS).click()

    def get_quantity(self) -> int:
        """Retorna la cantidad actual seleccionada."""
        return int(self.driver.find_element(*self.QUANTITY_VALUE).text)

    def go_to_checkout(self):
        """Navega a la pantalla de pago."""
        self.wait.until(EC.element_to_be_clickable(self.CHECKOUT_BTN)).click()

    def is_order_success_visible(self) -> bool:
        """Retorna True si la pantalla de orden exitosa es visible."""
        try:
            return self.wait.until(
                EC.visibility_of_element_located(self.SUCCESS_SCREEN)
            ).is_displayed()
        except TimeoutException:
            return False

    def is_offline_banner_visible(self) -> bool:
        """Retorna True si el banner de modo offline está visible."""
        try:
            return self.driver.find_element(*self.OFFLINE_BANNER).is_displayed()
        except Exception:
            return False
