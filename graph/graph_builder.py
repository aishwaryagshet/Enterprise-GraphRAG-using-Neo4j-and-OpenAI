import json
import os
from dotenv import load_dotenv
from openai import OpenAI

from neo4j import GraphDatabase
import pandas as pd
import numpy as np
from graph.cypher_generator import identify_relationships_and_nodes,generate_cypher_for_node_creation, node_creation_cypher_list
from graph.format import strip_markdown_code_blocks
import plotly.graph_objs as go

# Load environment variables
load_dotenv()


client=OpenAI()


# Function to create the knowledge graph in Neo4j
def create_knowledge_graph(hotel_reviews):
    """
    Create a knowledge graph in Neo4j from hotel reviews
    
    Args:
        hotel_reviews: List of hotel review texts
    """
    # Process each hotel review
    for review in hotel_reviews:
        # Identify relationships and nodes
        ontology = identify_relationships_and_nodes(review)
        
        # Generate Cypher query for node creation
        cypher_query = generate_cypher_for_node_creation(ontology)
    
    # Connect to Neo4j and create the graph
    uri = os.getenv("NEO4J_URI")
    #url = f"neo4j+s://{uri}.databases.neo4j.io"
    neo4j_username = os.getenv("NEO4J_USERNAME")
    neo4j_password = os.getenv("NEO4J_PASSWORD")
    
    driver = GraphDatabase.driver(uri, auth=(neo4j_username, neo4j_password))
    
    with driver.session() as session:
        for cypher_query in node_creation_cypher_list:
            # Remove markdown code block markers
            clean_query = strip_markdown_code_blocks(cypher_query)
            try:
                session.run(clean_query)
                print(f"Executed: {clean_query}")
            except Exception as e:
                print(f"Error executing query: {e}")
                print(f"Failed query: {clean_query}")