# Instalación de ArcadeDB
Hay una guía en la página oficial de ArcadeDB para llevar a cabo su instalación con Docker, Kubernetes y en local. Debido a problemas técnicos, no hemos podido utilizar Docker ni Kubernetes, por lo que utilizaremos la versión local.   

## Descarga de ArcadeDB
Primero se debe descargar la versión deseada de ArcadeDB desde el siguiente enlace: [Releases · ArcadeData/arcadedb](https://github.com/ArcadeData/arcadedb/releases)  

Se decidió trabajar con la (última versión disponible, la 25.3.2)[https://github.com/ArcadeData/arcadedb/releases/tag/25.3.2]. Se descargó la versión completa, con todos los módulos (otras versiones excluyen gremlin, redisw, mongodbw, graphql y studio).  

Tras descargar el zip, se descomprimió y movió al directorio del usuario:  

```bash
C:\Users\estudiante\arcadedb-25.3.2
```

## Ejecución del servidor
El servidor se inicia con los ejecutables bin/server.sh o bin/server.bat en Windows. Aunque ArcadeDB se pueda ejecutar en Windows, hemos preferido utilizar WSL. Es necesario tener como mínimo Java 17, por lo que después se explicará cómo instalar Java 17 para evitar problemas con la JVM al ejecutar el servidor de ArcadeDB.  

Para acceder a este directorio desde WSL:  
```bash
cd /mnt/c/Users/estudiante/arcadedb-25.3.2/
cd bin
```
Y se inicializa el servidor:  
```bash
./server.sh
```

La primera vez que se inicie el servidor, solicitará una contraseña para el usuario root, que deberá tener al menos 8 caracteres.  

Si todo va bien, el servidor se iniciará sin complicaciones. La propia terminal indica la URL para acceder a ArcadeDB desde el navegador: http://172.24.134.105:2480/  
¡Y ya estaría listo para su uso!  

## Ejecución del cliente

Se deben ajustar las variables del fichero `arcadedb.py`:

```python
ARCADEDB_URL = "http://localhost:2480"
DB_NAME = "pokemondb"
AUTH = ("root", "123456789")
```

Para que se correspondan con la configuración del servidor.