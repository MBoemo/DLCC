from lib.parsing import Parsing
p = Parsing()

import sympy
import sys
from sympy import symbols
from sympy.logic import simplify_logic

####
# put something here that reads everything we need from the xml at once
####

print('Condensing Boolean logic expression...')
from lib.xml_input import Inputs
i = Inputs() 
str_simplified_logic_statement = '('+str(i.extract_logic(sys.argv[1]))+')'
print('Simplified Boolean logic: '+str(i.extract_logic(sys.argv[1])))
print('Done.')


print('Calling nested argument parser...')
import pyparsing
from pyparsing import nestedExpr
lst_nested_logic_statement = nestedExpr('(',')').parseString(str_simplified_logic_statement).asList()
print('Done.')


print('Building tree...')
from treelib import Tree, Node
tree_nested_logic_statement = Tree()
tree_nested_logic_statement.create_node(str(lst_nested_logic_statement[0][0]),str(lst_nested_logic_statement[0][0]))
reduced_list = lst_nested_logic_statement[0][1]
parent_Names = []
parent_Name = lst_nested_logic_statement[0][0]
p.tree_build(lst_nested_logic_statement[0],parent_Name,parent_Names,tree_nested_logic_statement)
tree_nested_logic_statement.show()
print('Done.')	


print('Computing track topology...')
from lib.topology import Topology
t = Topology()
tree_topology = Tree()
int_running_label = 1
tree_topology = t.fun_nested_logic_tree_2_topology_tree(tree_topology,tree_nested_logic_statement,int_running_label)
tree_topology.show()
print('Done.')

print('Refining track topology...')
tree_refined_topology = t.refine_topology(tree_topology,tree_topology.leaves(tree_topology.root))
tree_refined_topology.show()
print('Done.')











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
