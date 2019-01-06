#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import random
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import Qt


class MyWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.current_zoom = 1
        self.zoom_factor = 1.2
        self.maybe_save = False

        self.bg_brush = QtGui.QBrush(Qt.white)
        self.node_pen = QtGui.QPen(Qt.black, 2)
        self.node_brush = QtGui.QBrush(Qt.lightGray)
        self.edge_pen = QtGui.QPen(Qt.black, 5)

        self.setWindowTitle("Main App")
        self.showMaximized()

        self.init_icons()
        self.init_actions()
        self.init_widgets()

        self.no_drag_mode()
        self.status_bar.showMessage("Ready")

    def init_icons(self):
        self.open_icon = QtGui.QIcon("icons/Open.png")
        self.save_icon = QtGui.QIcon("icons/Save.png")
        self.save_as_icon = QtGui.QIcon("icons/Save-As.png")
        self.quit_icon = QtGui.QIcon("icons/Logout.png")
        self.add_new_icon = QtGui.QIcon("icons/Add-New.png")
        self.zoom_in_icon = QtGui.QIcon("icons/Zoom-In.png")
        self.zoom_out_icon = QtGui.QIcon("icons/Zoom-Out.png")
        self.select_icon = QtGui.QIcon("icons/Cursor.png")
        self.move_icon = QtGui.QIcon("icons/Mouse-Drag.png")

    def init_actions(self):
        self.open_action = QtWidgets.QAction("Open", parent=self)
        self.open_action.setIcon(self.open_icon)
        self.save_action = QtWidgets.QAction("Save", parent=self)
        self.save_action.setIcon(self.save_icon)
        self.save_as_action = QtWidgets.QAction("Save as", parent=self)
        self.save_as_action.setIcon(self.save_as_icon)
        self.quit_action = QtWidgets.QAction("Quit Program", parent=self)
        self.quit_action.setIcon(self.quit_icon)
        self.quit_action.triggered.connect(self.close)

        self.add_node_action = QtWidgets.QAction("Add Node", parent=self)
        self.add_node_action.setIcon(self.add_new_icon)
        self.add_node_action.triggered.connect(self.add_node)

        self.add_edge_action = QtWidgets.QAction("Add Edge", parent=self)
        self.add_edge_action.triggered.connect(self.add_edge)

        self.zoom_in_action = QtWidgets.QAction("Zoom in", parent=self)
        self.zoom_in_action.setIcon(self.zoom_in_icon)
        self.zoom_in_action.triggered.connect(self.zoom_in)
        self.zoom_out_action = QtWidgets.QAction("Zoom out", parent=self)
        self.zoom_out_action.setIcon(self.zoom_out_icon)
        self.zoom_out_action.triggered.connect(self.zoom_out)
        self.select_action = QtWidgets.QAction("Select Mode", parent=self)
        self.select_action.setIcon(self.select_icon)
        self.select_action.setCheckable(True)
        self.select_action.triggered.connect(self.select_mode)
        self.move_action = QtWidgets.QAction("Move Mode", parent=self)
        self.move_action.setIcon(self.move_icon)
        self.move_action.setCheckable(True)
        self.move_action.triggered.connect(self.move_mode)
        self.info_action = QtWidgets.QAction("Info", parent=self)
        self.info_action.triggered.connect(self.info)

    def init_widgets(self):
        self.scene = QtWidgets.QGraphicsScene()
        self.scene.setBackgroundBrush(self.bg_brush)
        self.view = QtWidgets.QGraphicsView(self.scene)
        self.view.setMinimumWidth(400)
        self.view.setMinimumHeight(300)
        self.view.setInteractive(True)
        self.setCentralWidget(self.view)
        # Menu Bar:
        self.menu_bar = QtWidgets.QMenuBar(parent=self)
        self.menu_bar.setNativeMenuBar(False)
        self.file_menu = self.menu_bar.addMenu("File")
        self.file_menu.addAction(self.open_action)
        self.file_menu.addAction(self.save_action)
        self.file_menu.addAction(self.save_as_action)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.quit_action)
        self.edit_menu = self.menu_bar.addMenu("Edit")
        self.edit_menu.addAction(self.add_node_action)
        self.edit_menu.addAction(self.add_edge_action)
        self.edit_menu.addSeparator()
        self.edit_menu.addAction(self.select_action)
        self.edit_menu.addAction(self.move_action)
        self.view_menu = self.menu_bar.addMenu("View")
        self.view_menu.addAction(self.zoom_in_action)
        self.view_menu.addAction(self.zoom_out_action)
        self.about_menu = self.menu_bar.addMenu("About")
        self.about_menu.addAction(self.info_action)
        self.setMenuBar(self.menu_bar)
        # Tool Bar:
        self.tool_bar = QtWidgets.QToolBar("Main Tool Bar", parent=self)
        self.tool_bar.addAction(self.add_node_action)
        self.tool_bar.addAction(self.add_edge_action)

        self.tool_bar.addAction(self.zoom_in_action)
        self.tool_bar.addAction(self.zoom_out_action)
        self.tool_bar.addSeparator()
        self.tool_bar.addAction(self.select_action)
        self.tool_bar.addAction(self.move_action)
        self.tool_bar.addSeparator()
        self.tool_bar.addAction(self.quit_action)
        self.addToolBar(self.tool_bar)
        # Status Bar:
        self.status_bar = QtWidgets.QStatusBar()
        self.setStatusBar(self.status_bar)

    def closeEvent(self, event):
        if self.maybe_save:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setText("Quit program without saving.")
            msgBox.setInformativeText(
                "Do you really want to quit? Unsaved changes maybe lost.")
            msgBox.setStandardButtons(
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            msgBox.setDefaultButton(QtWidgets.QMessageBox.No)
            ret = msgBox.exec_()
            if ret == QtWidgets.QMessageBox.No:
                event.ignore()
        else:
            event.accept()

    def add_node(self):
        x = random.randint(-200, 200)
        y = random.randint(-150, 150)
        node = QtWidgets.QGraphicsEllipseItem(x, y, 10, 10)
        node.setPen(self.node_pen)
        node.setBrush(self.node_brush)
        node.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable)
        node.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)
        node.setCursor(Qt.PointingHandCursor)
        self.scene.addItem(node)

        self.maybe_save = True
        self.status_bar.showMessage(f"Added node at ({x}, {y})")

    def add_edge(self):
        selection = self.scene.selectedItems()
        if not selection:
            self.status_bar.showMessage("No node selected. No edge added.")
        else:
            first = selection[0]
            edge = QtWidgets.QGraphicsLineItem(0, 0, first.x(), first.y())
            edge.setPen(self.edge_pen)
            self.scene.addItem(edge)

            self.maybe_save = True
            self.status_bar.showMessage(
                f"Added edge from (0, 0) to ({first.x()}, {first.y()})")

    def zoom_in(self):
        self.view.scale(self.zoom_factor, self.zoom_factor)
        self.current_zoom *= self.zoom_factor
        self.status_bar.showMessage(
            f"Zoomed in to zoom factor of {self.current_zoom}")

    def zoom_out(self):
        self.view.scale(1 / self.zoom_factor, 1 / self.zoom_factor)
        self.current_zoom /= self.zoom_factor
        self.status_bar.showMessage(
            f"Zoomed in to zoom factor of {self.current_zoom}")

    def no_drag_mode(self):
        self.view.setDragMode(QtWidgets.QGraphicsView.NoDrag)
        self.move_action.setChecked(False)
        self.select_action.setChecked(False)
        self.status_bar.showMessage("Activated No Drag Mode")

    def select_mode(self):
        self.view.setDragMode(QtWidgets.QGraphicsView.RubberBandDrag)
        self.move_action.setChecked(False)
        self.select_action.setChecked(True)
        self.status_bar.showMessage("Activated Select Mode")

    def move_mode(self):
        self.view.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
        self.select_action.setChecked(False)
        self.move_action.setChecked(True)
        self.status_bar.showMessage("Activated Move Mode")

    def info(self):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setText("Info")
        msgBox.setInformativeText(
            "This is some useful information.")
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msgBox.setDefaultButton(QtWidgets.QMessageBox.Ok)
        msgBox.exec_()


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
