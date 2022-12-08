"""Fluid Property Selctor GUI"""

import sys

from PySide6.QtCore import QLocale, Qt, Slot
from PySide6.QtGui import QDoubleValidator
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QGridLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QWidget,
)
from pint import Quantity

from mepcalc.common.medium import Medium, media_map
from mepcalc.common.units import Units, units_map


class FluidPropertyWidget(QWidget):
    """Fluid property calculator widget."""

    SHOW_TEXT = "Show Details"
    HIDE_TEXT = "Hide Details"

    def __init__(self, parent=None):
        """initializer."""
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        """Setup user interface."""
        self.create_widgets()
        self.setup_widgets()
        self.setup_layout()
        self.setup_signals_and_slots()
        # initialize ui by calling slot method
        self.fluid_type_or_unit_changed()

    def create_widgets(self):
        """Create widgets for the user interface."""
        self.label_fluid_type = QLabel()
        self.combo_fluid_type = QComboBox()
        self.button_fluid = QPushButton()
        self.label_heat_capacity_name = QLabel()
        self.label_heat_capacity_symbol = QLabel()
        self.edit_heat_capacity_magnitude = QLineEdit()
        self.combo_heat_capacity_unit = QComboBox()
        self.label_density_name = QLabel()
        self.label_density_symbol = QLabel()
        self.edit_density_magnitude = QLineEdit()
        self.combo_density_unit = QComboBox()
        self.label_vol_heat_cap_name = QLabel()
        self.label_vol_heat_cap_symbol = QLabel()
        self.edit_vol_heat_cap_magnitude = QLineEdit()
        self.combo_vol_heat_cap_unit = QComboBox()

    def setup_widgets(self):
        """Setup widgets for the user interface."""
        # Setup double validator
        c_locale = QLocale.c()
        c_locale.setNumberOptions(QLocale.NumberOption.RejectGroupSeparator)
        double_validator = QDoubleValidator()
        double_validator.setLocale(c_locale)
        double_validator.setNotation(QDoubleValidator.Notation.StandardNotation)
        # Fluid Type
        self.label_fluid_type.setText("Fluid")
        for medium in media_map.values():
            self.combo_fluid_type.addItem(medium.name, medium)
        self.combo_fluid_type.addItem(
            "Custom",
            Medium(
                "Custom",
                heat_cap=Quantity(1.0, "kJ/(kg K)"),
                density=Quantity(1.0, "kg/m³"),
            ),
        )
        self.button_fluid.setText("Hide Details")
        # Heat Capacity
        self.label_heat_capacity_name.setText("Heat Cap.")
        self.label_heat_capacity_symbol.setText("cp")
        self.edit_heat_capacity_magnitude.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.edit_heat_capacity_magnitude.setPlaceholderText("Heat Capacity")
        self.edit_heat_capacity_magnitude.setValidator(double_validator)
        self.combo_heat_capacity_unit.addItems(units_map[Units.HeatCapacity])
        # Density Magnitude Line Edit
        self.label_density_name.setText("Density")
        self.label_density_symbol.setText("ϱ")
        self.edit_density_magnitude.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.edit_density_magnitude.setPlaceholderText("Density")
        self.edit_density_magnitude.setValidator(double_validator)
        self.combo_density_unit.addItems(units_map[Units.Density])
        # Volumetric Heat Capacity Magnitude Line Edit
        self.label_vol_heat_cap_name.setText("Vol. Heat Cap.")
        self.label_vol_heat_cap_symbol.setText("C")
        self.edit_vol_heat_cap_magnitude.setDisabled(True)  # always calculated!
        self.edit_vol_heat_cap_magnitude.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.edit_vol_heat_cap_magnitude.setPlaceholderText("Vol. Heat Cap.")
        self.edit_vol_heat_cap_magnitude.setValidator(double_validator)
        self.combo_vol_heat_cap_unit.addItems(units_map[Units.VolumetricHeatCapacity])

    def setup_layout(self):
        """Setup layout of the user interface in a grid.

        row | 0               | 1    | 2     | 3     | 4      |
        col |-----------------|------|-------|-------|--------|
          0 |"Fluid           |      | Combo         | Button |
          1 |"Heat Cap."      | "cp" | Edit  | Combo |        |
          2 |"Density"        | "ϱ"  | Edit  | Combo |        |
          3 |"Vol. Heat Cap." | "C"  | Edit  | Combo |        |
        """
        layout = QGridLayout()
        row = 0  # Fluid Selection
        layout.addWidget(self.label_fluid_type, row, 0)
        layout.addWidget(self.combo_fluid_type, row, 2, 1, 2)
        layout.addWidget(self.button_fluid, row, 4)
        row = 1  # Heat Capacity
        layout.addWidget(self.label_heat_capacity_name, row, 0)
        layout.addWidget(self.label_heat_capacity_symbol, row, 1)
        layout.addWidget(self.edit_heat_capacity_magnitude, row, 2)
        layout.addWidget(self.combo_heat_capacity_unit, row, 3)
        row = 2  # Density
        layout.addWidget(self.label_density_name, row, 0)
        layout.addWidget(self.label_density_symbol, row, 1)
        layout.addWidget(self.edit_density_magnitude, row, 2)
        layout.addWidget(self.combo_density_unit, row, 3)
        row = 3  # Volumetric Heat Capacity
        layout.addWidget(self.label_vol_heat_cap_name, row, 0)
        layout.addWidget(self.label_vol_heat_cap_symbol, row, 1)
        layout.addWidget(self.edit_vol_heat_cap_magnitude, row, 2)
        layout.addWidget(self.combo_vol_heat_cap_unit, row, 3)
        self.setLayout(layout)

    def setup_signals_and_slots(self):
        """Setup signals and slots."""
        # fluid type and units -> read from storage
        self.combo_fluid_type.currentTextChanged.connect(
            self.fluid_type_or_unit_changed
        )
        self.combo_heat_capacity_unit.currentTextChanged.connect(
            self.fluid_type_or_unit_changed
        )
        self.combo_density_unit.currentTextChanged.connect(
            self.fluid_type_or_unit_changed
        )
        self.combo_vol_heat_cap_unit.currentTextChanged.connect(
            self.fluid_type_or_unit_changed
        )
        # custom fluid magnitudes -> write to storage
        self.edit_heat_capacity_magnitude.textEdited.connect(
            self.custom_fluid_properties_changed
        )
        self.edit_density_magnitude.textEdited.connect(
            self.custom_fluid_properties_changed
        )
        # action button -> toggle
        self.button_fluid.clicked.connect(self.details_button_toggled)

    @Slot()
    def fluid_type_or_unit_changed(self):
        """Change fluid type or units slot."""
        # get the update inputs
        fluid_type = self.combo_fluid_type.currentText()
        heat_capacity_unit = self.combo_heat_capacity_unit.currentText()
        density_unit = self.combo_density_unit.currentText()
        # read the values from internal storage (combo box data)
        current_medium = self.combo_fluid_type.currentData()
        heat_capacity = current_medium.heat_capacity
        heat_capacity_value = heat_capacity.to(heat_capacity_unit).magnitude
        density = current_medium.density
        density_value = density.to(density_unit).magnitude
        # write the values to the widgets
        self.edit_heat_capacity_magnitude.setText(str(heat_capacity_value))
        self.edit_density_magnitude.setText(str(density_value))
        # enable line edit inputs for custom fluid type
        if fluid_type == "Custom":
            self.edit_heat_capacity_magnitude.setEnabled(True)
            self.edit_density_magnitude.setEnabled(True)
        else:
            self.edit_heat_capacity_magnitude.setDisabled(True)
            self.edit_density_magnitude.setDisabled(True)
        self.calculate_volumetric_heat_capacity()

    @Slot()
    def custom_fluid_properties_changed(self):
        """Change fluid parameter magnitude slot."""
        self.combo_fluid_type.currentData().heat_capacity = Quantity(
            float(self.edit_heat_capacity_magnitude.text() or 0),
            self.combo_heat_capacity_unit.currentText(),
        )
        self.combo_fluid_type.currentData().density = Quantity(
            float(self.edit_density_magnitude.text() or 0),
            self.combo_density_unit.currentText(),
        )
        self.calculate_volumetric_heat_capacity()

    @Slot()
    def details_button_toggled(self):
        """Details button clicked slot, toggling details visibility."""
        if self.button_fluid.text() == self.SHOW_TEXT:
            self.show_details_widgets()
            self.button_fluid.setText(self.HIDE_TEXT)
        else:  # self.button_fluid.text() == self.HIDE_TEXT
            self.hide_details_widgets()
            self.button_fluid.setText(self.SHOW_TEXT)

    def hide_details_widgets(self):
        """Hide detailed fluid property widgets."""
        self.label_heat_capacity_name.hide()
        self.label_heat_capacity_symbol.hide()
        self.label_density_name.hide()
        self.label_density_symbol.hide()
        self.label_vol_heat_cap_name.hide()
        self.label_vol_heat_cap_symbol.hide()
        self.edit_heat_capacity_magnitude.hide()
        self.combo_heat_capacity_unit.hide()
        self.edit_density_magnitude.hide()
        self.combo_density_unit.hide()
        self.edit_vol_heat_cap_magnitude.hide()
        self.combo_vol_heat_cap_unit.hide()

    def show_details_widgets(self):
        """Show detailed fluid property widgets."""
        self.label_heat_capacity_name.show()
        self.label_heat_capacity_symbol.show()
        self.label_density_name.show()
        self.label_density_symbol.show()
        self.label_vol_heat_cap_name.show()
        self.label_vol_heat_cap_symbol.show()
        self.edit_heat_capacity_magnitude.show()
        self.combo_heat_capacity_unit.show()
        self.edit_density_magnitude.show()
        self.combo_density_unit.show()
        self.edit_vol_heat_cap_magnitude.show()
        self.combo_vol_heat_cap_unit.show()

    def calculate_volumetric_heat_capacity(self):
        """Calculate volumetric heat capacity:

        C = cp * rho.
        """
        heat_capacity = Quantity(
            float(self.edit_heat_capacity_magnitude.text() or 0),
            self.combo_heat_capacity_unit.currentText(),
        )
        density = Quantity(
            float(self.edit_density_magnitude.text() or 0),
            self.combo_density_unit.currentText(),
        )
        vol_heat_cap = heat_capacity * density
        vol_heat_cap_unit = self.combo_vol_heat_cap_unit.currentText()
        self.edit_vol_heat_cap_magnitude.setText(
            str(vol_heat_cap.to(vol_heat_cap_unit).magnitude)
        )


def main():
    """Main program."""
    app = QApplication()
    window = FluidPropertyWidget()
    window.setWindowTitle("Fluid Properties")
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
