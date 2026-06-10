from data.sample_reviews import sample_hotel_reviews
from graph.graph_builder import create_knowledge_graph
from rag.retrieval import rag_query
import os
from visualization.dashboard import create_visualization_app


def main():
    # Check if environment variables are set
    required_vars = ["NEO4J_URI", "NEO4J_USERNAME", "NEO4J_PASSWORD"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"Error: Missing environment variables: {', '.join(missing_vars)}")
        print("Please set these variables in your .env file")
        return
    
    print("Starting Graph RAG pipeline... to test from console")
    
    # Create knowledge graph
    print("\n1. Creating knowledge graph from hotel reviews...")
    create_knowledge_graph(sample_hotel_reviews)
    
    # Test RAG query
    print("\n2. Testing RAG query...")
    test_query = "which hotels are visited by Businessmen?"
    answer = rag_query(test_query)
    print(f"\nQuery: {test_query}")
    print(f"Answer: {answer}")
    
    # Create visualization app
    print("\n3. Creating visualization app...")
    print(os.getenv("NEO4J_URI"))
    app = create_visualization_app(
        os.getenv("NEO4J_URI"),
        os.getenv("NEO4J_USERNAME"),
        os.getenv("NEO4J_PASSWORD")
    )
    
    # Run the app
    print("\nStarting Dash app for visualization. Open http://127.0.0.1:8050/ in your browser.")
    app.run(debug=True)

if __name__ == "__main__":
    main()
