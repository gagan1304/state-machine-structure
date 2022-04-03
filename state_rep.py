import pydot
import os
from local_vars import pth

# path to GraphViz's executables -> try: C:/Program Files/Graphviz/bin/
os.environ["PATH"] += os.pathsep + pth


class StateRep:
    """
    -> Contains the representation of State machine structure for 1 session.
    -> Uses Brute force approach to find the structure for state machine
    """

    def __init__(self, *args, **kwargs):
        self.nodes = {}  # Nodes as keys, Edges as values
        self.G = pydot.Dot(graph_type="digraph")  # Graph (Graphviz library)
        self.max_iter = 1000  # maximum number of cycles
        self.count = 0  # Total count of cycles / iterations
        self.total_edges = 0  # number of edges
        self.same_path_traversal = 0  # Number of times already created edge has been traversed.
        self.__dict__.update(kwargs)

    def status_done(self):
        """
        -> Contains logic to break the session.
        -> Code can be extended for more logics
        """
        return self.count == self.max_iter

    def update_nodes(self, state):
        """
        -> Update nodes and values in node dict and graph
        """
        # add state if not already present
        if state not in self.nodes:
            self.nodes[state] = []
            node = pydot.Node(state, style="filled", fillcolor="grey")
            self.G.add_node(node)

        # update node value
        len_state = len(self.nodes[state])
        self.nodes[state].append(str(len_state % 3 + 1))

    def update_edge(self, state, next_state):
        """
        -> Add edges (with labels) if not exist between states
        """
        len_state = len(self.nodes[state])
        # check for Z state
        if state == "Z":
            if len(self.nodes[state]) == 1:
                edge = pydot.Edge(state, next_state)
                self.G.add_edge(edge)
                self.total_edges += 1
            else:
                self.same_path_traversal += 1
        else:
            # logic for adding edges
            lbl = self.nodes[state][-1]
            if len_state <= 3:
                edge = pydot.Edge(state, next_state, label=lbl)
                self.G.add_edge(edge)
                self.total_edges += 1  # increment total edges by 1
            else:
                self.same_path_traversal += 1  # No edge created i.e. edge already existed

    def get_message_to_send(self, state):
        """
        -> Find message to send to server
        """
        self.count += 1  # Increment total count of cycles
        msg = self.nodes[state][-1]
        msg += "\n"  # adding line feed
        return msg
