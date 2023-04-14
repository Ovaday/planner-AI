from helpers.openAIHelper import *

from django.test import TestCase


class ParseResponseCase(TestCase):
    input_text = "Here is your output: {'is_reminder': True, 'is_event': False}"
    output_parsable_expected = "Here is your output: {'is_reminder': true, 'is_event': false}"
    output_parsed_json = {"is_reminder": True, "is_event": False}

    def test_bool_replaced(self):
        self.assertEqual(replace_bools(self.input_text), self.output_parsable_expected)

    def test_parse_json(self):
        self.assertEqual(parse_json(self.input_text), self.output_parsed_json)
