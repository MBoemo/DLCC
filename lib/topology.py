class Topology:
	
	def __init__(self):

		from lib.xml_input import Inputs
		self.Inputs = Inputs

		import networkx as nx
		self.nx = nx
		

	def fun_gate_topology(self,G_topology_Digraph,inputs,outputs,node,int_counter):
		str_gate_type = node.translate(None,'0')
		if str_gate_type == 'Not':
		        G_topology_Digraph.add_edge(inputs[0],'1_'+str(int_counter))
			if outputs:
				G_topology_Digraph.add_edge('1_'+str(int_counter),outputs[0])
			G_topology_Digraph.remove_node(node)
		        int_counter = int_counter + 1
		if str_gate_type == 'Or':
			G_topology_Digraph.add_edge('1_'+str(int_counter+1),'1_'+str(int_counter))
		        G_topology_Digraph.add_edge(inputs[0],'1_'+str(int_counter+1))
		        G_topology_Digraph.add_edge(inputs[1],'1_'+str(int_counter+1))
			if outputs:
				G_topology_Digraph.add_edge('1_'+str(int_counter),outputs[0])
			G_topology_Digraph.remove_node(node)
		        int_counter = int_counter + 2
		if str_gate_type == 'And':
			G_topology_Digraph.add_edge('1_'+str(int_counter),inputs[1])
		        G_topology_Digraph.add_edge(inputs[0],'1_'+str(int_counter))
			if outputs:
				G_topology_Digraph.add_edge(inputs[1],outputs[0])
			G_topology_Digraph.remove_node(node)
		        int_counter = int_counter + 1
		return int_counter

	
	def fun_nestedLogicDigraph_2_topologyDigraph(self,G_nestedLogicDigraph):
		
		print('Creating topology digraph...')
		from lib.graph_tools import Graph_Tools
		gt = Graph_Tools() 
		
		G_topology_Digraph = G_nestedLogicDigraph
		int_counter = 1
		for node in reversed(G_topology_Digraph.nodes()):
			if node.translate(None,'0') in ['And','Or','Not']:

				int_counter = self.fun_gate_topology(G_topology_Digraph,G_topology_Digraph.predecessors(node),G_topology_Digraph.successors(node),node,int_counter)
		
		gt.fun_save_graph(G_topology_Digraph,'topology_digraph')
		
		print('Done.')

		self.fun_refineTopology(G_topology_Digraph)

		return G_topology_Digraph

	def fun_refineTopology(self,G_topology_Digraph):
		
		import networkx as nx

		print('Refining topology...')

		# Find all paths from 'leaf' nodes to 'root' node
		lst_inDegree = G_topology_Digraph.in_degree().items()
		lst_outDegree = G_topology_Digraph.out_degree().items()
		lst_paths = []		

		for node in lst_outDegree:
			if node[1] == 0:
				terminal_node = node[0]
		for node in lst_inDegree:
			if node[1] == 0:
				lst_paths.append([p for p in nx.all_simple_paths(G_topology_Digraph,source=node[0],target=terminal_node)])

		# Check for a series of 3x 1's
		for path in lst_paths:
			lst_orderedNodes = path[0]
			if len(lst_orderedNodes) >= 3:
				for i in range(len(lst_orderedNodes) - 2):
					if lst_orderedNodes[i][0] == '1' and lst_orderedNodes[i + 1][0] == '1' and lst_orderedNodes[i + 2][0] == '1':
						print('Identified simplified topology.  Condensing network...')
			
		#print(lst_paths)
		print('Done.')













	
