from manim import *
from mobjects.path_finding_graph import PathFindingGraph


class HamiltonPath(Scene):
    def construct(self):
        # --- Phase 1: Small graph (5 nodes, 6 edges) ---
        small_positions = [
            [3.8378238140915517, -0.5733057553287386],   # 0
            [3.9094422441839445, -1.50972436618488],     # 1
            [1.22728219167647, 2.8840997591867765],      # 2
            [-0.9014937142731325, -2.886678029017851],   # 3
            [-4.4408807914835835, 0.38928870636404467],  # 4
        ]
        line_list = [
            [0, 1],
            [1, 2],
            [2, 3],
            [3, 0],
            [2, 4],
            [3, 4]
        ]

        small_graph = PathFindingGraph(
            dot_positions=small_positions,
            edges=line_list,
            show_labels=False
        )
        self.add(small_graph)

        small_graph.show_non_hamilton_graph(self)
        small_graph.show_hamilton_graph(self)

        self.wait(2)

        # --- Phase 2: Full graph (16 nodes, 23 edges) ---
        extended_positions = [
            [-1.5190050841020142, -0.555995671348672],   # 5
            [1.87625422654442, 1.3674150662044973],      # 6
            [3.355581091063108, 2.8278229998944537],     # 7
            [2.144193665966549, -2.8786121097563795],    # 8
            [-1.6778929303556458, 0.9683144634387277],   # 9
            [-2.467284852119872, -0.2263938676336097],   # 10
            [-4.09644323847631, -1.0267798936875705],    # 11
            [0.13104734778506, 1.2031149280588904],      # 12
            [2.477545942167559, 0.582829322973079],      # 13
            [0.7878419899872489, 0.7838878005782175],    # 14
            [-4.611300071071119, 0.6147144346102609],    # 15
        ]
        extended_edges = [
            [3, 14], [3, 5], [15, 10], [15, 9], [11, 5],
            [8, 13], [13, 11], [6, 7], [8, 14], [9, 3],
            [9, 7], [10, 12], [12, 6], [6, 13], [3, 11],
            [12, 14], [10, 5],
        ]

        full_graph = PathFindingGraph(
            dot_positions=small_positions + extended_positions,
            edges=line_list + extended_edges,
            show_labels=False,
        )

        # Hide new dots/lines before adding full graph to scene
        for dot in full_graph.dots[5:]:
            dot.set_opacity(0)
        for line in full_graph.lines[6:]:
            line.set_opacity(0)

        self.remove(small_graph)
        self.add(full_graph)

        # Animate new nodes and edges appearing
        self.play(
            *[dot.animate.set_opacity(1) for dot in full_graph.dots[5:]],
            *[line.animate.set_opacity(1) for line in full_graph.lines[6:]],
            run_time=2,
        )

        self.wait(10)

        full_graph.show_non_hamilton_graph(self)

        n_p = Text("NP").shift(RIGHT * 6)
        self.play(Write(n_p))

        full_graph.show_hamilton_graph(self)

        p = Text("P").shift(LEFT * 6)
        self.play(Write(p))

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
        big_question_mark = MathTex("?", color=RED).scale(4)
        self.play(Write(big_question_mark))
