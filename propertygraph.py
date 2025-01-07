"""
File: propertygraph.py
Description: An implementation of a PropertyGraph consisting of
Node and Relationship objects.  Nodes and Relationships carry
properties.  Property graphs are used to represent connected knowledge.

Author: Diya Ganesh
"""

class Node:

    def __init__(self, name, category, props=None):
        """ Class constructor """
        self.name = name
        self.category = category
        if props is None:
            self.props = {}
        else:
            self.props = props

    def __getitem__(self, key):
        """ Fetch a property from the node using []
         return None if property doesn't exist """
        if key in self.props:
            return self.props[key]
        else:
            return None

    def __setitem__(self, key, value):
        """ Set a node property with a specified value using [] """
        self.props[key] = value

    def __eq__(self, other):
        """ Two nodes are equal if they have the same
        name and category irrespective of their properties """
        return self.name == other.name and self.category == other.category

    def __hash__(self):
        """ By making Nodes hashable we can now
        store them as keys in a dictionary! """
        return hash(str(self.name) + str(self.category))

    def __repr__(self):
        """ Output the node as a string in the following format:
        name:category<tab>properties.
        Note: __repr__ is more versatile than __str__ """
        return str(self.name) + ":" + str(self.category) + "\t" + str(self.props)

class Relationship:

    def __init__(self, category, props=None):
        """ Class constructor """
        self.category = category
        if props is None:
            self.props = {}
        else:
            self.props = props

    def __getitem__(self, key):
        """ Fetch a property from the node using []
         return None if property doesn't exist """
        if key in self.props:
            return self.props[key]
        else:
            return None

    def __setitem__(self, key, value):
        """ Set a node property with a specified value using [] """
        self.props[key] = value

    def __repr__(self):
        """ Output the relationship as a string in the following format:
        :category<space>properties.
        Note: __repr__ is more versatile than __str__ """
        return ":" + str(self.category) + " " + str(self.props)

class PropertyGraph:

    def __init__(self):
        """ Construct an empty property graph """
        self.nodes = {}

    def add_node(self, node):
        """ Add a node to the property graph """
        if node not in self.nodes:
            self.nodes[node] = []

    def add_relationship(self, src, targ, rel):
        """ Connect src and targ nodes via the specified directed relationship.
        If either src or targ nodes are not in the graph, add them.
        Note that there can be many relationships between two nodes! """
        if src not in self.nodes:
            self.add_node(src)
        if targ not in self.nodes:
            self.add_node(targ)
        self.nodes[src].append((targ, rel))

    def get_nodes(self, name=None, category=None, key=None, value=None):
        """ Return the SET of nodes matching all the specified criteria.
        If the criterion is None it means that the particular criterion is ignored."""
        node_set = []
        for node in self.nodes.keys():
            if ((name is None or name == node.name) and
                    (category is None or category == node.category) and
                    (key is None or key in node.props.keys()) and
                    (value is None or value in node.props.values())):
                node_set.append(node)

        return node_set

    def adjacent(self, node, node_category=None, rel_category=None):
        """ Return a set of all nodes that are adjacent to node.
        If specified include only adjacent nodes with the specified node_category.
        If specified include only adjacent nodes connected via relationships with
        the specified rel_category """
        adj_set = []
        for rel_node in self.nodes[node]:
            adj_node = rel_node[0]
            relation = rel_node[1]
            if ((node_category is None or node_category == adj_node.category) and
                    (rel_category is None or rel_category == getattr(relation, 'category', None))):
                adj_set.append(adj_node)
        return adj_set

    def subgraph(self, nodes):
        """ Return the subgraph as a PropertyGraph consisting of the specified
        set of nodes and all interconnecting relationships """
        graph = PropertyGraph()
        for node in nodes:
            graph.add_node(node)
            for rel_node in self.nodes[node]:
                adj_node = rel_node[0]
                rel = rel_node[1]
                if adj_node in nodes:
                    graph.add_relationship(node, adj_node, rel)
        return graph

    def __repr__(self):
        """ A string representation of the property graph
        Properties are not displaced.

        Node
            Relationship Node
            Relationship Node
            .
            .
            etc.
        Node
            Relationship Node
            Relationship Node
            .
            .
            etc.
        .
        .
        etc.
        """
        graph_repr = ""
        for node in self.nodes.keys():
            graph_repr += str(node) + "\n"
            for rel_node in self.nodes[node]:
                adj_node = rel_node[0]
                relation = rel_node[1]
                graph_repr += f"\t{relation} {adj_node}\n"

        return graph_repr