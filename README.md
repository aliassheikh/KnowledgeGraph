# Assignment: Photos in a Knowledge Graph

My `KnowledgeGraph` repository includes:

- A custom **RDF vocabulary** (`vocab.ttl`) with classes and properties for students, skills, photos and locations, aligned to FOAF
- A corresponding **RDF dataset** (`data.ttl`) with students, skills, locations and photographs
- A **Notation3 query** (`lab5-photos-query.n3`) for the EYE reasoner
- Publication of all files using **GitHub Pages**
- An automated **test suite** (pytest) that validates both local files and the live web endpoints via CI

---

## Vocabulary (`vocab.ttl`)

**Classes**

| Class | FOAF alignment |
|-------|----------------|
| `exvoc:Student` | `rdfs:subClassOf foaf:Person` |
| `exvoc:Skill` | — |
| `exvoc:Photo` | `rdfs:subClassOf foaf:Image` |
| `exvoc:Location` | — |

**Properties**

| Property | Type | FOAF alignment |
|----------|------|----------------|
| `exvoc:hasSkill` | ObjectProperty | — |
| `exvoc:studentId` | DatatypeProperty | — |
| `exvoc:title` | DatatypeProperty | `rdfs:subPropertyOf foaf:name` |
| `exvoc:hasPhotographer` | ObjectProperty | `rdfs:subPropertyOf foaf:maker` |
| `exvoc:depicts` | ObjectProperty | `rdfs:subPropertyOf foaf:depicts` |
| `exvoc:takenAt` | ObjectProperty | — |
| `exvoc:description` | DatatypeProperty | — |

Vocabulary URL: **https://aliassheikh.github.io/KnowledgeGraph/vocab.ttl**

---

## Dataset (`data.ttl`)

The dataset describes Ali (a student), his skills, three photographs and the locations where they were taken.

Dataset URL: **https://aliassheikh.github.io/KnowledgeGraph/data.ttl**

---

## Reasoning (`lab5-photos-query.n3`)

An N3 rule used with the [EYE reasoner](https://github.com/eyereasoner/eye) queries all photographs and their depicted persons using only FOAF terms. Because the ontology declares `exvoc:Photo rdfs:subClassOf foaf:Image` and `exvoc:depicts rdfs:subPropertyOf foaf:depicts`, RDFS entailment bridges the custom vocabulary to FOAF automatically.

The same command works over multiple students' datasets simultaneously:

```bash
eye --nope --turtle vocab.ttl --turtle data.ttl --query lab5-photos-query.n3
```

---

## GitHub Pages Publication

Both RDF files are published as Linked Data:

- `Content-Type: text/turtle; charset=utf-8`
- `Access-Control-Allow-Origin: *` (CORS enabled)
- HTTP/2 200

---

## Testing

[![Test RDF files](https://github.com/aliassheikh/KnowledgeGraph/actions/workflows/test.yml/badge.svg)](https://github.com/aliassheikh/KnowledgeGraph/actions/workflows/test.yml)

Two automated test jobs run on every push:

| Job | What it tests |
|-----|--------------|
| `test` | Local `vocab.ttl` and `data.ttl`: syntax, classes, properties, FOAF alignment, instance data |
| `test-web` | Live GitHub Pages endpoints: HTTP 200, `Content-Type`, CORS, Turtle validity |

Run locally:

```bash
pip install rdflib pytest
pytest tests/ -v
```

Full documentation is in [lab5-photos.md](lab5-photos.md).
