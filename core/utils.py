
def force_text(value, encoding='utf-8'):
    if not isinstance(value, str):
        return value.decode(encoding)
    return value


def force_bytes(value, encoding='utf-8'):
    if not isinstance(value, bytes):
        return value.encode(encoding, 'strict')
    return value
