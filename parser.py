from lark import Lark, Transformer, UnexpectedInput
import json

class SnippetTransformer(Transformer):
    """
    Transforms the parsed tree into a structured Python dictionary.
    """
    def snippet(self, items):
        metadata, codeblock = items
        return {**metadata, **codeblock}

    def metadata(self, items):
        return dict(items)

    def header(self, items):
        return ("name", items[0].strip())

    def prefix(self, items):
        return ("prefix", items[0].strip())

    def description(self, items):
        return ("description", items[0].strip())

    def codeblock(self, items):
        return {
            "language": items[0].strip(),
            "code": items[1].strip(),
            "placeholders": self.extract_placeholders(items[1].strip()),
        }

    def extract_placeholders(self, code):
        """
        Extracts placeholders in the format ${1:placeholder}.
        """
        import re
        placeholder_pattern = r"\$\{(\d+):([^}]+)\}"
        matches = re.finditer(placeholder_pattern, code)

        return [
            {"index": int(match.group(1)), "default": match.group(2)}
            for match in matches
        ]


def parse_snippets(snippet_text):
    """
    Parses the snippet text and returns a list of snippets as Python dictionaries.

    Args:
        snippet_text (str): The content of the `.snippet` file.

    Returns:
        list: A list of parsed snippets as structured dictionaries.
    """
    try:
        # Load the grammar from the grammar file
        with open("grammar/snippet_grammar.lark", "r") as grammar_file:
            snippet_parser = Lark(grammar_file.read(), parser="lalr", transformer=SnippetTransformer())

        # Parse the snippet text
        parsed_snippets = snippet_parser.parse(snippet_text)
        return parsed_snippets
    except UnexpectedInput as e:
        print("Failed to parse snippet file. Please check the syntax.")
        print(e)
        return None

if __name__ == "__main__":
    # Read the test snippet file
    with open("javascript.snippet", "r") as file:
        snippet_text = file.read()

    # Parse the snippet file
    parsed_snippets = parse_snippets(snippet_text)

    # Print the parsed output as JSON
    if parsed_snippets:
        print(json.dumps(parsed_snippets, indent=4))

