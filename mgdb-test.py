#!/usr/bin/env python3
""" Tests the mgdb library by creating a graph and running traversals on it """
import mgdb

# Create a new Graph Database Instance
db = mgdb.GraphDB()

db.addNode("A", {"type": "router", "model": "N7700"})
db.addNode("B", {"type": "switch", "model": "N5600"})
db.addNode("C")
db.addNode("D")
db.addNode("E")
db.addNode("F")

db.mergeNodeProperties("C", {"type": "router", "model": "N7700"})
db.mergeNodeProperties("D", {"type": "switch", "model": "N5600"})


db.addRelationship("10G", "A", "B", props={"MTU": "1500"})
db.addRelationship("1G", "A", "D", weight=10)
db.addRelationship("10G", "B", "C")
db.addRelationship("10G", "B", "E")
db.addRelationship("10G", "C", "D")
db.addRelationship("1G", "D", "B", weight=10)
db.addRelationship("10G", "D", "E")
db.addRelationship("10G", "E", "A")


db.mergeRelProperties("10G", "A", "B", {"type": "Ethernet", "MTU": "9000"})

print(db.nodes["A"]["type"], db.nodes["A"]["model"])

print(db.nodes["A"]["_rels"])

print(db.getNodeProps("A"))
print(db.getRelProps("10G", "A", "B"))
print(db.getRelProps("10G", "E", "A"))

print(db.getRelationships("A"))
print(db.getRelationships("F"))

db.traverse("A", "E")
