class Parsing:

        def check_duplicates(self,name,parent_Names):
		# You might have multiple 'And's or 'Or's in a given logic statement: assign them each a unique name by pinning on 0s
                if name in parent_Names:
			
                        parent_Names.append(name+'0')
                        return name + '0'
                else:
                        parent_Names.append(name)
                        return name



	def tree_build(self,dummy_list,parent_Name,parent_Names,tree):
		if ',' not in dummy_list[-1]:
			if len(dummy_list) == 2:
				key = dummy_list[-1]
				if len(key) == 2:
					tree.create_node(key[0][0],key[0][0],parent=parent_Name)
					tree.create_node(key[1],key[1],parent=parent_Name)
				else:
					tree.create_node(key[0],key[0],parent=parent_Name)

		else:
			comma_index = dummy_list[1].index(',')
			first_partition = dummy_list[1][0:comma_index]
			second_partition = dummy_list[1][comma_index + 1:]
			first_ID = self.check_duplicates(str(first_partition[0]),parent_Names)
			second_ID = self.check_duplicates(str(second_partition[0]),parent_Names)
			tree.create_node(str(first_partition[0]),first_ID,parent=parent_Name)
			tree.create_node(str(second_partition[0]),second_ID,parent=parent_Name)
			self.tree_build(first_partition,first_ID,parent_Names,tree)
			self.tree_build(second_partition,second_ID,parent_Names,tree)
