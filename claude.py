import json
from typing import List, Dict, Any, Optional, Tuple

class PokemonPathProcessor:
    def __init__(self, json_data: Dict[str, Any]):
        """
        Inicializa el procesador con los datos JSON de ArcadeDB
        
        Args:
            json_data: Diccionario con la respuesta JSON de ArcadeDB
        """
        self.json_data = json_data
        self.vertices = {vertex['r']: vertex['p'] for vertex in json_data['result']['vertices']}
        self.edges = json_data['result']['edges']
        
    def get_shortest_path(self) -> List[str]:
        records = self.json_data['result']['records']
        if not records:
            return []
            
        # El primer registro contiene la ruta del SHORTESTPATH
        path_key = list(records[0].keys())[0]
        return records[0][path_key]
    
    def get_path_details(self) -> List[Dict[str, Any]]:
        path_ids = self.get_shortest_path()
        path_details = []
        
        for node_id in path_ids:
            if node_id in self.vertices:
                node_info = self.vertices[node_id].copy()
                node_info['@rid'] = node_id
                path_details.append(node_info)
                
        return path_details
    
    def get_path_summary(self) -> Dict[str, Any]:
        path_details = self.get_path_details()
        
        if not path_details:
            return {'error': 'No se encontró ruta'}
        
        # Separar Pokémon de Grupos de Huevo
        pokemon_nodes = [node for node in path_details if node.get('@type') == 'Pokemon']
        egg_group_nodes = [node for node in path_details if node.get('@type') == 'GrupoHuevo']
        
        return {
            'total_nodes': len(path_details),
            'pokemon_count': len(pokemon_nodes),
            'egg_groups_count': len(egg_group_nodes),
            'origin': pokemon_nodes[0] if pokemon_nodes else None,
            'destination': pokemon_nodes[-1] if len(pokemon_nodes) > 1 else None,
            'connecting_egg_groups': [group['name'] for group in egg_group_nodes],
            'full_path': [self._format_node_name(node) for node in path_details]
        }
    
    def _format_node_name(self, node: Dict[str, Any]) -> str:
        if node.get('@type') == 'Pokemon':
            return f"{node['name']} (#{node['num']})"
        elif node.get('@type') == 'GrupoHuevo':
            return f"{node['name']} (Grupo Huevo)"
        else:
            return f"{node.get('name', 'Desconocido')}"
    
    def print_path(self) -> None:
        """Imprime la ruta de forma legible"""
        summary = self.get_path_summary()
        
        if 'error' in summary:
            print(f"{summary['error']}")
            return
        
        print("=" * 60)
        print("  RUTA MÁS CORTA ENTRE POKÉMON")
        print("=" * 60)
        
        print(f" Resumen:")
        print(f"   • Total de nodos: {summary['total_nodes']}")
        print(f"   • Pokémon en la ruta: {summary['pokemon_count']}")
        print(f"   • Grupos de huevo: {summary['egg_groups_count']}")
        
        if summary['origin'] and summary['destination']:
            print(f"\n🎯 Origen: {summary['origin']['name']} (#{summary['origin']['num']})")
            print(f"🏁 Destino: {summary['destination']['name']} (#{summary['destination']['num']})")
        
        if summary['connecting_egg_groups']:
            print(f"\n🥚 Grupos de huevo conectores: {', '.join(summary['connecting_egg_groups'])}")
        
        print(f"\n  Ruta completa:")
        for i, node_name in enumerate(summary['full_path']):
            connector = " → " if i < len(summary['full_path']) - 1 else ""
            print(f"   {i+1:2d}. {node_name}{connector}")
        
        print("=" * 60)

def process_pokemon_path(json_string: str) -> PokemonPathProcessor:
    """
    Función helper para procesar directamente un string JSON
    
    Args:
        json_string: String con el JSON de respuesta de ArcadeDB
        
    Returns:
        Instancia de PokemonPathProcessor
    """
    try:
        json_data = json.loads(json_string)
        return PokemonPathProcessor(json_data)
    except json.JSONDecodeError as e:
        raise ValueError(f"Error al parsear JSON: {e}")

