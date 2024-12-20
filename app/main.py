import sys
error_code = 0

class Token:
    def __init__(self, token_type, lexeme, literal=None):
        self.token_type = token_type
        self.lexeme = lexeme
        self.literal = literal

    def __str__(self):
        return f"{self.token_type} {self.lexeme} {self.literal if self.literal is not None else 'null'}"


def scan_tokens(source):
    global error_code
    tokens = []
    i = 0

    while i < len(source):
        char = source[i]

        if char == '(':
            tokens.append(Token("LEFT_PAREN", "(", None))
        elif char == ')':
            tokens.append(Token("RIGHT_PAREN", ")", None))

        elif char == '{':
            tokens.append(Token("LEFT_BRACE", "{", None))
        elif char == '}':
            tokens.append(Token("RIGHT_BRACE", "}", None))

        elif char == '*':
            tokens.append(Token("STAR", "*", None))
        elif char == '.':
            tokens.append(Token("DOT", ".", None))
        elif char == ',':
            tokens.append(Token("COMMA", ",", None))
        elif char == '+':
            tokens.append(Token("PLUS", "+", None))
        elif char == '-':
            tokens.append(Token("MINUS", "-", None))
        elif char == ';':
            tokens.append(Token("SEMICOLON", ";", None))

        elif char == '=':

            # check if next char is also = 
            if i + 1 < len(source) and source[i + 1] == '=':
                tokens.append(Token("EQUAL_EQUAL", "==", None))

                # skip the 2nd =
                i += 1
            else:
                tokens.append(Token("EQUAL", "=", None))
        
        # handle invalid tokens
        else:
            error_code = 65
            line_num = source.count("\n", 0, source.find(char)) + 1

            print(
                "[line %s] Error: Unexpected character: %s" % (line_num, char),
                file=sys.stderr
            )
        i += 1
        
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

    exit(error_code)

if __name__ == "__main__":
    main()
