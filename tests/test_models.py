"""
Test cases for Product Model

"""
import os
import logging
import unittest
from datetime import date
from werkzeug.exceptions import NotFound
from service.models import Product, DataValidationError, db
from service import app
from tests.factories import ProductFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/testdb"
)

######################################################################
#  Product   M O D E L   T E S T   C A S E S
######################################################################
class TestProduct(unittest.TestCase):
    """ Test Cases for Product Model """

    @classmethod
    def setUpClass(cls):
        """ This runs once before the entire test suite """
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Product.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """
        db.session.close()

    def setUp(self):
        """ This runs before each test """
        db.session.query(Product).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """ This runs after each test """
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_a_product(self):
        """It should Create a product and assert that it exists"""
        product = Product(name="product1", price=10, category="category1", stock=10, create_date=date.today())
        self.assertEqual(str(product), "<Product product1 id=[None]>")
        self.assertTrue(product is not None)
        self.assertEqual(product.id, None)
        self.assertEqual(product.name, "product1")
        self.assertEqual(product.price, 10)
        self.assertEqual(product.category, "category1")
        self.assertEqual(product.stock, 10)
        self.assertEqual(product.create_date, date.today())
        product = Product(name="product1", desc="description of product1", price=20, category="category1", stock=20, create_date=date.today())
        self.assertEqual(product.price, 20)
        self.assertEqual(product.desc, "description of product1")
        self.assertEqual(product.stock, 20)

    def test_add_a_product(self):
        """It should Create a product and add it to the database"""
        products = Product.all()
        self.assertEqual(products, [])
        product = Product(name="product1", price=10, category="category1", stock=10, create_date=date.today())
        self.assertTrue(product is not None)
        self.assertEqual(product.id, None)
        product.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(product.id)
        products = Product.all()
        self.assertEqual(len(products), 1)

    def test_read_a_product(self):
        """It should Read a Product"""
        product = ProductFactory()
        logging.debug(product)
        product.id = None
        product.create()
        self.assertIsNotNone(product.id)
        # Fetch it back
        found_product = Product.find(product.id)
        self.assertEqual(found_product.id, product.id)
        self.assertEqual(found_product.name, product.name)
        self.assertEqual(found_product.price, product.price)
        self.assertEqual(found_product.desc, product.desc)
        self.assertEqual(found_product.category, product.category)
        self.assertEqual(found_product.stock, product.stock)
        self.assertEqual(found_product.create_date, product.create_date)
