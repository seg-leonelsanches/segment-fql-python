from segment_fql.lexer.token import Token
from segment_fql.lexer.token_type import TokenType

class Lexer:
    def __init__(self, text):
        self.MAXIMUM_INDENT_LENGTH = 100000 # bug catcher
        self.MAXIMUM_NUMBER_LENGTH = 100000
        self.MAXIMUM_STRING_LENGTH = 100000
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]
        self.reserved_keywords = {
            'true': Token(TokenType.Ident, 'true'),
            'false': Token(TokenType.Ident, 'false'),
            'null': Token(TokenType.Null, 'null'),
            'event': Token(TokenType.Ident, 'event'),
            'contains': Token(TokenType.Ident, 'contains'),
            'match': Token(TokenType.Ident, 'match'),
            'and': Token(TokenType.Logical, 'and'),
            'or': Token(TokenType.Logical, 'or')
        }

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

    def _is_terminator(self, char):
        return char is None or char.isspace() or char in ['(', ')', '[', ']', ',', '.', '"']

    def _is_identifier_character(self, char):
        return char.isalpha() or char.isdigit() or char in ['-', '\\', '_']

    def _lex_identifier(self, previous):
        result = ''
        char = previous
        while True:
            if char is None:
                break

            if char == '\\':
                self._advance()
                char = self.current_char
                if char is None:
                    raise Exception('Unexpected end of string')

                char = self.current_char

            result += char

            if len(result) > self.MAXIMUM_STRING_LENGTH:
                raise Exception('Unreasonable string length')

            if not self._is_identifier_character(char):
                break

            self._advance()
            char = self.current_char

        coming_up = self.current_char
        if coming_up is not None and not (self._is_terminator(coming_up) or coming_up in ['!', '=', '(', '.']):
            raise Exception(f'Expected termination character after identifier, got {coming_up}')

        result = result.strip().strip('.')

        if result in self.reserved_keywords:
            return self.reserved_keywords[result]

        return Token(TokenType.Ident, result)

    def _lex_number(self, previous):
        result = ''
        self._advance()
        coming_up = self.current_char
        is_decimal = False
        while coming_up is not None and (coming_up.isdigit() or coming_up == '.'):
            result += self.current_char
            self._advance()

            # Prevent multiple decimal points and stray decimal points
            if coming_up == '.':
                if self._is_terminator(self.current_char):
                    raise Exception('Unexpected terminator after decimal point')

                if is_decimal:
                    raise Exception('Multiple decimal points in one number')
                
                is_decimal = True

            # Prevent infinite loops
            if (len(result) > self.MAXIMUM_NUMBER_LENGTH):
                raise Exception('Unreasonable number length')
            
            coming_up = self.current_char

        return Token(TokenType.Number, previous + result)

    def _lex_operator_or_conditional(self, previous):
        if previous == '=':
            self._advance()
            return Token(TokenType.Operator, '=')
 
        if previous == '!':
            next_char = self.text[self.pos + 1]
            if next_char == '(':
                self._advance()
                return Token(TokenType.Operator, '!')
            elif next_char == '=':
                self._advance()
                self._advance()
                return Token(TokenType.Operator, '!=')

        if previous == '=':
            self._advance()
            return Token(TokenType.Operator, '=')

        if previous == '+':
            self._advance()
            return Token(TokenType.Operator, '+')

        if previous == '-':
            self._advance()
            return Token(TokenType.Operator, '-')

        if previous == '*':
            self._advance()
            return Token(TokenType.Operator, '*')

        if previous == '/':
            self._advance()
            return Token(TokenType.Operator, '/')

        return self._lex_identifier(previous)


    def _lex_string(self):
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

            if self.current_char.isdigit() or self.current_char in ['+', '-']:
                return self._lex_number(self.current_char)

            if self.current_char.isalpha() or self.current_char in ['!', '=', '>', '<', '\\', '_']:
                return self._lex_operator_or_conditional(self.current_char)

            if self.current_char == '.':
                self._advance()
                return Token(TokenType.Dot, '.')

            if self.current_char == ',':
                self._advance()
                return Token(TokenType.Comma, ',')

            if self.current_char == '[':
                self._advance()
                return Token(TokenType.BrackLeft, '[')

            if self.current_char == ']':
                self._advance()
                return Token(TokenType.BrackRight, ']')

            if self.current_char == '(':
                self._advance()
                return Token(TokenType.ParenLeft, '(')

            if self.current_char == ')':
                self._advance()
                return Token(TokenType.ParenRight, ')')

            if self.current_char == '"':
                return self._lex_string()

            if self.current_char.isalpha():
                return self._lex_identifier()

            self.error()

        return Token(TokenType.EOS, 'eos')

    def error(self):
        raise Exception('Invalid character')