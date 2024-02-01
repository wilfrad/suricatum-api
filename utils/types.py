def get_enum_ref(_str, _enum):
    for ref in _enum:
        if _str == ref.value:
            return ref
    return None