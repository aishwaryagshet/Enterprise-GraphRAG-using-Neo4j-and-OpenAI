from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()


client=OpenAI()
from rag.query_generator import execute_neo4j_query
from graph.cypher_generator import query_neo4j_graph
from graph.format import strip_markdown_code_blocks
# Function to perform RAG query


def rag_query(user_query):
    """
    Perform a RAG query using Neo4j and  OpenAI
    
    Args:
        user_query: User's natural language query
    
    Returns:
        Answer to the user's query
    """
    # Generate Cypher query from user query
    cypher_query = query_neo4j_graph(user_query)
    
    # Clean the query
    clean_query = strip_markdown_code_blocks(cypher_query)
    
    # Execute the query
    results = execute_neo4j_query(clean_query)
    
    # Format the results for the LLM
    def json_to_text(obj, prefix=""):
        lines = []

        if isinstance(obj, dict):
            for key, value in obj.items():
                new_prefix = f"{prefix}.{key}" if prefix else key
                lines.extend(json_to_text(value, new_prefix))

        elif isinstance(obj, list):
            for item in obj:
                lines.extend(json_to_text(item, prefix))

        else:
            lines.append(f"{prefix}: {obj}")

        return lines

    formatted_results = "\n".join(json_to_text(results))
    print(formatted_results)  
    print(cypher_query)  
    
    # Generate answer using Azure OpenAI
    system_prompt = f"""You are a Neo4j GraphRAG assistant.

The Cypher query explains the meaning of the returned records.

Interpret the query first.

Example:

Cypher:
MATCH (h:Hotel)-[:has_customers]-(c:CustomerType {{name:'Businessmen'}})
RETURN h

Results:
h.name: Creek Hotel

Reasoning:
The query asks for hotels connected to CustomerType='Businessmen'.
The result shows Creek Hotel.
Therefore Creek Hotel is visited by Businessmen.

Use this same reasoning process for every query.
    """
    
    user_prompt = f"""Question:
{user_query}

Cypher Query:
{cypher_query}

Returned Records:
{formatted_results}

First understand what the Cypher query is searching for.
Then interpret the returned records using that meaning.
Finally answer the question.
    """
    try:
        response = client.chat.completions.create(
            model = "gpt-4o-mini",
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7
        )
        print(response.choices[0].message.content)
    
        return response.choices[0].message.content
    except Exception as e:
        print("error - ", str(e))
        return str(e)
    