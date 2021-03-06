from unittest import main, TestCase
import neo4jUtilities as neo
import questionProcessingOpenie as qa

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

        parsed_q = qa.process_question(q)
        result = set(neo.getAnswer(parsed_q))
        assert(result == a)

    def test_who2(self):
        """
        Simple who is on a team test.
        """
        q = "Who plays for the knicks?" # if knicks was replaced with bulls, this would fail!!
        a = {"Emmanuel Mudiay",
            "Allonzo Trier",
            "Noah Vonleh",
            "Mitchell Robinson",
            "Frank Ntilikina",
            "Kevin Knox",
            "David Fizdale",
            "Tim Hardaway Jr."
            }

        parsed_q = qa.process_question(q)
        result = set(neo.getAnswer(parsed_q))
        assert(result == a)

    def test_which1(self):
        """
        Simple which team won a specific game.
        """
        q = "Which team won in Nets@Knicks-2018-10-19?"
        a = "New York Knicks" #107-105
        parsed_q = qa.process_question(q)
        result = neo.getAnswer(parsed_q)
        assert(result == a)

    def test_when1(self):
        """
        Simple when did two teams play.
        """
        q = "When did the Rockets and the Spurs play?"
        # todo: check for multiple dates that are still valid
        a = "2019-03-23" # Rockets@Spurs-2019-03-23

        parsed_q = qa.process_question(q)
        result = neo.getAnswer(parsed_q)

        assert(a in result)

    def test_when2(self):
        """
        When did two teams play? (Given the teams' full names)
        """
        q = "When did the San Antonio Spurs and Houston Rockets play?"
        # todo: check for multiple dates that are still valid
        a = "2019-03-23" # Rockets@Spurs-2019-03-23

        parsed_q = qa.process_question(q)
        result = neo.getAnswer(parsed_q)

        assert(a in result)

    def test_which2(self):
        """
        Which team was at home? (Check relationship attribute)
        """
        q = "Which team was at home on 2019-03-23, the Spurs or Rockets?"
        a = "San Antonio Spurs"

        parsed_q = qa.process_question(q)
        result = neo.getAnswer(parsed_q)
        assert(result == a)

    def test_points(self):
        """
        How many total points were scored in a specific game?
        """
        q = "How many total points were scored in Hornets@Wizards-2019-03-08?"
        a = "223" # Washington Wizards 112; Charlotte Hornets 111

        #result = neo.getScoresFromGame("Hornets@Wizards-2019-03-08")
        parsed_q = qa.process_question(q)
        result = neo.getAnswer(parsed_q)
        assert(int(a) == result)

    def test_score(self):
        """
        What was the final score of a specific game?
        """
        q = "What was the final score in Hornets@Wizards-2019-03-08?"
        a = {"Washington Wizards 112", "Charlotte Hornets 111"}

        parsed_q = qa.process_question(q)
        result = neo.getAnswer(parsed_q)
        assert(a == result)

    def test_points2(self):
        """
        How many points did person score in specific game?
        """
        q = "How many points did Kemba Walker score in Hornets@Wizards-2019-03-08?"
        a = 18

        parsed_q = qa.process_question(q)
        result = neo.getAnswer(parsed_q)
        assert(a == result)

    def test_who3(self):
        """
        Who scored X points in specific game?
        """
        q = "Who scored 18 points in Hornets@Wizards-2019-03-08?"
        a = {"Kemba Walker"} # Changed to set

        parsed_q = qa.process_question(q)
        result = neo.getAnswer(parsed_q)
        assert(a == result)

    def test_who4(self):
        """
        Who had X rebounds in specific game?
        """
        q = "Who had 10 rebounds in Hornets@Wizards-2019-03-08?"
        a = "Jeremy Lamb"

        parsed_q = qa.process_question(q)
        result = neo.getAnswer(parsed_q)
        assert(a in result)

    def test_who5(self):
        """
        Who scored the most points in specific game?
        """
        q = "Who scored the most points in Heat@Nets-2019-03-02?"
        a = "Derrick Jones Jr."

        parsed_q = qa.process_question(q)
        result = neo.getAnswer(parsed_q)
        assert(a in result)

    def test_who6(self):
        """
        Who scored the least points in specific game?
        """
        q = "Who scored the least points in Bucks@76ers-2019-03-17?"
        a = "Khris Middleton"

        parsed_q = qa.process_question(q)
        result = neo.getAnswer(parsed_q)
        assert(a in result)

    def test_who7(self):
        q = "Who plays for the Bulls?"
        a = {'Lauri Markkanen', 'Zach LaVine', 'Jim Boylen', 'Kris Dunn', 'Fred Hoiberg', 'Justin Holiday', 'Robin Lopez', 'Wendell Carter Jr.', 'Bobby Portis'}

        parsed_q = qa.process_question(q)
        result = neo.getAnswer(parsed_q)
        assert(a == set(result))

    def test_who8(self):
        q = "Who plays for the bulls?"
        a = {'Lauri Markkanen', 'Zach LaVine', 'Jim Boylen', 'Kris Dunn', 'Fred Hoiberg', 'Justin Holiday', 'Robin Lopez', 'Wendell Carter Jr.', 'Bobby Portis'}

        parsed_q = qa.process_question(q)
        result = neo.getAnswer(parsed_q)
        assert(a == set(result))

    def test_who9(self):
        q = "Who plays for the Heat?"
        a = {'Tyler Johnson', 'Erik Spoelstra', 'Josh Richardson', 'Hassan Whiteside', 'Justise Winslow', 'Dwyane Wade', 'James Johnson', 'Goran Dragic', 'Derrick Jones Jr.'}

        parsed_q = qa.process_question(q)
        result = neo.getAnswer(parsed_q)
        assert(a == set(result))

    def test_who10(self):
        q = "Who plays for the heat?"
        a = {'Tyler Johnson', 'Erik Spoelstra', 'Josh Richardson', 'Hassan Whiteside', 'Justise Winslow', 'Dwyane Wade', 'James Johnson', 'Goran Dragic', 'Derrick Jones Jr.'}

        parsed_q = qa.process_question(q)
        result = neo.getAnswer(parsed_q)
        assert(a == set(result))

    def test_score2(self):
        """
        What was the final score of a specific game given in a general format?
        """
        q = "What was the final score for the Hornets and the Wizards on 2019-03-08?"
        a = {"Washington Wizards 112", "Charlotte Hornets 111"}

        parsed_q = qa.process_question(q)
        result = neo.getAnswer(parsed_q)
        assert(a == result)

    def test_which5(self):
        """
        Simple which team won a specific game given in a general format.
        """
        q = "Which team won on 2018-10-19, the Knicks or the Nets?"
        a = "New York Knicks" #107-105
        parsed_q = qa.process_question(q)
        result = neo.getAnswer(parsed_q)
        assert(result == a)

    def test_which6(self):
        """
        Simple which team won a specific game given in a general format.
        """
        q = "Which team won on 2018-10-19, the New York Knicks or the Brooklyn Nets?"
        a = "New York Knicks" #107-105
        parsed_q = qa.process_question(q)
        result = neo.getAnswer(parsed_q)
        assert(result == a)

    def test_points4(self):
        """
        How many total points were scored in a specific game?
        """
        q = "How many total points were scored between the Hornets and the Wizards on 2019-03-08?"
        a = "223" # Washington Wizards 112; Charlotte Hornets 111

        #result = neo.getScoresFromGame("Hornets@Wizards-2019-03-08")
        parsed_q = qa.process_question(q)
        result = neo.getAnswer(parsed_q)
        assert(int(a) == result)

    def test_points5(self):
        """
        How many points did person score in specific game?
        """
        q = "How many points did Kemba Walker score in the Hornets and the Wizards game on 2019-03-08?"
        a = 18

        parsed_q = qa.process_question(q)
        result = neo.getAnswer(parsed_q)
        assert(a == result)

    def test_whoa(self):
        """
        Who scored X points in specific game?
        """
        q = "Who scored 18 points in the Hornets and the Wizards game on 2019-03-08?"
        a = {"Kemba Walker"} # Changed to set

        parsed_q = qa.process_question(q)
        result = neo.getAnswer(parsed_q)
        assert(a == result)

    def test_whob(self):
        """
        Who had X rebounds in specific game?
        """
        q = "Who had 10 rebounds in the Hornets and the Wizards game on 2019-03-08?"
        a = "Jeremy Lamb"

        parsed_q = qa.process_question(q)
        result = neo.getAnswer(parsed_q)
        assert(a in result)

    def test_whoc(self):
        """
        Who scored the most points in specific game?
        """
        q = "Who scored the most points in the Heat and the Nets game on 2019-03-02?"
        a = "Derrick Jones Jr."

        parsed_q = qa.process_question(q)
        result = neo.getAnswer(parsed_q)
        assert(a in result)

    def test_whod(self):
        """
        Who scored the least points in specific game?
        """
        q = "Who scored the least points in the Bucks and the 76ers game on 2019-03-17?"
        a = "Khris Middleton"

        parsed_q = qa.process_question(q)
        result = neo.getAnswer(parsed_q)
        assert(a in result)

    def test_team(self):
        """
        What team does x play for?
        """
        q = "What team does Jimmy Butler play for?"
        a = 'Philadelphia 76ers'

        parsed_q = qa.process_question(q)
        result = neo.getAnswer(parsed_q)
        assert(a in result)

    def test_team2(self):
        """
        Who does x play for?
        """
        q = "Who does Jimmy Butler play for?"
        a = 'Philadelphia 76ers'

        parsed_q = qa.process_question(q)
        result = neo.getAnswer(parsed_q)
        assert(a in result)

    def test_team3(self):
        """
        What team does x play on?
        """
        q = "What team does Jimmy Butler play on?"
        a = 'Philadelphia 76ers'

        parsed_q = qa.process_question(q)
        result = neo.getAnswer(parsed_q)
        assert(a in result)

if __name__ == "__main__":
    main()
