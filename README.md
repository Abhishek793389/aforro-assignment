# Aforro Backend Assignment

A small Django REST API demonstrating data modeling, REST API design, PostgreSQL, Redis caching, Celery asynchronous processing, query optimization, testing, and Docker.

## Tech Stack

* Python
* Django
* Django REST Framework
* PostgreSQL
* Redis
* Celery
* Docker & Docker Compose

## Project Structure

```text
aforro/
├── aforro/
├── orders/
├── products/
├── search/
├── stores/
├── test/
├── manage.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env
```

## Local Setup

Create and activate a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure PostgreSQL in `.env`.

Run migrations:

```bash
python manage.py migrate
```

Start Django:

```bash
python manage.py runserver
```

## Seed Data

Generate sample data:

```bash
python manage.py seed_data
```

The command creates:

* 10 categories
* 1000 products
* 20 stores
* 300 inventory products for each store

## Docker Setup

Build and start all services:

```bash
docker compose up --build
```

Services:

* Django application
* PostgreSQL
* Redis
* Celery worker

Stop the services:

```bash
docker compose down
```

## API Endpoints

### Create Order

```http
POST /api/orders/
```

Example:

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


### Store Orders

```http
GET /api/stores/<store_id>/orders/
```

Returns orders for a store, newest first.

### Store Inventory

```http
GET /api/stores/<store_id>/inventory/
```

Returns:

* Product title
* Price
* Category
* Quantity

### Product Search

```http
GET /api/search/products/
```

Example:

```text
/api/search/products/?q=laptop
```

Supported filters include:

```text
q
category
min_price
max_price
store_id
in_stock
sort
```

### Product Suggestions

```http
GET /api/search/suggest/?q=lap
```

The suggestion endpoint requires at least 3 characters and returns up to 10 product titles.

### Products

```http
GET /api/products/
POST /api/products/
```

### Categories

```http
GET /api/products/categories/
POST /api/products/categories/
```

### Stores

```http
GET /api/stores/
POST /api/stores/
```

## Redis Caching

Redis is used to cache product search results.

Search responses are cached for 5 minutes.

The cache is cleared when a new product is created so that product search results remain up to date.

## Celery

Celery uses Redis as its message broker.

After a confirmed order is successfully committed to the database, an asynchronous confirmation task is triggered:

```python
send_order_confirmation.delay(order.id)
```

The task is triggered using `transaction.on_commit()` so it only runs after the database transaction succeeds.

Run the Celery worker locally:

```bash
celery -A aforro worker --loglevel=info --pool=solo
```

With Docker, the Celery worker is started automatically by Docker Compose.

## Query Optimization

The project uses Django ORM optimization techniques including:

* `select_related()` for related foreign-key data
* `annotate()` and `Count()` for order item counts
* `bulk_create()` for seed data and order items
* `select_for_update()` when checking inventory during order creation

These reduce unnecessary database queries and help prevent N+1 query problems.

## Tests

Three tests are included:

1. Successful order creation
2. Insufficient stock rejection
3. Store inventory API

Run tests:

```bash
python manage.py test test
```

## Running the Project

For Docker:

```bash
docker compose up --build
```

Then the API is available at:

```text
http://localhost:8000/
```