# Ejemplo de uso
if __name__ == "__main__":
    # JSON de ejemplo (el que proporcionaste)
    json_example = '''{
  "user": "root",
  "version": "25.3.2 (build 5995e2d561169414958d65552371bf5ec149ebcd/1742848840057/main)",
  "serverName": "ArcadeDB_0",
  "result": {
    "vertices": [
      {
        "p": {
          "male_ratio": 0.875,
          "female_ratio": 0.125,
          "num": 1,
          "name": "Bulbasaur",
          "id": "bulbasaur",
          "weightkg": 6.9,
          "heightm": 0.7,
          "@cat": "v",
          "@type": "Pokemon",
          "@rid": "#1:0"
        },
        "r": "#1:0",
        "t": "Pokemon",
        "i": 0,
        "o": 75
      },
      {
        "p": {
          "name": "Grass",
          "@cat": "v",
          "@type": "GrupoHuevo",
          "@rid": "#16:6"
        },
        "r": "#16:6",
        "t": "GrupoHuevo",
        "i": 97,
        "o": 0
      },
      {
        "p": {
          "male_ratio": 0.875,
          "female_ratio": 0.125,
          "num": 908,
          "name": "Meowscarada",
          "id": "meowscarada",
          "weightkg": 31.2,
          "heightm": 1.5,
          "@cat": "v",
          "@type": "Pokemon",
          "@rid": "#1:2603"
        },
        "r": "#1:2603",
        "t": "Pokemon",
        "i": 1,
        "o": 81
      },
      {
        "p": {
          "name": "Field",
          "@cat": "v",
          "@type": "GrupoHuevo",
          "@rid": "#16:2"
        },
        "r": "#16:2",
        "t": "GrupoHuevo",
        "i": 343,
        "o": 0
      },
      {
        "p": {
          "male_ratio": 0.875,
          "female_ratio": 0.125,
          "num": 133,
          "name": "Eevee",
          "id": "eevee",
          "weightkg": 6.5,
          "heightm": 0.3,
          "@cat": "v",
          "@type": "Pokemon",
          "@rid": "#1:204"
        },
        "r": "#1:204",
        "t": "Pokemon",
        "i": 0,
        "o": 72
      }
    ],
    "edges": [
      {
        "p": {
          "@cat": "e",
          "@type": "PerteneceGrupoHuevo",
          "@rid": "#32:1505",
          "@in": "#16:6",
          "@out": "#1:2603"
        },
        "r": "#32:1505",
        "t": "PerteneceGrupoHuevo",
        "i": "#16:6",
        "o": "#1:2603"
      },
      {
        "p": {
          "@cat": "e",
          "@type": "PerteneceGrupoHuevo",
          "@rid": "#32:1504",
          "@in": "#16:2",
          "@out": "#1:2603"
        },
        "r": "#32:1504",
        "t": "PerteneceGrupoHuevo",
        "i": "#16:2",
        "o": "#1:2603"
      },
      {
        "p": {
          "@cat": "e",
          "@type": "PerteneceGrupoHuevo",
          "@rid": "#32:252",
          "@in": "#16:2",
          "@out": "#1:204"
        },
        "r": "#32:252",
        "t": "PerteneceGrupoHuevo",
        "i": "#16:2",
        "o": "#1:204"
      },
      {
        "p": {
          "@cat": "e",
          "@type": "PerteneceGrupoHuevo",
          "@rid": "#32:1",
          "@in": "#16:6",
          "@out": "#1:0"
        },
        "r": "#32:1",
        "t": "PerteneceGrupoHuevo",
        "i": "#16:6",
        "o": "#1:0"
      }
    ],
    "records": [
      {
        "SHORTESTPATH((_$$$SUBQUERY$$$_0), (_$$$SUBQUERY$$$_1), 'BOTH', ['PerteneceGrupoHuevo'])": [
          "#1:0",
          "#16:6",
          "#1:2603",
          "#16:2",
          "#1:204"
        ]
      }
    ]
  }
}'''
    
    # Procesar el JSON
    processor = process_pokemon_path(json_example)
    
    # Mostrar resultados
    processor.print_path()
    
    print("\n" + "="*60)
    print("📋 MÉTODOS DISPONIBLES:")
    print("="*60)
    
    # Mostrar diferentes formas de obtener los datos
    print("\n1️⃣ Ruta simple (IDs):")
    path = processor.get_shortest_path()
    print(f"   {' → '.join(path)}")
    
    print("\n2️⃣ Detalles completos:")
    details = processor.get_path_details()
    for i, node in enumerate(details):
        print(f"   {i+1}. {node.get('name', 'Sin nombre')} (Tipo: {node.get('@type')})")
    
    print("\n3️⃣ Resumen estructurado:")
    summary = processor.get_path_summary()
    print(f"   Nodos totales: {summary['total_nodes']}")
    print(f"   Pokémon conectados: {summary['pokemon_count']}")
    print(f"   Grupos conectores: {summary['connecting_egg_groups']}")