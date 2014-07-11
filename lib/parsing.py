class Parsing:

        def check_duplicates(self,name,parent_Names):
		# You might have multiple 'And's or 'Or's in a given logic statement: assign them each a unique name by pinning on 0s
                if name in parent_Names:
			
                        parent_Names.append(name+'0')
                        return name + '0'
                else:
                        parent_Names.append(name)
                        return name



	def tree_build(self,dummy_list,parent_Name,parent_Names,tree_nested_logic_statement):
		if ',' not in dummy_list[-1]:
			if len(dummy_list) == 2:
				key = dummy_list[-1]
				if len(key) == 2:
					tree_nested_logic_statement.add_edge(parent_Name,key[0][0])
					tree_nested_logic_statement.add_edge(parent_Name,key[1])
				else:
					tree_nested_logic_statement.add_edge(parent_Name,key[0])

		else:
			comma_index = dummy_list[1].index(',')
			first_partition = dummy_list[1][0:comma_index]
			second_partition = dummy_list[1][comma_index + 1:]
			first_ID = self.check_duplicates(str(first_partition[0]),parent_Names)
			second_ID = self.check_duplicates(str(second_partition[0]),parent_Names)
			tree_nested_logic_statement.add_edge(parent_Name,first_ID)
			tree_nested_logic_statement.add_edge(parent_Name,second_ID)
			self.tree_build(first_partition,first_ID,parent_Names,tree_nested_logic_statement)
			self.tree_build(second_partition,second_ID,parent_Names,tree_nested_logic_statement)
