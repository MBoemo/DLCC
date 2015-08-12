import sys
import os
import time

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




# take xml file specified on the command line and parse it into a list
from lib.parser import cls_dlin_parser
i = cls_dlin_parser() 
lst_nested_logic_statement = i.fun_dlin_parse(sys.argv[1])

# build a diagraph out of the nested logic statement list
from lib.parsing import Parsing
p = Parsing()
G_nested_logic_statement = p.fun_build_parsed_logic_graph(lst_nested_logic_statement,str_time)

# compute topology
from lib.topology import Topology
t = Topology()
G_topology_Digraph = t.fun_nestedLogicDigraph_2_topologyDigraph(G_nested_logic_statement,str_time)

# find lengths with Prism
from lib.prism import Prism_Compiler
pc = Prism_Compiler()
hash_track_lengths = pc.fun_iterate_through_graph(G_topology_Digraph)

print(hash_track_lengths)

# plot final track layout
from lib.geometry import Track_Layout
tl = Track_Layout()
tl.plot_final(G_topology_Digraph,hash_track_lengths,str_time)

