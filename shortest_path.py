# Endpoint y controladores para Flask
from flask import request, render_template, Response
import json
from arcadedb import execute_sql

class PokemonPathProcessor:
    def __init__(self, json_data):
        """Inicializa el procesador con los datos JSON de ArcadeDB"""
        self.json_data = json_data
        self.vertices = {vertex['r']: vertex['p'] for vertex in json_data['result']['vertices']}
        self.edges = json_data['result']['edges']
        
    def get_shortest_path(self):
        """Extrae la ruta más corta de los registros"""
        records = self.json_data['result']['records']
        if not records:
            return []
            
        path_key = list(records[0].keys())[0]
        return records[0][path_key]
    
    def get_path_details(self):
        """Obtiene los detalles completos de cada nodo en la ruta"""
        path_ids = self.get_shortest_path()
        path_details = []
        
        for node_id in path_ids:
            if node_id in self.vertices:
                node_info = self.vertices[node_id].copy()
                node_info['@rid'] = node_id
                path_details.append(node_info)
                
        return path_details
    
    def get_path_summary(self):
        """Obtiene un resumen de la ruta con información útil"""
        path_details = self.get_path_details()
        
        if not path_details:
            return {'error': 'No se encontró ruta'}
        
        pokemon_nodes = [node for node in path_details if node.get('@type') == 'Pokemon']
        egg_group_nodes = [node for node in path_details if node.get('@type') == 'GrupoHuevo']
        
        return {
            'total_nodes': len(path_details),
            'pokemon_count': len(pokemon_nodes),
            'egg_groups_count': len(egg_group_nodes),
            'origin': pokemon_nodes[0] if pokemon_nodes else None,
            'destination': pokemon_nodes[-1] if len(pokemon_nodes) > 1 else None,
            'connecting_egg_groups': [group['name'] for group in egg_group_nodes],
            'full_path': path_details,
            'path_ids': self.get_shortest_path()
        }

def render_shortest_path(request):
    """Controlador para procesar la ruta más corta"""
    origin_id = request.args.get('origin', '').strip()
    destination_id = request.args.get('destination', '').strip()
    
    if not origin_id or not destination_id:
        return Response("IDs de Pokémon origen y destino son requeridos", status=400)
    
    if origin_id == destination_id:
        return Response("El Pokémon origen y destino no pueden ser el mismo", status=400)
    
    try:
        # Obtener datos de la ruta
        shortest_path_data = get_shortest_path_between_pokemon(origin_id, destination_id)
        
        if not shortest_path_data:
            return render_template('resultados_ruta.html', 
                                 error="No se encontró una ruta entre los Pokémon especificados",
                                 origin_id=origin_id, 
                                 destination_id=destination_id)
        
        # Procesar los datos
        processor = PokemonPathProcessor(shortest_path_data)
        path_summary = processor.get_path_summary()
        
        if 'error' in path_summary:
            return render_template('resultados_ruta.html', 
                                 error=path_summary['error'],
                                 origin_id=origin_id, 
                                 destination_id=destination_id)
        
        return render_template('resultados_ruta.html', 
                             path_summary=path_summary,
                             origin_id=origin_id, 
                             destination_id=destination_id)
        
    except Exception as e:
        return render_template('resultados_ruta.html', 
                             error=f"Error al procesar la consulta: {str(e)}",
                             origin_id=origin_id, 
                             destination_id=destination_id)

def get_shortest_path_between_pokemon(origin_id, destination_id):
    """Ejecuta la consulta SHORTESTPATH en ArcadeDB"""
    query = f"""
        SELECT SHORTESTPATH(
            (SELECT FROM Pokemon WHERE id = '{origin_id}'),
            (SELECT FROM Pokemon WHERE id = '{destination_id}'),
            'BOTH', ['PerteneceGrupoHuevo']
        )
    """
    
    try:
        response = execute_sql(query)
        return response
    except Exception as e:
        print(f"Error ejecutando shortest path query: {e}")
        return None

def get_pokemon_basic_info(pokemon_id):
    """Obtiene información básica de un Pokémon por ID"""
    query = f"SELECT FROM Pokemon WHERE id = '{pokemon_id}'"
    response = execute_sql(query)
    result = response.get("result", [])
    return result[0] if result else None