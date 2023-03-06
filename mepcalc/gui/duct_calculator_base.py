"""Duct Air Flow Calculator GUI base."""

import sys

from PySide6.QtCore import QLocale
from PySide6.QtGui import QDoubleValidator, Qt
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QRadioButton,
    QLabel,
    QLineEdit,
    QComboBox,
    QFormLayout,
    QHBoxLayout,
    QGridLayout,
)

from mepcalc.common.medium import Medium
from mepcalc.common.units import units_map, Units


# TODO: implement! Extract ABC?
class DuctCalculatorWidget(QWidget):
    """Duct air flow calculator widget."""

    def __init__(self, parent=None, medium: Medium = Medium.air()):
        """Initializer."""
        super().__init__(parent)
        self.medium = medium
        self.setup_ui()

    def setup_ui(self):
        """Setup user interface."""
        # configure and layout widgets
        self.create_widgets()
        self.initialize_widgets()
        self.build_layout()
        self.connect_signals_and_slots()
        # setup calculation fields by calling slots
        # TODO: implement like in the other example?
        # self.output_changed()

    def create_widgets(self):
        """Create widgets."""
        # Radio Buttons
        self.radio_width = QRadioButton()
        self.radio_height = QRadioButton()
        self.radio_diameter = QRadioButton()
        self.radio_area = QRadioButton()
        self.radio_volume_flow = QRadioButton()
        self.radio_mass_flow = QRadioButton()
        self.radio_velocity = QRadioButton()
        # Labels
        self.label_width_name = QLabel()
        self.label_width_symbol = QLabel()
        self.label_height_name = QLabel()
        self.label_height_symbol = QLabel()
        self.label_diameter_name = QLabel()
        self.label_diameter_symbol = QLabel()
        self.label_area_name = QLabel()
        self.label_area_symbol = QLabel()
        self.label_volume_flow_name = QLabel()
        self.label_volume_flow_symbol = QLabel()
        self.label_mass_flow_name = QLabel()
        self.label_mass_flow_symbol = QLabel()
        self.label_velocity_name = QLabel()
        self.label_velocity_symbol = QLabel()
        # Fields
        self.edit_width_magnitude = QLineEdit()
        self.edit_height_magnitude = QLineEdit()
        self.edit_diameter_magnitude = QLineEdit()
        self.edit_area_magnitude = QLineEdit()
        self.edit_volume_flow_magnitude = QLineEdit()
        self.edit_mass_flow_magnitude = QLineEdit()
        self.edit_velocity_magnitude = QLineEdit()
        # Dropdowns
        self.combo_width_unit = QComboBox()
        self.combo_height_unit = QComboBox()
        self.combo_diameter_unit = QComboBox()
        self.combo_area_unit = QComboBox()
        self.combo_volume_flow_unit = QComboBox()
        self.combo_mass_flow_unit = QComboBox()
        self.combo_velocity_unit = QComboBox()

    def initialize_widgets(self) -> None:
        """Setup widgets for the user interface."""
        # Setup double validator
        c_locale = QLocale.c()
        c_locale.setNumberOptions(QLocale.NumberOption.RejectGroupSeparator)
        double_validator = QDoubleValidator()
        double_validator.setLocale(c_locale)
        double_validator.setNotation(QDoubleValidator.Notation.StandardNotation)
        # Radio Buttons
        self.radio_width.setChecked(True)
        self.radio_height.setDisabled(True)
        # Width
        self.label_width_name.setText("Width")
        self.label_width_symbol.setText("w")
        self.edit_width_magnitude.setText("1.0")
        self.edit_width_magnitude.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.edit_width_magnitude.setPlaceholderText("Duct Width")
        self.edit_width_magnitude.setValidator(double_validator)
        self.combo_width_unit.addItems(units_map[Units.Length])
        # Height
        self.label_height_name.setText("Height")
        self.label_height_symbol.setText("h")
        self.edit_height_magnitude.setText("1.0")
        self.edit_height_magnitude.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.edit_height_magnitude.setPlaceholderText("Duct Height")
        self.edit_height_magnitude.setValidator(double_validator)
        self.combo_height_unit.addItems(units_map[Units.Length])
        # Diameter
        self.label_diameter_name.setText("Diameter")
        self.label_diameter_symbol.setText("d")
        self.edit_diameter_magnitude.setText("1.0")
        self.edit_diameter_magnitude.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.edit_diameter_magnitude.setPlaceholderText("Duct Diameter")
        self.edit_diameter_magnitude.setValidator(double_validator)
        self.combo_diameter_unit.addItems(units_map[Units.Length])
        # Cross-section Area
        self.label_area_name.setText("Area")
        self.label_area_symbol.setText("A")
        self.edit_area_magnitude.setText("1.0")
        self.edit_area_magnitude.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.edit_area_magnitude.setPlaceholderText("Cross-section Area")
        self.edit_area_magnitude.setValidator(double_validator)
        self.combo_area_unit.addItems(units_map[Units.Area])
        # Volume Flow
        self.label_volume_flow_name.setText("Volume Flow")
        self.label_volume_flow_symbol.setText("V")
        self.edit_volume_flow_magnitude.setText("1.0")
        self.edit_volume_flow_magnitude.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.edit_volume_flow_magnitude.setPlaceholderText("Volume Flow")
        self.edit_volume_flow_magnitude.setValidator(double_validator)
        self.combo_volume_flow_unit.addItems(units_map[Units.VolumeFlow])
        # Mass Flow
        self.label_mass_flow_name.setText("Mass Flow")
        self.label_mass_flow_symbol.setText("m")
        self.edit_mass_flow_magnitude.setText("1.0")
        self.edit_mass_flow_magnitude.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.edit_mass_flow_magnitude.setPlaceholderText("Mass Flow")
        self.edit_mass_flow_magnitude.setValidator(double_validator)
        self.combo_mass_flow_unit.addItems(units_map[Units.MassFlow])
        # Velocity
        self.label_velocity_name.setText("Velocity")
        self.label_velocity_symbol.setText("v")
        self.edit_velocity_magnitude.setText("1.0")
        self.edit_velocity_magnitude.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.edit_velocity_magnitude.setPlaceholderText("Flow Velocity")
        self.edit_velocity_magnitude.setValidator(double_validator)
        self.combo_velocity_unit.addItems(units_map[Units.Velocity])

    def build_layout(self) -> None:
        """Setup layout of the user interface in a grid.

        col | 0     | 1           | 2 | 3    | 4     |
        row |-------|-------------|---|------|-------|
          0 | Radio | Width       | w | Edit | Combo |
          1 | Radio | Height      | h | Edit | Combo |
          2 | Radio | Diameter    | d | Edit | Combo |
          3 | Radio | Area        | A | Edit | Combo |
          4 | Radio | Volume Flow | V | Edit | Combo |
          5 | Radio | Mass Flow   | m | Edit | Combo |
          6 | Radio | Velocity    | v | Edit | Combo |
        """
        layout = QGridLayout()
        row = 0  # Width
        layout.addWidget(self.radio_width, row, 0)
        layout.addWidget(self.label_width_name, row, 1)
        layout.addWidget(self.label_width_symbol, row, 2)
        layout.addWidget(self.edit_width_magnitude, row, 3)
        layout.addWidget(self.combo_width_unit, row, 4)
        row = 1  # Height
        layout.addWidget(self.radio_height, row, 0)
        layout.addWidget(self.label_height_name, row, 1)
        layout.addWidget(self.label_height_symbol, row, 2)
        layout.addWidget(self.edit_height_magnitude, row, 3)
        layout.addWidget(self.combo_height_unit, row, 4)
        row = 2  # Diameter
        layout.addWidget(self.radio_diameter, row, 0)
        layout.addWidget(self.label_diameter_name, row, 1)
        layout.addWidget(self.label_diameter_symbol, row, 2)
        layout.addWidget(self.edit_diameter_magnitude, row, 3)
        layout.addWidget(self.combo_diameter_unit, row, 4)
        row = 3  # Cross-section Area
        layout.addWidget(self.radio_area, row, 0)
        layout.addWidget(self.label_area_name, row, 1)
        layout.addWidget(self.label_area_symbol, row, 2)
        layout.addWidget(self.edit_area_magnitude, row, 3)
        layout.addWidget(self.combo_area_unit, row, 4)
        row = 4  # Volume Flow
        layout.addWidget(self.radio_volume_flow, row, 0)
        layout.addWidget(self.label_volume_flow_name, row, 1)
        layout.addWidget(self.label_volume_flow_symbol, row, 2)
        layout.addWidget(self.edit_volume_flow_magnitude, row, 3)
        layout.addWidget(self.combo_volume_flow_unit, row, 4)
        row = 5  # Mass Flow
        layout.addWidget(self.radio_mass_flow, row, 0)
        layout.addWidget(self.label_mass_flow_name, row, 1)
        layout.addWidget(self.label_mass_flow_symbol, row, 2)
        layout.addWidget(self.edit_mass_flow_magnitude, row, 3)
        layout.addWidget(self.combo_mass_flow_unit, row, 4)
        row = 6  # Velocity
        layout.addWidget(self.radio_velocity, row, 0)
        layout.addWidget(self.label_velocity_name, row, 1)
        layout.addWidget(self.label_velocity_symbol, row, 2)
        layout.addWidget(self.edit_velocity_magnitude, row, 3)
        layout.addWidget(self.combo_velocity_unit, row, 4)
        self.setLayout(layout)

    def connect_signals_and_slots(self) -> None:
        """Connect signals to slots."""
        ...


def main():
    """Main program."""
    app = QApplication()
    window = DuctCalculatorWidget()
    window.setWindowTitle("Duct Calculator Base")
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
