from app import mongo
from app.utils.serialization import serialize_document, cursor_to_list, string_to_object_id

class UserModel:
  collection = mongo.db.users

  @staticmethod
  def create_user(fullname, password, email, role = "USER"):
    user_data = {
      "fullname": fullname,
      "password": password,
      "email": email,
      "role": role
    }

    return UserModel.collection.insert_one(user_data)
  
  @staticmethod 
  def get_user_by_email(email):
    user = UserModel.collection.find_one({ "email": email })
    return serialize_document(user) if user else None
  
  @staticmethod
  def get_all_users(filter = {}):
    users_cursor = UserModel.collection.find(filter)
    return cursor_to_list(users_cursor)
  
  @staticmethod
  def update_user(id, update_data):
    object_id = string_to_object_id(id)
    return UserModel.collection.update_one({"_id": object_id}, {"$set": update_data})
  
  @staticmethod
  def delete_user(id):
    object_id = string_to_object_id(id)
    return UserModel.collection.delete_one({"_id": object_id})