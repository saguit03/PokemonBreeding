# PokemonBreeding

Proyecto de Recuperación de la Información y Búsqueda en la Web  
Curso 2024-2025  
==================================================

Autores:

- Guillén Torrado, Sara
- Mocinha Sánchez, Daniel

## Herramientas

- Python 3.10.12
- ArcadeDB 25.3.2
- VSCode
- GitHub

## Objetivo principal

Dado un Pokémon A y un movimiento X, cómo podría aprenderlo a través de cadenas de crianza.

1. Obtenemos los Pokémon que pueden aprender el movimiento X.
2. Buscamos las cadenas de crianza entre el Pokémon A y los Pokémon que pueden aprender el movimiento X.
3. Mostramos las cadenas de crianza encontradas.

## Otras consultas

- Mostrar Pokémon por Generación
- Mostrar Pokémon por Tipo
- Mostrar Pokémon por Habilidad
- Mostrar Pokémon por Grupo Huevo
- Mostrar Pokémon por Colores
- Mostrar Pokémon por Categoría

## Ejecución

Para que la aplicación funcione correctamente, es necesario tener versiones compatibles con Python y ArcadeDB.

### Ejecución de ArcadeDB

Es imprescindible que ArcadeDB esté en ejecución. Para ello, se debe seguir la guía de instalación de ArcadeDB (dentro
de `./docs`) y ejecutar el servidor.

```
cd /mnt/c/Users/estudiante/arcadedb-25.3.2/bin
./server.sh
```

### Carga de datos

La primera vez que se utilice la aplicación, es necesario cargar los datos en la base de datos. Para ello, se debe
ejecutar el script `load_data.py`:

```bash
python3 load_data.py
```

Cuidado, porque tenemos variables para no tener que cargar los datos durante la realización de pruebas. Para su correcto
funcionamiento desde cero, se deben cambiar las siguientes variables a `True`:


```python
CARGAR_TODO = True
CARGAR_LEARNSETS = True
```

### Ejecución de la aplicación

Para ejecutar la aplicación, se debe ejecutar el script `app.py`:

```bash
python3 app.py
```

## Fuentes

### Documentación ArcadeDB

- [Documentación de ArcadeDB](https://docs.arcadedb.com)
- [Comandos ArcadeDB con SQL](https://docs.arcadedb.com/#sql)
- [Shortest Path](https://docs.arcadedb.com/#shortest-path-function)

### Datasets

- [Datos de Pokémon](https://play.pokemonshowdown.com/data/pokedex.json)
- [Datos de Movimientos](https://play.pokemonshowdown.com/data/moves.json)
- [Datos de Aprendizaje](https://play.pokemonshowdown.com/data/learnsets.json)