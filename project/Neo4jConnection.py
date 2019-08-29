from neo4j import GraphDatabase
import credentials

class Neo4JConnection:
    def __init__(self):
        uri = credentials.LOCAL_URI
        user = credentals.LOCAL_USER
        pw = credentials.LOCAL_PASSWORD
        self.driver = GraphDatabase.driver(uri, auth=(user, pw))

    


    def create_liked_relationship(self, username1, username2):
        '''
        username1 is the liker, username2 is the likee
        '''

        with self.driver.session() as session:
            assert username1[0] == '@'
            assert username2[0] == '@'
            session.run("MERGE (u1:User {Username: $username1}) "
                             "MERGE (u2:User {Username: $username2}) "
                             "MERGE (u1)-[r:LIKED]->(u2)", parameters={'username1':username1, 'username2':username2})
