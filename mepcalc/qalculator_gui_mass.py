"""Heat Flow Calculator GUI, using mass flow based formula."""
# TODO: clean up code

import sys

from medium import Medium
from pint import Quantity
from PySide6.QtCore import QLocale, Qt, Slot
from PySide6.QtGui import QDoubleValidator
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QGridLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QRadioButton,
    QWidget,
)
from units import Units, units_map


class QalculatorMassWidget(QWidget):
    """Heat flow from mass flow calculator widget."""

    def __init__(self, parent=None, medium: Medium = Medium.water()) -> None:
        """initializer."""
        super().__init__(parent)
        self.medium = medium
        self.setup_ui()

    def setup_ui(self):
        """Setup user interface"""
        # configure and layout widgets
        self.create_widgets()
        self.initialize_widgets()
        self.setup_layout()
        self.setup_signals_and_slots()
        # setup calculation fields by calling slots
        self.radio_output_selection_changed()

    def create_widgets(self):
        """Create widgets."""
        # Radio Buttons
        self.radio_heat_flow = QRadioButton()
        self.radio_fluid_flow = QRadioButton()
        self.radio_temp_diff = QRadioButton()
        # Labels
        self.label_heat_flow_name = QLabel()
        self.label_heat_flow_symbol = QLabel()
        self.label_mass_flow_name = QLabel()
        self.label_mass_flow_symbol = QLabel()
        self.label_volume_flow_name = QLabel()
        self.label_volume_flow_symbol = QLabel()
        self.label_temp_diff_name = QLabel()
        self.label_temp_diff_symbol = QLabel()
        # Fields
        self.edit_heat_flow_magnitude = QLineEdit()
        self.edit_mass_flow_magnitude = QLineEdit()
        self.edit_volume_flow_magnitude = QLineEdit()
        self.edit_temp_diff_magnitude = QLineEdit()
        # Dropdowns
        self.combo_heat_flow_unit = QComboBox()
        self.combo_mass_flow_unit = QComboBox()
        self.combo_volume_flow_unit = QComboBox()
        self.combo_temp_diff_unit = QComboBox()
        # Buttons
        self.button_mass_flow_action = QPushButton()
        self.button_volume_flow_action = QPushButton()

    def initialize_widgets(self):
        """Setup widgets for the user interface."""
        # Setup double validator
        c_locale = QLocale.c()
        c_locale.setNumberOptions(QLocale.NumberOption.RejectGroupSeparator)
        double_validator = QDoubleValidator()
        double_validator.setLocale(c_locale)
        double_validator.setNotation(QDoubleValidator.Notation.StandardNotation)
        # Radio Buttons
        self.radio_heat_flow.setChecked(True)
        # Heat Flow
        self.label_heat_flow_name.setText("Heat Flow")
        self.label_heat_flow_symbol.setText("Q")
        self.edit_heat_flow_magnitude.setText("1.0")
        self.edit_heat_flow_magnitude.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.edit_heat_flow_magnitude.setPlaceholderText("Heat Flow")
        self.edit_heat_flow_magnitude.setValidator(double_validator)
        self.combo_heat_flow_unit.addItems(units_map[Units.HeatFlow])
        # Mass Flow
        self.label_mass_flow_name.setText("Mass Flow")
        self.label_mass_flow_symbol.setText("m")
        self.edit_mass_flow_magnitude.setText("1.0")
        self.edit_mass_flow_magnitude.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.edit_mass_flow_magnitude.setPlaceholderText("Mass Flow")
        self.edit_mass_flow_magnitude.setValidator(double_validator)
        self.combo_mass_flow_unit.addItems(units_map[Units.MassFlow])
        self.button_mass_flow_action.setText("Action")
        # Volume Flow
        self.label_volume_flow_name.setText("Volume Flow")
        self.label_volume_flow_symbol.setText("V")
        self.edit_volume_flow_magnitude.setText("1.0")
        self.edit_volume_flow_magnitude.setDisabled(True)
        self.edit_volume_flow_magnitude.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.combo_volume_flow_unit = QComboBox()
        self.combo_volume_flow_unit.addItems(units_map[Units.VolumeFlow])
        self.button_volume_flow_action.setText("Action")
        # Temperature Difference
        self.label_temp_diff_name.setText("Temp. Diff.")
        self.label_temp_diff_symbol.setText("𝛥T")
        self.edit_temp_diff_magnitude.setText("1.0")
        self.edit_temp_diff_magnitude.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.edit_temp_diff_magnitude.setPlaceholderText("Temp. Diff.")
        self.edit_temp_diff_magnitude.setValidator(double_validator)
        self.combo_temp_diff_unit.addItems(units_map[Units.TemperatureDifference])

    def setup_layout(self):
        """Setup layout of the user interface in a grid.

        col | 0     | 1           | 2  | 3    | 4     | 5      |
        row |-------|-------------|----|------|-------|--------|
          0 | Radio | Heat Flow   | Q  | Edit | Combo |        |
          1 | Radio | Mass Flow   | m  | Edit | Combo | Button |
          2 |       | Volume Flow | V  | Edit | Combo | Button |
          3 | Radio | Temp. Diff. | dT | Edit | Combo |        |
        """
        layout = QGridLayout()
        row = 0  # Heat Flow
        layout.addWidget(self.radio_heat_flow, row, 0)
        layout.addWidget(self.label_heat_flow_name, row, 1)
        layout.addWidget(self.label_heat_flow_symbol, row, 2)
        layout.addWidget(self.edit_heat_flow_magnitude, row, 3)
        layout.addWidget(self.combo_heat_flow_unit, row, 4)
        row = 1  # Mass Flow
        layout.addWidget(self.radio_fluid_flow, row, 0)
        layout.addWidget(self.label_mass_flow_name, row, 1)
        layout.addWidget(self.label_mass_flow_symbol, row, 2)
        layout.addWidget(self.edit_mass_flow_magnitude, row, 3)
        layout.addWidget(self.combo_mass_flow_unit, row, 4)
        layout.addWidget(self.button_mass_flow_action, row, 5)
        row = 2  # Volume Flow
        layout.addWidget(self.label_volume_flow_name, row, 1)
        layout.addWidget(self.label_volume_flow_symbol, row, 2)
        layout.addWidget(self.edit_volume_flow_magnitude, row, 3)
        layout.addWidget(self.combo_volume_flow_unit, row, 4)
        layout.addWidget(self.button_volume_flow_action, row, 5)
        row = 3  # Temperature Difference
        layout.addWidget(self.radio_temp_diff, row, 0)
        layout.addWidget(self.label_temp_diff_name, row, 1)
        layout.addWidget(self.label_temp_diff_symbol, row, 2)
        layout.addWidget(self.edit_temp_diff_magnitude, row, 3)
        layout.addWidget(self.combo_temp_diff_unit, row, 4)
        self.setLayout(layout)

    def setup_signals_and_slots(self):
        """Setup signals and slots"""
        # radio buttons -> calculation target
        self.radio_heat_flow.toggled.connect(self.radio_output_selection_changed)
        self.radio_fluid_flow.toggled.connect(self.radio_output_selection_changed)
        self.radio_temp_diff.toggled.connect(self.radio_output_selection_changed)
        # magnitudes and units -> recalculate
        self.edit_heat_flow_magnitude.textEdited.connect(self.inputs_changed)
        self.combo_heat_flow_unit.currentTextChanged.connect(self.inputs_changed)
        self.edit_mass_flow_magnitude.textEdited.connect(self.inputs_changed)
        self.combo_mass_flow_unit.currentTextChanged.connect(self.inputs_changed)
        self.edit_volume_flow_magnitude.textEdited.connect(self.inputs_changed)
        self.combo_volume_flow_unit.currentTextChanged.connect(self.inputs_changed)
        self.edit_temp_diff_magnitude.textEdited.connect(self.inputs_changed)
        self.combo_temp_diff_unit.currentTextChanged.connect(self.inputs_changed)

    @Slot()
    def radio_output_selection_changed(self):
        """Set output variable: heat flow, fluid flow or temperature difference."""
        # enable all line edit fields
        self.edit_heat_flow_magnitude.setEnabled(True)
        self.edit_mass_flow_magnitude.setEnabled(True)
        self.edit_temp_diff_magnitude.setEnabled(True)
        # diasble current output field
        if self.radio_heat_flow.isChecked():
            self.edit_heat_flow_magnitude.setDisabled(True)
        elif self.radio_fluid_flow.isChecked():
            self.edit_mass_flow_magnitude.setDisabled(True)
        else:  # self.radio_temperature_difference.isChecked():
            self.edit_temp_diff_magnitude.setDisabled(True)
        # call inputs_changed run calculation
        self.inputs_changed()

    @Slot()
    def inputs_changed(self):
        """Recalculate on changed inputs slot."""
        if self.radio_heat_flow.isChecked():
            self.calculate_heat_flow()
        elif self.radio_fluid_flow.isChecked():
            self.calculate_mass_flow()
        else:  # self.radio_temperature_difference.isChecked():
            self.calculate_temperature_difference()
        self.calculate_volume_flow()

    def calculate_heat_flow(self):
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

    def calculate_mass_flow(self):
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

    def calculate_volume_flow(self):
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

    def calculate_temperature_difference(self):
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


def main():
    """Main program."""
    app = QApplication()
    window = QalculatorMassWidget()
    window.setWindowTitle("Qalculator Mass")
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
