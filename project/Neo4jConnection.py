from neo4j import GraphDatabase
import neo4j_credentials

class Neo4JConnection:
    def __init__(self):
        uri = neo4j_credentials.LOCAL_URI
        user = neo4j_credentials.LOCAL_USER
        pw = neo4j_credentials.LOCAL_PASSWORD
        self.driver = GraphDatabase.driver(uri, auth=(user, pw))

    def close(self):
        self.driver.close()
        
    def create_liked_relationship(self, username1, username2):
        """
        username1 is the liker, username2 is the likee
        """

        with self.driver.session() as session:
            assert username1[0] == '@' and username2[0] == '@'
            session.run("MERGE (u1:User {username: $username1}) "
                             "MERGE (u2:User {username: $username2}) "
                             "MERGE (u1)-[r:LIKED]->(u2)", parameters={'username1':username1, 'username2':username2})


    def create_follow_relationship(self, username1, username2):
        """
        username1 is the follower, username2 is the followed
        """

        with self.driver.session() as session:
            assert username1[0] == '@' and username2[0] == '@'
            session.run("MERGE (u1:User {username: $username1}) "
                             "MERGE (u2:User {username: $username2}) "
                             "MERGE (u1)-[r:FOLLOWS]->(u2)", parameters={'username1':username1, 'username2':username2})

            
    def create_follow_relationship_politics(self, username1, username2, politics):
        """
        create follower with a political label
        """
        with self.driver.session() as session:
            assert username1[0] == '@' and username2[0] == '@'
            session.run("MERGE (u1:User {username: $username1, politics: $politics}) "
                             "MERGE (u2:User {username: $username2, politics: $politics}) "
                             "MERGE (u1)-[r:FOLLOWS]->(u2)", parameters={'username1':username1, 'username2':username2, 'politics':politics})
