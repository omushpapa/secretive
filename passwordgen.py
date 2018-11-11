#! /usr/bin/env python3
"""Generate a simple but complex password limited by characters and specifications provided"""

import click
from cypher import Cypher
from random import choice, randint
from string import (ascii_letters as letters, digits,
                    ascii_uppercase, ascii_lowercase)

punctuation = '!#$%&\'()*+,-./:;<=>?@[\\]^_{|}'

RULES = ['number', 'lowercase', 'uppercase', 'special', 'all']

cypher = Cypher()
select_cyphers = cypher.get_available_cyphers()


def get_cypher(char):
    """Get the cypher for a character

    :param str char: A single character
    :return: A cypher for the character
    :rtype: str
    """
    result = choice(select_cyphers)[1](str(char))
    return str(result)


def fill_length(number):
    """Add character paddings

    :param int number: The number of characters to return
    :return: The extra characters required to pad the password
    :rtype: str
    """
    chars = []
    for _ in range(number):
        char = get_cypher(choice(letters))
        chars.append(str(char))

    return ''.join(chars)


def passes_rule(rule, password):
    """Check if password passes the rule

    :param str rule: The rule to verify
    :param str password: The password
    :return: True if rule passes, else False
    :rtype: bool
    """
    if rule == 'number':
        for c in password:
            if c.isdigit():
                return True
    elif rule == 'lowercase':
        for c in password:
            if c.islower():
                return True
    elif rule == 'uppercase':
        for c in password:
            if c.isupper():
                return True
    elif rule == 'special':
        for c in password:
            if c in punctuation:
                return True

    return False


def fix_rule(rule, password):
    """Apply a rule

    :param str rule: The password rule
    :param str password: The password
    :return: A character that meets the rule
    :rtype: str
    """
    value = '.'
    if rule == 'number':
        value = choice(digits)

    elif rule == 'lowercase':
        l = (i for i in password if i in ascii_lowercase)
        value = next(l, ascii_lowercase)

    elif rule == 'uppercase':
        l = (i for i in password if i in ascii_uppercase)
        value = next(l, ascii_uppercase)

    elif rule == 'special':
        l = (i for i in password if i in punctuation)
        value = next(l, choice(punctuation))

    result = list(password)
    length = len(result)
    result.insert(randint(int(length/2), length), value)
    return ''.join(result)


@click.command()
@click.option('--length', default=8)
@click.option('--rule', default=['all'], multiple=True, type=click.Choice(RULES))
@click.argument('name')
def generate_password(**kwargs):
    """Generate a simple but complex password

    Tries as much to use the provided character limitations.
    """
    name = ''.join(kwargs['name'].split())
    length = kwargs['length']
    rules = kwargs['rule']

    password = ''.join(map(get_cypher, name))
    rem = length - len(password)
    if rem > 0:
        fillers = fill_length(rem)
        password = '{}{}'.format(password, fillers)

    if 'all' in rules:
        rules = RULES
        rules.remove('all')

    for rule in rules:
        if not passes_rule(rule, password):
            password = fix_rule(rule, password)

    print('Your password: {}'.format(password))


if __name__ == "__main__":
    generate_password()
