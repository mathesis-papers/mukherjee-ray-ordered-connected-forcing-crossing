import itertools
import json


def graph(order, edges):
    neighbors = [set() for vertex in range(order)]
    for first, second in edges:
        assert 0 <= first < second < order
        neighbors[first].add(second)
        neighbors[second].add(first)
    return neighbors


def connected(neighbors, initial):
    if not initial:
        return False
    reached = {min(initial)}
    pending = list(reached)
    while pending:
        vertex = pending.pop()
        additions = (neighbors[vertex] & initial) - reached
        reached.update(additions)
        pending.extend(additions)
    return reached == initial


def sequential_closure(neighbors, initial):
    colored = set(initial)
    forces = []
    while True:
        chosen = None
        for vertex in sorted(colored):
            white = neighbors[vertex] - colored
            if len(white) == 1:
                chosen = (vertex, next(iter(white)))
                break
        if chosen is None:
            return colored, forces
        forces.append(list(chosen))
        colored.add(chosen[1])


def parallel_closure(neighbors, initial):
    colored = set(initial)
    while True:
        additions = set()
        for vertex in colored:
            white = neighbors[vertex] - colored
            if len(white) == 1:
                additions.update(white)
        if not additions:
            return colored
        colored.update(additions)


def coefficients(neighbors):
    order = len(neighbors)
    result = [0] * (order + 1)
    accepted = []
    for mask in range(1 << order):
        initial = {vertex for vertex in range(order) if mask & (1 << vertex)}
        closure, forces = sequential_closure(neighbors, initial)
        assert closure == parallel_closure(neighbors, initial)
        if connected(neighbors, initial) and len(closure) == order:
            result[len(initial)] += 1
            accepted.append(sorted(initial))
    return result, accepted


def cutoffs(first, second):
    order = len(first) - 1
    return [cutoff for cutoff in range(1, order + 1)
            if all(first[index] <= second[index] for index in range(1, cutoff + 1))
            and all(first[index] >= second[index] for index in range(cutoff + 1, order + 1))]


def multiply(first, second):
    result = [0] * (len(first) + len(second) - 1)
    for first_degree, first_value in enumerate(first):
        for second_degree, second_value in enumerate(second):
            result[first_degree + second_degree] += first_value * second_value
    return result


def starlike(arms):
    edges = []
    next_vertex = 1
    for length in arms:
        previous = 0
        for offset in range(length):
            edges.append((previous, next_vertex))
            previous = next_vertex
            next_vertex += 1
    return graph(next_vertex, edges), edges


def starlike_formula(arms):
    result = [0] * (sum(arms) + 2)
    for omitted in [None] + list(range(len(arms))):
        product = [1]
        for index, length in enumerate(arms):
            if index != omitted:
                product = multiply(product, [0] + [1] * length)
        for degree, value in enumerate(product):
            result[degree + 1] += value
    return result


def isomorphic_to(edges, target_edges, order):
    target = {tuple(sorted(edge)) for edge in target_edges}
    for permutation in itertools.permutations(range(order)):
        image = {tuple(sorted((permutation[first], permutation[second]))) for first, second in edges}
        if image == target:
            return True
    return False


