from fastapi import FastAPI, Request
from fastapi.middleware.base import BaseHTTPMiddleware
from bson import ObjectId
import json


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        elif isinstance(obj, str) and ObjectId.is_valid(obj):
            return ObjectId(obj)
        return super().default(obj)


def custom_decoder(dct):
    for key, value in dct.items():
        if isinstance(value, dict):
            dct[key] = custom_decoder(value)
        elif isinstance(value, list):
            dct[key] = [ObjectId(val) if isinstance(
                val, str) and ObjectId.is_valid(val) else val for val in value]
        elif isinstance(value, str) and ObjectId.is_valid(value):
            dct[key] = ObjectId(value)
    return dct


class CustomJSONMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Decoding the payload
        if "application/json" in request.headers.get("Content-Type", ""):
            try:
                request.body = json.loads(
                    request.body, object_hook=custom_decoder)
            except json.JSONDecodeError:
                pass  # Handle JSON decode error as per your requirement

        # Call the next middleware or route handler
        response = await call_next(request)

        # Encoding the response
        if "application/json" in response.headers.get("Content-Type", ""):
            response.body = json.dumps(response.body, cls=CustomEncoder)

        return response
