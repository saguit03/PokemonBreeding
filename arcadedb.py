import json
import requests

from globals import *

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


def get_pokemons_data(query):
    response = execute_sql(query)
    pokemons = []
    result = response.get("result", [])
    for pokemon in result:
        p = {
            "id": pokemon["id"],
            "num": pokemon["num"],
            "name": pokemon["name"],
            "weightkg": pokemon["weightkg"],
            "heightm": pokemon["heightm"],
            "male_ratio": pokemon["male_ratio"],
            "female_ratio": pokemon["female_ratio"]
        }
        pokemons.append(p)
    return pokemons
