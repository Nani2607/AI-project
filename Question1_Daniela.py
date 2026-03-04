# Step 1: Define the Semantic Network (Knowledge Graph)
# This dictionary represents concepts and their hierarchical relationships
semantic_network = {
    "Person": {
        "is_a": [], 
        "has": ["Intelligence"], 
        "can": ["Breathe"]
    },
    "Museum": {
        "is_a": [], 
        "has": ["Art Collections"], 
        "can": ["Be visited"]
    },
    "James": {
        "is_a": ["Person"], 
        "has": ["Intelligence"], 
        "likes": ["Mona Lisa"]
    },
    "Da Vinci": {
        "is_a": ["Person"], 
        "has": ["Intelligence"], 
        "can": ["Paint"], 
        "painted": ["Mona Lisa"]
    },
    "Mona Lisa": {
        "is_a": ["Painting"], 
        "is_in": ["Louvre"], 
        "painted": ["Da Vinci"]
    },
    "Louvre": {
        "is_a": ["Museum"], 
        "located_in": ["Paris"], 
        "has": ["Mona Lisa"], 
        "can": ["Be visited"]
    }
}

def get_all_properties(concept):
    """
    Performs a recursive traversal to find all properties of a concept, 
    including those inherited from parent nodes (is_a relationships).
    """
    visited = set()
    properties = {
        "is_a": set(), "has": set(), "can": set(), 
        "likes": set(), "painted": set(), "located_in": set(), "is_in": set()
    }

    def traverse(node):
        if node in visited or node not in semantic_network:
            return
        visited.add(node)
        data = semantic_network[node]
        
        # Collect each type of defined relationship
        for rel in properties.keys():
            if rel in data:
                values = data[rel]
                if isinstance(values, list):
                    # Filter out empty strings and update the set
                    properties[rel].update([v for v in values if v])
                else:
                    if values: 
                        properties[rel].add(values)
        
        # Recursive step: Move up the hierarchy (Inheritance)
        for parent in data.get("is_a", []):
            traverse(parent)

    traverse(concept)
    # Return results as a dictionary, filtering out empty property sets
    return {k: list(v) for k, v in properties.items() if v}

def get_options():
    """Returns a list of all available nodes in the network."""
    return list(semantic_network.keys())

def get_graphviz_data():
    """
    Generates DOT code for visual representation in Streamlit.
    """
    dot_code = 'digraph G {\n'
    dot_code += '  rankdir=LR;\n'  # Left to Right direction
    # Node styling (Pink background, Dark Magenta borders)
    dot_code += '  node [style=filled, fillcolor="#FFDBE5", color="#D02A77", fontname="Arial", shape=box, style="filled,rounded"];\n'
    # Edge styling (Hot Pink lines)
    dot_code += '  edge [color="#FF69B4", fontname="Arial", fontsize=10, fontcolor="#4B0082"];\n'
    
    for node, relations in semantic_network.items():
        for rel, targets in relations.items():
            if isinstance(targets, list):
                for target in targets:
                    if target:
                        dot_code += f'  "{node}" -> "{target}" [label="{rel}"];\n'
            elif targets:
                dot_code += f'  "{node}" -> "{targets}" [label="{rel}"];\n'
                
    dot_code += '}'
    return dot_code