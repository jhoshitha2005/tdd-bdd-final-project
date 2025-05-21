from service.models import Product
from service.common import status
from tests.factories import ProductFactory

BASE_URL = "/products"

class TestProductRoutes:
    """Test cases for Product Service Routes"""

    def _create_products(self, count):
        """Factory method to create test products"""
        products = []
        for _ in range(count):
            test_product = ProductFactory()
            response = self.client.post(BASE_URL, json=test_product.serialize())
            assert response.status_code == status.HTTP_201_CREATED
            new_product = response.get_json()
            test_product.id = new_product["id"]
            products.append(test_product)
        return products

    def test_get_product(self):
        """It should Get a single Product"""
        test_product = self._create_products(1)[0]
        response = self.client.get(f"{BASE_URL}/{test_product.id}")
        assert response.status_code == status.HTTP_200_OK
        data = response.get_json()
        assert data["name"] == test_product.name
        assert data["description"] == test_product.description
        assert data["price"] == test_product.price
        assert data["available"] == test_product.available
        assert data["category"] == test_product.category

    def test_get_product_not_found(self):
        """It should not Get a Product that's not found"""
        response = self.client.get(f"{BASE_URL}/0")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        data = response.get_json()
        assert "was not found" in data["message"]

    def test_update_product(self):
        """It should Update an existing Product"""
        test_product = self._create_products(1)[0]
        new_data = test_product.serialize()
        new_data["name"] = "Updated Product Name"
        response = self.client.put(f"{BASE_URL}/{test_product.id}", json=new_data)
        assert response.status_code == status.HTTP_200_OK
        updated = response.get_json()
        assert updated["name"] == "Updated Product Name"

    def test_delete_product(self):
        """It should Delete a Product"""
        test_product = self._create_products(1)[0]
        response = self.client.delete(f"{BASE_URL}/{test_product.id}")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        # Check if it is deleted
        get_response = self.client.get(f"{BASE_URL}/{test_product.id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    def test_list_all_products(self):
        """It should List all Products"""
        self._create_products(3)
        response = self.client.get(BASE_URL)
        assert response.status_code == status.HTTP_200_OK
        data = response.get_json()
        assert len(data) >= 3

    def test_list_products_by_name(self):
        """It should List Products by Name"""
        test_product = self._create_products(1)[0]
        response = self.client.get(f"{BASE_URL}?name={test_product.name}")
        assert response.status_code == status.HTTP_200_OK
        data = response.get_json()
        assert any(product["name"] == test_product.name for product in data)

    def test_list_products_by_category(self):
        """It should List Products by Category"""
        test_product = self._create_products(1)[0]
        response = self.client.get(f"{BASE_URL}?category={test_product.category}")
        assert response.status_code == status.HTTP_200_OK
        data = response.get_json()
        assert all(product["category"] == test_product.category for product in data)

    def test_list_products_by_availability(self):
        """It should List Products by Availability"""
        available_product = self._create_products(1)[0]
        response = self.client.get(f"{BASE_URL}?available={available_product.available}")
        assert response.status_code == status.HTTP_200_OK
        data = response.get_json()
        assert all(product["available"] == available_product.available for product in data)
