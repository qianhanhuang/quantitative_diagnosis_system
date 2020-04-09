from igraph import Graph

def detect_community(path):
	edges = []
	with open(path, 'r') as f:
		for row in f.read().splitlines():
			u, v, w = row.split('\t')
			edges.append((u, v, w))
	g = Graph.TupleList(edges, directed=False, vertex_name_attr='name', edge_attrs=None, weights=True)
	communities = g.community_edge_betweenness(directed=False).as_clustering()
	print(communities)

if __name__ == '__main__':
	detect_community('data.txt')

