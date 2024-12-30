class SnippetParsingError(Exception):
    """Base class for all snippet parsing errors."""
    pass

class SyntaxError(SnippetParsingError):
    """Raised when there is a syntax error in the snippet."""
    def __init__(self, file_path, line, column, unexpected, expected, context):
        self.file_path = file_path
        self.line = line
        self.column = column
        self.unexpected = unexpected
        self.expected = expected
        self.context = context
        super().__init__(self.__str__())

    def __str__(self):
        return (
            f"HELLOSyntax error in snippet file '{self.file_path}' at line {self.line}, column {self.column}.\n"
            f"Unexpected token: {self.unexpected}. Expected one of: {self.expected}.\n"
            f"Context: {self.context}"
        )

class UnexpectedCharactersError(SnippetParsingError):
    """Raised when unexpected characters are encountered."""
    def __init__(self, file_path, line, column, allowed, context):
        self.file_path = file_path
        self.line = line
        self.column = column
        self.allowed = allowed
        self.context = context
        super().__init__(self.__str__())

    def __str__(self):
        return (
            f"Unexpected characters in snippet file '{self.file_path}' at line {self.line}, column {self.column}.\n"
            f"Allowed tokens: {self.allowed}.\n"
            f"Context: {self.context}"
        )

class UnexpectedEOFError(SnippetParsingError):
    """Raised when the input ends unexpectedly."""
    def __init__(self, file_path, expected):
        self.file_path = file_path
        self.expected = expected
        super().__init__(self.__str__())

    def __str__(self):
        return (
            f"Unexpected EOF in snippet file '{self.file_path}'. Expected one of: {self.expected}."
        )

class GeneralParsingError(SnippetParsingError):
    """Raised for general parsing errors."""
    def __init__(self, file_path, message):
        self.file_path = file_path
        self.message = message
        super().__init__(self.__str__())

    def __str__(self):
        return f"Parsing error in snippet file '{self.file_path}': {self.message}"

class FileNotFoundError(SnippetParsingError):
    """Raised when the snippet file is not found."""
    def __init__(self, file_path):
        self.file_path = file_path
        super().__init__(self.__str__())

    def __str__(self):
        return f"File not found: '{self.file_path}'. Ensure the file exists."

