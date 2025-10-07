from typing import Final

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

# Our default presets
color_options: Final[dict[str, str]] = {
    "node_color": "#ffffff",
    "edgecolors": "#111827",
    "edge_color": "#94a3b8",
}


def draw_graph(graph: nx.Graph) -> plt.Figure:
    """Draws the graph `graph` with our default presets.

    Example
    ---
    >>> example = nx.Graph([(1, 2), (1, 3), (2, 3)])
    >>> plot = draw_graph(example)
    """
    fig = plt.figure()
    plt.axis("off")

    nx.draw_networkx(
        graph,
        **color_options
    )
    return fig


def couleur_aleatoire() -> tuple[float, float, float]:
    """
    Renvoie une couleur aléatoire.
    Pour ne pas avoir une couleur trop foncée, on fixe une limite.
    """
    limite = 0.5
    r, g, b = (
        np.random.uniform(limite, 1),
        np.random.uniform(limite, 1),
        np.random.uniform(limite, 1),
    )
    return r, g, b
