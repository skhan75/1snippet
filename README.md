# Snippet Parser

![Development Status](https://img.shields.io/badge/status-in%20progress-orange)

A universal snippet parser that allows you to define code snippets in a consistent format and converts them into a format suitable for IDEs like Visual Studio Code, Neovim, Sublime Text, and others.

This parser simplifies the process of writing and managing snippets by using a human-readable grammar and generating language-specific JSON files that can be directly used in IDEs.

## 🚧 Development in Progress

Its my first (Noob) attempt at building something with language grammar and parsers. It is currently under active development, and the parser is being tested. Features are being added, and the parser is being tested extensively, so bear with me. Please expect changes and improvements in upcoming versions. Feedback and contributions are always welcome!

## Why Are We Building This?

Managing and sharing code snippets across different IDEs and editors can be a cumbersome task. Different editors expect snippets in their own specific formats, leading to duplicate effort, reduced productivity, and inconsistency in snippet usage. 

The **Snippet Parser** solves this problem by introducing:
- **A single source of truth**: Write snippets once using a simple and flexible grammar.
- **Cross-IDE compatibility**: Generate editor-specific snippet files for Visual Studio Code, Neovim, Sublime Text, and other IDEs from the same source.
- **Enhanced organization**: Keep your snippets structured and validated to avoid missing fields or incorrect syntax.
- **Time-Saving**: Write once, use everywhere! No need to manually duplicate or translate snippets for each editor.

## Features

- **Supports Multiple Languages**: Parse snippets for supported languages like JavaScript, Python, Java, C++, etc.
- **Extensible Grammar**: Define your snippets using a simple, flexible grammar.
- **Error Handling**: Comprehensive error handling with detailed messages for:
  - Missing fields
  - Malformed brackets
  - Unsupported languages
  - Incomplete or invalid snippets
- **VSCODE-Compatible Output**: Converts parsed snippets into JSON format directly compatible with Visual Studio Code.
- **Validation**: Ensures snippets adhere to supported language and format.

---

## Supported Languages

- JavaScript
- Python
- Java
- C++
- C#
- Go
- Ruby
- TypeScript
- Elixir

---

## Grammar Definition

Snippets are defined in a `.snippet` file using the following format:

```plaintext
<!language
  (
    "prefix",
    "description",
    ```code body```
  )
  (
    "prefix",
    "description",
    ```code body```
  )
>
```

## Example Snippet 
```plaintext 
<!javascript
  (
    "log",
    "Logs a Message to the console",
    ```console.log("Hello world")```
  )
  (
    "logerr",
    "Logs an Error Message to the console",
    ```console.error("This is an Error")```
  )
  (
    "trycatch",
    "Creates a basic try catch block",
    ```
    try {
        ${1:// code here}
    } catch (${2:error}) {
        console.error(${2:error});
    }
    ```
  )
  (
    "function",
    "Creates a JavaScript function",
    ```
    function ${1:functionName}(${2:args}) {
      ${3:// function body here}
    }
    ```
  )
>
```

## Installation

### Step 1. Clone the Repository
```bash
git clone https://github.com/your-repo/snippet-parser.git
cd snippet-parser
```

### Step 2. Create and Activate a Virtual Environment
```bash
python3 -m venv env
source env/bin/activate  # On Linux/Mac
env\Scripts\activate  # On Windows
```

### Step 3: Install the Package
Run the following command to install the package:
```bash
pip install .
```

Alternatively, for development mode:
```bash
pip install -e .
```

## Usage 

### Parsing a Snippet File 
Run the following command to parse a `.snippet` file and generate a JSON output
```bash
snippet-parser path/to/snippet/file.snippet
```

### Sample Output 
```JSON
{
  "scope": "javascript",
  "snippets": {
    "log": {
      "prefix": "log",
      "body": ["console.log(\"Hello world\")"],
      "description": "Logs a Message to the console"
    }
  }
}
```
