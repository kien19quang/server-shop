import jwt
from flask import request, jsonify
from functools import wraps

JWT_SECRET_KEY = 'shop-access-token'

def token_required(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    token = None
    
    # Lấy token từ headers (Authorization)
    if 'Authorization' in request.headers:
        auth_header = request.headers['Authorization']
        token = auth_header.split(" ")[1]  # Bearer <token>
    
    if not token:
        return jsonify({"message": "Token is missing!"}), 401

    try:
        # Giải mã token
        data = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
        current_user = data['user']  # Lấy thông tin người dùng từ payload
    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token has expired!"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"message": "Invalid token!"}), 401

    # Thêm thông tin người dùng vào context để các API khác sử dụng
    return f(current_user, *args, **kwargs)
  
  return decorated
