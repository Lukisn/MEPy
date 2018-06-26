#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import random
from PySide2 import QtCore, QtGui, QtWidgets


class HelloWorld(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.texts = [
            "Hello World!",
            "Hallo Welt!",
            "Hola Mundo!",
        ]

        self.label = QtWidgets.QLabel(self.texts[0])
        self.button = QtWidgets.QPushButton("Magic")
        self.button.clicked.connect(self.magic)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

    def magic(self):
        self.label.setText(random.choice(self.texts))
        self.label.repaint()


def main():
    app = QtWidgets.QApplication()
    window = HelloWorld()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
