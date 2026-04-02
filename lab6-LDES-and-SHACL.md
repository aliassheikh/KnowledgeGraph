# Assessment of the LDES + SHACL Lab 

## Files structure

```Code
In the folder lab6:

ldes/
├── index.js                ← the completed Express server
├── package.json            ← npm dependencies declaration
├── package-lock.json       ← exact dependency versions (good to include)
└── data/
    ├── node_0.ttl          ← fragment 0 (John v0, v1)
    └── node_1.ttl          ← fragment 1 (John v2, v3)
    └── node_2.ttl          ← fragment 2 (John v4, v5)

shacl/
├── shape.ttl               ← SHACL constraints
├── rdfc-pipeline.ttl       ← RDF-Connect validation pipeline
└── package.json            ← pipeline dependencies
```

## Test LDES
### Run the script
```Bash
> cd /home/work/git/practice/rdf/lab6/ldes
lab6/ldes> npm install && node index.js
```

If you see `high severity vulnerability` then run:
```Bash
lab6/ldes> npm audit fix
lab6/ldes> npm install && node index.js
```
### Check the web

Open a browser and navigate to: http://localhost:3000/ldes\node_0.ttl
==>
```
<http://localhost:3000/ldes> a <https://w3id.org/ldes#EventStream>;
    <https://w3id.org/ldes#timestampPath> <http://purl.org/dc/terms/modified>;
    <https://w3id.org/ldes#versionOfPath> <http://purl.org/dc/terms/isVersionOf>;
    <https://w3id.org/tree#member> <https://persons.org/john/v0>, <https://persons.org/john/v1>;
    <https://w3id.org/tree#view> <http://localhost:3000/ldes/node_0.ttl>.
<https://persons.org/john/v0> a <http://www.w3.org/ns/person#Person>;
    <http://purl.org/dc/terms/modified> "1989-06-27T17:00:00.000Z"^^<http://www.w3.org/2001/XMLSchema#dateTime>;
    <http://purl.org/dc/terms/isVersionOf> <https://persons.org/john>;
    <http://www.w3.org/ns/person#birthName> "John Doe"@en;
    <http://purl.org/dc/terms/alternativeName> "Johnny Doe"@en;
    <http://data.europa.eu/m8g/domicile> _:n3-5;
    <http://www.w3.org/ns/person#residency> _:n3-6.
<https://persons.org/john/v1> a <http://www.w3.org/ns/person#Person>;
    <http://purl.org/dc/terms/modified> "2012-08-01T00:00:00.000Z"^^<http://www.w3.org/2001/XMLSchema#dateTime>;
    <http://purl.org/dc/terms/isVersionOf> <https://persons.org/john>;
    <http://www.w3.org/ns/person#birthName> "John Doe"@en;
    <http://purl.org/dc/terms/alternativeName> "Johnny Doe"@en;
    <http://data.europa.eu/m8g/domicile> _:n3-7;
    <http://www.w3.org/ns/person#residency> _:n3-8.
_:n3-5 a <http://www.w3.org/ns/locn#Address>;
    <http://www.w3.org/ns/locn#fullAddress> "123 Main St";
    <http://www.w3.org/ns/locn#postName> "Ghent"@en.
_:n3-6 a <http://purl.org/dc/terms/Jurisdiction>;
    <http://purl.org/dc/terms/id> <http://publications.europa.eu/resource/authority/country/BEL>;
    <http://www.w3.org/2000/01/rdf-schema#label> "Belgium"@en.
_:n3-7 a <http://www.w3.org/ns/locn#Address>;
    <http://www.w3.org/ns/locn#fullAddress> "Avenida de Betanzos 79";
    <http://www.w3.org/ns/locn#postName> "Madrid"@es.
_:n3-8 a <http://purl.org/dc/terms/Jurisdiction>;
    <http://purl.org/dc/terms/id> <http://publications.europa.eu/resource/authority/country/ESP>;
    <http://www.w3.org/2000/01/rdf-schema#label> "Spain"@en.
<http://localhost:3000/ldes/node_0.ttl> a <https://w3id.org/tree#Node>;
    <https://w3id.org/tree#relation> _:n3-9.
_:n3-9 a <https://w3id.org/tree#GreaterThanRelation>;
    <https://w3id.org/tree#node> <http://localhost:3000/ldes/node_1.ttl>;
    <https://w3id.org/tree#path> <http://purl.org/dc/terms/modified>;
    <https://w3id.org/tree#value> "2012-08-01T00:00:00.000Z"^^<http://www.w3.org/2001/XMLSchema#dateTime>.
```
***

## Test SHACL
While the http://localhost:3000/ldes is running,
### run in your terminal:

```Bash
> cd /home/work/git/practice/rdf/lab6/shacle
lab6/shacl> npm install && npx rdfc rdfc-pipeline.ttl
```
==>
```
up to date, audited 1406 packages in 7s

224 packages are looking for funding
  run `npm fund` for details

46 high severity vulnerabilities

To address all issues, run:
  npm audit fix

Run `npm audit` for details.
E No address added out of total 1 resolved
2026-04-02T15:23:08.766Z [start] info: Grpc server is bound! localhost:50051
2026-04-02T15:23:08.795Z [rdfc:NodeRunner, CommandInstantiator] info: debug msg should follow
```
