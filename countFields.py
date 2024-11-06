import json
import sys

def load_introspection_data(introspection_file):
    # Load introspection data from file
    with open(introspection_file, 'r') as f:
        return json.load(f)

def get_field_count_for_type(introspection_data, type_name):
    # Search for the type in introspection data and count its fields
    for type_info in introspection_data['data']['__schema']['types']:
        if type_info['name'] == type_name:
            if 'fields' in type_info and type_info['fields'] is not None:
                return len(type_info['fields'])
            else:
                return 0  # Type has no fields
    return None  # Type not found

def analyze_types(type_list_file, introspection_data):
    # Read list of types from file
    with open(type_list_file, 'r') as f:
        type_list = [line.strip() for line in f.readlines()]

    # Output each type with its field count
    for type_name in type_list:
        field_count = get_field_count_for_type(introspection_data, type_name)
        if field_count is not None:
            print(f"{type_name}: {field_count} fields")
        else:
            print(f"{type_name}: Type not found in introspection data")

# Main execution
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python count_type_fields.py <type_list_file.txt> <introspection_file.json>")
        sys.exit(1)

    type_list_file = sys.argv[1]
    introspection_file = sys.argv[2]

    introspection_data = load_introspection_data(introspection_file)
    analyze_types(type_list_file, introspection_data)

