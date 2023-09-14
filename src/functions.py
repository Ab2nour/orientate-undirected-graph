from typing import Final

import networkx as nx
import matplotlib.pyplot as plt

# Our default presets
COLORS: Final[dict[str, str]] = {
    "node_color": "#ffffff",
    "node_border_color": "#111827",
    "edge_color": "#94a3b8",
}


def _draw_graph(graph: nx.Graph, node_color: str, node_border_color: str, edge_color: str) -> None:
    """Draws the graph `graph` with the color parameters specified.

    Example
    ---
    >>> example = nx.Graph([(1, 2), (1, 3), (2, 3)])
    >>> _draw_graph(example, "white", "black", "gray")
    """
    nx.draw(graph, node_color=node_color, edge_color=edge_color)

    ax = plt.gca()
    ax.collections[0].set_edgecolor(node_border_color)


def draw_graph(graph: nx.Graph) -> None:
    """Draws the graph `graph` with our default presets.

    Example
    ---
    >>> example = nx.Graph([(1, 2), (1, 3), (2, 3)])
    >>> draw_graph(example)
    """
    _draw_graph(graph, COLORS["node_color"], COLORS["node_border_color"], COLORS["edge_color"])
