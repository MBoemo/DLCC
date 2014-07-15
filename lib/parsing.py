class Parsing:

        def check_duplicates(self,name,parent_Names):
		# You might have multiple 'And's or 'Or's in a given logic statement: assign them each a unique name by pinning on 0s
                if name in parent_Names:
			
                        parent_Names.append(name+'0')
                        return name + '0'
                else:
                        parent_Names.append(name)
                        return name



	def fun_recursive_add_to_logic_graph(self,dummy_list,parent_Name,parent_Names,tree_nested_logic_statement):
		if ',' not in dummy_list[-1]:
			if len(dummy_list) == 2:
				key = dummy_list[-1]
				if len(key) == 2:
					tree_nested_logic_statement.add_edge(parent_Name,key[0][0])
					tree_nested_logic_statement.add_edge(parent_Name,key[1])
				else:
					tree_nested_logic_statement.add_edge(parent_Name,key[0])

		else:
			comma_index = dummy_list[1].index(',')
			first_partition = dummy_list[1][0:comma_index]
			second_partition = dummy_list[1][comma_index + 1:]
			first_ID = self.check_duplicates(str(first_partition[0]),parent_Names)
			second_ID = self.check_duplicates(str(second_partition[0]),parent_Names)
			tree_nested_logic_statement.add_edge(parent_Name,first_ID)
			tree_nested_logic_statement.add_edge(parent_Name,second_ID)
			self.fun_recursive_add_to_logic_graph(first_partition,first_ID,parent_Names,tree_nested_logic_statement)
			self.fun_recursive_add_to_logic_graph(second_partition,second_ID,parent_Names,tree_nested_logic_statement)

	def fun_build_parsed_logic_graph(self,lst_nested_logic_statement):
		
		import networkx as nx
		import matplotlib.pyplot as plt

		print('Building tree...')
		G_nested_logic_statement = nx.MultiDiGraph()
		G_nested_logic_statement.add_node(str(lst_nested_logic_statement[0][0]))
		reduced_list = lst_nested_logic_statement[0][1]
		parent_Names = []
		parent_Name = str(lst_nested_logic_statement[0][0])
		self.fun_recursive_add_to_logic_graph(lst_nested_logic_statement[0],parent_Name,parent_Names,G_nested_logic_statement)
	
		plt.figure()
		pos=nx.spring_layout(G_nested_logic_statement,iterations=10)
		nx.draw(G_nested_logic_statement,pos,node_size=0,alpha=0.4,edge_color='r',font_size=16)
		plt.savefig("out/nested_logic_statement")
		print('Done.')

		return G_nested_logic_statement
