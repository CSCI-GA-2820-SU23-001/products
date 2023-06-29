"""
Test Factory to make fake objects for testing
"""
from datetime import date

import factory
from factory.fuzzy import FuzzyChoice, FuzzyDate, FuzzyFloat, FuzzyInteger
from service.models import Product


class ProductFactory(factory.Factory):
    """Creates fake products"""

    class Meta:  # pylint: disable=too-few-public-methods
        """Maps factory to data model"""

        model = Product

    id = factory.Sequence(lambda n: n)
    name = FuzzyChoice(choices=["product1", "product2", "product3, product4, product5"])
    price = FuzzyFloat(10, 60)
    desc = factory.Faker("description of product1")
    category = FuzzyChoice(choices=["category1", "category2", "category3, category4, category5"])
    stock = FuzzyInteger(0, 40)
    create_date = FuzzyDate(date(2008, 1, 1))