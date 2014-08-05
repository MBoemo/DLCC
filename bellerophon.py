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
hash_track_lengths = pc.fun_iterate_through_graph(G_topology_Digraph)
print(hash_track_lengths)




#print('Creating circuit design...')
#from lib.geometry import Track_Layout
#tl = Track_Layout()
#tl.plot_final(G_topology_Digraph,hash_track_lengths)
#print('Done.')
