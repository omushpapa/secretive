import unittest
from random import choice, randint
from string import ascii_uppercase, ascii_lowercase, digits, ascii_letters

from passwordgen.gen import passes_rule, punctuation, update_password, apply_rule, RuleType, generate_password


def get_random_string(length=10):
    """Generate a random string of fixed length"""
    letters = ascii_lowercase
    return ''.join(choice(letters) for i in range(length))


class GenTestCase(unittest.TestCase):

    def test_returns_false_if_invalid_number_rule_passes(self):
        self.assertFalse(
            passes_rule(RuleType.NUMBER, 'kdjkfg')
        )

    def test_returns_false_if_invalid_lowercase_rule_passes(self):
        self.assertFalse(
            passes_rule(RuleType.LOWERCASE, choice(ascii_uppercase))
        )

    def test_returns_false_if_invalid_uppercase_rule_passes(self):
        self.assertFalse(
            passes_rule(RuleType.UPPERCASE, choice(ascii_lowercase))
        )

    def test_returns_false_if_invalid_special_rule_passes(self):
        self.assertFalse(
            passes_rule(RuleType.SPECIAL, 'k')
        )

    def test_returns_false_if_valid_number_rule_fails(self):
        self.assertTrue(
            passes_rule(RuleType.NUMBER, choice(digits))
        )

    def test_returns_false_if_valid_lowercase_rule_fails(self):
        self.assertTrue(
            passes_rule(RuleType.LOWERCASE, choice(ascii_lowercase))
        )

    def test_returns_false_if_valid_uppercase_rule_fails(self):
        self.assertTrue(
            passes_rule(RuleType.UPPERCASE, choice(ascii_uppercase))
        )

    def test_returns_false_if_valid_special_rule_fails(self):
        self.assertTrue(
            passes_rule(RuleType.SPECIAL, choice(punctuation))
        )

    def test_returns_false_if_updated_password_fails(self):
        password = get_random_string()
        char_index = randint(0, len(password) - 1)
        char = password[char_index]
        new_char = char

        while new_char == char:
            new_char = choice(ascii_letters)

        with self.subTest():
            self.assertNotEqual(new_char, char)

        with self.subTest():
            self.assertNotEqual(password[char_index], new_char)

        new_password = update_password(password, new_char, char_index)

        with self.subTest():
            self.assertNotEqual(password, new_password)

        self.assertEqual(new_password[char_index], new_char)

    def test_returns_false_if_updated_password_fails_without_given_position(self):
        password = get_random_string()

        new_char = choice(ascii_letters)
        while new_char in password:
            new_char = choice(ascii_letters)

        with self.subTest():
            self.assertFalse(new_char in password)

        new_password = update_password(password, new_char)

        with self.subTest():
            self.assertFalse(new_char in password)

        self.assertTrue(new_char in new_password)

    def test_returns_false_if_apply_rule_number_fails(self):
        password = 'rt'
        with self.subTest():
            self.assertFalse(
                passes_rule(RuleType.NUMBER, password)
            )

        new_password = apply_rule(RuleType.NUMBER, password)
        with self.subTest():
            self.assertGreater(len(new_password), 0)

        self.assertTrue(
            passes_rule(RuleType.NUMBER, new_password)
        )

    def test_returns_false_if_apply_rule_lowercase_fails(self):
        password = 'RT'
        with self.subTest():
            self.assertFalse(
                passes_rule(RuleType.LOWERCASE, password)
            )

        new_password = apply_rule(RuleType.LOWERCASE, password)
        with self.subTest():
            self.assertGreater(len(new_password), 0)

        self.assertTrue(
            passes_rule(RuleType.LOWERCASE, new_password)
        )

    def test_returns_false_if_apply_rule_uppercase_fails(self):
        password = 'rt'
        with self.subTest():
            self.assertFalse(
                passes_rule(RuleType.UPPERCASE, password)
            )

        new_password = apply_rule(RuleType.UPPERCASE, password)
        with self.subTest():
            self.assertGreater(len(new_password), 0)

        self.assertTrue(
            passes_rule(RuleType.UPPERCASE, new_password)
        )

    def test_returns_false_if_apply_rule_special_fails(self):
        password = 'rt'
        with self.subTest():
            self.assertFalse(
                passes_rule(RuleType.SPECIAL, password)
            )

        new_password = apply_rule(RuleType.SPECIAL, password)
        with self.subTest():
            self.assertGreater(len(new_password), 0)

        self.assertTrue(
            passes_rule(RuleType.SPECIAL, new_password)
        )

    def test_returns_false_if_generated_password_not_match_all_rules(self):
        length = 8
        kwargs = {
            'length': length,
            'rule': [
                'all'
            ]
        }
        password = generate_password(**kwargs)
        with self.subTest():
            self.assertGreaterEqual(len(password), length)

        for rule in RuleType:
            with self.subTest():
                self.assertTrue(
                    passes_rule(rule, password)
                )

    def test_returns_false_if_generated_password_not_match_uppercase_rule(self):
        length = 8
        kwargs = {
            'length': length,
            'rule': [
                RuleType.UPPERCASE.value
            ]
        }
        password = generate_password(**kwargs)
        with self.subTest():
            self.assertGreaterEqual(len(password), length)

        self.assertTrue(
            passes_rule(RuleType.UPPERCASE, password)
        )

    def test_returns_false_if_generated_password_not_match_lowercase_rule(self):
        length = 8
        kwargs = {
            'length': length,
            'rule': [
                RuleType.LOWERCASE.value
            ]
        }
        password = generate_password(**kwargs)
        with self.subTest():
            self.assertGreaterEqual(len(password), length)

        self.assertTrue(
            passes_rule(RuleType.LOWERCASE, password)
        )

    def test_returns_false_if_generated_password_not_match_special_rule(self):
        length = 8
        kwargs = {
            'length': length,
            'rule': [
                RuleType.SPECIAL.value
            ]
        }
        password = generate_password(**kwargs)
        with self.subTest():
            self.assertGreaterEqual(len(password), length)

        self.assertTrue(
            passes_rule(RuleType.SPECIAL, password)
        )

    def test_returns_false_if_generated_password_not_match_number_rule(self):
        length = 8
        kwargs = {
            'length': length,
            'rule': [
                RuleType.NUMBER.value
            ]
        }
        password = generate_password(**kwargs)
        with self.subTest():
            self.assertGreaterEqual(len(password), length)

        self.assertTrue(
            passes_rule(RuleType.NUMBER, password)
        )

    def test_returns_false_if_generated_password_not_match_length(self):
        length = randint(1, 100)
        kwargs = {
            'length': length,
            'rule': 'all'
        }
        password = generate_password(**kwargs)
        self.assertGreaterEqual(len(password), length)


if __name__ == "__main__":
    unittest.main()
