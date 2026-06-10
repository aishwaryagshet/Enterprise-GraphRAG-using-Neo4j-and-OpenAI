# Enterprise-GraphRAG-using-Neo4j-and-OpenAI
End-to-end GraphRAG pipeline using Neo4j and GPT-4o that converts unstructured hotel reviews into a knowledge graph, generates Cypher from natural language, performs graph-based retrieval, and delivers explainable answers through a Dash dashboard.

# Neo4j GraphRAG Knowledge Assistant

An end-to-end Graph Retrieval-Augmented Generation (GraphRAG) system that transforms unstructured hotel reviews into a Neo4j Knowledge Graph and enables natural language querying using OpenAI GPT-4o.

## Features

* Named Entity Recognition using GPT-4o
* Relationship extraction from natural language
* Automatic Cypher query generation
* Neo4j Knowledge Graph creation
* Natural Language to Cypher conversion
* Graph-based retrieval
* LLM-powered answer generation
* Interactive Dash visualization dashboard

## Architecture

Hotel Reviews
→ Entity & Relationship Extraction
→ Cypher Generation
→ Neo4j Knowledge Graph
→ Natural Language Query
→ Cypher Query Generation
→ Graph Retrieval
→ OpenAI Answer Generation

## Example Query

Question:

Which hotels are visited by businessmen?

Generated Cypher:

MATCH (h:Hotel)-[:has_customers]-(c:CustomerType {name:'Businessmen'})
RETURN h

Answer:

Creek Hotel is visited by businessmen.

## Technologies Used

* Python
* OpenAI GPT-4o
* Neo4j
* Cypher
* Dash
* Plotly
* Pandas

## Installation

git clone <repository>

pip install -r requirements.txt

Create .env file:

OPENAI_API_KEY=

NEO4J_URI=

NEO4J_USERNAME=

NEO4J_PASSWORD=

Run:

python app.py

## Future Improvements

* GraphRAG with embeddings
* Nodes representation in dashboard instaed of table
* Structured output extraction
* Agentic Cypher generation
* Support for multiple domains

