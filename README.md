# Assignment: Vocabulary Creation, Data Publication, and Technical Analysis

## 1. Vocabulary Definition

The following vocabulary was created to describe students, their identifiers, and their skills.

```ttl
@prefix exvoc: <https://github.com/aliassheikh/KnowledgeGraph/blob/main/vocab#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl:  <http://www.w3.org/2002/07/owl#> .

### Classes
exvoc:Student a rdfs:Class ;
    rdfs:label "Student" ;
    rdfs:comment "A person enrolled in an educational program." .

exvoc:Skill a rdfs:Class ;
    rdfs:label "Skill" ;
    rdfs:comment "A technical or academic skill." .

### Properties
exvoc:hasSkill a owl:ObjectProperty ;
    rdfs:label "has skill" ;
    rdfs:comment "Links a student to a skill they possess." ;
    rdfs:domain exvoc:Student ;
    rdfs:range exvoc:Skill .

exvoc:studentId a owl:DatatypeProperty ;
    rdfs:label "student identifier" ;
    rdfs:comment "A unique identifier for a student." ;
    rdfs:domain exvoc:Student ;
    rdfs:range rdfs:Literal .

curl -I https://github.com/aliassheikh/KnowledgeGraph/blob/main/data.ttl

HTTP/2 200 
date: Thu, 05 Mar 2026 13:35:32 GMT
content-type: text/html; charset=utf-8
vary: X-PJAX, X-PJAX-Container, Turbo-Visit, Turbo-Frame, X-Requested-With, Sec-Fetch-Site,Accept-Encoding, Accept, X-Requested-With
x-repository-download: git clone https://github.com/aliassheikh/KnowledgeGraph.git
x-raw-download: https://raw.githubusercontent.com/aliassheikh/KnowledgeGraph/main/data.ttl
etag: W/"f0606487563f5bd198ec8799eb1982df"
cache-control: max-age=0, private, must-revalidate
strict-transport-security: max-age=31536000; includeSubdomains; preload
x-frame-options: deny
x-content-type-options: nosniff
x-xss-protection: 0
referrer-policy: no-referrer-when-downgrade
