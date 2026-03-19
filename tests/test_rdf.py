"""Tests for KnowledgeGraph RDF files.

Validates that vocab.ttl and data.ttl parse as valid Turtle and contain
the expected classes, properties, instances, and FOAF alignments.

Run locally:
    pip install rdflib pytest
    pytest tests/ -v
"""
import pytest
from pathlib import Path
from rdflib import Graph, Namespace, RDF, RDFS, OWL, Literal

# ── Namespaces ─────────────────────────────────────────────────────────────────
EXVOC = Namespace("https://aliassheikh.github.io/KnowledgeGraph/vocab.ttl#")
EX    = Namespace("https://aliassheikh.github.io/KnowledgeGraph/data.ttl#")
FOAF  = Namespace("http://xmlns.com/foaf/0.1/")

ROOT  = Path(__file__).parent.parent


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def vocab():
    g = Graph()
    g.parse(ROOT / "vocab.ttl", format="turtle")
    return g


@pytest.fixture(scope="module")
def data():
    g = Graph()
    g.parse(ROOT / "data.ttl", format="turtle")
    return g


@pytest.fixture(scope="module")
def combined(vocab, data):
    g = Graph()
    g += vocab
    g += data
    return g


# ── vocab.ttl: syntax ─────────────────────────────────────────────────────────

def test_vocab_parses(vocab):
    """vocab.ttl must parse without errors and contain at least one triple."""
    assert len(vocab) > 0


# ── vocab.ttl: classes ────────────────────────────────────────────────────────

@pytest.mark.parametrize("cls", [
    EXVOC.Student,
    EXVOC.Skill,
    EXVOC.Photo,
    EXVOC.Location,
])
def test_vocab_defines_class(vocab, cls):
    assert (cls, RDF.type, RDFS.Class) in vocab, \
        f"Expected class {cls} to be declared in vocab.ttl"


# ── vocab.ttl: properties ─────────────────────────────────────────────────────

@pytest.mark.parametrize("prop", [
    EXVOC.hasSkill,
    EXVOC.studentId,
    EXVOC.title,
    EXVOC.hasPhotographer,
    EXVOC.depicts,
    EXVOC.takenAt,
    EXVOC.description,
])
def test_vocab_defines_property(vocab, prop):
    is_object    = (prop, RDF.type, OWL.ObjectProperty)   in vocab
    is_datatype  = (prop, RDF.type, OWL.DatatypeProperty) in vocab
    assert is_object or is_datatype, \
        f"Expected property {prop} to be declared in vocab.ttl"


# ── vocab.ttl: FOAF alignment ─────────────────────────────────────────────────

def test_student_subclass_of_foaf_person(vocab):
    assert (EXVOC.Student, RDFS.subClassOf, FOAF.Person) in vocab


def test_photo_subclass_of_foaf_image(vocab):
    assert (EXVOC.Photo, RDFS.subClassOf, FOAF.Image) in vocab


def test_depicts_subproperty_of_foaf_depicts(vocab):
    assert (EXVOC.depicts, RDFS.subPropertyOf, FOAF.depicts) in vocab


def test_photographer_subproperty_of_foaf_maker(vocab):
    assert (EXVOC.hasPhotographer, RDFS.subPropertyOf, FOAF.maker) in vocab


def test_title_subproperty_of_foaf_name(vocab):
    assert (EXVOC.title, RDFS.subPropertyOf, FOAF.name) in vocab


# ── data.ttl: syntax ─────────────────────────────────────────────────────────

def test_data_parses(data):
    """data.ttl must parse without errors and contain at least one triple."""
    assert len(data) > 0


# ── data.ttl: students ────────────────────────────────────────────────────────

@pytest.mark.parametrize("student,name", [
    (EX.me,       "Ali"),
    (EX.studentA, "Student A"),
    (EX.studentB, "Student B"),
])
def test_data_student_exists(data, student, name):
    assert (student, RDF.type, EXVOC.Student) in data, \
        f"Expected {student} to be typed as exvoc:Student"
    assert (student, FOAF.name, Literal(name)) in data, \
        f"Expected {student} to have foaf:name {name!r}"


def test_data_me_has_three_skills(data):
    skills = list(data.objects(EX.me, EXVOC.hasSkill))
    assert len(skills) == 3, f"Expected 3 skills for ex:me, got {len(skills)}"


def test_data_me_knows_two_students(data):
    known = list(data.objects(EX.me, FOAF.knows))
    assert len(known) == 2


# ── data.ttl: skills ─────────────────────────────────────────────────────────

