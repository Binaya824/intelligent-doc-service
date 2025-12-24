# app/core/responses.py
from typing import T

def success(data: T = None, message: str = "success"):
    return {
        "success": True,
        "message": message,
        "data": data,
    }
