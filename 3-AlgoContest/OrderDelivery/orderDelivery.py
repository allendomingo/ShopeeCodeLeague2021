class Graph(object):
    def __init__(self, size=21):
        self.adj_matrix = []
        self.adj_list = []
        self.warehouses = []
        self.orders = []
        for i in range(size):
            self.adj_matrix.append([0 for i in range(size)])
            self.adj_list.append([])
            self.warehouses.append([0, 0])
            self.orders.append(0)
        self.size = size

    def add_edge(self, v1, v2):
        self.adj_matrix[v1][v2] = 1
        self.adj_matrix[v2][v1] = 1
        self.adj_list[v1].append(v2)
        self.adj_list[v2].append(v1)

    def add_warehouse(self, item_count, cost, place):
        self.warehouses[place][0] = item_count
        self.warehouses[place][1] = cost

    def add_order(self, item_count, place):
        self.orders[place] += item_count

    def deliver_items(self, c_target, w_source, item_count):
        self.orders[c_target] -= item_count

def get_line():
    return [int(num) for num in input().split()] # for input from terminal

# Input
N, D, E = get_line()

graph = Graph(N + 1)

for e in range(E):
    v1, v2 = get_line()
    graph.add_edge(v1, v2)

for d in range(D):
    w, c, p = get_line()
    graph.add_warehouse(w, c, p)

M, = get_line()
for m in range(M):
    k, g = get_line()
    graph.add_order(k, g)

# Main Algo
cur_cost = 0
pending_orders = [(city, order) for city, order in enumerate(graph.orders[1:]) if order > 1]

for city, order in pending_orders:# recursively (greedy, bfs is better) find the cheapest way to accomplish the remaining orders
    remaining_items = order
    queued_cities = [(city, 0)]

    while (len(queued_cities) > 0):
        cur_city, cur_dist = queued_cities.pop(0)
        print(cur_dist)
        local_items = graph.warehouses[cur_city][0]
        local_cost = graph.warehouses[cur_city][1]
        if (local_items > remaining_items):
            graph.deliver_items(city, cur_city, remaining_items)
            cur_cost += remaining_items * local_cost * cur_dist
            remaining_items = 0
        else:
            graph.deliver_items(city, cur_city, local_items)
            cur_cost += local_items * local_cost * cur_dist
            remaining_items -= local_items
        
        if (remaining_items == 0):
            break
        
        queued_cities = queued_cities + [(n_city, cur_dist + 1) for n_city in graph.adj_list[cur_city]]


# Output
print(cur_cost)