#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import pint
from PySide2 import QtCore, QtGui, QtWidgets


ureg = pint.UnitRegistry()


class Converter(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Unit Converter")

        self.units = sorted(get_all_units(ureg))

        # Widgets:
        self.input_value = QtWidgets.QLineEdit("1.0")
        self.input_value.setValidator(QtGui.QDoubleValidator())
        self.input_value.setMinimumWidth(200)
        self.input_unit = QtWidgets.QComboBox()
        self.input_unit.addItems(self.units)
        self.input_unit.setEditable(True)
        self.input_unit.setInsertPolicy(QtWidgets.QComboBox.NoInsert)
        self.input_unit.setEditText("feet")

        self.output_value = QtWidgets.QLineEdit()
        self.output_value.setValidator(QtGui.QDoubleValidator())
        self.output_value.setMinimumWidth(200)
        self.output_unit = QtWidgets.QComboBox()
        self.output_unit.addItems(self.units)
        self.output_unit.setEditable(True)
        self.input_unit.setInsertPolicy(QtWidgets.QComboBox.NoInsert)
        self.output_unit.setEditText("meter")

        self.convert_button = QtWidgets.QPushButton("Convert")
        self.convert_button.setDefault(True)
        self.convert_button.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.switch_button = QtWidgets.QPushButton("Switch")
        self.switch_button.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.clear_button = QtWidgets.QPushButton("Clear")

        # Layouts:
        self.input_layout = QtWidgets.QHBoxLayout()
        self.input_layout.addWidget(self.input_value)
        self.input_layout.addWidget(self.input_unit)

        self.output_layout = QtWidgets.QHBoxLayout()
        self.output_layout.addWidget(self.output_value)
        self.output_layout.addWidget(self.output_unit)

        self.control_layout = QtWidgets.QHBoxLayout()
        self.control_layout.addWidget(self.convert_button)
        self.control_layout.addWidget(self.switch_button)
        self.control_layout.addWidget(self.clear_button)

        # Main Layout:
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addLayout(self.input_layout)
        self.layout.addLayout(self.output_layout)
        self.layout.addLayout(self.control_layout)
        self.setLayout(self.layout)

        # Signals and Slots:
        self.convert_button.clicked.connect(self.convert)
        self.switch_button.clicked.connect(self.switch)
        self.clear_button.clicked.connect(self.clear)

    def convert(self):
        input_amount = float(self.input_value.text())
        input_unit = self.input_unit.currentText()
        output_unit = self.output_unit.currentText()
        result = convert(input_amount, input_unit, output_unit)
        self.output_value.setText(str(result.magnitude))
        self.repaint()

    def switch(self):
        input_unit = self.input_unit.currentText()
        output_unit = self.output_unit.currentText()
        self.input_unit.setCurrentText(output_unit)
        self.output_unit.setCurrentText(input_unit)
        self.repaint()
        self.convert()

    def clear(self):
        self.input_value.clear()
        self.input_unit.clearEditText()
        self.output_value.clear()
        self.output_unit.clearEditText()
        self.input_value.setFocus()
        self.repaint()


def convert(amount, input_unit, output_unit):
    """Convert a quantity from one to another unit."""
    input_quantity = ureg.Quantity(amount, ureg.parse_expression(input_unit))
    return input_quantity.to(output_unit)


def get_all_units(registry):
    """Get all units from a pint unit registry."""
    members = registry.__dict__["_units"]
    return list(members.keys())


def main():
    """Main function."""
    app = QtWidgets.QApplication()
    conv = Converter()
    conv.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
