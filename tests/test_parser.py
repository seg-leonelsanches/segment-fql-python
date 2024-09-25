import pytest

from segment_fql.lexer import Lexer
from segment_fql.parser import Parser, ASTNode, ASTType

class TestParser:
    def test_parser(self):
        lexer = Lexer('true')
        tokens = lexer.lex()
        parser = Parser(tokens)
        node = parser.parse()
        assert node.type == ASTType.ROOT
        assert node.children[0].type == ASTType.STATEMENT
        child = node.children[0]
        assert len(child.children) == 1
        grandchild = child.children[0]
        assert grandchild.type == ASTType.EXPR
        assert len(grandchild.children) > 0
        greatgrandchild = grandchild.children[0]
        assert greatgrandchild.value == 'true'
        

    def test_parser_event(self):
        lexer = Lexer('event = "Order Completed"')
        tokens = lexer.lex()
        parser = Parser(tokens)
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


    def test_parser_path(self):
        lexer = Lexer('properties.product = "dfs"')
        tokens = lexer.lex()
        parser = Parser(tokens)
        node = parser.parse()
        assert node.type == ASTType.ROOT
        assert len(node.children) == 1
        statement = node.children[0]
        assert statement.type == ASTType.STATEMENT
        assert len(statement.children) == 1
        conditional = statement.children[0]
        assert conditional.type == ASTType.CONDITIONAL
        assert len(conditional.children) == 3
        first_conditional_child = conditional.children[0]
        assert first_conditional_child.type == ASTType.PATH
        assert len(first_conditional_child.children) == 3
        assert first_conditional_child.children[0].value == 'properties'
        assert first_conditional_child.children[1].value == '.'
        assert first_conditional_child.children[2].value == 'product'
        assert conditional.children[1].value == '='
        assert conditional.children[2].value == 'dfs'

    def test_parser_or(self):
        lexer = Lexer('!(event = "User Created" or event = "Product Account Created" or event = "User Status Changed")')
        tokens = lexer.lex()
        parser = Parser(tokens)
        node = parser.parse()
        assert node.type == ASTType.ROOT
        assert len(node.children) == 1
        statement = node.children[0]
        assert statement.type == ASTType.STATEMENT
        assert len(statement.children) == 1
        not_node = statement.children[0]
        assert not_node.type == ASTType.NOT
        assert len(not_node.children) == 1
        grouping = not_node.children[0]
        assert grouping.type == ASTType.GROUPING
        assert len(grouping.children) == 1
        statement = grouping.children[0]
        assert statement.type == ASTType.STATEMENT
        assert len(statement.children) == 3
        first_conditional = statement.children[0]
        assert first_conditional.children[0].value == 'event'
        assert first_conditional.children[1].value == '='
        assert first_conditional.children[2].value == 'User Created'
        first_logical_connector = statement.children[1]
        assert first_logical_connector.value == 'or'
        second_statement = statement.children[2]
        assert len(second_statement.children) == 3
        second_conditional_event = second_statement.children[0]
        assert second_conditional_event.type == ASTType.CONDITIONAL
        assert len(second_conditional_event.children) == 3
        assert second_conditional_event.children[0].value == 'event'
        assert second_conditional_event.children[1].value == '='
        assert second_conditional_event.children[2].value == 'Product Account Created'
        second_logical_connector = second_statement.children[1]
        assert second_logical_connector.value == 'or'
        third_conditional = second_statement.children[2]
        assert third_conditional.type == ASTType.STATEMENT
        assert len(third_conditional.children) == 1
        third_conditional_event = third_conditional.children[0]
        assert third_conditional_event.type == ASTType.CONDITIONAL
        assert len(third_conditional_event.children) == 3
        assert third_conditional_event.children[0].value == 'event'
        assert third_conditional_event.children[1].value == '='
        assert third_conditional_event.children[2].value == 'User Status Changed'
        