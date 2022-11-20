"""MEP Calculator GUI"""

import sys

from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QTabWidget


class MEPCalc(QMainWindow):
    """MEP Calculator GUI."""

    def __init__(self, title="MEP Calculator"):
        """Initializer."""
        super().__init__(parent=None)
        self.setWindowTitle(title)
        self.setup_ui()

    def setup_ui(self):
        """Setup User Interface."""
        # Second Level Tabs
        heat_flow_tabs = QTabWidget()
        heat_flow_tabs.addTab(QLabel("Heat Flow: Mass Flow"), "Mass Flow")
        heat_flow_tabs.addTab(QLabel("Heat Flow: Volume Flow"), "Volume Flow")
        duct_tabs = QTabWidget()
        duct_tabs.addTab(QLabel("Duct: Rectangular"), "Rectangular")
        duct_tabs.addTab(QLabel("Duct: Round"), "Round")
        pipe_tabs = QTabWidget()
        pipe_tabs.addTab(QLabel("Pipe: Pressure"), "Pressure")
        pipe_tabs.addTab(QLabel("Pipe: Gravitation"), "Gravitation")
        # Top Level Tabs
        main_tabs = QTabWidget(self)
        main_tabs.addTab(heat_flow_tabs, "Heat Flow")
        main_tabs.addTab(duct_tabs, "Duct")
        main_tabs.addTab(pipe_tabs, "Pipe")
        # Central Widget
        self.setCentralWidget(main_tabs)


def main():
    """Main Program."""
    app = QApplication()
    window = MEPCalc()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
