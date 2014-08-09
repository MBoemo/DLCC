class Graph_Tools:

	def fun_save_graph(self,graph,file_name,str_time):
		
		# prints the graph you hand it as a .png file in the directory specified by file_name

		import matplotlib.pyplot as plt
		import networkx as nx
		
		plt.figure()
		pos=nx.spring_layout(graph,iterations=10)
		nx.draw(graph,pos,node_size=0,alpha=0.4,edge_color='r',font_size=16)
		plt.savefig("out/" + str_time + "/%(pHolder_file_name)s" %dict(pHolder_file_name = file_name))
		
		print('Saved graph '+"out/" + str_time + "/%(file_name)s" %dict(file_name = file_name))
		
