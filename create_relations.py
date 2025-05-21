from tqdm import tqdm
from globals import *
from utils import *
from arcadedb import execute_sql

def create_pokemon_relations(pokemon_data):
    for poke_id, data in tqdm(pokemon_data.items(), desc="Creando relaciones hacia los Pokémon"):
        gen_id = get_generacion_id(num=data.get("num"))
        execute_sql(f"""
            CREATE EDGE PerteneceGeneracion FROM 
                (SELECT FROM Pokemon WHERE id = '{poke_id}') 
                TO 
                (SELECT FROM Generacion WHERE id = '{gen_id}')
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
                    (SELECT FROM Pokemon WHERE id = '{normalize_string(evo)}') 
            """)
            
def create_learnsets_relations(learnsets_data):
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
