from lark import Lark, Transformer
import json

# Transformer to convert parsed tree into JSON
class SnippetTransformer(Transformer):
    def start(self, items):
        return items

    def snippet(self, items):
        # Combine snippet components into a dictionary
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

with open("grammar/snippet_grammar.lark", "r") as grammar_file:
    snippet_grammar = grammar_file.read()

# Create the parser
snippet_parser = Lark(snippet_grammar, parser="lalr", transformer=SnippetTransformer())

def test():
    with open("test.snippet", "r") as f:
        test_snippet = f.read()

    parsed = snippet_parser.parse(test_snippet)
    json_output = json.dumps(parsed, indent=4)
    print(json_output)  # Output the JSON-like dictionary

if __name__ == '__main__':
    test()


