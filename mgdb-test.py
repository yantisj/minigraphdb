#!/usr/bin/env python3
""" Tests the mgdb library by creating a graph and running traversals on it """
import pprint
import mgdb

# Create a new Graph Database Instance
db = mgdb.GraphDB()

# Add nodes to graph, append properties to some
db.addNode("A", {"type": "router", "model": "N7700"})
db.addNode("B", {"type": "switch", "model": "N5600"})
db.addNode("C", {"type": "router", "model": "N7700"})
db.addNode("D", {"type": "switch", "model": "N5600"})
db.addNode("E")
db.addNode("F")

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
db.addRelationship("1G", "A", "F", props={"MTU": "1500"})

# Update properties on an existing relationship
db.mergeRelProperties("10G", "A", "B", {"type": "Ethernet", "MTU": "9000"})


## Various tests of mgdb

# Instantiate a pretty printer
pp = pprint.PrettyPrinter(indent=2, width=4, depth=1)

print("\nNode A Type and Model values")
pp.pprint([db.nodes["A"]["type"], db.nodes["A"]["model"]])

print("\nNode A Property Dump")
pp.pprint(db.getNodeProps("A"))

print("\nRelationship r Property Dump: (D)-[r:1G]->(B)")
pp.pprint(db.getRelProps("1G", "D", "B"))

print("\nA's Relationships")
print(db.getRelationships("A"))

print("\nF's Relationships (null)")
print(db.getRelationships("F"))

print("\nTraverse using BFS from A -> E on relationships [10G, 1G]")
print(db.traverse("A", "E", allowRels=["1G", "10G"]))

print("\nTraverse using BFS from A -> D on relationship [10G] only")
print(db.traverse("A", "D", allowRels=["10G"]))

print("\nTraverse from F -> E (orphaned) on any relationship type")
print(db.traverse("F", "E"))

print("\nTraverse from E -> F on any relationship type")
print(db.traverse("E", "F"))

print("\nTraverse from A -> A on any relationship type")
print(db.traverse("A", "A"))

print("\nTraverse from A -> A on 10G links only")
print(db.traverse("A", "A", allowRels=["10G"]))

print("\nTraverse from A -> A on 1G links only")
print(db.traverse("A", "A", allowRels=["1G"]))

