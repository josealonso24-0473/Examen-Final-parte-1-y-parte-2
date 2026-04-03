"""
base_page.py
Clase base para todos los Page Objects de Selenium.
Encapsula WebDriverWait y métodos comunes de interacción con el DOM.
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class BasePage:
    """
    Clase base con métodos reutilizables de espera y localización.
    Todos los Page Objects deben heredar de esta clase.
    """

    DEFAULT_TIMEOUT = 10  # segundos

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout=self.DEFAULT_TIMEOUT)

    def find(self, locator):
        """Espera hasta que el elemento sea visible y lo retorna."""
        return self.wait.until(EC.visibility_of_element_located(locator))

    def click(self, locator):
        """Espera hasta que el elemento sea clickeable y hace clic."""
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def type_text(self, locator, text: str):
        """Limpia el campo y escribe el texto dado."""
        el = self.find(locator)
        el.clear()
        el.send_keys(text)

    def get_text(self, locator) -> str:
        """Retorna el texto visible del elemento."""
        return self.find(locator).text

    def is_visible(self, locator) -> bool:
        """Retorna True si el elemento es visible, False en caso contrario."""
        try:
            return self.find(locator).is_displayed()
        except (TimeoutException, NoSuchElementException):
            return False

    def wait_for_url_contains(self, fragment: str):
        """Espera hasta que la URL actual contenga el fragmento dado."""
        self.wait.until(EC.url_contains(fragment))

    def scroll_to_element(self, locator):
        """Desplaza la vista hasta el elemento."""
        el = self.find(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", el)
        return el
