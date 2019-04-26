from stanfordnlp.server import CoreNLPClient
import json
import os
import re

#To run openie cd into stanford folder and run this command: java -mx8g -Xmx8g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -annotators "tokenize,ssplit,pos,lemma,parse,sentiment,coref,openie" -port 9000 -timeout 30000
os.environ['CORENLP_HOME'] = os.path.join(os.getcwd(), 'stanford-corenlp-full-2018-10-05/')
nlpClient = CoreNLPClient(timeout=30000, memory='16G', output_format='json')

team_names = json.load(open("teams.json"))
team_nicknames_as_key = {v: k for k, v in team_names.items()}

def coleman():
    global nlpClient
    text = "Does Jimmy Butler play for the Chicago Bulls?" #Doesn't pick up 'Bulls' as a team
    #text = "When did the San Antonio Spurs and Houston Rockets play?"
    output = nlpClient.annotate(text, annotators=['pos, ner, relation'])
    players = []
    teams = []
    relation = None
    for s in output['sentences']:
        for e in s['entitymentions']:
            if e['ner'] == 'PERSON':
                players.append(e['text'])
            elif e['ner'] == 'ORGANIZATION':
                teams.append(e['text'])
        for t in s['tokens']:
            if t['pos'] in {'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'}:
                tokenAfter = s['tokens'][t['index']]
                if(tokenAfter['pos'] == 'IN'):
                    relation = t['word'] + " " + tokenAfter['word']
    print(players)
    print(teams)
    print(relation)
    return players, teams, relation

def process_question(text):
    global nlpClient
    #text = "Does Jimmy Butler play for the Chicago Bulls?" #Doesn't pick up 'Bulls' as a team
    #text = "When did the San Antonio Spurs and Houston Rockets play?"
    output = nlpClient.annotate(text, annotators=['pos, ner, relation'])
    players = []
    teams = []
    games = []
    nouns = []
    relation = None
    relationIndex = -1
    w_word = None
    lookingFor = None
    num = None
    adjectives = []
    for s in output['sentences']:
        #print(s)
        for e in s['entitymentions']:
            if e['ner'] == 'PERSON':
                players.append(e['text'])
            elif e['ner'] == 'ORGANIZATION':
                teams.append(e['text'])
            elif e['ner'] == 'DATE':
                games.append(e['text'])

        relation = s['basicDependencies'][0]['dependentGloss']
        relationIndex = s['basicDependencies'][0]['dependent']
        for d in s['basicDependencies']:
            if(d['governor'] == relationIndex):
                if(d['dep'] in {'dobj', 'nmod', 'nsubj', 'nsubjpass'}):
                    if(len(list(filter(lambda x: re.match('.*'+d['dependentGloss']+'.*$', x), [*players, *teams, *games]))) == 0):
                        lookingFor = d['dependentGloss']

        for t in s['tokens']:
            if t['pos'] in {'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'}:
                tokenAfter = s['tokens'][t['index']]
                if(tokenAfter['pos'] == 'IN'):
                    if t['word'] == relation:
                        relation = t['word'] + " " + tokenAfter['word']
            elif t['pos'] in {'WP', 'WRB', 'WDT', 'WP$'}:
                w_word = t['word']
            elif t['pos'] in {'NNS', 'NN', 'NNP'}: # plural nouns and nouns (i.e. points, rebounds, score)
                if t['word'] not in players and t['word'] not in teams and t['word'] not in games:
                    nouns.append(t['word'])
            elif t['pos'] == 'CD' and t['ner'] != "DATE":
                num = int(t['word'])
            elif t['pos'] in {'JJ', 'JJR', 'JJS', 'RB', 'RBR', 'RBS'}:
                adjectives.append(t['word'])
    
    for n in nouns:
        if n.title() in team_nicknames_as_key:
            teams.append(team_nicknames_as_key[n.title()])

    # print('w word:')
    # print(w_word)
    # print('players:')
    # print(players)
    # print('teams:')
    # print(teams)
    # print('games:')
    # print(games)
    # print('relation:')
    # print(relation)
    # print('looking for:')
    # print(lookingFor)
    # print('nouns:')
    # print(nouns)
    # print('num:')
    # print(num)
    # print('adjectives:')
    # print(adjectives)
    return players, teams, relation, w_word, games, nouns, lookingFor, num, adjectives
