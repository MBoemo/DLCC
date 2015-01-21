class Prism_Templates:

	def single_blocked_module(self,track,blocked_by):

		track = self.correct_1(track)
		blocked_by = self.correct_1(blocked_by)

		template = '''//Prism model generated automatically by Bellerophon

// Forward walk rate
const double walk_rate = 1;

ctmc

//-----------------------------------------------------

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

		template = '''//Prism model generated automatically by Bellerophon

// Forward walk rate
const double walk_rate = 1;

ctmc

//-----------------------------------------------------

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

       
	def fun_build_singleBlock_properties_list(self,node,blocker):
		node = self.correct_1(node)
		blocker = self.correct_1(blocker)
		template = 'P=? [ F (%(blocker1)s_step=%(blocker1)s_max)&(%(track_name)s_step>=%(blocker1)s_%(track_name)s_intersection) ]\n'
		return template %dict(blocker1 = blocker,track_name = node)


	def fun_build_doubleBlock_properties_list(self,node,blocker_1,blocker_2):
		node = self.correct_1(node)
		blocker_1 = self.correct_1(blocker_1)
		blocker_2 = self.correct_1(blocker_2)
		template = 'P=? [ F (%(blocker1)s_step=%(blocker1)s_max)&(%(track_name)s_step>=%(blocker1)s_%(track_name)s_intersection)  | (%(blocker1)s_step=%(blocker2)s_max)&(%(track_name)s_step>=%(blocker2)s_%(track_name)s_intersection) ]\n'
		return template %dict(blocker1 = blocker_1,blocker2 = blocker_2,track_name = node)


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

	def fun_iterate_through_graph(self,G):

		G_temp = G.copy()

		hash_track_lengths = {}

		lst_leafNodeParents = []
		lst_inDegree = G.in_degree().items()
		
		for node in lst_inDegree:
			if node[1] == 0: # find leaf nodes
				hash_track_lengths[node[0]] = 2 # set the length of the leaf nodes = 2
				
		hash_track_lengths = self.fun_build_prism_code(G_temp,hash_track_lengths)
		
		return hash_track_lengths

	def fun_build_prism_code(self,G,hash_track_input_lengths):
	# takes the level above the leaf nodes 

	### hash_track_input_lengths will be the hash of track lengths that we continually update
		from sets import Set
		import os
		import sys
		import subprocess

		lst_leafNodeParents = []
		lst_inDegree = G.in_degree().items()
		
		for node in lst_inDegree:
			if node[1] == 0: # find leaf nodes
				lst_leafNodeParents.append(G.successors(node[0]))
		lst_leafNodeParents = Set(lst_leafNodeParents[0])

		for parent in lst_leafNodeParents:
			if len(G.predecessors(parent)) == 1:

				# build prism code
				fHandle_f = open('temp/prism_code.sm','w')
				fHandle_g = open('temp/properties_list.csl','w')
				fHandle_f.write(self.pt.single_blocked_module(parent,G.predecessors(parent)[0]))
				fHandle_g.write(self.pt.fun_build_singleBlock_properties_list(parent,G.predecessors(parent)[0]))
				fHandle_f.close()
				fHandle_g.close()
				
				# run prism
				cmd = 'prism-4.1.beta2-linux64/bin/prism temp/prism_code.sm temp/properties_list.csl -const ' + self.pt.correct_1(parent)+'_max=1:20'+','+self.pt.correct_1(G.predecessors(parent)[0])+'_max='+str(2) + ' -exportresults temp/prism_results.txt,csv'
				FNULL = open(os.devnull,'w')
				subprocess.call([cmd],shell=True,stdout=FNULL)
				FNULL.close()

				# delete the nodes that we used
				str_child1 = G.predecessors(parent)[0]
				G.remove_node(str_child1) # child 1


			elif len(G.predecessors(parent)) == 2:
			
				# build prism code
				fHandle_f = open('temp/prism_code.sm','w')
				fHandle_g = open('temp/properties_list.csl','w')
				fHandle_f.write(self.pt.double_blocked_module(parent,G.predecessors(parent)[0],G.predecessors(parent)[1]))
				fHandle_g.write(self.pt.fun_build_doubleBlock_properties_list(parent,G.predecessors(parent)[0],G.predecessors(parent)[1]))
				fHandle_f.close()
				fHandle_g.close()
				
				# run prism
				cmd = 'prism-4.1.beta2-linux64/bin/prism temp/prism_code.sm temp/properties_list.csl -const ' + self.pt.correct_1(parent)+'_max=1:20'+','+self.pt.correct_1(G.predecessors(parent)[0])+'_max='+str(hash_track_input_lengths[self.pt.correct_1(G.predecessors(parent)[0])])+','+self.pt.correct_1(G.predecessors(parent)[1])+'_max='+str(hash_track_input_lengths[self.pt.correct_1(G.predecessors(parent)[1])]) + ' -exportresults temp/prism_results.txt,csv'
				FNULL = open(os.devnull,'w')
				subprocess.call([cmd],shell=True,stdout=FNULL)
				#subprocess.call([cmd],shell=True)
				FNULL.close()

				# delete the nodes that we used
				str_child1 = G.predecessors(parent)[0]
				str_child2 = G.predecessors(parent)[1]
				G.remove_node(str_child1) # child 1
				G.remove_node(str_child2) # child 2



			hash_track_input_lengths[self.pt.correct_1(parent)] = self.fun_read_prism_output()
	
		if len(G.nodes()) >= 2: # if you have two or more nodes left in the graph, we haven't reached the root so keep going
			self.fun_build_prism_code(G,hash_track_input_lengths)

		return hash_track_input_lengths



	def fun_read_prism_output(self):
		fHandle_f = open('temp/prism_results.txt','r')
		fHandle_g = fHandle_f.readlines()
		
		for str_line in fHandle_g[1:]:
			if float(str_line.split(',')[1]) < 0.15:
				int_optimal_track_length = int(str_line.split(',')[0])
				break

			# else:
				# some error message saying we didn't reach the desired precision 	

		return int_optimal_track_length
		










