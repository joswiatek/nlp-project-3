from neo4j import GraphDatabase
from os import environ
import json

neo4j_params = {
     'user': environ['NLP_NEO4J_USER'],
     'password': environ['NLP_NEO4J_PASS'],
     'uri': environ['NLP_NEO4J_URI']
     }
team_names = json.load(open("teams.json"))

def queryDB(nodeType, nodeName):
    """Retrieve the node of type nodeType with the name nodeName, along with all
    related nodes and the relationships between them."""

    try:
        neo4jDriver = GraphDatabase.driver(neo4j_params['uri'], auth=(neo4j_params['user'], neo4j_params['password']))
        with neo4jDriver.session() as session:
            matchStatement = "MATCH (n:%s {name: \"%s\"})-[r]-(m) RETURN n, r, m" % (nodeType, nodeName)
            return session.run(matchStatement).graph()
    except Exception as e:
        print('Exception during read from Neo4j: %s' % e)

def queryContainsDB(nodeType, nodeName):
    """Retrieve the node of type nodeType with the name nodeName using the contains clause, along with all
    related nodes and the relationships between them."""

    try:
        neo4jDriver = GraphDatabase.driver(neo4j_params['uri'], auth=(neo4j_params['user'], neo4j_params['password']))
        with neo4jDriver.session() as session:
            matchStatement = "MATCH (n:%s)-[r]-(m) WHERE n.name contains \"%s\" RETURN n, r, m" % (nodeType, nodeName)
            return session.run(matchStatement).graph()
    except Exception as e:
        print('Exception during read from Neo4j: %s' % e)

def getHomeFromTeamsAndDate(team1, team2, date):
    if team1 in team_names:
        team1 = team_names[team1]
    if team2 in team_names:
        team2 = team_names[team2]

    try:
        neo4jDriver = GraphDatabase.driver(neo4j_params['uri'], auth=(neo4j_params['user'], neo4j_params['password']))
        with neo4jDriver.session() as session:
            matchStatement = "MATCH (n:%s)-[r]-(m) WHERE (n.name contains \"%s\"  AND n.name contains \"%s\" AND n.name contains \"%s\") RETURN n, r, m" % ("Game", team1, team2, date)
            graph = session.run(matchStatement).graph()
    except Exception as e:
        print('Exception during read from Neo4j: %s' % e)
    
    for r in getRelsOfType(graph, "Played"):
        if "home_team" in r and r["home_team"] == True:
            return r.start_node["name"]

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
    teams = parsed_q[1]
    relation = parsed_q[2]
    w_word = parsed_q[3]
    games = parsed_q[4]
    nouns = parsed_q[5]
    lookingFor = parsed_q[6]
    num = parsed_q[7]

    if w_word is None:
        return 'IDK Google it!'
    try:
        if w_word == 'Who':
            if relation == 'plays for':
                return getPlayersFromTeam(teams[0])
            if lookingFor == 'points' and games != []:
                result = getScoresFromGame(games[0])
                return {name for name, points in result["Players"].items() if points == num}

        if w_word == 'Which':
            if relation == 'play for':
                return getTeamFromPlayer(players[0])
            elif 'won' in relation:
                scores = getScoresFromGame(games[0])
                return scores['Winner']
            elif 'home' in nouns:
                return getHomeFromTeamsAndDate(teams[0], teams[1], games[0])

        if w_word == 'How':
            # either how many points or rebounds
            if players != [] and games != []:
                result = getScoresFromGame(games[0])
                return result['Players'][players[0]]
            if games != []:
                result = getScoresFromGame(games[0])
                return result["Total Points"]
            if player != []:
                result = "todo"

        if w_word == 'What':
            if games != [] and nouns[0] == 'score':
                result = getScoresFromGame(games[0])
                return {name + " " + str(score) for name, score in result["Teams"].items()}

    except:
        return 'IDK Google it!'
