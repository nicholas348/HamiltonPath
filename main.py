from manim import *
from mobjects.path_finding_graph import PathFindingGraph
from data import *

class HamiltonPath(Scene):
    def construct(self):
        # --- Phase 1: Small graph (5 nodes, 6 edges) ---

        # Build the small graph and display its first 4 dots and all edges
        small_graph = PathFindingGraph(
            dot_positions=small_positions,
            edges=line_list,
            show_labels=False
        )
        self.add(small_graph)

        # Demonstrate a failed (non-Eulerian) path, then a successful Eulerian path
        small_graph.show_non_eulerian_graph(self)
        small_graph.show_eulerian_graph(self, delay_after=3)

        # Demonstrate a failed (non-Hamilton) path, then a successful Hamilton path
        small_graph.show_non_hamilton_graph(self)
        small_graph.show_hamilton_graph(self,delay_after=3)

        self.wait(2)

        # --- Phase 2: Full graph (16 nodes, 23 edges) ---

        # Build the full graph combining small and extended data
        full_graph = PathFindingGraph(
            dot_positions=small_positions + extended_positions,
            edges=line_list + extended_edges,
            show_labels=False,
        )

        # Hide the new (extended) dots and lines so they can be animated in
        for dot in full_graph.dots[5:]:
            dot.set_opacity(0)
        for line in full_graph.lines[6:]:
            line.set_opacity(0)

        # Swap the small graph for the full graph in the scene
        self.remove(small_graph)
        self.add(full_graph)

        # Fade in the extended nodes and edgesx
        self.play(
            *[dot.animate.set_opacity(1) for dot in full_graph.dots[5:]],
            *[line.animate.set_opacity(1) for line in full_graph.lines[6:]],
            run_time=2,
        )

        # Show failed (non-Hamilton) paths on the full graph
        for _ in range(3):
            full_graph.show_non_hamilton_graph(self, recompute=True)

        # Display "NP" label to represent NP-hard complexity
        n_p = Text("NP").shift(RIGHT * 6)
        self.play(Write(n_p))

        # Show the successful Hamilton path on the full graph
        full_graph.show_hamilton_graph(self,delay_after=3)

        # Display "P" label to represent polynomial-time verification
        p = Text("P").shift(LEFT * 6)
        self.play(Write(p))

        # Transform P, NP, and the graph into the "P = NP" equation
        P_equal_NP = VGroup(
            MathTex("P"),
            MathTex("="),
            MathTex(" NP"),
        ).arrange(RIGHT).scale(2)
        self.play(
            ReplacementTransform(p, P_equal_NP[0]),
            ReplacementTransform(n_p, P_equal_NP[2]),
            ReplacementTransform(full_graph, P_equal_NP[1]),
        )

        # End with a big red question mark — the P vs NP open problem
        big_question_mark = MathTex("?", color=RED).scale(4)
        self.play(Write(big_question_mark))
        