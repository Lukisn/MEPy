"""Heat Flow Calculator GUI, using volume flow based formulae.

Simplified GUI for only calculation heat flow, fluid flow and temperature difference
based on volume flow.
"""

import sys

from pint import Quantity
from PySide6.QtWidgets import QApplication
from qalculator_gui_base import QalculatorWidget


class QalculatorVolumeWidget(QalculatorWidget):
    """Heat flow from volume flow calculator widget."""

    def initialize_widgets(self) -> None:
        """Setup widgets for the user interface."""
        super().initialize_widgets()
        self.permanently_disable(self.radio_mass_flow)
        self.permanently_disable(self.edit_mass_flow_magnitude)

    def calculate_heat_flow(self) -> None:
        """Calculate heat flow from volume flow and temperature difference.

        Using formila: Q = m * cp * dT, m = V * rho and C := rho * cp
        effectively running: Q = V * C * dT
        """
        # read inputs
        volume_flow = Quantity(
            float(self.edit_volume_flow_magnitude.text() or 0),
            self.combo_volume_flow_unit.currentText(),
        )
        temp_diff = Quantity(
            float(self.edit_temp_diff_magnitude.text() or 0),
            self.combo_temp_diff_unit.currentText(),
        )
        heat_flow_unit = self.combo_heat_flow_unit.currentText()
        # calculate result
        heat_flow = volume_flow * self.medium.volumetric_heat_capacity * temp_diff
        print("calculating heat flow using Q = V * C * dT:")
        print(
            f"{heat_flow:~P} = "
            f"{volume_flow:~P} * {self.medium.volumetric_heat_capacity:~P} * "
            f"{temp_diff:~P}"
        )
        # write output
        self.edit_heat_flow_magnitude.setText(
            str(heat_flow.to(heat_flow_unit).magnitude)
        )

    def calculate_volume_flow(self) -> None:
        """Calculate volume flow from heat flow and temperature difference.

        Using formula: V = m / rho, m = Q / (cp * dT) and C := rho * cp
        effectively running: V = Q / (C * dT)
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
        volume_flow_unit = self.combo_volume_flow_unit.currentText()
        # calculate result
        volume_flow = heat_flow / (self.medium.volumetric_heat_capacity * temp_diff)
        print("calculating volume flow using V = Q / (C * dT):")
        print(
            f"{volume_flow:~P} = "
            f"{heat_flow:~P} / "
            f"{self.medium.volumetric_heat_capacity:~P} * {temp_diff:~P}"
        )
        # write outputs
        self.edit_volume_flow_magnitude.setText(
            str(volume_flow.to(volume_flow_unit).magnitude)
        )

    def calculate_temperature_difference(self) -> None:
        """Calculate temperature difference from heat flow and volume flow.

        Using: dT = Q / (m * cp), m = V * rho and C:= rho * cp
        effectively running: dt = Q / (V * C)
        """
        # read inputs
        heat_flow = Quantity(
            float(self.edit_heat_flow_magnitude.text() or 0),
            self.combo_heat_flow_unit.currentText(),
        )
        volume_flow = Quantity(
            float(self.edit_volume_flow_magnitude.text() or 0),
            self.combo_volume_flow_unit.currentText(),
        )
        temp_diff_unit = self.combo_temp_diff_unit.currentText()
        # calculate result
        temp_diff = heat_flow / (volume_flow * self.medium.volumetric_heat_capacity)
        print("calculating temperature differenceusing dT = Q / (V * C):")
        print(
            f"{temp_diff:~P} = "
            f"{heat_flow:~P} / "
            f"{volume_flow:~P} * {self.medium.volumetric_heat_capacity:~P}"
        )
        # write output
        self.edit_temp_diff_magnitude.setText(
            str(temp_diff.to(temp_diff_unit).magnitude)
        )

    def calculate_mass_flow(self) -> None:
        """Calculate mass flow from volume flow.

        Using: m = V * rho"""
        # read inputs
        volume_flow = Quantity(
            float(self.edit_volume_flow_magnitude.text() or 0),
            self.combo_volume_flow_unit.currentText(),
        )
        mass_flow_unit = self.combo_mass_flow_unit.currentText()
        # calculate result
        mass_flow = volume_flow * self.medium.density
        print("calculating mass flow using m = V * rho:")
        print(f"{mass_flow:~P} = {volume_flow:~P} * {self.medium.density:~P}")
        # write output
        self.edit_mass_flow_magnitude.setText(
            str(mass_flow.to(mass_flow_unit).magnitude)
        )


def main():
    """Main program."""
    app = QApplication()
    window = QalculatorVolumeWidget()
    window.setWindowTitle("Qalculator Volume")
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
