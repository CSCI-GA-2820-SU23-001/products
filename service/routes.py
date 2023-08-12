"""
My Service

Describe what your service does here
"""


# from flask import abort
from flask_restx import Resource, fields, reqparse, inputs
from service.common import status  # HTTP Status Codes
from service.models import Product
# from service.common.utils import apply_filters

# Import Flask application
from . import app, api

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
    return app.send_static_file("index.html")


# Define the model so that the docs reflect what can be sent
create_model = api.model(
    "Product",
    {
        "name": fields.String(required=True, description="The name of the Product"),
        "price": fields.Float(required=True, description="The price of the Product"),
        "desc": fields.String(required=False, description="The description of the Product"),
        "category": fields.String(
            required=True,
            description="The category of Product (e.g., dog, cat, fish, etc.)",
        ),
        "stock": fields.Integer(required=True, description="The number of stock of the Product"),
        "create_date": fields.Date(required=True, description="The day the Product was created"),
        "available": fields.Boolean(
            required=True, description="Is the Product available for purchase?"
        ),
        # pylint: disable=protected-access
        # "gender": fields.String(
        #     enum=Gender._member_names_, description="The gender of the product"
        # ),
        "likes": fields.Integer(required=True, description="The number of like of the Product"),
    },
)

product_model = api.inherit(
    "ProductModel",
    create_model,
    {
        "id": fields.Integer(
            readOnly=True, description="The unique id assigned internally by service"
        ),
    },
)

# query string arguments
product_args = reqparse.RequestParser()
product_args.add_argument(
    "name", type=str, location="args", required=False, help="List Products by name"
)
product_args.add_argument(
    "category", type=str, location="args", required=False, help="List Products by category"
)
product_args.add_argument(
    "price", type=float, location="args", required=False, help="List Products by price"
)
product_args.add_argument(
    "stock", type=int, location="args", required=False, help="List Products by stock"
)
product_args.add_argument(
    "create_date", type=inputs.date, location="args", required=False, help="List Products by create_date"
)
product_args.add_argument(
    "available",
    type=inputs.boolean,
    location="args",
    required=False,
    help="List Products by availability",
)


######################################################################
#  PATH: /products/{id}
######################################################################
@api.route("/products/<product_id>")
@api.param("product_id", "The product identifier")
class productResource(Resource):
    """
    productResource class

    Allows the manipulation of a single product
    GET /product{id} - Returns a product with the id
    PUT /product{id} - Update a product with the id
    DELETE /product{id} -  Deletes a product with the id
    """

    # ------------------------------------------------------------------
    # RETRIEVE A product
    # ------------------------------------------------------------------
    @api.doc("get_products")
    @api.response(404, "product not found")
    @api.marshal_with(product_model)
    def get(self, product_id):
        """
        Retrieve a single product

        This endpoint will return a product based on it's id
        """
        app.logger.info("Request to Retrieve a product with id [%s]", product_id)
        product = Product.find(product_id)
        if not product:
            abort(status.HTTP_404_NOT_FOUND, f"product with id '{product_id}' was not found.")
        return product.serialize(), status.HTTP_200_OK

    # ------------------------------------------------------------------
    # UPDATE AN EXISTING product
    # ------------------------------------------------------------------
    @api.doc("update_products")
    @api.response(404, "product not found")
    @api.response(400, "The posted product data was not valid")
    @api.expect(product_model)
    @api.marshal_with(product_model)
    def put(self, product_id):
        """
        Update a product

        This endpoint will update a product based the body that is posted
        """
        app.logger.info("Request to Update a product with id [%s]", product_id)
        product = Product.find(product_id)
        if not product:
            abort(status.HTTP_404_NOT_FOUND, f"product with id '{product_id}' was not found.")
        app.logger.debug("Payload = %s", api.payload)
        data = api.payload
        product.deserialize(data)
        product.id = product_id
        product.update()
        return product.serialize(), status.HTTP_200_OK

    # ------------------------------------------------------------------
    # DELETE A product
    # ------------------------------------------------------------------
    @api.doc("delete_products")
    @api.response(204, "product deleted")
    def delete(self, product_id):
        """
        Delete a product

        This endpoint will delete a product based the id specified in the path
        """
        app.logger.info("Request to Delete a product with id [%s]", product_id)
        product = Product.find(product_id)
        if product:
            product.delete()
            app.logger.info("product with id [%s] was deleted", product_id)

        return "", status.HTTP_204_NO_CONTENT


