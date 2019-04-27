This repository is for Coleman Oei, Rileigh Bandy, Rizwan Lubis, and Joel Swiatek's project for Practical Applications of Natural Language Processing.

Rough idea of a pipeline:
1. Use OpenIE to extract named entities from the question.
1. Query the Neo4J database to extract all related nodes and relationships.
1. Do question classification/answer type prediction to determine the LAT (lexical answer type).
1. Use the LAT and the extracted info from Neo4j to determine the answer to the question.
