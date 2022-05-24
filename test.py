import unittest
from misc.constants import testMargin

from unit_test.testWeights import TestWeights
from unit_test.testISA import TestISA

# from unit_test.testExample import TestExample


def main():
    """Main function for running unit tests"""
    unittest.main()


if __name__ == "__main__":
    main()

# Run the followign two commands in order to generate a code coverage report.
# coverage run -m unittest discover
# coverage report
