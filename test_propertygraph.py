"""
File: test_propertygraph.py
Description: Unit tests for the Node, Relationship, and PropertyGraph classes
Author: Diya Ganesh
"""

from propertygraph import Node, Relationship, PropertyGraph
import pytest

@pytest.fixture
def node_a():
    return Node(name="A", category="Test", props={"key1": "value1"})

@pytest.fixture
def node_b():
    return Node(name="B", category="OtherTest")

@pytest.fixture
def node_c():
    return Node(name="C", category="Test")

@pytest.fixture
def relationship_connected():
    return Relationship("Connected")

@pytest.fixture
def relationship_friend():
    return Relationship("Friend", {"since": "2000"})

@pytest.fixture
def example_graph():
    return PropertyGraph()

def test_constructor():
    test_node = Node("test", "test2")
    test_relation = Relationship("test")
    test_graph = PropertyGraph()
    assert isinstance(test_node, Node), "constructor failed to create a node"
    assert isinstance(test_relation, Relationship), "constructor failed to create a relationship"
    assert isinstance(test_graph, PropertyGraph), "constructor failed to create a PropertyGraph"

"""
--------------------------------------------------------------------------------
TESTS FOR NODE CLASS
--------------------------------------------------------------------------------
"""

def test_node_getitem(node_a):
    assert node_a["key1"] == "value1", "failed to get node key1"
    assert node_a["key2"] is None, "expected None for key2"

def test_node_setitem(node_a):
    node_a["key2"] = "value2"
    assert node_a.props["key2"] == "value2", "failed to set prop key2: value2"

def test_node_equality(node_a, node_b):
    assert node_a == node_a, "equality fails"
    assert node_b == node_b, "equality fails"
    assert node_a != node_b, "inequality fails"

def test_node_hash(node_a, node_b):
    assert hash(node_a) == hash(node_a), "hash fails"
    assert hash(node_b) == hash(node_b), "hash fails"
    assert hash(node_a) != hash(node_b), "hash fails"

def test_node_repr(node_a):
    assert repr(node_a) == "A:Test\t{'key1': 'value1'}", "repr not formatted correctly"

"""
--------------------------------------------------------------------------------
TESTS FOR RELATIONSHIP CLASS
--------------------------------------------------------------------------------
"""

def test_relationship_getitem(relationship_friend, relationship_connected):
    assert relationship_friend["since"] == "2000", "failed to get relationship since"
    print(relationship_friend.props)
    assert relationship_connected["since"] is None, "expected None for since"

def test_relationship_setitem(relationship_connected):
    relationship_connected["through"] = "university"
    assert relationship_connected.props["through"] == "university", "failed to set prop through"

def test_relationship_repr(relationship_friend):
    assert repr(relationship_friend) == ":Friend {'since': '2000'}", "repr not formatted correctly"

"""
--------------------------------------------------------------------------------
TESTS FOR PROPERTYGRAPH CLASS
--------------------------------------------------------------------------------
"""

def test_add_node(example_graph, node_a):
    example_graph.add_node(node_a)
    assert node_a in example_graph.nodes, "failed to add node"

def test_add_relationship(example_graph, node_a, node_b, relationship_connected):
    example_graph.add_relationship(node_a, node_b, relationship_connected)
    assert (node_b, relationship_connected) in example_graph.nodes[node_a], "failed to add relationship"

def test_get_nodes(example_graph, node_a, node_b):
    example_graph.add_node(node_a)
    example_graph.add_node(node_b)
    # all nodes
    all_nodes = example_graph.get_nodes()
    assert node_a in all_nodes, "failed to get node a for no constraints"
    assert node_b in all_nodes, "failed to get node b for no constraints"

    # only name constraint set
    only_a = example_graph.get_nodes(name="A")
    assert node_a in only_a, "failed to get node a for name constraint"
    assert node_b not in only_a, "expected no node b for name constraint"

    # only category constraint set
    only_test = example_graph.get_nodes(category="Test")
    assert node_a in only_test, "failed to get node a for category constraint"
    assert node_b not in only_test, "expected no node b for category constraint"

    # only key constraint set
    only_key1 = example_graph.get_nodes(key="key1")
    assert node_a in only_key1, "failed to get node a for key1 constraint"
    assert node_b not in only_key1, "expected no node b for key1 constraint"

    # only value constraint set
    only_value1 = example_graph.get_nodes(value="value1")
    assert node_a in only_value1, "failed to get node a for value constraint"
    assert node_b not in only_value1, "expected no node b for value constraint"

    # all constraints set
    all_constraints = example_graph.get_nodes(name="A", category="Test", key="key1", value="value1")
    assert node_a in all_constraints, "failed to get node a for all constraints"
    assert node_b not in all_constraints, "expected no node b for all constraints"

def test_adjacent(example_graph, node_a, node_b, node_c, relationship_connected, relationship_friend):
    example_graph.add_node(node_a)
    example_graph.add_node(node_b)
    example_graph.add_node(node_c)
    example_graph.add_relationship(node_a, node_b, relationship_connected)

    # no categories specified
    a_adj = example_graph.adjacent(node_a)
    assert node_b in a_adj, "failed to get node b in a adjacent nodes with no categories specified"
    assert node_c not in a_adj, "expected no node c in a adjacent nodes with no categories specified"

    example_graph.add_relationship(node_a, node_c, relationship_friend)

    # node category specified
    a_adj_othertest = example_graph.adjacent(node_a, node_category="Test")
    assert node_b not in a_adj_othertest, "expected no node b in a adjacent nodes with node category specified"
    assert node_c in a_adj_othertest, "failed to get node c in a adjacent nodes with node category specified"

    # relation category specified
    a_adj_connected = example_graph.adjacent(node_a, rel_category="Connected")
    assert node_b in a_adj_connected, "failed to get node b in a adjacent nodes with relation category specified"
    assert node_c not in a_adj_connected, "expected no node c in a adjacent nodes with relation category specified"

def test_subgraph(example_graph, node_a, node_b, node_c, relationship_connected):
    example_graph.add_node(node_a)
    example_graph.add_node(node_b)
    example_graph.add_node(node_c)
    example_graph.add_relationship(node_a, node_b, relationship_connected)
    example_graph.add_relationship(node_b, node_c, relationship_connected)
    example_subgraph = example_graph.subgraph([node_a, node_b, node_c])
    assert node_a in example_subgraph.nodes.keys(), "failed to create node a in subgraph"
    assert node_b in example_subgraph.nodes.keys(), "failed to create node b in subgraph"
    assert node_c in example_subgraph.nodes.keys(), "failed to create node c in subgraph"
    assert (node_b, relationship_connected) in example_subgraph.nodes[node_a], \
        "failed to create relationship in subgraph"

def test_property_graph_repr(example_graph, node_a, node_b, relationship_connected):
    example_graph.add_node(node_a)
    example_graph.add_node(node_b)
    example_graph.add_relationship(node_a, node_b, relationship_connected)
    expected_repr = "A:Test\t{'key1': 'value1'}\n\t:Connected {} B:OtherTest\t{}\nB:OtherTest\t{}\n"
    assert repr(example_graph) == expected_repr, "repr failed to match expected repr"