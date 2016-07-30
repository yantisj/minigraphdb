# Minimal Graph Database (MiniGraphDB)

## Synopsis

MiniGraphDB implements a minimal directed graph database in memory via Python3.
Nodes are stored as dictionary data structures. Outgoing relationships are
stored on each node as a nested dictionary __rels of relationships with their
own properties and pointers to other nodes. Both nodes and relationships may
contain key value properties, stored in their respective dict data structures.

## Sample Graph

![Sample Graph](sample-graph.png)

## Data Structures

### Node data structure

nodes dict() holds all nodes. Each node in nodes is a dict() itself. New nodes
are initialized with an empty nodes[name]['__rels'] dictionary of outgoing
relationships. Each relationship key in \_\_rels is a tuple of (relationship_name, dstNode).

### Relationship data structure: 

Relationships are stored as dicts and added to the srcNode's __rels dictionary.
We keep track of __src, __dst and __weight for future capabilities, but
currently the (relationship_name, dstNode) key in __rels suffices for all
current needs.

### Traversals

MiniGraphDB supports both breadth-first and depth-first traversals on the graph.

## Usage

To load the sample graph, test queries and well as run traversal algorithms,
execute ./testmgdb.py on any machine with a Python3.4+ interpreter installed.
There are no dependencies outside the standard libraries.

## Sample Output
```
Loading MiniGraphDB nodes and relationships based on sample graph...[success]

Testing MiniGraphDB with Various Queries and Traversals...

Node A Property "type": db.nodes["A"]["type"]
{ 'Type': 'router'}

Node "A" Property Dump: db.getNodeProps("A")
{ 'model': 'N7700',
  'role': 'core',
  'type': 'router'}

Non-existent Node Property Dump: db.getNodeProps("Z")
Caught Exception: No node named Z found in database

Relationship (D)-[e:1G]->(B) Property Dump: db.getRelProps("1G", "D", "B")
{ 'MTU': '9000'}

Non-existent Relationship (A)-[e:1G]->(C) db.getRelProps(...) Dump:
Caught Exception: Nodes A, C exist in database, but no relationship [1G] exists from A -> C

Outgoing Relationships from A: db.getRelationships(A)
[('10G', 'B'), ('10G', 'G'), ('1G', 'D')]

Outgoing Relationships from E: db.getRelationships(E)
[('10G', 'A'), ('1G', 'A')]

BFS Traversal A -> E on Relationships [10G, 1G]:
(True, [['A', '10G', 'B'], ['B', '1G', 'E']])

DFS Traversal A -> E on any Relationship Type:
(True, [['A', '1G', 'D'], ['D', '10G', 'E']])

BFS Traversal E -> F (orphaned) on any Relationship Type:
(False, [])

BFS Traversal F -> E on any Relationship Type:
(True, [['F', '10G', 'A'], ['A', '10G', 'B'], ['B', '1G', 'E']])

BFS Traversal A -> A on any Relationship Type (always SPF):
(True, [['A', '10G', 'B'], ['B', '1G', 'E'], ['E', '10G', 'A']])

DFS Traversal A -> A on any Relationship Type (path length varies):
(True, [['A', '1G', 'D'], ['D', '1G', 'B'], ['B', '1G', 'E'], ['E', '10G', 'A']])

BFS Traversal A -> A on 10G Links Only:
(True, [['A', '10G', 'B'], ['B', '10G', 'C'], ['C', '10G', 'D'], ['D', '10G', 'E'], ['E', '10G', 'A']])

DFS Traversal A -> A on 1G Links Only:
(True, [['A', '1G', 'D'], ['D', '1G', 'B'], ['B', '1G', 'E'], ['E', '1G', 'A']])

Checking for Loops Starting at F: db.hasloop("F")
(True, ['Path TBD: Found loop around G'])

Checking for Loops Starting at G: db.hasloop("G")
(False, [])

Create new MiniGraphDB Instance (loopdb) A -> B -> C -> B for Testing hasloop()

Checking for Loops Starting at A: loopdb.hasloop("A")
(True, ['Path TBD: Found loop around B'])

Done for now! Please enjoy...
```

## Motivation

MiniGraphDB was written to explore what would be required to create a Graph
Database from scratch in Python3 using the standard libraries, with no prior
knowledge about how a Graph Database should be implemented. It should be used
for understanding potential implementations of Graph Databases only, and is not
considered production ready. MiniGraphDB was written for clarity and
understanding over performance.

## Expandibility of MiniGraphDB

MiniGraphDB could be easily expanded in many ways. Here are a few examples.

### Storing the Graph to Disk

Using the standard pickle module, a GraphDB object
could be saved to disk, and then recovered at the next runtime. This would not
be the most efficient storage method, but for the purposes of this program, it
should suffice.

### Custom Exceptions

Currently, all exceptions are generic. Specific Exceptions should be added for
cases such as NoNodeFound or NoRelationshipFound.

### Proper Test Suite

MiniGraphDB could include py-tests to unit tests as well as larger tests on the
database overall, but this would require installing modules outside of the
standard libraries.

### Undirected Traversals

It should be easy to reverse the graph traversal direction as well as add
direction-less graph traversal by adding an __inrels dictionary to each node to
keep track of all incoming relationships. The traversal algorithms could be
modified to traverse in either/both directions.

### Weighted Traversals

Traversals could take into account the __weight variable of relationships to
implement a version of Dijkstra's algorithm.

### All Shortest Paths Traversal

Combining an implemetation of Dijkstra's algorithm above, a special type of
traversal could be created to return all shortest paths, instead of only the
first path found.

### hasloop() Path Representation

Currently hasloop() only detects a loop, and does not return the loop structure.
_traverseBFS() could be modified to return the found loop with a few
modifications.

### Merge Methods

Adding mergeNode and mergeRelationship would create or merge existing nodes
and/or relationships along with updated/additional properties.

### Where Clauses

Traversal algorithms could be modified to check whether properties on nodes or
relationships meet certain criteria, such as (==, !=, <, >, etc).

### Adopt the Cypher Query Lanuage

It's possible to implement a subset of the Cypher query language to allow for
easy graph queries. Cypher is an easy to use graph query language used by Neo4j,
and is available open-source for all implementation of Graph Databases:
[Open Cypher](http://www.opencypher.org)

### Optimization

It's possible to cache traversals on graphs that do not change often. This could
be accomplished with the @functools.lru_cache decorator along with a call to
invalidate the cache as the graph changes. While there are many avenues of
optimization, none will add clarity to MiniGraphDB.

## Contributors
* Jonathan Yantis ([yantisj](https://github.com/yantisj))

## License
NetGrph is licensed under the GNU AGPLv3 License.
