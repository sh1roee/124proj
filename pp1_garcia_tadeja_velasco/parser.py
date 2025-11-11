'''
CMSC 124: LOLCODE Syntax Analyzer
- Sophia Ysabel Garcia
- James Andrei Tadeja
- Ron Russell Velasco
'''

import lexer_analyzer
import os

class SyntaxAnalyzer:
    def __init__(self, tokens):
        self.lines = self.organize_tokens_by_line(tokens)
        self.current_line_number = min(self.lines.keys()) if self.lines else None
        self.current_tokens = self.lines[self.current_line_number] if self.lines else []
        self.current_position = 0
        self.current_token = self.current_tokens[0] if self.current_tokens else None
        self.error_messages = []
        self.variables = {"IT": {"value": None, "type": None}}
        self.in_wazzup_block = False
        self.inside_switch_block = False
    
    # organize tokens by line number
    def organize_tokens_by_line(self, tokens):
        organized = {}
        for token in tokens:
            if token.type != "Comment Line":
                if token.line_number not in organized:
                    organized[token.line_number] = []
                organized[token.line_number].append(token)
        return organized
    
    # log syntax errors
    def log_syntax_error(self, message, expected=None, found=None):
        if expected and found:
            error_message = (
                f"Syntax Error: {message}. Expected '{expected}', but found '{found}' "
                f"(line {self.current_line_number})"
            )
        elif expected:
            error_message = (
                f"Syntax Error: {message}. Expected '{expected}' "
                f"(line {self.current_line_number})"
            )
        else:
            error_message = f"Syntax Error: {message} (line {self.current_line_number})"
        
        self.error_messages.append(error_message)
        print(f"{error_message}")
    
    # print variables
    def print_variables(self):
        print("\nVariables:")
        for identifier, identifier_info in self.variables.items():
            value = identifier_info.get("value", "undefined")
            var_type = identifier_info.get("type", "unknown")
            print(f"Identifier: {identifier}, Value: {value}, Type: {var_type}")
    
    # advance to next line
    def advance_to_next_line(self):
        if self.current_line_number is None:
            self.current_tokens = []
            self.current_token = None
            return
        
        line_numbers = sorted(self.lines.keys())
        next_line_index = line_numbers.index(self.current_line_number) + 1
        if next_line_index < len(line_numbers):
            self.current_line_number = line_numbers[next_line_index]
            self.current_tokens = self.lines[self.current_line_number]
            self.current_position = 0
            self.current_token = self.current_tokens[0] if self.current_tokens else None
        else:
            self.current_tokens = []
            self.current_token = None
            self.current_line_number = None
    
    # advance to next token
    def advance_to_next_token(self):
        if self.current_position < len(self.current_tokens) - 1:
            self.current_position += 1
            self.current_token = self.current_tokens[self.current_position]
        else:
            self.current_token = None
    
    # parse expression
    def parse_expression(self):
        if self.current_token.type in ['NUMBR Literal', 'NUMBAR Literal', 'TROOF Literal']:
            result = self.current_token.value
            self.advance_to_next_token()
            return result
        elif self.current_token.type == 'YARN Literal':
            result = self.current_token.value
            self.advance_to_next_token()
            return result
        elif self.current_token.type == 'Variable Identifier':
            if self.current_token.value in self.variables:
                result = self.variables[self.current_token.value]
                self.advance_to_next_token()
                return result
            else:
                result = self.current_token.value
                self.advance_to_next_token()
                return result
        elif self.current_token.type in ['Arithmetic Operation', 'Boolean Operation', 'Comparison Operation']:
            return self.parse_operation()
        elif self.current_token.type == 'String Concatenation':
            return self.parse_concatenation()
        else:
            self.log_syntax_error("Expected literal or operation")
            return None
    
    # parse operations
    def parse_operation(self):
        operation = self.current_token.value
        self.advance_to_next_token()
        
        if operation == 'NOT':
            return self.parse_unary_operation(operation)
        elif operation in ['SUM OF', 'DIFF OF', 'PRODUKT OF', 'QUOSHUNT OF', 'MOD OF', 'BIGGR OF', 'SMALLR OF']:
            return self.parse_binary_operation(operation)
        elif operation in ['ALL OF', 'ANY OF']:
            return self.parse_infinite_arity_operation(operation)
        elif operation in ['BOTH OF', 'EITHER OF', 'WON OF', 'BOTH SAEM', 'DIFFRINT']:
            return self.parse_binary_operation(operation)
        elif operation == 'SMOOSH':
            return self.parse_concatenation()
        else:
            self.log_syntax_error("Unknown operation", found=operation)
            return f"Unknown operation '{operation}'"
    
    # parse unary operations (NOT)
    def parse_unary_operation(self, operation):
        operands = []
        
        if not self.current_token:
            self.log_syntax_error("Expected operand for 'NOT'")
            return f"{operation} Missing Operand"
        
        if self.current_token.type in ['TROOF Literal', 'Variable Identifier']:
            operands.append(self.current_token.value)
            self.advance_to_next_token()
        elif self.current_token.type in ['Arithmetic Operation', 'Boolean Operation', 'Comparison Operation']:
            operands.append(self.parse_operation())
        else:
            self.log_syntax_error("Expected TROOF, variable, or operation for 'NOT'", 
                                found=self.current_token.type if self.current_token else "None")
        
        print(f"Will evaluate '{operation} {operands[0]}'")
        return f"{operation} {operands[0]}" if operands else f"{operation} Missing Operand"
    
    # parse binary operations
    def parse_binary_operation(self, operation):
        def parse_single_operand():
            if not self.current_token:
                self.log_syntax_error(f"Missing operand for '{operation}'")
                return None
            
            if self.current_token.type in ['NUMBR Literal', 'NUMBAR Literal', 'TROOF Literal', 'Variable Identifier']:
                operand = self.current_token.value
                self.advance_to_next_token()
                return operand
            elif self.current_token.type == 'YARN Literal':
                operand = self.current_token.value
                self.advance_to_next_token()
                return operand
            elif self.current_token.type in ['Arithmetic Operation', 'Boolean Operation', 'Comparison Operation']:
                return self.parse_operation()
            else:
                self.log_syntax_error(f"Expected operand for '{operation}'",
                                    found=self.current_token.type if self.current_token else "None")
                return None
        
        first_operand = parse_single_operand()
        if first_operand is None:
            return f"{operation} Missing First Operand"
        
        if not self.current_token or self.current_token.value != 'AN':
            self.log_syntax_error(f"Missing 'AN' after first operand in '{operation}'")
            return f"{operation} {first_operand} Missing AN"
        
        self.advance_to_next_token()
        
        second_operand = parse_single_operand()
        if second_operand is None:
            return f"{operation} {first_operand} AN Missing Second Operand"
        
        print(f"Will evaluate '{operation} {first_operand} AN {second_operand}'")
        return f"{operation} {first_operand} AN {second_operand}"
    
    # parse infinite-arity operations (ALL OF/ANY OF)
    def parse_infinite_arity_operation(self, operation):
        operands = []
        
        if not self.current_token:
            self.log_syntax_error(f"Missing operands for '{operation}'")
            return f"{operation} Missing Operands"
        
        first_operand_parsed = False
        
        while self.current_token and self.current_token.value != 'MKAY':
            if self.current_token.value == 'AN':
                if not first_operand_parsed:
                    self.log_syntax_error(f"Unexpected 'AN' at the start of {operation}")
                    return f"{operation} Invalid Start with AN"
                
                self.advance_to_next_token()
                
                if not self.current_token:
                    self.log_syntax_error(f"Missing operand after 'AN' in {operation}")
                    return f"{operation} {' AN '.join(operands)} AN Missing Operand"
            
            if self.current_token.type in ['TROOF Literal', 'NUMBR Literal', 'NUMBAR Literal', 'Variable Identifier']:
                operands.append(self.current_token.value)
                first_operand_parsed = True
                self.advance_to_next_token()
            elif self.current_token.type in ['Arithmetic Operation', 'Boolean Operation', 'Comparison Operation']:
                operand = self.parse_operation()
                operands.append(operand)
                first_operand_parsed = True
            elif self.current_token.type == 'YARN Literal':
                operands.append(self.current_token.value)
                first_operand_parsed = True
                self.advance_to_next_token()
            else:
                self.log_syntax_error(f"Unexpected token in {operation}", 
                                    found=self.current_token.type if self.current_token else "None")
                return f"{operation} {' AN '.join(operands)} Unexpected Token"
            
            if self.current_token and self.current_token.value not in ['AN', 'MKAY']:
                if operands:
                    self.log_syntax_error(f"Missing 'AN' between operands in {operation}")
                    return f"{operation} {' AN '.join(operands)} Missing 'AN'"
        
        if not self.current_token or self.current_token.value != 'MKAY':
            self.log_syntax_error(f"Missing 'MKAY' at the end of {operation}")
            return f"{operation} {' AN '.join(operands)} Missing MKAY"
        
        self.advance_to_next_token()
        
        if self.current_token:
            self.log_syntax_error(f"Unexpected tokens after 'MKAY' in {operation}")
            return f"{operation} {' AN '.join(operands)} MKAY Extra Tokens"
        
        if not operands:
            self.log_syntax_error(f"No operands provided for {operation}")
            return f"{operation} Missing Operands"
        
        print(f"Will evaluate '{operation} {' AN '.join(operands)} MKAY'")
        return f"{operation} {' AN '.join(operands)} MKAY"
    
    # parse string concatenation
    def parse_concatenation(self):
        operands = []
        self.advance_to_next_token()
        
        first_operand_parsed = False
        
        while self.current_token:
            if first_operand_parsed and self.current_token.value != 'AN':
                self.log_syntax_error("Expected 'AN' between operands in SMOOSH", found=self.current_token.value)
                return f"SMOOSH {' + '.join(operands)} Missing AN"
            
            if self.current_token.value == 'AN':
                if not first_operand_parsed:
                    self.log_syntax_error("Unexpected 'AN' at the start of SMOOSH")
                    return "SMOOSH Invalid Start with AN"
                
                self.advance_to_next_token()
                
                if not self.current_token:
                    self.log_syntax_error("Missing operand after 'AN' in SMOOSH")
                    return f"SMOOSH {' + '.join(operands)} AN Missing Operand"
            
            if self.current_token.type in ['NUMBR Literal', 'NUMBAR Literal', 'TROOF Literal', 'Variable Identifier']:
                if self.current_token.type == 'Variable Identifier' and self.current_token.value in self.variables:
                    operands.append(str(self.variables[self.current_token.value]['value']))
                else:
                    operands.append(str(self.current_token.value))
                first_operand_parsed = True
                self.advance_to_next_token()
            elif self.current_token.type == 'YARN Literal':
                operands.append(self.current_token.value)
                first_operand_parsed = True
                self.advance_to_next_token()
            elif self.current_token.type in ['Arithmetic Operation', 'Boolean Operation', 'Comparison Operation']:
                operation_output = self.parse_operation()
                operands.append(operation_output)
                first_operand_parsed = True
            else:
                self.log_syntax_error("Unexpected token in SMOOSH", found=self.current_token.type)
                return f"SMOOSH {' + '.join(operands)} Unexpected Token"
        
        if not operands:
            self.log_syntax_error("No operands specified after SMOOSH")
            return "SMOOSH Missing Operands"
        elif len(operands) == 1:
            self.log_syntax_error("Only one operand specified after SMOOSH, requires at least two")
            return f"SMOOSH {' + '.join(operands)} Missing AN"
        
        return f"{' + '.join(operands)}"
    
    # parse variable declaration
    def parse_variable_declaration(self):
        self.advance_to_next_token()
        
        if not self.current_token or self.current_token.type != 'Variable Identifier':
            self.log_syntax_error("Variable name is missing or invalid after 'I HAS A'")
            return
        
        variable_name = self.current_token.value
        self.advance_to_next_token()
        
        if self.current_token and self.current_token.value == "ITZ":
            self.advance_to_next_token()
            
            if not self.current_token:
                self.log_syntax_error(f"Missing expression to initialize variable '{variable_name}' after 'ITZ'")
                return
            
            if self.current_token.type == 'YARN Literal':
                data_type = 'YARN'
            elif self.current_token.type in ['Arithmetic Operation', 'Boolean Operation', 'Comparison Operation', 'String Concatenation', 'Typecasting Operation']:
                data_type = None
            else:
                data_type = self.current_token.type.split()[0]
            
            value = self.parse_expression()
            
            self.variables[variable_name] = {
                "value": value,
                "type": data_type
            }
            print(f"Declared variable {variable_name} initialized to {value} with type {data_type}")
        else:
            if self.current_token and self.current_token.value != 'ITZ':
                self.log_syntax_error("Expected 'ITZ' after variable name for initialization", found=self.current_token.value)
                return
            
            self.variables[variable_name] = {
                "value": "NOOB",
                "type": "NOOB"
            }
            print(f"Declared uninitialized variable {variable_name} (default value: None, type: NOOB)")
    
    # parse print statement
    def parse_print(self):
        output = []
        self.advance_to_next_token()
        
        if not self.current_token:
            self.log_syntax_error("No output specified after VISIBLE")
            return "VISIBLE Missing Output"
        
        while self.current_token:
            if self.current_token.type in ['NUMBR Literal', 'NUMBAR Literal', 'TROOF Literal', 'Variable Identifier']:
                output.append(str(self.current_token.value))
                self.advance_to_next_token()
            elif self.current_token.type == 'YARN Literal':
                output.append(self.current_token.value)
                self.advance_to_next_token()
            elif self.current_token.type in ['Arithmetic Operation', 'Boolean Operation', 'Comparison Operation']:
                output.append(self.parse_operation())
            elif self.current_token.type == 'String Concatenation':
                output.append(self.parse_concatenation())
            elif self.current_token.type in ['Parameter Delimiter', 'Output Separator']:
                self.advance_to_next_token()
            else:
                self.log_syntax_error("Unexpected token in VISIBLE", found=self.current_token.type)
                break
        
        print('Will print "' + ''.join(output) + '"')
    
    # parse input statement
    def parse_input(self):
        self.advance_to_next_token()
        
        if not self.current_token:
            self.log_syntax_error("Missing variable identifier after GIMMEH")
            return "GIMMEH Missing Variable"
        
        variable_name = self.current_token.value
        self.advance_to_next_token()
        
        if self.current_token:
            self.log_syntax_error("Unexpected tokens after variable identifier", found=self.current_token.type)
        
        print(f"Will store user input in variable {variable_name}")
        return variable_name
    
    # parse assignment
    def parse_assignment(self):
        if not self.current_token or self.current_token.type != 'Variable Identifier':
            self.log_syntax_error("Invalid variable name for assignment", 
                                found=self.current_token.type if self.current_token else "None")
            return "Assignment Missing Variable"
        
        variable_name = self.current_token.value
        self.advance_to_next_token()
        
        if not self.current_token or self.current_token.value != "R":
            self.log_syntax_error("Expected assignment operator 'R'", 
                                found=self.current_token.value if self.current_token else "None")
            return f"{variable_name} Missing Assignment Operator"
        
        self.advance_to_next_token()
        
        if not self.current_token:
            self.log_syntax_error("Missing value after assignment operator", found="None")
            return f"{variable_name} R Missing Value"
        
        if self.current_token.type in ['NUMBR Literal', 'NUMBAR Literal', 'TROOF Literal']:
            value = self.current_token.value
            self.advance_to_next_token()
            print(f"Assigned literal value '{value}' to variable {variable_name}")
            return f"{variable_name} R {value}"
        elif self.current_token.type == 'YARN Literal':
            value = self.current_token.value
            self.advance_to_next_token()
            print(f"Assigned string '{value}' to variable {variable_name}")
            return f"{variable_name} R {value}"
        elif self.current_token.type == 'Variable Identifier':
            value = self.current_token.value
            self.advance_to_next_token()
            print(f"Assigned value of variable {value} to variable {variable_name}")
            return f"{variable_name} R {value}"
        elif self.current_token.type in ['Arithmetic Operation', 'Boolean Operation', 'Comparison Operation']:
            value = self.parse_operation()
            print(f"Assigned result of operation {value} to variable {variable_name}")
            return f"{variable_name} R {value}"
        elif self.current_token.type == 'String Concatenation':
            value = self.parse_concatenation()
            print(f"Assigned concatenated string '{value}' to variable {variable_name}")
            return f"{variable_name} R {value}"
        elif self.current_token.type == 'Typecasting Operation':
            value = self.parse_typecasting()
            print(f"Assigned typecasted value '{value}' to variable {variable_name}")
            return f"{variable_name} R {value}"
        else:
            self.log_syntax_error("Invalid value for assignment", found=self.current_token.type)
            return f"{variable_name} R Invalid Value: {self.current_token.type}"
    
    # parse typecasting
    def parse_typecasting(self):
        if self.current_token.value == 'MAEK':
            self.advance_to_next_token()
            
            if not self.current_token or self.current_token.value != 'A':
                self.log_syntax_error("Expected 'A' after 'MAEK'", 
                                    found=self.current_token.value if self.current_token else "None")
                return "MAEK Missing A"
            
            self.advance_to_next_token()
            
            if self.current_token and self.current_token.type in ['Variable Identifier', 'NUMBR Literal', 'NUMBAR Literal', 'TROOF Literal']:
                cast_value = self.current_token.value
                self.advance_to_next_token()
                
                if self.current_token and self.current_token.type == 'Type Literal':
                    target_type = self.current_token.value
                    self.advance_to_next_token()
                    print(f"Casting value of {cast_value} to type '{target_type}'")
                    return f"MAEK A {cast_value} {target_type}"
                else:
                    self.log_syntax_error("Expected type literal after value in 'MAEK A' operation", 
                                        found=self.current_token.type if self.current_token else "None")
                    return "MAEK A Missing Type Literal"
            else:
                self.log_syntax_error("Expected value to cast in 'MAEK A' operation", 
                                    found=self.current_token.type if self.current_token else "None")
                return "MAEK A Missing Value"
        
        self.advance_to_next_token()
        
        if self.current_token.value == 'IS NOW A':
            cast_value = self.current_tokens[self.current_position - 1].value
            self.advance_to_next_token()
            
            if self.current_token and self.current_token.type == 'Type Literal':
                target_type = self.current_token.value
                self.advance_to_next_token()
                print(f"Casting value of {cast_value} to type {target_type}")
                return f"IS NOW A {target_type}"
            else:
                self.log_syntax_error("Expected type literal after 'IS NOW A'", 
                                    found=self.current_token.type if self.current_token else "None")
                return "IS NOW A Missing Type Literal"
        else:
            self.log_syntax_error("Expected 'MAEK' or 'IS NOW A' for typecasting", 
                                found=self.current_token.value if self.current_token else "None")
            return "Typecasting Missing Operator"
    
    # parse a single line
    def parse_line(self):
        print(f"\nParsing line {self.current_line_number}: {self.current_tokens}")
        
        while self.current_token:
            if self.current_token.value == 'WAZZUP':
                self.in_wazzup_block = True
                print("Entered 'WAZZUP' block")
            elif self.current_token.value == 'BUHBYE' and self.in_wazzup_block:
                self.in_wazzup_block = False
                print("Exited 'WAZZUP' block")
            elif self.in_wazzup_block and self.current_token.value == 'I HAS A':
                self.parse_variable_declaration()
            elif self.current_token.type == 'Output Keyword':
                self.parse_print()
            elif self.current_token.type == 'Input Keyword':
                self.parse_input()
            elif self.current_token.value == 'O RLY?':
                self.parse_conditional()
            elif self.current_token.value == 'IM IN YR':
                self.parse_loop()
            elif self.current_token.value == 'HOW IZ I':
                self.parse_function()
            elif self.current_token.value == 'I IZ':
                self.parse_functioncall()
            elif self.current_token.value == 'WTF?':
                self.parse_switch()
                print(f"Entering WTF? block at line {self.current_line_number}")
            elif self.current_token.value == 'OMG' or self.current_token.value == 'OMGWTF':
                if not self.inside_switch_block:
                    self.log_syntax_error(f"Found '{self.current_token.value}' without preceding 'WTF?'", 
                                        found=self.current_token.value)
                    return {"error": f"Invalid token '{self.current_token.value}' at line {self.current_line_number}"}
            elif self.current_token.type == 'Variable Identifier':
                next_token = self.current_tokens[self.current_position + 1] if self.current_position + 1 < len(self.current_tokens) else None
                if next_token and next_token.type == 'Variable Assignment':
                    self.parse_assignment()
                elif next_token and next_token.type == 'Typecasting Operation':
                    self.parse_typecasting()
                else:
                    # Unknown statement starting with Variable Identifier
                    self.log_syntax_error("Unknown statement", found=self.current_token.value)
                    return
            else:
                # General fallback for unrecognized tokens
                self.log_syntax_error("Unexpected or invalid statement", found=self.current_token.value)
                return
            
            self.advance_to_next_token()
    
    # parse conditional (O RLY?)
    def parse_conditional(self):
        has_o_rly = False
        for line_number, tokens in self.lines.items():
            for token in tokens:
                if token.value == "O RLY?":
                    has_o_rly = True
                elif token.value == "YA RLY" and not has_o_rly:
                    self.log_syntax_error("Found 'YA RLY' without preceding 'O RLY?'", found="YA RLY without O RLY?")
        
        if self.current_token.value == "O RLY?":
            print("Parsing conditional 'O RLY?'")
            self.advance_to_next_token()
            
            while not self.current_token and self.current_line_number is not None:
                self.advance_to_next_line()
            
            if self.current_token:
                print(f"DEBUG: Token after 'O RLY?': {self.current_token.value}, Type: {self.current_token.type}")
            else:
                print("DEBUG: No token found after 'O RLY?'")
            
            if self.current_token and self.current_token.value == "YA RLY":
                print("Found 'YA RLY', parsing <if code block>")
                self.advance_to_next_line()
                
                while self.current_token and self.current_token.value not in ["NO WAI", "OIC"]:
                    self.parse_line()
                    self.advance_to_next_line()
                
                if self.current_token and self.current_token.value == "NO WAI":
                    print("Found 'NO WAI', parsing <else code block>")
                    self.advance_to_next_line()
                    
                    while self.current_token and self.current_token.value != "OIC":
                        self.parse_line()
                        self.advance_to_next_line()
                
                if self.current_token and self.current_token.value == "OIC":
                    print("Found 'OIC', end of conditional block")
                    self.advance_to_next_token()
                else:
                    self.log_syntax_error("Expected 'OIC' to close 'O RLY?' block", 
                                        found=self.current_token.value if self.current_token else "None")
            else:
                self.log_syntax_error("Expected 'YA RLY' after 'O RLY?'", 
                                    found=self.current_token.value if self.current_token else "None")
        else:
            self.log_syntax_error("Expected 'O RLY?' for conditional block", 
                                found=self.current_token.value if self.current_token else "None")
    
    # parse loop (IM IN YR)
    def parse_loop(self):
        if self.current_token.value == "IM IN YR":
            print("Parsing loop 'IM IN YR'")
            self.advance_to_next_token()
            
            if not self.current_token or self.current_token.type != "Variable Identifier":
                self.log_syntax_error("Expected loop label after 'IM IN YR'",
                                    found=self.current_token.value if self.current_token else "None")
                return
            
            loop_label = self.current_token.value
            print(f"Found loop label: {loop_label}")
            self.advance_to_next_token()
            
            if not self.current_token or self.current_token.value not in ["UPPIN", "NERFIN"]:
                self.log_syntax_error("Expected loop operation (UPPIN/NERFIN) after loop label",
                                    found=self.current_token.value if self.current_token else "None")
                return
            
            operation = self.current_token.value
            print(f"Found loop operation: {operation}")
            self.advance_to_next_token()
            
            if not self.current_token or self.current_token.value != "YR":
                self.log_syntax_error("Expected 'YR' after loop operation",
                                    found=self.current_token.value if self.current_token else "None")
                return
            
            print(f"Found 'YR' after loop operation")
            self.advance_to_next_token()
            
            if not self.current_token or self.current_token.type !="Variable Identifier":
                self.log_syntax_error("Expected variable name after 'YR'",
                                    found=self.current_token.value if self.current_token else "None")
                return
            
            loop_variable = self.current_token.value
            print(f"Found loop variable: {loop_variable}")
            self.advance_to_next_token()
            
            if self.current_token and self.current_token.value in ["TIL", "WILE"]:
                loop_condition = self.current_token.value
                print(f"Found loop condition: {loop_condition}")
                self.advance_to_next_token()
                
                condition_expression = self.parse_expression()
                if condition_expression is None:
                    self.log_syntax_error("Invalid loop condition expression")
                    return
                print(f"Loop condition expression: {condition_expression}")
            else:
                self.log_syntax_error("Expected loop condition (TIL/WILE) after loop variable",
                                    found=self.current_token.value if self.current_token else "None")
                return
            
            print(f"Parsing loop body for loop '{loop_label}'")
            
            while True:
                if not self.current_token:
                    self.advance_to_next_line()
                
                if self.current_token and self.current_token.value == "IM OUTTA YR":
                    break
                
                if self.current_token:
                    self.parse_line()
                else:
                    break
            
            print(f"DEBUG: Exiting loop body for '{loop_label}', current token: {self.current_token.value if self.current_token else 'None'}")
            
            if self.current_token and self.current_token.value == "IM OUTTA YR":
                self.advance_to_next_token()
                
                print(f"DEBUG: Token after 'IM OUTTA YR': {self.current_token.value if self.current_token else 'None'}")
                
                if self.current_token and self.current_token.value == loop_label:
                    print(f"Loop '{loop_label}' closed correctly")
                    self.advance_to_next_token()
                else:
                    self.log_syntax_error(f"Expected loop label '{loop_label}' after 'IM OUTTA YR'",
                                        found=self.current_token.value if self.current_token else "None")
            else:
                self.log_syntax_error(f"Expected 'IM OUTTA YR {loop_label}' to close loop",
                                    found=self.current_token.value if self.current_token else "None")
        else:
            self.log_syntax_error("Expected 'IM IN YR' to define a loop",
                                found=self.current_token.value if self.current_token else "None")
    
    # parse switch statement (WTF?)
    def parse_switch(self):
        self.inside_switch_block = True
        if self.current_token and self.current_token.value == "WTF?":
            print("\nSwitch starts with 'WTF?'")
            self.advance_to_next_line()
            
            found_cases = False
            
            while self.current_token:
                if self.current_token.value == "OIC":
                    break
                
                if self.current_token.value == "OMG":
                    found_cases = True
                    print("DEBUG: Found 'OMG'")
                    self.advance_to_next_token()
                    
                    if not self.current_token or self.current_token.type not in ["NUMBR Literal", "NUMBAR Literal", "YARN Literal", "TROOF Literal"]:
                        self.log_syntax_error("Expected literal value after 'OMG'",
                                            found=self.current_token.value if self.current_token else "None")
                        return
                    
                    case_value = self.current_token.value
                    print(f"DEBUG: Found case value: {case_value}")
                    self.advance_to_next_token()
                    
                    while self.current_token and self.current_token.value == "OMG":
                        print(f"DEBUG: Parsing line in case {case_value}: {self.current_token.value}")
                        self.parse_line()
                        if self.current_token is None:
                            self.advance_to_next_line()
                
                elif self.current_token.value == "OMGWTF":
                    found_cases = True
                    print("DEBUG: Found 'OMGWTF'")
                    self.parse_line()
                    if self.current_token is None:
                        self.advance_to_next_line()
                
                self.parse_line()
                self.advance_to_next_line()
            
            if self.current_token and self.current_token.value == "OIC":
                print("\nSwitch ends with 'OIC'")
            else:
                self.log_syntax_error("Switch must end with 'OIC'")
            
            if not found_cases:
                self.log_syntax_error("Switch must have at least one case (OMG/OMGWTF)")
        else:
            self.log_syntax_error("Switch must start with 'WTF?'")
        
        return self.error_messages, self.variables
    
    # parse function definition (HOW IZ I)
    def parse_function(self):
        has_how_iz_i = False
        for line_number, tokens in self.lines.items():
            for token in tokens:
                if token.value == "HOW IZ I":
                    has_how_iz_i = True
                elif token.value == "IF U SAY SO" and not has_how_iz_i:
                    self.log_syntax_error("Found 'IF U SAY SO' without preceding 'HOW IZ I'", 
                                        found="IF U SAY SO without HOW IZ I")
        
        if self.current_token and self.current_token.value == "HOW IZ I":
            print("\nFunction starts with 'HOW IZ I'")
            self.advance_to_next_token()
            
            if not self.current_token or self.current_token.type != "Variable Identifier":
                self.log_syntax_error("Expected function name after 'HOW IZ I'",
                                    found=self.current_token.value if self.current_token else "None")
                return
            
            function_name = self.current_token.value
            print(f"Found function name: {function_name}")
            self.advance_to_next_token()
            
            parameters = []
            
            while self.current_token:
                if self.current_token and self.current_token.value == "IF U SAY SO":
                    break
                
                if self.current_token and self.current_token.value == "YR":
                    self.advance_to_next_token()
                    if not self.current_token or self.current_token.type != "Variable Identifier":
                        self.log_syntax_error("Expected parameter name after 'YR'",
                                            found=self.current_token.value if self.current_token else "None")
                        return
                    
                    parameter_name = self.current_token.value
                    parameters.append(parameter_name)
                    print(f"Found parameter name: {parameter_name}")
                    self.advance_to_next_token()
                    
                    if self.current_token and self.current_token.value == "AN":
                        self.advance_to_next_token()
                    elif self.current_token and self.current_token.value == "YR":
                        self.log_syntax_error("Expected 'AN' between multiple parameters, but found another 'YR'",
                                            found=self.current_token.value)
                        return
                
                print("Parameter list:", parameters)
                
                if self.current_token and self.current_token.value == "FOUND YR":
                    self.advance_to_next_token()
                    
                    if self.current_token:
                        return_value = self.current_token.type
                        
                        if return_value in ["NUMBR Literal", "NUMBAR Literal", "TROOF Literal", "YARN Literal"]:
                            print(f"Return statement value: {return_value}")
                            self.advance_to_next_token()
                        elif return_value == "Variable Identifier":
                            print(f"Return statement variable: {return_value}")
                            self.advance_to_next_token()
                        elif self.current_token and self.current_token.type == "Arithmetic Operation":
                            operator = self.current_token.value
                            self.advance_to_next_token()
                            
                            if not self.current_token:
                                self.log_syntax_error("Missing first operand in arithmetic operation after 'AN'", found="None")
                                return
                            
                            if self.current_token and self.current_token.type not in ["NUMBR Literal", "NUMBAR Literal", "Variable Identifier"]:
                                self.log_syntax_error("Invalid first operand for arithmetic operation",
                                                    found=self.current_token.value if self.current_token else "None")
                                return
                            
                            operand1 = self.current_token.value
                            print(f"Found first operand: {operand1}")
                            self.advance_to_next_token()
                            
                            if not self.current_token or self.current_token.value != "AN":
                                self.log_syntax_error("Expected 'AN' before second operand in arithmetic operation",
                                                    found=self.current_token.value if self.current_token else "None")
                                return
                            self.advance_to_next_token()
                            
                            if not self.current_token:
                                self.log_syntax_error("Missing second operand in arithmetic operation after 'AN'", found="None")
                                return
                            
                            if self.current_token and self.current_token.type not in ["NUMBR Literal", "NUMBAR Literal", "Variable Identifier"]:
                                self.log_syntax_error("Invalid second operand for arithmetic operation",
                                                    found=self.current_token.value if self.current_token else "None")
                                return
                            
                            operand2 = self.current_token.value
                            print(f"Found second operand: {operand2}")
                            self.advance_to_next_token()
                            
                            print(f"Found valid arithmetic operation: {operand1} {operator} {operand2}")
                        else:
                            self.log_syntax_error("Invalid return value. Must be a literal, variable, or valid arithmetic operation",
                                                found=self.current_token.value if self.current_token else "None")
                            return
                    else:
                        self.log_syntax_error("Expected return value after 'FOUND YR'", found="None")
                
                self.parse_line()
                self.advance_to_next_line()
            
            if self.current_token and self.current_token.value == "IF U SAY SO":
                print("\nFunction ends with 'IF U SAY SO'")
            else:
                self.log_syntax_error("Function must end with 'IF U SAY SO'")
        else:
            self.log_syntax_error("Function must start with 'HOW IZ I'")
    
    # parse function call (I IZ)
    def parse_functioncall(self):
        if self.current_token and self.current_token.value == "I IZ":
            print("\nFunction call 'I IZ'")
            self.advance_to_next_token()
            
            if not self.current_token or self.current_token.type != "Variable Identifier":
                self.log_syntax_error("Expected function name after 'I IZ'",
                                    found=self.current_token.value if self.current_token else "None")
                return
            
            function_name = self.current_token.value
            print(f"Found function name: {function_name}")
            self.advance_to_next_token()
            
            while self.current_token and self.current_token.value == "YR":
                self.advance_to_next_token()
                
                if self.current_token.type in ["NUMBR Literal", "NUMBAR Literal", "TROOF Literal", "YARN Literal", "Variable Identifier"]:
                    argument_value = self.current_token.value
                    print(f"Found argument: {argument_value}")
                    self.advance_to_next_token()
                elif self.current_token and self.current_token.type == "Arithmetic Operation":
                    operator = self.current_token.value
                    self.advance_to_next_token()
                    
                    if not self.current_token:
                        self.log_syntax_error("Missing first operand in arithmetic operation after 'YR'", found="None")
                        return
                    
                    if self.current_token and self.current_token.type not in ["NUMBR Literal", "NUMBAR Literal", "Variable Identifier"]:
                        self.log_syntax_error("Invalid first operand for arithmetic operation",
                                            found=self.current_token.value if self.current_token else "None")
                        return
                    
                    operand1 = self.current_token.value
                    print(f"Found first operand: {operand1}")
                    self.advance_to_next_token()
                    
                    if not self.current_token or self.current_token.value != "AN":
                        self.log_syntax_error("Expected 'AN' before second operand in arithmetic operation",
                                            found=self.current_token.value if self.current_token else "None")
                        return
                    self.advance_to_next_token()
                    
                    if not self.current_token:
                        self.log_syntax_error("Missing second operand in arithmetic operation after 'AN'", found="None")
                        return
                    
                    if self.current_token and self.current_token.type not in ["NUMBR Literal", "NUMBAR Literal", "Variable Identifier"]:
                        self.log_syntax_error("Invalid second operand for arithmetic operation",
                                            found=self.current_token.value if self.current_token else "None")
                        return
                    
                    operand2 = self.current_token.value
                    print(f"Found second operand: {operand2}")
                    self.advance_to_next_token()
                    
                    print(f"Found valid arithmetic operation: {operand1} {operator} {operand2}")
                elif self.current_token.value == "I IZ":
                    argument_value = self.parse_functioncall()
                    print(f"Found nested function call as argument: {argument_value}")
                else:
                    self.log_syntax_error("Expected literal, variable, or function call after 'YR'",
                                        found=self.current_token.value if self.current_token else "None")
                    return
                
                if self.current_token and self.current_token.value == "AN":
                    self.advance_to_next_token()
                    
                    if not self.current_token or self.current_token.value != "YR":
                        self.log_syntax_error("Expected another argument after 'AN'",
                                            found=self.current_token.value if self.current_token else "None")
                        return
                else:
                    break
            
            print(f"Function call to '{function_name}' parsed successfully.")
        else:
            self.log_syntax_error("Function call must start with 'I IZ'")
    
    # parse program (entry point)
    def parse_program(self):
        print("\nSYNTAX ANALYSIS")
        
        if self.current_token and self.current_token.value == "HAI":
            print("\nProgram starts with 'HAI'")
            self.advance_to_next_line()
            
            while self.current_line_number is not None and self.current_token:
                if self.current_token.value == "KTHXBYE":
                    break
                
                self.parse_line()
                
                if self.error_messages and self.error_messages[-1].startswith("Syntax Error: Function must end with 'IF U SAY SO'"):
                    print("Found 'Function must end with IF U SAY SO' error. Stopping further parsing.")
                    break
                
                self.advance_to_next_line()
            
            # Always verify program termination. Log once if missing.
            if self.current_token and self.current_token.value == "KTHXBYE":
                print("\nProgram ends with 'KTHXBYE'")
            else:
                if not any("Program must end with 'KTHXBYE'" in e for e in self.error_messages):
                    self.log_syntax_error("Program must end with 'KTHXBYE'")
        else:
            self.log_syntax_error("Program must start with 'HAI'")
        
        return self.error_messages