def unicyclic_class():
    order = 5
    possible = list(itertools.combinations(range(order), 2))
    first_edges = [(0, 1), (0, 2), (1, 2), (0, 3), (0, 4)]
    second_edges = [(0, 1), (0, 2), (1, 2), (0, 3), (1, 4)]
    first_expected = [0, 0, 0, 4, 4, 1]
    second_expected = [0, 0, 2, 5, 3, 1]
    totals = {'same_triangle_vertex': 0, 'different_triangle_vertices': 0}
    vectors = []
    examined = 0
    for edge_mask in range(1 << len(possible)):
        examined += 1
        edges = [edge for index, edge in enumerate(possible) if edge_mask & (1 << index)]
        if len(edges) != order:
            continue
        neighbors = graph(order, edges)
        if not connected(neighbors, set(range(order))):
            continue
        if sum(len(adjacent) == 1 for adjacent in neighbors) != 2:
            continue
        counts, accepted = coefficients(neighbors)
        first_class = isomorphic_to(edges, first_edges, order)
        second_class = isomorphic_to(edges, second_edges, order)
        assert first_class != second_class
        if first_class:
            assert counts == first_expected
            totals['same_triangle_vertex'] += 1
        else:
            assert counts == second_expected
            totals['different_triangle_vertices'] += 1
        vectors.append(counts)
    assert examined == 1024
    assert totals == {'same_triangle_vertex': 30, 'different_triangle_vertices': 60}
    assert not any(all(all(first <= second for first, second in zip(candidate, other))
                       for other in vectors) for candidate in vectors)
    assert not any(all(all(first >= second for first, second in zip(candidate, other))
                       for other in vectors) for candidate in vectors)
    return {
        'graphs_examined': examined, 'qualifying_labeled_graphs': len(vectors),
        'definition': 'connected simple graphs with five vertices, five edges, and two degree-one vertices',
        'isomorphism_class_sizes': totals, 'initial_subsets_checked': len(vectors) * (1 << order),
        'same_vertex_edges': first_edges, 'different_vertices_edges': second_edges,
        'same_vertex_coefficients': first_expected, 'different_vertices_coefficients': second_expected,
        'coefficientwise_least_exists': False, 'coefficientwise_greatest_exists': False,
    }


