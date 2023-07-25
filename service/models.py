"""
Models for Product

All of the models are stored in this module
"""
import logging
from datetime import date
# from flask import Flask
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()


# Function to initialize the database
def init_db(app):
    """ Initializes the SQLAlchemy app """
    Product.init_db(app)


class DataValidationError(Exception):
    """ Used for an data validation errors when deserializing """

# pylint: disable=too-many-instance-attributes


class Product(db.Model):
    """
    Class that represents a Product
    """

    app = None

    # Table Schema
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(63), nullable=False)
    price = db.Column(db.Float(), nullable=False)
    desc = db.Column(db.String(256))
    category = db.Column(db.String(63), nullable=False)
    stock = db.Column(db.Integer(), nullable=False)
    create_date = db.Column(db.Date(), nullable=False, default=date.today())
    available = db.Column(db.Boolean(), nullable=False, default=True)
    likes = db.Column(db.Integer(), nullable=False, default=0)

    def __repr__(self):
        return f"<Product {self.name} id=[{self.id}]>"

    def create(self):
        """
        Creates a Product to the database
        """
        logger.info("Creating product %s", self.name)
        self.id = None  # pylint: disable=invalid-name
        db.session.add(self)
        db.session.commit()

    def update(self):
        """
        Updates a Product to the database
        """
        logger.info("Saving %s", self.name)
        if not self.id:
            raise DataValidationError("Update called with empty ID field")
        db.session.commit()

    def delete(self):
        """ Removes a Product from the data store """
        logger.info("Deleting product %s", self.name)
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """ Serializes a Product into a dictionary """
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "desc": self.desc,
            "category": self.category,
            "stock": self.stock,
            "create_date": self.create_date.isoformat(),
            "available": self.available,
            "likes": self.likes
        }

    def deserialize(self, data):
        """
        Deserializes a Product from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.name = data["name"]
            self.price = data["price"]
            if "desc" in data:
                self.desc = data["desc"]
            self.category = data["category"]
            self.stock = data["stock"]
            self.create_date = date.fromisoformat(data["create_date"])
            if isinstance(data["available"], bool):
                self.available = data["available"]
            else:
                raise DataValidationError("Invalid Attribute: available must be a boolean: "
                                          + str(type(data["available"])))
            self.likes = data["likes"]
        except KeyError as error:
            raise DataValidationError("Invalid Product: missing " + error.args[0]) from error
        except TypeError as error:
            raise DataValidationError("Invalid Product: body of request contained bad or no data " + str(error)) from error
        return self

    @classmethod
    def init_db(cls, app):
        """ Initializes the database session """
        logger.info("Initializing database")
        cls.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    def all(cls) -> list:
        """ Returns all of the Products in the database """
        logger.info("Processing all Products")
        return cls.query.all()

    @classmethod
    def find(cls, product_id: int):
        """ Finds a Product by it's ID """
        logger.info("Processing lookup for id %s ...", product_id)
        return cls.query.get(product_id)

    @classmethod
    def find_or_404(cls, product_id: int):
        """Find a Product by it's id

        :param product_id: the id of the Product to find
        :type product_id: int

        :return: an instance with the product_id, or 404_NOT_FOUND if not found
        :rtype: Product

        """
        logger.info("Processing lookup or 404 for id %s ...", product_id)
        return cls.query.get_or_404(product_id)

    @classmethod
    def find_by_name(cls, name: str) -> list:
        """Returns all Products with the given name

        :param name: the name of the Products you want to match
        :type name: str

        :return: a collection of Products with that name
        :rtype: list

        """
        logger.info("Processing name query for %s ...", name)
        return cls.query.filter(cls.name == name)

    @classmethod
    def find_by_category(cls, category: str) -> list:
        """Returns all of the Products in a category

        :param category: the category of the Products you want to match
        :type category: str

        :return: a collection of Products in that category
        :rtype: list

        """
        logger.info("Processing category query for %s ...", category)
        return cls.query.filter(cls.category == category)

    @classmethod
    def find_by_price(cls, price: float) -> list:
        """Returns all of the Products of a given price

        :param category: the price of the Products you want to match
        :type category: float

        :return: a collection of Products with that price
        :rtype: list

        """
        logger.info("Processing price query for %s ...", price)
        return cls.query.filter(cls.price == price)

    @classmethod
    def find_by_stock(cls, stock: int) -> list:
        """Returns all of the Products of a given stock

        :param category: the stock of the Products you want to match
        :type category: int

        :return: a collection of Products with that stock
        :rtype: list

        """
        logger.info("Processing stock query for %s ...", stock)
        return cls.query.filter(cls.stock == stock)

    @classmethod
    def find_by_create_date(cls, create_date: date) -> list:
        """Returns all of the Products of a given date

        :param category: the date of the Products you want to match
        :type category: date

        :return: a collection of Products with that date
        :rtype: list

        """
        logger.info("Processing date query for %s ...", create_date)
        return cls.query.filter(cls.create_date == create_date)

    @classmethod
    def find_by_available(cls, available: bool = True) -> list:
        """Returns all of the Products that are available

        :param available: the availability of the Products you want to match
        :type available: bool

        :return: a collection of Products with that availability
        :rtype: list

        """
        logger.info("Processing availability query for %s ...", available)
        return cls.query.filter(cls.available == available)

    def purchase(self):
        """Purchases the product and updates the stock and availability"""
        if self.stock > 0:
            self.stock -= 1

            if self.stock == 0:
                self.available = False

            db.session.commit()

            return True
        else:
            return False