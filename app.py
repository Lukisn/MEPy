#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from PySide2 import QtCore, QtGui, QtWidgets


class MyView(QtWidgets.QGraphicsView):

    def __init__(self, scene):
        super().__init__(scene)

    def zoom_in(self):
        self.scale(1.2, 1.2)

    def zoom_out(self):
        self.scale(1 / 1.2, 1 / 1.2)


class MyWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.status_bar = QtWidgets.QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Initializing...")

        self.scene = QtWidgets.QGraphicsScene()

        self.view = MyView(self.scene)
        self.view.setMinimumWidth(400)
        self.view.setMinimumHeight(300)
        self.view.setBackgroundBrush(QtGui.QBrush(QtCore.Qt.darkGray))

        self.setCentralWidget(self.view)

        self.status_bar.showMessage("Ready")


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
