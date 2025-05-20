import json
from pyarcadedb import Client

client = Client("http://localhost:2480", "pokemon", "root", "root")

pokemon_path = "data/pokemon.json"
moves_path = "data/moves.json"
learnset_path = "data/learnsets.json"

# --- Cargar y procesar datos de Pokémon ---
with open(pokemon_path) as f:
    data_pokemon = json.load(f)

tipos_creados = set()
habilidades_creadas = set()
categorias_creadas = set()
colores_creados = set()
grupos_creados = set()
generaciones_creadas = set()

for key, pokemon in data_pokemon.items():
    nombre = pokemon.get("name", key)
    num = pokemon.get("num", -1)
    tipos = pokemon.get("types", [])
    habilidades = list(pokemon.get("abilities", {}).values())
    color = pokemon.get("color", "")
    grupo_huevo = pokemon.get("eggGroups", [])
    gen = pokemon.get("gen", 1)
    categoria = pokemon.get("baseSpecies", nombre)

    # Insertar nodo Pokémon
    client.command(f"""
        INSERT INTO Pokemon SET
        id = {num},
        nombre = '{nombre}',
        categoria = '{categoria}',
        color = '{color}'
    """)

    # Relaciones con Tipo
    for tipo in tipos:
        if tipo not in tipos_creados:
            client.command(f"INSERT INTO Tipo SET nombre = '{tipo}'")
            tipos_creados.add(tipo)
        client.command(f"""
            CREATE EDGE DeTipo FROM 
            (SELECT FROM Pokemon WHERE nombre = '{nombre}')
            TO (SELECT FROM Tipo WHERE nombre = '{tipo}')
        """)

    # Relaciones con Habilidad
    for habilidad in habilidades:
        if habilidad not in habilidades_creadas:
            client.command(f"INSERT INTO Habilidad SET nombre = '{habilidad}'")
            habilidades_creadas.add(habilidad)
        client.command(f"""
            CREATE EDGE PoseeHabilidad FROM 
            (SELECT FROM Pokemon WHERE nombre = '{nombre}')
            TO (SELECT FROM Habilidad WHERE nombre = '{habilidad}')
        """)

    # Relación con Color
    if color and color not in colores_creados:
        client.command(f"INSERT INTO Color SET nombre = '{color}'")
        colores_creados.add(color)
    if color:
        client.command(f"""
            CREATE EDGE EsDeColor FROM 
            (SELECT FROM Pokemon WHERE nombre = '{nombre}')
            TO (SELECT FROM Color WHERE nombre = '{color}')
        """)

    # Relación con Grupo Huevo
    for grupo in grupo_huevo:
        if grupo not in grupos_creados:
            client.command(f"INSERT INTO GrupoHuevo SET nombre = '{grupo}'")
            grupos_creados.add(grupo)
        client.command(f"""
            CREATE EDGE PerteneceGrupoHuevo FROM 
            (SELECT FROM Pokemon WHERE nombre = '{nombre}')
            TO (SELECT FROM GrupoHuevo WHERE nombre = '{grupo}')
        """)

    # Relación con Generación
    if gen not in generaciones_creadas:
        client.command(f"INSERT INTO Generacion SET numero = {gen}")
        generaciones_creadas.add(gen)
    client.command(f"""
        CREATE EDGE PerteneceGeneracion FROM 
        (SELECT FROM Pokemon WHERE nombre = '{nombre}')
        TO (SELECT FROM Generacion WHERE numero = {gen})
    """)

    # Relación con Categoría
    if categoria not in categorias_creadas:
        client.command(f"INSERT INTO Categoria SET nombre = '{categoria}'")
        categorias_creadas.add(categoria)
    client.command(f"""
        CREATE EDGE PerteneceCategoria FROM 
        (SELECT FROM Pokemon WHERE nombre = '{nombre}')
        TO (SELECT FROM Categoria WHERE nombre = '{categoria}')
    """)

# --- Cargar y procesar datos de Movimientos ---
with open(moves_path) as f:
    data_movimientos = json.load(f)

tipos_movimiento_creados = set()
categorias_movimiento_creadas = set()

for key, mov in data_movimientos.items():
    nombre = mov["name"]
    tipo = mov["type"]
    categoria = mov["category"]

    num = mov.get("num", -1)
    precision = mov.get("accuracy", 'null')
    potencia = mov.get("basePower", 'null')
    prioridad = mov.get("priority", 0)
    pp = mov.get("pp", 'null')
    crit_ratio = mov.get("critRatio", 1)
    descripcion = mov.get("desc", "").replace("'", "\\'")
    short_desc = mov.get("shortDesc", "").replace("'", "\\'")
    z_move = mov.get("isZ", "null")
    secondary = mov.get("secondary", None)
    efecto_secundario = json.dumps(secondary).replace("'", "\\'") if secondary else "null"

    # Insertar nodo Movimiento
    client.command(f"""
        INSERT INTO Movimiento SET
        id = {num},
        nombre = '{nombre}',
        tipo = '{tipo}',
        categoria = '{categoria}',
        precision = {precision},
        potencia = {potencia},
        prioridad = {prioridad},
        pp = {pp},
        crit_ratio = {crit_ratio},
        descripcion = '{descripcion}',
        short_desc = '{short_desc}',
        esZ = '{z_move}',
        efecto_secundario = '{efecto_secundario}'
    """)

    # Relacionar con Tipo
    if tipo not in tipos_creados and tipo not in tipos_movimiento_creados:
        client.command(f"INSERT INTO Tipo SET nombre = '{tipo}'")
        tipos_movimiento_creados.add(tipo)
    client.command(f"""
        CREATE EDGE DeTipo FROM 
        (SELECT FROM Movimiento WHERE nombre = '{nombre}')
        TO (SELECT FROM Tipo WHERE nombre = '{tipo}')
    """)

    # Relacionar con Categoría
    if categoria not in categorias_creadas and categoria not in categorias_movimiento_creadas:
        client.command(f"INSERT INTO Categoria SET nombre = '{categoria}'")
        categorias_movimiento_creadas.add(categoria)
    client.command(f"""
        CREATE EDGE PerteneceCategoria FROM 
        (SELECT FROM Movimiento WHERE nombre = '{nombre}')
        TO (SELECT FROM Categoria WHERE nombre = '{categoria}')
    """)

# --- Relacionar Pokémon con Movimientos ---
with open(learnset_path) as f:
    data_aprendizaje = json.load(f)

for nombre_pokemon, datos in data_aprendizaje.items():
    learnset = datos.get("learnset", {})
    for nombre_movimiento in learnset.keys():
        client.command(f"""
            CREATE EDGE AprendeMovimiento FROM 
            (SELECT FROM Pokemon WHERE nombre = '{nombre_pokemon.capitalize()}')
            TO (SELECT FROM Movimiento WHERE nombre = '{nombre_movimiento.replace('-', ' ').title().replace(' ', '')}')
        """)
