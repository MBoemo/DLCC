class cls_symbolic_logic:

	def fun_simplifyLogic(self,str_symbols,str_formula):
		import sympy
		from sympy import symbols
		from sympy import sympify
		from sympy.logic import simplify_logic
		from pyparsing import nestedExpr

		sympy.var(str_symbols) # use sympy to make the logic symbols into symbolic logic variables
		simplified_logic_equation = simplify_logic(sympify(str_formula)) # and use sympy to simplify the equation

		print('Simplified formula: '+str(simplified_logic_equation))

		simplified_logic_equation = '('+str(simplified_logic_equation)+')' # needs to be surrounded by brackets so pyparsing can parse it into a list		
		lst_nested_logic_statement = nestedExpr('(',')').parseString(simplified_logic_equation).asList() # use pyparsing to parse the simplified logic equation into a list
		
		return lst_nested_logic_statement

      

