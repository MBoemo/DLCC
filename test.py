from lib.fanout import Fanout
f = Fanout()

import networkx as nx

G = nx.MultiDiGraph()
f.fun_draw_fanout_digraph('A',1)
