import json
import sys

def build_type_graph(introspection_data):
    # Initialize an empty graph
    type_graph = {}

    # Extract types from the introspection data
    for type_info in introspection_data['data']['__schema']['types']:
        type_name = type_info['name']
        type_graph[type_name] = []

        # Only process types that have fields
        if 'fields' in type_info and type_info['fields'] is not None:
            for field in type_info['fields']:
                field_type = extract_base_type(field['type'])
                if field_type:  # Avoid None types (e.g., scalars)
                    type_graph[type_name].append(field_type)

    return type_graph

def extract_base_type(type_obj):
    # Recursively retrieve the base type, handling wrappers like LIST and NON_NULL
    while 'ofType' in type_obj and type_obj['ofType'] is not None:
        type_obj = type_obj['ofType']
    return type_obj.get('name')

def detect_circular_dependencies(type_graph):
    visited = set()
    stack = set()
    circular_types = []

    def dfs(type_name):
        # Detect a cycle with stack
        if type_name in stack:
            circular_types.append(type_name)
            return True
        if type_name in visited:
            return False

        visited.add(type_name)
        stack.add(type_name)

        # Traverse neighboring types
        for neighbor in type_graph.get(type_name, []):
            if dfs(neighbor):
                return True

        stack.remove(type_name)
        return False

    # Run DFS on each type to detect cycles
    for type_name in type_graph:
        if type_name not in visited:
            dfs(type_name)

    return circular_types

def analyze_introspection(introspection_file):
    # Load introspection data from file
    with open(introspection_file, 'r') as f:
        introspection_data = json.load(f)
    
    # Step 1: Build the type graph
    type_graph = build_type_graph(introspection_data)
    
    # Step 2: Detect circular dependencies
    circular_types = detect_circular_dependencies(type_graph)
    
    # Report circular types
    if circular_types:
        print("Potentially nestable circular types detected:")
        for type_name in circular_types:
            print(f"{type_name}")
    else:
        print("No circular types detected.")

# Main execution
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python detect_circular_dependencies.py <introspection_file.json>")
        sys.exit(1)

    introspection_file = sys.argv[1]
    analyze_introspection(introspection_file)

