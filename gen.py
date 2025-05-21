GENERACIONES = [
    ("Gen 1", 1, 151),
    ("Gen 2", 152, 251),
    ("Gen 3", 252, 386),
    ("Gen 4", 387, 493),
    ("Gen 5", 494, 649),
    ("Gen 6", 650, 721),
    ("Gen 7", 722, 809),
    ("Gen 8", 810, 905),
    ("Gen 9", 906, 1025),
    ("Unknown", 0, 0)
]

def obtener_generacion(num: int) -> str:
    # Usamos match para controlar distintos rangos con un loop sobre GENERACIONES
    for gen, start, end in GENERACIONES:
        match num:
            case n if start <= n <= end:
                return gen
    return "Unknown"