import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import tkinter.font as tkfont

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return f'Token({self.type}, {self.value})'

class Scanner:
    def __init__(self):
        self.keywords = {
            'if', 'else', 'while', 'for', 'int', 
            'float', 'string', 'return', 'void'
        }
        self.operators = {
            '+', '-', '*', '/', '=', '==', '!=', 
            '<', '>', '<=', '>=', '(', ')', '{', 
            '}', ';', ','
        }

    def is_digit(self, char):
        return char.isdigit()

    def is_letter(self, char):
        return char.isalpha()

    def is_whitespace(self, char):
        return char.isspace()

    def scan(self, source_code):
        tokens = []
        position = 0
        
        while position < len(source_code):
            char = source_code[position]

            if self.is_whitespace(char):
                position += 1
                continue

            if self.is_digit(char):
                number = ''
                while position < len(source_code) and self.is_digit(source_code[position]):
                    number += source_code[position]
                    position += 1
                tokens.append(Token('NUMBER', number))
                continue

            if self.is_letter(char):
                identifier = ''
                while position < len(source_code) and (self.is_letter(source_code[position]) or 
                      self.is_digit(source_code[position])):
                    identifier += source_code[position]
                    position += 1
                
                if identifier in self.keywords:
                    tokens.append(Token('KEYWORD', identifier))
                else:
                    tokens.append(Token('IDENTIFIER', identifier))
                continue

            if char in self.operators:
                if position + 1 < len(source_code):
                    double_op = char + source_code[position + 1]
                    if double_op in self.operators:
                        tokens.append(Token('OPERATOR', double_op))
                        position += 2
                        continue
                
                tokens.append(Token('OPERATOR', char))
                position += 1
                continue

            tokens.append(Token('UNKNOWN', char))
            position += 1

        return tokens

class CompilerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Compiler - Scanner Phase")
        self.root.geometry("1000x600")
        self.scanner = Scanner()
        
        # Configure the grid
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        
        # Style configuration
        style = ttk.Style()
        style.configure('TButton', padding=5)
        style.configure('TFrame', padding=5)
        
        # Source code frame
        self.source_frame = ttk.LabelFrame(root, text="Source Code", padding="5")
        self.source_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # Source code text area
        self.source_text = scrolledtext.ScrolledText(self.source_frame, wrap=tk.WORD, width=40, height=20)
        self.source_text.pack(fill=tk.BOTH, expand=True)
        
        # Analyze button
        self.analyze_button = ttk.Button(self.source_frame, text="Analyze", command=self.analyze_code)
        self.analyze_button.pack(pady=5)
        
        # Token output frame
        self.token_frame = ttk.LabelFrame(root, text="Tokens", padding="5")
        self.token_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        
        # Token output text area
        self.token_text = scrolledtext.ScrolledText(self.token_frame, wrap=tk.WORD, width=40, height=20)
        self.token_text.pack(fill=tk.BOTH, expand=True)
        
        # Configure monospace font
        self.code_font = tkfont.Font(family="Courier", size=10)
        self.source_text.configure(font=self.code_font)
        self.token_text.configure(font=self.code_font)

    def analyze_code(self):
        # Clear previous output
        self.token_text.delete(1.0, tk.END)
        
        # Get source code and analyze
        source_code = self.source_text.get(1.0, tk.END)
        tokens = self.scanner.scan(source_code)
        
        # Display tokens
        self.token_text.insert(tk.END, "Tokens found:\n")
        self.token_text.insert(tk.END, "-" * 40 + "\n")
        for token in tokens:
            self.token_text.insert(tk.END, f"{token}\n")

def main():
    root = tk.Tk()
    app = CompilerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()