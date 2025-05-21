import json
import requests
import re
from tqdm import tqdm
import os
from gen import GENERACIONES, obtener_generacion

ARCADEDB_URL = "http://localhost:2480"
DB_NAME = "pokemondb"
AUTH = ("root", "123456789")
HEADERS = {"Content-Type": "application/json"}

BASE_PATH = "./data/"
POKEMON_PATH = BASE_PATH + "pokedex.json"
MOVES_PATH = BASE_PATH + "moves.json"
LEARNSETS_PATH = BASE_PATH + "learnsets.json"

MOSTRAR_EJECUCION = False

import time

start_time = time.time()

def clean_string(s):
    # Conserva solo letras, números, guiones y espacios (si quieres espacios también)
    # Si NO quieres espacios, elimina el espacio de la expresión
    return re.sub(r"[^a-zA-Z0-9\- ]", "", s)

def clean_json(obj):
    if isinstance(obj, dict):
        return {k: clean_json(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [clean_json(elem) for elem in obj]
    elif isinstance(obj, str):
        return clean_string(obj)
    else:
        return obj

# Cargar y limpiar los datos
with open(POKEMON_PATH) as f:
    pokemon_data = clean_json(json.load(f))

with open(MOVES_PATH) as f:
    moves_data = clean_json(json.load(f))

with open(LEARNSETS_PATH) as f:
    learnsets_data = clean_json(json.load(f))

def execute_sql(command: str):
    payload = {
        "language": "sql",
        "command": command
    }
    if (MOSTRAR_EJECUCION): print(f"Ejecutando: {command}")
    response = requests.post(
        f"{ARCADEDB_URL}/api/v1/command/{DB_NAME}",
        headers=HEADERS,
        auth=AUTH,
        data=json.dumps(payload)
    )
    if not response.ok:
        print("Error:", response.status_code, response.text)
        response.raise_for_status()
    return response.json()

# Crear tipos de vértices si no existen
VERTEX_TYPES = [
    "Pokemon", "Movimiento", "Habilidad", "Categoria",
    "Generacion", "GrupoHuevo", "Color", "Tipo"
]

EDGE_TYPES = [
    "PerteneceGeneracion", "DeTipo", "PerteneceCategoria",
    "PoseeHabilidad", "AprendeMovimiento", "EvolucionaEn",
    "EsDeColor", "PerteneceGrupoHuevo"
]

for vt in tqdm(VERTEX_TYPES, desc="Creando tipos de nodos"):
    execute_sql(f"CREATE VERTEX TYPE {vt} IF NOT EXISTS")

for et in tqdm(EDGE_TYPES, desc="Creando tipos de enlaces"):
    execute_sql(f"CREATE EDGE TYPE {et} IF NOT EXISTS")

# Wait

def create_node_if_not_exists(class_name: str, key: str, value: str):
    """Crea un nodo si no existe ya uno con el mismo valor en la propiedad dada"""
    check_cmd = f"SELECT COUNT(*) FROM {class_name} WHERE {key} = '{value}'"
    result = execute_sql(check_cmd)
    if (MOSTRAR_EJECUCION): print("Resultado:", result)
    if result['result'][0]['COUNT(*)'] == 0:
        insert_cmd = f"CREATE VERTEX {class_name} SET {key} = '{value}'"
        execute_sql(insert_cmd)

# Primero recogemos todos los valores únicos
tipos_unicos = set()
habilidades_unicas = set()
grupos_huevo_unicos = set()
colores_unicos = set()
categorias_unicas = set()

for name, data in pokemon_data.items():
    tipos_unicos.update(data.get("types", []))

    habilidades_unicas.update(data.get("abilities", {}).values())

    grupos_huevo_unicos.update(data.get("eggGroups", []))

    color = data.get("color")
    if color:
        colores_unicos.add(color)

    tier = data.get("tier")
    if tier:
        categorias_unicas.add(tier)

for gen_name, start, end in tqdm(GENERACIONES, desc="Creando nodos de Generación"):
    props = {
        "name": gen_name,
        "start": start,
        "end": end
    }
    command = f"INSERT INTO Generacion CONTENT {json.dumps(props)}"
    execute_sql(command)

# Ahora creamos nodos uno a uno para cada conjunto único

print("Creando nodos de Tipo...")
for tipo in tqdm(tipos_unicos):
    create_node_if_not_exists("Tipo", "name", tipo)

print("Creando nodos de Habilidad...")
for habilidad in tqdm(habilidades_unicas):
    create_node_if_not_exists("Habilidad", "name", habilidad)

print("Creando nodos de GrupoHuevo...")
for grupo in tqdm(grupos_huevo_unicos):
    create_node_if_not_exists("GrupoHuevo", "name", grupo)

print("Creando nodos de Color...")
for color in tqdm(colores_unicos):
    create_node_if_not_exists("Color", "name", color)

print("Creando nodos de Categoria...")
for categoria in tqdm(categorias_unicas):
    create_node_if_not_exists("Categoria", "name", categoria)

# Crear nodos de Pokémon
for poke_id, data in  tqdm(pokemon_data.items(), desc="Creando nodos de Pokémon"):
    props = {
        "id": poke_id,
        "name": data.get("name"),
        "num": data.get("num"),
        "heightm": data.get("heightm"),
        "weightkg": data.get("weightkg"),
        "genderRatio": data.get("genderRatio"),
    }
    command = f"INSERT INTO Pokemon CONTENT {json.dumps(props)}"
    execute_sql(command)

# Crear nodos de movimientos
for move_id, data in  tqdm(moves_data.items(), desc="Creando nodos de movimientos"):
    props = {
        "id": move_id,
        "name": data.get("name"),
        "num": data.get("num"),
        "type": data.get("type"),
        "description": data.get("shortDesc"),
        # "accuracy": data.get("accuracy"),
        # "basePower": data.get("basePower"),
        # "pp": data.get("pp"),
        # "desc": data.get("desc"),
        # "secondary": data.get("secondary")
    }
    command = f"INSERT INTO Movimiento CONTENT {json.dumps(props)}"
    execute_sql(command)

# Wait

# Crear relaciones desde Pokémon
for poke_id, data in tqdm(pokemon_data.items(), desc="Creando relaciones hacia los Pokémon"):
    gen_name = obtener_generacion(num=data.get("num"))
    execute_sql(f"""
        CREATE EDGE PerteneceGeneracion FROM 
            (SELECT FROM Pokemon WHERE id = '{poke_id}') 
            TO 
            (SELECT FROM Generacion WHERE name = '{gen_name}')
    """)

    for tipo in data.get("types", []):
        execute_sql(f"""
            CREATE EDGE DeTipo FROM 
                (SELECT FROM Pokemon WHERE id = '{poke_id}') 
                TO 
                (SELECT FROM Tipo WHERE name = '{tipo}')
        """)

    for habilidad in data.get("abilities", {}).values():
        execute_sql(f"""
            CREATE EDGE PoseeHabilidad FROM 
                (SELECT FROM Pokemon WHERE id = '{poke_id}') 
                TO 
                (SELECT FROM Habilidad WHERE name = '{habilidad}')
        """)

    for grupo in data.get("eggGroups", []):
        execute_sql(f"""
            CREATE EDGE PerteneceGrupoHuevo FROM 
                (SELECT FROM Pokemon WHERE id = '{poke_id}') 
                TO 
                (SELECT FROM GrupoHuevo WHERE name = '{grupo}')
        """)

    color = data.get("color")
    if color:
        execute_sql(f"""
            CREATE EDGE EsDeColor FROM 
                (SELECT FROM Pokemon WHERE id = '{poke_id}') 
                TO 
                (SELECT FROM Color WHERE name = '{color}')
        """)

    tier = data.get("tier")
    if tier:
        execute_sql(f"""
            CREATE EDGE PerteneceCategoria FROM 
                (SELECT FROM Pokemon WHERE id = '{poke_id}') 
                TO 
                (SELECT FROM Categoria WHERE name = '{tier}')
        """)

    for evo in data.get("evos", []):
        execute_sql(f"""
            CREATE EDGE EvolucionaEn FROM 
                (SELECT FROM Pokemon WHERE id = '{poke_id}') 
                TO 
                (SELECT FROM Pokemon WHERE id = '{evo}') 
        """) # TODO procesar las evoluciones de forma más completa

# Crear relaciones AprendeMovimiento usando el nombre del Pokémon y del Movimiento
for poke_id, poke_info in tqdm(learnsets_data.items(), desc="Creando relaciones AprendeMovimiento para cada Pokémon"):
    learnsets = poke_info.get("learnset", {})
    for move_id in learnsets.keys():
        try:
            execute_sql(f"""
                CREATE EDGE AprendeMovimiento FROM 
                (SELECT FROM Pokemon WHERE id = '{poke_id}') TO 
                (SELECT FROM Movimiento WHERE id = '{move_id}')
            """)
        except Exception as e:
            print(f"No se pudo crear relación AprendeMovimiento para {poke_id} -> {move_id}: {e}")

end_time = time.time()
print(f"Tiempo transcurrido: {end_time - start_time:.2f} segundos")