import sys

class Token:
    def __init__(self, token_type, lexeme, literal=None):
        self.token_type = token_type
        self.lexeme = lexeme
        self.literal = literal

    def __str__(self):
        return f"{self.token_type} {self.lexeme} {self.literal if self.literal is not None else 'null'}"


def scan_tokens(source):
    tokens = []
    for char in source:
        if char == '(':
            tokens.append(Token("LEFT_PAREN", "(", None))
        elif char == ')':
            tokens.append(Token("RIGHT_PAREN", ")", None))
    
    tokens.append(Token("EOF", "", None))  
    return tokens

def main():
    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    if command != "tokenize":
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)

    try:
        with open(filename) as file:
            file_contents = file.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found", file=sys.stderr)
        exit(1)

    tokens = scan_tokens(file_contents)
    for token in tokens:
        print(token)

if __name__ == "__main__":
    main()
