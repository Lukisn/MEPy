"""Unit knds and mapping"""

from enum import Enum, auto


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
