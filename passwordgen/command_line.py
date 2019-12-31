from .gen import cli


def password_from():
    cli()


def password_gen():
    cli(word=False)
