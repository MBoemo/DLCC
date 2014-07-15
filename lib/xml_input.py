class Inputs:

	def __init__(self):
		import xml.etree.ElementTree as ET
		self.ET = ET

	def extract_logic(self,str_cmd_arg):
		
		import sympy
		from sympy import symbols
		from sympy import sympify
		from sympy.logic import simplify_logic
		from pyparsing import nestedExpr # 

		print('Condensing Boolean logic expression...')
		tree_xml = self.ET.parse(str_cmd_arg) # takes the xml file specified on the command line and parses it into a tree
		root = tree_xml.getroot() # grab the root of the xml tree
		for item in root.findall('LogicArguments'): # search through the tree for the fields we want
			logic_symbols = item.find('Symbols').text
			logic_equation = item.find('Equation').text
		sympy.var(logic_symbols) # use sympy to make the logic symbols into symbolic logic variables
		simplified_logic_equation = simplify_logic(sympify(logic_equation)) # and use sympy to simplify the equation
		print('Simplified Boolean logic equation: ' + str(simplified_logic_equation)) 
		print('Done.')
		
		print('Calling pyparsing nested argument parser...')
		simplified_logic_equation = '('+str(simplified_logic_equation)+')' # needs to be surrounded by brackets so pyparsing can parse it into a list		
		lst_nested_logic_statement = nestedExpr('(',')').parseString(simplified_logic_equation).asList() # use pyparsing to parse the simplified logic equation into a list
		print('Done.')
		
		return lst_nested_logic_statement

        def extract_topology(self,str_cmd_arg):

                str_cmd_arg = str(str_cmd_arg)
                tree_xml = self.ET.parse(str_cmd_arg)
                root = tree_xml.getroot()
                for item in root.findall('Topology'):
                        display = item.find('Display_Topology').text
                        extension = item.find('File_Extension').text
                return [display,extension]


	def extract_prism(self,str_cmd_arg):

                str_cmd_arg = str(str_cmd_arg)
                tree_xml = self.ET.parse(str_cmd_arg)
                root = tree_xml.getroot()
                for item in root.findall('ModelChecking'):
                        path = item.find('PathToPrism').text
                        intersect = item.find('SmartIntersect').text
			length = item.find('InitialiseLength').text
			error_bound = item.find('MaxErrTolerance').text
                return [path,intersect,length,error_bound]


