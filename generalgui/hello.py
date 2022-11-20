#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Hello World GUI."""
import random
import sys

import PySide6
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget


class HelloWorld(QWidget):
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

        self.label = QLabel(self.texts[0])
        self.label.setAlignment(Qt.AlignCenter)
        self.button = QPushButton("Do Magic")
        self.button.clicked.connect(self.magic)

        self.layout = QVBoxLayout()
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
    print(f"PySide6 version:        {PySide6.__version__}")
    print(f"PySide6.QtCore version: {PySide6.QtCore.__version__}")

    app = QApplication()
    hello = HelloWorld()
    hello.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
