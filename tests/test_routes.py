"""
TestProduct API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
import os
import logging
from unittest import TestCase
from datetime import date
# from unittest.mock import MagicMock, patch
from service import app
from service.models import db, init_db, Product
from service.common import status  # HTTP Status Codes

from tests.factories import ProductFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/testdb"
)
BASE_URL = "/api/products"
CONTENT_TYPE_JSON = "application/json"

######################################################################
#  T E S T   C A S E S
######################################################################


# pylint: disable=too-many-public-methods
class TestProductService(TestCase):
    """Product Server Tests"""

    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        # Set up the test database
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        init_db(app)

    @classmethod
    def tearDownClass(cls):
        """Run once after all tests"""
        db.session.close()

    def setUp(self):
        """Runs before each test"""
        self.client = app.test_client()
        db.session.query(Product).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        db.session.remove()

    def _create_products(self, count):
        """Factory method to create products in bulk"""
        products = []
        for _ in range(count):
            test_product = ProductFactory()
            response = self.client.post(BASE_URL, json=test_product.serialize())
            self.assertEqual(
                response.status_code,
                status.HTTP_201_CREATED,
                "Could not create test product",
            )
            new_product = response.get_json()
            test_product.id = new_product["id"]
            products.append(test_product)
        return products

    ######################################################################
    #  P L A C E   T E S T   C A S E S   H E R E
    ######################################################################

    def test_index(self):
        """ It should call the home page """
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_health(self):
        """It should be healthy"""
        response = self.client.get("/health")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["status"], "OK")

    def test_get_product(self):
        """It should Get a single Product"""
        # get the id of a product
        test_product = self._create_products(1)[0]
        response = self.client.get(f"{BASE_URL}/{test_product.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["name"], test_product.name)

    def test_get_product_not_found(self):
        """It should not Get a Product thats not found"""
        response = self.client.get(f"{BASE_URL}/0")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        data = response.get_json()
        logging.debug("Response data = %s", data)
        self.assertIn("was not found", data["message"])

    def test_update_product(self):
        """It should Update an existing Product"""
        # create a product to update
        test_product = ProductFactory()
        response = self.client.post(BASE_URL, json=test_product.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # update the product
        new_product = response.get_json()
        logging.debug(new_product)
        new_product["category"] = "category10"
        response = self.client.put(f"{BASE_URL}/{new_product['id']}", json=new_product)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_product = response.get_json()
        self.assertEqual(updated_product["category"], "category10")

    def test_list_products(self):
        """Test listing products without filters"""
        # Create test products
        product1 = ProductFactory(name="Product 1", category="Category A", price=10.0)
        response = self.client.post(BASE_URL, json=product1.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        product2 = ProductFactory(name="Product 2", category="Category B", price=15.0)
        response = self.client.post(BASE_URL, json=product2.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        product3 = ProductFactory(name="Product 3", category="Category A", price=20.0)
        response = self.client.post(BASE_URL, json=product3.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Send GET request without filters
        response = self.client.get(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        products = response.get_json()
        self.assertEqual(len(products), 3)  # Should return all products

    def test_list_products_with_category(self):
        """Test listing products with category filter"""
        # Create test products
        product1 = ProductFactory(name="Product 1", category="Category A", price=10.0)
        response = self.client.post(BASE_URL, json=product1.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        product2 = ProductFactory(name="Product 2", category="Category B", price=15.0)
        response = self.client.post(BASE_URL, json=product2.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        product3 = ProductFactory(name="Product 3", category="Category A", price=20.0)
        response = self.client.post(BASE_URL, json=product3.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Send GET request with category filter
        response = self.client.get(BASE_URL + "?category=Category%20A")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        filtered_products = response.get_json()
        self.assertEqual(len(filtered_products), 2)  # Should return products with Category A

    def test_list_products_with_price(self):
        """Test listing products with price filter"""
        # Create test products
        product1 = ProductFactory(name="Product 1", category="Category A", price=10.0)
        response = self.client.post(BASE_URL, json=product1.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        product2 = ProductFactory(name="Product 2", category="Category B", price=15.0)
        response = self.client.post(BASE_URL, json=product2.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        product3 = ProductFactory(name="Product 3", category="Category A", price=20.0)
        response = self.client.post(BASE_URL, json=product3.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Send GET request with price filter
        response = self.client.get(BASE_URL + "?price=15.0")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        filtered_products = response.get_json()
        self.assertEqual(len(filtered_products), 1)  # Should return Product 2

    def test_list_products_with_stock(self):
        """Test listing products with stock filter"""
        # Create test products
        product1 = ProductFactory(name="Product 1", category="Category A", price=10.0)
        response = self.client.post(BASE_URL, json=product1.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        product2 = ProductFactory(name="Product 2", category="Category B", price=15.0)
        response = self.client.post(BASE_URL, json=product2.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        product3 = ProductFactory(name="Product 3", category="Category A", price=20.0)
        response = self.client.post(BASE_URL, json=product3.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Send GET request with both category and price filter
        response = self.client.get(BASE_URL + "?category=Category%20A&price=20.0")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        filtered_products = response.get_json()
        self.assertEqual(len(filtered_products), 1)  # Should return Product 3
        self.assertEqual(filtered_products[0]["name"], "Product 3")
        self.assertEqual(filtered_products[0]["category"], "Category A")
        self.assertEqual(filtered_products[0]["price"], 20.0)

    def test_list_products_with_category_and_stock(self):
        """Test listing products with category and stock filter"""
        # Create test products
        product1 = ProductFactory(name="Product 1", category="Category A", stock=5)
        response = self.client.post(BASE_URL, json=product1.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        product2 = ProductFactory(name="Product 2", category="Category B", stock=10)
        response = self.client.post(BASE_URL, json=product2.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        product3 = ProductFactory(name="Product 3", category="Category A", stock=20)
        response = self.client.post(BASE_URL, json=product3.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # # Send GET request with both category and price filter
        response = self.client.get(BASE_URL + "?stock=10")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        filtered_products = response.get_json()
        self.assertEqual(len(filtered_products), 1)  # Should return Product 2

    def test_list_products_with_non_matching_filter(self):
        """Test listing products with non-matching filter"""
        # Create test products
        product1 = ProductFactory(name="Product 1", category="Category A", price=0)
        response = self.client.post(BASE_URL, json=product1.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        product2 = ProductFactory(name="Product 2", category="Category B", price=15.0)
        response = self.client.post(BASE_URL, json=product2.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        product3 = ProductFactory(name="Product 3", category="Category A", price=20.0)
        response = self.client.post(BASE_URL, json=product3.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Send GET request with non-matching filter
        response = self.client.get(BASE_URL + "?category=Category%20C")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        filtered_products = response.get_json()
        self.assertEqual(len(filtered_products), 0)  # Should return an empty list

    def test_create_product(self):
        """It should Create a new Product"""
        test_product = ProductFactory()
        logging.debug("Test Product: %s", test_product.serialize())
        response = self.client.post(BASE_URL, json=test_product.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Make sure location header is set
        location = response.headers.get("Location", None)
        self.assertIsNotNone(location)

        # Check the data is correct
        new_product = response.get_json()
        self.assertEqual(new_product["name"], test_product.name)
        self.assertEqual(new_product["price"], test_product.price)
        self.assertEqual(new_product["desc"], test_product.desc)
        self.assertEqual(new_product["category"], test_product.category)
        self.assertEqual(new_product["stock"], test_product.stock)
        self.assertEqual(date.fromisoformat(new_product["create_date"]), test_product.create_date)
        self.assertEqual(new_product["available"], test_product.available)
        self.assertEqual(new_product["likes"], test_product.likes)

        # TO-DO: When get_product is implemented, uncommented below
        # Check that the location header was correct

        # response = self.client.get(location)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # new_product = response.get_json()
        # self.assertEqual(new_product["name"], test_product.name)
        # self.assertEqual(new_product["price"], test_product.price)
        # self.assertEqual(new_product["desc"], test_product.desc)
        # self.assertEqual(new_product["category"], test_product.category)
        # self.assertEqual(new_product["stock"], test_product.stock)
        # self.assertEqual(new_product["create_date"], test_product.create_date)

    def test_delete_product(self):
        """It should Delete a Product"""
        test_product = self._create_products(1)[0]
        response = self.client.delete(f"{BASE_URL}/{test_product.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(response.data), 0)

        # TO-DO: make sure they are deleted
        # After get_product is completed, uncomment the following codes

        # response = self.client.get(f"{BASE_URL}/{test_product.id}")
        # self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_like_product(self):
        """It should Like an existing Product"""
        test_product = ProductFactory()
        response = self.client.post(BASE_URL, json=test_product.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        new_product = response.get_json()
        logging.debug(new_product)
        old_like = new_product["likes"]
        response = self.client.put(f"{BASE_URL}/{new_product['id']}/like", json=new_product)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_product = response.get_json()
        self.assertEqual(updated_product["likes"], old_like + 1)

    def test_purchase_product(self):
        """It should Purchase a Product"""
        test_product = ProductFactory()
        test_product.available = True
        test_product.stock = 5
        response = self.client.post(BASE_URL, json=test_product.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        new_product = response.get_json()
        logging.debug(new_product)
        old_stock = new_product["stock"]
        response = self.client.post(f"{BASE_URL}/{new_product['id']}/purchase", json=new_product)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_product = response.get_json()
        self.assertEqual(updated_product["stock"], old_stock - 1)

    def test_purchase_product_out_of_stock(self):
        """It should not Purchase a Product that is out of stock"""
        test_product = ProductFactory()
        test_product.available = False
        test_product.stock = 0
        response = self.client.post(BASE_URL, json=test_product.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        new_product = response.get_json()
        logging.debug(new_product)
        response = self.client.post(f"{BASE_URL}/{new_product['id']}/purchase")
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        data = response.get_json()
        self.assertEqual(data["error"], "Product out of stock")

    def test_purchase_product_not_found(self):
        """It should not Purchase a Product that is not found"""
        response = self.client.post(f"{BASE_URL}/0/purchase")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        data = response.get_json()
        self.assertIn("was not found", data["message"])

    def test_purchase_product_update_status(self):
        """It should Purchase a Product and update stock and availability"""
        test_product = ProductFactory()
        test_product.available = True
        test_product.stock = 1  # Set stock to 1 for this test case
        response = self.client.post(BASE_URL, json=test_product.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        new_product = response.get_json()
        logging.debug(new_product)
        response = self.client.post(f"{BASE_URL}/{new_product['id']}/purchase")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the stock is updated to 0 and availability is set to False
        response = self.client.get(f"{BASE_URL}/{new_product['id']}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_product = response.get_json()
        self.assertEqual(updated_product["stock"], 0)
        self.assertEqual(updated_product["available"], False)

    ######################################################################
    #  T E S T   S A D   P A T H S
    ######################################################################

    def test_create_product_no_data(self):
        """It should not Create a Product with missing data"""
        response = self.client.post(BASE_URL, json={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_product_no_content_type(self):
        """It should not Create a Product with no content type"""
        response = self.client.post(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_create_product_wrong_content_type(self):
        """It should not Create a Product with the wrong content type"""
        response = self.client.post(BASE_URL, data="hello", content_type="text/html")
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_method_not_supported(self):
        """It should respond with a method not allowed"""
        response = self.client.put(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_product_not_found(self):
        """It should not Update a product that is not found"""
        test_product = ProductFactory()
        response = self.client.put(
            f"{BASE_URL}/{test_product.id}", json=test_product.serialize()
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_like_product_not_found(self):
        """It should not Like a product that is not found"""
        test_product = ProductFactory()
        response = self.client.put(
            f"{BASE_URL}/{test_product.id}/like", json=test_product.serialize()
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
