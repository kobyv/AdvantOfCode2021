from typing import List, Dict

idx_to_name: List[str] = []
remaining_visits: List[int] = []  # 1 for lowercase, LARGEINT for uppercase
graph: List[List[int]] = []  # indexed by node: vector of nodes forming edges


def print_graph(graph: List[List[int]], idx_to_name: List[str]) -> None:
    for x, vec in enumerate(graph):
        for y in vec:
            print(f"{idx_to_name[x]}-{idx_to_name[y]} ({x}-{y})")


def print_path(path: List[int]):
    print(",".join([idx_to_name[x] for x in path]))


def calc_num_paths_part1(node: int) -> int:
    num_paths = 0
    if node == 1:  # end node
        return 1
    if not remaining_visits[node]:
        return 0
    remaining_visits[node] -= 1
    for next_node in graph[node]:
        num_paths += calc_num_paths_part1(next_node)
    remaining_visits[node] += 1  # passed by reference / global, so roll-back
    return num_paths


def calc_num_paths_part2(node: int, path: List[int] = []) -> int:
    # Path is added in order to be able to print all paths
    num_paths = 0
    path = path + [node]
    if node == 1:  # end node
        # print_path(path)
        return 1
    if not remaining_visits[node]:
        return 0
    # only one node can be visited twice.
    # So if at least one node got no remaining_visits, the rest are bounded by 1
    if remaining_visits[node] == 1 and any([x == 0 for x in remaining_visits]):
        return 0
    remaining_visits[node] -= 1
    for next_node in graph[node]:
        if next_node != 0:  # not start node
            num_paths += calc_num_paths_part2(next_node, path)
    remaining_visits[node] += 1  # passed by reference / global, so roll-back
    return num_paths


with open("data.txt") as f:
    node_names: Dict[str, int] = {}
    node_names["start"] = 0

    def update_node(node: str) -> int:
        x = node_names.get(node, len(idx_to_name))
        node_names[node] = x
        assert x <= len(idx_to_name)
        if x == len(idx_to_name):
            idx_to_name.append(node)
            remaining_visits.append(1 if node[0].islower() else 1000000)
        return x

    update_node("start")
    update_node("end")
    graph = [[], []]
    for line in f:
        nodeA, nodeB = line.strip().split("-")
        x = update_node(nodeA)
        y = update_node(nodeB)

        def update_edge(x: int, y: int) -> None:
            assert x <= len(graph)
            if x == len(graph):
                graph.append([y])
            else:
                if not y in graph[x]:
                    graph[x].append(y)

        update_edge(x, y)
        update_edge(y, x)

# print_graph(graph, idx_to_name)
num_paths = calc_num_paths_part1(0)  # 0 = start node
print("Paths:", num_paths)

################################
# PART 2
print("PART 2")
remaining_visits = [
    2 if x == 1 else x for x in remaining_visits
]  # we now can have two visits for small caves
remaining_visits[0] = 1000000  # start node
num_paths = calc_num_paths_part2(0, [])  # 0 = start node
print("Paths:", num_paths)
