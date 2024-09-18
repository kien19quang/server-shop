from app.controllers.user_controller import user_bp
from app.controllers.product_controller import product_bp

def register_routes(app):
  app.register_blueprint(user_bp, url_prefix='/user')
  app.register_blueprint(product_bp, url_prefix='/product')