class Fanout:

	def __init__(self):


		import matplotlib
		import matplotlib.pyplot as plt

	def fun_draw_fanout_digraph(self,str_input,int_counter):

		import networkx as nx
		self.nx = nx

		import matplotlib
		matplotlib.use('pdf')
		import matplotlib.pyplot as plt

       		G_topology_Digraph = nx.MultiDiGraph()

		G_topology_Digraph.add_edge(str_input,'1_'+str(int_counter))                 # input -> 1_1
        	G_topology_Digraph.add_edge(str_input,'1_'+str(int_counter+1))               # input -> 1_2
        	G_topology_Digraph.add_edge('1_'+str(int_counter),'1_'+str(int_counter+2))   # 1_1   -> 1_3
        	G_topology_Digraph.add_edge('1_'+str(int_counter+1),'1_'+str(int_counter+3)) # 1_2   -> 1_4             
        	int_counter = int_counter + 1


		plt.figure()
                pos=nx.spring_layout(G_topology_Digraph,iterations=10)
                nx.draw(G_topology_Digraph,pos,node_size=0,alpha=0.4,edge_color='r',font_size=16)
		plt.savefig('testFig.png')
		
