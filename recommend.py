"""
File: recommend.py
Description: Book recommendation engine using propertygraph classes and methods
Author: Diya Ganesh

Code Output:
    Original Property Graph:
    Emily:Person	{}
        :Knows {} Spencer:Person	{}
        :Bought {} Database Design:Book	{'Price': '$195.00'}
    Spencer:Person	{}
        :Knows {} Emily:Person	{}
        :Knows {} Brendan:Person	{}
        :Bought {} Cosmos:Book	{'Price': '$17.00'}
        :Bought {} Database Design:Book	{'Price': '$195.00'}
    Brendan:Person	{}
        :Bought {} Database Design:Book	{'Price': '$195.00'}
        :Bought {} DNA & You:Book	{'Price': '$11.50'}
    Database Design:Book	{'Price': '$195.00'}
    Cosmos:Book	{'Price': '$17.00'}
    DNA & You:Book	{'Price': '$11.50'}
    Trevor:Person	{}
        :Bought {} Cosmos:Book	{'Price': '$17.00'}
        :Bought {} Database Design:Book	{'Price': '$195.00'}
    Paxtyn:Person	{}
        :Bought {} Database Design:Book	{'Price': '$195.00'}
        :Bought {} The Life of Cronkite:Book	{'Price': '$29.95'}
    The Life of Cronkite:Book	{'Price': '$29.95'}

    Spencer's Recommendation Graph:
    Spencer:Person	{}
    DNA & You:Book	{'Price': '$11.50'}

    Linked Subgraph:
    Spencer:Person	{}
        :Recommend {} DNA & You:Book	{'Price': '$11.50'}
    DNA & You:Book	{'Price': '$11.50'}
"""

from propertygraph import Node, Relationship, PropertyGraph

# Initialize Person Nodes
def Emily():
    return Node("Emily", "Person")

def Spencer():
    return Node("Spencer", "Person")

def Brendan():
    return Node("Brendan", "Person")

def Trevor():
    return Node("Trevor", "Person")

def Paxtyn():
    return Node("Paxtyn", "Person")

# Initialize Book Nodes
def Cosmos():
    return Node("Cosmos", "Book", {"Price": "$17.00"})

def DatabaseDesign():
    return Node("Database Design", "Book", {"Price": "$195.00"})

def LifeCronkite():
    return Node("The Life of Cronkite", "Book", {"Price": "$29.95"})

def DNAYou():
    return Node("DNA & You", "Book", {"Price": "$11.50"})

# Initialize Relationships
def Knows():
    return Relationship("Knows")

def Bought():
    return Relationship("Bought")

def Recommend():
    return Relationship("Recommend")

def RecommendationGraph():
    """
    Create a property graph based on the picture given,
    Add all nodes and relationships
    """

    rec_graph = PropertyGraph()

    # Add Knows Relationships
    rec_graph.add_relationship(Emily(), Spencer(), Knows())
    rec_graph.add_relationship(Spencer(), Emily(), Knows())
    rec_graph.add_relationship(Spencer(), Brendan(), Knows())

    # Add Bought Relationships
    rec_graph.add_relationship(Emily(), DatabaseDesign(), Bought())
    rec_graph.add_relationship(Spencer(), Cosmos(), Bought())
    rec_graph.add_relationship(Spencer(), DatabaseDesign(), Bought())
    rec_graph.add_relationship(Brendan(), DatabaseDesign(), Bought())
    rec_graph.add_relationship(Brendan(), DNAYou(), Bought())
    rec_graph.add_relationship(Trevor(), Cosmos(), Bought())
    rec_graph.add_relationship(Trevor(), DatabaseDesign(), Bought())
    rec_graph.add_relationship(Paxtyn(), DatabaseDesign(), Bought())
    rec_graph.add_relationship(Paxtyn(), LifeCronkite(), Bought())

    return rec_graph

def Recommendations(person_name, graph_type="Unlinked"):
    """
    Based on the person's name that is given, find all books they bought, all people they are connected to,
    and all books the people they are connected to bought (possible_recs). Determine which of the possible
    recommendations the person has not already bought and create a graph with the person and books as nodes.
    If the graph type is unlinked it will return the person name and book recommendations as nodes,
    if the graph type is linked it will return the book recommendations as nodes
    related to the person name by the Recommend relationship
    """
    # initialize graph
    original_graph = RecommendationGraph()

    # find node of person of interest
    subgraph_person = original_graph.get_nodes(name=person_name)[0]

    # find people person of interest knows and which books person of interest bought
    people_known = original_graph.adjacent(subgraph_person, rel_category="Knows")
    books_bought = original_graph.adjacent(subgraph_person, rel_category="Bought")

    # find books people that person of interest knows bought that person of interest has not already bought
    recommended_books = []
    for person in people_known:
        possible_recs = original_graph.adjacent(person, rel_category="Bought")
        for rec in possible_recs:
            if rec not in books_bought:
                recommended_books.append(rec)

    # add person of interest to subgraph
    rec_graph = original_graph.subgraph([subgraph_person])

    # add recommended books to subgraph, either as nodes or as related nodes to person of interest
    if graph_type == "Unlinked":
        for book in recommended_books:
            rec_graph.add_node(book)
    elif graph_type == "Linked":
        for book in recommended_books:
            rec_graph.add_relationship(subgraph_person, book, Recommend())

    return rec_graph

def main():
    original_graph = RecommendationGraph()
    print(f"Original Property Graph: \n{repr(original_graph)}")
    rec_subgraph = Recommendations("Spencer")
    print(f"Spencer's Recommendation Graph:\n{repr(rec_subgraph)}")
    linked_subgraph = Recommendations("Spencer", "Linked")
    print(f"Linked Subgraph: \n{repr(linked_subgraph)}")

if __name__ == "__main__":
    main()
