from neo4j import GraphDatabase

class Neo4JConnection:
    def __init__(self):
        uri = 'bolt://localhost:7687'
        user = 'neo4j'
        pw = '1776'
        self.driver = GraphDatabase.driver(uri, auth=(user, pw))
        self.session = self.driver.session()
    


    def create_liked_relationship(self, username1, username2):
        '''
        username1 is the liker, username2 is the likee
        '''
        assert username1[0] == '@'
        assert username2[0] == '@'
        self.session.run("MERGE (u1:User {Username: $username1}) "
                         "MERGE (u2:User {Username: $username2}) "
                         "MERGE (u1)-[r:LIKED]->(u2)", parameters={'username1':username1, 'username2':username2})
