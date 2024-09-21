from segment_fql.token import Token
from segment_fql.token_type import TokenType

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def lex(self):
        tokens = []
        while True:
            token = self._get_next_token()
            tokens.append(token)
            if token.type == TokenType.EOS:
                break

        return tokens

    def _advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def _skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self._advance()

    def _integer(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self._advance()
        return int(result)

    def _lexString(self):
        self._advance()
        result = ''
        while self.current_char is not None and self.current_char != '"':
            result += self.current_char
            self._advance()
        self._advance()
        return Token(TokenType.String, result)

    def _get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self._skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(TokenType.Number, self._integer())

            if self.current_char == '=':
                self._advance()
                return Token(TokenType.Operator, '=')

            if self.current_char == '+':
                self._advance()
                return Token(TokenType.Operator, '+')

            if self.current_char == '-':
                self._advance()
                return Token(TokenType.Operator, '-')

            if self.current_char == '*':
                self._advance()
                return Token(TokenType.Operator, '*')

            if self.current_char == '/':
                self._advance()
                return Token(TokenType.Operator, '/')

            if self.current_char == '(':
                self._advance()
                return Token(TokenType.ParenLeft, '(')

            if self.current_char == ')':
                self._advance()
                return Token(TokenType.ParenRight, ')')

            if self.current_char == '"':
                return self._lexString()

            self.error()

        return Token(TokenType.EOS, None)

    def error(self):
        raise Exception('Invalid character')