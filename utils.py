import re

def clean_string(s):
    return re.sub(r"[^a-zA-Z0-9\- ]", "", s)

def normalize_string(s):
    # Solo mantiene letras y números, convertir a minúsculas y eliminar espacios
    return re.sub(r"[^a-zA-Z0-9]", "", s).lower()
    
def clean_json(obj):
    if isinstance(obj, dict):
        return {k: clean_json(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [clean_json(elem) for elem in obj]
    elif isinstance(obj, str):
        return clean_string(obj)
    else:
        return obj