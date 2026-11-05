# Kiosco El Rápido – Backend (Parte 2)

API hecha con FastAPI + SQLite (SQLAlchemy) + Pydantic.

## Instalación y ejecución

```bash
python -m venv venv
venv\Scripts\activate        # Linux / macOS: source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

- API: http://localhost:8000
- Documentación: http://localhost:8000/docs

Al arrancar por primera vez se crea `kiosco.db` y se cargan los productos iniciales.

## Endpoints

| Método | Ruta                 | Descripción                                   |
|--------|----------------------|-----------------------------------------------|
| GET    | `/api/products`      | Lista los productos. Acepta `?category=`      |
| GET    | `/api/products/{id}` | Detalle de un producto                        |
| POST   | `/api/orders`        | Crea un pedido y descuenta el stock           |
| GET    | `/api/orders`        | Lista los pedidos                             |

Ejemplo de body para `POST /api/orders`:

```json
{
  "items": [
    { "product_id": 1, "quantity": 2 },
    { "product_id": 5, "quantity": 1 }
  ]
}
```
