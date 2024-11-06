# graphQLSelfReferenceChecker
A couple of scripts to help check graphQL schemas for self references. This helps to identify DOS and Query Depth Limit vulnerabilities.

## Usage
1. Run the introspection (introspectionQuery.txt) query against the graphQL endpoint (typically done in graphQL playground)
2. Save the output to a text file, for example introspection.json
4. Run the introspectionCircularCheck.py passing introspection.json as a parameter. This should output a list of all types which reference themselves and can infinately nest. Save the output to a new file:
```python introspectionCircularCheck.py introspectionOutput.json > nestableTypes.txt```  
5. Run countFields.py passing in previously created files, this will print the number of fields for each nestable type.
```python countFields.py nestableTypes.txt introspectionOutput.json```
7. For ease of testing, select an item from the list which has the fewest fields as this will make identifying the recursive field easier.
7. Using GraphQL playground, perform a GraphQL recursive query as shown in the following example. The type-ahead should assist in querying for the correct properties. If not see if there is any API documentation that details the Types and their Properties.
![alt text](https://github.com/d-lan2/graphQLSelfReferenceChecker/blob/main/exampleNestedQuery.png)

