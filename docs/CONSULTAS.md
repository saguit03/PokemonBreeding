# Consultas sobre ArcadeDB
## Consultas simples
### Obtener Pokémon de una generación
```sql
SELECT FROM Pokemon WHERE out('PerteneceGeneracion').name = 'Gen 1'
```
### Obtener Pokémon por tipo
```sql
SELECT FROM Pokemon WHERE out('DeTipo').name = 'Grass'
```
### Obtener Pokémon por habilidad
```sql
SELECT FROM Pokemon WHERE out('PoseeHabilidad ').name = 'adaptability'
```
### Obtener Pokémon por grupo huevo
```sql
SELECT FROM Pokemon WHERE out('PerteneceGrupoHuevo').name = 'Dragon'
```
### Obtener Pokémon por colores
```sql
SELECT FROM Pokemon WHERE out('EsDeColor').name = 'Green'
```
### Obtener Pokémon por categoría
```sql
SELECT FROM Pokemon WHERE out('PerteneceCategoria').name = 'Illegal'
```
### Obtener Pokémon que pueden aprender un movimiento
```sql
SELECT expand(in('AprendeMovimiento')) FROM Movimiento WHERE id = 'tackle'
```
### Obtener Movimientos de un Pokémon
```sql
SELECT FROM Movimiento 
WHERE id IN (
  SELECT id FROM (
    SELECT expand(out('AprendeMovimiento')) FROM Pokemon WHERE id = 'pikachu'
  )
)
```
### Obtener Pokémon por nombre
- Similar to LIKE, but ILIKE is case insensitive.
- % is used as a wildcard
```sql
SELECT FROM Pokemon WHERE name ILIKE "%drapion%"
```
### Cómo saber si dos Pokémon pueden criar
```sql
SELECT SHORTESTPATH(
(SELECT FROM Pokemon WHERE id = "drapion"),
(SELECT FROM Pokemon WHERE id="cacturne"),
'BOTH', ['PerteneceGrupoHuevo'])
```
### Cadena de crianza
¿Cómo puede Pikachu aprender Lanzallamas?
La idea es obtener los Pokémon que aprenden Lanzallamas y calcular SHORTESTPATH con cada uno para averiguar si, a través de la crianza, Pikachu puede aprender Lanzallamas criando con un Charizard. 
1. Se obtienen los Pokémon que aprenden Lanzallamas.
2. En un bucle, se hacen peticiones de SHORTESTPATH hasta encontrar un camino.
3. Opcional. Obtener todos los caminos y hallar el mínimo de todos ellos
Esta idea combina consultas a ArcadeDB y procesamiento con Python.