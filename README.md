# bdacaII_knowledge_extraction 

This GitHub page is part of an assignment of the course Big Data II of the University of Amsterdam, and consists of the following steps:

The Knowledge Extraction Pipeline Core Stages:
1. Data Collection → Gathering raw data from sources
2. Preprocessing → Cleaning, tokenization, normalization
3. Extraction → Identifying entities, relationships, attributes
4. Representation → Structuring knowledge (graphs, triples, ontologies)
5. Validation & Refinement → Quality assurance, disambiguation

We will examine gender representation among current state leaders using the Wikipedia page “List of current heads of state and government” as our entry point. The research questions are as follows:

1. What is the gender distribution of current state leaders globally?
2. Are there differences in Wikipedia visibility between male and female leaders (e.g., page length, references, cross-language presence)?

## Entity Extraction (Named Entity Recognition):
- Entity Extraction (Named Entity Recognition): Identifying and classifying entities: persons, organizations, locations and dates
- Relation Extraction: Discovering relationships between entities (e.g., "works_at", "founded_by")
- Attribute Extraction: Extracting properties of entities (birth date, population, height)

## Knowledge Representation
Triples (Subject-Predicate-Object):
- "Barack Obama" → "was_president_of" → "United States"
- Foundation of knowledge graphs
- Standard format: RDF (Resource Description Framework)

### Knowledge Graphs:
- Networks of entities connected by relationships
- Example: DBpedia, Wikidata, Google Knowledge Graph

### Ontologies:
- Formal specifications of concepts and relationships in a domain

# Authors: