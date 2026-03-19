"""Live-URL tests for the KnowledgeGraph GitHub Pages publication.

These tests make real HTTP requests to the published endpoints and verify:
  - HTTP 200 status
  - Content-Type includes "text/turtle"
  - CORS header allows any origin
  - The response body parses as valid Turtle

They are marked ``network`` so they can be skipped when there is no internet
access::

    pytest tests/ -v -m "not network"   # offline  (skips this file)
    pytest tests/ -v                     # online   (runs everything)
    pytest tests/test_web.py -v         # only the live-URL tests

The GitHub Actions ``test-web`` job runs them automatically after every push.
"""
import io
import urllib.request
import urllib.error
import pytest
from rdflib import Graph, Namespace, RDF, RDFS, OWL

# ── Published endpoints ────────────────────────────────────────────────────────
VOCAB_URL = "https://aliassheikh.github.io/KnowledgeGraph/vocab.ttl"
DATA_URL  = "https://aliassheikh.github.io/KnowledgeGraph/data.ttl"

EXVOC = Namespace("https://aliassheikh.github.io/KnowledgeGraph/vocab.ttl#")
FOAF  = Namespace("http://xmlns.com/foaf/0.1/")

# ── Helpers ────────────────────────────────────────────────────────────────────

def _fetch(url: str):
    """Return (response_object, body_bytes).  Skip the test on network errors."""
    try:
        req = urllib.request.Request(url, headers={"Accept": "text/turtle"})
        resp = urllib.request.urlopen(req, timeout=15)
        body = resp.read()
        return resp, body
    except urllib.error.URLError as exc:
        pytest.skip(f"Network unavailable ({exc}): skipping live-URL test")


# ── Fixtures (one HTTP fetch per URL, cached for the whole module) ─────────────

@pytest.fixture(scope="module")
def vocab_response():
    return _fetch(VOCAB_URL)


@pytest.fixture(scope="module")
def data_response():
    return _fetch(DATA_URL)


@pytest.fixture(scope="module")
def vocab_graph(vocab_response):
    _, body = vocab_response
    g = Graph()
    g.parse(io.BytesIO(body), format="turtle")
    return g


@pytest.fixture(scope="module")
def data_graph(data_response):
    _, body = data_response
    g = Graph()
    g.parse(io.BytesIO(body), format="turtle")
    return g


# ── vocab.ttl endpoint ────────────────────────────────────────────────────────

@pytest.mark.network
def test_vocab_http_ok(vocab_response):
    """GET vocab.ttl returns HTTP 200."""
    resp, _ = vocab_response
    assert resp.status == 200, f"Expected 200, got {resp.status}"


@pytest.mark.network
def test_vocab_content_type(vocab_response):
    """vocab.ttl is served as text/turtle."""
    resp, _ = vocab_response
    ct = resp.headers.get("Content-Type", "")
    assert "text/turtle" in ct, \
        f"Expected Content-Type to contain 'text/turtle', got {ct!r}"


@pytest.mark.network
def test_vocab_cors_header(vocab_response):
    """vocab.ttl includes CORS header so browsers can fetch it."""
    resp, _ = vocab_response
    acao = resp.headers.get("Access-Control-Allow-Origin", "")
    assert acao == "*", \
        f"Expected Access-Control-Allow-Origin: *, got {acao!r}"


@pytest.mark.network
def test_vocab_parses_as_turtle(vocab_graph):
    """The response body of vocab.ttl is valid Turtle with at least one triple."""
    assert len(vocab_graph) > 0


@pytest.mark.network
@pytest.mark.parametrize("cls", [
    EXVOC.Student,
    EXVOC.Skill,
    EXVOC.Photo,
    EXVOC.Location,
])
def test_live_vocab_defines_class(vocab_graph, cls):
    assert (cls, RDF.type, RDFS.Class) in vocab_graph, \
        f"Live vocab missing class {cls}"


@pytest.mark.network
@pytest.mark.parametrize("prop", [
    EXVOC.hasSkill,
    EXVOC.studentId,
    EXVOC.title,
    EXVOC.hasPhotographer,
    EXVOC.depicts,
    EXVOC.takenAt,
    EXVOC.description,
])
def test_live_vocab_defines_property(vocab_graph, prop):
    is_object   = (prop, RDF.type, OWL.ObjectProperty)   in vocab_graph
    is_datatype = (prop, RDF.type, OWL.DatatypeProperty) in vocab_graph
    assert is_object or is_datatype, \
        f"Live vocab missing property {prop}"


@pytest.mark.network
def test_live_vocab_foaf_alignment(vocab_graph):
    """FOAF subClassOf / subPropertyOf axioms are present in the live vocab."""
    assert (EXVOC.Student,        RDFS.subClassOf,    FOAF.Person)  in vocab_graph
    assert (EXVOC.Photo,          RDFS.subClassOf,    FOAF.Image)   in vocab_graph
    assert (EXVOC.depicts,        RDFS.subPropertyOf, FOAF.depicts) in vocab_graph
    assert (EXVOC.hasPhotographer,RDFS.subPropertyOf, FOAF.maker)   in vocab_graph
    assert (EXVOC.title,          RDFS.subPropertyOf, FOAF.name)    in vocab_graph


# ── data.ttl endpoint ─────────────────────────────────────────────────────────

@pytest.mark.network
def test_data_http_ok(data_response):
    """GET data.ttl returns HTTP 200."""
    resp, _ = data_response
    assert resp.status == 200, f"Expected 200, got {resp.status}"


@pytest.mark.network
def test_data_content_type(data_response):
    """data.ttl is served as text/turtle."""
    resp, _ = data_response
    ct = resp.headers.get("Content-Type", "")
    assert "text/turtle" in ct, \
        f"Expected Content-Type to contain 'text/turtle', got {ct!r}"


@pytest.mark.network
def test_data_cors_header(data_response):
    """data.ttl includes CORS header so browsers can fetch it."""
    resp, _ = data_response
    acao = resp.headers.get("Access-Control-Allow-Origin", "")
    assert acao == "*", \
        f"Expected Access-Control-Allow-Origin: *, got {acao!r}"


@pytest.mark.network
def test_data_parses_as_turtle(data_graph):
    """The response body of data.ttl is valid Turtle with at least one triple."""
    assert len(data_graph) > 0


@pytest.mark.network
def test_live_data_has_three_students(data_graph):
    students = list(data_graph.subjects(RDF.type, EXVOC.Student))
    assert len(students) == 3, f"Expected 3 students in live data, got {len(students)}"


@pytest.mark.network
def test_live_data_has_three_photos(data_graph):
    photos = list(data_graph.subjects(RDF.type, EXVOC.Photo))
    assert len(photos) == 3, f"Expected 3 photos in live data, got {len(photos)}"


@pytest.mark.network
def test_live_data_has_three_skills(data_graph):
    skills = list(data_graph.subjects(RDF.type, EXVOC.Skill))
    assert len(skills) == 3, f"Expected 3 skills in live data, got {len(skills)}"


@pytest.mark.network
def test_live_data_has_three_locations(data_graph):
    locations = list(data_graph.subjects(RDF.type, EXVOC.Location))
    assert len(locations) == 3, f"Expected 3 locations in live data, got {len(locations)}"
