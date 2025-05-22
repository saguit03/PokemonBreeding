# Consultas sobre ArcadeDB

## Consultas simples

### Obtener Pokémon de una generación

```sql
SELECT FROM Pokemon WHERE out('PerteneceGeneracion').name = 'Gen 1'
```

