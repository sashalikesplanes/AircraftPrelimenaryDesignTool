import unittest
from pathlib import Path

from misc.constants import testMargin
from misc.openData import openData
from detailedDesign.classes.State import State
from detailedDesign.classes.Aircraft import Aircraft


class TestAircraft(unittest.TestCase):
    def test_fuselage_group_sizing(self):
        config_file = Path('data', 'new_designs', 'config.yaml')
        states = {"cruise": State('cruise')}
        aircraft = Aircraft(openData(config_file), states)
