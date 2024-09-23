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
        assert len(grandchild.children[0]) > 0
        assert grandchild.children[0].value == True
        

    def test_parser_event(self):
        lexer = Lexer('event.name = "Order Completed"')
        tokens = lexer.lex()
        parser = Parser(lexer, tokens)
        node = parser.parse()
        assert node.type == ASTType.ROOT
        assert node.children[0].type == ASTType.STATEMENT

    def test_parser_string(self):
        lexer = Lexer('1 + "hello world" + 2')
        tokens = lexer.lex()
        parser = Parser(lexer, tokens)
        node = parser._statement()
        assert node.type == ASTType.STATEMENT
        assert node.children[0].type == ASTType.EXPR
        assert node.children[0].children[0].value == 1
        assert node.children[1].value == '+'
        assert node.children[2].type == ASTType.EXPR
        assert node.children[2].children[0].value == 'hello world'
        assert node.children[3].value == '+'
        assert node.children[4].type == ASTType.EXPR
        assert node.children[4].children[0].value == 2

    def test_parser_string(self):
        lexer = Lexer('1 + "hello world" + 2 + "foo"')
        tokens = lexer.lex()
        parser = Parser(lexer, tokens)
        node = parser._statement()
        assert node.type == ASTType.STATEMENT
        assert node.children[0].type == ASTType.EXPR
        assert node.children[0].children[0].value == 1
        assert node.children