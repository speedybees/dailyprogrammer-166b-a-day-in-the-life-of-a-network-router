import argparse, re, sys

def next_letter(letter):
    return chr(ord(letter) + 1)

class Node(object):
    def __init__(self, name):
        self.name = name
        self.distances = {}

    def __getitem__(self, location):
        return self.distances[location]

    def __repr__(self):
        return "'" + self.name + ': {' + ', '.join(['{0}: {1}'.format(node.name, distance) for (node, distance) in self.distances.items()]) + "}'"

    def add_path(self, other, distance):
        if self.distances.has_key(other):
            assert self.distances[other] == distance
            assert other.distances[self] == distance
        else:
            self.distances[other] = distance
            other.distances[self] = distance

class Graph(object):
    def __init__(self):
        self._nodes = {}

    def __getitem__(self, location):
        return self._nodes[location]

    def __iter__(self):
        return self._nodes.__iter__()

    def __repr__(self):
        to_return = ''
        for node in self._nodes:
            to_return += str(node) + "\n"
        return to_return

    @property
    def nodes(self):
        return self._nodes.values()

    def add_node(self, node):
        self._nodes[node.name] = node

    def parse(self, file):
        lines = file.readlines()
        if len(lines) < 2:
            raise IOException("Insufficient lines")
        number_of_nodes = int(lines[0])
        self._nodes = {}
        letter = 'A'
        line_number = 1
        for line in lines[1:-1]:
             # We can't use len(self._nodes) since new Nodes can get added
             # and we risk underflow if we do that
             if (line_number >= number_of_nodes):
                 break
             try:
                 self.parse_line(letter, line)
                 # This is going to get weird if there are more than 26 nodes,
                 # but the problem statement specifies that won't happen
                 letter = next_letter(letter)
             except ValueError:
                 print >> sys.stderr, "Improperly formatted line", line
             line_number += 1
        return re.split('\s+', lines[-1])

    def parse_line(self, name, line):
        distances = [int(distance) for distance in line.split(',')]
        if not self._nodes.has_key(name):
            self._nodes[name] = Node(name)
        letter = 'A'
        for distance in distances:
            if distance != -1:
                if not self._nodes.has_key(letter):
                    self._nodes[letter] = Node(letter)
                self._nodes[name].add_path(self._nodes[letter], distance)
            letter = next_letter(letter)

    # Dijkstra's algorithm as described at 
    # http://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
    # Using this instead of A* since we don't have a convenient way to 
    # estimate expected costs
    def find_shortest_path(self, start, end):
        distances = {}
        previous = {}
        for node in self._nodes.values():
            distances[node] = float('inf')
        distances[start] = 0 # Free to go to start node from start node
        unvisited_nodes = set(self._nodes.values())

        while (len(unvisited_nodes) > 0):
            sub = dict((k, v) for k, v in distances.iteritems() if k in unvisited_nodes)
            next_node = min(sub, key=sub.get)
            unvisited_nodes.remove(next_node)
            if next_node == end:
                break
            for (neighbor, distance) in next_node.distances.items():
                 if neighbor in unvisited_nodes:
                     alt = distances[next_node] + distance
                     if alt < distances[neighbor]:
                         distances[neighbor] = alt
                         previous[neighbor] = next_node
        to_return = [end]
        current_node = end
        while previous.has_key(current_node):
            to_return.insert(0, previous[current_node])
            current_node = previous[current_node]
        return (distances[end], to_return)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Calculate the shortest path through a graph.')

    parser.add_argument('-i', '--input', action='store', default=None, dest='input', help='Input file to use.  If not provided, uses stdin.')
    parser.add_argument('-o', '--output', action='store', default=None, dest='output', help='Output file to use.  If not provided, uses stdin.')

    args = parser.parse_args()

    with (open(args.input) if args.input is not None else sys.stdin) as infile:
        with (open(args.output, 'w') if args.output is not None else sys.stdout) as outfile:
            graph = Graph()
            points = graph.parse(infile)
            start, end = points[0], points[1]
            distance, path = graph.find_shortest_path(graph[start], graph[end])
            outfile.write("{0}\n".format(distance))
            outfile.write(''.join([node.name for node in path]))
            outfile.write("\n")
