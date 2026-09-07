from django.core.management.base import BaseCommand
from faker import Faker

from products.models import Category, Product
from stores.models import Store, Inventory


class Command(BaseCommand):
    help = "Generate dummy categories, products, stores and inventory"

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Categories
        categories = [
            "Electronics",
            "Clothing",
            "Shoes",
            "Furniture",
            "Books",
            "Beauty",
            "Sports",
            "Grocery",
            "Toys",
            "Accessories",
        ]

        category_objects = []

        for name in categories:
            category, _ = Category.objects.get_or_create(name=name)
            category_objects.append(category)

        self.stdout.write(
            self.style.SUCCESS("Categories created.")
        )

        # Products
        products = []

        for i in range(1000):
            products.append(
                Product(
                    title=fake.unique.catch_phrase(),
                    description=fake.text(max_nb_chars=200),
                    price=fake.pydecimal(
                        left_digits=5,
                        right_digits=2,
                        positive=True
                    ),
                    category=fake.random_element(category_objects),
                )
            )

        Product.objects.bulk_create(products)

        products = list(Product.objects.all())

        self.stdout.write(
            self.style.SUCCESS("1000 products created.")
        )

        # Stores
        stores = []

        for i in range(20):
            stores.append(
                Store(
                    name=f"Store {i + 1}",
                    location=fake.city(),
                )
            )

        Store.objects.bulk_create(stores)

        stores = list(Store.objects.all())

        self.stdout.write(
            self.style.SUCCESS("20 stores created.")
        )

        # Inventory
        inventory = []

        for store in stores:
            selected_products = products[:300]

            for product in selected_products:
                inventory.append(
                    Inventory(
                        store=store,
                        product=product,
                        quantity=fake.random_int(min=0, max=100),
                    )
                )

        Inventory.objects.bulk_create(
            inventory,
            batch_size=1000
        )

        self.stdout.write(
            self.style.SUCCESS(
                "Inventory created for all stores."
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                "Seed data completed successfully!"
            )
        )