# Copyright 2016, 2023 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Test cases for Product Model

Test cases can be run with:
    nosetests
    coverage report -m

While debugging just these tests it's convenient to use this:
    nosetests --stop tests/test_models.py:TestProductModel

"""
import os
import logging
import unittest
from decimal import Decimal
from service.models import Product, Category, db
from service import app
from tests.factories import ProductFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/postgres"
)


######################################################################
#  P R O D U C T   M O D E L   T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestProductModel(unittest.TestCase):
    """Test Cases for Product Model"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Product.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        db.session.query(Product).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_a_product(self):
        """It should Create a product and assert that it exists"""
        product = Product(name="Fedora", description="A red hat", price=12.50, available=True, category=Category.CLOTHS)
        self.assertEqual(str(product), "<Product Fedora id=[None]>")
        self.assertTrue(product is not None)
        self.assertEqual(product.id, None)
        self.assertEqual(product.name, "Fedora")
        self.assertEqual(product.description, "A red hat")
        self.assertEqual(product.available, True)
        self.assertEqual(product.price, 12.50)
        self.assertEqual(product.category, Category.CLOTHS)

    def test_add_a_product(self):
        """It should Create a product and add it to the database"""
        products = Product.all()
        self.assertEqual(products, [])
        product = ProductFactory()
        product.id = None
        product.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(product.id)
        products = Product.all()
        self.assertEqual(len(products), 1)
        # Check that it matches the original product
        new_product = products[0]
        self.assertEqual(new_product.name, product.name)
        self.assertEqual(new_product.description, product.description)
        self.assertEqual(Decimal(new_product.price), product.price)
        self.assertEqual(new_product.available, product.available)
        self.assertEqual(new_product.category, product.category)

    #
    # ADD YOUR TEST CASES HERE
    #

    def test_read_a_product(self):
        """It should Read a Product"""
        product = ProductFactory()
        product.id = None
        product.create()
        self.assertIsNotNone(product.id)
        # Fetch it back
        found_product = Product.find(product.id)
        self.assertEqual(found_product.id, product.id)
        self.assertEqual(found_product.name, product.name)
        self.assertEqual(found_product.description, product.description)
        self.assertEqual(found_product.price, product.price)
        self.assertEqual(found_product.available, product.available)
        self.assertEqual(found_product.category, product.category)

    def test_update_a_product(self):
        """It should Update a Product"""
        product = ProductFactory()
        product.id = None
        product.create()
        self.assertIsNotNone(product.id)
        # Update the product
        product.name = "UpdatedName"
        product.description = "Updated Description"
        product.price = 99.99
        product.available = not product.available
        product.category = Category.FOOD  # assuming Category.FOOD exists
        product.update()
        # Fetch it back
        updated_product = Product.find(product.id)
        self.assertEqual(updated_product.name, "UpdatedName")
        self.assertEqual(updated_product.description, "Updated Description")
        self.assertEqual(updated_product.price, 99.99)
        self.assertEqual(updated_product.available, product.available)
        self.assertEqual(updated_product.category, Category.FOOD)

    def test_delete_a_product(self):
        """It should Delete a Product"""
        product = ProductFactory()
        product.id = None
        product.create()
        product_id = product.id
        self.assertIsNotNone(product_id)
        # Delete it
        product.delete()
        # Try to fetch it back
        deleted_product = Product.find(product_id)
        self.assertIsNone(deleted_product)

    def test_list_all_products(self):
        """It should List All Products"""
        ProductFactory.create_batch(5)
        products = Product.all()
        self.assertEqual(len(products), 5)

    def test_search_product_by_name(self):
        """It should Search Products by Name"""
        product = ProductFactory(name="UniqueProductName")
        product.id = None
        product.create()
        found = Product.find_by_name("UniqueProductName")
        self.assertTrue(any(p.id == product.id for p in found))

    def test_search_product_by_category(self):
        """It should Search Products by Category"""
        product = ProductFactory(category=Category.CLOTHS)
        product.id = None
        product.create()
        found = Product.find_by_category(Category.CLOTHS)
        self.assertTrue(any(p.id == product.id for p in found))

    def test_search_product_by_availability(self):
        """It should Search Products by Availability"""
        product = ProductFactory(available=True)
        product.id = None
        product.create()
        found = Product.find_by_availability(True)
        self.assertTrue(any(p.id == product.id for p in found))

