# Parte 1 — Pruebas de Integración & Carga con k6

## Descripción

Scripts de pruebas de integración y carga para un sistema de comercio electrónico
(frontend HTML/CSS/JS + backend REST API + base de datos MySQL).

## Estructura del proyecto

```
parte1/
├── tests/
│   └── load-test-ecommerce.js   # Script principal de carga con k6
├── data/
│   └── test-users.json          # Datos de usuarios de prueba
└── README.md
```

## Requisitos previos

- [k6](https://k6.io/docs/get-started/installation/) v0.50+
- Acceso al entorno de pruebas del backend

## Ejecución

```bash
# Prueba básica (verificar que el script funciona)
k6 run tests/load-test-ecommerce.js

# Prueba con variables de entorno personalizadas
BASE_URL=https://api.mitienda.com k6 run tests/load-test-ecommerce.js

# Salida con resumen en JSON
k6 run --out json=results.json tests/load-test-ecommerce.js
```

## Escenarios de prueba documentados

### Escenario 1 — Flujo completo de compra
Verifica la integración completa: autenticación → catálogo → carrito → checkout → confirmación.

### Escenario 2 — Consistencia de inventario bajo concurrencia
20 usuarios compran el último artículo disponible simultáneamente. Solo 1 debe completarse (HTTP 200);
los 19 restantes deben recibir HTTP 409.

### Escenario 3 — Carrito persistente entre sesiones
El estado del carrito debe sobrevivir al cierre y reapertura de sesión, sincronizando
frontend (cookie/localStorage) con el sessionId almacenado en MySQL.

## Thresholds configurados

| Métrica              | Umbral     | Descripción                        |
|----------------------|------------|------------------------------------|
| http_req_duration    | p(95)<2000 | 95% de requests bajo 2 segundos    |
| http_req_failed      | rate<0.01  | Menos del 1% de errores HTTP       |
| error_rate           | rate<0.05  | Menos del 5% de errores de negocio |
| checkout_duration    | p(90)<3000 | Checkout p90 menor a 3 segundos    |

## Perfil de carga

| Etapa     | Duración | Usuarios | Descripción       |
|-----------|----------|----------|-------------------|
| Rampa     | 1 min    | 0 → 50   | Calentamiento     |
| Subida    | 2 min    | 50 → 100 | Pico de carga     |
| Sostenido | 2 min    | 100      | Carga constante   |
| Descenso  | 1 min    | 100 → 0  | Enfriamiento      |
