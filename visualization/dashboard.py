from rag.retrieval import rag_query
from dotenv import load_dotenv
from openai import OpenAI

from neo4j import GraphDatabase
import pandas as pd
import numpy as np
import dash
from dash import dcc, html
import plotly.graph_objs as go

# Load environment variables
load_dotenv()


client=OpenAI()
# Create a Dash app for visualization
def create_visualization_app(neo4j_uri, neo4j_username, neo4j_password):
    """
    Create a Dash app for visualizing the knowledge graph
    """
    app = dash.Dash(__name__)
    
    # Connect to Neo4j
    url=neo4j_uri
    #url = f"neo4j+s://{neo4j_uri}.databases.neo4j.io"
    driver = GraphDatabase.driver(url, auth=(neo4j_username, neo4j_password))
    
    # Get all nodes and relationships
    with driver.session() as session:
        # Get hotels
        hotels_result = session.run("MATCH (h:Hotel) RETURN h.name as name")
        hotels = [record["name"] for record in hotels_result]
        
        # Get all relationships
        relationships_result = session.run("""
            MATCH (h:Hotel)-[r]->(n)
            RETURN h.name as hotel, type(r) as relation, labels(n)[0] as node_type, n.name as related_entity
        """)
        
        relationships_data = [
            {
                "hotel": record["hotel"],
                "relation": record["relation"],
                "node_type": record["node_type"],
                "related_entity": record["related_entity"]
            }
            for record in relationships_result
        ]
    
    # Convert to DataFrame for easier manipulation
    df = pd.DataFrame(relationships_data)
    
    # Create network graph
    def create_network_graph():
        # Create nodes
        nodes = []
        node_colors = {
            "Hotel": "red",
            "Location": "blue",
            "Facilities": "green",
            "CustomerType": "purple",
            "Reviewer": "orange"
        }
        
        # Add hotel nodes
        for hotel in hotels:
            nodes.append({
                "id": hotel,
                "label": hotel,
                "color": node_colors["Hotel"]
            })
        
        # Add other nodes
        for _, row in df.iterrows():
            nodes.append({
                "id": row["related_entity"],
                "label": row["related_entity"],
                "color": node_colors[row["node_type"]]
            })
        
        # Create edges
        edges = []
        for _, row in df.iterrows():
            edges.append({
                "from": row["hotel"],
                "to": row["related_entity"],
                "label": row["relation"]
            })
        
        # Return network data
        return {
            "nodes": nodes,
            "edges": edges
        }
    
    # Create app layout
    app.layout = html.Div([
        html.H1("Hotel Knowledge Graph Visualization"),
        
        html.Div([
    html.H3("Knowledge Graph Data"),
    dcc.Graph(
        figure={
            "data": [
                go.Table(
                    header=dict(
                        values=["Hotel", "Relation", "Node Type", "Related Entity"]
                    ),
                    cells=dict(
                        values=[
                            df["hotel"],
                            df["relation"],
                            df["node_type"],
                            df["related_entity"]
                        ]
                    )
                )
            ]
        }
    )
]),
        
        html.Div([
            html.H3("Query the Knowledge Graph"),
            dcc.Input(
                id="query-input",
                type="text",
                placeholder="Enter your query...",
                style={"width": "100%"}
            ),
            html.Button("Submit", id="submit-button"),
            html.Div(id="query-result")
        ])
    ])
    from dash import Input, Output, State

    @app.callback(
        Output("query-result", "children"),
        Input("submit-button", "n_clicks"),
        State("query-input", "value")
    )
    def test_callback(n_clicks, query):
        if not n_clicks:
            return ""

        print("Button clicked")
        print("Query:", query)
        answer=rag_query(query)
        return answer
    
    return app
