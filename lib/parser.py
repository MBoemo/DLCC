class cls_dlin_parser:

	def __init__(self):
		import string
		import ast

	def fun_dlin_parse(self,str_input_file):
		try:
			hdl_f = open(str_input_file,'r')
		except IOError:
			print 'Input file could either not be found or not be opened.  Check the path and try again.'

		lst_g = hdl_f.readlines()
		
		# check the symbols first (because we'll need them to check the formula)
		for str_line in lst_g:
			if str_line[0] == '#':
				pass
			elif '=' in str_line:
				lst_eqSplit = str_line.split('=',1)
				str_field = lst_eqSplit[0]
				str_argument = lst_eqSplit[1]

				# strip out in-line comments
				lst_argSplit = str_argument.split('#',1)
				str_argument = lst_argSplit[0]

				# check the syntax for each field
				if str_field == 'symbols':
					lst_symbols = fun_check_symbols(str_argument)
					
		# check the other fields
		for str_line in lst_g:
			if str_line[0] == '#':
				pass
			elif '=' in str_line:
				lst_eqSplit = str_line.split('=',1)
				str_field = lst_eqSplit[0]
				str_argument = lst_eqSplit[1]

				# strip out in-line comments
				lst_argSplit = str_argument.split('#',1)
				str_argument = lst_argSplit[0]

				if str_field == 'formula':
					fun_check_formula(str_argument,lst_symbols)					
				
				elif str_field == 'pathToPrism':
					fun_check_path(str_argument)					

				elif str_field == 'trivial_length':
					fun_check_length(str_argument)					

				elif str_field == 'MCE_tolerance':
					fun_check_tolerance(str_argument)					

				else:
					raise Input_Field_Error(str_field)


	def fun_check_symbols(self,str_argument):
		lst_symbols = str_argument.split(' ') # symbols (variables) should have been given in a list separated by a single space
		lst_symbols = [x for x in lst_symbols if x != '']

		# make sure symbols don't contain illegal characters
		# - punctuation 
		# - a digit as the first character
		# - multiple variables of the same name
		# - a protected word (and,or,not,fanout)
		for str_symbol in lst_symbols:
			if (len(set(list(str_symbol)).intersection(list(string.punctuation))) != 0) or (str_symbol[0] in list(string.digits)) or (lst_symbols.count(str_symbol) > 1) or (str_symbol in ['and','or','not','fanout']):
				raise Illegal_Variable(str_symbol)
		
		# if we didn't raise an error, return the list of checked symbols
		return lst_symbols
		
	def fun_check_formula(self,str_argument,lst_symbols):
		import ast
		tree_parse = ast.parse(str_argument)
		allnames().visit(tree_parse)


	#def fun_check_path(self,str_argument):

	#def fun_check_length(self,str_argument):

	#def fun_check_tolerance(self,str_argument):





class allnames(ast.NodeVisitor):
	def visit_Module(self, node):
		self.names = set()
		self.generic_visit(node)
		print sorted(self.names)
	def visit_Name(self, node):
		self.names.add(node.id)





## Errors for this module
class Error(Exception): 
	# error base class
	pass

class Input_Field_Error(Error):
	# Exception raised for invalid fields in the input file.  There are only five input fields and they must be spelled correctly.
	# This error is raised when an invalid field name is entered by the user. 
	def __init__(self,expr):
		print "'Invalid field in input file: %s.  Valid fields are: symbols, formula, pathToPrism, trivial_length, and MCE_tolerance.  Check the input file and try again. '" %expr

class Illegal_Variable(Error):
	# Exception raised if one of the propositional variables given in the input has an illegal format.
	def __init__(self,expr):
		print "'Invalid formatting of symbol: %s.  Symbols should be given in a list separated by whitespace, should not contain illegal characters, and may not be duplicates of one another.  Please check the formatting and try again.'"%expr


				












	
