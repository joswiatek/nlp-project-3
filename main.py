import neo4jUtilities as neo
import questionProcessingOpenie as qa

import json


if __name__ == "__main__":
    text = "Which team was at home on 2019-03-23, the Spurs or Rockets?"
    parsed_q = qa.process_question(text)
    # temp = neo.getAnswer(parsed_q)
    # print('temp', temp)


    # with open("raw_teams.json") as f:
    #     d = json.load(f)
    
    # dicti = {}
    # for i in d:
    #     dicti[i['teamName']] = i['simpleName']
    # with open('teams.json', 'w') as fp:
    #     json.dump(dicti, fp)


    # result = neo.queryContainsDB("Game", "Nets@Knicks-2018-10-19")
    # # Retrieve all nodes of a certain type
    # for n in neo.getNodesOfType(result, 'Player'):
    #     print(n)
    # # Retrieve all nodes with a specific type of relationship
    # for r in neo.getRelsOfType(result, 'Played'):
    #     print(r)
    # print(neo.getScoresFromGame("Nets@Knicks-2018-10-19"))
