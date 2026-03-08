# Assignment: Vocabulary Creation, Data Publication, and Technical Analysis

## 1. Vocabulary Definition

The following vocabulary was created to describe students, their identifiers, and their skills.

```ttl
@prefix exvoc: <https://aliassheikh.github.io/KnowledgeGraph/vocab#> .
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

curl -I https://aliassheikh.github.io/KnowledgeGraph/data.ttl

HTTP/2 200 
server: GitHub.com
content-type: text/turtle; charset=utf-8
last-modified: Sun, 08 Mar 2026 08:24:17 GMT
access-control-allow-origin: *
strict-transport-security: max-age=31556952
etag: "69ad3231-2c8"
expires: Sun, 08 Mar 2026 08:35:46 GMT
cache-control: max-age=600
x-proxy-cache: MISS
x-github-request-id: 9569:644BE:21FAE35:2263EB7:69AD328A
accept-ranges: bytes
age: 0
date: Sun, 08 Mar 2026 08:25:46 GMT
via: 1.1 varnish
x-served-by: cache-ams2100087-AMS
x-cache: MISS
x-cache-hits: 0
x-timer: S1772958347.597178,VS0,VE109
vary: Accept-Encoding
x-fastly-request-id: bed67b6fd065aec9290c6b9667228e59346ee081
content-length: 712
