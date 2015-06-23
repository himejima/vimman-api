import os
import sys
import unittest

TEST_TARGETS = [
    'api_informations_test',
    'api_operators_test',
    'api_questions_test',
]


def suite():
    suite = unittest.TestSuite()
    for testmodule in TEST_TARGETS:
        exec 'from ' + testmodule + ' import suite as _suite'
        suite.addTests(_suite())
    return suite
