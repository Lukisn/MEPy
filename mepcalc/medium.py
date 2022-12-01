"""Medium class and medium mapping."""

from enum import Enum, auto

from pint import Quantity


class Medium:
    """Medium Properties."""

    @classmethod
    def water(cls):
        return Medium(
            name="Water",
            heat_cap=Quantity(4148.0, "kJ/(kg K)"),
            density=Quantity(998.2, "kg/m³"),
        )

    @classmethod
    def air(cls):
        return Medium(
            name="Air",
            heat_cap=Quantity(1006.0, "kJ/(kg K)"),
            density=Quantity(1.205, "kg/m³"),
        )

    def __init__(self, name: str, heat_cap: Quantity, density: Quantity) -> None:
        """Initializer."""
        self._name = name
        # TODO: check dimensionality of Quantity instances
        self._heat_capacity = heat_cap
        self._density = density

    def __repr__(self) -> str:
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
    def heat_capacity(self, value):
        """Setter for (isobaric heat capacity property."""
        self._heat_capacity = value  # TODO: check dimensionality

    @property
    def density(self) -> Quantity:
        """Getter for density property."""
        return self._density

    @density.setter
    def density(self, value):
        """Setter for density property."""
        self._density = value  # TODO: check dimensionality

    @property
    def volumetric_heat_capacity(self) -> Quantity:
        """Getter for volumetric heat capacity."""
        return self.heat_capacity * self.density


class Media(Enum):
    Water = auto()
    Air = auto()


media_map = {Media.Water: Medium.water(), Media.Air: Medium.air()}


def main():
    for kind, medium in media_map.items():
        print(f"{kind:20s} {medium}")

    print(Medium.water())


if __name__ == "__main__":
    main()
