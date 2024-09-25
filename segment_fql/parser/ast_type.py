from enum import Enum

class ASTType(str, Enum):
    ROOT = 'root',
    EXPR = 'expr',
    PATH = 'path',
    FUNC = 'func',
    ERR = 'err',
    NOT = 'not',
    OPERATOR = 'operator',
    CONDITIONAL = 'conditional',
    STATEMENT = 'statement',
    GROUPING = 'grouping'