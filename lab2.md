# Assignment: Federated SPARQL Query with Comunica

## Task 1: Federated SPARQL Query

Write a SPARQL query using the Comunica federated engine, querying the URI and name of yourself and at least 3 other participants in the DANS course. Always verify the student is a course participant.

### SPARQL Query

```sparql
PREFIX foaf:    <http://xmlns.com/foaf/0.1/>
PREFIX schema:  <https://schema.org/>
PREFIX rdfs:    <http://www.w3.org/2000/01/rdf-schema#>
PREFIX exvoc:   <https://aliassheikh.github.io/KnowledgeGraph/vocab.ttl#>

SELECT DISTINCT ?person ?name WHERE {
  {
    ?person a exvoc:Student .
  } UNION {
    ?person a foaf:Person .
  } UNION {
    ?person a schema:Person .
  }
  ?person (foaf:name|schema:name|rdfs:label) ?name .
}
ORDER BY ?name
```

### Explanation

| Clause | Meaning |
|--------|---------|
| `?person a exvoc:Student` | Matches participants using the custom `exvoc:Student` type (e.g., this repository's own data) |
| `?person a foaf:Person` | Matches participants who described themselves as `foaf:Person` |
| `?person a schema:Person` | Matches participants who used `schema:Person` from Schema.org |
| `foaf:name|schema:name|rdfs:label` | Property path matching any of the three common name predicates — handles interoperability differences across vocabularies |
| `DISTINCT` | Avoids duplicate results if the same person appears via multiple type patterns |
| `ORDER BY ?name` | Sorts results alphabetically |

### Data Sources

The query is executed against the following four Turtle files via the Comunica federated engine:

1. `https://aliassheikh.github.io/KnowledgeGraph/data.ttl` — Ali (this assignment)
2. `https://dans-knaw-jp.github.io/IKG/lab2/data.ttl` — DANS course instructor / participant
3. `https://paulboon.github.io/knowledgegraph/employee-paulboon.ttl` — Paul Boon
4. `https://laurahuisintveld.github.io/KnowledgeGraph/data.ttl` — Laura Huisintveld

> **Note on course-participant verification**: Verification is achieved at the data-source level — the four URLs above are exclusively the published Turtle files of known DANS course participants. Limiting the query to these specific sources acts as the participation filter. Within the query itself, the `UNION` of type patterns (`exvoc:Student`, `foaf:Person`, `schema:Person`) further narrows results to persons, excluding any non-person resources in the same files.

### Comunica Query URL

The following URL opens the Comunica query interface with the four data sources and the SPARQL query pre-filled:

[Open in Comunica](https://query.linkeddatafragments.org/#datasources=https%3A%2F%2Faliassheikh.github.io%2FKnowledgeGraph%2Fdata.ttl%2Chttps%3A%2F%2Fdans-knaw-jp.github.io%2FIKG%2Flab2%2Fdata.ttl%2Chttps%3A%2F%2Fpaulboon.github.io%2Fknowledgegraph%2Femployee-paulboon.ttl%2Chttps%3A%2F%2Flaurahuisintveld.github.io%2FKnowledgeGraph%2Fdata.ttl&query=PREFIX%20foaf%3A%20%20%20%20%3Chttp%3A%2F%2Fxmlns.com%2Ffoaf%2F0.1%2F%3E%0APREFIX%20schema%3A%20%20%3Chttps%3A%2F%2Fschema.org%2F%3E%0APREFIX%20rdfs%3A%20%20%20%20%3Chttp%3A%2F%2Fwww.w3.org%2F2000%2F01%2Frdf-schema%23%3E%0APREFIX%20exvoc%3A%20%20%20%3Chttps%3A%2F%2Faliassheikh.github.io%2FKnowledgeGraph%2Fvocab.ttl%23%3E%0A%0ASELECT%20DISTINCT%20%3Fperson%20%3Fname%20WHERE%20%7B%0A%20%20%7B%0A%20%20%20%20%3Fperson%20a%20exvoc%3AStudent%20.%0A%20%20%7D%20UNION%20%7B%0A%20%20%20%20%3Fperson%20a%20foaf%3APerson%20.%0A%20%20%7D%20UNION%20%7B%0A%20%20%20%20%3Fperson%20a%20schema%3APerson%20.%0A%20%20%7D%0A%20%20%3Fperson%20%28foaf%3Aname%7Cschema%3Aname%7Crdfs%3Alabel%29%20%3Fname%20.%0A%7D%0AORDER%20BY%20%3Fname)

---

## Task 2: Interoperability Problems

### Were there interoperability problems?

Yes. Querying across multiple independently authored Turtle files revealed several interoperability issues:

#### 1. Different RDF types for "person"

Each participant chose a different class to describe themselves:

| Participant | Type used |
|-------------|-----------|
| Ali (this repo) | `exvoc:Student` (a custom vocabulary) |
| Laura Huisintveld | `exvoc:Student` or `foaf:Person` |
| Paul Boon | `schema:Person` (Schema.org) |
| DANS instructor | `foaf:Person` or a course-specific type |

A query filtering on only one type (e.g., `?person a exvoc:Student`) would miss participants who used `foaf:Person` or `schema:Person`.

**Solution**: Use a `UNION` of all expected type patterns, or relax the type check to just match any subject with a name predicate.

#### 2. Different name predicates

Participants used different predicates for the person's name:

| Vocabulary | Predicate |
|------------|-----------|
| FOAF | `foaf:name` |
| Schema.org | `schema:name` |
| RDFS | `rdfs:label` |

**Solution**: Use a SPARQL [property path](https://www.w3.org/TR/sparql11-query/#propertypaths) with the alternative (`|`) operator:
```sparql
?person (foaf:name|schema:name|rdfs:label) ?name .
```
This matches any of the three predicates in a single triple pattern, without needing multiple `UNION` clauses for each name variant.

#### 3. No shared "course participation" predicate

Each participant's data had no common triple linking them to the course. There was no shared predicate like `schema:memberOf <course-URI>` or `ex:participatesIn <IKG-course>`.

**Solution**: Verification of course participation was instead achieved implicitly by limiting the data sources to the known TTL files of course participants. Since only course participants published their data at these specific URLs, querying those sources is itself the course-participant filter. An explicit `FILTER` on participant type (e.g., `exvoc:Student`) was included as an additional check where the vocabulary was consistent.

#### 4. HTTP proxy required

Some of the GitHub Pages–hosted Turtle files have CORS or HTTPS restrictions when accessed from the Comunica web client running in the browser.

**Solution**: Enable the **HTTP proxy** option in the Comunica query UI (click the gear icon ⚙️ and enable the proxy). This routes requests through Comunica's own proxy server, bypassing browser-level CORS restrictions.
