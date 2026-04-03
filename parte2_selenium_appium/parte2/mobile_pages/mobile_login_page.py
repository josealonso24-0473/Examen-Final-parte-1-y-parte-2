"""
mobile_login_page.py
Page Object para la pantalla de Login en la aplicación móvil.
Compatible con Android (UIAutomator2) e iOS (XCUITest) mediante accessibility_id.
"""

from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui    import WebDriverWait
from selenium.webdriver.support       import expected_conditions as EC
from selenium.common.exceptions       import TimeoutException


class MobileLoginPage:
    """Page Object de la pantalla de login en la app móvil."""

    # ── Locators (accessibility_id es compatible con Android e iOS) ───────────
    EMAIL_FIELD    = (AppiumBy.ACCESSIBILITY_ID, "login_email_input")
    PASSWORD_FIELD = (AppiumBy.ACCESSIBILITY_ID, "login_password_input")
    LOGIN_BTN      = (AppiumBy.ACCESSIBILITY_ID, "login_submit_button")
    HOME_TITLE     = (AppiumBy.ACCESSIBILITY_ID, "home_screen_title")
    ERROR_TOAST    = (AppiumBy.XPATH, '//*[@content-desc="error_toast"]')

    def __init__(self, driver):
        self.driver = driver
        self.wait   = WebDriverWait(driver, timeout=10)

    def login(self, email: str, password: str):
        """Introduce credenciales y pulsa el botón de ingreso."""
        self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD)).send_keys(email)
        self.driver.find_element(*self.PASSWORD_FIELD).send_keys(password)
        self.driver.find_element(*self.LOGIN_BTN).click()

    def is_home_visible(self) -> bool:
        """Retorna True si la pantalla principal cargó correctamente."""
        try:
            return self.wait.until(
                EC.visibility_of_element_located(self.HOME_TITLE)
            ).is_displayed()
        except TimeoutException:
            return False

    def is_error_toast_visible(self) -> bool:
        """Retorna True si el toast de error es visible."""
        try:
            return self.driver.find_element(*self.ERROR_TOAST).is_displayed()
        except Exception:
            return False
