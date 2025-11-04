'''
CMSC 124: LOLCODE Lexical Analyzer
- Sophia Ysabel Garcia
- James Andrei Tadeja
- Ron Russell Velasco
'''

import re, os

tokens = [
    
    # invalid keywords. these are declared first to avoid partial matches
    (r'O RLY\b', 'INVALID Keyword'),
    (r'WTF\b', 'INVALID Keyword'),
    
    # Code Delimiters
    (r'HAI\b', 'Code Delimiter'),
    (r'KTHXBYE\b', 'Code Delimiter'),
    
    # Comments
    (r'BTW.*', 'Comment Line'),
    (r'OBTW\b', 'Comment Line'),
    (r'TLDR\b', 'Comment Line'),
    
    # Variable Declaration and Assignment
    (r'I HAS A\b', 'Variable Declaration'),
    (r'ITZ\b', 'Variable Assignment'),
    (r'R\b', 'Variable Assignment'),
    
    # Arithmetic Operations 
    (r'SUM OF\b', 'Arithmetic Operation'),
    (r'DIFF OF\b', 'Arithmetic Operation'),
    (r'PRODUKT OF\b', 'Arithmetic Operation'),
    (r'QUOSHUNT OF\b', 'Arithmetic Operation'),
    (r'MOD OF\b', 'Arithmetic Operation'),
    (r'BIGGR OF\b', 'Arithmetic Operation'),
    (r'SMALLR OF\b', 'Arithmetic Operation'),
    
    # Boolean Operations
    (r'BOTH OF\b', 'Boolean Operation'),
    (r'EITHER OF\b', 'Boolean Operation'),
    (r'WON OF\b', 'Boolean Operation'),
    (r'NOT\b', 'Boolean Operation'),
    (r'ANY OF\b', 'Boolean Operation'),
    (r'ALL OF\b', 'Boolean Operation'),
    
    # Comparison Operations
    (r'BOTH SAEM\b', 'Comparison Operation'),
    (r'DIFFRINT\b', 'Comparison Operation'),
    
    # String Operations
    (r'SMOOSH\b', 'String Concatenation'),
    
    
    # Typecasting
    (r'IS NOW A\b', 'Typecasting Operation'),
    (r'MAEK \b', 'Typecasting Operation'),
    (r'A\b', 'Typecasting Operation'),
    
    # I/O Operations
    (r'VISIBLE\b', 'Output Keyword'),
    (r'\+', 'Output Separator'),
    (r'GIMMEH\b', 'Input Keyword'),
    
    # Conditionals 
    (r'O RLY\?', 'If-then Keyword'),
    (r'YA RLY\b', 'If-then Keyword'),
    (r'MEBBE\b', 'If-then Keyword'),
    (r'NO WAI\b', 'If-then Keyword'),
    (r'OIC\b', 'Exit Keyword'),
    
    # Switch-Case
    (r'WTF\?', 'Switch-Case Keyword'),
    (r'OMG\b', 'Switch-Case Keyword'),
    (r'OMGWTF\b', 'Switch-Case Keyword'),
    
    # Loops
    (r'IM IN YR\b', 'Loop Keyword'),
    (r'IM OUTTA YR\b', 'Loop Keyword'),
    (r'UPPIN\b', 'Loop Operation'),
    (r'NERFIN\b', 'Loop Operation'),
    (r'YR\b', 'Loop Variable Assignment'),
    (r'TIL\b', 'Loop Keyword'),
    (r'WILE\b', 'Loop Keyword'),
    
    # Functions
    (r'HOW IZ I\b', 'Function Keyword'),
    (r'IF U SAY SO\b', 'Function Keyword'),
    (r'FOUND YR\b', 'Return Keyword'),
    (r'GTFO\b', 'Return Keyword'),
    (r'I IZ\b', 'Function Call'),
    (r'MKAY\b', 'Function Call Delimiter'),
    
    # Literals
    (r'\"[^\"]*\"', 'YARN Literal'),
    (r'-?[0-9]+\.[0-9]+', 'NUMBAR Literal'),
    (r'-?[0-9]+', 'NUMBR Literal'),
    (r'(WIN|FAIL)', 'TROOF Literal'),
    (r'(NUMBR|NUMBAR|YARN|TROOF|NOOB)', 'Type Literal'),
    
    # Parameter Delimiter
    (r'AN\b', 'Parameter Delimiter'),
    
    # Else, Identifiers
    (r'[a-zA-Z][a-zA-Z0-9_]*', 'Variable Identifier'),
]
def showOutput():
    pass

def tokenizer(content):
   
    for filename, file_content in content.items():
        print(f"\n--- Tokenizing: {filename} ---")
        





def readFile():
    """
    Reads .lol file(s) from the given path.
    Returns a string if single file, or a dictionary of {filename: content} if directory.
    """

    path = input("Enter the LOLCODE file or directory path: ").strip()
    try:
        # Check if path exists
        if not os.path.exists(path):
            print(f"Error: Path '{path}' does not exist.")
            return None
        
        # Single file case
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
        
        # Directory case
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

def menu():
    print("-----------------------------------")
    print("LOLCODE Lexical Analyzer")
    print("-----------------------------------")
    print("[1] Read and Analyze LOLCODE File/Directory")
    print("[2] Exit")

def main():

    while True:
        menu()
        choice = input("Enter your choice: ")

        if choice == '1':
            content = readFile()
        elif choice == '2':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")            
    



main()
