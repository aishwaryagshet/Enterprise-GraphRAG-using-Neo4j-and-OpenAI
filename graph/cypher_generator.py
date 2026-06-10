# Function to generate Cypher query for node creation

from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()


client=OpenAI()


# Initialize lists to store data
ontology_list = []
node_creation_cypher_list = []

# Function to identify relationships and nodes
def identify_relationships_and_nodes(file_text):
    
    system_prompt = f"""Assistant is a Named Entity Recognition (NER) expert. The assistant can identify named entities 
    such as a person, place, or thing. The assistant can also identify entity relationships, which describe
    how entities relate to each other (eg: married to, located in, held by). Identify the named entities
    and the entity relationships present in the text by returning comma separated list of tuples
    representing the relationship between two entities in the format (entity, relationship, entity). Only
    generate tuples from the list of entities and the possible entity relationships listed below. Return
    only generated tuples in a comma separated tuple separated by a new line for each tuple.

    Entities:
    - Hotel
    - Location
    - Facilities
    - CustomerType
    - Reviewer

    Relationships:
    - [Hotel],is_located_in,[Location]
    - [Hotel],has_facilities,[Facilities]
    - [Hotel],has_customers,[CustomerType]
    - [Hotel],has_reviewer,[Reviewer]

    Example Output:
    Creek Hotel,is_located_in,Dubai
    Creek Hotel,has_facilities,swimming pool
    Creek Hotel,has_customers,Businessmen
    Creek Hotel,has_customers,senior citizens
    Creek Hotel,has_reviewer,John Doe

    """

    user_prompt = f"""Identify the named entities and entity relationships in the hotel review text above. Return the
    entities and entity relationships in a tuple separated by commas. Return only generated tuples in a
    comma separated tuple separated by a new line for each tuple.

    Text: {file_text}"""

    chat_completions_response = client.chat.completions.create(
        model = "gpt-4o-mini",
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0
    )
    
    ontology_list.append(chat_completions_response.choices[0].message.content)

    print(chat_completions_response.choices[0].message.content)
    return chat_completions_response.choices[0].message.content

def generate_cypher_for_node_creation(ontology_text):
    cypher_system_prompt = f""" Assistant is an expert in Neo4j Cypher development. Create a cypher query to generate a graph using the data points provided. 
    make sure to only include the cypher query in your response so that I can directly send this cypher query to the Neo4j database API endpoint
    via a POST request. The data is in the format of a comma separated tuple separated by a new line for each tuple.

    """
    
    cypher_user_prompt = f"""Generate a cypher query to create new nodes and their relationships given the data provided. Return only the cypher query. 
    Data is composed of relationships between entities that have been extracted using NER.
    The data is in the format of a comma separated tuple separated by a new line for each tuple.
    
    Example Input: 
    Creek Hotel,is_located_in,Dubai
    Creek Hotel,has_customers,businessmen
    Creek Hotel,has_customers,tourists
    Creek Hotel,has_reviewer,Ryouta Sato
    Creeh Hotel,has_facilities,swimming pool

    Example Output:
    MERGE (ch:Hotel {{name: 'Creek Hotel'}})-[:is_located_in]->(d:Location {{name: 'Dubai'}}),
        (ch)-[:has_customers]->(b:CustomerType {{name: 'businessmen'}}),
        (ch)-[:has_customers]->(t:CustomerType {{name: 'tourists'}}),
        (ch)-[:has_reviewer]->(rs:Reviewer {{name: 'Ryouta Sato'}}),
        (ch)-[:has_facilities]->(sp:Facilities {{name: 'swimming pool'}})
        
    strictly stick to the above output format
    
    use distinct variable names for each node and relationship to avoid conflicts

    the data is: {ontology_text}

    """

    
    cypher_query = client.chat.completions.create(
        model = "gpt-4o-mini",
        messages = [
            {"role": "system", "content": cypher_system_prompt},
            {"role": "user", "content": cypher_user_prompt}
        ],
        temperature=0
    )
    
    node_creation_cypher_list.append(cypher_query.choices[0].message.content)

    print(cypher_query.choices[0].message.content)
    return cypher_query.choices[0].message.content




# Function to query Neo4j graph
def query_neo4j_graph(user_query):
    query_with_cypher_system_prompt = f"""Assistant is an expert in Neo4j Cypher development. Only return a cypher query based on the user query
    the cypher graph has the following schema:

    Nodes:
    - Hotel
    - Location
    - Facilities
    - CustomerType
    - Reviewer

    Relationships:
    - [Hotel],is_located_in,[Location]
    - [Hotel],has_facilities,[Facilities]
    - [Hotel],has_customers,[CustomerType]
    - [Hotel],has_reviewer,[Reviewer]

    example of a node created through cypher query:
    {node_creation_cypher_list[0] if node_creation_cypher_list else ""}
    
    Example Input:
    what hotels are reviewed by Ryouta Sato?
    
    Example Output:
    MATCH (h:Hotel)-[:has_reviewer]-(r:Reviewer {{name: 'Ryouta Sato'}})
    RETURN h

    stick strictly to the above output format
    """

    query_with_cypher_user_prompt = f"""Generate a cypher query to answer the user query.
    user_query = {user_query}"""
    
    query_response = client.chat.completions.create(
        model = "gpt-4o-mini",
        messages = [
            {"role": "system", "content": query_with_cypher_system_prompt},
            {"role": "user", "content": query_with_cypher_user_prompt}
        ],
        temperature=0
    )    
    
    cypher_query_for_retrieval = query_response.choices[0].message.content
    
    print(cypher_query_for_retrieval)
    
    return cypher_query_for_retrieval