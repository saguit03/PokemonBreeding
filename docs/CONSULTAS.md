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

### Cómo saber si dos Pokémon pueden criar

```sql
SELECT SHORTESTPATH(
(SELECT FROM Pokemon WHERE id = "drapion"),
(SELECT FROM Pokemon WHERE id="cacturne"),
'BOTH', ['PerteneceGrupoHuevo'])
```

### Cadena de crianza

```sql
EN PROCESO
```