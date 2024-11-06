# graphQLSelfReferenceChecker
A couple of scripts to help check graphQL schemas for self references

## Usage
1. Run the introspection (introspectionQuery.txt) query against the graphQL endpoint (typically done in graphQL playground)
2. Save the output to a text file, for example introspection.json
4. Run the python script introspectionCircularCheck.py passing introspection.json as a parameter. This should output a list of all types which reference themselves and can infinately nest.
```python introspectionCircularCheck.py introspectionOutput.json > nestableTypes.txt```
5. Feed the output file and the introspection output json into countFields.py. This will print the number of fields for each nestable type.
```python countFields.py nestableTypes.txt introspectionOutput.json```
6. For ease of testing, select an item from the list which has the fewest field as this will make testing easier.
7. Perform a GraphQL recursive query. This can help to identify DOS and Query Depth Limit vulnerabilities.

