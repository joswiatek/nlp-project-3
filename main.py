import neo4jUtilities as neo

if __name__ == "__main__":
    result = neo.queryDB("Team", "Portland Trail Blazers")
    # Retrieve all nodes of a certain type
    for n in neo.getNodesOfType(result, 'Player'):
        print(n)
    # Retrieve all nodes with a specific type of relationship
    for r in neo.getRelsOfType(result, 'Plays for'):
        print(r)
