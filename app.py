#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import random
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

        self.setWindowTitle("Main App")

        self.status_bar = QtWidgets.QStatusBar()
        self.setStatusBar(self.status_bar)

        self.scene = QtWidgets.QGraphicsScene()
        self.view = MyView(self.scene)
        self.view.setMinimumWidth(400)
        self.view.setMinimumHeight(300)
        self.view.setBackgroundBrush(QtGui.QBrush(QtCore.Qt.darkGray))
        self.setCentralWidget(self.view)

        # Actions:
        self.add_node_action = QtWidgets.QAction("Add Node", parent=self)
        self.add_node_action.triggered.connect(self.add_node)
        self.zoom_in_action = QtWidgets.QAction("Zoom in", parent=self)
        self.zoom_in_action.triggered.connect(self.zoom_in)
        self.zoom_out_action = QtWidgets.QAction("Zoom out", parent=self)
        self.zoom_out_action.triggered.connect(self.zoom_out)

        # Tool Bar:
        self.tool_bar = QtWidgets.QToolBar("Main Tool Bar")
        self.tool_bar.addAction(self.add_node_action)
        self.tool_bar.addAction(self.zoom_in_action)
        self.tool_bar.addAction(self.zoom_out_action)
        self.addToolBar(self.tool_bar)

        self.status_bar.showMessage("Ready")

    def add_node(self):
        x = random.randint(-200, 200)
        y = random.randint(-150, 150)
        self.scene.addEllipse(x, y, 10, 10)

    def zoom_in(self):
        self.view.zoom_in()

    def zoom_out(self):
        self.view.zoom_out()


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
