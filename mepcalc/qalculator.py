"""Heat flow Calculator for calculations around the equation(s):
Q = m * cp * dT, with
    m = V * rho

Q = V * rho * cp * dT, with
   C := rho * cp

Q = V * C * dT, where
            dT = T1 - T2
"""
# TODO: extract calculation into separate class

import sys

from medium import Medium


class Qalculator:
    """Calculator for heat and mass/volume flow equations"""

    def __init__(self, medium: Medium) -> None:
        """Initializer."""
        self._medium = medium

    def __repr__(self) -> str:
        """String representation."""
        return f"{self.__class__.__name__}(medium={self._medium._name})"


def main():
    """Main program."""
    qalc = Qalculator(medium=Medium.water())
    print(qalc)

    sys.exit()


if __name__ == "__main__":
    main()
