# Aforro Backend Assignment

## 1. Project Setup and Run Instructions

```bash
git clone https://github.com/Abhishek793389/aforro-assignment.git
cd aforro-assignment
cd aforro

But before run docker build create a .env file inside the root folder where file like readme.md, docker are there.
And paste this there. Enter you password in the POSTGRES_PASSWORD section.
    POSTGRES_DB=aforro
    POSTGRES_USER="postgres"
    POSTGRES_PASSWORD="password"
    POSTGRES_HOST=localhost
    POSTGRES_PORT=5432

 Then run this command "docker compose up --build"
```

Run seed data:

```bash
docker compose exec web python manage.py seed_data
```

Swagger UI:

```text
http://localhost:8000/api/docs/
```
Postman collection

```text
Open Postman/file/import/select-Aforro-API.postman_collection.json 

It will import all api and you can test.
```

## 2. API Endpoint Details

| Method | Endpoint                            | Description                |
| ------ | ----------------------------------- | -------------------------- |
| POST   | `/api/orders/`                      | Create an order            |
| GET    | `/api/stores/{store_id}/orders/`    | List store orders          |
| GET    | `/api/stores/{store_id}/inventory/` | Get store inventory        |
| GET    | `/api/search/products/`             | Search and filter products |
| GET    | `/api/search/suggest/?q=xxx`        | Product autocomplete       |
| GET    | `/api/products/`                    | List products              |
| POST   | `/api/products/`                    | Create product             |
| GET    | `/api/products/categories/`         | List categories            |
| POST   | `/api/products/categories/`         | Create category            |
| GET    | `/api/stores/`                      | List stores                |
| POST   | `/api/stores/`                      | Create store               |

## 3. Request and Response Formats

### Create Order

**Request:**

```json
{
    "store_id": 1,
    "items": [
        {
            "product_id": 1,
            "quantity_requested": 2
        }
    ]
}
```

**Response:**

```json
{
    "id": 1,
    "store": 1,
    "status": "CONFIRMED",
    "created_at": "2026-09-07T10:00:00Z",
    "items": [
        {
            "product_id": 1,
            "quantity_requested": 2
        }
    ]
}
```

### Create Product

**Request:**

```json
{
    "title": "Laptop",
    "description": "Business laptop",
    "price": "50000.00",
    "category": 1
}
```

### Create Category

**Request:**

```json
{
    "name": "Electronics"
}
```

### Create Store

**Request:**

```json
{
    "name": "Store 1",
    "location": "Delhi"
}
```

## 4. Database / Setup Requirements

* PostgreSQL is used as the database.
* Redis is used for caching and Celery.
* Celery uses Redis as the broker.
* Docker Compose runs Django, PostgreSQL, Redis, and Celery.
* Database configuration is provided through environment variables. so create a .env file and metion these
    POSTGRES_DB=aforro
    POSTGRES_USER="postgres"
    POSTGRES_PASSWORD="password"
    POSTGRES_HOST=localhost
    POSTGRES_PORT=5432
