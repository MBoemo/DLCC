class Track_Layout:

	import matplotlib.pyplot as plt


	def plot_tracks(self,G,node,starting_coords,direction,track_lengths,first):
		import numpy as np
		from lib.prism import Prism_Templates
		pt = Prism_Templates()

		int_length = int(track_lengths[pt.correct_1(node)]) + 1

		# start out in the x direction
		# direction that is varied
		lst_x = [x + int(starting_coords[0]) for x in range(int_length)]

		# direction that is constant
		lst_y = [int(starting_coords[1])]*int_length
		area = np.pi*(100)

		# vector of (x,y) coords we have so far
		# look up intersections
		# if > 1, reverse
		
		global lst_coordsUsed		
		if direction == 1:
			lst_coords = zip(lst_x,lst_y)
		elif direction == -1:
			lst_coords = zip(lst_y,lst_x)

		if len(set(lst_coordsUsed).intersection(set(lst_coords))) > 1:
			lst_x = [int(starting_coords[0]) - x for x in range(int_length)]
			flip = -1
		else:
			flip = 1

		lst_coordsUsed = lst_coordsUsed + lst_coords

		if first == 1:
			self.plt.text(lst_x[0] - 1,lst_y[-1],'END',size='large')
		first = 0



		# do the plotting
		if direction == -1:
	    		self.plt.scatter(lst_y,lst_x,s=area,alpha=0.5,c='orange')
		        self.plt.arrow(lst_y[-1],lst_x[-1],0,flip*-(int_length - 1.3),width=0.2,head_width=0.5,head_length=0.2,fc='royalblue',ec='darkblue',length_includes_head=True)
		        self.plt.text(lst_y[-1],lst_x[-1],node,size='large')
		else:
		        self.plt.scatter(lst_x,lst_y,s=area,alpha=0.5,c='orange')
		        self.plt.arrow(lst_x[-1],lst_y[-1],flip*-1*(int_length - 1.3),0,width=0.2,head_width=0.5,head_length=0.2,fc='royalblue',ec='darkblue',length_includes_head=True)
		        self.plt.text(lst_x[-1],lst_y[-1],node,size='large')
		new_node = G.predecessors(node)


		if new_node:
		        if len(new_node) == 2:
		        	self.plot_tracks(G,new_node[0],[lst_y[0],lst_x[1]],direction*-1,track_lengths,first)
		                self.plot_tracks(G,new_node[1],[lst_y[0],lst_x[2]],direction*-1,track_lengths,first)
		        else:
		                self.plot_tracks(G,new_node[0],[lst_y[0],lst_x[1]],direction*-1,track_lengths,first)

	def plot_final(self,G_refined,track_lengths,str_time):
		import networkx as nx
		for node in G_refined.nodes():
			if not G_refined.successors(node):
				terminal_node = node
		self.plt.figure()
		global lst_coordsUsed
		lst_coordsUsed = []
		first = 1
		self.plot_tracks(G_refined,terminal_node,[0,0],1,track_lengths,first)
		self.plt.axes().set_aspect('equal')
		self.plt.savefig("out/"+str_time+"/track_design.pdf")
		print('Done.')
