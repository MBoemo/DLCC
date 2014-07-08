class Prism_Templates:

	def preamble(self):
		template = '''//Prism model generated automatically by Bellerophon

// Forward walk rate
const double walk_rate = 1;

ctmc

//-----------------------------------------------------'''

		return template

	def single_blocked_module(self,track,blocked_by):

		track = self.correct_1(track)
		blocked_by = self.correct_1(blocked_by)

		template = '''//-----------------------------------------------------
// %(module_name)s TRACK (%(module_name)sT)

// Maximum track length
const int %(track_name)s_max;

// Intersections
const int %(blocker)s_%(track_name)s_intersection = %(track_name)s_max - 1;

module %(module_name)sT


	%(track_name)s_walk : bool init true;

	// States - where we are on the track
	%(track_name)s_step : [0..%(track_name)s_max] init 0;

	// Handle blockage
	[%(track_name)s_unblocked] %(track_name)s_walk -> walk_rate : (%(track_name)s_step'=min(%(track_name)s_step+1,%(track_name)s_max));
	[%(track_name)s_blocked] (%(track_name)s_step < %(blocker)s_%(track_name)s_intersection) & (%(blocker)s_step = %(blocker)s_max) -> walk_rate : (%(track_name)s_walk'=false);




endmodule

//-----------------------------------------------------

// %(blocker_module_name)s TRACK (%(blocker)sT)

// Maximum track length
const int %(blocker)s_max;

module %(blocker)sT
	
	// States - where we are on the track
	%(blocker)s_step : [0..%(blocker)s_max] init 0;

	// Walk
	[] true -> walk_rate : (%(blocker)s_step'= min(%(blocker)s_step+1,%(blocker)s_max));

endmodule

'''
		
		return template %dict(track_name=track,module_name=track.upper(),blocker=blocked_by,blocker_module_name=blocked_by.upper())
	
	def double_blocked_module(self,track,blocked_by_one,blocked_by_two):

		track = self.correct_1(track)
		blocked_by_one = self.correct_1(blocked_by_one)
		blocked_by_two = self.correct_1(blocked_by_two)

		template = '''//-----------------------------------------------------

// %(module_name)s TRACK (%(module_name)sT)

// Maximum track length
const int %(track_name)s_max;

// Intersections
const int %(blocker1)s_%(track_name)s_intersection = %(track_name)s_max - 1;
const int %(blocker2)s_%(track_name)s_intersection = %(track_name)s_max - 2;

module %(module_name)sT

	%(track_name)s_walk : bool init true;

	// States - where we are on the track
	%(track_name)s_step : [0..%(track_name)s_max] init 0;

	// Handle blockage
	[%(track_name)s_unblocked] %(track_name)s_walk -> walk_rate : (%(track_name)s_step'=min(%(track_name)s_step+1,%(track_name)s_max));
	[%(track_name)s_blocked] ((%(track_name)s_step < %(blocker1)s_%(track_name)s_intersection) & (%(blocker1)s_step = %(blocker1)s_max)) | ((%(track_name)s_step < %(blocker2)s_%(track_name)s_intersection) & (%(blocker2)s_step = %(blocker2)s_max)) 
-> walk_rate : (%(track_name)s_walk'=false);

endmodule

//-----------------------------------------------------

// %(blocker1_module_name)s TRACK (%(blocker1)sT)

// Maximum track length
const int %(blocker1)s_max;

module %(blocker1)sT
	
	// States - where we are on the track
	%(blocker1)s_step : [0..%(blocker1)s_max] init 0;

	// Walk
	[] true -> walk_rate : (%(blocker1)s_step'= min(%(blocker1)s_step+1,%(blocker1)s_max));

endmodule

//-----------------------------------------------------

// %(blocker2_module_name)s TRACK (%(blocker2)sT)

// Maximum track length
const int %(blocker2)s_max;

module %(blocker2)sT
	
	// States - where we are on the track
	%(blocker2)s_step : [0..%(blocker2)s_max] init 0;

	// Walk
	[] true -> walk_rate : (%(blocker2)s_step'= min(%(blocker2)s_step+1,%(blocker2)s_max));

endmodule

'''
		return template %dict(track_name = track,module_name = track.upper(),blocker1 = blocked_by_one,blocker1_module_name=blocked_by_one.upper(),blocker2 = blocked_by_two,blocker2_module_name=blocked_by_two.upper())

	def correct_1(self,track_name):
		# Converts a track name of '1' into 'ONE'
		if track_name[0] == '1':
			track_name = track_name.replace('1','ONE',1)
			return track_name
		else:
			return track_name	
		

class Prism_Compiler:

	def __init__(self):

		pt = Prism_Templates()
		self.pt = pt

	# function that moves through the graph and 
	def 

	def build_prism_code(self,G):
		nodes = G.out_degree(G.nodes()) # number of nodes a given node connects to, i.e. {'y': 1, 'x': 0, 'z': 1, '1_1': 1}.  So 'x' is the terminal node.
		# open a file for the prism code and properties list, and print the preamble on them
		f = open('out/prism_code.sm','w')
		f.write(self.pt.preamble())
		dic = []
		for node in nodes:
        		if not G.predecessors(node): # if a node has no predecessors... 
                		f.write(self.pt.leaf_module(node)) # then it's a leaf node, so write that module for it.
        		else:
                		if len(G.predecessors(node)) == 1: # if a node has one track feeding into it...
                        		f.write(self.pt.single_blocked_module(node,G.predecessors(node)[0])) # then it's only blocked by one track... 
                		elif len(G.predecessors(node)) == 2: # if a node has two tracks feeding into it...
                       			f.write(self.pt.double_blocked_module(node,G.predecessors(node)[0],G.predecessors(node)[1])) # then it's blocked by two tracks.
		f.close()
		return dic

        def build_properties_list(self,node,blocker,handle,dic):
		node = self.pt.correct_1(node)
		blocker = self.pt.correct_1(blocker)
		template = 'P=? [ F (%(blocker_temp)s_step=%(blocker_temp)s_max)&(%(track_name)s_step>=%(blocker_temp)s_%(track_name)s_intersection) ]\n'
		handle.write(template %dict(blocker_temp = blocker,track_name = node))
		dic.append(node + '_max')
		return dic

