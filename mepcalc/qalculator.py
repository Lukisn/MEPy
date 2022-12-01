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
    C := ϱ * cp: volumetric heat capacity (in J/(m³ K))

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

import sys

from .medium import Medium
from pint import Quantity, UnitRegistry, Unit

ureg = UnitRegistry()


class Qalculator:
    """Calculator for heat and mass/volume flow equations.
    (I)    Q = m * cp * 𝛥T
    (II)   m = V * ϱ
    (III)  C := cp * ϱ
    (IV)   Q = V * ϱ * cp * 𝛥T  (II) in (I)
    (V)    Q = V * C * 𝛥T       (III) in (IV)
    """

    HEAT_FLOW_UNIT = ureg.watt
    MASS_FLOW_UNIT = ureg.kilogram / ureg.second
    VOLUME_FLOW_UNIT = ureg.meter**3 / ureg.second
    TEMPERATURE_DIFFERENCE_UNIT = ureg.kelvin

    def __init__(self, medium: Medium) -> None:
        """Initializer."""
        self._medium = medium

    def __repr__(self) -> str:
        """String representation."""
        return f"{self.__class__.__name__}(medium={self._medium.name})"

    @property
    def medium(self):
        """Getter for medium."""
        return self._medium

    @staticmethod
    def check(quantity: Quantity, unit: Unit) -> None:
        """Check that quantity is of the dimensionality of the given unit."""
        expected_dimensionality = unit.dimensionality
        if not quantity.dimensionality == expected_dimensionality:
            raise ValueError(
                f"Unexpected dimensionality '{quantity.dimensionality}', "
                f"expected: '{expected_dimensionality}'"
            )

    def heat_flow_from_mass_flow(
        self,
        mass_flow: Quantity,
        temp_diff: Quantity,
        unit: Unit = HEAT_FLOW_UNIT,
    ) -> Quantity:
        """Calculate heat flow from mass flow and temperature difference.
        Q = f(m, 𝛥T) = m * cp * 𝛥T
        """
        self.check(mass_flow, self.MASS_FLOW_UNIT)
        self.check(temp_diff, self.TEMPERATURE_DIFFERENCE_UNIT)
        heat_flow = mass_flow * self.medium.heat_capacity * temp_diff
        return heat_flow.to(unit)

    def heat_flow_from_volume_flow(
        self,
        volume_flow: Quantity,
        temp_diff: Quantity,
        unit: Unit = HEAT_FLOW_UNIT,
    ):
        """Calculate heat flow from volume flow and temperature difference.
        Q = f(V, 𝛥T) = V * ϱ *cp * 𝛥T = V * C * 𝛥T
        """
        self.check(volume_flow, self.VOLUME_FLOW_UNIT)
        self.check(temp_diff, self.TEMPERATURE_DIFFERENCE_UNIT)
        heat_flow = volume_flow * self.medium.volumetric_heat_capacity * temp_diff
        return heat_flow.to(unit)

    def mass_flow_from_heat_flow(
        self,
        heat_flow: Quantity,
        temp_diff: Quantity,
        unit: Unit = MASS_FLOW_UNIT,
    ):
        """Calculate mass flow from heat flow and temperature difference.
        m = f(Q, 𝛥T) = Q / (cp * 𝛥T)
        """
        self.check(heat_flow, self.HEAT_FLOW_UNIT)
        self.check(temp_diff, self.TEMPERATURE_DIFFERENCE_UNIT)
        mass_flow = heat_flow / (self.medium.heat_capacity * temp_diff)
        return mass_flow.to(unit)

    def mass_flow_from_volume_flow(
        self, volume_flow: Quantity, unit: Unit = MASS_FLOW_UNIT
    ):
        """Calculate mass flow from volume flow.
        m = f(V) = V * ϱ
        """
        self.check(volume_flow, self.VOLUME_FLOW_UNIT)
        mass_flow = volume_flow * self.medium.density
        return mass_flow.to(unit)

    def volume_flow_from_heat_flow(
        self,
        heat_flow: Quantity,
        temp_diff: Quantity,
        unit: Unit = VOLUME_FLOW_UNIT,
    ):
        """Calculate volume flow from heat flow.
        V = f(Q, 𝛥T) = Q / (C * 𝛥T)
        """
        self.check(heat_flow, self.HEAT_FLOW_UNIT)
        self.check(temp_diff, self.TEMPERATURE_DIFFERENCE_UNIT)
        volume_flow = heat_flow / (self.medium.volumetric_heat_capacity * temp_diff)
        return volume_flow.to(unit)

    def volume_flow_from_mass_flow(
        self, mass_flow: Quantity, unit: Unit = VOLUME_FLOW_UNIT
    ):
        """Calculate volume flow from mass flow.
        V = f(m) = m / ϱ
        """
        self.check(mass_flow, self.MASS_FLOW_UNIT)
        volume_flow = mass_flow / self.medium.density
        return volume_flow.to(unit)

    def temperature_difference_from_mass_flow(
        self,
        heat_flow: Quantity,
        mass_flow: Quantity,
        unit: Unit = TEMPERATURE_DIFFERENCE_UNIT,
    ):
        """Calculate temperature difference from mass flow.
        𝛥T = f(Q, m) = Q / (m * cp)
        """
        self.check(heat_flow, self.HEAT_FLOW_UNIT)
        self.check(mass_flow, self.MASS_FLOW_UNIT)
        temp_diff = heat_flow / (mass_flow * self.medium.heat_capacity)
        return temp_diff.to(unit)

    def temperature_difference_from_volume_flow(
        self,
        heat_flow: Quantity,
        volume_flow: Quantity,
        unit: Unit = TEMPERATURE_DIFFERENCE_UNIT,
    ):
        """Calculate temperature difference from volume flow.
        𝛥T = f(Q, V) = Q / (V * C)
        """
        self.check(heat_flow, self.HEAT_FLOW_UNIT)
        self.check(volume_flow, self.VOLUME_FLOW_UNIT)
        temp_diff = heat_flow / (volume_flow * self.medium.volumetric_heat_capacity)
        return temp_diff.to(unit)
