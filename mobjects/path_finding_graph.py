from manim import *
import random


class PathFindingGraph(VGroup):
    """A path-finding mobject that manages dots at given coordinates and lines between them."""

    def __init__(self, dot_positions=None, edges=None, show_labels=True, label_type="index", **kwargs):
        super().__init__(**kwargs)
        self.dot_positions = dot_positions or []
        self.edge_list = edges or []
        self.non_hamilton_path = []
        self.hamilton_path = []
        self.non_eulerian_path = []
        self.eulerian_path = []
        self.show_labels = show_labels
        self.label_type = label_type  # "index" or "coord"

        # Create dots from coordinates
        self.dots = VGroup()
        self.lines = VGroup()
        self.dot_labels = VGroup()

        for i, pos in enumerate(self.dot_positions):
            dot = Dot(point=RIGHT * pos[0] + UP * pos[1])
            self.dots.add(dot)
            if self.show_labels:
                label = self._make_label(i, pos)
                label.next_to(dot, UR, buff=0.1)
                self.dot_labels.add(label)

        # Create lines between dots
        for u, v in self.edge_list:
            self.lines.add(Line(self.dots[u], self.dots[v]))

        self.add(self.dots, self.lines)
        if self.show_labels:
            self.add(self.dot_labels)

    def _make_label(self, index, pos):
        """Create a label for a dot based on label_type."""
        if self.label_type == "coord":
            text = f"({pos[0]:.1f}, {pos[1]:.1f})"
        else:
            text = str(index)
        return Text(text, font_size=18, color=YELLOW)

    # --- Mutators ---

    def add_dot(self, x, y):
        """Add a new dot at coordinate (x, y). Returns the index of the new dot."""
        dot = Dot(point=RIGHT * x + UP * y)
        self.dot_positions.append([x, y])
        self.dots.add(dot)
        if self.show_labels:
            label = self._make_label(len(self.dots) - 1, [x, y])
            label.next_to(dot, UR, buff=0.1)
            self.dot_labels.add(label)
        return len(self.dots) - 1

    def add_line(self, u, v):
        """Add a line between dot indices u and v. Returns the index of the new line."""
        line = Line(self.dots[u], self.dots[v])
        self.edge_list.append([u, v])
        self.lines.add(line)
        return len(self.lines) - 1

    def add_edges(self, edges):
        """Add multiple edges at once. Each edge is [u, v]."""
        for u, v in edges:
            self.add_line(u, v)

    # --- Queries ---

    def get_edge_index(self, u, v):
        """Return the index of the edge [u,v] or [v,u] in edge_list."""
        try:
            return self.edge_list.index([u, v])
        except ValueError:
            return self.edge_list.index([v, u])

    def get_dot(self, index):
        """Return the Dot mobject at the given index."""
        return self.dots[index]

    def get_line(self, index):
        """Return the Line mobject at the given index."""
        return self.lines[index]

    def get_line_between(self, u, v):
        """Return the Line mobject connecting dots u and v."""
        return self.lines[self.get_edge_index(u, v)]

    # --- Hamilton path ---

    def _get_next_dot(self, dot, previous=None):
        """Return a list of adjacent dot indices, excluding the previous dot."""
        neighbors = []
        for u, v in self.edge_list:
            if u == dot and v != previous:
                neighbors.append(v)
            elif v == dot and u != previous:
                neighbors.append(u)
        return neighbors

    def find_non_hamilton_path(self):
        """Find a path that cannot be a Hamilton path using randomized greedy DFS."""
        n = len(self.dot_positions)
        starts = list(range(n - 1, -1, -1))
        for start in starts:
            visited = {start}
            path = [start]
            current = start
            previous = None
            while len(path) < n:
                neighbors = self._get_next_dot(current, previous)
                unvisited = [nb for nb in neighbors if nb not in visited]
                if not unvisited:
                    break
                random.shuffle(unvisited)
                next_dot = unvisited[0]
                visited.add(next_dot)
                path.append(next_dot)
                previous = current
                current = next_dot
            if len(path) < n:
                self.non_hamilton_path = path
                return self.non_hamilton_path

        self.non_hamilton_path = []
        return self.non_hamilton_path

    def find_hamilton_path(self):
        """Find a Hamilton path using backtracking DFS."""
        if self.hamilton_path:
            return self.hamilton_path

        n = len(self.dot_positions)

        def backtrack(path, visited):
            if len(path) == n:
                return path
            current = path[-1]
            for nb in self._get_next_dot(current):
                if nb not in visited:
                    visited.add(nb)
                    path.append(nb)
                    result = backtrack(path, visited)
                    if result:
                        return result
                    path.pop()
                    visited.discard(nb)
            return None

        for start in range(n):
            result = backtrack([start], {start})
            if result:
                self.hamilton_path = list(result)
                return self.hamilton_path

        self.hamilton_path = []
        return self.hamilton_path

    def show_non_hamilton_graph(self, scene, run_time=0.5, recompute=False, max_tries=10):
        """Animate a non-Hamilton path: yellow while exploring, red on failure, then reset."""
        previous_path = list(self.non_hamilton_path) if self.non_hamilton_path else []

        if recompute:
            self.non_hamilton_path = []

        if not self.non_hamilton_path:
            for _ in range(max_tries):
                self.find_non_hamilton_path()
                if self.non_hamilton_path and self.non_hamilton_path != previous_path:
                    break
                if recompute:
                    self.non_hamilton_path = []

        if not self.non_hamilton_path:
            return

        path = self.non_hamilton_path

        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            line = self.get_line_between(u, v)
            scene.play(
                line.animate.set_color(YELLOW),
                self.dots[u].animate.set_color(YELLOW),
                self.dots[v].animate.set_color(YELLOW),
                run_time=run_time,
            )

        scene.play(
            *[self.dots[m].animate.set_color(RED) for m in path],
            *[self.get_line_between(path[m], path[m + 1]).animate.set_color(RED)
              for m in range(len(path) - 1)],
        )

        scene.play(
            self.dots.animate.set_color(WHITE),
            self.lines.animate.set_color(WHITE),
            run_time=run_time,
        )

    def show_hamilton_graph(self, scene, run_time=0.5, delay_after=1):
        """Animate the Hamilton path: yellow while exploring, green on success, then reset."""
        if not self.hamilton_path:
            self.find_hamilton_path()
        if not self.hamilton_path:
            return

        path = list(self.hamilton_path)

        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            line = self.get_line_between(u, v)
            scene.play(
                line.animate.set_color(YELLOW),
                self.dots[u].animate.set_color(YELLOW),
                self.dots[v].animate.set_color(YELLOW),
                run_time=run_time,
            )

        scene.play(
            *[self.dots[m].animate.set_color(GREEN) for m in path],
            *[self.get_line_between(path[m], path[m + 1]).animate.set_color(GREEN)
              for m in range(len(path) - 1)],
        )

        scene.wait(delay_after)

        scene.play(
            self.dots.animate.set_color(WHITE),
            self.lines.animate.set_color(WHITE),
            run_time=run_time,
        )

    # --- Eulerian path ---

    def _build_adjacency(self):
        """Build adjacency list with edge indices for Eulerian algorithms."""
        n = len(self.dot_positions)
        adj = [[] for _ in range(n)]
        for idx, (u, v) in enumerate(self.edge_list):
            adj[u].append((v, idx))
            adj[v].append((u, idx))
        return adj

    def find_non_eulerian_path(self):
        """Find a path that fails to traverse all edges using greedy edge traversal."""
        if self.non_eulerian_path:
            return self.non_eulerian_path

        num_edges = len(self.edge_list)
        n = len(self.dot_positions)
        adj = self._build_adjacency()

        for start in range(n):
            used = set()
            path = [start]
            current = start
            while True:
                found = False
                for nb, edge_idx in adj[current]:
                    if edge_idx not in used:
                        used.add(edge_idx)
                        path.append(nb)
                        current = nb
                        found = True
                        break
                if not found:
                    break
            if len(used) < num_edges:
                self.non_eulerian_path = path
                return self.non_eulerian_path

        self.non_eulerian_path = []
        return self.non_eulerian_path

    def find_eulerian_path(self):
        """Find an Eulerian path using Hierholzer's algorithm."""
        if self.eulerian_path:
            return self.eulerian_path

        n = len(self.dot_positions)
        num_edges = len(self.edge_list)
        adj = self._build_adjacency()

        odd_nodes = [i for i in range(n) if len(adj[i]) % 2 == 1]
        if len(odd_nodes) != 0 and len(odd_nodes) != 2:
            self.eulerian_path = []
            return self.eulerian_path

        start = odd_nodes[0] if odd_nodes else 0

        used = [False] * num_edges
        stack = [start]
        path = []
        adj_ptr = [0] * n

        while stack:
            v = stack[-1]
            found = False
            while adj_ptr[v] < len(adj[v]):
                nb, edge_idx = adj[v][adj_ptr[v]]
                adj_ptr[v] += 1
                if not used[edge_idx]:
                    used[edge_idx] = True
                    stack.append(nb)
                    found = True
                    break
            if not found:
                path.append(stack.pop())

        path.reverse()
        if len(path) != num_edges + 1:
            self.eulerian_path = []
        else:
            self.eulerian_path = path
        return self.eulerian_path

    def show_non_eulerian_graph(self, scene, run_time=0.5):
        """Animate a non-Eulerian path: yellow while exploring, red on failure, then reset."""
        if not self.non_eulerian_path:
            self.find_non_eulerian_path()
        if not self.non_eulerian_path:
            return

        path = self.non_eulerian_path

        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            line = self.get_line_between(u, v)
            scene.play(
                line.animate.set_color(YELLOW),
                self.dots[u].animate.set_color(YELLOW),
                self.dots[v].animate.set_color(YELLOW),
                run_time=run_time,
            )

        visited_dots = set(path)
        scene.play(
            *[self.dots[m].animate.set_color(RED) for m in visited_dots],
            *[self.get_line_between(path[m], path[m + 1]).animate.set_color(RED)
              for m in range(len(path) - 1)],
        )

        scene.play(
            self.dots.animate.set_color(WHITE),
            self.lines.animate.set_color(WHITE),
            run_time=run_time,
        )

    def show_eulerian_graph(self, scene, run_time=0.5, delay_after=1):
        """Animate the Eulerian path: yellow while exploring, green on success, then reset."""
        if not self.eulerian_path:
            self.find_eulerian_path()
        if not self.eulerian_path:
            return

        path = self.eulerian_path

        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            line = self.get_line_between(u, v)
            scene.play(
                line.animate.set_color(YELLOW),
                self.dots[u].animate.set_color(YELLOW),
                self.dots[v].animate.set_color(YELLOW),
                run_time=run_time,
            )

        scene.play(
            self.dots.animate.set_color(GREEN),
            self.lines.animate.set_color(GREEN),
        )

        scene.wait(delay_after)

        scene.play(
            self.dots.animate.set_color(WHITE),
            self.lines.animate.set_color(WHITE),
            run_time=run_time,
        )