# function to read file
def readFile():
    path = input("Enter the LOLCODE file or directory path: ").strip()
    try:
        if not os.path.exists(path):
            print(f"Error: Path '{path}' does not exist.")
            return None
        
        if os.path.isfile(path):
            if not path.endswith(".lol"):
                print(f"Error: Invalid file type. Only .lol files are supported.")
                return None
            
            try:
                with open(path, "r", encoding='utf-8') as f:
                    content = f.read()
                filename = os.path.basename(path)
                return {filename: content}
            except Exception as e:
                print(f"Error reading file '{path}': {e}")
                return None
        
        elif os.path.isdir(path):
            files_content = {}
            lol_files = [f for f in os.listdir(path) if f.endswith(".lol")]
            
            if not lol_files:
                print(f"Warning: No .lol files found in directory '{path}'.")
                return None
            
            for filename in lol_files:
                filepath = os.path.join(path, filename)
                try:
                    with open(filepath, "r", encoding='utf-8') as f:
                        files_content[filename] = f.read()
                except Exception as e:
                    print(f"Error reading file '{filename}': {e}. Skipping.")
                    continue
            
            if not files_content:
                print(f"Error: Failed to read any files from directory '{path}'.")
                return None
            
            print(f"Successfully read {len(files_content)} file(s) from directory.")
            return files_content
        else:
            print(f"Error: '{path}' is neither a file nor a directory.")
            return None
    except Exception as e:
        print(f"Unexpected error when processing '{path}': {e}")
        return None


