from pycorenlp import StanfordCoreNLP
import json

#To run openie cd into stanford folder and run this command: java -mx8g -Xmx8g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -annotators "tokenize,ssplit,pos,lemma,parse,sentiment,coref,openie" -port 9000 -timeout 30000

nlp = StanfordCoreNLP('http://localhost:9000')
text = "Does Jimmy Butler play for the Chicago Bulls?"
output = nlp.annotate(text, properties={'annotators': 'pos, ner, relation',' outputFormat': 'json'})
output = json.loads(output)
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
