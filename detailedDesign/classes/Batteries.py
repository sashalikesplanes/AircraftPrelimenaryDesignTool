# To check
from detailedDesign.classes.Component import Component


class Batteries(Component):
    def __init__(self, Power, config):
        my_config = super().__init__(config)
        self.Power = Power

        # Create all the parameters that this component must have here:
        # Using self.property_name = value

        self._freeze()

# "Battery" ACID ;)
#                      H
#                      |
#                H  H  C--H
#                 `.|,'|
#                   C  H  H
#                   |     |
#              O    N  H  C
#              \\ ,' `.|,'|`.
#                C     C  H  H
#                |     |
#             H--C     H
#              ,' `.
#       H  H--C  H--C--H
#       |     ||    |
# H     C     C     N  H  H
#  `. ,' `. ,' `. ,' `.|,'
#    C  _  C  H  C     C
#    | (_) |   `.|     |
#    C     C     C     H
#  ,' `. ,' `. ,' `.
# H     C     C     H
#       |    ||
#       N-----C
#       |     |
#       H     H
