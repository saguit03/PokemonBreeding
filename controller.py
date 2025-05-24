from flask import Flask, render_template, request, Response

from arcadedb import *


def render_generaciones():
    generaciones = get_all_generaciones()
    return render_template("pokefiltro.html", filtro="Generación",opciones=generaciones, selected_filter=None, pokemons=[])


def render_pokemon_de_generacion(request):
    generaciones = get_all_generaciones()
    selected_filter = request.form.get("filtro")
    query = f"""
        SELECT expand(in('PerteneceGeneracion')) FROM Generacion WHERE name = '{selected_filter}'
    """
    pokemons = get_pokemons_data(query)
    return render_template("pokefiltro.html", filtro="Generación",opciones=generaciones, selected_filter=selected_filter,
                           pokemons=pokemons)


def render_tipos():
    tipos = get_all_tipos()
    return render_template("pokefiltro.html", filtro="Tipo",opciones=tipos, selected_filter=None, pokemons=[])


def render_pokemon_de_tipo(request):
    tipos = get_all_tipos()
    selected_filter = request.form.get("filtro")
    query = f"""
        SELECT expand(in('DeTipo')) FROM Tipo WHERE name = '{selected_filter}'
    """
    pokemons = get_pokemons_data(query)
    return render_template("pokefiltro.html", filtro="Tipo",opciones=tipos, selected_filter=selected_filter, pokemons=pokemons)


def render_habilidades():
    habilidades = get_all_habilidades()
    return render_template("pokefiltro.html", filtro="Habilidad",opciones=habilidades, selected_filter=None, pokemons=[])


def render_pokemon_de_habilidad(request):
    habilidades = get_all_habilidades()
    selected_filter = request.form.get("filtro")
    query = f"""
        SELECT expand(in('PoseeHabilidad')) FROM Habilidad WHERE name = '{selected_filter}'
    """
    pokemons = get_pokemons_data(query)
    return render_template("pokefiltro.html", filtro="Habilidad",opciones=habilidades, selected_filter=selected_filter,
                           pokemons=pokemons)


def render_grupos_huevo():
    grupos_huevo = get_all_grupos_huevo()
    return render_template("pokefiltro.html", filtro="Grupo Huevo",opciones=grupos_huevo, selected_filter=None, pokemons=[])


def render_pokemon_de_grupo_huevo(request):
    grupos_huevo = get_all_grupos_huevo()
    selected_filter = request.form.get("filtro")
    query = f"""
        SELECT expand(in('PerteneceGrupoHuevo')) FROM GrupoHuevo WHERE name = '{selected_filter}'
    """
    pokemons = get_pokemons_data(query)
    return render_template("pokefiltro.html", filtro="Grupo Huevo",opciones=grupos_huevo, selected_filter=selected_filter, pokemons=pokemons)


def render_colores():
    colores = get_all_colores()
    return render_template("pokefiltro.html", filtro="Color",opciones=colores, selected_filter=None, pokemons=[])


def render_pokemon_de_color(request):
    colores = get_all_colores()
    selected_filter = request.form.get("filtro")
    query = f"""
        SELECT expand(in('EsDeColor')) FROM Color WHERE name = '{selected_filter}'
    """
    pokemons = get_pokemons_data(query)
    return render_template("pokefiltro.html", filtro="Color",opciones=colores, selected_filter=selected_filter, pokemons=pokemons)


def render_categorias():
    categorias = get_all_categorias()
    return render_template("pokefiltro.html", filtro="Categoría",opciones=categorias, selected_filter=None, pokemons=[])


def render_pokemon_de_categoria(request):
    categorias = get_all_categorias()
    selected_filter = request.form.get("filtro")
    query = f"""
        SELECT expand(in('PerteneceCategoria')) FROM Categoria WHERE name = '{selected_filter}'
    """
    pokemons = get_pokemons_data(query)
    return render_template("pokefiltro.html", filtro="Categoría",opciones=categorias, selected_filter=selected_filter, pokemons=pokemons)
