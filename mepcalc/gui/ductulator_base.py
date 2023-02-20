"""Duct Air Flow Calculator GUI."""

import sys

from PySide6.QtWidgets import QApplication, QWidget
from pint import Quantity

from mepcalc.common.medium import Medium


# TODO: implement! Extract ABC?
class DuctulatorWidget(QWidget):
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
        # ...?

    def create_widgets(self):
        """Create widgets."""
        ...

    def initialize_widgets(self) -> None:
        """Setup widgets for the user interface."""
        ...

    def build_layout(self) -> None:
        """Setup layout of the user interface in a grid."""
        ...

    def connect_signals_and_slots(self) -> None:
        """Connect signals to slots."""
        ...


def main():
    """Main program."""
    app = QApplication()
    window = DuctulatorWidget()
    window.setWindowTitle("Ductulator")
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
