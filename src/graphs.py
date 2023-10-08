from networkx import Graph

simple_graph = Graph([(1, 2), (1, 3), (2, 3), ])

example = Graph(
    [
        (1, 2),
        (1, 3),
        (1, 4),
        (2, 3),
        (2, 5),
        (3, 4),
        (3, 5),
        (5, 6),
        (5, 9),
        (5, 10),
        (6, 7),
        (6, 8),
        (7, 8),
        (9, 10),
    ]
)
