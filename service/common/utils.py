"""
Utils function

This module contains utility functions for filtering a list of products based on criteria
"""


def apply_filters(products, filters):
    """Apply filters to a list of products."""
    filtered_products = products

    # Filter by category
    if "category" in filters:
        category = filters["category"]
        filtered_products = [product for product in filtered_products if product.category == category]

    # Filter by price
    if "price" in filters:
        price = float(filters["price"])
        filtered_products = [product for product in filtered_products if product.price == price]

    # Filter by stock
    if "stock" in filters:
        stock = int(filters["stock"])
        filtered_products = [product for product in filtered_products if product.stock == stock]

    return filtered_products
