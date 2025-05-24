import json
import requests
import json
import requests
from shortest_path import *
from tqdm import tqdm

ARCADEDB_URL = "http://localhost:2480"
DB_NAME = "pokemondb"
AUTH = ("root", "123456789")
HEADERS = {"Content-Type": "application/json"}

MOSTRAR_EJECUCION = False


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


def create_node_if_not_exists(class_name: str, key: str, value: str):
    """Crea un nodo si no existe ya uno con el mismo valor en la propiedad dada"""
    check_cmd = f"SELECT COUNT(*) FROM {class_name} WHERE {key} = '{value}'"
    result = execute_sql(check_cmd)

    if (MOSTRAR_EJECUCION): print("Resultado:", result)

    if result['result'][0]['COUNT(*)'] == 0:
        insert_cmd = f"CREATE VERTEX {class_name} SET {key} = '{value}'"
        execute_sql(insert_cmd)


def get_all_generaciones():
    response = execute_sql("SELECT name FROM Generacion ORDER BY name")

    generaciones = []
    result = response.get("result", [])
    for res in result:
        generaciones.append(res["name"])
    return generaciones


def get_all_tipos():
    response = execute_sql("SELECT name FROM Tipo ORDER BY name")

    tipos = []
    result = response.get("result", [])
    for res in result:
        tipos.append(res["name"])
    return tipos


def get_all_habilidades():
    response = execute_sql("SELECT name FROM Habilidad ORDER BY name")

    habilidades = []
    result = response.get("result", [])
    for res in result:
        habilidades.append(res["name"])
    return habilidades


def get_all_grupos_huevo():
    response = execute_sql("SELECT name FROM GrupoHuevo ORDER BY name")

    grupos_huevo = []
    result = response.get("result", [])
    for res in result:
        grupos_huevo.append(res["name"])
    return grupos_huevo


def get_all_colores():
    response = execute_sql("SELECT name FROM Color ORDER BY name")

    colores = []
    result = response.get("result", [])
    for res in result:
        colores.append(res["name"])
    return colores


def get_all_categorias():
    response = execute_sql("SELECT name FROM Categoria ORDER BY name")
    categorias = []
    result = response.get("result", [])
    for res in result:
        categorias.append(res["name"])
    return categorias

def get_all_pokemons():
    query = "SELECT id, name, num FROM Pokemon ORDER BY num"
    result = execute_sql(query).get("result", [])
    pokemons = []
    for res in result:
        pokemons.append({
            "id": res["id"],
            "num": res["num"],
            "name": res["name"]
        })
    return pokemons

def get_all_movements():
    query = "SELECT id, name, num FROM Movimiento ORDER BY num"
    result = execute_sql(query).get("result", [])
    pokemons = []
    for res in result:
        pokemons.append({
            "id": res["id"],
            "num": res["num"],
            "name": res["name"]
        })
    return pokemons

def get_pokemon_by_name(pokename):
    query = f"""
        SELECT FROM Pokemon WHERE name ILIKE '%{pokename}%'
        """
    response = execute_sql(query)
    result = response.get("result", [])
    pokemons = []
    for p in result:
        pokemons.append(get_pokemon_info(p))
    return pokemons    

def get_pokemon_by_id(poke_id):
    query = f"""
        SELECT FROM Pokemon WHERE id = '{poke_id}'
        """
    response = execute_sql(query)
    result = response.get("result", [])
    pokemons = []
    for p in result:
        pokemons.append(get_pokemon_info(p))
    return pokemons[0]

def get_pokemon_info(pokemon):
    return {
            "id": pokemon["id"],
            "num": pokemon["num"],
            "name": pokemon["name"],
            "weightkg": pokemon["weightkg"],
            "heightm": pokemon["heightm"],
            "male_ratio": pokemon["male_ratio"],
            "female_ratio": pokemon["female_ratio"]
        }

def get_pokemons_data(query):
    response = execute_sql(query)
    pokemons = []
    result = response.get("result", [])
    for p in result:
        pokemons.append(get_pokemon_info(p))
    return pokemons


def fetch_vertices_by_rid(rid_list):
    rid_str = ', '.join(rid_list)
    response = execute_sql(f"SELECT FROM [{rid_str}]")
    
    path = []
    for record in response.get("result", []):
        if record["@type"] == "Pokemon":
            if(MOSTRAR_EJECUCION): print(f"ID: {record['id']}, Name: {record['name']}, Num: {record['num']}")
            path.append({
            "id": record["id"],
            "num": record["num"],
            "name": record["name"],
            "weightkg": record["weightkg"],
            "heightm": record["heightm"],
            "male_ratio": record["male_ratio"],
            "female_ratio": record["female_ratio"],
            "node_type": record["@type"]
        })
        elif record["@type"] == "GrupoHuevo":
            if(MOSTRAR_EJECUCION): print(f"Grupo Huevo: {record['name']}")
            path.append({
                "name": record["name"],
                "node_type": record["@type"]
            })
    return path

def get_shortest_egg_path(id_1, id_2):
    response = execute_sql(f"""
        SELECT SHORTESTPATH(
            (SELECT FROM Pokemon WHERE id = '{id_1}'),
            (SELECT FROM Pokemon WHERE id = '{id_2}'),
            'BOTH', ['PerteneceGrupoHuevo']
        )
    """)
    processor = ShortestPathProcessor(response)
    path = fetch_vertices_by_rid(processor.get_shortest_path())
    print(len(path), "nodos en el camino más corto")
    return path


def get_pokemon_movements(poke_id):
    query = f"""
        SELECT FROM Movimiento 
        WHERE id IN (
        SELECT id FROM (
        SELECT expand(out('AprendeMovimiento')) FROM Pokemon WHERE id = '{poke_id}'
        ))
        """
    response = execute_sql(query)
    movimientos = []
    result = response.get("result", [])
    for move in result:
        movimientos.append({
            "id": move["id"],
            "name": move["name"],
            "num": move["num"],
            "type": move["type"],
            "description": move.get("description", ""),
            "basePower": move.get("basePower", None),
        })
    return movimientos


def get_pokemon_that_learn_movement(move_id):
    query = f"""
        SELECT expand(in('AprendeMovimiento')) FROM Movimiento WHERE id = '{move_id}'
    """
    response = execute_sql(query)
    pokemons = []
    result = response.get("result", [])
    for p in result:
        pokemons.append(get_pokemon_info(p))
    return pokemons

def cadena_cria(poke_id, move_id):
    posibles_padres = get_pokemon_that_learn_movement(move_id)
    if not posibles_padres:
        return []

    padres = []
    for pp in tqdm(posibles_padres, desc="Evaluando posibles padres"):
        path = get_shortest_egg_path(poke_id, pp["id"])
        if path:
            padres.append({
                "pokemon": get_pokemon_info(pp),
                "path": path
            })
    print(padres)
    return padres
        