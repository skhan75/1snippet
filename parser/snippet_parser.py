from lark import Lark, Transformer, exceptions
from parser.exceptions import (
    SyntaxError,
    UnexpectedCharactersError,
    UnexpectedEOFError,
    GeneralParsingError,
    FileNotFoundError
)

import json

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
    snippet_text = ""  # Ensure snippet_text is always defined
    try:
        with open(file_path, "r") as f:
            snippet_text = f.read()
        parsed = parser.parse(snippet_text)
        return json.dumps(parsed, indent=4)

    except exceptions.UnexpectedToken as e:
        unexpected = getattr(e, 'token', 'Unknown')
        expected = ", ".join(e.expected) if hasattr(e, 'expected') else 'Unknown'
        context = e.get_context(snippet_text) if hasattr(e, 'get_context') else 'Unknown context'
        raise SyntaxError(
            file_path=file_path,
            line=e.line,
            column=e.column,
            unexpected=unexpected,
            expected=expected,
            context=context
        ) from e

    except exceptions.UnexpectedCharacters as e:
        context = e.get_context(snippet_text) if hasattr(e, 'get_context') else 'Unknown context'
        raise UnexpectedCharactersError(
            file_path=file_path,
            line=e.line,
            column=e.column,
            allowed=e.allowed,
            context=context
        ) from e

    except exceptions.UnexpectedEOF as e:
        expected = ", ".join(e.expected) if hasattr(e, 'expected') else 'Unknown'
        raise UnexpectedEOFError(
            file_path=file_path,
            expected=expected
        ) from e

    except exceptions.LarkError as e:
        raise GeneralParsingError(file_path, str(e)) from e

    except FileNotFoundError as e:
        raise FileNotFoundError(file_path) from e

    except Exception as e:
        raise GeneralParsingError(file_path, str(e)) from e

#def parse_snippet_file(file_path, grammar_path):
#    """Parse a snippet file and return the JSON output."""
#    parser = create_parser(grammar_path)
#    snippet_text = ""  # Ensure snippet_text is always defined
#    try:
#        with open(file_path, "r") as f:
#            snippet_text = f.read()
#        parsed = parser.parse(snippet_text)
#        return json.dumps(parsed, indent=4)
#    except Exception as e:
#        print("Exceptions>>>", e)
#        raise e
