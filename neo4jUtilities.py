from neo4j import GraphDatabase

neo4jUser = 'neo4j'
neo4jPassword = 'password'
neo4jUri = 'bolt://localhost:7687'

def queryDB(nodeType, nodeName):
    """Retrieve the node of type nodeType with the name nodeName, along with all
    related nodes and the relationships between them."""

    try:
        neo4jDriver = GraphDatabase.driver(neo4jUri, auth=(neo4jUser, neo4jPassword))
        with neo4jDriver.session() as session:
            matchStatement = "MATCH (n:%s {name: \"%s\"})-[r]-(m) RETURN n, r, m" % (nodeType, nodeName)
            return session.run(matchStatement).graph()
    except Exception as e:
        print('Exception during write to Neo4j: %s' % e)

def queryContainsDB(nodeType, nodeName):
    """Retrieve the node of type nodeType with the name nodeName using the contains clause, along with all
    related nodes and the relationships between them."""

    try:
        neo4jDriver = GraphDatabase.driver(neo4jUri, auth=(neo4jUser, neo4jPassword))
        with neo4jDriver.session() as session:
            matchStatement = "MATCH (n:%s)-[r]-(m) WHERE n.name contains \"%s\" RETURN n, r, m" % (nodeType, nodeName)
            return session.run(matchStatement).graph()
    except Exception as e:
        print('Exception during write to Neo4j: %s' % e)

def getNodesOfType(graph, label):
    return [n for n in graph.nodes if label in n.labels]

def getRelsOfType(graph, type):
    return [r for r in graph.relationships if r.type == type]

def getPlayersFromTeam(teamName):
    result = queryContainsDB("Team", teamName.title())
    return [p['name'] for p in getNodesOfType(result, "Player")]

def getScoresFromGame(gameName):
    result = queryContainsDB("Game", gameName)
    