# menu function
def menu():
    print("-----------------------------------")
    print("LOLCODE Syntax Analyzer")
    print("-----------------------------------")
    print("[1] Read and Analyze LOLCODE File/Directory")
    print("[2] Type LOLCODE String to Analyze")
    print("[3] Exit\n")


# main function
def main():
    while True:
        menu()
        choice = input("Enter your choice: ")
        
        if choice == '1':
            content = readFile()
            if content:
                for filename, file_content in content.items():
                    print(f"\n--- Analyzing: {filename} ---")
                    tokens = lexer_analyzer.tokenize(file_content)
                    
                    if tokens:
                        analyzer = SyntaxAnalyzer(tokens)
                        errors = analyzer.parse_program()
                        
                        if errors:
                            print("\nSyntax Errors found:")
                            for e in errors:
                                print(e)
                        else:
                            print("\nNo syntax errors detected.")
                        
                        analyzer.print_variables()
            else:
                print("No content to analyze.")
        
        elif choice == '2':
            input_string = input("Enter LOLCODE string to analyze: ").replace("\\n", "\n")
            if input_string.strip():
                tokens = lexer_analyzer.tokenize(input_string)
                
                if tokens:
                    analyzer = SyntaxAnalyzer(tokens)
                    errors = analyzer.parse_program()
                    
                    if errors:
                        print("\nSyntax Errors found:")
                        for e in errors:
                            print(e)
                    else:
                        print("\nNo syntax errors detected.")
                    
                    analyzer.print_variables()
            else:
                print("No input string provided.")
        
        elif choice == '3':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()