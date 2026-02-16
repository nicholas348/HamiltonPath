from manim import *
import networkx as nx
class PathFindingGraph(Graph):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.non_hamilton_path = []
        self.hamilton_path = []


    #hamilton graph
    def _get_next_dot(self):
        pass

    def find_non_hamilton_path(self):
        pass

    def find_hamilton_path(self):
        if self.hamilton_path:
            pass
        else:
            self.hamilton_path = nx.hamiltonian_path(self.graph)



    def show_non_hamilton_graph(self):
        pass

    def show_hamilton_graph(self):
        pass
