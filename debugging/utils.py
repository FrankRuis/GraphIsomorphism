from time import time


def time_this(method):
    def time_wrapper(*args, **kwargs):
        start = time()
        result = method(*args, **kwargs)
        end = time()

        print('{} done in {} seconds.'.format(method.__name__, end - start))
        return result

    return time_wrapper


def is_connected(graph):
    visited = set()
    stack = [graph[0]]
    while stack:
        cur = stack.pop()
        visited.add(cur)
        stack.extend(cur.nbs - visited)

    return len(visited) == len(graph)


def connected_components(graph):
    components = []
    visited = set()
    to_visit = set(graph)
    while not sum(map(len, components)) == len(graph):
        v = None
        to_visit = to_visit - visited
        visited = set()
        for v in to_visit:
            break

        if v is not None:
            stack = [v]
            while stack:
                cur = stack.pop()
                visited.add(cur)
                stack.extend(cur.nbs - visited)

        components.append(visited)

    return components


def is_tree(graph):
    """
    Use depth first search to find cycles.
    If the graph does not contain a cycle, the graph is a tree.
    """
    visited, stack = set(), [graph[0]]
    while stack:
        vertex = stack.pop()
        if vertex not in visited:
            visited.add(vertex)
            stack.extend(vertex.nbs - visited)
        else:
            return False
    return len(visited) == len(graph)
