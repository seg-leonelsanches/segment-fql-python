from segment_fql.lexer import TokenType, Token
from segment_fql.parser.ast_node import ASTNode
from segment_fql.parser.ast_type import ASTType

class Parser:
    def __init__(self, lexer, tokens):
        self.supported_functions = ['contains', 'match']
        self.queue = tokens

    def _next(self):
        upcoming = self.queue[0]
        if upcoming.type != TokenType.EOS:
            return self.queue.pop(0)
        return Token(TokenType.EOS, 'eos')
        
    def _statement(self):
        node = ASTNode(ASTType.STATEMENT)
        expression = self._expression()
        node.children.append(expression)

        if self.queue[0].type == TokenType.EOS:
            return node

        if self.queue[0].type == TokenType.Operator:
            node.children.append(self._operator())
            node.children.append(self._expression())
            return node

        first_child = expression.children[0]
        expression_is_function = first_child is not None and first_child.type == ASTType.FUNC
        if expression_is_function and self.queue[0].type == TokenType.Conditional:
            return node

        raise Exception(f'Unexpected token in statement: {self.queue[0].type} ({self.queue[0].value})')

    def _conditional(self, left_operand):
        node = ASTNode(ASTType.CONDITIONAL)
        node.children.append(left_operand)
        operator = self._next()
        node.children.append(operator)
        right_operand = self.queue[0]

        # Paths or functions
        if right_operand.type == TokenType.Ident:
            node.children.append(self._pathOrFunction(self._next()))
        # Lists
        elif right_operand.type == TokenType.BrackLeft:
            node.children.append(self._list())
        else:
            node.children.append(self._next())

        return node

    def _expression(self):
        first_child = self._next()
        upcoming = self.queue[0]

        if upcoming.type not in [TokenType.Operator, TokenType.Ident, TokenType.Number, TokenType.String, TokenType.Null, TokenType.BrackLeft]:
            raise Exception(f'Unsupported token: {upcoming.type} ({upcoming.value})')

        if upcoming.type == TokenType.Operator:
            return self._conditional(first_child)

        node = ASTNode(ASTType.EXPR)
        node.children.append(first_child)
        return node
        

    def _operator(self):
        node = ASTNode(ASTType.OPERATOR)
        node.children.append(self._next())
        return node

    def _pathOrFunction(self, previous):
        '''things like `message.event` or `contains(...)`'''
        next_token = self.queue[0]

        if next_token.type == TokenType.ParenLeft:
            return self._function(previous)

        return self._path(previous)

    def _path(self, previous):
        node = ASTNode(ASTType.PATH)
        node.children.append(previous)

        while self.queue[0].type == TokenType.Dot or self.queue[0].type == TokenType.Ident:
            node.children.append(self._next())

        return node

    def _function(self, previous):
        if previous.type != TokenType.Ident or previous.value not in self.supported_functions:
            raise Exception(f'Unsupported function: {previous.value}')

        node = ASTNode(ASTType.FUNC)
        node.children.append(previous)

        testing_left_paren = self._next()
        if testing_left_paren.type != TokenType.ParenLeft:
            raise Exception(f'Expected "\(", got {testing_left_paren.type} ({testing_left_paren.value})')

        left_operand = ASTNode(ASTType.EXPR)
        upcoming = self.queue[0]
        if upcoming.type == TokenType.String:
            left_operand.children.append(self._next())
        elif upcoming.type == TokenType.Ident:
            left_operand.children.append(self._path(self._next()))
        else:
            raise Exception(f'Unsupported left operand: {upcoming.type} ({upcoming.value})')

        node.children.append(left_operand)

        testing_comma = self._next()
        if testing_comma.type != TokenType.Comma:
            raise Exception(f'Expected ",", got {testing_comma.type} ({testing_comma.value})')

        testing_substring = self._next()
        if testing_substring.type != TokenType.String:
            raise Exception(f'Expected string, got {testing_substring.type} ({testing_substring.value})')

        substring_node = ASTNode(ASTType.EXPR)
        substring_node.children.append(testing_substring)
        node.children.append(substring_node)

        testing_right_paren = self._next()
        if testing_right_paren.type != TokenType.ParenRight:
            raise Exception(f'Expected "\)", got {testing_right_paren.type} ({testing_right_paren.value})')

        return node

    def parse(self):
        root_node = ASTNode(ASTType.ROOT)
        root_node.children.append(self._statement())
        while self.queue:
            token = self.queue.pop(0)
            if token.type == TokenType.EOS:
                return root_node

            root_node.children.append(self._operator())
            root_node.children.append(self._statement())

        raise Exception(f'Unexpected token of type "type" and value "value"')
            