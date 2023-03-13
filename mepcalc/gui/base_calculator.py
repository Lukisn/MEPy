"""Base Calculator."""

import sys
from typing import List

from PySide6.QtCore import Slot
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
)

from mepcalc.common.medium import Medium


class BaseCalculatorWidget(QWidget):
    """Base class for calculator ."""

    def __init__(self, medium: Medium, parent=None) -> None:
        super().__init__(parent)
        self.medium = medium
        self.permanently_disabled: List[QWidget] = []
        self.setup_ui()

    def setup_ui(self) -> None:
        """Setup user interface"""
        # configure and layout widgets
        self.create_widgets()
        self.initialize_widgets()
        self.build_layout()
        self.connect_signals_and_slots()
        # setup calculation fields by calling slots by hand
        self.output_changed()

    def create_widgets(self) -> None:
        pass

    def initialize_widgets(self) -> None:
        pass

    def build_layout(self) -> None:
        pass

    def connect_signals_and_slots(self) -> None:
        pass

    @Slot()
    def output_changed(self, checked=True) -> None:
        if not checked:
            return
        pass

    @Slot()
    def inputs_changed(self) -> None:
        pass

    def permanently_disable(self, widget: QWidget) -> None:
        """Permanently disable widget."""
        self.permanently_disabled.append(widget)

    def enable_all(self) -> None:
        """Enable all previously permanently disabled widgets."""
        self.permanently_disabled.clear()


def main():
    """Main program."""
    app = QApplication()
    window = BaseCalculatorWidget(medium=Medium.water())
    window.setWindowTitle("Base Calculator")
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
