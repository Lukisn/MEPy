"""Duct Air Flow Calculator GUI."""

import sys

from PySide6.QtWidgets import QApplication, QWidget
from pint import Quantity

from mepcalc.common.medium import Medium
from mepcalc.gui.duct_calculator_base import DuctCalculatorWidget


class DuctCalculatorRoundWidget(DuctCalculatorWidget):
    """Duct air flow calculator widget."""

    def initialize_widgets(self) -> None:
        """Setup widgets for the user interface."""
        ...

    def calculate_(self):
        """."""
        ...


def main():
    """Main program."""
    app = QApplication()
    window = DuctCalculatorRoundWidget()
    window.setWindowTitle("Duct Calculator Rectangular")
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
