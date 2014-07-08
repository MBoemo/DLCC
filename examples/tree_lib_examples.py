# Create a new object of tree structure
t = Tree()

# Get or set the ID of the root
t.root [=nid]

# Get the number of nodes in this tree
t.size()

# Check if the tree contains given node
t.contains(nid)

# Obtain node's parent (Node instance)
# Return None if the parent is None or does not exist in the tree
t.parent(nid)

# Get the list of all the nodes randomly belonging to this tree
t.all_nodes()

# Get leaves of give root
t.leaves([nid])

# Add a new node object to the tree and make the parent as the root by default
t.add_node(node[,parent])

# Create a new node and add it to this tree
t.create_node(tag[,identifier[,parent]])

# Traverse the tree nodes with different modes; NOTE:
# `nid` refers to the expanding point to start;
# `mode` refers to the search mode (Tree.DEPTH, Tree.WIDTH);
# `filter` refers to the function of one varible to act on the **node object**;
# `cmp`, `key`, `reverse` are present to sort **node objects** in the same level.
t.expand_tree([nid[,mode[,filter[,cmp[,key[,reverse]]]]]]) 

# Get the object of the node with ID of nid
# An alternative way is using '[]' operation on the tree.
# But small difference exists between them:
# the get_node() will return None if nid is absent, whereas '[]' will raise KeyError.
t.get_node(nid)

# Get the children (only sons) list of the node with ID == nid.
t.is_branch(nid)

# Move node (source) from its parent to another parent (destination).
t.move_node(source, destination)

# Paste a new tree to an existing tree, with `nid` becoming the parent of the root of this new tree.
t.paste(nid, new_tree) 

# Remove a node and free the memory along with its successors.
t.remove_node(nid)

# Remove a node and link its children to its parent (root is not allowed)
t.link_past_node(nid)

# Search the tree from `nid` to the root along links reversedly
# Note: `filter` refers to the function of one varible to act on the **node object**.
t.rsearch(nid[,filter]) 

# Print the tree structure in hierarchy style;
# Note:
# `nid` refers to the expanding point to start;
# `level` refers to the node level in the tree (root as level 0);
# `idhidden` refers to hiding the node ID when priting;
# `filter` refers to the function of one varible to act on the **node object**;
# `cmp`, `key`, `reverse` are present to sort **node objects** in the same level.
t.show([nid[,level[,idhidden[,filter[,cmp[,key[,reverse]]]]]]])

# Return a soft copy of the subtree with `nid` being the root; The softness 
# means all the nodes are shared between subtree and the original.
t.subtree(nid)

# Return a subtree with `nid` being the root, and
# remove all nodes in the subtree from the original one
t.remove_subtree(nid)

# Save the tree into file for offline analysis.
t.save2file(filename[,nid[,level[,idhidden[,filter[,cmp[,key[,reverse]]]]]]])
