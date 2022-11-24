"""Original Heat Flow Calculator GUI.

All in one widget with complicated logic for the different calculation paths.
"""

import sys

from pint import UnitRegistry
from PySide6.QtCore import QLocale, Qt, Slot
from PySide6.QtGui import QDoubleValidator
from PySide6.QtWidgets import (
    QApplication,
    QButtonGroup,
    QComboBox,
    QGridLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QRadioButton,
    QWidget,
)

ureg = UnitRegistry()


class QalculatorWidget(QWidget):
    """Heat flow calculator widget"""

    units = {  # TODO: refactor this using less har dcoded strings
        "heat_capacity": ["kJ/(kg K)", "J/(kg K)"],
        "density": ["kg/m³", "kg/dm³", "kg/cm³", "g/m³", "g/dm³", "g/cm³"],
        "heat_flow": ["kW", "W", "MW", "kWh/s", "Wh/s", "MWh/s"],
        "mass_flow": ["kg/s", "kg/min", "kg/h", "g/s", "g/min", "g/s"],
        "volume_flow": ["m³/h", "m³/min", "m³/s", "l/h", "l/min", "l/s"],
        "temperature_difference": ["K"],
    }

    fluids = {  # TODO: refactor this to make it more convenient to use
        "Water": {
            "heat_capacity": ureg.Quantity(4148.0, "kJ/(kg K)"),
            # https://www.wolframalpha.com/input?i=water+specific+heat+capacity+at+20+°C
            "density": ureg.Quantity(998.2, "kg/m³")
            # https://www.wolframalpha.com/input?i=water+density+at+20+°C
        },
        "Air": {
            "heat_capacity": ureg.Quantity(1006.0, "kJ/(kg K)"),
            # https://www.wolframalpha.com/input?i=air+specific+heat+capacity+at+20+°C
            "density": ureg.Quantity(1.205, "kg/m³")
            # https://www.wolframalpha.com/input?i=air+density+at+20+°C
        },
        "Custom": {
            "heat_capacity": ureg.Quantity(1.0, "kJ/(kg K)"),
            "density": ureg.Quantity(1.0, "kg/m³"),
        },
    }

    def __init__(self, parent=None):
        """initializer"""
        super().__init__(parent)
        self.setWindowTitle("Qalculator")
        self.setup_ui()

    def setup_ui(self):
        """Setup user interface"""
        # configure and layout widgets
        self.setup_widgets()
        self.setup_layout()
        # hook up signals and slots
        self.setup_signals_and_slots()
        # setup fluid property fields by calling slot
        self.fluid_type_or_unit_changed()
        # setup calculation fields by calling slots
        self.radio_output_selection_changed()
        self.radio_input_selection_changed()

    def setup_widgets(self):
        """Setup widgets for the user interface"""
        # Setup double validator
        c_locale = QLocale.c()
        c_locale.setNumberOptions(QLocale.NumberOption.RejectGroupSeparator)
        double_validator = QDoubleValidator()
        double_validator.setLocale(c_locale)
        double_validator.setNotation(QDoubleValidator.Notation.StandardNotation)
        # Fluid Section
        # Fluid Type
        self.combo_fluid_type = QComboBox()
        self.combo_fluid_type.addItem("Water")
        self.combo_fluid_type.addItem("Air")
        self.combo_fluid_type.addItem("Custom")
        self.button_fluid = QPushButton("Details")
        # Heat Capacity
        self.edit_heat_capacity_magnitude = QLineEdit()
        self.edit_heat_capacity_magnitude.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.edit_heat_capacity_magnitude.setPlaceholderText("Heat Capacity")
        self.edit_heat_capacity_magnitude.setValidator(double_validator)
        self.combo_heat_capacity_unit = QComboBox()
        self.combo_heat_capacity_unit.addItems(self.units["heat_capacity"])
        # Density
        self.edit_density_magnitude = QLineEdit()
        self.edit_density_magnitude.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.edit_density_magnitude.setPlaceholderText("Density")
        self.edit_density_magnitude.setValidator(double_validator)
        self.combo_density_unit = QComboBox()
        self.combo_density_unit.addItems(self.units["density"])
        # Heat Flow Section
        # Radio Buttons
        # Calculation Output Target Group
        self.radio_output_heat_flow = QRadioButton()
        self.radio_output_heat_flow.setChecked(True)  # initial calculation target
        self.radio_output_fluid_flow = QRadioButton()
        self.radio_output_temp_diff = QRadioButton()
        radio_group_calculation_output = QButtonGroup()
        radio_group_calculation_output.addButton(self.radio_output_heat_flow)
        radio_group_calculation_output.addButton(self.radio_output_fluid_flow)
        radio_group_calculation_output.addButton(self.radio_output_temp_diff)
        # Fluid Flow Input Target Group
        self.radio_input_mass_flow = QRadioButton()
        self.radio_input_mass_flow.setChecked(True)  # initial fluid flow target
        self.radio_input_volume_flow = QRadioButton()
        radio_group_fluid_flow_target = QButtonGroup()
        radio_group_fluid_flow_target.addButton(self.radio_input_mass_flow)
        radio_group_fluid_flow_target.addButton(self.radio_input_volume_flow)
        # Heat Flow
        self.edit_heat_flow_magnitude = QLineEdit("1.0")
        self.edit_heat_flow_magnitude.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.edit_heat_flow_magnitude.setPlaceholderText("Heat Flow")
        self.edit_heat_flow_magnitude.setValidator(double_validator)
        self.combo_heat_flow_unit = QComboBox()
        self.combo_heat_flow_unit.addItems(self.units["heat_flow"])
        # Mass Flow
        self.edit_mass_flow_magnitude = QLineEdit("1.0")
        self.edit_mass_flow_magnitude.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.edit_mass_flow_magnitude.setPlaceholderText("Mass Flow")
        self.edit_mass_flow_magnitude.setValidator(double_validator)
        self.combo_mass_flow_unit = QComboBox()
        self.combo_mass_flow_unit.addItems(self.units["mass_flow"])
        self.button_mass_flow_action = QPushButton("Action")
        # Volume Flow
        self.edit_volume_flow_magnitude = QLineEdit("1.0")
        self.edit_volume_flow_magnitude.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.edit_volume_flow_magnitude.setPlaceholderText("Volume Flow")
        self.edit_volume_flow_magnitude.setValidator(double_validator)
        self.combo_volume_flow_unit = QComboBox()
        self.combo_volume_flow_unit.addItems(self.units["volume_flow"])
        self.button_volume_flow = QPushButton("Action")
        # Temperature Difference
        self.edit_temp_diff_magnitude = QLineEdit("1.0")
        self.edit_temp_diff_magnitude.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.edit_temp_diff_magnitude.setPlaceholderText("Temp. Diff.")
        self.edit_temp_diff_magnitude.setValidator(double_validator)
        self.combo_temp_diff_unit = QComboBox()
        self.combo_temp_diff_unit.addItems(self.units["temperature_difference"])

    def setup_layout(self):
        """Setup layout of the user interface in a grid"""
        layout = QGridLayout()
        # 0 - Radio, 1 - Radio, 2 - Name, 3 - Symbol, 4 - Edit, 5 - Combo, 6 - Button
        # row 0: Fluid Header
        layout.addWidget(QLabel("Fluid Properties"), 0, 0, 1, 7)
        # row 1: Fluid Selection
        layout.addWidget(QLabel("Fluid"), 1, 2, 1, 2)
        layout.addWidget(self.combo_fluid_type, 1, 4, 1, 2)
        layout.addWidget(self.button_fluid, 1, 6)
        # row 2: Heat Capacity
        layout.addWidget(QLabel("Heat Capacity"), 2, 2)
        layout.addWidget(QLabel("cp"), 2, 3)
        layout.addWidget(self.edit_heat_capacity_magnitude, 2, 4)
        layout.addWidget(self.combo_heat_capacity_unit, 2, 5)
        # row 3: Density
        layout.addWidget(QLabel("Density"), 3, 2)
        layout.addWidget(QLabel("ϱ"), 3, 3)
        layout.addWidget(self.edit_density_magnitude, 3, 4)
        layout.addWidget(self.combo_density_unit, 3, 5)
        # row 4: Flow Header
        layout.addWidget(QLabel("Flow Properties"), 4, 0, 1, 7)
        # row 5: Heat Flow
        layout.addWidget(self.radio_output_heat_flow, 5, 0)
        layout.addWidget(QLabel("Heat Flow"), 5, 2)
        layout.addWidget(QLabel("Q"), 5, 3)
        layout.addWidget(self.edit_heat_flow_magnitude, 5, 4)
        layout.addWidget(self.combo_heat_flow_unit, 5, 5)
        # row 6: Mass Flow
        layout.addWidget(self.radio_output_fluid_flow, 6, 0)
        layout.addWidget(self.radio_input_mass_flow, 6, 1)
        layout.addWidget(QLabel("Mass Flow"), 6, 2)
        layout.addWidget(QLabel("m"), 6, 3)
        layout.addWidget(self.edit_mass_flow_magnitude, 6, 4)
        layout.addWidget(self.combo_mass_flow_unit, 6, 5)
        layout.addWidget(self.button_mass_flow_action, 6, 6)
        # row 7: Volume Flow
        layout.addWidget(self.radio_input_volume_flow, 7, 1)
        layout.addWidget(QLabel("Volume Flow"), 7, 2)
        layout.addWidget(QLabel("V"), 7, 3)
        layout.addWidget(self.edit_volume_flow_magnitude, 7, 4)
        layout.addWidget(self.combo_volume_flow_unit, 7, 5)
        layout.addWidget(self.button_volume_flow, 7, 6)
        # row 8: Temperature Difference
        layout.addWidget(self.radio_output_temp_diff, 8, 0)
        layout.addWidget(QLabel("Temp. Diff."), 8, 2)
        layout.addWidget(QLabel("ΔT"), 8, 3)
        layout.addWidget(self.edit_temp_diff_magnitude, 8, 4)
        layout.addWidget(self.combo_temp_diff_unit, 8, 5)
        self.setLayout(layout)

    def setup_signals_and_slots(self):
        """Setup signals and slots"""
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
        # custom fluid magnitudes -> write to storage
        self.edit_heat_capacity_magnitude.textEdited.connect(
            self.custom_fluid_properties_changed
        )
        self.edit_density_magnitude.textEdited.connect(
            self.custom_fluid_properties_changed
        )
        # radio buttons -> calculation target
        self.radio_output_heat_flow.toggled.connect(self.radio_output_selection_changed)
        self.radio_output_fluid_flow.toggled.connect(
            self.radio_output_selection_changed
        )
        self.radio_output_temp_diff.toggled.connect(self.radio_output_selection_changed)
        # radio buttons -> calculation input
        self.radio_input_mass_flow.toggled.connect(self.radio_input_selection_changed)
        self.radio_input_volume_flow.toggled.connect(self.radio_input_selection_changed)
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
    def fluid_type_or_unit_changed(self):
        """Change fluid type or units slot"""
        # get the update inputs
        fluid_type = self.combo_fluid_type.currentText()
        heat_capacity_unit = self.combo_heat_capacity_unit.currentText()
        density_unit = self.combo_density_unit.currentText()
        # read the values from internal storage
        heat_capacity = self.fluids[fluid_type]["heat_capacity"]
        heat_capacity_value = heat_capacity.to(heat_capacity_unit).magnitude
        density = self.fluids[fluid_type]["density"]
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
        # trigger recalculation
        self.inputs_changed()

    @Slot()
    def custom_fluid_properties_changed(self):
        """Change fluid parameter magnitude slot"""
        # read updated magnitude and unit values
        heat_capacity_unit = self.combo_heat_capacity_unit.currentText()
        heat_capacity_magnitude = float(self.edit_heat_capacity_magnitude.text() or 0)
        density_unit = self.combo_density_unit.currentText()
        density_magnitude = float(self.edit_density_magnitude.text() or 0)
        # write updated value to storage
        self.fluids["Custom"]["heat_capacity"] = ureg.Quantity(
            heat_capacity_magnitude, heat_capacity_unit
        )
        self.fluids["Custom"]["density"] = ureg.Quantity(
            density_magnitude, density_unit
        )
        # trigger recalculation
        self.inputs_changed()

    @Slot()
    def radio_output_selection_changed(self):
        """Set output variable: heat flow, fluid flow or temperature difference"""
        print(f"output radio button toggled: {self.sender()}")
        # enable all line edit fields
        self.edit_heat_flow_magnitude.setEnabled(True)
        self.edit_mass_flow_magnitude.setEnabled(True)
        self.edit_volume_flow_magnitude.setEnabled(True)
        self.edit_temp_diff_magnitude.setEnabled(True)
        # enable input radio fields
        self.radio_input_mass_flow.setEnabled(True)
        self.radio_input_volume_flow.setEnabled(True)
        # diasble current output field
        if self.radio_output_heat_flow.isChecked():
            self.edit_heat_flow_magnitude.setDisabled(True)
        elif self.radio_output_fluid_flow.isChecked():
            self.edit_mass_flow_magnitude.setDisabled(True)
            self.edit_volume_flow_magnitude.setDisabled(True)
            # also disable input radio buttons since fluid flow is not the output
            self.radio_input_mass_flow.setDisabled(True)
            self.radio_input_volume_flow.setDisabled(True)
        else:  # self.radio_temperature_difference.isChecked():
            self.edit_temp_diff_magnitude.setDisabled(True)
        # call radio_input_selection_changed to update and run calculation
        self.radio_input_selection_changed()

    @Slot()
    def radio_input_selection_changed(self):
        """Set input variable: mass flow or volume flow"""
        print(f"input radio button toggled: {self.sender()}")
        if not self.radio_output_fluid_flow.isChecked():
            # disable al line edit fields
            self.edit_mass_flow_magnitude.setDisabled(True)
            self.edit_volume_flow_magnitude.setDisabled(True)
            # enable current input field
            if self.radio_input_mass_flow.isChecked():
                self.edit_mass_flow_magnitude.setEnabled(True)
            else:  # self.radio_volume_flow.isChecked():
                self.edit_volume_flow_magnitude.setEnabled(True)
        # call inputs_changed to run calculation
        self.inputs_changed()

    @Slot()
    def inputs_changed(self):
        print(f"input changed: {self.sender()}")
        if self.radio_output_heat_flow.isChecked():
            if self.radio_input_mass_flow.isChecked():
                self.calculate_volume_flow_from_mass_flow()
                self.calculate_heat_flow_from_mass_flow()
            else:  # self.radio_volume_flow.isChecked():
                self.calculate_mass_flow_from_volume_flow()
                self.calculate_heat_flow_from_volume_flow()
        elif self.radio_output_fluid_flow.isChecked():
            self.calculate_mass_flow_from_heat_flow_and_temperature_difference()
            self.calculate_volume_flow_from_mass_flow()
        else:  # self.radio_temperature_difference.isChecked():
            if self.radio_input_mass_flow.isChecked():
                self.calculate_volume_flow_from_mass_flow()
                self.calculate_temperature_difference_from_mass_flow()
            else:  # self.radio_volume_flow.isChecked():
                self.calculate_mass_flow_from_volume_flow()
                self.calculate_temperature_difference_from_volume_flow()

    def calculate_heat_flow_from_mass_flow(self):
        """Calculate heat flow using: Q = m * cp * dT"""
        # read inputs
        mass_flow = ureg.Quantity(
            float(self.edit_mass_flow_magnitude.text() or 0),
            self.combo_mass_flow_unit.currentText(),
        )
        heat_capacity = ureg.Quantity(
            float(self.edit_heat_capacity_magnitude.text() or 0),
            self.combo_heat_capacity_unit.currentText(),
        )
        temp_diff = ureg.Quantity(
            float(self.edit_temp_diff_magnitude.text() or 0),
            self.combo_temp_diff_unit.currentText(),
        )
        heat_flow_unit = self.combo_heat_flow_unit.currentText()
        # calculate result
        heat_flow = mass_flow * heat_capacity * temp_diff
        print("calculating heat flow using Q = m * cp * dT:")
        print(f"{heat_flow:~P} = {mass_flow:~P} * {heat_capacity:~P} * {temp_diff:~P}")
        # write output
        self.edit_heat_flow_magnitude.setText(
            str(heat_flow.to(heat_flow_unit).magnitude)
        )

    def calculate_heat_flow_from_volume_flow(self):
        """Calculate heat flow using: Q = m * cp * dT and m = V * rho
        effectively running: Q = V * rho * cp * dT
        """
        self.calculate_mass_flow_from_volume_flow()
        self.calculate_heat_flow_from_mass_flow()

    def calculate_mass_flow_from_heat_flow_and_temperature_difference(self):
        """Calculate mass flow using: m = Q / (cp * dT)"""
        # read inputs
        heat_flow = ureg.Quantity(
            float(self.edit_heat_flow_magnitude.text() or 0),
            self.combo_heat_flow_unit.currentText(),
        )
        heat_capacity = ureg.Quantity(
            float(self.edit_heat_capacity_magnitude.text() or 0),
            self.combo_heat_capacity_unit.currentText(),
        )
        temp_diff = ureg.Quantity(
            float(self.edit_temp_diff_magnitude.text() or 0),
            self.combo_temp_diff_unit.currentText(),
        )
        mass_flow_unit = self.combo_mass_flow_unit.currentText()
        # calculate result
        mass_flow = heat_flow / (heat_capacity * temp_diff)
        print("calculating mass flow using m = Q / (cp * dT):")
        print(
            f"{mass_flow:~P} = {heat_flow:~P} / ({heat_capacity:~P} * {temp_diff:~P})"
        )
        # write outputs
        self.edit_mass_flow_magnitude.setText(
            str(mass_flow.to(mass_flow_unit).magnitude)
        )

    def calculate_volume_flow_from_mass_flow(self):
        """Calculate volume flow using: V = m / rho"""
        # read inputs
        mass_flow = ureg.Quantity(
            float(self.edit_mass_flow_magnitude.text() or 0),
            self.combo_mass_flow_unit.currentText(),
        )
        density = ureg.Quantity(
            float(self.edit_density_magnitude.text() or 0),
            self.combo_density_unit.currentText(),
        )
        volume_flow_unit = self.combo_volume_flow_unit.currentText()
        # calculate result
        volume_flow = mass_flow / density
        print("calculating volume flow using V = m / rho:")
        print(f"{volume_flow:~P} = {mass_flow:~P} / {density:~P}")
        # write outputs
        self.edit_volume_flow_magnitude.setText(
            str(volume_flow.to(volume_flow_unit).magnitude)
        )

    def calculate_mass_flow_from_volume_flow(self):
        """Calculate mass flow using: m = V * rho"""
        # read inputs
        volume_flow = ureg.Quantity(
            float(self.edit_volume_flow_magnitude.text() or 0),
            self.combo_volume_flow_unit.currentText(),
        )
        density = ureg.Quantity(
            float(self.edit_density_magnitude.text() or 0),
            self.combo_density_unit.currentText(),
        )
        mass_flow_unit = self.combo_mass_flow_unit.currentText()
        # calculate result
        mass_flow = volume_flow * density
        print("calculating mass flow using m = V * rho:")
        print(f"{mass_flow:~P} = {volume_flow:~P} * {density:~P}")
        # write outputs
        self.edit_mass_flow_magnitude.setText(
            str(mass_flow.to(mass_flow_unit).magnitude)
        )

    def calculate_temperature_difference_from_mass_flow(self):
        """Calculate temperature difference using: dT = Q / (m * cp)"""
        # read inputs
        heat_flow = ureg.Quantity(
            float(self.edit_heat_flow_magnitude.text() or 0),
            self.combo_heat_flow_unit.currentText(),
        )
        mass_flow = ureg.Quantity(
            float(self.edit_mass_flow_magnitude.text() or 0),
            self.combo_mass_flow_unit.currentText(),
        )
        heat_capacity = ureg.Quantity(
            float(self.edit_heat_capacity_magnitude.text() or 0),
            self.combo_heat_capacity_unit.currentText(),
        )
        temperature_difference_unit = self.combo_temp_diff_unit.currentText()
        # calculate result
        temp_diff = heat_flow / (mass_flow * heat_capacity)
        print("calculating temperature difference using dt = Q / (m * cp):")
        print(
            f"{temp_diff:~P} = {heat_flow:~P} / ({mass_flow:~P} * {heat_capacity:~P})"
        )
        # write outputs
        self.edit_temp_diff_magnitude.setText(
            str(temp_diff.to(temperature_difference_unit).magnitude)
        )

    def calculate_temperature_difference_from_volume_flow(self):
        """Calculate temperature difference using: dT = Q / (m * cp) and m = V * rho
        effectively running: dt = Q / (V * rho * cp)
        """
        self.calculate_mass_flow_from_volume_flow()
        self.calculate_temperature_difference_from_mass_flow()


def main():
    """Main program"""
    app = QApplication()
    window = QalculatorWidget()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
