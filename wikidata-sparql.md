# Assignment: SPARQL Queries on Wikidata

This document contains SPARQL queries written for [Wikidata Query Service](https://query.wikidata.org), along with explanations of the approach.

---

## Task 1 — Railway Stations in the Netherlands with Rijksmonument Designation

### Question

Select all railway stations in the Netherlands that have the **"Rijksmonument"** as heritage designation (`P1435`).

### SPARQL Query

```sparql
SELECT ?station ?stationLabel WHERE {
  ?station wdt:P31  wd:Q55488   .  # instance of: railway station
  ?station wdt:P17  wd:Q55      .  # country: Netherlands
  ?station wdt:P1435 wd:Q916333 .  # heritage designation: Rijksmonument

  SERVICE wikibase:label {
    bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en".
  }
}
ORDER BY ?stationLabel
```

### Explanation

| Clause | Meaning |
|--------|---------|
| `wdt:P31 wd:Q55488` | The item must be an *instance of* (`P31`) a **railway station** (`Q55488`) |
| `wdt:P17 wd:Q55` | The item must have **country** (`P17`) set to **Netherlands** (`Q55`) |
| `wdt:P1435 wd:Q916333` | The item must have **heritage designation** (`P1435`) set to **Rijksmonument** (`Q916333`) |
| `SERVICE wikibase:label` | A Wikidata-specific service that automatically fetches human-readable labels in the preferred language |

The `wdt:` prefix refers to *direct* (simple) property statements, and `wd:` refers to Wikidata entity URIs.

---

## Task 2 — Count All Rijksmonumenten in the Netherlands, Grouped by Type

### Question

Count all **Rijksmonumenten** in the Netherlands, grouped by their type (`instance of`, `P31`). Include the type labels.

### SPARQL Query

```sparql
SELECT ?type ?typeLabel (COUNT(?item) AS ?count) WHERE {
  ?item wdt:P1435 wd:Q916333 .  # heritage designation: Rijksmonument
  ?item wdt:P17   wd:Q55     .  # country: Netherlands
  ?item wdt:P31   ?type      .  # instance of: (any type, captured in ?type)

  SERVICE wikibase:label {
    bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en".
  }
}
GROUP BY ?type ?typeLabel
ORDER BY DESC(?count)
```

### Explanation

| Clause | Meaning |
|--------|---------|
| `wdt:P1435 wd:Q916333` | Filter to items whose heritage designation is Rijksmonument |
| `wdt:P17 wd:Q55` | Filter to items located in the Netherlands |
| `wdt:P31 ?type` | Bind the *instance of* value to variable `?type` (one row per type) |
| `COUNT(?item)` | Count the number of items per type |
| `GROUP BY ?type ?typeLabel` | Group the aggregated results by type URI and its label |
| `ORDER BY DESC(?count)` | Show the most common types first |

### Expected Result

The most common type is likely **building** (`Q41176`) or a closely related type such as **house** or **farm** (`boerderij`). Windmills, castles, and museums do appear in the results, but the Netherlands has tens of thousands of Rijksmonumenten, the vast majority of which are ordinary historical buildings. Windmills are iconic, but they represent only a small fraction.

---

## How Were the Right URIs Found?

### Step 1 — Search Wikidata directly

Using the [Wikidata entity search](https://www.wikidata.org/w/index.php?search=) or the autocomplete in the query editor, you can type a term (e.g. *railway station*, *Netherlands*, *Rijksmonument*) to find the matching Q-identifier.

### Step 2 — Use the Wikidata Query Service examples

The **Examples** menu at <https://query.wikidata.org> contains ready-made queries (e.g. "Cats", "Largest cities", "Mayors"). These show how properties such as `P31` (instance of), `P17` (country), and `P1435` (heritage designation) are used in practice, which makes it straightforward to adapt them for this task.

### Step 3 — Inspect property pages

Each property has a dedicated page, for example:

- [`P1435` — heritage designation](https://www.wikidata.org/wiki/Property:P1435)
- [`P31` — instance of](https://www.wikidata.org/wiki/Property:P31)
- [`P17` — country](https://www.wikidata.org/wiki/Property:P17)

These pages list usage examples and the expected value types, making it easy to confirm you are using the right URI.

### Step 4 — Verify entity pages

Visiting a known Rijksmonument on Wikidata (e.g. [Amsterdam Centraal station](https://www.wikidata.org/wiki/Q27670)) lets you read off the exact property values that are stored, which can then be copied into your query.

---

## Is the List Complete? — The Open World Assumption

### The Open World Assumption (OWA)

In classical databases (and everyday reasoning), we often apply the **Closed World Assumption (CWA)**: if something is not recorded, it is assumed to be false. Wikidata — and Linked Data in general — uses the **Open World Assumption (OWA)** instead:

> *The absence of information does not imply falsehood.*

This means: if a Rijksmonument is **not** in Wikidata, or its `P1435` property has not been filled in, the query will simply not return it — but that does **not** mean it is not a Rijksmonument in the real world.

### Why the list is not necessarily complete

1. **Missing items**: Not every Rijksmonument has a Wikidata entry yet. With more than 60,000 Rijksmonumenten in the Netherlands, manual and automated data imports are ongoing and may be incomplete.
2. **Missing statements**: An item may exist in Wikidata but lack the `P1435` or `P17` property, so it would be invisible to our query.
3. **Incorrect or outdated data**: Designations may have changed, and Wikidata might not reflect the current status.

### How to Guarantee a More Complete List

- **Compare with the authoritative source**: The Dutch Cultural Heritage Agency (Rijksdienst voor het Cultureel Erfgoed, RCE) maintains the official register of Rijksmonumenten at <https://cultureelerfgoed.nl>. Cross-referencing Wikidata with the RCE register (e.g. via the Rijksmonument ID property `P359`) would reveal gaps.
- **Use `P359` (Rijksmonument ID)**: Querying for items that have a Rijksmonument ID (`?item wdt:P359 ?id`) is more reliable than querying on `P1435`, because the ID comes from the official register and is more systematically added.
- **WikiProject monitoring**: Active Wikidata WikiProjects (e.g. WikiProject Netherlands) periodically import data from official sources to improve coverage.
- **Federated queries**: A SPARQL `SERVICE` call to an RCE SPARQL endpoint (if available) could combine both datasets in one query to find items missing from Wikidata.
