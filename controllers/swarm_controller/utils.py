import json
import math

def clamp(value, minimum, maximum):
    return max(minimum, min(maximum, value))

def distance(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])

def serialize_message(message):
    try:
        return json.dumps(message).encode("utf-8")
    except Exception:
        return b"{}"

def deserialize_message(payload):
    try:
        return json.loads(payload)
    except Exception:
        return None