@pytest.mark.parametrize("skill,label", [
    (EX.skillBash,   "BASH"),
    (EX.skillTS,     "TypeScript"),
    (EX.skillPython, "Python"),
])
def test_data_skill_exists(data, skill, label):
    assert (skill, RDF.type, EXVOC.Skill) in data, \
        f"Expected {skill} to be typed as exvoc:Skill"
    assert (skill, RDFS.label, Literal(label)) in data, \
        f"Expected {skill} to have rdfs:label {label!r}"


# ── data.ttl: locations ───────────────────────────────────────────────────────

@pytest.mark.parametrize("location,label", [
    (EX.locationAmsterdam,         "Amsterdam"),
    (EX.locationUniversityLibrary, "University Library"),
    (EX.locationUniversityGarden,  "University Garden"),
])
def test_data_location_exists(data, location, label):
    assert (location, RDF.type, EXVOC.Location) in data, \
        f"Expected {location} to be typed as exvoc:Location"
    assert (location, RDFS.label, Literal(label)) in data, \
        f"Expected {location} to have rdfs:label {label!r}"


# ── data.ttl: photos (count) ──────────────────────────────────────────────────

def test_data_has_exactly_three_photos(data):
    photos = list(data.subjects(RDF.type, EXVOC.Photo))
    assert len(photos) == 3, f"Expected 3 photos, got {len(photos)}"


@pytest.mark.parametrize("photo,title", [
    (EX.photoMe,         "Profile Photo of Ali"),
    (EX.photoGroupStudy, "Group Study Session"),
    (EX.photoCampus,     "Campus Walk"),
])
def test_data_photo_has_title(data, photo, title):
    assert (photo, RDF.type, EXVOC.Photo) in data, \
        f"Expected {photo} to be typed as exvoc:Photo"
    assert (photo, EXVOC.title, Literal(title)) in data, \
        f"Expected {photo} to have title {title!r}"


def test_photos_all_have_required_properties(data):
    """Every photo must have title, photographer, depicts, takenAt, and description."""
    photos = list(data.subjects(RDF.type, EXVOC.Photo))
    assert len(photos) == 3
    for photo in photos:
        assert len(list(data.objects(photo, EXVOC.title)))          == 1, f"{photo} missing title"
        assert len(list(data.objects(photo, EXVOC.hasPhotographer))) == 1, f"{photo} missing photographer"
        assert len(list(data.objects(photo, EXVOC.takenAt)))         == 1, f"{photo} missing takenAt"
        assert len(list(data.objects(photo, EXVOC.depicts)))         >= 1, f"{photo} missing depicts"
        assert len(list(data.objects(photo, EXVOC.description)))     == 1, f"{photo} missing description"


# ── data.ttl: photo-specific assertions ──────────────────────────────────────

def test_photo_me_photographer_and_location(data):
    assert (EX.photoMe, EXVOC.hasPhotographer, EX.studentA)       in data
    assert (EX.photoMe, EXVOC.takenAt,         EX.locationAmsterdam) in data
    assert (EX.photoMe, EXVOC.depicts,          EX.me)             in data


def test_group_study_depicts_three_people(data):
    depicted = list(data.objects(EX.photoGroupStudy, EXVOC.depicts))
    assert len(depicted) == 3
    assert EX.me       in depicted
    assert EX.studentA in depicted
    assert EX.studentB in depicted


def test_campus_walk_depicts_two_people(data):
    depicted = list(data.objects(EX.photoCampus, EXVOC.depicts))
    assert len(depicted) == 2
    assert EX.me       in depicted
    assert EX.studentB in depicted


# ── Combined graph: RDFS inference preconditions ──────────────────────────────

def test_combined_foaf_subproperty_declarations_present(combined):
    """
    Confirms the subPropertyOf triples required by the EYE N3 reasoning query
    (lab5-photos-query.n3) are present in the combined graph.  A reasoning engine
    applying RDFS rules will use these to derive foaf:depicts / foaf:Image triples.
    """
    assert (EXVOC.Photo,    RDFS.subClassOf,    FOAF.Image)   in combined
    assert (EXVOC.depicts,  RDFS.subPropertyOf, FOAF.depicts) in combined


def test_combined_depicts_triples_exist(combined):
    """
    Confirms there are exvoc:depicts triples in the data that the EYE reasoner
    will map to foaf:depicts via rdfs:subPropertyOf entailment.
    """
    triples = list(combined.subject_objects(EXVOC.depicts))
    assert len(triples) > 0, "Expected at least one exvoc:depicts triple"
