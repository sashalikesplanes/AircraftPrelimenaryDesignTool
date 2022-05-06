import unittest
from misc.constants import testMargin

# from unit_test.testExample import TestExample
from unit_test.testBalloonSizing import TestBalloonSizing
from unit_test.testEnergyRequired import TestEnergyRequired
from unit_test.testFuelMassEstimation import TestFuelMassEstimation


def main():
    """Main function for running unit tests"""
    unittest.main()


if __name__ == "__main__":
    main()

# Run the followign two commands in order to generate a code coverage report.
# coverage run -m unittest discover
# coverage report
