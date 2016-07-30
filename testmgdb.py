#!/usr/bin/env python3
# Copyright (c) 2016 "Jonathan Yantis"
#
# This file is a part of MiniGraphDB.
#
#    This program is free software: you can redistribute it and/or  modify
#    it under the terms of the GNU Affero General Public License, version 3,
#    as published by the Free Software Foundation.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#    As a special exception, the copyright holders give permission to link the
#    code of portions of this program with the OpenSSL library under certain
#    conditions as described in each individual source file and distribute
#    linked combinations including the program with the OpenSSL library. You
#    must comply with the GNU Affero General Public License in all respects
#    for all of the code used other than as permitted herein. If you modify
#    file(s) with this exception, you may extend this exception to your
#    version of the file(s), but you are not obligated to do so. If you do not
#    wish to do so, delete this exception statement from your version. If you
#    delete this exception statement from all source files in the program,
#    then also delete it in the license file.
#
"""
Tests the mgdb library by creating a graph, querying nodes/relationships, and
running several traversals on the graph. See the sample.png for a whiteboard
image of the test graph.
"""
import pprint
import mgdb

# Load the sample graph data
print("Loading MiniGraphDB nodes and relationships based " +
      "on sample graph...", end="")

# Create a new Graph Database Instance
db = mgdb.MiniGraphDB()

# Add nodes to the graph, append properties to some
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
db.addRelationship("10G", "F", "A", props={"MTU": "1500"})
db.addRelationship("10G", "F", "G", props={"MTU": "1500"})
db.addRelationship("10G", "A", "G", props={"MTU": "1500"})
db.addRelationship("10G", "G", "H", props={"MTU": "1500"})

# Update properties on an existing relationship
db.mergeRelProperties("10G", "A", "B", {"type": "Ethernet", "MTU": "9000"})

print("[success]\n")


## Various tests of graph database
print("Testing MiniGraphDB with Various Queries and Traversals...")

# Instantiate a pretty printer
pp = pprint.PrettyPrinter(indent=2, width=4, depth=1)

print('\nNode A Property "type": db.nodes["A"]["type"] ')
pp.pprint({"Type": db.nodes["A"]["type"]})

print('\nNode "A" Property Dump: db.getNodeProps("A")')
pp.pprint(db.getNodeProps("A"))

print('\nNon-existent Node Property Dump: db.getNodeProps("Z")')
try:
    print(db.getNodeProps("Z"))
except Exception as e:
    print("Caught Exception:", e)

print('\nRelationship (D)-[e:1G]->(B) Property Dump: db.getRelProps("1G", "D", "B")')
pp.pprint(db.getRelProps("1G", "D", "B"))

print("\nNon-existent Relationship (A)-[e:1G]->(C) db.getRelProps(...) Dump: ")
try:
    pp.pprint(db.getRelProps("1G", "A", "C"))
except Exception as e:
    print("Caught Exception:", e)

print("\nRelationships from A: db.getRelationships(A)")
print(db.getRelationships("A"))

print("\nRelationships from E: db.getRelationships(E)")
print(db.getRelationships("E"))

print("\nBFS Traversal A -> E on Relationships [10G, 1G]:")
print(db.traverse("A", "E", allowRels=["1G", "10G"]))

print("\nDFS Traversal A -> E on any Relationship Type:")
print(db.traverse("A", "E", algo="DFS"))

print("\nBFS Traversal E -> F (orphaned) on any Relationship Type:")
print(db.traverse("E", "F"))

print("\nBFS Traversal F -> E on any Relationship Type:")
print(db.traverse("F", "E"))

print("\nBFS Traversal A -> A on any Relationship Type (always SPF):")
print(db.traverse("A", "A"))

print("\nDFS Traversal A -> A on any Relationship Type (path length varies):")
print(db.traverse("A", "A", algo="DFS"))

print("\nBFS Traversal A -> A on 10G Links Only:")
print(db.traverse("A", "A", allowRels=["10G"], algo="BFS"))

print("\nDFS Traversal A -> A on 1G Links Only:")
print(db.traverse("A", "A", allowRels=["1G"], algo="DFS"))

print('\nChecking for Loops Starting at F: db.hasloop("F")')
print(db.hasloop("F"))

print('\nChecking for Loops Starting at G: db.hasloop("G")')
print(db.hasloop("G"))

print("\nCreate new MiniGraphDB Instance (loopdb) A -> B -> C -> B for Testing hasloop()")

loopdb = mgdb.MiniGraphDB()

loopdb.addNode("A")
loopdb.addNode("B")
loopdb.addNode("C")

loopdb.addRelationship("Connected", "A", "B")
loopdb.addRelationship("Connected", "B", "C")
loopdb.addRelationship("Connected", "C", "B")


print('\nChecking for Loops Starting at A: loopdb.hasloop("A")')
print(loopdb.hasloop("A"))

print('\nDone for now! Please enjoy...\n')
