# Assignment: SPARQL Queries on Wikidata


## Tasks - PART 1:
### Task 1:
Write a SPARQL query that selects all railway stations in the Netherlands that have the “Rijksmonument” as heritage designation (P1435).

```sparql
SELECT ?station ?stationLabel WHERE {
  ?station wdt:P31  wd:Q55488   .  # instance of: railway station
  ?station wdt:P17  wd:Q55      .  # country: Netherlands
  ?station wdt:P1435 wd:Q916333 .  # heritage designation: Rijksmonument
  SERVICE wikibase:label {
    bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en".
  }
}
ORDER BY ?stationLabel
```
#### Explanation
| Clause | Meaning |
|--------|---------|
| `wdt:P31 wd:Q55488` | The item must be an *instance of* (`P31`) a **railway station** (`Q55488`) |
| `wdt:P17 wd:Q55` | The item must have **country** (`P17`) set to **Netherlands** (`Q55`) |
| `wdt:P1435 wd:Q916333` | The item must have **heritage designation** (`P1435`) set to **Rijksmonument** (`Q916333`) |
| `SERVICE wikibase:label` | A Wikidata-specific service that automatically fetches human-readable labels in the preferred language |
The `wdt:` prefix refers to *direct* (simple) property statements, and `wd:` refers to Wikidata entity URIs.


### Task 2:
Write a SPARQL query that counts all “Rijksmonument” in the Netherlands, grouped by their type (instance of).
You can include the type labels. Which type do you think is most common? Windmills? Museums? Castles? ;-)
* no need to recurse the subTypes
```sparql
SELECT ?type ?typeLabel (COUNT(?item) AS ?count) WHERE {
  ?item wdt:P1435 wd:Q916333 .  # heritage designation: Rijksmonument
  ?item wdt:P17   wd:Q55     .  # country: Netherlands
  ?item wdt:P31   ?type      .  # instance of: (any type, captured in ?type)
  SERVICE wikibase:label {
    bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en".
  }
}
GROUP BY ?type ?typeLabel
ORDER BY DESC(?count)
```
#### Explanation
| Clause | Meaning |
|--------|---------|
| `wdt:P1435 wd:Q916333` | Filter to items whose heritage designation is Rijksmonument |
| `wdt:P17 wd:Q55` | Filter to items located in the Netherlands |
| `wdt:P31 ?type` | Bind the *instance of* value to variable `?type` (one row per type) |
| `COUNT(?item)` | Count the number of items per type |
| `GROUP BY ?type ?typeLabel` | Group the aggregated results by type URI and its label |
| `ORDER BY DESC(?count)` | Show the most common types first |

#### First six most common types:
| Type | TypeLabel | Count |
|------|-----------|-------|
| wd:Q3947 | house | 12917 |
| wd:Q41176 | building | 11257 |
| wd:Q17489143 | building with cornice | 3749|
| wd:Q489357|farmhouse | 3389 |
| wd:Q16970|church building | 2444 |
| wd:Q131596|farm | 2038 |

---

### To Find URIs for things: Using Wikidata serarch bar
* station       --> railway station (Q55488)
* Netherlands   --> Netherlands (Q55)
* Rijksmonument --> Rijksmonument (Q916333)

When you open an item, you can see
* its properties (for example P1435 = heritage designation)
* its classes (for example P31 = instance of)


### The Open World Assumption (OWA)
Wikidata uses the Open World Assumption: Just because something is not in Wikidata does not mean it does not exist.
So if a railway station is a Rijksmonument in reality but Wikidata lacks that statement, it will not see it in a query.

---

## Tasks - PART 2:
### A. First attempt: I used first this query but it doesn´t have any result:
```sparql
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX schema: <http://schema.org/>

SELECT ?person ?name WHERE {

  # Your own data
  SERVICE <https://aliassheikh.github.io/KnowledgeGraph/vocab.ttl> {
    ?person (foaf:name) ?name .
  }

  # DANS course participants
  SERVICE <https://dans-knaw-jp.github.io/IKG/lab2/data.ttl> {
    ?person (foaf:name) ?name .
  }

  SERVICE <https://paulboon.github.io/knowledgegraph/employee-paulboon.ttl> {
    ?person (foaf:name) ?name .
  }

  SERVICE <https://laurahuisintveld.github.io/KnowledgeGraph/data.ttl> {
    ?person (foaf:name) ?name .
  }
}
```

### B. Second attempt: Also with this query the result is empty:

```sparql
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX schema: <http://schema.org/>

SELECT ?person ?name WHERE {

  # Your own data
  SERVICE <https://aliassheikh.github.io/KnowledgeGraph/vocab.ttl> {
    ?person (foaf:name|schema:name) ?name .
  }

  # DANS course participants
  SERVICE <https://dans-knaw-jp.github.io/IKG/lab2/data.ttl> {
    ?person (foaf:name|schema:name) ?name .
  }

  SERVICE <https://paulboon.github.io/knowledgegraph/employee-paulboon.ttl> {
    ?person (foaf:name|schema:name) ?name .
  }

  SERVICE <https://laurahuisintveld.github.io/KnowledgeGraph/data.ttl> {
    ?person (foaf:name|schema:name) ?name .
  }
}
```
### C. Third attempt: with this query, I get 4 items:
```sparql
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX schema: <http://schema.org/>

SELECT  ?person ?name WHERE {

  {
    SERVICE <https://aliassheikh.github.io/KnowledgeGraph/vocab.ttl> {
      ?person (foaf:name|schema:name) ?name .
    }
  }
  UNION
  {
    SERVICE <https://dans-knaw-jp.github.io/IKG/lab2/data.ttl> {
      ?person (foaf:name|schema:name) ?name .
    }
  }
  UNION
  {
    SERVICE <https://paulboon.github.io/knowledgegraph/employee-paulboon.ttl> {
      ?person (foaf:name|schema:name) ?name .
    }
  }
  UNION
  {
    SERVICE <https://laurahuisintveld.github.io/KnowledgeGraph/data.ttl> {
      ?person (foaf:name|schema:name) ?name .
    }
  }
}
```
**===>**
**Query results**
```shell
?name "Paul Boon"
?person https://paulboon.github.io/knowledgegraph/employee-paulboon.ttl#PaulBoon
?name "Chris Baars"
?person https://paulboon.github.io/knowledgegraph/employee-paulboon.ttl#ChrisBaars
?name "Laura Huis in 't Veld"
?person https://paulboon.github.io/knowledgegraph/employee-paulboon.ttl#LauraHuisInTVeld
?name "Laurens Tobias"
?person https://paulboon.github.io/knowledgegraph/employee-paulboon.ttl#LaurensTobias
```

### Interoperability Problems:
1. Different RDF types (`exvoc:Student` vs `foaf:Person vs schema:Person`) → solved with `UNION`
2. Different name predicates (`foaf:name` vs `schema:name` vs `rdfs:label`) → solved with property path `foaf:name|schema:name`
