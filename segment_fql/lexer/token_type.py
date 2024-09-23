from enum import Enum

class TokenType(str, Enum):
    Err = 'err',
    Ident = 'ident',
    Dot = 'dot',
    Operator = 'operator',
    Conditional = 'conditional',
    String = 'string',
    Number = 'number',
    Null = 'null',
    BrackLeft = 'brackleft',
    BrackRight = 'brackright',
    ParenLeft = 'parenleft',
    ParenRight = 'parenright',
    Comma = 'comma',
    EOS = 'eos'