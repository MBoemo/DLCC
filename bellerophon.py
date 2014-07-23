import sys

#import matplotlib.pyplot as plt # make a graph plotting function that calls this

####
# put something here that reads everything we need from the xml at once
####

# take xml file specified on the command line and parse it into a list
from lib.xml_input import Inputs
i = Inputs() 
lst_nested_logic_statement = i.extract_logic(sys.argv[1])

# build a diagraph out of the nested logic statement list
from lib.parsing import Parsing
p = Parsing()
G_nested_logic_statement = p.fun_build_parsed_logic_graph(lst_nested_logic_statement)

# compute topology
from lib.topology import Topology
t = Topology()
G_topology_Digraph = t.fun_nestedLogicDigraph_2_topologyDigraph(G_nested_logic_statement)

# find lengths with Prism
from lib.prism import Prism_Compiler
pc = Prism_Compiler()
pc.fun_build_prism_code(G_topology_Digraph)




















#print('Computing track topology...')
#from lib.topology import Topology
#t = Topology()
#tree_topology = Tree()
#int_running_label = 1
#tree_topology = t.fun_nested_logic_tree_2_topology_tree(tree_topology,G_nested_logic_statement,int_running_label)
#tree_topology.show()
#print('Done.')

#print('Refining track topology...')
#tree_refined_topology = t.refine_topology(tree_topology,tree_topology.leaves(tree_topology.root))
#tree_refined_topology.show()
#print('Done.')











#print('Compiling Prism code...')
#from lib.prism import Prism_Compiler
#pc = Prism_Compiler()
#dic = pc.build_prism_code(G)
#print('Done.')

#print('Model checking...')
#from lib.prism import Evaluate_Track_Lengths
#etl = Evaluate_Track_Lengths()
#track_lengths = etl.execute_prism(etl.build_variables(G),sys.argv[1],dic)
#print('\nDone.')

#print('Creating circuit design...')
#from lib.geometry import Track_Layout
#tl = Track_Layout()
#tl.plot_final(G_refined,track_lengths)
#print('Done.')
