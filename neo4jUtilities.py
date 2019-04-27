from neo4j import GraphDatabase
from os import environ
import json
import operator

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

def getHomeFromTeamsAndDate(team1, team2, date, **d):
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

def getPlayersFromTeam(teamName, **d):
    result = queryContainsDB("Team", teamName.title())
    return [p['name'] for p in getNodesOfType(result, "Player")]

def getTeamFromPlayer(playerName, **d):
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

# def getAnswer(parsed_q):
#     players = parsed_q[0]
#     teams = parsed_q[1]
#     relation = parsed_q[2]
#     w_word = parsed_q[3]
#     games = parsed_q[4]
#     nouns = parsed_q[5]
#     lookingFor = parsed_q[6]
#     num = parsed_q[7]
#
#     if w_word is None:
#         return 'IDK Google it!'
#     try:
#         if w_word == 'Who':
#             if relation == 'plays for':
#                 # Who plays for this team
#                 return getPlayersFromTeam(teams[0])
#             if lookingFor == 'points' and games != []:
#                 # Who scored this number of points
#                 return getWhoScoredNumPoints(games[0], num)
#
#         if w_word == 'Which':
#             if relation == 'play for':
#                 #which team does blank play for
#                 return getTeamFromPlayer(players[0])
#             elif 'won' in relation:
#                 #Which team one in this game
#                 return getWinnerOfGame(games[0])
#             elif 'home' in nouns:
#                 #Which team was at home for this game
#                 return getHomeFromTeamsAndDate(teams[0], teams[1], games[0])
#
#         if w_word == 'How':
#             # either how many points or rebounds
#             if players != [] and games != []:
#                 #how many points did a player score in this game
#                 return getPointsOfPlayerInGame(games[0], players[0])
#             if games != []:
#                 #how many were score in this game
#                 return getTotalGamePoints(games[0])
#             if player != []:
#                 result = "todo"
#
#         if w_word == 'What':
#             if games != [] and nouns[0] == 'score':
#                 # what was the score of a given game
#                 return getTeamScoresFromGame(games[0])
#
#     except:
#         return 'IDK Google it!'

def getWhoScoredNumPoints(gameName, num, **d):
    result = getScoresFromGame(gameName)
    return {name for name, points in result["Players"].items() if points == num}

def getWinnerOfGame(gameName, **d):
    scores = getScoresFromGame(gameName, **d)
    return scores['Winner']

def getPointsOfPlayerInGame(gameName, playerName, **d):
    result = getScoresFromGame(gameName)
    return result['Players'][playerName]

def getTotalGamePoints(gameName, **d):
    result = getScoresFromGame(gameName)
    return result["Total Points"]

def getTeamScoresFromGame(gameName, **d):
    result = getScoresFromGame(gameName)
    return {name + " " + str(score) for name, score in result["Teams"].items()}

