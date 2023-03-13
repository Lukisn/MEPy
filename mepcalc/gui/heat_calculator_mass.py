"""Heat Flow Calculator GUI, using mass flow based formulae.

Simplified GUI for only calculation heat flow, fluid flow and temperature difference
based on mass flow.
"""

import sys

from PySide6.QtWidgets import QApplication
from pint import Quantity

from mepcalc.common.medium import Medium
from mepcalc.gui.heat_calculator_base import HeatCalculatorWidget


# TODO: format number output to reduce decimal places
class HeatCalculatorMassWidget(HeatCalculatorWidget):
    """Heat flow from mass flow calculator widget."""

    def initialize_widgets(self) -> None:
        """Setup widgets for the user interface."""
        super().initialize_widgets()
        self.permanently_disable(self.radio_volume_flow)
        self.permanently_disable(self.edit_volume_flow_magnitude)

    def calculate_heat_flow(self) -> None:
        """Calculate heat flow.

        Using formula: Q = m * cp * dT
        """
        # read inputs
        mass_flow = Quantity(
            float(self.edit_mass_flow_magnitude.text() or 0),
            self.combo_mass_flow_unit.currentText(),
        )
        temp_diff = Quantity(
            float(self.edit_temp_diff_magnitude.text() or 0),
            self.combo_temp_diff_unit.currentText(),
        )
        heat_flow_unit = self.combo_heat_flow_unit.currentText()
        # calculate result
        heat_flow = mass_flow * self.medium.heat_capacity * temp_diff
        print("calculating heat flow using Q = m * cp * dT:")
        print(
            f"{heat_flow:~P} = "
            f"{mass_flow:~P} * {self.medium.heat_capacity:~P} * {temp_diff:~P}"
        )
        # write output
        self.edit_heat_flow_magnitude.setText(
            str(heat_flow.to(heat_flow_unit).magnitude)
        )
        self.calculate_volume_flow()

    def calculate_mass_flow(self) -> None:
        """Calculate mass flow using:

        m = Q / (cp * dT)
        """
        # read inputs
        heat_flow = Quantity(
            float(self.edit_heat_flow_magnitude.text() or 0),
            self.combo_heat_flow_unit.currentText(),
        )
        temp_diff = Quantity(
            float(self.edit_temp_diff_magnitude.text() or 0),
            self.combo_temp_diff_unit.currentText(),
        )
        mass_flow_unit = self.combo_mass_flow_unit.currentText()
        # calculate result
        mass_flow = heat_flow / (self.medium.heat_capacity * temp_diff)
        print("calculating mass flow using m = Q / (cp * dT):")
        print(
            f"{mass_flow:~P} = "
            f"{heat_flow:~P} / ({self.medium.heat_capacity:~P} * {temp_diff:~P})"
        )
        # write outputs
        self.edit_mass_flow_magnitude.setText(
            str(mass_flow.to(mass_flow_unit).magnitude)
        )
        self.calculate_volume_flow()

    def calculate_volume_flow(self) -> None:
        """Calculate volume flow.

        Using formula: V = m / rho"""
        # read inputs
        mass_flow = Quantity(
            float(self.edit_mass_flow_magnitude.text() or 0),
            self.combo_mass_flow_unit.currentText(),
        )
        volume_flow_unit = self.combo_volume_flow_unit.currentText()
        # calculate result
        volume_flow = mass_flow / self.medium.density
        print("calculating volume flow using V = m / rho:")
        print(f"{volume_flow:~P} = {mass_flow:~P} / {self.medium.density:~P}")
        # write outputs
        self.edit_volume_flow_magnitude.setText(
            str(volume_flow.to(volume_flow_unit).magnitude)
        )

    def calculate_temperature_difference(self) -> None:
        """Calculate temperature difference.

        Using formula: dT = Q / (m * cp)"""
        # read inputs
        heat_flow = Quantity(
            float(self.edit_heat_flow_magnitude.text() or 0),
            self.combo_heat_flow_unit.currentText(),
        )
        mass_flow = Quantity(
            float(self.edit_mass_flow_magnitude.text() or 0),
            self.combo_mass_flow_unit.currentText(),
        )
        temperature_difference_unit = self.combo_temp_diff_unit.currentText()
        # calculate result
        temp_diff = heat_flow / (mass_flow * self.medium.heat_capacity)
        print("calculating temperature difference using dt = Q / (m * cp):")
        print(
            f"{temp_diff:~P} = "
            f"{heat_flow:~P} / ({mass_flow:~P} * {self.medium.heat_capacity:~P})"
        )
        # write outputs
        self.edit_temp_diff_magnitude.setText(
            str(temp_diff.to(temperature_difference_unit).magnitude)
        )
        self.calculate_volume_flow()


def main():
    """Main program."""
    app = QApplication()
    window = HeatCalculatorMassWidget(medium=Medium.water())
    window.setWindowTitle("Heat Flow Calculator Mass")
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
