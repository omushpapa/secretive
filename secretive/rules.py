from enum import Enum
from random import choice
from string import digits, ascii_lowercase, ascii_uppercase

punctuation = '!#$%&\'()*+,-./:;<=>?@[\\]^_{|}'


class RuleType(Enum):
    NUMBER = 'number'
    LOWERCASE = 'lowercase'
    UPPERCASE = 'uppercase'
    SPECIAL = 'special'


RULES = {
    RuleType.NUMBER: lambda: choice(digits),
    RuleType.LOWERCASE: lambda: choice(ascii_lowercase),
    RuleType.UPPERCASE: lambda: choice(ascii_uppercase),
    RuleType.SPECIAL: lambda: choice(punctuation),
}
