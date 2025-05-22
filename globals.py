BASE_PATH = "./data/"
POKEMON_PATH = BASE_PATH + "pokedex.json"
MOVES_PATH = BASE_PATH + "moves.json"
LEARNSETS_PATH = BASE_PATH + "learnsets.json"

VERTEX_TYPES = [
    "Pokemon",
    "Movimiento",
    "Habilidad",
    "Categoria",
    "Generacion",
    "GrupoHuevo",
    "Color",
    "Tipo"
]

EDGE_TYPES = [
    "PerteneceGeneracion",
    "DeTipo",
    "PerteneceCategoria",
    "PoseeHabilidad",
    "AprendeMovimiento",
    "EvolucionaEn",
    "EsDeColor",
    "PerteneceGrupoHuevo"
]

GENERACIONES = [
    ("Gen 1", 1, 151, 1),
    ("Gen 2", 152, 251, 2),
    ("Gen 3", 252, 386, 3),
    ("Gen 4", 387, 493, 4),
    ("Gen 5", 494, 649, 5),
    ("Gen 6", 650, 721, 6),
    ("Gen 7", 722, 809, 7),
    ("Gen 8", 810, 905, 8),
    ("Gen 9", 906, 1025, 9),
    ("Unknown", 0, 0, 0)
]


def get_generacion_name(num: int) -> str:
    for gen, start, end in GENERACIONES:
        match num:
            case n if start <= n <= end:
                return gen
    return "Unknown"


def get_generacion_id(num: int):
    for gen, start, end, id in GENERACIONES:
        match num:
            case n if start <= n <= end:
                return id
    return 0


def get_gender_ratio(data):
    gender = data.get("gender")
    ratio = data.get("genderRatio")
    if gender is not None:
        m_ratio, f_ratio = data.get("genderRatio", {}).get("M", 0), data.get("genderRatio", {}).get("F", 0)
        if gender == "M":
            m_ratio = 1
            f_ratio = 0
        elif gender == "F":
            m_ratio = 0
            f_ratio = 1
        elif gender == "N":
            m_ratio = 0
            f_ratio = 0
    elif ratio is not None:
        m_ratio = ratio.get("M", 0)
        f_ratio = ratio.get("F", 0)
    else:
        m_ratio = 0.5
        f_ratio = 0.5
    return m_ratio, f_ratio
