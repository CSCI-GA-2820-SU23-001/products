"""
Product Service with Swagger
Paths:
------
GET / - Displays a UI for Selenium testing
GET /products - Returns a list all of the products
GET /products/{product_id} - Returns the products with a given id number
POST /products - creates a new product
PUT /products/{id} - update an product
DELETE /products/{id} - delete an product
"""

from flask import jsonify, request, url_for, abort
from flask import request, abort
from flask_restx import Resource, fields, reqparse


from service.common import status  # HTTP Status Codes
from service.models import Product, DataValidationError
from service.common.utils import apply_filters

# Import Flask application
from . import app, api

############################################################
# Health Endpoint
############################################################


@app.route("/health")
def health():
    """Health Status"""
    return {"status": 'OK'}, status.HTTP_200_OK

# Define the model so that the docs reflect what can be sent
create_product_model = api.model(
    "Product",
    {
        "name": fields.String(required=True, description="The name of the Product"),
        "price": fields.Float(required=True, description="The price of the Product"),
        "desc": fields.String(required=False, description="The description of the Product"),
        "category": fields.String(required=True, description="The category of the Product"),
        "stock": fields.Integer(required=True, description="The stock number of the Product"),
        "create_date": fields.Date(required=True, description="The create date of the Product"),
        "available": fields.Boolean(required=True, description="Whether the Product is available"),
        "likes": fields.Integer(required=True, description="The degree of like of Product"),      

    },
)

product_model = api.inherit(
    "ProductModel",
    create_product_model,
    {
        "id": fields.Integer(
            readOnly=True, description="The product_id assigned internally by service"
        ),
    },
)


# query string arguments
product_args = reqparse.RequestParser()
product_args.add_argument(
    "category", type=str, location="args", required=False, help="Query Product by Category"
)


######################################################################
# GET INDEX
######################################################################


@app.route("/")
def index():
    """ Root URL response """
    return app.send_static_file("index.html")



######################################################################
#  R E S T   A P I   E N D P O I N T S
######################################################################

# Place your REST API code here ...

######################################################################
#  PATH: /products/{product_id}
######################################################################
@api.route("/products/<product_id>")
@api.param("product_id", "The Product identifier")
class ProductResource(Resource):
    """
    ProductResource class

    Allows the manipulation of a single Product
    GET /product{id} - Returns an Product with the id
    PUT /product{id} - Update an Product with the id
    DELETE /product{id} -  Deletes an Product with the id
    """

    # ------------------------------------------------------------------
    # RETRIEVE AN PRODUCT
    # ------------------------------------------------------------------
    @api.doc("get_products")
    @api.response(404, "Product not found")
    @api.marshal_with(product_model)
    def get(self, product_id):
        """
        Retrieve a single Product
        This endpoint will return an Product based on its id
        """
        app.logger.info("Request for Product with id: %s", product_id)

        # See if the product exists and abort if it doesn't
        product = Product.find(product_id)
        if not product:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Product with id '{product_id}' could not be found.",
            )
        app.logger.info("Returning product: %s", product.id)
        return product.serialize(), status.HTTP_200_OK
    
    # ------------------------------------------------------------------
    #  UPDATE AN PRODUCT
    # ------------------------------------------------------------------
    @api.doc("update_products")
    @api.response(404, "Product not found")
    @api.response(400, "The posted Product data was not valid")
    @api.expect(product_model)
    @api.marshal_with(product_model)
    def put(self, product_id):
        """
        Update an Product
        This endpoint will update an Product based the body that is posted
        """
        app.logger.info("Request to update product with id: %s", product_id)

        product = Product.find(product_id)
        if not product:
            abort(status.HTTP_404_NOT_FOUND, f"Product with id '{product_id}' does not exist.")

        # Update other fields as needed
        data = api.payload
        product.deserialize(data)
        product.update()

        return product.serialize(), status.HTTP_200_OK

    # ------------------------------------------------------------------
    # DELETE AN PRODUCT
    # ------------------------------------------------------------------
    @api.doc("delete_products")
    @api.response(204, "Product deleted")
    def delete(self, product_id):
        """
        Delete an Product
        This endpoint will delete an product based the id specified in the path
        """
        app.logger.info("Request to delete product with id: %s", product_id)
        account = Product.find(product_id)
        if account:
            account.delete()
            app.logger.info("Product with id [%s] was deleted", product_id)

        return "", status.HTTP_204_NO_CONTENT
    
    # ------------------------------------------------------------------
    # LIKE AN PRODUCT
    # ------------------------------------------------------------------
    @api.doc("like_products")
    @api.response(200, "The product has been liked!")
    @api.response(404, "Product not found")
    def like(self, product_id):
        """
        Like a Product
        This endpoint will like a Product based on it's id
        """
        app.logger.info("Request to like product with id: %s", product_id)
        product = Product.find(product_id)
        if not product:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Product with id '{product_id}' was not found."
            )
        
        product.likes += 1
        product.id=product_id
        product.update()

        app.logger.info("Product with id [%s] successfully liked.", product.id)

        return product.serialize(), status.HTTP_200_OK


