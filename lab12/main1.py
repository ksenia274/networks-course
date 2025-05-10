import json
import random
import ipaddress
from collections import defaultdict

class Router:
    def __init__(self, ip):
        self.ip = ip
        self.neighbors = set()
        self.routing_table = {}

    def initialize_table(self):
        self.routing_table[self.ip] = (self.ip, 0)
        for neighbor in self.neighbors:
            self.routing_table[neighbor.ip] = (neighbor.ip, 1)

    def update_routing_table(self):
        updated = False
        for neighbor in self.neighbors:
            for dest_ip, (next_hop, metric) in neighbor.routing_table.items():
                if dest_ip == self.ip:
                    continue
                new_metric = min(metric + 1, 16)
                if dest_ip not in self.routing_table or new_metric < self.routing_table[dest_ip][1]:
                    self.routing_table[dest_ip] = (neighbor.ip, new_metric)
                    updated = True
        return updated

    def print_table(self):
        print(f"Final state of router {self.ip} table:")
        print(f"[Source IP]      [Destination IP]    [Next Hop]       [Metric]")
        for dest_ip, (next_hop, metric) in sorted(self.routing_table.items()):
            print(f"{self.ip:<16} {dest_ip:<18} {next_hop:<15} {metric}")

def generate_random_ip(existing_ips):
    while True:
        ip = str(ipaddress.IPv4Address(random.randint(0x0B000000, 0xDF000000)))
        if ip not in existing_ips:
            return ip

def generate_network(num_routers=5):
    routers = []
    ip_set = set()
    for _ in range(num_routers):
        ip = generate_random_ip(ip_set)
        ip_set.add(ip)
        routers.append(Router(ip))

    for i in range(num_routers):
        connections = random.randint(1, min(3, num_routers - 1))
        neighbors = random.sample([r for j, r in enumerate(routers) if j != i], connections)
        for neighbor in neighbors:
            routers[i].neighbors.add(neighbor)
            neighbor.neighbors.add(routers[i])
    return routers

def load_network_from_json(path):
    with open(path) as f:
        data = json.load(f)

    ip_to_router = {ip: Router(ip) for ip in data}
    for ip, info in data.items():
        for neighbor_ip in info["neighbors"]:
            ip_to_router[ip].neighbors.add(ip_to_router[neighbor_ip])
    return list(ip_to_router.values())

def simulate_rip(routers):
    for router in routers:
        router.initialize_table()

    step = 0
    converged = False
    while not converged:
        step += 1
        print(f"\n--- Simulation Step {step} ---")
        converged = True
        for router in routers:
            print(f"\nSimulation step {step} of router {router.ip}")
            router.print_table()
            if router.update_routing_table():
                converged = False

    print("\n=== Final Routing Tables ===")
    for router in routers:
        print()
        router.print_table()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", help="Path to JSON file describing network")
    parser.add_argument("--random", type=int, help="Generate random network with N routers")
    args = parser.parse_args()

    if args.json:
        routers = load_network_from_json(args.json)
    else:
        routers = generate_network(args.random or 5)

    simulate_rip(routers)