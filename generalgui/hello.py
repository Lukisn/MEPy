#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Hello World GUI."""
import sys
import random

import PySide2
from PySide2 import QtCore, QtWidgets


class HelloWorld(QtWidgets.QWidget):
    """Simple GUI showing a text label and a button."""

    def __init__(self):
        """Initializer."""
        super().__init__()
        self.texts = [
            "Hello World!",
            "Hallo Welt!",
            "你好，世界",
            "Hei maailma",
            "Hola Mundo",
            "Привет мир",
        ]

        self.label = QtWidgets.QLabel(self.texts[0])
        self.label.setAlignment(QtCore.Qt.AlignCenter)
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
    print(f"PySide2 version:        {PySide2.__version__}")
    print(f"PySide2.QtCore version: {PySide2.QtCore.__version__}")

    app = QtWidgets.QApplication()
    window = HelloWorld()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
