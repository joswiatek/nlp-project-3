from neo4j import GraphDatabase
from os import environ

neo4j_params = {
     'user': environ['NLP_NEO4J_USER'],
     'password': environ['NLP_NEO4J_PASS'],
     'uri': environ['NLP_NEO4J_URI']
     }

def queryDB(nodeType, nodeName):
    """Retrieve the node of type nodeType with the name nodeName, along with all
    related nodes and the relationships between them."""

    try:
        neo4jDriver = GraphDatabase.driver(neo4j_params['uri'], auth=(neo4j_params['user'], neo4j_params['password']))
        with neo4jDriver.session() as session:
            matchStatement = "MATCH (n:%s {name: \"%s\"})-[r]-(m) RETURN n, r, m" % (nodeType, nodeName)
            return session.run(matchStatement).graph()
    except Exception as e:
        print('Exception during write to Neo4j: %s' % e)

def queryContainsDB(nodeType, nodeName):
    """Retrieve the node of type nodeType with the name nodeName using the contains clause, along with all
    related nodes and the relationships between them."""

    try:
        neo4jDriver = GraphDatabase.driver(neo4j_params['uri'], auth=(neo4j_params['user'], neo4j_params['password']))
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

def getTeamFromPlayer(playerName):
    result = queryContainsDB("Player", playerName.title())
    return [p['name'] for p in getNodesOfType(result, "Team")]

def getScoresFromGame(gameName):
    """Returns the scores of Players and Teams from a specific game in a dictionary. 
    scores["Players"] is a dictionary where the key is the player name, and the value is their score. 
    scores["Teams"] is a dictionary where the key is the team name and the value is their score. """

    result = queryContainsDB("Game", gameName)
    scores = {"Players" : {}, "Teams" : {}, "Total Points" : 0}
    for r in getRelsOfType(result, "Played"):
        if "Player" in r.start_node.labels:
            scores["Players"][r.start_node["name"]] = r["points"]
        elif "Team" in r.start_node.labels:
            scores["Teams"][r.start_node["name"]] = r["score"]
    scores["Total Points"] = sum(scores["Teams"].values())
    scores["Winner"] = max(scores["Teams"], key=scores["Teams"].get)
    return scores




def getAnswer(parsed_q):
    players = parsed_q[0]
    print(players)
    teams = parsed_q[1]
    relation = parsed_q[2]
    w_word = parsed_q[3]
    games = parsed_q[4]

    if w_word is None:
        return 'IDK Google it!'
    try:
        if relation == 'plays for' and w_word == 'Who':
            return getPlayersFromTeam(teams[0])
        if w_word == 'Which':
            if relation == 'play for':
                return getTeamFromPlayer(players[0])
            elif 'won' in relation:
                scores = getScoresFromGame(games[0])
                return scores['Winner']
    except:
        return 'IDK Google it!'
