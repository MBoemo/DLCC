from lib.parsing import Parsing
p = Parsing()

import sympy
import sys
from sympy import symbols
from sympy.logic import simplify_logic

print('Condensing Boolean logic expression...')
from lib.xml_input import Inputs
i = Inputs() 
simplified_expression = '('+str(i.extract_logic(sys.argv[1]))+')'
print('Simplified Boolean logic: '+str(i.extract_logic(sys.argv[1])))
print('Done.')


print('Calling nested argument parser...')
import pyparsing
from pyparsing import nestedExpr
nested_list = nestedExpr('(',')').parseString(simplified_expression).asList()
print('Done.')


print('Building tree...')
from treelib import Tree, Node
tree = Tree()
tree.create_node(str(nested_list[0][0]),str(nested_list[0][0]))
reduced_list = nested_list[0][1]
parent_Names = []
parent_Name = nested_list[0][0]
p.tree_build(nested_list[0],parent_Name,parent_Names,tree)
tree.show()
print('Done.')	


print('Computing track topology...')
from lib.topology import Topology
t = Topology()
import networkx as nx
G=nx.MultiDiGraph()
tree_chomp = tree
running_label = 1
t.chomp_tree(G,tree_chomp,running_label)
print('Done.')

print('Saving and displaying results...')
t.topology_plot(G,sys.argv[1])
G_refined = t.refine_topology(G,sys.argv[1])
print('Done.')

print('Compiling Prism code...')
from lib.prism_0.2 import Prism_Compiler
pc = Prism_Compiler()
dic = pc.build_prism_code(G)
print('Done.')

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
