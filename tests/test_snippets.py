import os
import json
from lark import Lark
from parser.snippet_parser import SnippetTransformer

# Load the grammar
with open("parser/snippet_grammar.lark", "r") as grammar_file:
    snippet_grammar = grammar_file.read()

# Create the parser
snippet_parser = Lark(snippet_grammar, parser="lalr", transformer=SnippetTransformer())

def parse_snippet_file(file_path):
    """Parse a snippet file and return the parsed JSON."""
    with open(file_path, "r") as f:
        snippet_text = f.read()
    return snippet_parser.parse(snippet_text)

def test_valid_snippets():
    """Test valid snippet files."""
    test_dir = "tests/snippets/valid_snippets"
    for file in os.listdir(test_dir):
        if file.endswith(".snippet"):
            print(f"Testing valid snippet: {file}")
            file_path = os.path.join(test_dir, file)
            try:
                result = parse_snippet_file(file_path)
                print(json.dumps(result, indent=4))
                print(f"✅ {file} passed\n")
            except Exception as e:
                print(f"❌ {file} failed with error: {e}\n")

def test_invalid_snippets():
    """Test invalid snippet files."""
    test_dir = "tests/snippets/invalid_snippets"
    for file in os.listdir(test_dir):
        if file.endswith(".snippet"):
            print(f"Testing invalid snippet: {file}")
            file_path = os.path.join(test_dir, file)
            try:
                result = parse_snippet_file(file_path)
                print(json.dumps(result, indent=4))
                print(f"❌ {file} passed unexpectedly\n")
            except Exception as e:
                print(f"✅ {file} failed as expected with error: {e}\n")

if __name__ == "__main__":
    print("Running tests for valid snippets...")
    test_valid_snippets()
   # print("Running tests for invalid snippets...")
   # test_invalid_snippets()

