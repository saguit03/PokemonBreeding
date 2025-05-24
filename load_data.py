import json

from arcade_nodes import *
from arcade_relations import *
from globals import *
from utils import *

CARGAR_TODO = False
CARGAR_LEARNSETS = True

def cargar_todos_datos_pokemon():
    with open(POKEMON_PATH) as f:
        pokemon_data = clean_json(json.load(f))

    with open(MOVES_PATH) as f:
        moves_data = clean_json(json.load(f))

    pokemon_data = {k: v for k, v in pokemon_data.items() if v.get("num") > 0}

    create_types()
    create_other_nodes(pokemon_data)
    create_pokemon_nodes(pokemon_data)
    create_moves_nodes(moves_data)
    create_pokemon_relations(pokemon_data)

def cargar_learnsets():
    with open(LEARNSETS_PATH) as f:
        learnsets_data = clean_json(json.load(f))

    create_learnsets_relations(learnsets_data)


if CARGAR_TODO:
    cargar_todos_datos_pokemon()

if CARGAR_LEARNSETS:
    cargar_learnsets()