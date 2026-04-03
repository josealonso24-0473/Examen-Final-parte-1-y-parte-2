/**
 * Prueba de Carga - Sistema E-Commerce
 * Herramienta: k6
 * Escenario: 100 usuarios realizando compras simultáneas
 * Autor: QA Engineering
 */

import http from 'k6/http';
import { check, sleep, group } from 'k6';
import { Counter, Rate, Trend } from 'k6/metrics';
import { randomIntBetween } from 'https://jslib.k6.io/k6-utils/1.4.0/index.js';

// ── Métricas personalizadas ──────────────────────────────────────────────────
const errorRate    = new Rate('error_rate');
const checkoutTime = new Trend('checkout_duration');
const orderCount   = new Counter('orders_completed');

// ── Configuración de carga ───────────────────────────────────────────────────
export const options = {
  scenarios: {
    compras_simultaneas: {
      executor:  'ramping-vus',
      startVUs:  0,
      stages: [
        { duration: '1m',  target: 50  },  // Rampa suave: 0 → 50 usuarios
        { duration: '2m',  target: 100 },  // Pico: 100 usuarios simultáneos
        { duration: '2m',  target: 100 },  // Sostenido a 100 usuarios
        { duration: '1m',  target: 0   },  // Descenso gradual
      ],
    },
  },
  thresholds: {
    http_req_duration:     ['p(95)<2000'],  // 95% de requests bajo 2s
    http_req_failed:       ['rate<0.01'],   // Menos del 1% de errores HTTP
    error_rate:            ['rate<0.05'],   // Menos del 5% errores de negocio
    checkout_duration:     ['p(90)<3000'],  // Checkout p90 menor a 3s
  },
};

const BASE_URL  = 'https://api.mitienda.com';
const PRODUCTS  = ['SKU-001', 'SKU-002', 'SKU-003', 'SKU-004'];

// ── Datos de prueba (usuarios simulados) ────────────────────────────────────
const USERS = [
  { email: 'usuario1@qa.com', password: 'Pass@1234', address: 'Calle 1' },
  { email: 'usuario2@qa.com', password: 'Pass@1234', address: 'Calle 2' },
  { email: 'usuario3@qa.com', password: 'Pass@1234', address: 'Calle 3' },
  { email: 'usuario4@qa.com', password: 'Pass@1234', address: 'Calle 4' },
  { email: 'usuario5@qa.com', password: 'Pass@1234', address: 'Calle 5' },
];

// ── Función principal ejecutada por cada VU ──────────────────────────────────
export default function purchaseFlow() {
  const user    = USERS[__VU % USERS.length];
  const product = PRODUCTS[randomIntBetween(0, 3)];
  const headers = { 'Content-Type': 'application/json' };
  let authToken;

  // ── GRUPO 1: Autenticación ─────────────────────────────────────────────────
  group('1. Autenticación', () => {
    const res = http.post(
      `${BASE_URL}/api/auth/login`,
      JSON.stringify({ email: user.email, password: user.password }),
      { headers }
    );
    const ok = check(res, {
      'login exitoso (200)': (r) => r.status === 200,
      'token JWT presente':  (r) => r.json('token') !== undefined,
    });
    errorRate.add(!ok);
    if (ok) authToken = res.json('token');
    sleep(1);
  });

  if (!authToken) return; // Abortar si no hay sesión
  const authHeaders = { ...headers, Authorization: `Bearer ${authToken}` };

  // ── GRUPO 2: Consulta de producto ─────────────────────────────────────────
  group('2. Buscar producto', () => {
    const res = http.get(`${BASE_URL}/api/products/${product}`, { headers: authHeaders });
    check(res, {
      'producto encontrado (200)': (r) => r.status === 200,
      'stock mayor a cero':        (r) => r.json('stock') > 0,
    });
    sleep(2);
  });

  // ── GRUPO 3: Agregar al carrito ───────────────────────────────────────────
  group('3. Agregar al carrito', () => {
    const res = http.post(
      `${BASE_URL}/api/cart/add`,
      JSON.stringify({ sku: product, qty: 1 }),
      { headers: authHeaders }
    );
    check(res, {
      'carrito actualizado (200)': (r) => r.status === 200,
      'itemCount > 0':             (r) => r.json('itemCount') > 0,
    });
    sleep(1.5);
  });

  // ── GRUPO 4: Checkout ─────────────────────────────────────────────────────
  group('4. Proceso de checkout', () => {
    const start = Date.now();
    const res = http.post(
      `${BASE_URL}/api/checkout`,
      JSON.stringify({
        paymentMethod: 'card',
        cardToken:     'tok_test_visa',
        address:       user.address,
      }),
      { headers: authHeaders, timeout: '10s' }
    );
    checkoutTime.add(Date.now() - start);

    const success = check(res, {
      'checkout exitoso (200)': (r) => r.status === 200,
      'orderId generado':       (r) => r.json('orderId') !== null,
    });
    if (success) orderCount.add(1);
    errorRate.add(!success);
    sleep(2);
  });

  // ── GRUPO 5: Confirmación ─────────────────────────────────────────────────
  group('5. Confirmación del pedido', () => {
    const res = http.get(`${BASE_URL}/api/orders/latest`, { headers: authHeaders });
    check(res, {
      'orden recuperada (200)':  (r) => r.status === 200,
      'estado = confirmed':      (r) => r.json('status') === 'confirmed',
    });
  });

  sleep(randomIntBetween(1, 3));
}