######################################################################
#  PATH: /products
######################################################################
@api.route("/products", strict_slashes=False)
class productCollection(Resource):
    """Handles all interactions with collections of products"""

    # ------------------------------------------------------------------
    # LIST ALL products
    # ------------------------------------------------------------------
    @api.doc("list_products")
    @api.expect(product_args, validate=True)
    @api.marshal_list_with(product_model)
    def get(self):
        """Returns all of the products"""
        app.logger.info("Request to list products...")
        # products = []
        # args = product_args.parse_args()
        # print(args)
        # if args["id"]:
        #     app.logger.info("Filtering by id: %s", args["id"])
        #     products = Product.find_by_user_id(args["id"])
        # else:
        # app.logger.info("Returning unfiltered list.")
        products = Product.all()

        app.logger.info("[%s] products returned", len(products))
        results = [product.serialize() for product in products]
        return results, status.HTTP_200_OK

    # ------------------------------------------------------------------
    # ADD A NEW product
    # ------------------------------------------------------------------
    @api.doc("create_products")
    @api.response(400, "The posted data was not valid")
    @api.expect(create_model)
    @api.marshal_with(product_model, code=201)
    def post(self):
        """
        Creates a product
        This endpoint will create a product based the data in the body that is posted
        """
        app.logger.info("Request to Create a product")
        product = Product()
        app.logger.debug("Payload = %s", api.payload)
        product.deserialize(api.payload)
        product.create()
        app.logger.info("product with new id [%s] created!", product.id)
        location_url = api.url_for(productResource, product_id=product.id, _external=True)
        return product.serialize(), status.HTTP_201_CREATED, {"Location": location_url}


######################################################################
#  PATH: /products/{id}/purchase
######################################################################
@api.route("/products/<product_id>/purchase")
@api.param("product_id", "The product identifier")
class PurchaseResource(Resource):
    """Purchase actions on a product"""

    @api.doc("purchase_products")
    @api.response(404, "product not found")
    @api.response(409, "The product is not available for purchase")
    def put(self, product_id):
        """
        Purchase a product

        This endpoint will purchase a product and make it unavailable
        """
        app.logger.info("Request to Purchase a product")
        product = Product.find(product_id)
        if not product:
            abort(status.HTTP_404_NOT_FOUND, f"product with id [{product_id}] was not found.")
        if not product.available:
            abort(status.HTTP_409_CONFLICT, f"product with id [{product_id}] is not available.")
        if product.stock > 0:
            product.stock -= 1
            if product.stock == 0:
                product.available = False
            # db.session.commit()
            # return True
        # product.available = False
        product.update()
        app.logger.info("product with id [%s] has been purchased!", product.id)
        return product.serialize(), status.HTTP_200_OK


######################################################################
#  PATH: /products/{id}/like
######################################################################
@api.route("/products/<product_id>/like")
@api.param("product_id", "The product identifier")
class LikeResource(Resource):
    """Like actions on a product"""

    @api.doc("like_products")
    @api.response(404, "product not found")
    # @api.response(409, "The product is not available for purchase")
    def put(self, product_id):
        """
        Like a product

        This endpoint will like a product and increment the number of like by one
        """
        app.logger.info("Request to Like a product")
        product = Product.find(product_id)
        if not product:
            abort(status.HTTP_404_NOT_FOUND, f"product with id [{product_id}] was not found.")
        product.likes += 1
        # product.id = product_id

        product.update()
        app.logger.info("product with id [%s] has been liked!", product.id)
        return product.serialize(), status.HTTP_200_OK
    

######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################
def abort(error_code: int, message: str):
    """Logs errors before aborting"""
    app.logger.error(message)
    api.abort(error_code, message)


def init_db(dbname="products"):
    """Initialize the model"""
    Product.init_db(dbname)

def data_reset():
    """Removes all Products from the database"""
    Product.remove_all()