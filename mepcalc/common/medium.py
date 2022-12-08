"""Medium class and medium mapping."""

from enum import Enum, auto
from typing import Self

from pint import Quantity, Unit

from mepcalc.common.units import check_dimensionality


class Medium:
    """Medium Properties."""

    HEAT_CAPACITY_UNIT = Unit("J/(kg K)")
    DENSITY_UNIT = Unit("kg/m³")

    @classmethod
    def water(cls) -> Self:
        return cls(
            name="Water",
            heat_cap=Quantity(4148.0, "kJ/(kg K)"),
            density=Quantity(998.2, "kg/m³"),
        )

    @classmethod
    def air(cls) -> Self:
        return cls(
            name="Air",
            heat_cap=Quantity(1006.0, "kJ/(kg K)"),
            density=Quantity(1.205, "kg/m³"),
        )

    def __init__(self, name: str, heat_cap: Quantity, density: Quantity) -> None:
        """Initializer."""
        self._name = name
        check_dimensionality(heat_cap, self.HEAT_CAPACITY_UNIT)
        check_dimensionality(density, self.DENSITY_UNIT)
        self._heat_capacity = heat_cap
        self._density = density

    def __repr__(self) -> str:  # pragma: no cover
        """String representation."""
        return (
            f"{self.__class__.__name__}("
            f"name={self._name},"
            f"heat_capacity={self._heat_capacity:~P},"
            f"density={self._density:~P}"
            f")"
        )

    @property
    def name(self) -> str:
        """Getter for name property."""
        return self._name

    @property
    def heat_capacity(self) -> Quantity:
        """Getter for (isobaric) heat capacity property."""
        return self._heat_capacity

    @heat_capacity.setter
    def heat_capacity(self, value: Quantity) -> None:
        """Setter for (isobaric) heat capacity property."""
        check_dimensionality(value, self.HEAT_CAPACITY_UNIT)
        self._heat_capacity = value

    @property
    def density(self) -> Quantity:
        """Getter for density property."""
        return self._density

    @density.setter
    def density(self, value: Quantity) -> None:
        """Setter for density property."""
        check_dimensionality(value, self.DENSITY_UNIT)
        self._density = value

    @property
    def volumetric_heat_capacity(self) -> Quantity:
        """Getter for volumetric heat capacity."""
        return self.heat_capacity * self.density


class Media(Enum):
    Water = auto()
    Air = auto()


media_map = {Media.Water: Medium.water(), Media.Air: Medium.air()}
