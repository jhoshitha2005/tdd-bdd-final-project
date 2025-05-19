# service/product_routes.py
######################################################################
# Product API Service Routes
######################################################################
from flask import Blueprint, jsonify, request, abort, make_response
from service.models import Product, db
from service.common import status

bp = Blueprint("products", __name__, url_prefix="/products")


@bp.route("", methods=["GET"])
def list_products():
    """List all products or filter by name/category/availability query params"""
    name = request.args.get("name")
    category = request.args.get("category")
    available = request.args.get("available")

    query = Product.query

    if name:
        query = query.filter(Product.name.ilike(f"%{name}%"))
    if category:
        query = query.filter(Product.category.has(name=category))
    if available is not None:
        # Convert query param to boolean
        available_bool = available.lower() in ["true", "1", "yes"]
        query = query.filter(Product.available == available_bool)

    products = query.all()
    results = [product.serialize() for product in products]
    return jsonify(results), status.HTTP_200_OK


@bp.route("/<int:product_id>", methods=["GET"])
def read_product(product_id):
    """Read a single Product by id"""
    product = Product.query.get(product_id)
    if not product:
        abort(make_response(jsonify(message=f"Product with id {product_id} not found"), status.HTTP_404_NOT_FOUND))
    return jsonify(product.serialize()), status.HTTP_200_OK


@bp.route("/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    """Update an existing Product by id"""
    product = Product.query.get(product_id)
    if not product:
        abort(make_response(jsonify(message=f"Product with id {product_id} not found"), status.HTTP_404_NOT_FOUND))

    data = request.get_json()
    if not data:
        abort(make_response(jsonify(message="Request body must be JSON"), status.HTTP_400_BAD_REQUEST))

    # Update fields if present
    if "name" in data:
        product.name = data["name"]
    if "description" in data:
        product.description = data["description"]
    if "price" in data:
        try:
            product.price = float(data["price"])
        except ValueError:
            abort(make_response(jsonify(message="Invalid price value"), status.HTTP_400_BAD_REQUEST))
    if "available" in data:
        product.available = bool(data["available"])
    if "category" in data:
        # Assuming category is a string for category name
        product.category = data["category"]

    db.session.commit()
    return jsonify(product.serialize()), status.HTTP_200_OK


@bp.route("/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    """Delete a Product by id"""
    product = Product.query.get(product_id)
    if not product:
        abort(make_response(jsonify(message=f"Product with id {product_id} not found"), status.HTTP_404_NOT_FOUND))

    db.session.delete(product)
    db.session.commit()
    return "", status.HTTP_204_NO_CONTENT
