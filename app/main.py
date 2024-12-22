import sys

error_code = 0

class Token:
    def __init__(self, token_type, lexeme, literal=None):
        self.token_type = token_type
        self.lexeme = lexeme
        self.literal = literal

    def __str__(self):
        return f"{self.token_type} {self.lexeme} {self.literal if self.literal is not None else 'null'}"

def report_error(line_num, char):
    global error_code
    error_code = 65
    print(f"[line {line_num}] Error: Unexpected character: {char}", file=sys.stderr)

def scan_tokens(source):
    single_char_tokens = {
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
    }

    multi_char_tokens = {
        "==": "EQUAL_EQUAL",
        "!=": "BANG_EQUAL",
    }

    tokens = []
    i = 0

    while i < len(source):
        char = source[i]

        # check for multi char tokens
        if i + 1 < len(source):
            two_char_sequence = char + source[i + 1]
            if two_char_sequence in multi_char_tokens:
                tokens.append(Token(multi_char_tokens[two_char_sequence], two_char_sequence, None))
                i += 2  
                continue

        # check for single char tokens
        if char in single_char_tokens:
            tokens.append(Token(single_char_tokens[char], char, None))
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
