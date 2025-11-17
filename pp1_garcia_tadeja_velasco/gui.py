import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import os
from lexer_analyzer import tokenize
from syntax_analyzer import SyntaxAnalyzer

# color scheme
BG = "#0B1220"
PANEL = "#172232"
INNER = "#0F1A26"
ACCENT_PURPLE = "#9B63FF"
CLEAR_RED = "#880808"
TEXT = "#D6E6FF"

ctk.set_appearance_mode("dark") # modes : "dark", "light"

# main gui class
class LOLCodeInterpreterGUI:  
    def __init__(self): # default constructor
        self.root = ctk.CTk()
        self.root.title("LOCODE Interpreter")
        self.root.configure(fg_color=BG)
        self.root.geometry("1200x800")
        self.root.minsize(900, 600)

        self.current_file = None
        self.create_gui()
        self._configure_grid_weights()  # enable full resizing

    # create gui layout
    def create_gui(self):
        # title
        title = ctk.CTkLabel(self.root, text="LOLCODE Interpreter",
                             font=("Arial", 22, "bold"), text_color=ACCENT_PURPLE)
        title.grid(row=0, column=0, columnspan=3, pady=(12, 6), sticky="n")

        # left editor panel
        left_panel = ctk.CTkFrame(self.root, fg_color=PANEL, corner_radius=16)
        left_panel.grid(row=1, column=0, sticky="nsew", padx=(16, 8), pady=8)

        file_row = ctk.CTkFrame(left_panel, fg_color=PANEL) # file selection row
        file_row.pack(fill="x", padx=12, pady=(10, 6)) 

        self.filename_label = ctk.CTkLabel(file_row, text="(None)", font=("Arial", 12, "bold"), text_color=TEXT) # filename display
        self.filename_label.pack(side="left")

        # file browse button
        browse_btn = ctk.CTkButton(file_row, text="📁", width=36, height=28, fg_color="#2A3350", 
                                   hover=False, command=self.browse_file)
        browse_btn.pack(side="right")

        # text editor frame
        editor_frame = ctk.CTkFrame(left_panel, fg_color=INNER, corner_radius=12)
        editor_frame.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        # text editor label
        editor_label_frame = ctk.CTkFrame(editor_frame, fg_color=INNER)
        editor_label_frame.pack(fill="x", padx=6, pady=(8, 4))
        ctk.CTkLabel(editor_label_frame, text="Text Editor", font=("Arial", 13, "bold"),
                     text_color=TEXT).pack(side="left", anchor="w")

        # text editor textbox
        self.text_editor = ctk.CTkTextbox(editor_frame, wrap="none", font=("Courier New", 12),
                                          fg_color="#091218", text_color=TEXT)
        self.text_editor.pack(fill="both", expand=True, padx=8, pady=(0, 12))

        # mid lexemes panel
        lex_panel = ctk.CTkFrame(self.root, fg_color=PANEL, corner_radius=16)
        lex_panel.grid(row=1, column=1, sticky="nsew", padx=8, pady=8)

        lex_title_row = ctk.CTkFrame(lex_panel, fg_color=PANEL) # lexemes title row
        lex_title_row.pack(fill="x", padx=12, pady=(10, 6))
        ctk.CTkLabel(lex_title_row, text="LEXEMES", font=("Arial", 14, "bold"),
                     text_color=TEXT).pack(side="left")

        lex_inner = ctk.CTkFrame(lex_panel, fg_color=INNER, corner_radius=12) # lexemes inner frame
        lex_inner.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        headers = ctk.CTkFrame(lex_inner, fg_color=INNER) # lexemes headers
        headers.pack(fill="x", padx=8, pady=(6, 4))
        ctk.CTkLabel(headers, text="Lexeme", font=("Arial", 11, "bold"),
                     text_color=TEXT).pack(side="left", padx=(4, 12))
        ctk.CTkLabel(headers, text="Classification", font=("Arial", 11, "bold"),
                     text_color=TEXT).pack(side="right")

        # lexemes textbox
        self.lexemes_textbox = ctk.CTkTextbox(lex_inner, wrap="none", font=("Courier New", 11),
                                              fg_color="#08121a", text_color=TEXT)
        self.lexemes_textbox.pack(fill="both", expand=True, padx=8, pady=(0, 8))

        # right symbol table panel
        sym_panel = ctk.CTkFrame(self.root, fg_color=PANEL, corner_radius=16)
        sym_panel.grid(row=1, column=2, sticky="nsew", padx=(8, 16), pady=8)

        sym_title_row = ctk.CTkFrame(sym_panel, fg_color=PANEL) # symbol table title row
        sym_title_row.pack(fill="x", padx=12, pady=(10, 6))
        ctk.CTkLabel(sym_title_row, text="SYMBOL TABLE", font=("Arial", 14, "bold"),
                     text_color=TEXT).pack(side="left")

        sym_inner = ctk.CTkFrame(sym_panel, fg_color=INNER, corner_radius=12) # symbol table inner frame
        sym_inner.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        # symbol table headers
        sheaders = ctk.CTkFrame(sym_inner, fg_color=INNER)
        sheaders.pack(fill="x", padx=8, pady=(6, 4))
        ctk.CTkLabel(sheaders, text="Identifier", font=("Arial", 11, "bold"),
                     text_color=TEXT).pack(side="left", padx=(4, 12))
        ctk.CTkLabel(sheaders, text="Value", font=("Arial", 11, "bold"),
                     text_color=TEXT).pack(side="right")

        # symbol table textbox
        self.symbol_textbox = ctk.CTkTextbox(sym_inner, wrap="none", font=("Courier New", 11),
                                             fg_color="#08121a", text_color=TEXT)
        self.symbol_textbox.pack(fill="both", expand=True, padx=8, pady=(0, 8))

        # execute & clear buttons
        controls_frame = ctk.CTkFrame(self.root, fg_color=BG)
        controls_frame.grid(row=2, column=0, columnspan=3, sticky="ew", pady=(4, 6), padx=16)

        ctk.CTkButton(controls_frame, text="🗑️ Clear", width=110, fg_color=CLEAR_RED,
                      hover_color="#9E5B4B", command=self.clear_all).pack(side="left", padx=(2, 6))
        ctk.CTkButton(controls_frame, text="Execute", width=140, fg_color=ACCENT_PURPLE,
                      hover_color=ACCENT_PURPLE, command=self.execute_code).pack(side="right", padx=(6, 2))

        # bottom console panel
        console_frame = ctk.CTkFrame(self.root, fg_color=PANEL, corner_radius=14)
        console_frame.grid(row=3, column=0, columnspan=3, sticky="nsew", padx=16, pady=(6, 16))

        self.console_textbox = ctk.CTkTextbox(console_frame, height=140, wrap="word",
                                              font=("Courier New", 12), fg_color=INNER, text_color=TEXT)
        self.console_textbox.pack(fill="both", expand=True, padx=12, pady=12)

    # configure grid weights for resizing
    def _configure_grid_weights(self):
        self.root.grid_rowconfigure(0, weight=0)
        self.root.grid_rowconfigure(1, weight=10)
        self.root.grid_rowconfigure(2, weight=0)
        self.root.grid_rowconfigure(3, weight=3)
        self.root.grid_columnconfigure(0, weight=5)
        self.root.grid_columnconfigure(1, weight=3)
        self.root.grid_columnconfigure(2, weight=3)

    # file browsing function
    def browse_file(self):
        filename = filedialog.askopenfilename(title="Select LOL Code File",
                                              filetypes=(("LOL files", "*.lol"), ("Text files", "*.txt"),
                                                         ("All files", "*.*")))
        if filename:
            self.current_file = filename
            self.filename_label.configure(text=os.path.basename(filename))
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    content = f.read()
                self.text_editor.delete("1.0", "end")
                self.text_editor.insert("1.0", content)
                self.log_to_console(f"File loaded: {os.path.basename(filename)}\n")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {e}")

    # execute code function
    def execute_code(self):
        self.console_textbox.delete("1.0", "end")
        code = self.text_editor.get("1.0", "end-1c")
        if not code.strip():
            messagebox.showwarning("Warning", "No code to execute!")
            return

        self.log_to_console("Running Lexical Analysis...\n")
        try:
            tokens = tokenize(code)
            self.display_lexemes(tokens)
            self.log_to_console(f"Found {len(tokens)} tokens\n\n")
        except Exception as e:
            self.log_to_console(f"Lexer error: {e}\n")
            return

        self.log_to_console("Running Syntax Analysis & Execution...\n")
        try:
            parser_obj = SyntaxAnalyzer(tokens, log_function=self.log_to_console)
            output_text, symbol_table = parser_obj.parse_program()

            if output_text:
                self.display_console(output_text)
            self.display_symbol_table(symbol_table)
        except Exception as e:
            self.log_to_console(f"\nSyntax/Runtime error: {e}\n")

    # display lexemes in textbox
    def display_lexemes(self, tokens):
        self.lexemes_textbox.delete("1.0", "end")
        for token in tokens:
            self.lexemes_textbox.insert("end", f"{token.value:<25} {token.type}\n")

    # display symbol table in textbox
    def display_symbol_table(self, variables):
        self.symbol_textbox.delete("1.0", "end")
        if not variables:
            return
        for identifier, info in variables.items():
            val = info.get("value", "NOOB")
            t = info.get("type", "")
            self.symbol_textbox.insert("end", f"{identifier:<18} {val} ({t})\n")

    # display console output
    def display_console(self, text):
        self.console_textbox.delete("1.0", "end")
        self.console_textbox.insert("1.0", text)

    # log messages to console
    def log_to_console(self, msg):
        self.console_textbox.insert("end", msg)
        self.console_textbox.see("end")
        self.root.update_idletasks()

    # clear all fields
    def clear_all(self):
        self.text_editor.delete("1.0", "end")
        self.lexemes_textbox.delete("1.0", "end")
        self.symbol_textbox.delete("1.0", "end")
        self.console_textbox.delete("1.0", "end")
        self.filename_label.configure(text="(None)")
        self.current_file = None
        self.log_to_console("✓ All fields cleared\n")

    # run main loop
    def run(self):
        self.root.mainloop()

# entry point
if __name__ == "__main__":
    app = LOLCodeInterpreterGUI()
    app.run()
