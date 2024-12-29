import sys

error_code = 0

class Token:
    def __init__(self, token_type, lexeme, literal=None):
        self.token_type = token_type
        self.lexeme = lexeme
        self.literal = literal

    def __str__(self):
        return f"{self.token_type} {self.lexeme} {self.literal if self.literal is not None else 'null'}"

def report_error(line_num, char=None, message=None):
    global error_code
    error_code = 65

    if message:
        print(f"[line {line_num}] Error: {message}", file=sys.stderr)
    elif char:
        print(f"[line {line_num}] Error: Unexpected character: {char}", file=sys.stderr)

def scan_tokens(source):
    token_types = {
        '(': "LEFT_PAREN",
        ')': "RIGHT_PAREN",
        '{': "LEFT_BRACE",
        '}': "RIGHT_BRACE",
        '*': "STAR",
        '.': "DOT",
        ',': "COMMA",
        '+': "PLUS",
        '-': "MINUS",
        ';': "SEMICOLON",
        '!': "BANG",
        '=': "EQUAL",
        '<': "LESS",
        '>': "GREATER",
        '/': "SLASH",

        "==": "EQUAL_EQUAL",
        "!=": "BANG_EQUAL",
        "<=": "LESS_EQUAL",
        ">=": "GREATER_EQUAL",
        "//": "COMMENT",

    }


    tokens = []
    i = 0
    line = 1

    while i < len(source):
        char = source[i]

        if char == '\n':
            line += 1

        # check for multi char tokens
        elif i + 1 < len(source):
            two_char_sequence = char + source[i + 1]
            if two_char_sequence in token_types:
                if token_types[two_char_sequence] == "COMMENT":
                    # skip the rest of the comment
                    while i < len(source) and source[i] != "\n":
                        i += 1
                    continue
                else:
                    tokens.append(Token(token_types[two_char_sequence], two_char_sequence, None))

                # skip the second idx for multi char token
                i += 2
                continue
            else:
                pass

        # string literals
        if char == '"':
            start = i + 1
            while i + 1 < len(source) and source[i + 1] != '"':
                if source[i + 1] == '\n':
                    line += 1
                i += 1

            if i + 1 >= len(source):  
                report_error(line, message="Unterminated string.")
                break

            # get string contents
            string_value = source[start:i + 1]
            tokens.append(Token("STRING", '"' + string_value + '"', string_value))
            i += 2  
            continue
        
        # number literals
        elif char.isdigit():
            start = i
            while i + 1 < len(source) and source[i + 1].isdigit():
                i += 1

            # fraction 
            if i + 1 < len(source) and source[i + 1] == '.' and i + 2 < len(source) and source[i + 2].isdigit():
                i += 1  # skip .
                while i + 1 < len(source) and source[i + 1].isdigit():
                    i += 1

            number = source[start:i + 1]
            tokens.append(Token("NUMBER", number, float(number)))
        

        # check for single char tokens
        elif char in token_types:
            tokens.append(Token(token_types[char], char, None))
        elif char.isspace():
            pass  
        else:
            # report invalid token
            line_num = source.count("\n", 0, i) + 1
            report_error(line_num, char)

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
