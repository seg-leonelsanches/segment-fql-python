import pytest

from segment_fql.lexer import Lexer, Token, TokenType

class TestLexer:
    def test_lexer_true(self):
        lexer = Lexer('true')
        tokens = lexer.lex()
        assert tokens[0] == Token(TokenType.Ident, 'true')

    def test_lexer_string(self):
        lexer = Lexer('1 = "hello"')
        tokens = lexer.lex()
        assert tokens[0] == Token(TokenType.Number, '1')
        assert tokens[1] == Token(TokenType.Operator, '=')
        assert tokens[2] == Token(TokenType.String, 'hello')

    def test_lexer_whitespace(self):
        lexer = Lexer('1 = 2')
        tokens = lexer.lex()
        assert tokens[0] == Token(TokenType.Number, '1')
        assert tokens[1] == Token(TokenType.Operator, '=')
        assert tokens[2] == Token(TokenType.Number, '2')
        assert tokens[3] == Token(TokenType.EOS, 'eos')

    def test_lexer_path(self):
        lexer = Lexer('properties.product = "dfs"')
        tokens = lexer.lex()
        assert tokens[0] == Token(TokenType.Ident, 'properties')
        assert tokens[1] == Token(TokenType.Dot, '.')
        assert tokens[2] == Token(TokenType.Ident, 'product')
        assert tokens[3] == Token(TokenType.Operator, '=')
        assert tokens[4] == Token(TokenType.String, 'dfs')
        assert tokens[5] == Token(TokenType.EOS, 'eos')

    def test_lexer_not(self):
        lexer = Lexer('!(1 = "hello")')
        tokens = lexer.lex()
        assert tokens[0] == Token(TokenType.Operator, '!')
        assert tokens[1] == Token(TokenType.ParenLeft, '(')
        assert tokens[2] == Token(TokenType.Number, '1')
        assert tokens[3] == Token(TokenType.Operator, '=')
        assert tokens[4] == Token(TokenType.String, 'hello')
        assert tokens[5] == Token(TokenType.ParenRight, ')')
        assert tokens[6] == Token(TokenType.EOS, 'eos')

    def test_lexer_whitespace_event(self):
        lexer = Lexer('event = "Order Completed"')
        tokens = lexer.lex()
        assert tokens[0] == Token(TokenType.Ident, 'event')
        assert tokens[1] == Token(TokenType.Operator, '=')
        assert tokens[2] == Token(TokenType.String, 'Order Completed')
        assert tokens[3] == Token(TokenType.EOS, 'eos')

    def test_lexer_or(self):
        lexer = Lexer('event = "User Created" or event = "Product Account Created" or event = "User Status Changed"')
        tokens = lexer.lex()
        assert tokens[0] == Token(TokenType.Ident, 'event')
        assert tokens[1] == Token(TokenType.Operator, '=')
        assert tokens[2] == Token(TokenType.String, 'User Created')
        assert tokens[3] == Token(TokenType.Logical, 'or')
        assert tokens[4] == Token(TokenType.Ident, 'event')
        assert tokens[5] == Token(TokenType.Operator, '=')
        assert tokens[6] == Token(TokenType.String, 'Product Account Created')
        assert tokens[7] == Token(TokenType.Logical, 'or')
        assert tokens[8] == Token(TokenType.Ident, 'event')
        assert tokens[9] == Token(TokenType.Operator, '=')
        assert tokens[10] == Token(TokenType.String, 'User Status Changed')
        assert tokens[11] == Token(TokenType.EOS, 'eos')

    def test_lexer_or_2(self):
        lexer = Lexer('!(event = "Notification Event" or event = "Marketing Control" or traits.fgd_marketing_comms_status != null or event = "Verification Succeeded")')
        tokens = lexer.lex()
        assert tokens[0] == Token(TokenType.Operator, '!')
        assert tokens[1] == Token(TokenType.ParenLeft, '(')
        assert tokens[2] == Token(TokenType.Ident, 'event')
        assert tokens[3] == Token(TokenType.Operator, '=')
        assert tokens[4] == Token(TokenType.String, 'Notification Event')
        assert tokens[5] == Token(TokenType.Logical, 'or')
        assert tokens[6] == Token(TokenType.Ident, 'event')
        assert tokens[7] == Token(TokenType.Operator, '=')
        assert tokens[8] == Token(TokenType.String, 'Marketing Control')
        assert tokens[9] == Token(TokenType.Logical, 'or')
        assert tokens[10] == Token(TokenType.Ident, 'traits')
        assert tokens[11] == Token(TokenType.Dot, '.')
        assert tokens[12] == Token(TokenType.Ident, 'fgd_marketing_comms_status')
        assert tokens[13] == Token(TokenType.Operator, '!=')
        assert tokens[14] == Token(TokenType.Null, 'null')
        assert tokens[15] == Token(TokenType.Logical, 'or')
        assert tokens[16] == Token(TokenType.Ident, 'event')
        assert tokens[17] == Token(TokenType.Operator, '=')
        assert tokens[18] == Token(TokenType.String, 'Verification Succeeded')
        assert tokens[19] == Token(TokenType.ParenRight, ')')
        

