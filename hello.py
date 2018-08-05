#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Hello World GUI."""
import sys
import random
from PySide2 import QtWidgets


class HelloWorld(QtWidgets.QWidget):
    """Simple GUI showing a text label and a button."""

    def __init__(self):
        """Initializer."""
        super().__init__()
        self.texts = [
            "Hello World!",
            "Hallo Welt!",
            "Hola Mundo!",
        ]

        self.label = QtWidgets.QLabel(self.texts[0])
        self.button = QtWidgets.QPushButton("Do Magic")
        self.button.clicked.connect(self.magic)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

    def magic(self):
        """Change the label text."""
        old_text = self.label.text()
        new_text = random.choice(self.texts)
        while old_text == new_text:
            new_text = random.choice(self.texts)
        self.label.setText(new_text)
        self.label.repaint()


def main():
    """Main function."""
    app = QtWidgets.QApplication()
    window = HelloWorld()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
