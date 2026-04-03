# Parte 2 — Automatización Web (Selenium) y Móvil (Appium)

## Descripción

Suite completa de pruebas automatizadas para la aplicación web y su versión
móvil, ambas con la misma funcionalidad de e-commerce.

## Estructura del proyecto

```
parte2/
├── pages/                         # Page Objects — aplicación web
│   ├── base_page.py               # Clase base con métodos comunes
│   ├── login_page.py              # Pantalla de login (web)
│   └── checkout_page.py           # Flujo de compra (web)
├── mobile_pages/                  # Page Objects — aplicación móvil
│   ├── mobile_login_page.py       # Pantalla de login (móvil)
│   └── mobile_product_page.py     # Producto + checkout + gestos (móvil)
├── tests/
│   ├── conftest.py                # Fixture de WebDriver (Chrome/Firefox/Edge)
│   ├── conftest_mobile.py         # Fixture de Appium (Android/iOS)
│   ├── test_ecommerce_web.py      # 7 casos de prueba web
│   └── test_ecommerce_mobile.py   # 7 casos de prueba móvil
├── requirements.txt
└── README.md
```

## Requisitos previos

### Para Selenium
- Python 3.10+
- Google Chrome 120+ / Firefox 121+ / Microsoft Edge 120+
- `pip install -r requirements.txt`

### Para Appium
- Python 3.10+
- Node.js 18+
- Appium 2.x: `npm install -g appium`
- Driver Android: `appium driver install uiautomator2`
- Driver iOS: `appium driver install xcuitest` (requiere macOS + Xcode)
- Android SDK (para emulador) o dispositivo físico
- `pip install -r requirements.txt`

## Ejecución

### Selenium — pruebas web (los 3 navegadores)
```bash
cd parte2
pytest tests/test_ecommerce_web.py -v
```

### Selenium — solo Chrome
```bash
pytest tests/test_ecommerce_web.py -v -k "chrome"
```

### Appium — pruebas móviles (iniciar servidor primero)
```bash
# Terminal 1: arrancar Appium Server
appium --port 4723

# Terminal 2: ejecutar tests
pytest tests/test_ecommerce_mobile.py -v --co conftest_mobile.py
```

### Reporte HTML
```bash
pytest tests/ --html=report.html --self-contained-html
```

## Casos de prueba

### Selenium Web
| ID         | Descripción                                  | Navegadores       |
|------------|----------------------------------------------|-------------------|
| TC-WEB-01  | Login exitoso con usuario válido             | Chrome/Firefox/Edge |
| TC-WEB-02  | Login con usuario inexistente                | Chrome/Firefox/Edge |
| TC-WEB-03  | Login con contraseña incorrecta              | Chrome/Firefox/Edge |
| TC-WEB-04  | Login con campos vacíos                      | Chrome/Firefox/Edge |
| TC-WEB-05  | Agregar producto al carrito                  | Chrome/Firefox/Edge |
| TC-WEB-06  | Compra completa end-to-end                   | Chrome/Firefox/Edge |
| TC-WEB-07  | Producto sin stock (botón deshabilitado)     | Chrome/Firefox/Edge |

### Appium Móvil
| ID         | Descripción                                  | Plataformas       |
|------------|----------------------------------------------|-------------------|
| TC-MOB-01  | Login exitoso en app nativa                  | Android 13 / iOS 17 |
| TC-MOB-02  | Login inválido muestra toast de error        | Android 13 / iOS 17 |
| TC-MOB-03  | Gesto swipe cambia imagen de galería         | Android 13 / iOS 17 |
| TC-MOB-04  | FAB agrega al carrito y actualiza badge      | Android 13 / iOS 17 |
| TC-MOB-05  | Compra completa end-to-end en dispositivo    | Android 13 / iOS 17 |
| TC-MOB-06  | Modo offline muestra banner informativo      | Android 13 / iOS 17 |
| TC-MOB-07  | Botón '+' incrementa cantidad correctamente  | Android 13 / iOS 17 |

## Patrones de diseño aplicados

- **Page Object Model (POM)**: Cada pantalla tiene su propia clase con locators
  y métodos de acción encapsulados. Los tests no contienen selectores directos.
- **Fixture parametrizado**: Un solo test se ejecuta automáticamente en múltiples
  navegadores (Selenium) o plataformas (Appium) sin duplicar código.
- **Precondiciones con autouse**: El fixture `login_before_each` autentica al
  usuario antes de cada test del módulo de checkout, sin repetir el código de login.
