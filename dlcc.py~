import sys
import os
import time
from lib.parser import cls_parser
from lib.symbolic_logic import cls_symbolic_logic
from lib.formula_digraph import cls_digraph_formula
from lib.topology import Topology
from lib.prism import Prism_Compiler
from lib.geometry import Track_Layout


####################################
# Some initialisation housekeeping #
####################################

# make sure the directories we need exist
if os.path.exists('out') == False:
	os.system('mkdir out')

if os.path.exists('temp') == False:
	os.system('mkdir temp')

# timestamped folder for output files
str_time = time.strftime("date_%Y-%m-%d_time_%H-%M-%S")
os.system('mkdir out/'+str_time)


##################
#   Main Stuff   #
##################

# take the .dlin input file, check and parse it
# contents: lst_parsed_input = [str_symbols,str_formula,str_path,str_trivLen,str_tol]
p = cls_parser() 
lst_parsed_input = p.fun_dlin_parse(sys.argv[1])

# simplify the propositional formula, format it into a nested list
s = cls_symbolic_logic()
lst_nested_formula = s.fun_simplifyLogic(lst_parsed_input[0],lst_parsed_input[1])

# build a diagraph out of the nested logic statement list
g = cls_digraph_formula()
G_nested_formula = g.fun_formula_parse_tree(lst_nested_formula,str_time)

# compute topology
t = Topology()
G_topology_Digraph = t.fun_nestedLogicDigraph_2_topologyDigraph(G_nested_formula,str_time)

# find lengths with Prism
pc = Prism_Compiler()
hash_track_lengths = pc.fun_iterate_through_graph(G_topology_Digraph,lst_parsed_input[2],lst_parsed_input[3],lst_parsed_input[4])

# plot final track layout
tl = Track_Layout()
tl.plot_final(G_topology_Digraph,hash_track_lengths,str_time)

