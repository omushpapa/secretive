#! /usr/bin/env python3
"""Generate a simple but complex password limited by characters and specifications provided"""

from random import choice
from string import ascii_letters

import click

from .cypher import Cypher
from .rules import RULES, RuleType, punctuation

RULE_IDS = list(map(lambda i: i.value, RULES.keys())) + ['all']

cypher = Cypher()
select_cyphers = cypher.sample_cyphers()


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
        char = get_cypher(choice(ascii_letters))
        chars.append(str(char))

    return ''.join(chars)


def passes_rule(rule, password):
    """Check if password passes the rule

    :param RuleType rule: The rule to verify
    :param str password: The password
    :return: True if rule passes, else False
    :rtype: bool
    """
    if rule == RuleType.NUMBER:
        return any((c for c in password if c.isdigit()))

    elif rule == RuleType.LOWERCASE:
        return any((c for c in password if c.islower()))

    elif rule == RuleType.UPPERCASE:
        return any((c for c in password if c.isupper()))

    elif rule == RuleType.SPECIAL:
        return any((c for c in password if c in punctuation))

    raise NotImplementedError(f'Rule {rule} has not been implemented')


def update_password(password, value, position=None):
    """Update password with value

    :param str password: The password string
    :param str value: The character(s) to update with
    :param int position: The position in which to insert the character(s)
    :return: The updated password
    """
    result = list(password)
    if position is None:
        position = choice(range(len(password)))

    result.insert(position, value)
    return ''.join(result)


def apply_rule(rule, password):
    """Apply a rule

    :param RuleType rule: The password rule
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
        rule_ = RuleType(rule)
        if not passes_rule(rule_, password):
            password = apply_rule(rule_, password)

    return password


def _password_gen(**kwargs):
    password = generate_password(**kwargs)
    information = 'Your password: '
    click.echo(information + click.style(password, fg='cyan'))


def from_word(word_arg):
    if word_arg:
        return click.argument('word')

    return lambda x: x


def cli(word=True):
    rule = click.option('--rule', default=['all'], multiple=True, type=click.Choice(RULE_IDS))
    length = click.option('--length', default=8)

    @click.command()
    @length
    @rule
    @from_word(word)
    def password_gen(**kwargs):
        """Generate a random password string"""
        return _password_gen(**kwargs)

    return password_gen()


if __name__ == "__main__":
    cli(word=False)
