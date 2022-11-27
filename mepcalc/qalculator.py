"""Heat Flow Calculator.

Calculator or calculations around the following equations:
    (I)  Q = m * cp * 𝛥T,
    (II) m = V * ϱ,

with the following symbols for the heat/fluid flow variables (SI units in
parentheses):
    Q:           heat flow                (in W)
    m:           mass flow                (in kg/s)
    V:           volume flow              (in m³/s)
    𝛥T:          temperature difference   (in K)
and the following fluid properties:
    cp:          isobaric heat capacity   (in J/(kg K)
    ϱ:           density                  (in m³/kg)
for brevity with the following definition:
    C := ϱ * cp: volumetric heat capacity (in J/(m³ K)

This results in the following calculation formulas (fluid properties omitted
as inputs, since they are assumed to be fixed):
    (A) Q = f(m, 𝛥T) = m * cp * 𝛥T
    (B) Q = f(V, 𝛥T) = V * C * 𝛥T
    (C) m = f(Q, 𝛥T) = Q / (cp * 𝛥T)
    (D) m = f(V) = V * ϱ
    (E) V = f(Q, 𝛥T) = Q / (C * 𝛥T)
    (F) V = f(m) = m / ϱ
    (G) 𝛥T = f(Q, m) = Q / (m * cp)
    (H) 𝛥T = f(Q, V) = Q / (V * C)
"""
# TODO: implement remaining calculation methods

import sys

from medium import Medium
from pint import Quantity, UnitRegistry, Unit

ureg = UnitRegistry()


class Qalculator:
    """Calculator for heat and mass/volume flow equations."""

    def __init__(self, medium: Medium) -> None:
        """Initializer."""
        self._medium = medium

    def __repr__(self) -> str:
        """String representation."""
        return f"{self.__class__.__name__}(medium={self._medium._name})"

    @staticmethod
    def check(quantity: Quantity, unit: Unit) -> None:
        """Check that quantity is of the dimensionality of the given unit."""
        expected_dimensionality = unit.dimensionality
        if not quantity.dimensionality == expected_dimensionality:
            raise ValueError(
                f"Unexpected dimensionality '{quantity.dimensionality}', "
                f"expected: '{expected_dimensionality}'"
            )

    def heat_flow_from_mass_flow(self,
            mass_flow: Quantity,
            temp_diff: Quantity,
            output_unit: Unit = ureg.watt
    ) -> Quantity:
        """Calculate heat capacity from mass flow and temperature difference.
        Q = f(m, 𝛥T) = m * cp * 𝛥T
        """
        self.check(mass_flow, ureg.kg / ureg.s)
        self.check(temp_diff, ureg.K)
        result = mass_flow * self._medium.heat_capacity * temp_diff
        return result.to(output_unit)


def main():
    """Main program."""
    qalc = Qalculator(medium=Medium.water())
    print(qalc)

    # TODO: extract testing code into unit tests
    mass_flow = Quantity(10.5, "kg/h")
    temp_diff = Quantity(15, "K")

    print(qalc.heat_flow_from_mass_flow(mass_flow, temp_diff, ureg.kilowatt))

    sys.exit()


if __name__ == "__main__":
    main()
