from flask import Blueprint, request, jsonify
from app.models.product_model import ProductModel
from app.middleware.auth_middleware import token_required
from app import redis_client
import json

product_bp = Blueprint('product', __name__)
CACHE_KEY_PRODUCTS = "products_cache"

@product_bp.route('/create', methods=['POST'])
@token_required
def create_product(current_user):
  if (current_user["role"] != 'ADMIN'):
    return jsonify({"error_message": "Bạn không có quyền thực hiện hành động này"}), 400
  
  data = request.json
  name = data.get('name')
  price = data.get('price')
  description = data.get('description')
  images = data.get('images')
  extra_info = data.get('extra_info')

  if not name or not price:
    return jsonify({"error_message": "Vui lòng cung cấp đầy đủ thông tin"}), 400

  ProductModel.create_product(name, price, description, images, extra_info)

  redis_client.delete(CACHE_KEY_PRODUCTS)

  return jsonify({"message": "Tạo sản phẩm thành công"}), 201

@product_bp.route('/products', methods=['GET'])
def get_all_products():
  cached_products = redis_client.get(CACHE_KEY_PRODUCTS)
  if cached_products:
    # Chuyển từ JSON sang Python object
    return jsonify(json.loads(cached_products)), 200

  # Nếu không có cache, lấy từ database
  products = ProductModel.get_all_products()

  products = ProductModel.get_all_products()
  redis_client.set(CACHE_KEY_PRODUCTS, json.dumps(products), ex=300)
  return jsonify(products), 200

@product_bp.route('/detail/<product_id>', methods=['GET'])
def get_product_by_id(product_id):
  product = ProductModel.get_product_by_id(product_id)
  if product:
    return jsonify(product), 200
  return jsonify({"error_message": "Không tìm thấy sản phẩm"}), 404

@product_bp.route('/update/<product_id>', methods=['PUT'])
@token_required
def update_product(current_user, product_id):
  if (current_user["role"] != 'ADMIN'):
    return jsonify({"error_message": "Bạn không có quyền thực hiện hành động này"}), 400
  
  update_data = request.json
  result = ProductModel.update_product(product_id, update_data)

  if result:
    redis_client.delete(CACHE_KEY_PRODUCTS)
    return jsonify({"message": "Cập nhật sản phẩm thành công"}), 200
  return jsonify({"error_message": "Cập nhật thất bại"}), 400

@product_bp.route('/delete/<product_id>', methods=['DELETE'])
@token_required
def delete_product(current_user, product_id):
  if (current_user["role"] != 'ADMIN'):
    return jsonify({"error_message": "Bạn không có quyền thực hiện hành động này"}), 400
  
  result = ProductModel.delete_product(product_id)
  if result:
    redis_client.delete(CACHE_KEY_PRODUCTS)
    return jsonify({"message": "Xoá sản phẩm thành công"}), 200
  return jsonify({"error": "Xoá sản phẩm thất bại"}), 400