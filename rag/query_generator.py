from neo4j import GraphDatabase
import os
# Function to execute Neo4j query and return results
def execute_neo4j_query(cypher_query):
    uri = os.getenv("NEO4J_URI")
    #url = f"neo4j+s://{uri}.databases.neo4j.io"
    neo4j_username = os.getenv("NEO4J_USERNAME")
    neo4j_password = os.getenv("NEO4J_PASSWORD")
    
    driver = GraphDatabase.driver(uri, auth=(neo4j_username, neo4j_password))
    
    with driver.session() as session:
        # Run the Cypher query
        result = session.run(cypher_query)
        
        # Extract and return results
        records = [record.data() for record in result]
        print(records)
        return records