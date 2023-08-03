"""
My Service

Describe what your service does here
"""

from flask import jsonify, request, url_for, abort
from service.common import status  # HTTP Status Codes
from service.models import Product
from service.common.utils import apply_filters

# Import Flask application
from . import app

############################################################
# Health Endpoint
############################################################
@app.route("/health")
def health():
    """Health Status"""
    return {"status": 'OK'}, status.HTTP_200_OK

######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """ Root URL response """
    return (
        jsonify(
            name="REST APIs for the Products service",
            paths=url_for("create_products", _external=True),
        ),
        status.HTTP_200_OK,
    )


######################################################################
#  R E S T   A P I   E N D P O I N T S
######################################################################

# Place your REST API code here ...

######################################################################
# CREATE A NEW PRODUCT
######################################################################
@app.route("/products", methods=["POST"])
def create_products():
    """
    Creates a Product
    This endpoint will create a Product based the data in the body that is posted
    """
    app.logger.info("Request to create a Product")
    check_content_type("application/json")
    product = Product()
    product.deserialize(request.get_json())
    product.create()
    message = product.serialize()
    location_url = url_for("get_products", product_id=product.id, _external=True)
    app.logger.info("Product with ID [%s] created.", product.id)
    return jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}

######################################################################
# READ A PRODUCT
######################################################################


@app.route("/products/<int:product_id>", methods=["GET"])
def get_products(product_id):
    """
    Retrieve a single product

    This endpoint will return a product based on it's id
    """
    app.logger.info("Request for product with id: %s", product_id)
    product = Product.find(product_id)
    if not product:
        abort(status.HTTP_404_NOT_FOUND, f"Product with id '{product_id}' was not found.")

    app.logger.info("Returning product: %s", product.name)
    return jsonify(product.serialize()), status.HTTP_200_OK

######################################################################
# UPDATE A PRODUCT
######################################################################


@app.route("/products/<int:product_id>", methods=["PUT"])
def update_products(product_id):
    """
    Update a Product
    This endpoint will update a Product based on the content that is posted
    """
    app.logger.info("Request to update the product with id: %s", product_id)
    check_content_type("application/json")

    product = Product.find(product_id)
    if not product:
        abort(
            status.HTTP_404_NOT_FOUND, f"Product with id '{product_id}' was not found."
        )

    product.deserialize(request.get_json())
    product.id = product_id
    product.update()
    message = product.serialize()

    app.logger.info("Product with id [%s] successfully updated.", product.id)
    return jsonify(message), status.HTTP_200_OK

######################################################################
# LIST PRODUCTS
######################################################################


@app.route("/products", methods=["GET"])
def list_products():
    """Returns all of the Products based on filters."""
    app.logger.info("Request to list Products...")

    # Get the query string parameters from the request
    filters = request.args.to_dict()

    # Call a function to retrieve the list of all products
    products = Product.all()

    # Apply filters and get the filtered results
    filtered_products = apply_filters(products, filters)

    results = [product.serialize() for product in filtered_products]
    return jsonify(results), status.HTTP_200_OK


######################################################################
# DELETE A PRODUCT
######################################################################
@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_products(product_id):
    """
    Delete an existing Product
    This endpoint will delete a Product based on it's id
    """
    app.logger.info("Request to delete product with id: %s", product_id)
    product = Product.find(product_id)

    if product:
        product.delete()

    return jsonify(message="success"), status.HTTP_204_NO_CONTENT


def check_content_type(content_type):
    """Checks that the media type is correct"""
    if "Content-Type" not in request.headers:
        app.logger.error("No Content-Type specified.")
        abort(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            f"Content-Type must be {content_type}",
        )

    if request.headers["Content-Type"] == content_type:
        return

    app.logger.error("Invalid Content-Type: %s", request.headers["Content-Type"])
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        f"Content-Type must be {content_type}",
    )

######################################################################
# LIKE A PRODUCT
######################################################################


@app.route("/products/<int:product_id>/like", methods=["PUT"])
def like_products(product_id):
    """
    Like a Product
    This endpoint will like a Product based on it's id
    """
    app.logger.info("Request to like the product with id: %s", product_id)
    check_content_type("application/json")

    product = Product.find(product_id)
    if not product:
        abort(
            status.HTTP_404_NOT_FOUND, f"Product with id '{product_id}' was not found."
        )

    product.likes += 1
    product.id = product_id
    product.update()
    message = product.serialize()

    app.logger.info("Product with id [%s] successfully liked.", product.id)
    return jsonify(message), status.HTTP_200_OK

######################################################################
# PURCHASE A PRODUCT
######################################################################


@app.route("/products/<int:product_id>/purchase", methods=["POST"])
def purchase_product(product_id):
    """
    Purchases a Product

    This endpoint will handle the purchase of a product based on its id
    """
    app.logger.info("Request to purchase product with id: %s", product_id)

    # Find the product with the given product_id
    product = Product.find(product_id)

    if not product:
        abort(status.HTTP_404_NOT_FOUND, f"Product with id '{product_id}' was not found.")

    if product.purchase():
        return jsonify(product.serialize()), status.HTTP_200_OK
    return jsonify({"error": "Product out of stock"}), status.HTTP_409_CONFLICT  # Removed the else statement
