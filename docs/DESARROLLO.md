# Desarrollo de la aplicación

## Carga de datos
- Fuente: tres ficheros JSON
1. Lectura de ficheros JSON
2. Peticiones a la API (protocolo HTTP/JSON) de ArcadeDB para cargar los datos:
   1. Crear los tipos de nodos y vértices
   2. Crear los nodos
   3. Crear los enlaces 

### Consideraciones

- Se ha hecho una limpieza manual de los datos para eliminar algunos Pokémon no oficiales en learnsets.
- Antes de crear los nodos y enlaces, se filtran los datos para eliminar Pokémon no oficiales.
- Debido a la gran cantidad de datos, se debe estudiar la posibilidad de realizar la carga de datos en paralelo.

## Creación de la aplicación web

### Estructura de la aplicación
Se utiliza Flask para crear una aplicación web que permita interactuar con la base de datos.
Se divide el código en distintos archivos para facilitar su mantenimiento:
- `app.py`: script principal de la aplicación y que contiene los *endpoints*.
- `globals.py`: contiene las variables globales y la configuración de la aplicación.
- `controller.py`: implementa la lógica de cada *endpoint*.
- `arcadedb.py`: funciones para interactuar con la API de ArcadeDB.
- `utils.py`: funciones auxiliares.
- `templates/`: directorio que contiene las plantillas HTML.
- `static/`: directorio que contiene los archivos estáticos (HTML, CSS...).
- `data/`: directorio que contiene los ficheros JSON.
- `docs/`: directorio que contiene la documentación.
- `create_nodes.py`: script para crear los nodos y enlaces a partir de los ficheros JSON.
- `create_relations.py`: script para crear las relaciones entre los nodos a partir de los ficheros JSON.
- `load_data.py`: script para cargar los datos en la base de datos.	
- `requirements.txt`: fichero que contiene las dependencias de la aplicación.

### Funcionalidades
- Se implementan las siguientes funcionalidades:
  - Carga de datos desde los ficheros JSON. (POR HACER)
  - Consultas a la base de datos a través de la API de ArcadeDB.
  - Visualización de los resultados en la aplicación web.

## Pruebas sobre la API

Consultas sobre la API de ArcadeDB a través de la aplicación web en Flask.

1. Se cargan los datos como se indica en la sección anterior.
2. Se implementan las consultas de `docs/CONSULTAS.md` en la aplicación web.
3. Se visualizan los resultados en la aplicación web.