def main():
    families = []
    subsets = 0
    for order in range(2, 11):
        path = graph(order, [(vertex, vertex + 1) for vertex in range(order - 1)])
        star = graph(order, [(0, vertex) for vertex in range(1, order)])
        path_counts, path_sets = coefficients(path)
        star_counts, star_sets = coefficients(star)
        assert path_counts == [0, 2] + [order - size + 1 for size in range(2, order + 1)]
        expected_star = [0] * (order + 1)
        if order == 2:
            expected_star = [0, 2, 1]
        elif order == 3:
            expected_star = [0, 2, 2, 1]
        else:
            expected_star[order - 1] = order - 1
            expected_star[order] = 1
        assert star_counts == expected_star
        if order >= 4:
            assert cutoffs(path_counts, star_counts) == []
            assert cutoffs(star_counts, path_counts) == [order - 2]
        families.extend([
            {'family': 'path', 'order': order, 'coefficients': path_counts},
            {'family': 'star', 'order': order, 'coefficients': star_counts}])
        subsets += 2 * (1 << order)
        if order == 4:
            witness = {
                'path_edges': [[0, 1], [1, 2], [2, 3]],
                'star_edges': [[0, 1], [0, 2], [0, 3]],
                'path_coefficients': path_counts,
                'star_coefficients': star_counts,
                'path_connected_forcing_subsets': path_sets,
                'star_connected_forcing_subsets': star_sets,
                'forward_cutoffs': cutoffs(path_counts, star_counts),
                'reverse_cutoffs': cutoffs(star_counts, path_counts),
                'singleton_closures': {
                    family: [{'initial': [vertex],
                              'closure': sorted(sequential_closure(neighbors, {vertex})[0]),
                              'forces': sequential_closure(neighbors, {vertex})[1]}
                             for vertex in range(order)]
                    for family, neighbors in [('path', path), ('star', star)]}}
    for order in range(3, 11):
        cycle = graph(order, [(vertex, vertex + 1) for vertex in range(order - 1)] + [(0, order - 1)])
        counts, accepted = coefficients(cycle)
        assert counts == [0, 0] + [order] * (order - 2) + [1]
        families.append({'family': 'cycle', 'order': order, 'coefficients': counts})
        subsets += 1 << order
    three_leaf_pairs = []
    for order in range(10, 15):
        first_arms = [1, 4, order - 6]
        second_arms = [2, 2, order - 5]
        first_graph, first_edges = starlike(first_arms)
        second_graph, second_edges = starlike(second_arms)
        first_counts, first_sets = coefficients(first_graph)
        second_counts, second_sets = coefficients(second_graph)
        assert first_counts == starlike_formula(first_arms)
        assert second_counts == starlike_formula(second_arms)
        difference = [first - second for first, second in zip(first_counts, second_counts)]
        assert [difference[4], difference[6], difference[order - 2]] == [-2, 1, -1]
        assert cutoffs(first_counts, second_counts) == []
        assert cutoffs(second_counts, first_counts) == []
        three_leaf_pairs.append({
            'order': order,
            'first_arms': first_arms, 'second_arms': second_arms,
            'first_edges': first_edges, 'second_edges': second_edges,
            'first_coefficients': first_counts, 'second_coefficients': second_counts,
            'difference': difference, 'forward_cutoffs': [], 'reverse_cutoffs': [],
        })
        subsets += 2 * (1 << order)
    polynomial_pairs = 0
    for first_arm in range(4, 31):
        for second_arm in range(first_arm, 31):
            order = first_arm + second_arm + 2
            first_counts = starlike_formula([1, first_arm, second_arm])
            second_counts = starlike_formula([2, 2, first_arm + second_arm - 3])
            difference = [first - second for first, second in zip(first_counts, second_counts)]
            assert [difference[4], difference[6], difference[order - 2]] == [-2, 1, -1]
            assert cutoffs(first_counts, second_counts) == []
            assert cutoffs(second_counts, first_counts) == []
            polynomial_pairs += 1
    assert polynomial_pairs == 378
    broom_identities = 0
    for leaves in range(3, 9):
        for length in range(1, 13):
            order = leaves + length
            counts = starlike_formula([1] * (leaves - 1) + [length])
            expected = [0] * leaves + [leaves] * length + [1]
            assert counts == expected
            assert next(index for index, count in enumerate(counts) if count) == leaves
            assert counts[leaves] == leaves
            broom_identities += 1
    unicyclic = unicyclic_class()
    tree_totals = {}
    for order in range(1, 5):
        possible = list(itertools.combinations(range(order), 2))
        tree_counts = []
        for edges in itertools.combinations(possible, order - 1):
            neighbors = graph(order, edges)
            if not connected(neighbors, set(range(order))):
                continue
            counts, accepted = coefficients(neighbors)
            tree_counts.append(counts)
            if order <= 3:
                assert counts == ([0, 1] if order == 1 else [0, 2] + [order - size + 1 for size in range(2, order + 1)])
        tree_totals[str(order)] = len(tree_counts)
        if order <= 3:
            assert all(cutoffs(first, second) for first in tree_counts for second in tree_counts)
        else:
            assert sum(not cutoffs(first, second) for first in tree_counts for second in tree_counts) == 48
    assert tree_totals == {'1': 1, '2': 1, '3': 3, '4': 16}
    print(json.dumps({
        'schema_version': 1,
        'status': 'pass',
        'arithmetic': 'exact integers and finite sets',
        'coefficient_indexing': 'array position is subset cardinality; position zero included',
        'closure_comparison': 'sequential and simultaneous forcing closures agree for every tested subset',
        'witness': witness,
        'family_graph_count': len(families) + 2 * len(three_leaf_pairs),
        'family_subset_count': subsets,
        'families': families,
        'three_leaf_pairs': three_leaf_pairs,
        'polynomial_identity_pairs': polynomial_pairs,
        'polynomial_identity_range': '4 <= a <= b <= 30; orders 10 through 62',
        'broom_identities': broom_identities,
        'broom_identity_range': '3 <= p <= 8, 1 <= long-arm length <= 12',
        'unicyclic_class': unicyclic,
        'total_initial_subsets_checked': subsets + sum(count * (1 << int(order))
                                                     for order, count in tree_totals.items())
                                          + unicyclic['initial_subsets_checked'],
        'all_labeled_trees_by_order': tree_totals,
        'first_failing_order': 4,
        'coverage': 'Finite checks of the stated graphs and orders; the all-order statements have written proofs in note.tex.'
    }, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
