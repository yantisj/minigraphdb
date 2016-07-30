#!/usr/bin/env python3
"""
Minimal Graph Database (MGDB)

Description: Implements a mini directed graph database in memory. Nodes are
stored as dictionary data structures. Relationships are stored on each node as a
list of relationships with their own properties and pointers to other nodes.
Both nodes and relationships can contain key value properties, stored in a
dictionary data structure.

Node data structure: nodes holds all nodes. Each node in nodes is a dict().
New nodes are initialized with a nodes[name]['__rels'] dictionary of outgoing
relationships. Each relationship key is a tuple of (relationship_name, dstNode)

Relationship data structure: Relationships are stored as dictionaries and added
to the srcNode's __rels dictionary. We keep track of __src, __dst and __weight for 
future capabilities.

Future of MGDB:

Undirected Traversals: It should be easy to reverse the graph traversal direction
as well as add directionless graph traversal by adding an __inrels dictionary to
each node to keep track of all incoming relationships. The traversal algoriths
could be modified to traverse in either/both directions.

Where Clauses: Traversal algorithms could be modified to check whether
properties on nodes or relationships meet certain criteria, such as (==, !=, <,
>, etc)



"""
import queue
from collections import defaultdict

class GraphDB:
    """
    GraphDB is a simple implementation of a directed graph of nodes and
    relationships (edges and vertices), each with properties, along with both
    breadth-first and depth-first traversal algorithms.
    """

    def __init__(self):
        """ Initializes GraphDB, creates nodes dict() """

        # Nodes is a dictionary of all nodes in the DB
        self.nodes = dict()


    def addNode(self, name, props=None):
        """
        Adds a node to the database

        Inputs: name => Unique name of node
                props => Optional node properties dictionary
        """

        if name in self.nodes:
            raise Exception("Node" + name + "already exists, did you mean to call mergeNode?")
        else:

            # Initialize empty node and relationships dictionary
            self.nodes[name] = dict()
            self.nodes[name]["__rels"] = dict()

            # If optional properties defined, merge those with new node
            if props:
                if isinstance(props, dict):
                    self.mergeNodeProperties(name, props)


    def mergeNodeProperties(self, name, props):
        """
        Merge node properties dictionary. Updates existing properties if the exist, or create new
        ones if they don't

        Inputs:
        - name: name of node
        - props: dictionary of key/values to merge
        """

        if name in self.nodes:

            for p in props:
                self.nodes[name][p] = props[p]

        else:
            raise Exception("Could not locate node to merge properties on:", name)


    def getNodeProps(self, name):
        """
        Get the properties for a node as a dict()

        Inputs: name - Name of node

        Returns: dict() of properties
        """

        if name in self.nodes:
            props = dict()

            # Only return public properties, double underscored properties are hidden
            for p in self.nodes[name]:
                if p[:2] != "__":
                    props[p] = self.nodes[name][p]

            return props
        else:
            raise Exception("No node named", name, "found in database")


    def addRelationship(self, name, srcNode, dstNode, props=None, weight=1):
        """
        Adds a relationship 'name' from srcnode to dstnode

        Inputs:
        Inputs: name: Relationship Name
                srcNode: Source Node Name
                dstNode: Destination Node Name
                weight: Optional Weight Value, defaults to 1
        """

        # Ensure both nodes exist in DB
        if set((srcNode, dstNode)).issubset(self.nodes):

            # Ensure relationship does not already exist
            if name not in self.nodes[srcNode]["__rels"]:

                # Relationship is a dictionary object based on a (name, dstNode)
                # tuple key between two nodes
                rel = self.nodes[srcNode]["__rels"][(name, dstNode)] = dict()
                rel["__src"] = self.nodes[srcNode]
                rel["__dst"] = self.nodes[dstNode]
                rel["__weight"] = weight

                # If optional properties defined, merge those with new relationship
                if props:
                    if isinstance(props, dict):
                        self.mergeRelProperties(name, srcNode, dstNode, props)

            # Ensure relationship name does not already exist between two nodes
            else:
                raise Exception("Relationship", name, "already exists between", srcNode, dstNode)

        else:
            raise Exception("Could not find nodes in DB to link:", srcNode, dstNode)


    def mergeRelProperties(self, name, srcNode, dstNode, props):
        """
        Merge relationship properties dictionary. Updates existing properties if the exist, or
        creates new ones if they don't.

        Inputs: name => name of relationship
                srcNode => Source Node of Relationship
                dstNode => Destination Node of Relationship
                props => dictionary of key/values to merge
        """

        # Ensure both nodes exist in DB
        if set((srcNode, dstNode)).issubset(self.nodes):

            # Ensure Relationship Exists
            if (name, dstNode) in self.nodes[srcNode]["__rels"]:
                rel = self.nodes[srcNode]["__rels"][(name, dstNode)]

                for p in props:
                    rel[p] = props[p]


    def getRelProps(self, name, srcNode, dstNode):
        """
        Get the properties for a relationship as a dict()

        Inputs: name => Name of relationship
                srcNode => Source Node
                dstNode => Destination Node

        Returns: dict() of properties
        """

        # Ensure both nodes exist in DB
        if set((srcNode, dstNode)).issubset(self.nodes):

            # Ensure Relationship Exists
            if (name, dstNode) in self.nodes[srcNode]["__rels"]:
                rel = self.nodes[srcNode]["__rels"][(name, dstNode)]
                props = dict()

                # Only return public properties, double underscored properties are hidden
                for p in rel:
                    if p[:2] != "__":
                        props[p] = rel[p]

                return props
            else:
                raise Exception("Nodes", srcNode, dstNode, "exist in database, but no relationship",
                                name, "exists between them")
        else:
            raise Exception("Nodes not found in database", srcNode, dstNode)


    def getRelationships(self, name):
        """
        Returns list of tuple relationships node (name) has.

        Input: name => Name of node

        Returns: [(relname, dstNode),{...}]
        """

        # Ensure Node exists in DB
        if name in self.nodes:
            rels = []

            # Append each relationship tuple to rels list
            for (relName, dstNode) in self.nodes[name]["__rels"]:
                rels.append((relName, dstNode))

            return rels

        else:
            raise Exception("Node", name, "not found in database")


    def traverse(self, startNode, endNode, allowRels=None, algo="BFS"):
        """
        Traverse Graph, starting at startNode until endNode is found.
        Defaults to a Breadth First Search, but can also perform a
        depth first search if desired.

        Inputs: startNode => Start Traversal from this node
                endNode => Search for path to endNode
                allowRels => Optional List of relationship names to traverse
                             None traverses all relationship names
                algo => Type of search (BFS, DFS), defaults to BFS

        Returns: tuple (found (bool), path (dict))
        """

        # Ensure both nodes exist in DB, they don't have to be connected
        if set((startNode, endNode)).issubset(self.nodes):

            if algo == "BFS":
                return self._traverseBFS(startNode, endNode, allowRels=allowRels)
            elif algo == "DFS":
                return self._traverseDFS(startNode, endNode, allowRels=allowRels)
            else:
                raise Exception("Unknown Traversal Algorithm:", algo)
        else:
            raise Exception("Nodes", startNode, endNode, "not found in DB")


    def _traverseBFS(self, startNode, endNode, allowRels=None, hasloop=False):
        """
        Breadth First Traversal of Graph searching for endNode from startNode

        Inputs:
            startNode => Start Traversal from this node
            endNode => Search for this node
            allowRels => list of allowed relationship traversal names (default all)
            hasLoop => Optional variable for use with hasLoop to detect looped graphs

        Returns: tuple of (found [bool], path[list])
        """

        # Initialize a queue with a sane maxsize value
        Q = queue.Queue(maxsize=10000)

        # Add startNode to the Queue
        Q.put(startNode)

        # Create a dictionary of visited nodes
        visited = dict()

        # Add startNode to visited along with distance and null parent value
        visited[startNode] = dict()
        visited[startNode]["distance"] = 0
        visited[startNode]["parent"] = None

        # Classic BFS Algorithm, keep processing relationships until queue is empty
        while not Q.empty():

            # Dequeue Current Node
            cnode = Q.get()

            # make sure to visit each node connected from here
            # rel => (name, dstNode)
            for (rname, adjacent) in self.getRelationships(cnode):

                # Make sure we are traversing allowed relationship types
                if allowRels is None or rname in allowRels:

                    # Only searching for loops, and loop found
                    if hasloop and adjacent in visited:
                        return(True, self._getPath(cnode, visited) + [[cnode, rname, startNode]])

                    # Newly discovered node, record in visited
                    elif adjacent not in visited:
                        visited[adjacent] = dict()
                        visited[adjacent]["distance"] = visited[cnode]["distance"] + 1
                        visited[adjacent]["parent"] = cnode
                        visited[adjacent]["rname"] = rname

                        # Found the endNode
                        if adjacent == endNode:
                            return (True, self._getPath(endNode, visited))

                        # Enqueue all nodes that are not endNode
                        Q.put(adjacent)

                    # Check for loop back to startNode
                    # startNode is equal to endNode and is adjacent
                    elif adjacent == startNode == endNode:

                        # Return True along with path (add last leg to current path)
                        return(True, self._getPath(cnode, visited) + [[cnode, rname, startNode]])

        # Node not found
        return(False, [])


    def _getPath(self, endNode, visited):
        """ Returns a path from startNode to endNode for use with BFS"""

        cnode = endNode
        path = []

        while visited[cnode]["parent"] is not None:
            path.append([visited[cnode]["parent"], visited[cnode]["rname"], cnode])
            cnode = visited[cnode]["parent"]

        # Return reversed path
        return [hop for hop in path[::-1]]
    

    def hasloop(self, startNode):
        """
        Calls _traverseBFS with an unreachable endNode, looking for any nodes
        that have been visited. If it finds a visited node, there must be a loop.

        Input: startNode => Start searching for loops from here

        Returns: (bool, [path])
        """
        return self._traverseBFS(startNode, "__INFINITY__", hasloop=True)


    def _traverseDFS(self, startNode, endNode, allowRels=None):
        """
        Depth First Traversal of Graph searching for endNode from startNode

        Inputs:
            startNode => Start Traversal from this node
            endNode => Search for this node

        Returns: tuple of (found [bool], path[list])
        """

        # Initiate a stack with a sane maxsize value
        S = queue.LifoQueue(maxsize=10000)

        # Keep track of paths in dictionary
        path = defaultdict(list)

        # Add startNode to Queue
        S.put(startNode)

        # Create a dictionary of visited nodes
        visited = dict()

        # Classic DFS Algorithm, keep digging until stack is empty
        while not S.empty():

            # Pop Current Node
            cnode = S.get()

            # first time visiting cnode
            if cnode not in visited and cnode not in S.queue:

                visited[cnode] = dict()

                # If we are starting out, make sure startNode has default populated values
                if S.empty() and cnode == startNode:
                    visited[cnode] = []

            # Get all relationships of cnode to add destinations to stack
            # rel => (name, dstNode)
            for (rname, adjacent) in self.getRelationships(cnode):

                # Make sure we are traversing allowed relationship types
                if allowRels is None or rname in allowRels:

                    if adjacent == endNode and len(path[cnode]):
                        return(True, path[cnode] + [[cnode, rname, adjacent]])

                    elif adjacent not in visited:
                        S.put(adjacent)

                        path[adjacent] = path[cnode] + [[cnode, rname, adjacent]]

        # Node not found
        return(False, [])



