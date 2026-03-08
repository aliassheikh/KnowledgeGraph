# # Assignment: Vocabulary Creation, Data Publication, and Technical Analysis 

My `KnowledgeGraph` repository including:

- A custom **RDF vocabulary** (`vocab.ttl`)
- A corresponding **RDF dataset** (`data.ttl`)
- Publication of both files using **GitHub Pages**

The project demonstrates how to design a small ontology, reuse it in a dataset, and publish both resources as Linked Data on the Web.

---

## Vocabulary (`vocab.ttl`)

The vocabulary defines:

### **Classes**
- `Student`
- `Skill`

### **Properties**
- `hasSkill` — links a student to a skill  
- `studentId` — a literal identifier for a student  

Vocabulary URL: **https://aliassheikh.github.io/KnowledgeGraph/vocab.ttl**

This file is served with the correct MIME type (`text/turtle`) and can be parsed by [rdf.ply](https://rdf-play.rubensworks.net/).

---

## Dataset (`data.ttl`)

The dataset uses the vocabulary to describe:

- A student (“Ali”)  
- Their skills (BASH, TypeScript, Python)  
- Their connections to other students  

Dataset URL:  **https://aliassheikh.github.io/KnowledgeGraph/data.ttl**

This file is also served as `text/turtle` and is fully parseable.

---

## GitHub Pages Publication

GitHub Pages is used to publish both RDF files as real web resources.  
This ensures:

- Correct content type (`text/turtle`)
- HTTPS access
- CORS enabled (`access-control-allow-origin: *`)
- Caching and CDN optimization
- Compatibility with Linked Data tools

Both files return **HTTP/2 200**, confirming successful publication.

---

## Testing

The URLs were tested using:

- `curl -I` to inspect HTTP headers  
- **rdf‑play** to validate RDF parsing (RDF Quads: 18)  

Both files load correctly and behave as expected for Linked Data resources.

1. `curl -I` `data.ttl`
```BASH
curl -I https://aliassheikh.github.io/KnowledgeGraph/data.ttl
```
```BASH
HTTP/2 200 
server: GitHub.com
content-type: text/turtle; charset=utf-8

last-modified: Sun, 08 Mar 2026 08:28:12 GMT
access-control-allow-origin: *
strict-transport-security: max-age=31556952
etag: "69ad331c-2c6"
expires: Sun, 08 Mar 2026 08:39:21 GMT
cache-control: max-age=600
x-proxy-cache: MISS
x-github-request-id: 402E:1426:D91019:DBE72C:69AD3361
accept-ranges: bytes
age: 0
date: Sun, 08 Mar 2026 08:29:21 GMT
via: 1.1 varnish
x-served-by: cache-ams21021-AMS
x-cache: MISS
x-cache-hits: 0
x-timer: S1772958562.846106,VS0,VE109
vary: Accept-Encoding
x-fastly-request-id: 1c20e44185135b0959f713348a06d92bffe0f80b
content-length: 710
```
2. `curl -I` `vocabs.ttl`
```BASH
curl -I https://aliassheikh.github.io/KnowledgeGraph/vocab.ttl
```
```BASH
curl -I https://aliassheikh.github.io/KnowledgeGraph/vocab.ttl
HTTP/2 200 
server: GitHub.com
content-type: text/turtle; charset=utf-8
last-modified: Sun, 08 Mar 2026 08:29:35 GMT
access-control-allow-origin: *
strict-transport-security: max-age=31556952
etag: "69ad336f-334"
expires: Sun, 08 Mar 2026 08:40:40 GMT
cache-control: max-age=600
x-proxy-cache: MISS
x-github-request-id: 97BC:2E7B21:2155C84:21BEC96:69AD33B0
accept-ranges: bytes
age: 0
date: Sun, 08 Mar 2026 08:30:40 GMT
via: 1.1 varnish
x-served-by: cache-ams21039-AMS
x-cache: MISS
x-cache-hits: 0
x-timer: S1772958640.179924,VS0,VE107
vary: Accept-Encoding
x-fastly-request-id: ac9206c7b8c6a4e34441d90b4a032411b492097d
content-length: 820
```

3. rdf-ply `data-ttl`
 https://rdf-play.rubensworks.net#url=https://aliassheikh.github.io/KnowledgeGraph/data.ttl
 ```RDF
<https://aliassheikh.github.io/KnowledgeGraph/data#me> a <https://aliassheikh.github.io/KnowledgeGraph/vocab#Student>;
    <http://xmlns.com/foaf/0.1/name> "Ali";
    <https://aliassheikh.github.io/KnowledgeGraph/vocab#studentId> "1234567";
    <https://aliassheikh.github.io/KnowledgeGraph/vocab#hasSkill> <https://aliassheikh.github.io/KnowledgeGraph/data#skillBash>, <https://aliassheikh.github.io/KnowledgeGraph/data#skillTS>, <https://aliassheikh.github.io/KnowledgeGraph/data#skillPython>;
    <http://xmlns.com/foaf/0.1/knows> <https://aliassheikh.github.io/KnowledgeGraph/data#studentA>, <https://aliassheikh.github.io/KnowledgeGraph/data#studentB>.
<https://aliassheikh.github.io/KnowledgeGraph/data#studentA> a <https://aliassheikh.github.io/KnowledgeGraph/vocab#Student>;
    <http://xmlns.com/foaf/0.1/name> "Student A".
<https://aliassheikh.github.io/KnowledgeGraph/data#studentB> a <https://aliassheikh.github.io/KnowledgeGraph/vocab#Student>;
    <http://xmlns.com/foaf/0.1/name> "Student B".
<https://aliassheikh.github.io/KnowledgeGraph/data#skillBash> a <https://aliassheikh.github.io/KnowledgeGraph/vocab#Skill>;
    <http://www.w3.org/2000/01/rdf-schema#label> "BASH".
<https://aliassheikh.github.io/KnowledgeGraph/data#skillTS> a <https://aliassheikh.github.io/KnowledgeGraph/vocab#Skill>;
    <http://www.w3.org/2000/01/rdf-schema#label> "TypeScript".
<https://aliassheikh.github.io/KnowledgeGraph/data#skillPython> a <https://aliassheikh.github.io/KnowledgeGraph/vocab#Skill>;
    <http://www.w3.org/2000/01/rdf-schema#label> "Python".
```

