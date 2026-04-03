"""
conftest.py
Fixtures de pytest para inicializar y cerrar WebDriver en Chrome, Firefox y Edge.
El parámetro `driver` ejecuta cada test en los tres navegadores automáticamente.
"""

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options   import Options as ChromeOptions
from selenium.webdriver.firefox.options  import Options as FirefoxOptions
from selenium.webdriver.edge.options     import Options as EdgeOptions


@pytest.fixture(scope="function", params=["chrome", "firefox", "edge"])
def driver(request):
    """
    Fixture parametrizado: lanza Chrome, Firefox y Edge en modo headless.
    Se destruye al finalizar cada test (scope='function').
    """
    browser = request.param

    if browser == "chrome":
        opts = ChromeOptions()
        opts.add_argument("--headless=new")
        opts.add_argument("--window-size=1920,1080")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        d = webdriver.Chrome(options=opts)

    elif browser == "firefox":
        opts = FirefoxOptions()
        opts.add_argument("-headless")
        d = webdriver.Firefox(options=opts)

    else:  # edge
        opts = EdgeOptions()
        opts.add_argument("--headless=new")
        opts.add_argument("--window-size=1920,1080")
        d = webdriver.Edge(options=opts)

    d.implicitly_wait(5)
    yield d
    d.quit()
