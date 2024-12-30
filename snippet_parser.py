import re

class SnippetParser:
    """
    A parser for `.snippet` files that validates the format,
    extracts metadata, and outputs structured data.
    """

    def parse_snippets(self, snippet_text):
        """
        Parses the entire snippet text containing one or more snippets.

        Args:
            snippet_text (str): The text content of the `.snippet` file.

        Returns:
            list: A list of parsed snippets in structured format.
        """
        snippets = snippet_text.strip().split("\n\n")
        parsed_snippets = []

        for i,snippet in enumerate(snippets):
            #print(f"Processing snippet {i + 1}:\n{snippet}\n{'-' * 40}")
            parsed_snippets.append(self.__parse_single_snippet(snippet))

        return parsed_snippets


    def __parse_single_snippet(self, snippet_text):
        """
        Parses a single snippet block.

        Args:
            snippet_text (str): The text of a single snippet.

        Returns:
            dict: Parsed snippet with metadata and code.
        """

        # Match metadata 'prefix' and 'description'
        metadata_pattern = r"^(#\s*(.+))\nprefix:\s*(.+)\ndescription:\s*(.+)"
        metadata_match = re.search(metadata_pattern, snippet_text, re.MULTILINE)

        if not metadata_match:
            #print(f"Metadata not matched for snippet:\n{snippet_text}\n{'-' * 40}")
            raise ValueError(f"Invalid snippet format:\n{snippet_text}")

        # Extract metadata
        name = metadata_match.group(2).strip()
        prefix = metadata_match.group(3).strip()
        description = metadata_match.group(4).strip()

        # Match code block
        #code_pattern = r"```(\w+)\n([\s\S]+?)```"
        code_pattern = r"```(\w+)\n([\s\S]+?)```"

        code_match = re.search(code_pattern, snippet_text, re.MULTILINE)

        if not code_match:
            #print(f"Code block not matched for snippet:\n{snippet_text}\n{'-' * 40}")
            raise ValueError(f"Missing or invalid code block in snippet:\n{snippet_text}")

        language = code_match.group(1).strip()
        code = code_match.group(2).strip()

        # Extract placeholders
        placeholders = self._extract_placeholders(code)

        return {
            "name": name,
            "prefix": prefix,
            "description": description,
            "language": language,
            "code": code,
            "placeholders": placeholders,
        }

    def _extract_placeholders(self, code):
        """
        Extracts placeholders from the code.

        Args:
            code (str): The code block with placeholders.

        Returns:
            list: A list of placeholders with indices and defaults.
        """
        placeholder_pattern = r"\$\{(\d+):([^}]+)\}"
        matches = re.finditer(placeholder_pattern, code)

        placeholders = [
            {"index": int(match.group(1)), "default": match.group(2)}
            for match in matches
        ]

        return placeholders


