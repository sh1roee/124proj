'''
CMSC 124: LOLCODE Semantics Evaluator (30% - Basic Operations)
Implements: arithmetic, concatenation, boolean, comparison, assignment, VISIBLE
'''

#  semantics evaluator for LOLCODE
class SemanticsEvaluator:
    def __init__(self, symbol_table):
        self.symbol_table = symbol_table
        self.output_buffer = []
    
    # evaluate arithmetic operations
    def evaluate_arithmetic(self, operation, operand1, operand2):
        # convert operands to numeric values
        val1 = self._to_numeric(operand1)
        val2 = self._to_numeric(operand2)
        
        if val1 is None or val2 is None:
            return None

        # perform the operation
        if operation == 'SUM OF':
            result = val1 + val2
        elif operation == 'DIFF OF':
            result = val1 - val2
        elif operation == 'PRODUKT OF':
            result = val1 * val2
        elif operation == 'QUOSHUNT OF':
            if val2 == 0:
                return None  # Division by zero
            result = val1 / val2
        elif operation == 'MOD OF':
            if val2 == 0:
                return None
            result = val1 % val2
        elif operation == 'BIGGR OF':
            result = max(val1, val2)
        elif operation == 'SMALLR OF':
            result = min(val1, val2)
        else:
            return None
        
        return result

    # evaluate boolean operations
    def evaluate_boolean(self, operation, operand1, operand2):
        # evaluate boolean operations
        val1 = self._to_bool(operand1)
        val2 = self._to_bool(operand2)
        
        if operation == 'BOTH OF':  # AND
            result = val1 and val2
        elif operation == 'EITHER OF':  # OR
            result = val1 or val2
        elif operation == 'WON OF':  # XOR
            result = val1 != val2
        else:
            return None
        
        return 'WIN' if result else 'FAIL'
    
    # evaluate comparison operations
    def evaluate_comparison(self, operation, operand1, operand2):
        val1 = self._to_numeric(operand1)
        val2 = self._to_numeric(operand2)
        
        if val1 is None or val2 is None:
            # try string comparison
            val1 = str(operand1)
            val2 = str(operand2)
        
        # perform the comparison
        if operation == 'BOTH SAEM':
            result = val1 == val2
        elif operation == 'DIFFRINT':
            result = val1 != val2
        else:
            return None
        
        return 'WIN' if result else 'FAIL'
    
    # evaluate unary NOT operation
    def evaluate_unary_not(self, operand):
        # evaluate NOT operation
        val = self._to_bool(operand)
        return 'FAIL' if val else 'WIN'
    
    #  evaluate string concatenation
    def evaluate_concatenation(self, operands):
        result = []
        for operand in operands:
            result.append(str(operand))
        return ''.join(result)
    
    def resolve_value(self, token_value, token_type):
        if token_type == 'Variable Identifier':
            if token_value in self.symbol_table:
                return self.symbol_table[token_value].get('value', 'NOOB')
            return 'NOOB'
        elif token_type in ['NUMBR Literal', 'NUMBAR Literal']:
            return token_value
        elif token_type == 'TROOF Literal':
            return token_value
        elif token_type == 'YARN Literal':
            return token_value
        else:
            return token_value
    
    def _to_numeric(self, value):
        if isinstance(value, (int, float)):
            return value
        
        # handle string inputs
        if isinstance(value, str):
            # handle TROOF values
            value_upper = value.upper()
            if value_upper == 'WIN':
                return 1
            elif value_upper == 'FAIL':
                return 0
            
            # try to parse as number
            try:
                if '.' in str(value):
                    return float(value)
                else:
                    return int(value)
            except (ValueError, AttributeError):
                # try to resolve as variable
                if value in self.symbol_table:
                    return self._to_numeric(self.symbol_table[value].get('value'))
                return None
        
        return None
    
    # convert to boolean
    def _to_bool(self, value):
        if isinstance(value, bool):
            return value
        
        if isinstance(value, str):
            value_upper = value.upper()
            if value_upper == 'WIN':
                return True
            elif value_upper == 'FAIL':
                return False
            
            # check if variable
            if value in self.symbol_table:
                return self._to_bool(self.symbol_table[value].get('value'))
            
            # empty string is false
            return len(value) > 0
        
        if isinstance(value, (int, float)):
            return value != 0
        
        return False
    
    # handle VISIBLE statement
    def get_output(self):
        return ''.join(self.output_buffer)
    
    # append to output buffer
    def clear_output(self):
        self.output_buffer = []