######################################################################
#  PATH: /products
######################################################################
@api.route("/products", strict_slashes=False)
class ProductCollection(Resource):
    """
    ProductCollection class

    GET / - List/Query Products
    POST / - Add a New Product
    """

    # ------------------------------------------------------------------
    # LIST ALL PRODUCTS
    # ------------------------------------------------------------------
    @api.doc("list_products")
    @api.expect(product_args, validate=True)
    @api.marshal_list_with(product_model)
    def get(self):
        """Returns all of the Products"""
        app.logger.info("Request to list all products")

        products = []
        args = product_args.parse_args()

        if args["category"]:
            products = Product.find_by_category(args["category"])
        else:
            products = Product.all()

        resp = [product.serialize() for product in products]
        app.logger.info("[%s] products returned", len(resp))
        return resp, status.HTTP_200_OK

    # ------------------------------------------------------------------
    # ADD A NEW PRODUCT
    # ------------------------------------------------------------------
    @api.doc("create_products")
    @api.response(400, "The posted data was not valid")
    @api.expect(create_product_model)
    @api.marshal_with(product_model, code=201)
    def post(self):
        """
        Creates an Product
        This endpoint will create an Product based the data in the body that is posted
        """
        app.logger.info("Request to Create product...")
        product_data = api.payload
        product = Product()
        product.deserialize(product_data)
        product.create()
        app.logger.info("New product %s is created!", product.id)

        resp = product.serialize()
        location_url = api.url_for(ProductResource, product_id=product.id, _external=True)
        return resp, status.HTTP_201_CREATED, {"Location": location_url}


# ######################################################################
# # CREATE A NEW PRODUCT
# ######################################################################
# @app.route("/products", methods=["POST"])
# def create_products():
#     """
#     Creates a Product
#     This endpoint will create a Product based the data in the body that is posted
#     """
#     app.logger.info("Request to create a Product")
#     check_content_type("application/json")
#     product = Product()
#     product.deserialize(request.get_json())
#     product.create()
#     message = product.serialize()
#     location_url = url_for("get_products", product_id=product.id, _external=True)
#     app.logger.info("Product with ID [%s] created.", product.id)
#     return jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}

# ######################################################################
# # READ A PRODUCT
# ######################################################################


# @app.route("/products/<int:product_id>", methods=["GET"])
# def get_products(product_id):
#     """
#     Retrieve a single product

#     This endpoint will return a product based on it's id
#     """
#     app.logger.info("Request for product with id: %s", product_id)
#     product = Product.find(product_id)
#     if not product:
#         abort(status.HTTP_404_NOT_FOUND, f"Product with id '{product_id}' was not found.")

