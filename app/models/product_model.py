from app import mongo
from app.utils.serialization import serialize_document, cursor_to_list, string_to_object_id

class ProductModel:
  collection = mongo.db.products

  @staticmethod
  def create_product(name, price, description, images, extra_info):
    try:
      price = float(price)
    except ValueError:
      return {"error_message": "Giá sản phẩm phải là số float."}, 400
    
    product_data = {
      "name": name,
      "price": price,
      "description": description,
      "images": images,
      "extra_info": extra_info
    }

    return ProductModel.collection.insert_one(product_data)
  
  def get_all_products():
    products_cursor = ProductModel.collection.find()
    return cursor_to_list(products_cursor)
  
  @staticmethod
  def get_product_by_id(product_id):
    object_id = string_to_object_id(product_id)
    product = ProductModel.collection.find_one({"_id": object_id})
    return serialize_document(product) if product else None
  
  @staticmethod
  def update_product(product_id, update_data):
    object_id = string_to_object_id(product_id)

    return ProductModel.collection.update_one({"_id": object_id}, {"$set": update_data})
  
  @staticmethod
  def delete_product(product_id):
    object_id = string_to_object_id(product_id)

    return ProductModel.collection.delete_one({"_id": object_id})