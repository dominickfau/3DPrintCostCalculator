# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\CalculateServiceCostDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CalculateServiceCostDialog(object):
    def setupUi(self, CalculateServiceCostDialog):
        CalculateServiceCostDialog.setObjectName("CalculateServiceCostDialog")
        CalculateServiceCostDialog.resize(442, 291)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(CalculateServiceCostDialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.addItemButton = QtWidgets.QPushButton(CalculateServiceCostDialog)
        self.addItemButton.setObjectName("addItemButton")
        self.verticalLayout.addWidget(self.addItemButton)
        self.removeSelectedItemButton = QtWidgets.QPushButton(CalculateServiceCostDialog)
        self.removeSelectedItemButton.setObjectName("removeSelectedItemButton")
        self.verticalLayout.addWidget(self.removeSelectedItemButton)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.itemsTableWidget = QtWidgets.QTableWidget(CalculateServiceCostDialog)
        self.itemsTableWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.itemsTableWidget.setAlternatingRowColors(True)
        self.itemsTableWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.itemsTableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.itemsTableWidget.setObjectName("itemsTableWidget")
        self.itemsTableWidget.setColumnCount(3)
        self.itemsTableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.itemsTableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.itemsTableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.itemsTableWidget.setHorizontalHeaderItem(2, item)
        self.itemsTableWidget.horizontalHeader().setStretchLastSection(True)
        self.verticalLayout_2.addWidget(self.itemsTableWidget)
        self.saveButton = QtWidgets.QPushButton(CalculateServiceCostDialog)
        self.saveButton.setObjectName("saveButton")
        self.verticalLayout_2.addWidget(self.saveButton)

        self.retranslateUi(CalculateServiceCostDialog)
        self.saveButton.clicked.connect(CalculateServiceCostDialog.close)
        QtCore.QMetaObject.connectSlotsByName(CalculateServiceCostDialog)

    def retranslateUi(self, CalculateServiceCostDialog):
        _translate = QtCore.QCoreApplication.translate
        CalculateServiceCostDialog.setWindowTitle(_translate("CalculateServiceCostDialog", "Calculate Service Cost"))
        self.addItemButton.setText(_translate("CalculateServiceCostDialog", "Add Item"))
        self.removeSelectedItemButton.setText(_translate("CalculateServiceCostDialog", "Remove Selected Item"))
        item = self.itemsTableWidget.horizontalHeaderItem(0)
        item.setText(_translate("CalculateServiceCostDialog", "Item"))
        item = self.itemsTableWidget.horizontalHeaderItem(1)
        item.setText(_translate("CalculateServiceCostDialog", "Price"))
        item = self.itemsTableWidget.horizontalHeaderItem(2)
        item.setText(_translate("CalculateServiceCostDialog", "Life Interval (min)"))
        self.saveButton.setText(_translate("CalculateServiceCostDialog", "Save"))
