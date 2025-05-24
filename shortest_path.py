from typing import List, Dict, Any

class ShortestPathProcessor:
    def __init__(self, json_data: Dict[str, Any]):
        self.json_data = json_data
        result = json_data.get('result', {})
        self.vertices = {}
        self.edges = []
        self.path_data = []
        if not result:
            return
        
        if 'vertices' in result and isinstance(result['vertices'], list):
            for vertex in result['vertices']:
                if 'r' in vertex and 'p' in vertex:
                    self.vertices[vertex['r']] = vertex['p']
        
        if 'edges' in result and isinstance(result['edges'], list):
            self.edges = result['edges']
        if 'records' in result and isinstance(result['records'], list):
            for record in result['records']:
                # Look for SHORTESTPATH key
                for key, value in record.items():
                    if 'SHORTESTPATH' in key and isinstance(value, list):
                        self.path_data = value
        
        if isinstance(result, list) and len(result) > 0:
            for record in result:
                if isinstance(record, dict):
                    for key, value in record.items():
                        if 'SHORTESTPATH' in key and isinstance(value, list):
                            self.path_data = value
                            break

    def get_shortest_path(self) -> List[str]:
        """Get the shortest path as a list of node IDs"""
        if not self.path_data:
            return self._reconstruct_path_from_graph()
        return self.path_data
    
    def _reconstruct_path_from_graph(self) -> List[str]:
        """Reconstruct path from vertices and edges when path_data is empty"""
        if not self.vertices or not self.edges:
            return []
        pokemon_vertices = []
        grupo_huevo_vertices = []
        for rid, vertex_data in self.vertices.items():
            if vertex_data.get('@type') == 'Pokemon':
                pokemon_vertices.append(rid)
            elif vertex_data.get('@type') == 'GrupoHuevo':
                grupo_huevo_vertices.append(rid)
        if len(pokemon_vertices) < 2:
            return []
        path = [pokemon_vertices[0]]  
        for grupo_rid in grupo_huevo_vertices:
            path.append(grupo_rid)
        if len(pokemon_vertices) > 1:
            path.append(pokemon_vertices[-1])
        return path
    