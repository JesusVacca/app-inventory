def generate_unique_sku(fields=None):
    if fields is None:
        fields = {}
    parts = []
    for _, value in fields.items():
        value_str = str(value).strip().upper()
        try:
            int(value_str)
            parts.append(value_str.zfill(3))
        except ValueError:
            parts.append(value_str)

    sku = "-".join(parts)
    return sku
