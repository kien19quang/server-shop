from flask import Blueprint, jsonify, request
from app.models.user_model import UserModel
import jwt
from datetime import datetime, timedelta
from app.middleware.auth_middleware import token_required

user_bp = Blueprint('user', __name__)
JWT_SECRET_KEY = 'shop-access-token'

@user_bp.route('/login', methods=['POST'])
def login():
  data = request.json
  email = data.get('email')
  password = data.get('password')

  if not email or not password:
    return jsonify({"error": "Email và password không được để trống"}), 400

  user = UserModel.get_user_by_email(email)
  if not user:
    return jsonify({"error": "Email không tồn tại"}), 404

  # Kiểm tra password
  if user["password"] != password:
    return jsonify({"error": "Sai mật khẩu"}), 401

  # Tạo payload chứa thông tin người dùng
  payload = {
    "user": {
      "_id": str(user["_id"]),
      "email": user["email"],
      "fullname": user["fullname"],
      "role": user["role"]
    }
  }

  # Tạo JWT access token
  try:
    access_token = jwt.encode(
      payload,
      JWT_SECRET_KEY,
      algorithm='HS256'
    )
  except Exception as e:
    return jsonify({"error": "Lỗi tạo token"}), 500

  # Trả về payload và token
  return jsonify({
    "user": payload["user"],
    "accessToken": access_token,
    "expiresIn": int((datetime.now() + timedelta(days=58)).timestamp())  # 58 ngày
  }), 200

@user_bp.route('/create_user', methods=['POST'])
def create_user():
  data = request.json
  fullname = data.get('fullname')
  email = data.get('email')
  password = data.get('password')
  role = data.get('role', "USER")
  
  if not fullname:
    return jsonify({"error": "Fullname là bắt buộc"}), 400
  if not email:
    return jsonify({"error": "Email là bắt buộc"}), 400
  if not password:
    return jsonify({"error": "Password là bắt buộc"}), 400

  # Kiểm tra xem email đã tồn tại chưa
  if UserModel.get_user_by_email(email):
    return jsonify({"error": "Email đã tồn tại"}), 400

  UserModel.create_user(fullname, password, email, role)
  return jsonify({"message": "Tạo user thành công"}), 201

@user_bp.route('/get_list', methods=['GET'])
@token_required
def get_all_users(current_user):
  if (current_user["role"] != 'ADMIN'):
    return jsonify({"error_message": "Bạn không có quyền thực hiện hành động này"}), 400
  
  users = UserModel.get_all_users()
  return jsonify(users), 200

@user_bp.route('admin/get_list', methods=['GET'])
@token_required
def get_all_admin(current_user):
  if (current_user["role"] != 'ADMIN'):
    return jsonify({"error_message": "Bạn không có quyền thực hiện hành động này"}), 400
  
  admins = UserModel.get_all_users({ "role": 'ADMIN' })
  return jsonify(admins), 200

@user_bp.route('/update/<id>', methods=['PUT'])
@token_required
def update_user(current_user, id):
  update_data = request.json
  result = UserModel.update_user(id, update_data)
  
  if result.matched_count == 0:
    return jsonify({"error_message": "Không tìm thấy người dùng"}), 404
  
  return jsonify({"message": "Cập nhật thông tin người dùng thành công"}), 200

@user_bp.route('/delete/<id>', methods=['DELETE'])
@token_required
def delete_user(current_user, id):
  result = UserModel.delete_user(id)
    
  if result.deleted_count == 0:
    return jsonify({"error_message": "Không tìm thấy người dùng"}), 404
    
  return jsonify({"message": "Xoá người dùng thành công"}), 200