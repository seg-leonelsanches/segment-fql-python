# segment-fql-python

Segment FQL Language Tools for Python.

## Motivation

This project implements a Python library for working with [Segment's FQL](https://segment.com/docs/api/public-api/fql/) (Filter Query Language) queries. The library provides: 

- A lexer, which gets a FQL query string and returns a list of tokens;
- A parser, which given a list of tokens, returns an abstract syntax tree (AST).

This library is useful for working with FQL queries in Python, for example, to parse and validate queries, or to generate queries programmatically.

## Usage

### Lexer

The lexer class is implemented in the `segment_fql.lexer` module. The class asks for a string in the constructor, which it corresponds to the FQL query. It provides a single method, `lex`, which returns a list of tokens based on this string.

```python
from segment_fql.lexer import Lexer

lexer = Lexer('event = "page" and properties.url = "https://segment.com"')
tokens = lexer.lex()
print(tokens) # Output: [
              #     Token(ident, event), 
              #     Token(operator, =), 
              #     Token(string, page), 
              #     Token(logical, and), 
              #     Token(ident, properties), 
              #     Token(dot, .), 
              #     Token(ident, url), 
              #     Token(operator, =), 
              #     Token(string, https://segment.com),
              #     Token(eos, eos)
              # ]
```

Token types:

- `ident`: Identifier (e.g., `event`, `properties`, `url`);
- `operator`: Operator (e.g., `=`, `>`, `<`);
- `logical`: Logical operator (e.g., `and`, `or`);
- `string`: String value (e.g., `"page"`, `"https://segment.com"`);
- `dot`: Dot operator (`.`);
- `eos`: End of string.

### Parser

The parser class is implemented in the `segment_fql.parser` module. The class asks for a list of tokens in the constructor, which it corresponds to the FQL query. It provides a single method, `parse`, which returns an abstract syntax tree (AST) based on this list of tokens.

```python
from segment_fql.lexer import Lexer
from segment_fql.parser import Parser

lexer = Lexer('event = "page" and properties.url = "https://segment.com"')
tokens = lexer.lex()
parser = Parser(tokens)
ast = parser.parse()
print(ast) # Output:
           # <root (Children: [
           #     <statement (Children: [
           #         <conditional (Children: [
           #             Token(ident, event), 
           #             Token(operator, =), 
           #             Token(string, page)
           #         ])>, 
           #         Token(logical, and), 
           #         <statement (Children: [
           #             <conditional (Children: [
           #                 <path (Children: [
           #                     Token(ident, properties), 
           #                     Token(dot, .), 
           #                     Token(ident, url)
           #                 ])>, 
           #                 Token(operator, =), 
           #                 Token(string, https://segment.com)
           #             ])>
           #         ])>
           #     ])>
           # ])>
```

AST Node Types:

- `root`: Root node. It contains 1 or more `statement` nodes as children;
- `statement`: Statement node. It contains 1 or more AST nodes and/or tokens as children. Tokens come from the Lexer, and they never have children;
- `conditional`: Conditional node. It contains 3 children: in general, an identifier, an operator, and a string (value);
- `path`: Path node. It contains N children, with the minimum of 3: in general even indexes are identifiers, and odd indexes are dots.