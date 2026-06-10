# Function to strip markdown code blocks from Cypher queries
def strip_markdown_code_blocks(query):
    """
    Remove markdown code block markers (```) from Cypher queries
    """
    if query.startswith('```'):
        # Find the end of the first code block marker
        first_marker_end = query.find('\n', 3)
        if first_marker_end != -1:
            query = query[first_marker_end + 1:]
    
    # Remove trailing code block markers
    if '```' in query:
        query = query.split('```')[0]
    
    return query.strip()