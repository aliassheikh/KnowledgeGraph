# Assignment: Photos in a Knowledge Graph

## Files

- **Ontology (vocabulary):** [vocab.ttl](https://aliassheikh.github.io/KnowledgeGraph/vocab.ttl)
- **Dataset:** [data.ttl](https://aliassheikh.github.io/KnowledgeGraph/data.ttl)

---

## Tasks - PART 1: Update your data and ontology

The vocabulary (`vocab.ttl`) was extended with two new classes and five new properties to model photographs:

### New Classes

| Class | Description |
|-------|-------------|
| `exvoc:Photo` | A photograph |
| `exvoc:Location` | A physical place where a photo was taken |

### New Properties

| Property | Type | Description |
|----------|------|-------------|
| `exvoc:title` | DatatypeProperty | The title or name of the photo |
| `exvoc:hasPhotographer` | ObjectProperty | Links a photo to its photographer |
| `exvoc:depicts` | ObjectProperty | Links a photo to a person depicted in it |
| `exvoc:takenAt` | ObjectProperty | Links a photo to the location where it was taken |
| `exvoc:description` | DatatypeProperty | A textual description or summary of the photo |

### New Data Instances

Three photos were added to `data.ttl`, including one of myself (`ex:photoMe`):

| Photo | Title | Photographer | Depicts | Location |
|-------|-------|--------------|---------|----------|
| `ex:photoMe` | Profile Photo of Ali | Student A | Ali | Amsterdam |
| `ex:photoGroupStudy` | Group Study Session | Student A | Ali, Student A, Student B | University Library |
| `ex:photoCampus` | Campus Walk | Student B | Ali, Student B | University Garden |

Example triple for the self-portrait:
```turtle
ex:photoMe a exvoc:Photo ;
    exvoc:title "Profile Photo of Ali" ;
    exvoc:hasPhotographer ex:studentA ;
    exvoc:depicts ex:me ;
    exvoc:takenAt ex:locationAmsterdam ;
    exvoc:description "A personal profile photo of Ali, taken in Amsterdam." .
```

---

## Tasks - PART 2: Link to an existing ontology

The ontology was extended with `rdfs:subClassOf` and `rdfs:subPropertyOf` statements to connect its concepts to [FOAF](http://xmlns.com/foaf/spec/):

```turtle
exvoc:Student     rdfs:subClassOf    foaf:Person .
exvoc:Photo       rdfs:subClassOf    foaf:Image .
exvoc:depicts     rdfs:subPropertyOf foaf:depicts .
exvoc:hasPhotographer rdfs:subPropertyOf foaf:maker .
exvoc:title       rdfs:subPropertyOf foaf:name .
```

**Rationale:**
- `exvoc:Student` is a specialisation of a person, so `foaf:Person` is the right superclass.
- `exvoc:Photo` is a specialisation of an image, matching `foaf:Image`.
- `exvoc:depicts` maps directly to `foaf:depicts`, which FOAF already defines for images.
- `exvoc:hasPhotographer` corresponds to FOAF's `foaf:maker` (the creator of a document/image).
- `exvoc:title` is used as the name of a photo, which aligns with `foaf:name`.

---

## Tasks - PART 3: Reasoning over your data

The EYE reasoner (a Notation3 reasoner) was used to query the data with FOAF-only terms.
The N3 rule file [`lab5-photos-query.n3`](lab5-photos-query.n3) contains the following rule:

```n3
@prefix foaf: <http://xmlns.com/foaf/0.1/> .

{
    ?photo a foaf:Image ;
           foaf:depicts ?person .
    ?person foaf:name ?name .
} => {
    ?photo foaf:depicts ?person .
    ?person foaf:name ?name .
} .
```

The EYE reasoner is loaded with:
1. `data.ttl` — the instance data
2. `vocab.ttl` — the ontology (containing the subclass/subproperty links)
3. RDFS rules — so the reasoner applies `rdfs:subClassOf` and `rdfs:subPropertyOf` entailments
4. The N3 rule file as the query

Because of the RDFS entailments, the reasoner first infers:
- Every `exvoc:Photo` instance is also a `foaf:Image` instance.
- Every `exvoc:depicts` triple is also a `foaf:depicts` triple.
- Every `exvoc:Student` instance is also a `foaf:Person` instance.

This allows the FOAF-only query to match all three photos and their depicted persons, even though the data uses `exvoc:` predicates.

**Expected output triples:**

| Photo | Depicted person | Name |
|-------|----------------|------|
| `ex:photoMe` | `ex:me` | "Ali" |
| `ex:photoGroupStudy` | `ex:me` | "Ali" |
| `ex:photoGroupStudy` | `ex:studentA` | "Student A" |
| `ex:photoGroupStudy` | `ex:studentB` | "Student B" |
| `ex:photoCampus` | `ex:me` | "Ali" |
| `ex:photoCampus` | `ex:studentB` | "Student B" |

---

## How to Test

The Turtle files and the FOAF alignment can be validated automatically using the Python test suite in `tests/test_rdf.py`.

### Prerequisites

```bash
pip install rdflib pytest
```

### Run all tests

```bash
pytest tests/ -v
```

The suite covers:

| Test group | What is checked |
|------------|-----------------|
| `test_vocab_parses` | `vocab.ttl` is valid Turtle with at least one triple |
| `test_vocab_defines_class` | All four classes are declared (`Student`, `Skill`, `Photo`, `Location`) |
| `test_vocab_defines_property` | All seven properties are declared |
| `test_*_subclass/subproperty_of_foaf_*` | FOAF alignment axioms are present |
| `test_data_parses` | `data.ttl` is valid Turtle with at least one triple |
| `test_data_student_exists` | All three students exist with correct `foaf:name` |
| `test_data_skill_exists` | All three skills exist with correct `rdfs:label` |
| `test_data_location_exists` | All three locations exist with correct `rdfs:label` |
| `test_data_photo_has_title` | All three photos exist with correct `exvoc:title` |
| `test_photos_all_have_required_properties` | Every photo has title, photographer, depicts, takenAt, and description |
| `test_combined_*` | The combined graph contains the subClassOf/subPropertyOf triples the EYE reasoner needs |

Tests run automatically on every push via the [GitHub Actions workflow](.github/workflows/test.yml).

### Test the N3 reasoning with EYE

To run the reasoning query from Part 3 locally, install the [EYE reasoner](https://github.com/eyereasoner/eye) and execute:

```bash
eye --nope --turtle vocab.ttl --turtle data.ttl --query lab5-photos-query.n3
```

The `--nope` flag limits output to only the query conclusions. You should see six inferred triples — one for each (photo, depicted-person) pair — using only FOAF terms.

---

## Tasks - PART 4: Reflection

### Question 1: What does the reasoner infer, and why does it work?

The EYE reasoner applies RDFS rules to the combined input of `data.ttl` and `vocab.ttl`. The key inferences are driven by the `rdfs:subClassOf` and `rdfs:subPropertyOf` axioms in the ontology:

- **RDFS rule for subClassOf:**  
  If `C rdfs:subClassOf D` and `x a C`, then `x a D`.  
  → Because `exvoc:Photo rdfs:subClassOf foaf:Image`, every instance typed as `exvoc:Photo` in `data.ttl` is automatically also inferred to be of type `foaf:Image`.

- **RDFS rule for subPropertyOf:**  
  If `P rdfs:subPropertyOf Q` and `x P y`, then `x Q y`.  
  → Because `exvoc:depicts rdfs:subPropertyOf foaf:depicts`, every triple `?photo exvoc:depicts ?person` in `data.ttl` is also inferred as `?photo foaf:depicts ?person`.

Without these RDFS rules the query `{ ?photo a foaf:Image ; foaf:depicts ?person }` would return no results, because the raw data only contains `exvoc:Photo` and `exvoc:depicts`. The reasoner makes the bridge possible.

### Question 2: What is the benefit of linking your ontology to FOAF?

Linking the custom ontology to FOAF provides **semantic interoperability**:

1. **Reuse of existing tooling** — Any application or query that understands FOAF can now work with the custom data without needing to know about `exvoc:` terms.
2. **Integration with other datasets** — Other knowledge graphs that use FOAF can be combined with this data through federated queries or reasoning, enabling discovery of common persons and images across sources.
3. **Expressiveness without duplication** — The custom ontology can add domain-specific detail (e.g. `exvoc:takenAt`, `exvoc:studentId`) while still inheriting the semantics and interoperability of a well-known vocabulary.
4. **Future-proofing** — FOAF is a widely adopted standard. Aligning to it means the data remains interpretable even if the custom ontology evolves.

### Question 3: Why is `rdfs:subPropertyOf` preferred over simply using `foaf:depicts` directly in the data?

Using `rdfs:subPropertyOf` keeps **ontology-level decisions separate from data-level decisions**. The data is modelled in the domain vocabulary (`exvoc:`), which can carry additional semantics (e.g. a domain or range constraint specific to photos). The alignment to FOAF is declared once in the ontology, rather than duplicating every triple in the data. This also means that if the mapping to FOAF changes (e.g. a better-fitting property is found), only the ontology needs to be updated, not every data triple.
