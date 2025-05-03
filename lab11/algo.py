import copy
import unittest

initial_network = {
    0: {1: 1, 3: 7, 2: 3},
    1: {0: 1, 2: 1},
    2: {0: 3, 1: 1, 3: 2},
    3: {0: 7, 2: 2}
}

def init_routing_tables(network):
    return {
        node: {
            dest: (network[node][dest] if dest in network[node] else (0 if dest == node else float('inf')))
            for dest in network
        }
        for node in network
    }

def distance_vector_routing(network, routing_tables):
    updated = True
    while updated:
        updated = False
        for node in network:
            for neighbor in network[node]:
                for dest in routing_tables[neighbor]:
                    if dest == node:
                        continue
                    new_cost = network[node][neighbor] + routing_tables[neighbor][dest]
                    if new_cost < routing_tables[node][dest]:
                        routing_tables[node][dest] = new_cost
                        updated = True

def print_routing_tables(title, routing_tables):
    print(f"\n{title}")
    for node in sorted(routing_tables):
        print(f"Routing table for node {node}:")
        for dest in sorted(routing_tables[node]):
            cost = routing_tables[node][dest]
            print(f"  to {dest}: {cost}")
        print()

network = copy.deepcopy(initial_network)
routing_tables = init_routing_tables(network)
distance_vector_routing(network, routing_tables)
print_routing_tables("Initial routing tables", routing_tables)

network[0][2] = 1
network[2][0] = 1

routing_tables_after_change = init_routing_tables(network)
distance_vector_routing(network, routing_tables_after_change)
print_routing_tables("Routing tables after changing cost 0-2 from 3 to 1", routing_tables_after_change)


class TestDistanceVector(unittest.TestCase):

    def test_route_cost_reduction(self):
        """После изменения стоимости 0-2 с 3 до 1 маршрут от 0 до 3 должен стать дешевле"""
        old_cost = routing_tables[0][3]
        new_cost = routing_tables_after_change[0][3]
        self.assertLess(new_cost, old_cost, "Route cost from node 0 to 3 did not improve")

    def test_symmetry_of_costs(self):
        """Стоимость от A до B должна совпадать с B до A, т.к. каналы двусторонние"""
        for a in initial_network:
            for b in initial_network:
                if a != b:
                    self.assertEqual(routing_tables[a][b], routing_tables[b][a],
                                     f"Cost from {a} to {b} != cost from {b} to {a}")

    def test_final_cost_not_greater_than_direct(self):
        """Стоимость после алгоритма не превышает прямую стоимость (если путь существует)"""
        for node in initial_network:
            for neighbor, direct_cost in initial_network[node].items():
                self.assertLessEqual(routing_tables[node][neighbor], direct_cost,
                                     f"Cost from {node} to {neighbor} became worse than direct link")

    def test_cost_to_self_is_zero(self):
        """Стоимость маршрута до самого себя всегда должна быть ноль"""
        for node in routing_tables:
            self.assertEqual(routing_tables[node][node], 0,
                             f"Cost to self for node {node} is not zero")

    def test_no_unreachable_nodes(self):
        """После завершения алгоритма все узлы должны быть достижимы (не Inf)"""
        for node in routing_tables:
            for dest in routing_tables[node]:
                self.assertNotEqual(routing_tables[node][dest], float('inf'),
                                    f"Node {node} cannot reach {dest}")

unittest.main(argv=[''], exit=False)