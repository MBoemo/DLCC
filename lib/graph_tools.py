class Graph_Tools:

	def fun_save_graph(self,graph,file_name,str_time):
		
		# prints the graph you hand it as a .png file in the directory specified by file_name

		import matplotlib
		import matplotlib.pyplot as plt
		import networkx as nx
		

		plt.figure()
		nx.draw_spring(graph,node_color='w',with_labels=True,node_size=1000,arrows=True)
		plt.savefig("out/" + str_time + "/%(pHolder_file_name)s" %dict(pHolder_file_name = file_name))
		
		print('Saved graph '+"out/" + str_time + "/%(file_name)s" %dict(file_name = file_name))
		
