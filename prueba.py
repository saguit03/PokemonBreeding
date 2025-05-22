from database import (
    get_all_generaciones, get_all_tipos, get_all_habilidades,
    get_all_grupos_huevo, get_all_colores, get_all_categorias,
    get_pokemons_data
)
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


# --- GENERACION ---
@app.route("/generaciones", methods=["GET"])
def generaciones():
    return render_filtro_form("Generación", get_all_generaciones(), None, [])


@app.route("/generaciones", methods=["POST"])
def pokemon_generaciones():
    selected = request.form.get("filtro")
    query = f"""
        SELECT FROM Pokemon 
        WHERE out('PerteneceGeneracion').name = '{selected}'
    """
    pokemons = get_pokemons_data(query)
    return render_filtro_form("Generación", get_all_generaciones(), selected, pokemons)


# --- TIPO ---
@app.route("/tipos", methods=["GET"])
def tipos():
    return render_filtro_form("Tipo", get_all_tipos(), None, [])


@app.route("/tipos", methods=["POST"])
def pokemon_tipos():
    selected = request.form.get("filtro")
    query = f"""
        SELECT FROM Pokemon 
        WHERE out('DeTipo').name = '{selected}'
    """
    pokemons = get_pokemons_data(query)
    return render_filtro_form("Tipo", get_all_tipos(), selected, pokemons)


# --- HABILIDAD ---
@app.route("/habilidades", methods=["GET"])
def habilidades():
    return render_filtro_form("Habilidad", get_all_habilidades(), None, [])


@app.route("/habilidades", methods=["POST"])
def pokemon_habilidades():
    selected = request.form.get("filtro")
    query = f"""
        SELECT FROM Pokemon 
        WHERE out('PoseeHabilidad').name = '{selected}'
    """
    pokemons = get_pokemons_data(query)
    return render_filtro_form("Habilidad", get_all_habilidades(), selected, pokemons)


# --- GRUPO HUEVO ---
@app.route("/grupos_huevo", methods=["GET"])
def grupos_huevo():
    return render_filtro_form("Grupo Huevo", get_all_grupos_huevo(), None, [])


@app.route("/grupos_huevo", methods=["POST"])
def pokemon_grupos_huevo():
    selected = request.form.get("filtro")
    query = f"""
        SELECT FROM Pokemon 
        WHERE out('PerteneceGrupoHuevo').name = '{selected}'
    """
    pokemons = get_pokemons_data(query)
    return render_filtro_form("Grupo Huevo", get_all_grupos_huevo(), selected, pokemons)


# --- COLOR ---
@app.route("/colores", methods=["GET"])
def colores():
    return render_filtro_form("Color", get_all_colores(), None, [])


@app.route("/colores", methods=["POST"])
def pokemon_colores():
    selected = request.form.get("filtro")
    query = f"""
        SELECT FROM Pokemon 
        WHERE out('EsDeColor').name = '{selected}'
    """
    pokemons = get_pokemons_data(query)
    return render_filtro_form("Color", get_all_colores(), selected, pokemons)


# --- CATEGORIA ---
@app.route("/categorias", methods=["GET"])
def categorias():
    return render_filtro_form("Categoría", get_all_categorias(), None, [])


@app.route("/categorias", methods=["POST"])
def pokemon_categorias():
    selected = request.form.get("filtro")
    query = f"""
        SELECT FROM Pokemon 
        WHERE out('PerteneceCategoria').name = '{selected}'
    """
    pokemons = get_pokemons_data(query)
    return render_filtro_form("Categoría", get_all_categorias(), selected, pokemons)


# --- FUNCION DE RENDER GENERAL ---
def render_filtro_form(filtro_label, filtro_valores, selected_valor, pokemons):
    return render_template(
        "filtro_pokemon.html",
        filtro_label=filtro_label,
        filtro_valores=filtro_valores,
        selected_valor=selected_valor,
        pokemons=pokemons
    )


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080)
