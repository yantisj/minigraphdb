#!/usr/bin/env python3
"""
Mini Graph Database

Description: Implements a mini directed graph database in memory. Nodes are
stored as dictionary data structures. Relationships are stored on each node as a
list of relationships with their own properties and pointers to other nodes.
Both nodes and relationships can contain key value properties, stored in the
dictionary data structure.
"""
import queue

class GraphDB:
    """
    GraphDB is a simple implementation of a directed graph of nodes and
    relationships (edges and vertices), each with properties, along with both
    breadth-first and depth-first traversal algorithms.
    """

    def __init__(self):
        """ Initializes GraphDB Instance """

        # Nodes is a dictionary of all nodes in the DB
        self.nodes = dict()


    def addNode(self, name, props=None):
        """
        Adds a node to the database

        Inputs: name  - Uniqueue name of node
                props - Optional node properties dictionary
        """

        if name in self.nodes:
            raise Exception("Node" + name + "already exists, did you mean to call mergeNode?")
        else:
            self.nodes[name] = dict()

            # Initialize empty relationships dictionary
            self.nodes[name]["_rels"] = dict()

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

            # Only return public properties, underscored properties are hidden
            for p in self.nodes[name]:
                if p[:1] != "_":
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
            if name not in self.nodes[srcNode]["_rels"]:

                # Relationship is a dictionary object based on a (name, dstNode)
                # tuple key between two nodes
                rel = self.nodes[srcNode]["_rels"][(name, dstNode)] = dict()
                rel["_dst"] = self.nodes[dstNode]
                rel["_weight"] = weight

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
            if (name, dstNode) in self.nodes[srcNode]["_rels"]:
                rel = self.nodes[srcNode]["_rels"][(name, dstNode)]

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
            if (name, dstNode) in self.nodes[srcNode]["_rels"]:
                rel = self.nodes[srcNode]["_rels"][(name, dstNode)]
                props = dict()

                # Only return public properties, underscored properties are hidden
                for p in rel:
                    if p[:1] != "_":
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
            for (relName, dstNode) in self.nodes[name]["_rels"]:
                rels.append((relName, dstNode))

            return rels

        else:
            raise Exception("Node", name, "not found in database")


    def traverse(self, startNode, endNode, rels=None, ttype="BFS"):
        """
        Traverse Graph, starting at startNode until endNode is found.
        Defaults to a Breadth First Search, but can also perform a
        depth first search if desired.

        Inputs: startNode - Start Traversal from this node
                endNode   - Search for path to endNode
                rels      - Optional List of relationship names to traverse
                            None traverses all relationship names
                ttype     - Type of search (BFS, DFS), defaults to BFS

        Returns: tuple (found (bool), path (dict))
        """

        # Ensure both nodes exist in DB, they don't have to be connected
        if set((startNode, endNode)).issubset(self.nodes):

            if ttype == "BFS":
                return self._traverseBFS(startNode, endNode, rels=None)
        else:
            raise Exception("Nodes", startNode, endNode, "not found in DB")

    def _traverseBFS(self, startNode, endNode, rels=None):
        """
        Breadth First Traversal of Graph searching for endNode, starting at startNode

        Inputs:
            startNode => Start Traversal from this node
            endNode => Search for this node

        Returns: tuple of (found [bool], path[list])
        """

        # Initiate a queue with a sane maxsize value
        Q = queue.LifoQueue(maxsize=10000)

        # Add startNode to Queue
        Q.put(startNode)

        # Create a dictionary of visited nodes
        visited = dict()

        # Add startNode to visited along with distance and null parent value
        visited[startNode]["distance"] = 0
        visited[startNode]["parent"] = None

        while Q.full():

            cnode = Q.get()
            print(cnode)
