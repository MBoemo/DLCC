class Inputs:

	#No idea why this works

	def extract_logic(self,cmd_arg):
		import xml.etree.ElementTree as ET
		cmd_arg = str(cmd_arg)
		tree = ET.parse(cmd_arg)
		root = tree.getroot()
		for item in root.findall('LogicArguments'):
			logic_symbols = item.find('Symbols').text
			logic_equation = item.find('Equation').text
		import sympy
		from sympy import symbols
		from sympy import sympify
		from sympy.logic import simplify_logic
		sympy.var(logic_symbols)
		logic_equation = simplify_logic(sympify(logic_equation))
		return logic_equation

        def extract_topology(self,cmd_arg):
                import xml.etree.ElementTree as ET
                cmd_arg = str(cmd_arg)
                tree = ET.parse(cmd_arg)
                root = tree.getroot()
                for item in root.findall('Topology'):
                        display = item.find('Display_Topology').text
                        extension = item.find('File_Extension').text
                return [display,extension]


	def extract_prism(self,cmd_arg):
                import xml.etree.ElementTree as ET
                cmd_arg = str(cmd_arg)
                tree = ET.parse(cmd_arg)
                root = tree.getroot()
                for item in root.findall('ModelChecking'):
                        path = item.find('PathToPrism').text
                        intersect = item.find('SmartIntersect').text
			length = item.find('InitialiseLength').text
			error_bound = item.find('MaxErrTolerance').text
                return [path,intersect,length,error_bound]


