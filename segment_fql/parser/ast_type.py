from enum import Enum

class ASTType(str, Enum):
    ROOT = 'root',
    EXPR = 'expr',
    PATH = 'path',
    FUNC = 'func',
    ERR = 'err',
    OPERATOR = 'operator',
    CONDITIONAL = 'conditional',
    STATEMENT = 'statement'