def getAnswer(parsed_q):
    players = parsed_q[0]
    teams = parsed_q[1]
    relation = parsed_q[2]
    w_word = parsed_q[3]
    games = parsed_q[4]
    nouns = parsed_q[5]
    lookingFor = parsed_q[6].lower()
    num = parsed_q[7]
    votingDict = {
                'playersFromTeam': {'votes': 0, 'validParams': False},
                'teamScoresFromGame': {'votes': 0, 'validParams': False},
                'teamFromPlayer': {'votes': 0, 'validParams': False},
                'homeFromTeamsAndDate': {'votes': 0, 'validParams': False},
                'whoScoredNumPoints': {'votes': 0, 'validParams': False},
                'winnerOfGame': {'votes': 0, 'validParams': False},
                'pointsOfPlayerInGame': {'votes': 0, 'validParams': False},
                'totalGamePoints': {'votes': 0, 'validParams': False}}
    invalidQuestion = 'IDK Google it!'

    if(lookingFor == 'team'):
        votingDict['teamFromPlayer']['votes'] += 1
        votingDict['winnerOfGame']['votes'] += 1
        votingDict['homeFromTeamsAndDate']['votes'] += 1
        votingDict['whoScoredNumPoints']['votes'] += 1
    elif(lookingFor == 'score'):
        votingDict['totalGamePoints']['votes'] += 1
        votingDict['pointsOfPlayerInGame']['votes'] += 1
        votingDict['teamScoresFromGame']['votes'] += 1
    elif(lookingFor == 'who'):
        votingDict['playersFromTeam']['votes'] += 1
        votingDict['whoScoredNumPoints']['votes'] += 1


    if w_word == 'Who':
        if relation == 'plays for':
            # Who plays for this team
            votingDict['playersFromTeam']['votes'] += 1
        if lookingFor == 'points' and games != []:
            # Who scored this number of points
            votingDict['whoScoredNumPoints']['votes'] += 1

    if w_word == 'Which':
        if relation == 'play for':
            #which team does blank play for
            votingDict['teamFromPlayer']['votes'] += 1
        elif 'won' in relation:
            #Which team one in this game
            votingDict['winnerOfGame']['votes'] += 1
        elif 'home' in nouns:
            #Which team was at home for this game
            votingDict['homeFromTeamsAndDate']['votes'] += 1

    if w_word == 'How':
        # either how many points or rebounds
        if players != [] and games != []:
            #how many points did a player score in this game
            votingDict['pointsOfPlayerInGame']['votes'] += 1
        if games != []:
            #how many were score in this game
            votingDict['totalGamePoints']['votes'] += 1
        if players != []:
            result = "todo"

    if w_word == 'What':
        if games != [] and nouns[0] == 'score':
            # what was the score of a given game
            votingDict['teamScoresFromGame']['votes'] += 1

    #validate validParams
    for k in votingDict:
        if k == 'playersFromTeam':
            votingDict[k]['validParams'] = len(teams) > 0
        elif k == 'whoScoredNumPoints':
            votingDict[k]['validParams'] = len(games) > 0
        elif k == 'teamFromPlayer':
            votingDict[k]['validParams'] = len(players) > 0
        elif k == 'winnerOfGame':
            votingDict[k]['validParams'] = len(games) > 0
        elif k == 'homeFromTeamsAndDate':
            votingDict[k]['validParams'] = len(games) > 0 and len(teams) > 1
        elif k == 'pointsOfPlayerInGame':
            votingDict[k]['validParams'] = len(games) > 0 and len(players) > 0
        elif k == 'totalGamePoints':
            votingDict[k]['validParams'] = len(games) > 0
        elif k == 'teamScoresFromGame':
            votingDict[k]['validParams'] = len(games) > 0

    maxKey = None
    maxVotes = 0
    for k in votingDict:
        if votingDict[k]['votes'] > maxVotes and votingDict[k]['validParams']:
            maxKey = k
            maxVotes = votingDict[k]['votes']
    print(maxKey)
    print(lookingFor)
    if (maxKey == 'playersFromTeam'):
        return getPlayersFromTeam(teams[0])
    elif (maxKey == 'whoScoredNumPoints'):
        return getWhoScoredNumPoints(games[0], num)
    elif (maxKey == 'teamFromPlayer'):
        return getTeamFromPlayer(players[0])
    elif (maxKey == 'winnerOfGame'):
        return getWinnerOfGame(games[0])
    elif (maxKey == 'homeFromTeamsAndDate'):
        return getHomeFromTeamsAndDate(teams[0], teams[1], games[0])
    elif (maxKey == 'pointsOfPlayerInGame'):
        return getPointsOfPlayerInGame(games[0], players[0])
    elif (maxKey == 'totalGamePoints'):
        return getTotalGamePoints(games[0])
    elif (maxKey == 'teamScoresFromGame'):
        return getTeamScoresFromGame(games[0])
    else:
        return invalidQuestion
