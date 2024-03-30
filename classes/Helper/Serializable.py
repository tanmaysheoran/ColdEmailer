import json
from bson import ObjectId


class Serializable():

    def __init__(self, json: dict = None):
        self = json

    def to_dict(self, convert_object_id: bool = False):
        """
        Converts the object to a dictionary representation.

        Returns:
            dict: A dictionary representation of the object.
        """
        result_dict = {}
        for key, value in vars(self).items():
            if isinstance(value, list):
                result_dict[key] = [item.to_dict() if hasattr(
                    item, "to_dict") else item for item in value]
            elif hasattr(value, "to_dict"):
                result_dict[key] = value.to_dict()
            elif convert_object_id and isinstance(value, ObjectId):
                result_dict[key] = str(value)
            else:
                result_dict[key] = value
        return result_dict

    def to_json(self):
        """
        Converts the object to a JSON string.

        Returns:
            str: A JSON string representation of the object.
        """
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super().default(obj)


class JSONEncoder(json.JSONDecoder):
    def default(self, obj):
        if ObjectId.is_valid(obj):
            return ObjectId(obj)
        return super().default(obj)
