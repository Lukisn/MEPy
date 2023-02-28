"""Base Calculator"""
from mepcalc import ureg
from mepcalc.common.medium import Medium


class BaseCalculator:

    DEFAULT_HEAT_FLOW_UNIT = ureg.watt
    DEFAULT_MASS_FLOW_UNIT = ureg.kilogram / ureg.second
    DEFAULT_VOLUME_FLOW_UNIT = ureg.meter**3 / ureg.second
    DEFAULT_TEMP_DIFF_UNIT = ureg.kelvin
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
