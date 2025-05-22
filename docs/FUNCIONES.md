Generado por ChatGPT a partir de la documentación oficial: https://docs.arcadedb.com/#sql-functions
---

ArcadeDB es una base de datos multi-modelo que admite modelos de grafos, documentos, clave-valor, series temporales y vectores. En el contexto de grafos, ArcadeDB ofrece funciones SQL específicas para facilitar la navegación y manipulación de estructuras de grafos. A continuación, se presentan algunas de las funciones de grafos disponibles en ArcadeDB, junto con ejemplos sencillos de su uso:

---

### 🔹 `TRAVERSE`

La función `TRAVERSE` permite recorrer el grafo a partir de un vértice específico, siguiendo las aristas conectadas.

**Ejemplo:**

```sql
TRAVERSE out() FROM (SELECT FROM Persona WHERE nombre = 'Juan') WHILE $depth <= 2
```



Este comando recorre los vértices conectados a 'Juan' hasta una profundidad de 2.

---

### 🔹 `MATCH`

La cláusula `MATCH` se utiliza para realizar consultas de patrones en el grafo, similar a cómo se usa en otros lenguajes de consulta de grafos como Cypher.

**Ejemplo:**

```sql
MATCH {class: Persona, as: p} -[AmigoDe]-> {class: Persona, as: amigo}
RETURN p.nombre, amigo.nombre
```



Esta consulta devuelve pares de personas y sus amigos.

---

### 🔹 `SHORTESTPATH()`

La función `SHORTESTPATH()` encuentra el camino más corto entre dos vértices en el grafo.

**Ejemplo:**

```sql
SELECT SHORTESTPATH((SELECT FROM Pokemon WHERE name = "Ivysaur"), (SELECT FROM Pokemon WHERE name = "Caterpie"), 'BOTH', ['PerteneceGrupoHuevo','EvolucionaEn'])

SELECT SHORTESTPATH((SELECT FROM Pokemon WHERE name = "Bulbasaur"), (SELECT FROM Movimiento WHERE id="lightscreen"), 'BOTH', ['PerteneceGrupoHuevo','AprendeMovimiento'])
```



Esta consulta encuentra el camino más corto entre las ciudades de Madrid y Barcelona a través de la arista 'ConectadoA'.

---

### 🔹 `Dijkstra()`

La función `Dijkstra()` calcula el camino más corto entre dos vértices considerando pesos en las aristas.

**Ejemplo:**

```sql
SELECT DIJKSTRA((SELECT FROM Ciudad WHERE nombre = 'Madrid'), (SELECT FROM Ciudad WHERE nombre = 'Barcelona'), 'ConectadoA', 'distancia')
```



Esta consulta encuentra el camino más corto entre Madrid y Barcelona, considerando la propiedad 'distancia' en las aristas 'ConectadoA'.

---

### 🔹 `BREADTHFIRST()`

La función `BREADTHFIRST()` realiza una búsqueda en anchura desde un vértice inicial.

**Ejemplo:**

```sql
SELECT BREADTHFIRST((SELECT FROM Persona WHERE nombre = 'Juan'), 'AmigoDe')
```



Esta consulta realiza una búsqueda en anchura de los amigos de 'Juan' a través de la arista 'AmigoDe'.

---

### 🔹 `DEPTHFIRST()`

La función `DEPTHFIRST()` realiza una búsqueda en profundidad desde un vértice inicial.

**Ejemplo:**

```sql
SELECT DEPTHFIRST((SELECT FROM Persona WHERE nombre = 'Juan'), 'AmigoDe')
```



Esta consulta realiza una búsqueda en profundidad de los amigos de 'Juan' a través de la arista 'AmigoDe'.

---

Estas funciones permiten realizar consultas complejas y eficientes en estructuras de grafos dentro de ArcadeDB utilizando SQL. Para más detalles y funciones adicionales, se recomienda consultar la documentación oficial de ArcadeDB.
