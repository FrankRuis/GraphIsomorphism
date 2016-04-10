from collections import OrderedDict
from debugging.utils import time_this
from isomorphism.graph import Graph, Vertex


def initial_coloring(g):
    """
    Set the label (color) of all nodes to -1
    """
    for v in g:
        v.label = -1
        v.old = None
        v.neighborhood = []


def refine(g, i=0, do_initial=True) -> dict:
    """
    Apply a color refinement algorithm to graph g
    """
    neighborhoods = {}
    if do_initial:
        initial_coloring(g)

    while True:
        neighborhoods = {}

        # For each vertex in G, create a list of its neighborhood coloring
        for v in g:
            # Add the color of each neighbor to a list
            neighbor_colors = []
            for n in v.nbs:
                neighbor_colors.append(n.label)

            # Convert to color neighborhood to a sorted tuple, so it can be compared to other neighbourhoods
            t = tuple(sorted(neighbor_colors))

            # Add the vertex to a list of vertices with an identically colored neighborhood
            if t in neighborhoods:
                neighborhoods[t].append(v)
            else:
                neighborhoods[t] = [v]

        # Sort the neighborhoods dictionary on the amount of vertices in the neighborhood (descending)
        neighborhoods = OrderedDict(sorted(neighborhoods.items(), key=lambda v: len(v[1]), reverse=True))

        # For each new neighborhood coloring, give the vertices in that neighborhood new color
        # (unique to their new neighborhood)
        for neighborhood in neighborhoods:
            for group in split_neighborhood(neighborhoods[neighborhood]):
                for v in group:
                    v.old, v.neighborhood = v.neighborhood, neighborhoods[neighborhood]
                    v.label = i
                i += 1

        # Stop if the neighborhoods haven't changed
        if neighborhoods and all((all((v.neighborhood == v.old for v in neighborhoods[neighborhood]))
                                  for neighborhood in neighborhoods)):
            break

    # Return the dict containing the neighborhoods
    return neighborhoods


def split_neighborhood(neighborhood) -> list:
    """
    Help-method for splitting the list of vertices that have the same neighborhood in the current iteration into
    lists of vertices that also had the same neighborhood in the previous iteration.
    """
    split = []

    # Continue until all vertices have been assigned to a group
    while neighborhood:
        # Take all vertices that had the same neighborhood as the first vertex and add it to the list
        group = [v for v in neighborhood
                 if v.neighborhood == neighborhood[0].neighborhood and v.label == neighborhood[0].label]
        split.append(group)

        # Remove the resulting group of vertices from the total list of vertices
        neighborhood = list(set(neighborhood) - set(group))
        # neighborhood = [v for v in neighborhood if v not in group]

    return split


def count_isomorphisms(union, d=None, i=None, single=False) -> int:
    """
    Count the number of isomorphisms in the disjoint union of two graphs
    The two graphs should have their graph label set so they can be differentiated
    Graph labels are set when creating a union with disjoint_union(g, h)
    """
    if i is None:
        i = []

    if d is None:
        d = []

    # Make sure d and i are of equal length
    assert (len(d) == len(i))

    # Apply a uniform coloring to the graph
    initial_coloring(union)

    # Give every n'th vertex in D and I the color n (i.e. α(D, I))
    for n in range(len(d)):
        d[n].label = n
        i[n].label = n

    # Compute the coarsest stable coloring that refines α(D, I)
    refine(union, i=len(d), do_initial=False)

    # Group the nodes by their color class
    colors = {}
    gids = set()
    for v in union:
        if v.label in colors:
            colors[v.label].append(v)
        else:
            colors[v.label] = [v]
        gids.add(v.gid)

    # Check if the coloring is balanced
    for color in colors:
        # Count how many vertices in the neighborhood belong to graph 0 or graph 1
        count = {}

        for v in colors[color]:
            if v.gid in count:
                count[v.gid] += 1
            else:
                count[v.gid] = 1

        # If there are more vertices that belong to one graph than the other, the coloring is not balanced
        if len(count) < len(gids) or not len(set(map(lambda x: count[x] if x in count else 0, gids))) == 1:
            return 0

    # If every color class contains exactly two vertices, the coloring defines a bijection
    if set(map(len, colors.values())) == {2}:
        return 1

    # Apply branching if the coloring is balanced but does not define a bijection
    # Go through all color classes
    for color in colors.values():
        # If there are at least 4 vertices in the color class (i.e. a guess is needed)
        if len(color) >= 4:
            # Choose an x from graph 0
            # Set ys to the list of vertices in this color class belonging to graph 1
            ys = []
            x = None
            color = (set(color) - set(d)) - set(i)
            for v in color:
                if x is None:
                    x = v
                elif v.gid is not x.gid:
                    ys.append(v)

            # Recursively count the number of isomorphisms by making guesses using x and y
            num = 0
            for y in ys:
                if not single:
                    num += count_isomorphisms(union, d + [x], i + [y])
                else:
                    num += count_isomorphisms(union, d + [x], i + [y], True)
                    if num > 0:
                        return num

            return num


def disjoint_union(*args):
    """
    Create a new graph that is a disjoint union of the given graphs
    The new vertices get a label based on their original graph
    Calling this with one graph is effectively making a copy of the graph
    """
    g = Graph()
    vertices = {}

    # Go through the graphs and add their vertices and edges to the new graph
    for i in range(len(args)):
        for v in args[i]:
            # Give the new vertex a label based on their position in the list
            label = "{vertex}-G{n}".format(vertex=v.id, n=i)
            vertices[v] = Vertex(v.id, graph=g)
            vertices[v].label = label
            vertices[v].gid = i
            g.append(vertices[v])

        for e in args[i].edges:
            g.add_edge(vertices[e[0]], vertices[e[1]])

    return g


@time_this
def main():
    graphs = Graph.read_graph('C:\\Development\\PycharmProjects\\GraphIsomorphism\\graphs\\custom.gr')
    print(count_isomorphisms(disjoint_union(graphs[0], graphs[0])))

if __name__ == "__main__":
    """
    Only executed when the this module is executed, not when imported
    """
    main()
