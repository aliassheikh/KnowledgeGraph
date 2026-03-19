# Lab 5 Submission

## A — Links to data and ontology

| Resource | URL |
|----------|-----|
| Ontology (vocabulary) | <https://aliassheikh.github.io/KnowledgeGraph/vocab.ttl> |
| Dataset | <https://aliassheikh.github.io/KnowledgeGraph/data.ttl> |

---

## B — Task 4: Why this works and what the impact is

### Why the reasoning query works

The ontology (`vocab.ttl`) declares two alignment axioms:

```turtle
exvoc:Photo   rdfs:subClassOf    foaf:Image .
exvoc:depicts rdfs:subPropertyOf foaf:depicts .
```

When an RDFS-aware reasoner (e.g. EYE) loads both `vocab.ttl` and `data.ttl`, it applies the standard RDFS entailment rules:

- **subClassOf rule:** if `exvoc:Photo rdfs:subClassOf foaf:Image` and `ex:photoMe a exvoc:Photo`, then `ex:photoMe a foaf:Image` is inferred.
- **subPropertyOf rule:** if `exvoc:depicts rdfs:subPropertyOf foaf:depicts` and `ex:photoMe exvoc:depicts ex:me`, then `ex:photoMe foaf:depicts ex:me` is inferred.

A query written entirely in FOAF terms — `{ ?photo a foaf:Image ; foaf:depicts ?person }` — therefore matches all three photos, even though the raw data only uses `exvoc:` predicates. The same query also works over another student's dataset as long as their ontology is similarly aligned to FOAF, because FOAF acts as the shared vocabulary bridging the two datasets.

### What the impact is

1. **Interoperability without data changes** — The FOAF alignment lives in the ontology, so the data file never needs to be touched. Any tool or query that understands FOAF can already work with the data.
2. **Cross-dataset querying** — Loading multiple students' datasets alongside the shared vocabulary lets a single FOAF query retrieve photos and depicted persons from all of them in one pass.
3. **Separation of concerns** — Domain-specific properties (e.g. `exvoc:takenAt`, `exvoc:studentId`) stay in the custom vocabulary while the semantic bridge to a widely adopted standard is managed in one place. Changing the mapping later only requires updating the ontology, not every data triple.
