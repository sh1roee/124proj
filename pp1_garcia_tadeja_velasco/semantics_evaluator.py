'''
CMSC 124: LOLCODE Semantics Evaluator (30% - Basic Operations)
Implements: arithmetic, concatenation, boolean, comparison, assignment, VISIBLE
'''

class SemanticsEvaluator:
    """Lightweight semantics evaluator for basic LOLCODE operations"""
    
    def __init__(self, symbol_table):
        self.symbol_table = symbol_table
        self.output_buffer = []
    
    def evaluate_arithmetic(self, operation, operand1, operand2):
        """Evaluate arithmetic operations"""
        # Convert operands to numeric values
        val1 = self._to_numeric(operand1)
        val2 = self._to_numeric(operand2)
        
        if val1 is None or val2 is None:
            return None
        
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
    
    def evaluate_boolean(self, operation, operand1, operand2):
        """Evaluate boolean operations"""
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
    
    def evaluate_comparison(self, operation, operand1, operand2):
        """Evaluate comparison operations"""
        val1 = self._to_numeric(operand1)
        val2 = self._to_numeric(operand2)
        
        if val1 is None or val2 is None:
            # Try string comparison
            val1 = str(operand1)
            val2 = str(operand2)
        
        if operation == 'BOTH SAEM':
            result = val1 == val2
        elif operation == 'DIFFRINT':
            result = val1 != val2
        else:
            return None
        
        return 'WIN' if result else 'FAIL'
    
    def evaluate_unary_not(self, operand):
        """Evaluate NOT operation"""
        val = self._to_bool(operand)
        return 'FAIL' if val else 'WIN'
    
    def evaluate_concatenation(self, operands):
        """Evaluate SMOOSH (string concatenation)"""
        result = []
        for operand in operands:
            result.append(str(operand))
        return ''.join(result)
    
    def resolve_value(self, token_value, token_type):
        """Resolve a token to its actual value"""
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
        """Convert value to numeric (int or float)"""
        if isinstance(value, (int, float)):
            return value
        
        # Handle string representations
        if isinstance(value, str):
            # Handle TROOF values
            value_upper = value.upper()
            if value_upper == 'WIN':
                return 1
            elif value_upper == 'FAIL':
                return 0
            
            # Try to parse as number
            try:
                if '.' in str(value):
                    return float(value)
                else:
                    return int(value)
            except (ValueError, AttributeError):
                # Try to parse as variable name
                if value in self.symbol_table:
                    return self._to_numeric(self.symbol_table[value].get('value'))
                return None
        
        return None
    
    def _to_bool(self, value):
        """Convert value to boolean"""
        if isinstance(value, bool):
            return value
        
        if isinstance(value, str):
            value_upper = value.upper()
            if value_upper == 'WIN':
                return True
            elif value_upper == 'FAIL':
                return False
            
            # Check if it's a variable
            if value in self.symbol_table:
                return self._to_bool(self.symbol_table[value].get('value'))
            
            # Empty string is false, non-empty is true
            return len(value) > 0
        
        if isinstance(value, (int, float)):
            return value != 0
        
        return False
    
    def get_output(self):
        """Get accumulated output"""
        return ''.join(self.output_buffer)
    
    def clear_output(self):
        """Clear output buffer"""
        self.output_buffer = []
