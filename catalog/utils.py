import uuid


def generate_sku(name):
    name_prefix = name[:3].upper()
    unique_id = uuid.uuid4().hex[:6].upper()
    sku = f"{name_prefix}-{unique_id}"
    return sku
