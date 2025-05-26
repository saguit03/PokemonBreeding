from flask import Flask, render_template, request, Response

from arcade_relations import *
from arcadedb import *


def render_generaciones():
    generaciones = get_all_generaciones()
    return render_template("pokefiltro.html", filtro="Generación", opciones=generaciones, selected_filter=None,
                           pokemons=[])


def render_pokemon_de_generacion(request):
    generaciones = get_all_generaciones()
    selected_filter = request.form.get("filtro")
    query = f"""
        SELECT expand(in('PerteneceGeneracion')) FROM Generacion WHERE name = '{selected_filter}'
        ORDER BY num
    """
    pokemons = get_pokemons_data(query)
    return render_template("pokefiltro.html", filtro="Generación", opciones=generaciones,
                           selected_filter=selected_filter,
                           pokemons=pokemons)


def render_tipos():
    tipos = get_all_tipos()
    return render_template("pokefiltro.html", filtro="Tipo", opciones=tipos, selected_filter=None, pokemons=[])


def render_pokemon_de_tipo(request):
    tipos = get_all_tipos()
    selected_filter = request.form.get("filtro")
    query = f"""
        SELECT expand(in('DeTipo')) FROM Tipo WHERE name = '{selected_filter}'
        ORDER BY num
    """
    pokemons = get_pokemons_data(query)
    return render_template("pokefiltro.html", filtro="Tipo", opciones=tipos, selected_filter=selected_filter,
                           pokemons=pokemons)


def render_habilidades():
    habilidades = get_all_habilidades()
    return render_template("pokefiltro.html", filtro="Habilidad", opciones=habilidades, selected_filter=None,
                           pokemons=[])


def render_pokemon_de_habilidad(request):
    habilidades = get_all_habilidades()
    selected_filter = request.form.get("filtro")
    query = f"""
        SELECT expand(in('PoseeHabilidad')) FROM Habilidad WHERE name = '{selected_filter}'
        ORDER BY num
    """
    pokemons = get_pokemons_data(query)
    return render_template("pokefiltro.html", filtro="Habilidad", opciones=habilidades, selected_filter=selected_filter,
                           pokemons=pokemons)


def render_grupos_huevo():
    grupos_huevo = get_all_grupos_huevo()
    return render_template("pokefiltro.html", filtro="Grupo Huevo", opciones=grupos_huevo, selected_filter=None,
                           pokemons=[])


def render_pokemon_de_grupo_huevo(request):
    grupos_huevo = get_all_grupos_huevo()
    selected_filter = request.form.get("filtro")
    query = f"""
        SELECT expand(in('PerteneceGrupoHuevo')) FROM GrupoHuevo WHERE name = '{selected_filter}'
        ORDER BY num
    """
    pokemons = get_pokemons_data(query)
    return render_template("pokefiltro.html", filtro="Grupo Huevo", opciones=grupos_huevo,
                           selected_filter=selected_filter, pokemons=pokemons)


def render_colores():
    colores = get_all_colores()
    return render_template("pokefiltro.html", filtro="Color", opciones=colores, selected_filter=None, pokemons=[])


def render_pokemon_de_color(request):
    colores = get_all_colores()
    selected_filter = request.form.get("filtro")
    query = f"""
        SELECT expand(in('EsDeColor')) FROM Color WHERE name = '{selected_filter}'
        ORDER BY num
    """
    pokemons = get_pokemons_data(query)
    return render_template("pokefiltro.html", filtro="Color", opciones=colores, selected_filter=selected_filter,
                           pokemons=pokemons)


def render_categorias():
    categorias = get_all_categorias()
    return render_template("pokefiltro.html", filtro="Categoría", opciones=categorias, selected_filter=None,
                           pokemons=[])


def render_pokemon_de_categoria(request):
    categorias = get_all_categorias()
    selected_filter = request.form.get("filtro")
    query = f"""
        SELECT expand(in('PerteneceCategoria')) FROM Categoria WHERE name = '{selected_filter}'
        ORDER BY num
    """
    pokemons = get_pokemons_data(query)
    return render_template("pokefiltro.html", filtro="Categoría", opciones=categorias, selected_filter=selected_filter,
                           pokemons=pokemons)


def render_pokemon_por_nombre(request):
    pokename = request.args.get('pokename').strip()
    if not pokename:
        return Response("Nombre de Pokémon no proporcionado", status=400)
    pokemons = get_pokemon_by_name(pokename)
    return render_template('pokeresult.html', filtro="de nombre", pokemons=pokemons, selected_filter=pokename)


def render_pokemon_por_movimiento(request):
    movename = request.args.get('movename')
    if not movename:
        return Response("Movimiento Pokémon no proporcionado", status=400)
    pokemons = get_pokemon_that_learn_movement(movename)
    return render_template('pokeresult.html', filtro="que aprenden el movimiento", pokemons=pokemons,
                           selected_filter=movename)


def render_pokemon_por_id(id):
    pokemon = get_pokemon_by_id(id)
    if not pokemon:
        return Response("Pokémon no encontrado", status=404)
    relaciones = get_pokemon_relations(id)
    movimientos = get_pokemon_movements(id)
    return render_template('pokeinfo.html', pokemon=pokemon, relaciones=relaciones, movimientos=movimientos)


def render_shortest_path_form():
    pokemons = get_all_pokemons()
    return render_template('shortest_path.html', pokemons=pokemons)


def render_shortest_path_data(request):
    origen = request.form.get('source_id')
    destino = request.form.get('target_id')
    path_data = get_shortest_egg_path(origen, destino)
    return render_template('shortest_path.html', path_data=path_data, origen=origen, destino=destino)


def render_cadena_form():
    pokemons = get_all_pokemons()
    movements = get_all_movements()
    return render_template('cadena_cria.html', pokemons=pokemons, movements=movements)


def render_cadena_data(request):
    origen = request.form.get('source_id')
    destino = request.form.get('target_id')
    pokemons = get_all_pokemons()
    movements = get_all_movements()
    posibles_padres = cadena_cria(poke_id=origen, move_id=destino)
    return render_template('cadena_cria.html',  pokemons=pokemons, movements=movements, posibles_padres=posibles_padres, origen=origen, destino=destino)
