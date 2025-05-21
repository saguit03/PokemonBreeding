import json
from tqdm import tqdm
import time
from globals import *
from utils import *
from arcadedb import execute_sql, create_node_if_not_exists

def create_types():
    for vt in tqdm(VERTEX_TYPES, desc="Creando tipos de nodos"):
        execute_sql(f"CREATE VERTEX TYPE {vt} IF NOT EXISTS")

    for et in tqdm(EDGE_TYPES, desc="Creando tipos de enlaces"):
        execute_sql(f"CREATE EDGE TYPE {et} IF NOT EXISTS")

def create_other_nodes(pokemon_data):
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

    for gen_name, start, end, number in tqdm(GENERACIONES, desc="Creando nodos de Generación"):
        props = {
            "id": number,
            "name": gen_name,
            "start": start,
            "end": end,
        }
        command = f"INSERT INTO Generacion CONTENT {json.dumps(props)}"
        execute_sql(command)

    for tipo in tqdm(tipos_unicos, desc="Creando nodos de Tipo"):
        create_node_if_not_exists("Tipo", "name", tipo)

    for habilidad in tqdm(habilidades_unicas, desc="Creando nodos de Habilidad"):
        create_node_if_not_exists("Habilidad", "name", habilidad)

    for grupo in tqdm(grupos_huevo_unicos, desc="Creando nodos de Grupo Huevo"):
        create_node_if_not_exists("GrupoHuevo", "name", grupo)

    for color in tqdm(colores_unicos, desc="Creando nodos de Color"):
        create_node_if_not_exists("Color", "name", color)

    for categoria in tqdm(categorias_unicas, desc="Creando nodos de Categoria"):
        create_node_if_not_exists("Categoria", "name", categoria)

def create_pokemon_nodes(pokemon_data):
    for poke_id, data in  tqdm(pokemon_data.items(), desc="Creando nodos de Pokémon"):
        m_ratio, f_ratio = get_gender_ratio(data)
        props = {
            "id": poke_id,
            "name": data.get("name"),
            "num": data.get("num"),
            "heightm": data.get("heightm"),
            "weightkg": data.get("weightkg"),
            "male_ratio": m_ratio,
            "female_ratio": f_ratio
        }
        command = f"INSERT INTO Pokemon CONTENT {json.dumps(props)}"
        execute_sql(command)

def create_moves_nodes(moves_data):
    for move_id, data in  tqdm(moves_data.items(), desc="Creando nodos de movimientos"):
        props = {
            "id": move_id,
            "name": data.get("name"),
            "num": data.get("num"),
            "type": data.get("type"),
            "description": data.get("shortDesc"),
            "basePower": data.get("basePower"),
            # "accuracy": data.get("accuracy"),
            # "pp": data.get("pp"),
            # "desc": data.get("desc"),
            # "secondary": data.get("secondary")
        }
        command = f"INSERT INTO Movimiento CONTENT {json.dumps(props)}"
        execute_sql(command)