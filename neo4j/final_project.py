#ZACHARY ADLER - zpa2001
#RUNNING PY@NEO V2.0.8

# Put the use case you chose here. Then justify your database choice:
# USE CASE: Bike share app.  I chose to use neo4j as their is an obvious relationship physically when using a bike sharing app and that idea was fairly simple to model virtually.
#
# Explain what will happen if coffee is spilled on one of the servers in your cluster, causing it to go down.
#  If coffee is spilled on a server, then because there is more than 1 core server, the read/write abilities would be performed on the other core servers, to be accpeted by majority of the core servers, to then be distributed through the Raft Protocol to the Replica Servers.
#
# What data is it not ok to lose in your app? What can you do in your commands to mitigate the risk of lost data?
# Data like the Node's Label and Name would be important to keep, and in order to mitigate risk of loss of data I should be sure to make sure the DELETE queries are deleting one relationship and not many at a time, otherwie a good portion of data can be tampered with.
#

from py2neo import authenticate, Graph
authenticate("localhost:7474", "neo4j","test")
graph = Graph()
# to ensure the data in the DB isn't reloaded for this assignment. This is not something you would do for real database implementation
graph.cypher.execute("MATCH (n)-[r]-() DELETE r,n")
graph.cypher.execute("CREATE (aa:User { name: 'Andy', area: 'Inwood'}), (bb:User { name: 'Brad', area: 'Midtown'}), (cc:User { name: 'Carl', area: 'Tudor'}), (a:Station { loc: 'Inwood', numBikes: 2, racks:6 }), (b:Station { loc: 'Harlem', numBikes: 1, racks:6 }), (c:Station { loc: 'Central Park', numBikes: 4 ,racks:6}), (d:Station { loc: 'Midtown', numBikes: 3, racks:6}), (e:Station { loc: 'Theater', numBikes: 2, racks:6 }), (f:Station { loc: 'Garment', numBikes: 5, racks:6 }), (g:Station { loc: 'Chelsea', numBikes: 6, racks:6 }), (h:Station { loc: 'Greenwich', numBikes: 1, racks:6 }), (i:Station { loc: 'Noho', numBikes: 1, racks:6 }), (j:Station { loc: 'Soho', numBikes: 2, racks:6 }), (k:Station { loc: 'Tribeca', numBikes: 1, racks:6 }), (l:Station { loc: 'Chinatown', numBikes: 4, racks:6 }), (m:Station { loc: 'Gramercy', numBikes: 3, racks:6 }), (n:Station { loc: 'Tudor', numBikes: 4, racks:6 }), (o:Station { loc: 'Beekman', numBikes: 3, racks:6 }), (a)-[:NEXT]->(b),(b)-[:NEXT]->(c),(c)-[:NEXT]->(d),(d)-[:NEXT]->(e),(e)-[:NEXT]->(f),(f)-[:NEXT]->(g),(g)-[:NEXT]->(h), (h)-[:NEXT]->(i), (i)-[:NEXT]->(j), (j)-[:NEXT]->(k),(k)-[:NEXT]->(l),(l)-[:NEXT]->(m), (m)-[:NEXT]->(n), (n)-[:NEXT]->(o), (aa)-[:FAV_STAT]->(a), (bb)-[:FAV_STAT]->(d), (cc)-[:FAV_STAT]->(n), (b)-[:NEXT]->(a),(c)-[:NEXT]->(b),(d)-[:NEXT]->(c),(e)-[:NEXT]->(d),(f)-[:NEXT]->(e),(g)-[:NEXT]->(f),(g)-[:NEXT]->(h), (i)-[:NEXT]->(h), (j)-[:NEXT]->(i), (k)-[:NEXT]->(j),(l)-[:NEXT]->(k),(m)-[:NEXT]->(l), (n)-[:NEXT]->(m), (o)-[:NEXT]->(n)")

# Action 1: User creates account
graph.cypher.execute("CREATE (b:User {name:'Dave', area: 'Soho'})")

# Action 2: User picks their favorite station 
graph.cypher.execute("MATCH (n:User), (m:Station) WHERE n.name='Dave' AND m.loc = n.area CREATE (n)-[:FAV_STAT]->(m)")

# Action 3: User looks at the stations next to their favorite station
graph.cypher.execute("MATCH (a:User)-[:FAV_STAT]-(m:Station),(m:Station)-[:NEXT]->(o:Station) WHERE a.name='Dave' RETURN o.loc")

# Action 4: User looks for the number of bikes at their favorite station
graph.cypher.execute("MATCH (a:User)-[:FAV_STAT]-(m:Station) WHERE a.name='Dave' RETURN m.numBikes")

# Action 5: User takes a bike from their favorite station
graph.cypher.execute("MATCH (a:User)-[:FAV_STAT]-(m:Station) WHERE a.name='Dave' SET a.borrowing = 'True', m.numBikes = m.numBikes - 1 CREATE (a)-[:BORROWED_FROM]->(m)")

# Action 6: User looks at which station next to the current station has empty spots
graph.cypher.execute("MATCH (a:User)-[:FAV_STAT]-(m:Station),(m:Station)-[:NEXT]->(o:Station) WHERE a.name='Dave' RETURN o.loc, o.racks-o.numBikes")

# Action 7: User docks their bike at the new location
graph.cypher.execute("MATCH (a:User),(b:Station) WHERE a.name='Dave' AND b.loc='Tribeca' CREATE (a)-[:DOCKED]->(b) SET a.borrowing='False', b.numBikes = b.numBikes + 1")

# Action 8: User updates ther favorite station
graph.cypher.execute("MATCH (a)-[r:FAV_STAT]->(b), (a)-[:DOCKED]->(c) WHERE a.name='Dave' DELETE r CREATE (a)-[:FAV_STAT]->(c)")