#     app.logger.info("Returning product: %s", product.name)
#     return jsonify(product.serialize()), status.HTTP_200_OK

# ######################################################################
# # UPDATE A PRODUCT
# ######################################################################


# @app.route("/products/<int:product_id>", methods=["PUT"])
# def update_products(product_id):
#     """
#     Update a Product
#     This endpoint will update a Product based on the content that is posted
#     """
#     app.logger.info("Request to update the product with id: %s", product_id)
#     check_content_type("application/json")

#     product = Product.find(product_id)
#     if not product:
#         abort(
#             status.HTTP_404_NOT_FOUND, f"Product with id '{product_id}' was not found."
#         )

#     product.deserialize(request.get_json())
#     product.id = product_id
#     product.update()
#     message = product.serialize()

#     app.logger.info("Product with id [%s] successfully updated.", product.id)
#     return jsonify(message), status.HTTP_200_OK

# ######################################################################
# # LIST PRODUCTS
# ######################################################################


# @app.route("/products", methods=["GET"])
# def list_products():
#     """Returns all of the Products based on filters."""
#     app.logger.info("Request to list Products...")

#     # Get the query string parameters from the request
#     filters = request.args.to_dict()

#     # Call a function to retrieve the list of all products
#     products = Product.all()

#     # Apply filters and get the filtered results
#     filtered_products = apply_filters(products, filters)

#     results = [product.serialize() for product in filtered_products]
#     return jsonify(results), status.HTTP_200_OK


# ######################################################################
# # DELETE A PRODUCT
# ######################################################################
# @app.route("/products/<int:product_id>", methods=["DELETE"])
# def delete_products(product_id):
#     """
#     Delete an existing Product
#     This endpoint will delete a Product based on it's id
#     """
#     app.logger.info("Request to delete product with id: %s", product_id)
#     product = Product.find(product_id)

#     if product:
#         product.delete()

#     return jsonify(message="success"), status.HTTP_204_NO_CONTENT


# def check_content_type(content_type):
#     """Checks that the media type is correct"""
#     if "Content-Type" not in request.headers:
#         app.logger.error("No Content-Type specified.")
#         abort(
#             status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
#             f"Content-Type must be {content_type}",
#         )

#     if request.headers["Content-Type"] == content_type:
#         return

#     app.logger.error("Invalid Content-Type: %s", request.headers["Content-Type"])
#     abort(
#         status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
#         f"Content-Type must be {content_type}",
#     )

# ######################################################################
# # LIKE A PRODUCT
# ######################################################################


# @app.route("/products/<int:product_id>/like", methods=["PUT"])
# def like_products(product_id):
#     """
#     Like a Product
#     This endpoint will like a Product based on it's id
#     """
#     app.logger.info("Request to like the product with id: %s", product_id)
#     check_content_type("application/json")

#     product = Product.find(product_id)
#     if not product:
#         abort(
#             status.HTTP_404_NOT_FOUND, f"Product with id '{product_id}' was not found."
#         )

#     product.likes += 1
#     product.id = product_id
#     product.update()
#     message = product.serialize()

#     app.logger.info("Product with id [%s] successfully liked.", product.id)
#     return jsonify(message), status.HTTP_200_OK

# ######################################################################
# # PURCHASE A PRODUCT
# ######################################################################


# @app.route("/products/<int:product_id>/purchase", methods=["POST"])
# def purchase_product(product_id):
#     """
#     Purchases a Product

#     This endpoint will handle the purchase of a product based on its id
#     """
#     app.logger.info("Request to purchase product with id: %s", product_id)

#     # Find the product with the given product_id
#     product = Product.find(product_id)

#     if not product:
#         abort(status.HTTP_404_NOT_FOUND, f"Product with id '{product_id}' was not found.")

#     if product.purchase():
#         return jsonify(product.serialize()), status.HTTP_200_OK
#     return jsonify({"error": "Product out of stock"}), status.HTTP_409_CONFLICT  # Removed the else statement
