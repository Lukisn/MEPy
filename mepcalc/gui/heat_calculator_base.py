"""Heat Flow Calculator GUI base."""

import sys
from typing import List

from PySide6.QtCore import QLocale, Qt, Slot
from PySide6.QtGui import QDoubleValidator
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QGridLayout,
    QLabel,
    QLineEdit,
    QRadioButton,
    QWidget,
)

from mepcalc.common.medium import Medium
from mepcalc.common.units import Units, units_map


# TODO: debug double calculation on changed output
# outputs changed is triggered twice because one radio button is switched off
# when another one is switched on
# https://stackoverflow.com/questions/58780920/can-i-get-a-signal-from-a-qgroupbox-when-one-of-the-radiobuttons-in-it-is-change
class HeatCalculatorWidget(QWidget):
    """Heat flow from mass flow calculator widget."""

    def __init__(self, parent=None, medium: Medium = Medium.water()) -> None:
        """Initializer."""
        # print("initializing")
        super().__init__(parent)
        self.medium = medium
        self.permanently_disabled: List[QWidget] = []
        self.setup_ui()

    def setup_ui(self) -> None:
        """Setup user interface"""
        # print("setting up ui")
        # configure and layout widgets
        self.create_widgets()
        self.initialize_widgets()
        self.build_layout()
        self.connect_signals_and_slots()
        # setup calculation fields by calling slots by hand
        self.output_changed(checked=True)

    def create_widgets(self) -> None:
        """Create widgets."""
        # print("creating widgets")
        # Radio Buttons
        self.radio_heat_flow = QRadioButton()
        self.radio_mass_flow = QRadioButton()
        self.radio_volume_flow = QRadioButton()
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

    def initialize_widgets(self) -> None:
        """Setup widgets for the user interface."""
        # print("initializing widgets")
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
        # Volume Flow
        self.label_volume_flow_name.setText("Volume Flow")
        self.label_volume_flow_symbol.setText("V")
        self.edit_volume_flow_magnitude.setText("1.0")
        self.edit_volume_flow_magnitude.setPlaceholderText("Volume Flow")
        self.edit_volume_flow_magnitude.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.edit_volume_flow_magnitude.setValidator(double_validator)
        self.combo_volume_flow_unit.addItems(units_map[Units.VolumeFlow])
        # Temperature Difference
        self.label_temp_diff_name.setText("Temp. Diff.")
        self.label_temp_diff_symbol.setText("𝛥T")
        self.edit_temp_diff_magnitude.setText("1.0")
        self.edit_temp_diff_magnitude.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.edit_temp_diff_magnitude.setPlaceholderText("Temp. Diff.")
        self.edit_temp_diff_magnitude.setValidator(double_validator)
        self.combo_temp_diff_unit.addItems(units_map[Units.TemperatureDifference])

    def build_layout(self) -> None:
        """Setup layout of the user interface in a grid.

        col | 0     | 1           | 2  | 3    | 4     |
        row |-------|-------------|----|------|-------|
          0 | Radio | Heat Flow   | Q  | Edit | Combo |
          1 | Radio | Mass Flow   | m  | Edit | Combo |
          2 | Radio | Volume Flow | V  | Edit | Combo |
          3 | Radio | Temp. Diff. | dT | Edit | Combo |
        """
        # print("building layout")
        layout = QGridLayout()
        row = 0  # Heat Flow
        layout.addWidget(self.radio_heat_flow, row, 0)
        layout.addWidget(self.label_heat_flow_name, row, 1)
        layout.addWidget(self.label_heat_flow_symbol, row, 2)
        layout.addWidget(self.edit_heat_flow_magnitude, row, 3)
        layout.addWidget(self.combo_heat_flow_unit, row, 4)
        row = 1  # Mass Flow
        layout.addWidget(self.radio_mass_flow, row, 0)
        layout.addWidget(self.label_mass_flow_name, row, 1)
        layout.addWidget(self.label_mass_flow_symbol, row, 2)
        layout.addWidget(self.edit_mass_flow_magnitude, row, 3)
        layout.addWidget(self.combo_mass_flow_unit, row, 4)
        row = 2  # Volume Flow
        layout.addWidget(self.radio_volume_flow, row, 0)
        layout.addWidget(self.label_volume_flow_name, row, 1)
        layout.addWidget(self.label_volume_flow_symbol, row, 2)
        layout.addWidget(self.edit_volume_flow_magnitude, row, 3)
        layout.addWidget(self.combo_volume_flow_unit, row, 4)
        row = 3  # Temperature Difference
        layout.addWidget(self.radio_temp_diff, row, 0)
        layout.addWidget(self.label_temp_diff_name, row, 1)
        layout.addWidget(self.label_temp_diff_symbol, row, 2)
        layout.addWidget(self.edit_temp_diff_magnitude, row, 3)
        layout.addWidget(self.combo_temp_diff_unit, row, 4)
        self.setLayout(layout)

    def connect_signals_and_slots(self) -> None:
        """Connect signals to slots."""
        # print("connecting signals and slots")
        # radio buttons -> calculation output changed -> recalculate
        self.radio_heat_flow.toggled.connect(self.output_changed)
        self.radio_mass_flow.toggled.connect(self.output_changed)
        self.radio_volume_flow.toggled.connect(self.output_changed)
        self.radio_temp_diff.toggled.connect(self.output_changed)
        # magnitudes and units -> inputs changed -> recalculate
        self.edit_heat_flow_magnitude.textEdited.connect(self.inputs_changed)
        self.combo_heat_flow_unit.currentTextChanged.connect(self.inputs_changed)
        self.edit_mass_flow_magnitude.textEdited.connect(self.inputs_changed)
        self.combo_mass_flow_unit.currentTextChanged.connect(self.inputs_changed)
        self.edit_volume_flow_magnitude.textEdited.connect(self.inputs_changed)
        self.combo_volume_flow_unit.currentTextChanged.connect(self.inputs_changed)
        self.edit_temp_diff_magnitude.textEdited.connect(self.inputs_changed)
        self.combo_temp_diff_unit.currentTextChanged.connect(self.inputs_changed)

    @Slot()
    def output_changed(self, checked=False) -> None:
        """Set output to: heat flow, fluid flow or temperature difference."""
        # print(f"output changed triggered by {self.sender()} checked = {checked}")
        if not checked:
            # print("returning")
            return
        # enable all line edit fields
        self.edit_heat_flow_magnitude.setEnabled(True)
        self.edit_mass_flow_magnitude.setEnabled(True)
        self.edit_volume_flow_magnitude.setEnabled(True)
        self.edit_temp_diff_magnitude.setEnabled(True)
        # disable permanently disabled widgets
        for widget in self.permanently_disabled:
            widget.setDisabled(True)
        # disable current output field
        if self.radio_heat_flow.isChecked():
            self.edit_heat_flow_magnitude.setDisabled(True)
        elif self.radio_mass_flow.isChecked():
            self.edit_mass_flow_magnitude.setDisabled(True)
        elif self.radio_volume_flow.isChecked():
            self.edit_volume_flow_magnitude.setDisabled(True)
        else:  # self.radio_temperature_difference.isChecked():
            self.edit_temp_diff_magnitude.setDisabled(True)
        # call inputs_changed run calculation
        self.inputs_changed()

    @Slot()
    def inputs_changed(self) -> None:
        """Recalculate on changed inputs."""
        # print(f"inputs changed triggered by {self.sender()}")
        if self.radio_heat_flow.isChecked():
            self.calculate_heat_flow()
        elif self.radio_mass_flow.isChecked():
            self.calculate_mass_flow()
        elif self.radio_volume_flow.isChecked():
            self.calculate_volume_flow()
        else:  # self.radio_temperature_difference.isChecked():
            self.calculate_temperature_difference()

    def permanently_disable(self, widget: QWidget) -> None:
        """Permanently disable widget."""
        self.permanently_disabled.append(widget)

    def enable_all(self) -> None:
        """Enable all previously permanently disabled widgets."""
        self.permanently_disabled.clear()

    def calculate_heat_flow(self) -> None:
        """Calculate heat flow."""
        print("calculating heat flow")

    def calculate_mass_flow(self) -> None:
        """Calculate mass flow."""
        print("calculating mass flow")

    def calculate_volume_flow(self) -> None:
        """Calculate volume flow."""
        print("calculating volume flow")

    def calculate_temperature_difference(self) -> None:
        """Calculate temperature difference."""
        print("calculating temperature difference")


def main():
    """Main program."""
    app = QApplication()
    window = HeatCalculatorWidget()
    window.setWindowTitle("Heat Flow Calculator Base")
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
