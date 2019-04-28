import json
import requests
from os import environ

google_API_key = environ['GOOGLE_API_KEY']
entity_endpoint = 'https://language.googleapis.com/v1/documents:analyzeEntities'
syntax_endpoint = 'https://language.googleapis.com/v1/documents:analyzeSyntax'
api_params = {'key': google_API_key}
w_words_bank = {'who', 'what', 'when', 'where', 'which', 'whose', 'whom'}

def get_entities(text):
    # text = "Does Jimmy Butler play for the Chicago Bulls?" #Doesn't pick up 'Bulls' as a team
    # text = "When did the San Antonio Spurs and Houston Rockets play?"
    payload = json.dumps({
        'document':{
            "content": text,
            "type":"PLAIN_TEXT",
            "language": "EN"},
        'encodingType': 'UTF8'
        })

    # Make request for entities
    r = requests.post(entity_endpoint, params=api_params, data=payload)
    entity_output = json.loads(r.text)

    # Make request for syntax
    r = requests.post(syntax_endpoint, params=api_params, data=payload)
    syntax_output = json.loads(r.text)

    players = []
    teams = []
    games = []
    relation = None
    w_word = None
    for e in entity_output['entities']:
        if e['type'] == 'PERSON':
            players.append(e['name'])
        elif e['type'] == 'ORGANIZATION':
            teams.append(e['name'])
        elif e['type'] == 'DATE':
            games.append(e['name'])

    for i, t in enumerate(syntax_output['tokens']):
        if t['partOfSpeech']['tag'] in {'VERB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'}:
            token_after = syntax_output['tokens'][i+1]
            if(token_after['partOfSpeech']['tag'] in {'IN', 'ADP'}):
                relation = t['text']['content'] + " " + token_after['text']['content']

        elif t['lemma'].lower() in w_words_bank:
            w_word = t['text']['content']


    # print('INPUT: %s' % text)
    # print('W_WORDS: %s' % w_word)
    # print('PLAYERS: %s' % players)
    # print('TEAMS: %s' % teams)
    # print('RELATION: %s' % relation)
    return players, teams, relation, w_word, games
