from manim import *


class PathFindingGraph(VGroup):
    """A path-finding mobject that manages dots at given coordinates and lines between them."""

    def __init__(self, dot_positions=None, edges=None, show_labels=True, label_type="index", **kwargs):
        super().__init__(**kwargs)
        self.dot_positions = dot_positions or []
        self.edge_list = edges or []
        self.non_hamilton_path = []
        self.hamilton_path = []
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
        """Find a path that cannot be a Hamilton path using greedy DFS."""
        if self.non_hamilton_path:
            return self.non_hamilton_path

        n = len(self.dot_positions)
        for start in range(n):
            visited = {start}
            path = [start]
            current = start
            previous = None
            while len(path) < n:
                neighbors = self._get_next_dot(current, previous)
                unvisited = [nb for nb in neighbors if nb not in visited]
                if not unvisited:
                    break
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

    def show_non_hamilton_graph(self, scene, run_time=0.5):
        """Animate a non-Hamilton path: yellow while exploring, red on failure, then reset."""
        if not self.non_hamilton_path:
            self.find_non_hamilton_path()
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

    def show_hamilton_graph(self, scene, run_time=0.5):
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

        scene.play(
            self.dots.animate.set_color(WHITE),
            self.lines.animate.set_color(WHITE),
            run_time=run_time,
        )
