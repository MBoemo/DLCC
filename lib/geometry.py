class Track_Layout:

	def __init__(self):
		import matplotlib.pyplot as plt
		self.plt = plt


	def plot_tracks(self,G,node,starting_coords,direction,track_lengths):
		import numpy as np
		from lib.prism import Prism_Templates
		pt = Prism_Templates()

		int_length = int(track_lengths[pt.correct_1(node)]) + 1
		# direction that is varied
		lst_x = [x + int(starting_coords[0]) for x in range(int_length)]
		# direction that is constant
		lst_y = [int(starting_coords[1])]*int_length
		area = np.pi*(100)

		# vector of (x,y) coords we have so far
		# look up intersections
		# if > 1, reverse


		if direction == -1:
		        self.plt.scatter(lst_y,lst_x,s=area,alpha=0.5)
		        self.plt.arrow(lst_y[-1],lst_x[-1],0,-int_length+1,head_width=0.2,head_length=0.2,fc='g',ec='g',length_includes_head=True)
		        self.plt.text(lst_y[-1],lst_x[-1],node,size='xx-large')
		else:
		        self.plt.scatter(lst_x,lst_y,s=area,alpha=0.5)
		        self.plt.arrow(lst_x[-1],lst_y[-1],-int_length+1,0,head_width=0.2,head_length=0.2,fc='g',ec='g',length_includes_head=True)
		        self.plt.text(lst_x[-1],lst_y[-1],node,size='xx-large')
		new_node = G.predecessors(node)

		if new_node:
		        if len(new_node) == 2:
		                self.plot_tracks(G,new_node[0],[lst_y[0],lst_x[1]],direction*-1,track_lengths)
		                self.plot_tracks(G,new_node[1],[lst_y[0],lst_x[2]],direction*-1,track_lengths)
		        else:
		                self.plot_tracks(G,new_node[0],[lst_y[0],lst_x[1]],direction*-1,track_lengths)

	def plot_final(self,G_refined,track_lengths,str_time):
		print('Creating circuit design...')
		import networkx as nx
		for node in G_refined.nodes():
			if not G_refined.successors(node):
				terminal_node = node
		self.plt.figure()
		self.plot_tracks(G_refined,terminal_node,[0,0],1,track_lengths)
		self.plt.axes().set_aspect('equal')
		self.plt.savefig("out/"+str_time+"/track_design.pdf")
		print('Done.')
