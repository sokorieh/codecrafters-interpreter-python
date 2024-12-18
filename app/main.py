import sys
import re

def scan_tokens(source):
    if not source.strip():
        return [Token("EOF", "null")]

class Token:
    def __init__(self, token_type, lexeme, literal=None):
        self.token_type = token_type
        self.lexeme = lexeme
        self.literal = literal

    def __str__(self):
        return f"{self.token_type} {self.literal}"


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!", file=sys.stderr)

    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    if command != "tokenize":
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)

    with open(filename) as file:
        file_contents = file.read()

    if file_contents:
        raise NotImplementedError("Scanner not implemented")
    
    # print out all the tokens
    else:
        source = ""  
        tokens = scan_tokens(source)
        for token in tokens:
            print(token)


if __name__ == "__main__":
    main()
