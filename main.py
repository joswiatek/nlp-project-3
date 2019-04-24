import neo4jUtilities as neo
import questionProcessingOpenie as qa


if __name__ == "__main__":
    text = "Who plays for the Chicago Bulls?"
    parsed_q = qa.process_question(text)
    neo.getAnswer(parsed_q)

    # result = neo.queryContainsDB("Game", "Nets@Knicks-2018-10-19")
    # # Retrieve all nodes of a certain type
    # for n in neo.getNodesOfType(result, 'Player'):
    #     print(n)
    # # Retrieve all nodes with a specific type of relationship
    # for r in neo.getRelsOfType(result, 'Played'):
    #     print(r)
    # print(neo.getScoresFromGame("Nets@Knicks-2018-10-19"))
