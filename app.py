from flask import Flask, render_template, Response
from flask import request

from arcadedb import *
from controller import *

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/pokemons/<id>', methods=['GET'])
def pokeinfo_id(id):
    return render_pokemon_por_id(id)


@app.route('/pokemons', methods=['GET'])
def pokeinfo_name():
    return render_pokemon_por_nombre(request)


@app.route('/moves', methods=['GET'])
def moves():
    return render_pokemon_por_movimiento(request)


@app.route('/shortest_path', methods=['GET'])
def shortest_path():
    return render_shortest_path_form()


@app.route('/shortest_path', methods=['POST'])
def shortest_path_data():
    return render_shortest_path_data(request)


@app.route('/cadena', methods=['GET'])
def cadena_form():
    return render_cadena_form()


@app.route('/cadena', methods=['POST'])
def cadena_data():
    return render_cadena_data(request)


@app.route("/generaciones", methods=["GET"])
def generaciones():
    return render_generaciones()


@app.route("/generaciones", methods=["POST"])
def pokemon_generaciones():
    return render_pokemon_de_generacion(request)


@app.route("/tipos", methods=["GET"])
def tipos():
    return render_tipos()


@app.route("/tipos", methods=["POST"])
def pokemon_tipos():
    return render_pokemon_de_tipo(request)


@app.route("/habilidades", methods=["GET"])
def habilidades():
    return render_habilidades()


@app.route("/habilidades", methods=["POST"])
def pokemon_habilidades():
    return render_pokemon_de_habilidad(request)


@app.route("/grupos", methods=["GET"])
def grupos_huevo():
    return render_grupos_huevo()


@app.route("/grupos", methods=["POST"])
def pokemon_grupos_huevo():
    return render_pokemon_de_grupo_huevo(request)


@app.route("/colores", methods=["GET"])
def colores():
    return render_colores()


@app.route("/colores", methods=["POST"])
def pokemon_colores():
    return render_pokemon_de_color(request)


@app.route("/categorias", methods=["GET"])
def categorias():
    return render_categorias()


@app.route("/categorias", methods=["POST"])
def pokemon_categorias():
    return render_pokemon_de_categoria(request)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080)
