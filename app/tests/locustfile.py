import random

from faker import Faker
from locust import FastHttpUser, task

fake = Faker()


class ProductApiUser(FastHttpUser):
    """
    User class that simulates a user interacting with the Product API.
    """

    host = "https://sqlite-cloudrun-555528739632.us-central1.run.app"
    created_product_ids = []

    @task(5)
    def list_products(self):
        """
        Task to simulate a user listing products with random pagination.
        """
        skip = random.randint(0, 20)
        limit = random.randint(10, 100)
        self.client.get(f"/products/?skip={skip}&limit={limit}", name="/products/?skip=[skip]&limit=[limit]")

    @task(3)
    def create_and_manage_product(self):
        """
        Task to simulate a full product lifecycle: create, get, update, and delete.
        """
        # Create a new product
        product_data = {
            "name": fake.text(max_nb_chars=100),
            "price": round(random.uniform(5.0, 500.0), 2),
            "description": fake.text(max_nb_chars=100),
        }
        with self.client.post("/products/", json=product_data, name="/products/", catch_response=True) as response:
            if response.status_code == 200:
                product_id = response.json().get("id")
                if product_id:
                    self.created_product_ids.append(product_id)
                    response.success()
                else:
                    response.failure("Failed to extract product_id from response")
                    return
            else:
                response.failure(f"Failed to create product, status: {response.status_code}")
                return

        # Get, Update, and Delete the created product
        if not self.created_product_ids:
            return

        product_id_to_manage = self.created_product_ids.pop()

        # Get the specific product
        self.client.get(f"/products/{product_id_to_manage}", name="/products/{product_id}")

        # Update the product
        update_data = {"price": round(random.uniform(5.0, 500.0), 2)}
        self.client.patch(f"/products/{product_id_to_manage}", json=update_data, name="/products/{product_id}")

        # Delete the product
        self.client.delete(f"/products/{product_id_to_manage}", name="/products/{product_id}")

    @task(1)
    def get_random_product(self):
        """
        Task to get a random product from the list of created products.
        This task will only run if there are products created by the user session.
        """
        if self.created_product_ids:
            product_id = random.choice(self.created_product_ids)
            self.client.get(f"/products/{product_id}", name="/products/{product_id}")
