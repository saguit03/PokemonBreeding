from flask import Flask, render_template, request, Response

from arcadedb import *


def render_generaciones():
    generaciones = get_all_generaciones()
    return render_template("generaciones.html", generaciones=generaciones, selected_filter=None, pokemons=[])


def render_pokemon_de_generacion(request):
    generaciones = get_all_generaciones()
    selected_filter = request.form.get("generacion")
    query = f"""
        SELECT FROM Pokemon 
        WHERE out('PerteneceGeneracion').name = '{selected_filter}'
    """
    pokemons = get_pokemons_data(query)
    return render_template("generaciones.html", generaciones=generaciones, selected_filter=selected_filter,
                           pokemons=pokemons)


def render_tipos():
    tipos = get_all_tipos()
    return render_template("tipos.html", tipos=tipos, selected_filter=None, pokemons=[])


def render_pokemon_de_tipo(request):
    tipos = get_all_tipos()
    selected_filter = request.form.get("tipo")
    query = f"""
        SELECT FROM Pokemon 
        WHERE out('DeTipo').name = '{selected_filter}'
    """
    pokemons = get_pokemons_data(query)
    return render_template("tipos.html", tipos=tipos, selected_filter=selected_filter, pokemons=pokemons)


def render_habilidades():
    habilidades = get_all_habilidades()
    return render_template("habilidades.html", habilidades=habilidades, selected_filter=None, pokemons=[])


def render_pokemon_de_habilidad(request):
    habilidades = get_all_habilidades()
    selected_filter = request.form.get("habilidad")
    query = f"""
        SELECT FROM Pokemon 
        WHERE out('PoseeHabilidad').name = '{selected_filter}'
    """
    pokemons = get_pokemons_data(query)
    return render_template("habilidades.html", habilidades=habilidades, selected_filter=selected_filter,
                           pokemons=pokemons)


def render_grupos_huevo():
    grupos_huevo = get_all_grupos_huevo()
    return render_template("grupos_huevo.html", grupos=grupos_huevo, selected_filter=None, pokemons=[])


def render_pokemon_de_grupo_huevo(request):
    grupos_huevo = get_all_grupos_huevo()
    selected_filter = request.form.get("grupo_huevo")
    query = f"""
        SELECT FROM Pokemon 
        WHERE out('PerteneceGrupoHuevo').name = '{selected_filter}'
    """
    pokemons = get_pokemons_data(query)
    return render_template("grupos_huevo.html", grupos=grupos_huevo, selected_filter=selected_filter, pokemons=pokemons)


def render_colores():
    colores = get_all_colores()
    return render_template("colores.html", colores=colores, selected_filter=None, pokemons=[])


def render_pokemon_de_color(request):
    colores = get_all_colores()
    selected_filter = request.form.get("color")
    query = f"""
        SELECT FROM Pokemon 
        WHERE out('EsDeColor').name = '{selected_filter}'
    """
    pokemons = get_pokemons_data(query)
    return render_template("colores.html", colores=colores, selected_filter=selected_filter, pokemons=pokemons)


def render_categorias():
    categorias = get_all_categorias()
    return render_template("categorias.html", categorias=categorias, selected_filter=None, pokemons=[])


def render_pokemon_de_categoria(request):
    categorias = get_all_categorias()
    selected_filter = request.form.get("categoria")
    query = f"""
        SELECT FROM Pokemon 
        WHERE out('PerteneceCategoria').name = '{selected_filter}'
    """
    pokemons = get_pokemons_data(query)
    return render_template("categorias.html", categorias=categorias, selected_filter=selected_filter, pokemons=pokemons)
