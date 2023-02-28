"""Duct Air Flow Calculator.

V = v * A
        A_rect = B * H
        A_round = pi/4 * D^2
(V = m / ϱ)

-> Volume Flow
V = v * A
V = v * B * H
V = v * pi/4 * D^2

-> Velocity
v = V / A
v = V / (B * H)
v = V / (pi/4 * D^2)

-> Mass Flow
m = V * ϱ
"""
import math

from pint import Quantity, Unit

from mepcalc import ureg
from mepcalc.common.medium import Medium
from mepcalc.common.units import check_dimensionality


# TODO: extract base class with defaults and init
class Ductulator:
    """Calculator for duct air flow."""

    DEFAULT_VOLUME_FLOW_UNIT = ureg.meter**3 / ureg.second
    DEFAULT_MASS_FLOW_UNIT = ureg.kilogram / ureg.second
    DEFAULT_VELOCITY_UNIT = ureg.meter / ureg.second
    DEFAULT_AREA_UNIT = ureg.meter**2
    DEFAULT_LENGTH_UNIT = ureg.meter

    def __init__(self, medium: Medium) -> None:
        """Initializer."""
        self._medium = medium

    def __repr__(self) -> str:  # pragma: no cover
        """String representation."""
        return f"{self.__class__.__name__}(medium={self._medium.name})"

    @property
    def medium(self):
        """Getter for medium."""
        return self._medium

    def volume_flow_from_area(
        self, velocity: Quantity, area: Quantity, unit: Unit = DEFAULT_VOLUME_FLOW_UNIT
    ):
        """V = v * A"""
        check_dimensionality(velocity, self.DEFAULT_VELOCITY_UNIT)
        check_dimensionality(area, self.DEFAULT_AREA_UNIT)
        volume_flow = velocity * area
        return volume_flow.to(unit)

    def volume_flow_from_width_height(
        self,
        velocity: Quantity,
        width: Quantity,
        height: Quantity,
        unit: Unit = DEFAULT_VOLUME_FLOW_UNIT,
    ):
        """V = v * B * H"""
        check_dimensionality(velocity, self.DEFAULT_VELOCITY_UNIT)
        check_dimensionality(width, self.DEFAULT_LENGTH_UNIT)
        check_dimensionality(height, self.DEFAULT_LENGTH_UNIT)
        volume_flow = velocity * width * height
        return volume_flow.to(unit)

    def volume_flow_from_diameter(
        self,
        velocity: Quantity,
        diameter: Quantity,
        unit: Unit = DEFAULT_VOLUME_FLOW_UNIT,
    ):
        """V = v * pi/4 * D^2"""
        check_dimensionality(velocity, self.DEFAULT_VELOCITY_UNIT)
        check_dimensionality(diameter, self.DEFAULT_LENGTH_UNIT)
        volume_flow = velocity * (math.pi / 4) * diameter**2
        return volume_flow.to(unit)

    def velocity_from_area(
        self, volume_flow: Quantity, area: Quantity, unit: Unit = DEFAULT_VELOCITY_UNIT
    ):
        """v = V / A"""
        check_dimensionality(volume_flow, self.DEFAULT_VOLUME_FLOW_UNIT)
        check_dimensionality(area, self.DEFAULT_AREA_UNIT)
        velocity = volume_flow / area
        return velocity.to(unit)

    def velocity_from_width_height(
        self,
        volume_flow: Quantity,
        width: Quantity,
        height: Quantity,
        unit: Unit = DEFAULT_VELOCITY_UNIT,
    ):
        """v = V / (B * H)"""
        check_dimensionality(volume_flow, self.DEFAULT_VOLUME_FLOW_UNIT)
        check_dimensionality(width, self.DEFAULT_LENGTH_UNIT)
        check_dimensionality(height, self.DEFAULT_LENGTH_UNIT)
        velocity = volume_flow / (width * height)
        return velocity.to(unit)

    def velocity_from_diameter(
        self,
        volume_flow: Quantity,
        diameter: Quantity,
        unit: Unit = DEFAULT_VELOCITY_UNIT,
    ):
        """v = V / (pi/4 * D^2)"""
        check_dimensionality(volume_flow, self.DEFAULT_VOLUME_FLOW_UNIT)
        check_dimensionality(diameter, self.DEFAULT_LENGTH_UNIT)
        velocity = volume_flow / ((math.pi / 4) * diameter**2)
        return velocity.to(unit)

    def mass_flow_from_volume_flow(
        self, volume_flow: Quantity, unit: Unit = DEFAULT_MASS_FLOW_UNIT
    ):
        """m = V * ϱ"""
        check_dimensionality(volume_flow, self.DEFAULT_VOLUME_FLOW_UNIT)
        mass_flow = volume_flow * self.medium.density
        return mass_flow.to(unit)

    def volume_flow_from_mass_flow(
        self, mass_flow: Quantity, unit: Unit = DEFAULT_VOLUME_FLOW_UNIT
    ):
        """V = m / ϱ"""
        check_dimensionality(mass_flow, self.DEFAULT_MASS_FLOW_UNIT)
        volume_flow = mass_flow / self.medium.density
        return volume_flow.to(unit)
