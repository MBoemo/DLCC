class Graph_Tools:

	def fun_save_graph(self,graph,file_name):
		
		import matplotlib.pyplot as plt
		import networkx as nx
		
		plt.figure()
		pos=nx.spring_layout(graph,iterations=10)
		nx.draw(graph,pos,node_size=0,alpha=0.4,edge_color='r',font_size=16)
		plt.savefig("out/%(pHolder_file_name)s" %dict(pHolder_file_name = file_name))
		
		print('Saved graph '+"out/%(file_name)s" %dict(file_name = file_name))
		