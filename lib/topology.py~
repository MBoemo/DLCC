class Topology:
	
	def __init__(self):

		from lib.xml_input import Inputs
		self.Inputs = Inputs

		import networkx as nx
		self.nx = nx
		

	def fun_gate_topology(self,G_topology_Digraph,inputs,outputs,node,int_counter):
		str_gate_type = node.translate(None,'0')
		print(str_gate_type)
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
		if str_gate_type == 'Fanout':
			print('recognised')
			G_topology_Digraph.add_edge(inputs[0],'1_'+str(int_counter))                 # input -> 1_1
                	G_topology_Digraph.add_edge(inputs[0],'1_'+str(int_counter+1))               # input -> 1_2
                	G_topology_Digraph.add_edge('1_'+str(int_counter),'1_'+str(int_counter+2))   # 1_1   -> 1_3
                	G_topology_Digraph.add_edge('1_'+str(int_counter+1),'1_'+str(int_counter+3)) # 1_2   -> 1_4             
			if outputs:
				G_topology_Digraph.add_edge('1_'+str(int_counter+2),output[0])
				G_topology_Digraph.add_edge('1_'+str(int_counter+3),output[0])
			G_topology_Digraph.remove_node(node)			
			int_counter = int_counter + 4

		return int_counter

	
	def fun_nestedLogicDigraph_2_topologyDigraph(self,G_nestedLogicDigraph,str_time):
		
		print('Creating topology digraph...')
		from lib.graph_tools import Graph_Tools
		gt = Graph_Tools() 
		
		G_topology_Digraph = G_nestedLogicDigraph
		
		int_counter = 1
		for node in reversed(G_topology_Digraph.nodes()): # you have to go from the bottom up on the tree - but just reversing the list may not always work.  need to confirm this is okay
			if node.translate(None,'0') in ['And','Or','Not','Fanout']: # if one of the nodes in the graph is a logic gate...

				int_counter = self.fun_gate_topology(G_topology_Digraph,G_topology_Digraph.predecessors(node),G_topology_Digraph.successors(node),node,int_counter) # replace it with the appropriate track topology
		
		gt.fun_save_graph(G_topology_Digraph,'topology_digraph',str_time)
		
		print('Done.')

		self.fun_refineTopology(G_topology_Digraph,str_time) # refine topology - may want to make this an option

		return G_topology_Digraph

	def fun_refineTopology(self,G_topology_Digraph,str_time):
		
		import networkx as nx
		from lib.graph_tools import Graph_Tools
		gt = Graph_Tools()

		print('Attempting to refine topology...')

		G_topology_refined = G_topology_Digraph # make a new graph we can edit for refinement
		bool_topologyRefined = False # we'll switch this to true if we actually find any possible refinements

		# Find all paths from 'leaf' nodes to 'root' node
		lst_inDegree = G_topology_refined.in_degree().items()
		lst_outDegree = G_topology_refined.out_degree().items()
		lst_paths = []		

		# Find the 'leaf nodes' and the 'root nodes'.  This is a bit boilerplate, would be nice to have a neater way to do this
		for node in lst_outDegree:
			if node[1] == 0:
				terminal_node = node[0]
		for node in lst_inDegree:
			if node[1] == 0:
				lst_paths.append([p for p in nx.all_simple_paths(G_topology_refined,source=node[0],target=terminal_node)])

		# Check for a series of 3x 1's
		for path in lst_paths:
			lst_orderedNodes = path[0]
			if len(lst_orderedNodes) >= 3: # we need a path of at least length 3 to be able to refine topology 
				for i in range(len(lst_orderedNodes) - 2):
					if lst_orderedNodes[i][0] == '1' and lst_orderedNodes[i + 1][0] == '1' and lst_orderedNodes[i + 2][0] == '1': # if you've found a series of 3 x 1's...
						G_topology_refined.add_edge(G_topology_refined.predecessors(lst_orderedNodes[i])[0],lst_orderedNodes[i + 2]) # add an edge that circuments the redundant 1's
						# regarding prev line: if there are two predecessors, we may end up triple blocking a track, which we may not want to do
						G_topology_refined.remove_node(lst_orderedNodes[i]) # delete the redundant nodes
						G_topology_refined.remove_node(lst_orderedNodes[i + 1]) # delete the redundant nodes
						bool_topologyRefined = True # indicate that we've done some refinement

		if bool_topologyRefined == True: # if we've done any refinement, say so and save it
			print('Identified simplified topology.  Condensing network...')
			gt.fun_save_graph(G_topology_refined,'topology_refinement',str_time)
		elif bool_topologyRefined == False:
			print('No topology refinement possible.')
		
		print('Done.')













	
