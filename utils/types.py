def get_enum_ref(_str, _enum):
    for ref in _enum:
        if _str == ref.value:
            return ref
    return None

def clean_text(text):
    while text and not text[0].isalnum():
        text = text[1:]
    
    text = text.replace("\n", "")
    
    text = ''.join(char for char in text if char.isalpha() or char.isdigit())
    
    text = text.strip()
    
    return text