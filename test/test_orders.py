from django.test import TestCase
from rest_framework.test import APIClient

from products.models import Category, Product
from stores.models import Store, Inventory


class OrderTest(TestCase):

    def test_create_order(self):
        client = APIClient()

        category = Category.objects.create(name="Test Category")
        product = Product.objects.create(title="Test Product",price=100,category=category)
        store = Store.objects.create(name="Test Store",location="Delhi")
        Inventory.objects.create(store=store,product=product,quantity=10)

        response = client.post(
            "/api/orders/",
            {
                "store_id": store.id,
                "items": [
                    {
                        "product_id": product.id,
                        "quantity_requested": 2
                    }
                ]
            },
            format="json"
        )

        self.assertEqual(response.status_code, 201)