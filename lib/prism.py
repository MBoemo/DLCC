class Prism_Templates:

	def preamble(self):
		template = '''//Prism model generated automatically by Bellerophon

// Forward walk rate
const double walk_rate = 1;

ctmc

//-----------------------------------------------------'''

		return template

	def leaf_module(self,track):

		track = self.correct_1(track)
		template = '''//-----------------------------------------------------

// %(module_name)s TRACK (%(module_name)sT)

// Maximum track length
const int %(track_name)s_max;

module %(module_name)sT
	
	// States - where we are on the track
	%(track_name)s_step : [0..%(track_name)s_max] init 0;

	// Walk
	[] true -> walk_rate : (%(track_name)s_step'= min(%(track_name)s_step+1,%(track_name)s_max));

endmodule

'''

		return template %dict(track_name = track,module_name = track.upper())

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
'''
		
		return template %dict(track_name=track,module_name=track.upper(),blocker=blocked_by)
	
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
'''
		return template %dict(track_name = track,module_name = track.upper(),blocker1 = blocked_by_one,blocker2 = blocked_by_two)

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

	def build_prism_code(self,G):
		nodes = G.out_degree(G.nodes()) # number of nodes a given node connects to, i.e. {'y': 1, 'x': 0, 'z': 1, '1_1': 1}.  So 'x' is the terminal node.
		# open a file for the prism code and properties list, and print the preamble on them
		f = open('out/prism_code.sm','w')
		g = open('out/properties_list.csl','w')
		f.write(self.pt.preamble())
		dic = []
		for node in nodes:
        		if not G.predecessors(node): # if a node has no predecessors... 
                		f.write(self.pt.leaf_module(node)) # then it's a leaf node, so write that module for it.
        		else:
                		if len(G.predecessors(node)) == 1: # if a node has one track feeding into it...
                        		f.write(self.pt.single_blocked_module(node,G.predecessors(node)[0])) # then it's only blocked by one track... 
					dic = self.build_properties_list(node,G.predecessors(node)[0],g,dic) # 
                		elif len(G.predecessors(node)) == 2:
                       			f.write(self.pt.double_blocked_module(node,G.predecessors(node)[0],G.predecessors(node)[1]))
					dic = self.build_properties_list(node,G.predecessors(node)[0],g,dic)
					dic = self.build_properties_list(node,G.predecessors(node)[1],g,dic)
		f.close()
		g.close()
		print(dic)
		return dic

        def build_properties_list(self,node,blocker,handle,dic):
		node = self.pt.correct_1(node)
		blocker = self.pt.correct_1(blocker)
		template = 'P=? [ F (%(blocker_temp)s_step=%(blocker_temp)s_max)&(%(track_name)s_step>=%(blocker_temp)s_%(track_name)s_intersection) ]\n'
		handle.write(template %dict(blocker_temp = blocker,track_name = node))
		dic.append(node + '_max')
		return dic
		

class Evaluate_Track_Lengths:

	def __init__(self):
                pt = Prism_Templates()
                self.pt = pt


	def build_variables(self,G):
		prism_variables = []
		nodes = G.out_degree(G.nodes())
		for node in nodes:
			prism_variables.append(self.pt.correct_1(node)+'_max')
		return prism_variables

	def execute_prism(self,variable_list,cmd_arg,dic):
		from lib.xml_input import Inputs
		i = Inputs()
		arg_list = i.extract_prism(cmd_arg)
		import os
		import sys
		import subprocess
		variable_lengths = {}
		for variable in variable_list:
			variable_lengths[variable] = int(arg_list[2])
		cont = 1
		counter = 1
		while cont == 1:
		
			variable_range_string = ''
			for variable in variable_list:
				variable_range_string = variable_range_string + variable+'='+str(variable_lengths[variable])+','
			variable_range_string = variable_range_string[:-1]
			cmd = arg_list[0] +  ' out/prism_code.sm out/properties_list.csl -const ' + variable_range_string +' -exportresults out/prism_results.txt,csv'
			FNULL = open(os.devnull,'w')
			subprocess.call([cmd],shell=True,stdout=FNULL)
			FNULL.close()

			modify_lengths = self.iteratively_check_results(dic,arg_list[3])
			for variable in modify_lengths:
				variable_lengths[variable] = variable_lengths[variable] + 1
			if not modify_lengths:
				cont = 0
			sys.stdout.flush()
			sys.stdout.write('Iteration ' + str(counter) + '\r')
			counter = counter + 1
		return variable_lengths
			

	def iteratively_check_results(self,dic,tolerance):
		f = open('out/prism_results.txt','r')
		g = f.readlines()
		counter = 0
		to_change = []
		for line in g:
			if line[0] == '0' or line[0] == '1':
				if float(line) > float(tolerance):
					to_change.append(dic[counter])
				counter = counter + 1
		f.close()
		return to_change
