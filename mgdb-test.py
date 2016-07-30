#!/usr/bin/env python3
""" Tests the mgdb library by creating a graph and running traversals on it """
import pprint
import mgdb


print("Loading Database nodes and relationships based " +
      "on sample graph...", end="")

# Create a new Graph Database Instance
db = mgdb.GraphDB()

# Add nodes to graph, append properties to some
db.addNode("A", {"type": "router", "model": "N7700"})
db.addNode("B", {"type": "switch", "model": "N5600"})
db.addNode("C", {"type": "router", "model": "N7700"})
db.addNode("D", {"type": "switch", "model": "N5600"})
db.addNode("E")
db.addNode("F")
db.addNode("G")
db.addNode("H")

# Add some properties to existing nodes
db.mergeNodeProperties("E", {"type": "router", "model": "N7700"})
db.mergeNodeProperties("F", {"type": "switch", "model": "N5600"})
db.mergeNodeProperties("A", {"role": "core"})

# Build relationships between nodes, add some properties, and set weight=10
# on 1G links
db.addRelationship("10G", "A", "B", props={"MTU": "1500"})
db.addRelationship("1G", "A", "D", weight=10, props={"MTU": "1500"})
db.addRelationship("10G", "B", "C", props={"MTU": "1500"})
db.addRelationship("1G", "B", "E", props={"MTU": "1500"})
db.addRelationship("10G", "C", "D", props={"MTU": "1500"})
db.addRelationship("1G", "D", "B", weight=10, props={"MTU": "9000"})
db.addRelationship("10G", "D", "E", props={"MTU": "9000"})
db.addRelationship("10G", "E", "A", props={"MTU": "9000"})
db.addRelationship("1G", "E", "A", props={"MTU": "1500"})
db.addRelationship("1G", "F", "A", props={"MTU": "1500"})
db.addRelationship("1G", "A", "G", props={"MTU": "1500"})
db.addRelationship("1G", "G", "H", props={"MTU": "1500"})

# Update properties on an existing relationship
db.mergeRelProperties("10G", "A", "B", {"type": "Ethernet", "MTU": "9000"})

print("Success!\n")


## Various tests of graph database
print("Testing MGDB with various queries and traversals")
# Instantiate a pretty printer
pp = pprint.PrettyPrinter(indent=2, width=4, depth=1)

print('\nNode A Property "type": db.nodes["A"]["type"] ')
pp.pprint({"Type": db.nodes["A"]["type"]})

print("\nNode A Property Dump: getNodeProps(A)")
pp.pprint(db.getNodeProps("A"))

print("\nRelationship (D)-[rel:1G]->(B) getRelProps Dump: ")
pp.pprint(db.getRelProps("1G", "D", "B"))

print("\ngetRelationships(A)")
print(db.getRelationships("A"))

print("\ngetRelationships(E)")
print(db.getRelationships("E"))

print("\nBFS Traversal A -> E on relationships [10G, 1G]")
print(db.traverse("A", "E", allowRels=["1G", "10G"]))

print("\nDFS Traversal A -> E on any relationship type")
print(db.traverse("A", "E", algo="DFS"))

print("\nBFS Traversal E -> F (orphaned) on any relationship type")
print(db.traverse("E", "F"))

print("\nBFS Traversal F -> E on any relationship type")
print(db.traverse("F", "E"))

print("\nBFS Traversal A -> A on any relationship type (always SPF)")
print(db.traverse("A", "A"))

print("\nDFS Traversal A -> A on any relationship type (path length varies)")
print(db.traverse("A", "A", algo="DFS"))

print("\nBFS Traversal A -> A on 10G links only")
print(db.traverse("A", "A", allowRels=["10G"], algo="BFS"))

print("\nDFS Traversal A -> A on 1G links only")
print(db.traverse("A", "A", allowRels=["1G"], algo="DFS"))

print("\nChecking for loops starting at F")
print(db.hasloop("F"))

print("\nChecking for loops starting at G")
print(db.hasloop("G"))

