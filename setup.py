from setuptools import setup, find_packages

setup(
    name="snippet-parser",
    version="1.0.0",
    description="A universal snippet parser for various code editors",
    author="Your Name",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "lark-parser>=0.12.0"
    ],
    package_data={
        "parser": ["snippet_grammar.lark"],  # Include grammar file
    },
    entry_points={
        "console_scripts": [
            "snippet-parser=parser.snippet_parser:main",
        ],
    },
)

