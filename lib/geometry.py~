class Track_Layout:

	def __init__(self):
		import matplotlib.pyplot as plt
		self.plt = plt


	def plot_tracks(self,G,node,starting_coords,direction,track_lengths):
		import numpy as np
		from lib.prism import Prism_Templates
		pt = Prism_Templates()

		length = int(track_lengths[pt.correct_1(node) + '_max']) + 1
		x = [x + int(starting_coords[0]) for x in range(length)]
		y = [int(starting_coords[1])]*length
		area = np.pi*(100)
		if direction == -1:
		        self.plt.scatter(y,x,s=area,alpha=0.5)
		        self.plt.arrow(y[-1],x[-1],0,-length+1,head_width=0.2,head_length=0.2,fc='g',ec='g',length_includes_head=True)
		        self.plt.text(y[-1],x[-1],node,size='xx-large')
		else:
		        self.plt.scatter(x,y,s=area,alpha=0.5)
		        self.plt.arrow(x[-1],y[-1],-length+1,0,head_width=0.2,head_length=0.2,fc='g',ec='g',length_includes_head=True)
		        self.plt.text(x[-1],y[-1],node,size='xx-large')
		new_node = G.predecessors(node)
		if new_node:
		        if len(new_node) == 2:
		                self.plot_tracks(G,new_node[0],[y[0],x[1]],direction*-1,track_lengths)
		                self.plot_tracks(G,new_node[1],[y[0],x[2]],direction*-1,track_lengths)
		        else:
		                self.plot_tracks(G,new_node[0],[y[0],x[1]],direction*-1,track_lengths)

	def plot_final(self,G_refined,track_lengths):
		import networkx as nx
		for node in G_refined.nodes():
			if not G_refined.successors(node):
				terminal_node = node
		self.plt.figure()
		self.plot_tracks(G_refined,terminal_node,[0,0],1,track_lengths)
		self.plt.savefig("out/track_design.png")
