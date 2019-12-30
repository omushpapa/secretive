#! /usr/bin/env python3
"""Generate a simple but complex password limited by characters and specifications provided"""

import click
from cypher import Cypher
from random import choice
from string import (ascii_letters as letters, digits,
                    ascii_uppercase, ascii_lowercase)

punctuation = '!#$%&\'()*+,-./:;<=>?@[\\]^_{|}'

RULES = {
    'number': lambda: choice(digits),
    'lowercase': lambda: choice(ascii_lowercase),
    'uppercase': lambda: choice(ascii_uppercase),
    'special': lambda: choice(punctuation),
}
RULE_IDS = list(RULES.keys()) + ['all']

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


def update_password(password, value, position=None):
    """Update password with value

    :param str password: The password string
    :param str value: The value to update with
    :return: The updated password
    """
    result = list(password)
    if position is None:
        position = choice(range(len(password)))

    result.insert(position, value)
    return ''.join(result)


def fix_rule(rule, password):
    """Apply a rule

    :param str rule: The password rule
    :param str password: The password
    :return: A character that meets the rule
    :rtype: str
    """

    value = RULES.get(rule, lambda: choice(punctuation))()
    return update_password(password, value)


def generate_password(**kwargs):
    """Generate a simple but complex password

    Tries as much to use the provided character limitations.
    """
    word = ''.join(kwargs.get('word', '').split())
    length = kwargs['length']
    rules = kwargs['rule']

    password = ''.join(map(get_cypher, word))
    rem = length - len(password)
    if rem > 0:
        fillers = fill_length(rem)
        password = '{}{}'.format(password, fillers)

    if 'all' in rules:
        rules = RULE_IDS[:-1]

    for rule in rules:
        if not passes_rule(rule, password):
            password = fix_rule(rule, password)

    information = 'Your password: '
    click.echo(information + click.style(password, fg='cyan'))


def cli(word=True):
    rule = click.option('--rule', default=['all'], multiple=True, type=click.Choice(RULE_IDS))
    length = click.option('--length', default=8)

    if word:
        @click.command()
        @length
        @rule
        @click.argument('word')
        def password_gen(**kwargs):
            """Generate a random password string based off of specific characters"""
            return generate_password(**kwargs)

    else:
        @click.command()
        @length
        @rule
        def password_gen(**kwargs):
            """Generate a random password string"""
            return generate_password(**kwargs)

    return password_gen()


if __name__ == "__main__":
    cli(word=False)
