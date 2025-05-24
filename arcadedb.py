import json
import requests
import json
import requests
from shortest_path import *

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

def get_pokemon_relations(poke_id):
    relaciones = {
        "tipos": [],
        "habilidades": [],
        "grupo_huevo": [],
        "color": None,
        "generacion": None,
        "categoria": None,
        "evoluciona_en": [],
        "evoluciona_de": []
    }

    def get_names(resp):
        return [r["name"] for r in resp.get("result", [])]

    # Relaciones múltiples
    relaciones["tipos"] = get_names(execute_sql(f"""
            SELECT out('DeTipo').name as name FROM Pokemon WHERE id = '{poke_id}'
        """))
        
    relaciones["habilidades"] = get_names(execute_sql(f"""
            SELECT out('PoseeHabilidad').name as name FROM Pokemon WHERE id = '{poke_id}'
        """))

    relaciones["grupo_huevo"] = get_names(execute_sql(f"""
            SELECT out('PerteneceGrupoHuevo').name as name FROM Pokemon WHERE id = '{poke_id}'
        """))

    color_resp = execute_sql(f"""
            SELECT out('EsDeColor').name as name FROM Pokemon WHERE id = '{poke_id}'
        """)
    relaciones["color"] = color_resp["result"][0]["name"] if color_resp["result"] else None

    gen_resp = execute_sql(f"""
            SELECT out('PerteneceGeneracion').name as name FROM Pokemon WHERE id = '{poke_id}'
        """)
    relaciones["generacion"] = gen_resp["result"][0]["name"] if gen_resp["result"] else None

    cat_resp = execute_sql(f"""
            SELECT out('PerteneceCategoria').name as name FROM Pokemon WHERE id = '{poke_id}'
        """)
    relaciones["categoria"] = cat_resp["result"][0]["name"] if cat_resp["result"] else None

    evol_en_resp = execute_sql(f"""
            SELECT expand(out('EvolucionaEn')) FROM Pokemon WHERE id = '{poke_id}'
        """)
    relaciones["evoluciona_en"] = [{"id": p["id"], "name": p["name"]} for p in evol_en_resp.get("result", [])]

    evol_de_resp = execute_sql(f"""
            SELECT expand(in('EvolucionaEn')) FROM Pokemon WHERE id = '{poke_id}'
        """)
    relaciones["evoluciona_de"] = [{"id": p["id"], "name": p["name"]} for p in evol_de_resp.get("result", [])]

    return relaciones


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