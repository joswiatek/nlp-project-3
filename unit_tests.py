from unittest import main, TestCase
import neo4jUtilities as neo

class MyUnitTests(TestCase):
    """
    Here are some questions our DB should be able to answer.
    Todo: add asserts once our pipeline is developed to compare
    expected answers to actual answers.
    """

    def test_who1(self):
        """
        Simple who is on a team test.
        """
        q = "Who plays for the New York Knicks?"
        a = {"Emmanuel Mudiay",
            "Allonzo Trier",
            "Noah Vonleh",
            "Mitchell Robinson",
            "Frank Ntilikina",
            "Kevin Knox",
            "David Fizdale",
            "Tim Hardaway Jr."
            }
        
        result = set(neo.getPlayersFromTeam("New York Knicks"))
        assert(result == a)

    def test_who2(self):
        """
        Simple who is on a team test.
        """
        q = "Who plays for the New York Knicks?"
        a = {"Emmanuel Mudiay",
            "Allonzo Trier",
            "Noah Vonleh",
            "Mitchell Robinson",
            "Frank Ntilikina",
            "Kevin Knox",
            "David Fizdale",
            "Tim Hardaway Jr."
            }
        
        result = set(neo.getPlayersFromTeam("knicks"))
        assert(result == a)

    def test_which1(self):
        """
        Simple which team won a specific game.
        """
        q = "Which team won in Nets@Knicks-2018-10-19?"
        a = "New York Knicks" #107-105

        result = neo.getScoresFromGame("Nets@Knicks-2018-10-19")
        winner = max(result["Teams"], key=result["Teams"].get)

        assert(winner == a)

    def test_when1(self):
        """
        Simple when did two teams play.
        """
        q = "When did the Rockets and the Spurs play?"
        # todo: check for multiple dates that are still valid
        a = "2019-03-23" # Rockets@Spurs-2019-03-23

    def test_when2(self):
        """
        When did two teams play? (Given the teams' full names)
        """
        q = "When did the San Antonio Spurs and Houston Rockets play?"
        # todo: check for multiple dates that are still valid
        a = "2019-03-23" # Rockets@Spurs-2019-03-23


    def test_which2(self):
        """
        Which team was at home? (Check relationship attribute)
        """    
        q = "Were the Spurs or Rockets at home on 2019-03-23?"
        a = "Houston Rockets"

    def test_points(self):
        """
        How many points were scored in a specific game?
        """
        q = "How many points were scored in Hornets@Wizards-2019-03-08?"
        a = "223" # Washington Wizards 112; Charlotte Hornets 111

    def test_score(self):
        """
        What was the final score of a specific game?
        """
        q = "What was the final score in Hornets@Wizards-2019-03-08?"
        a = {"Washington Wizards 112", "Charlotte Hornets 111"}

    def test_who3(self):
        """
        Who scored X points in specific game?
        """
        q = "Who scored 18 points in Hornets@Wizards-2019-03-08?"
        a = "Kemba Walker"

    def test_who4(self):
        """
        Who had X rebounds in specific game?
        """
        q = "Who had 10 rebounds in Hornets@Wizards-2019-03-08?"
        a = "Jeremy Lamb"
    


if __name__ == "__main__":
    main()