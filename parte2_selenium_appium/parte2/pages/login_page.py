"""
login_page.py
Page Object para la pantalla de Login (web).
Hereda de BasePage y encapsula todos los locators y acciones de autenticación.
"""

from selenium.webdriver.common.by import By
from .base_page import BasePage


class LoginPage(BasePage):
    """Page Object de la página de inicio de sesión."""

    # ── Locators ──────────────────────────────────────────────────────────────
    EMAIL_INPUT    = (By.ID,           "email")
    PASSWORD_INPUT = (By.ID,           "password")
    LOGIN_BUTTON   = (By.CSS_SELECTOR, "button[type='submit']")
    ERROR_MSG      = (By.CSS_SELECTOR, ".alert-error")
    WELCOME_BANNER = (By.CSS_SELECTOR, ".user-greeting")
    FORGOT_LINK    = (By.LINK_TEXT,    "¿Olvidaste tu contraseña?")

    # ── Acciones ──────────────────────────────────────────────────────────────

    def login(self, email: str, password: str):
        """Rellena el formulario y envía las credenciales."""
        self.type_text(self.EMAIL_INPUT,    email)
        self.type_text(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

    def is_logged_in(self) -> bool:
        """Retorna True si el banner de bienvenida es visible."""
        return self.is_visible(self.WELCOME_BANNER)

    def get_error_message(self) -> str:
        """Retorna el texto del mensaje de error mostrado."""
        return self.get_text(self.ERROR_MSG)

    def click_forgot_password(self):
        """Navega al flujo de recuperación de contraseña."""
        self.click(self.FORGOT_LINK)
