from globals import *
import json
import requests

MOSTRAR_EJECUCION = False

def execute_sql(command: str):
    payload = {
        "language": "sql",
        "command": command
        }
    
    if (MOSTRAR_EJECUCION): print(f"Ejecutando: {command}")

    response = requests.post(
        f"{ARCADEDB_URL}/api/v1/command/{DB_NAME}",
        headers=HEADERS,
        auth=AUTH,
        data=json.dumps(payload)
        )
    if not response.ok:
        print("Error:", response.status_code, response.text)
        response.raise_for_status()
    return response.json()

def create_node_if_not_exists(class_name: str, key: str, value: str):
    """Crea un nodo si no existe ya uno con el mismo valor en la propiedad dada"""
    check_cmd = f"SELECT COUNT(*) FROM {class_name} WHERE {key} = '{value}'"
    result = execute_sql(check_cmd)
    
    if (MOSTRAR_EJECUCION): print("Resultado:", result)

    if result['result'][0]['COUNT(*)'] == 0:
        insert_cmd = f"CREATE VERTEX {class_name} SET {key} = '{value}'"
        execute_sql(insert_cmd)