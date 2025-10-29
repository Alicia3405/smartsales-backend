# API Testing Plan for backend_salessmart

## Priority 1: Seguridad y Autenticación (CU6, CU4)
- [ ] Test user registration: POST /api/v1/registro/
- [ ] Test login and JWT generation: POST /api/v1/token/
- [ ] Test admin endpoint rejection for non-admin: POST /api/v1/productos/ (expect 403 or 401)

## Priority 2: Flujo Crítico de Inventario (CU3, CU1, CU10)
- [ ] Test product creation: POST /api/v1/productos/
- [ ] Test stock entry (IN movement): POST /api/v1/movimientos-inventario/
- [ ] Test stock decrease (OUT movement): POST /api/v1/movimientos-inventario/

## Priority 3: Flujo de Compra (CU7, CU8, CU9)
- [ ] Test add to cart: POST /api/v1/carrito/add_item/
- [ ] Test checkout: POST /api/v1/checkout/
- [ ] Test payment processing: POST /api/v1/pago/

## Documentation
- [ ] Compile results with curl commands, expected JSON, actual responses
