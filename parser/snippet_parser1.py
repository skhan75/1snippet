from lark import Lark, Transformer
import json
import os

# Transformer to convert parsed tree into JSON
class SnippetTransformer(Transformer):
    def start(self, items):
        return items

    def snippet(self, items):
        return {
            "prefix": items[0],
            "title": items[1],
            "description": items[2],
            "body": items[3]["code"].strip(),
            "language": items[3]["language"]
        }

    def prefix(self, items):
        return str(items[0])[1:-1]

    def title(self, items):
        return str(items[0])[1:-1]

    def description(self, items):
        return str(items[0])[1:-1]

    def code(self, items):
        language = str(items[0])
        body = str(items[1])
        return {"language": language, "code": body}

    def CODE_BODY(self, items):
        return "".join(items)


def load_grammar(grammar_path):
    """Load the Lark grammar from a file."""
    with open(grammar_path, "r") as grammar_file:
        return grammar_file.read()


def create_parser(grammar_path):
    """Create and return a Lark parser using the provided grammar path."""
    snippet_grammar = load_grammar(grammar_path)
    return Lark(snippet_grammar, parser="lalr", transformer=SnippetTransformer())


def parse_snippet_file(file_path, grammar_path):
    """Parse a snippet file and return the JSON output."""
    parser = create_parser(grammar_path)
    with open(file_path, "r") as f:
        snippet_text = f.read()
    parsed = parser.parse(snippet_text)
    return json.dumps(parsed, indent=4)


# Main script for standalone testing
if __name__ == "__main__":
    grammar_path = os.path.join(os.path.dirname(__file__), "snippet_grammar.lark")
    snippet_file = os.path.join(os.getcwd(), "test.snippet")
    
    try:
        output = parse_snippet_file(snippet_file, grammar_path)
        print(output)
    except Exception as e:
        print(f"Error parsing snippet file: {e}")

