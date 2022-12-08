"""Unit kinds and mapping"""

from enum import Enum, auto

from pint import Quantity, Unit


def check_dimensionality(quantity: Quantity, unit: Unit) -> None:
    """Check that quantity is of the same dimension as unit."""
    expected_dimensionality = unit.dimensionality
    if not quantity.dimensionality == expected_dimensionality:
        raise ValueError(
            f"Unexpected dimensionality '{quantity.dimensionality}', "
            f"expected: '{expected_dimensionality}'"
        )


class Units(Enum):
    HeatCapacity = auto()
    Density = auto()
    VolumetricHeatCapacity = auto()
    HeatFlow = auto()
    MassFlow = auto()
    VolumeFlow = auto()
    TemperatureDifference = auto()


units_map = {
    # Fluid Properties
    Units.HeatCapacity: ["kJ/(kg K)", "J/(kg K)"],
    Units.Density: ["kg/m³", "kg/dm³", "kg/cm³", "g/m³", "g/dm³", "g/cm³"],
    Units.VolumetricHeatCapacity: ["kJ/(m³ K)", "J/(m³ K)"],
    # Flow Properties
    Units.HeatFlow: ["kW", "W", "MW", "kWh/s", "Wh/s", "MWh/s"],
    Units.MassFlow: ["kg/s", "kg/min", "kg/h", "g/s", "g/min", "g/s"],
    Units.VolumeFlow: ["m³/h", "m³/min", "m³/s", "l/h", "l/min", "l/s"],
    Units.TemperatureDifference: ["K"],
}
