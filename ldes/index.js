const express = require('express');
const path = require('path');
const fsPromises = require('fs/promises');
const fs = require('fs');
const { DataFactory, StreamParser, Store, Writer } = require('n3');
const { quad, namedNode, blankNode, literal } = DataFactory;

const app = express();
const port = 3000;

const BASE_URL = "http://localhost:3000/ldes";

const RDF = "http://www.w3.org/1999/02/22-rdf-syntax-ns#";
const XSD = "http://www.w3.org/2001/XMLSchema#";
const TREE = "https://w3id.org/tree#";
const DCT = "http://purl.org/dc/terms/";

// State map that contains the set of available fragments
const fragments = new Map();

// Redirect to the first fragment (a.k.a tree:view)
app.get('/ldes', (req, res) => {
    const sortedFragments = Array.from(fragments.values()).sort((a, b) => a.lastModified - b.lastModified);

    // Handle trailing slash
    const redirectPath = req.url.endsWith('/')
        ? req.url + sortedFragments[0].name
        : req.url + '/' + sortedFragments[0].name

    res.redirect(redirectPath);
});

// Route handler for a specific fragment
app.get('/ldes/:fragment', async (req, res) => {

    // Check that the requested node exist in the data folder. Respond with a 404 otherwise.
    if (fragments.has(req.params.fragment)) {

        // Read the data file and parse its content into RDF-JS quads
        const fragmentName = fragments.get(req.params.fragment).name;
        const store = new Store();
        const rdfStream = fs.createReadStream(path.join(__dirname, 'data', fragmentName)).pipe(new StreamParser());
        for await (const quad of rdfStream) {
            store.addQuad(quad);
        }

        // Sort the fragments by last modified date
        const sortedFragments = Array.from(fragments.values()).sort((a, b) => a.lastModified - b.lastModified);
        // Get the index of the current fragment
        const index = sortedFragments.findIndex(f => f.name === fragmentName);

        // URL of the current and first fragments
        const currentFragmentUrl = `${BASE_URL}/${fragmentName}`;
        const firstFragmentUrl = `${BASE_URL}/${sortedFragments[0].name}`;

        // Add tree:view pointing to the first fragment
        store.addQuad(quad(
            namedNode(BASE_URL),
            namedNode(`${TREE}view`),
            namedNode(firstFragmentUrl)
        ));

        // Mark the current fragment as a tree:Node
        store.addQuad(quad(
            namedNode(currentFragmentUrl),
            namedNode(`${RDF}type`),
            namedNode(`${TREE}Node`)
        ));

        // Add tree:relation to the next fragment (if any) using the proper type (tree:GreaterThanRelation)
        // and value (see findGreaterThanValue function below).
        if (index < sortedFragments.length - 1) {
            const nextFragmentUrl = `${BASE_URL}/${sortedFragments[index + 1].name}`;
            const relationNode = blankNode();

            store.addQuad(quad(
                namedNode(currentFragmentUrl),
                namedNode(`${TREE}relation`),
                relationNode
            ));
            store.addQuad(quad(
                relationNode,
                namedNode(`${RDF}type`),
                namedNode(`${TREE}GreaterThanRelation`)
            ));
            store.addQuad(quad(
                relationNode,
                namedNode(`${TREE}node`),
                namedNode(nextFragmentUrl)
            ));
            store.addQuad(quad(
                relationNode,
                namedNode(`${TREE}path`),
                namedNode(`${DCT}modified`)
            ));
            store.addQuad(quad(
                relationNode,
                namedNode(`${TREE}value`),
                literal(findGreaterThanValue(store), namedNode(`${XSD}dateTime`))
            ));
        }

        // Set proper cache header ('Cache-Control: max-age=10' if this is the latest fragment
        // and 'Cache-Control: immutable' otherwise)
        if (index === sortedFragments.length - 1) {
            // This is the latest fragment
            res.set('Cache-Control', 'max-age=10');
        } else {
            // This is not the latest fragment
            res.set('Cache-Control', 'immutable');
        }

        // Serialize the store to Turtle and send the response
        res.set('Content-Type', 'text/turtle');
        const writer = new Writer({ format: 'text/turtle' });
        for (const q of store.getQuads(null, null, null, null)) {
            writer.addQuad(q);
        }
        writer.end((error, result) => {
            if (error) {
                res.status(500).send('Error serializing RDF');
            } else {
                res.send(result);
            }
        });

    } else {
        res.status(404).send('Not found');
        return;
    }
});

// Start HTTP server
app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}/`);
});

// Function to monitor the data folder and refresh the state array
fs.watch(path.join(__dirname, 'data'), updateState);

// Function to update the state array
async function updateState() {
    console.log("Storage state change detected!");
    const files = await fsPromises.readdir(path.join(__dirname, 'data'));

    for (const fileName of files) {
        // Read the last modified time of this file
        const lastModified = (await fsPromises.stat(path.join(__dirname, 'data', fileName))).mtimeMs;
        // Add it to the state map
        fragments.set(fileName, { name: fileName, lastModified });
    }
}

// Function to extract the member timestamps from a RDF-JS Store and return the most recent one
function findGreaterThanValue(store) {
    const values = store.getQuads(null, namedNode(`${DCT}modified`), null, null).map(q => {
        return new Date(q.object.value).getTime();
    });

    values.sort((a, b) => b - a);
    return new Date(values[0]).toISOString();
}

// Initialize the state array at start up
updateState();
