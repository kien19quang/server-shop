from bson import ObjectId

def serialize_document(document):
  if isinstance(document, list):
    return [serialize_document(doc) for doc in document]
  
  if isinstance(document, dict):
    if '_id' in document:
      document['_id'] = str(document['_id'])
    return {k: serialize_document(v) for k, v in document.items()}
  
  if isinstance(document, ObjectId):
    return str(document)
  
  return document


def cursor_to_list(cursor):
  return [serialize_document(doc) for doc in cursor]

def string_to_object_id(id):
  try:
    # Chuyển đổi id từ chuỗi thành ObjectId
    object_id = ObjectId(id)
    return object_id
  except Exception as e:
    # Xử lý lỗi nếu id không hợp lệ
    print(f"Error converting id to ObjectId: {e}")
    return None