from lark import Lark, Transformer, exceptions
from parser.exceptions import (
    SyntaxError,
    UnexpectedCharactersError,
    UnexpectedEOFError,
    GeneralParsingError,
    FileNotFoundError
)

import json

SUPPORTED_LANGUAGES = {"javascript", "python", "java", "c++", "c#", "go", "ruby",
                       "typescript", "elixir"}

# Transformer to convert parsed tree into JSON
class SnippetTransformer(Transformer):
    def start(self, items):
        if not items:
            raise ValueError("No items found in the snippet file.")

        language = items[0]
        snippets = items[1:]

        return {
            "language": self.validate_language(language),
            "snippets": snippets,
        }

    def LANGUAGE_HEADER(self, items):
        language = str(items).replace("<!", "").strip()
        return language

    def snippet(self, items):
        if len(items) != 3:
            raise ValueError(f"Snippet block does not have exactly 3 items: {items}")

        # Properly assign the values to prefix, description, and body
        prefix = items[0]
        description = items[1]
        body = items[2]

        return {
            "prefix": prefix,
            "description": description,
            "body": body,
        }

    def code(self, items):
        return str(items[0]).strip()

    def ESCAPED_STRING(self, items):
        return items

    def CODE_BODY(self, items):
        return "".join(items)

    def validate_language(self, language):
        """Validate that the language is in the supported languages list."""
        if language.lower().strip() not in SUPPORTED_LANGUAGES:
            raise ValueError(f"Unsupported language: {language}. Supported languages are: {', '.join(SUPPORTED_LANGUAGES)}")
        return language

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
        parsed = construct_vscode_json(parser.parse(snippet_text))
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
        raise GeneralParsingError(file_path, f"Unexpected error: {e}") from e

def construct_vscode_json(parsed_output):
    """Format parsed snippets into VSCode JSON format."""
    if not isinstance(parsed_output, dict):
        raise ValueError("Parsed output is not in the expected dictionary format.")
    
    # Initialize the VSCode snippets dictionary
    vscode_snippets = {}
    
    # Extract the language scope
    language = parsed_output.get("language", "global")  # Default to "global" if no language is provided
    vscode_snippets["scope"] = language
    vscode_snippets["snippets"] = {}

    # Iterate over all snippets in the parsed output
    for snippet in parsed_output.get("snippets", []):
        prefix = snippet.get("prefix", "").strip()
        description = snippet.get("description", "").strip()
        body = snippet.get("body", "").strip().split("\n")  # Split multi-line code into an array

        if not prefix or not body:
            raise ValueError(f"Invalid snippet data: {snippet}")

        # Add each snippet into the snippets dictionary
        vscode_snippets["snippets"][prefix] = {
            "prefix": prefix,
            "body": body,
            "description": description
        }

    return vscode_snippets

