import pytest

from segment_fql.lexer import Lexer
from segment_fql.parser import Parser, ASTNode, ASTType

class TestParser:
    def test_parser(self):
        lexer = Lexer('true')
        tokens = lexer.lex()
        parser = Parser(lexer, tokens)
        node = parser.parse()
        assert node.type == ASTType.ROOT
        assert node.children[0].type == ASTType.STATEMENT
        child = node.children[0]
        assert len(child.children) == 1
        grandchild = child.children[0]
        assert grandchild.type == ASTType.EXPR
        assert len(grandchild.children) > 0
        greatgrandchild = grandchild.children[0]
        assert len(greatgrandchild.children) > 0
        assert greatgrandchild.children[0].value == 'true'
        

    def test_parser_event(self):
        lexer = Lexer('event = "Order Completed"')
        tokens = lexer.lex()
        parser = Parser(lexer, tokens)
        node = parser.parse()
        assert node.type == ASTType.ROOT
        assert len(node.children) == 1
        statement = node.children[0]
        assert statement.type == ASTType.STATEMENT
        assert len(statement.children) == 1
        conditional = statement.children[0]
        assert conditional.type == ASTType.CONDITIONAL
        assert len(conditional.children) == 3
        assert conditional.children[0].value == 'event'
        assert conditional.children[1].value == '='
        assert conditional.children[2].value == 'Order Completed'
