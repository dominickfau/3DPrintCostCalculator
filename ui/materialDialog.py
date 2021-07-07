# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\ui\MaterialDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MaterialDialog(object):
    def setupUi(self, MaterialDialog):
        MaterialDialog.setObjectName("MaterialDialog")
        MaterialDialog.resize(359, 226)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Small Icons/Icons/Prigram_Icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MaterialDialog.setWindowIcon(icon)
        self.verticalLayout = QtWidgets.QVBoxLayout(MaterialDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.materialNameLabel = QtWidgets.QLabel(MaterialDialog)
        self.materialNameLabel.setObjectName("materialNameLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.materialNameLabel)
        self.materialNameLineEdit = QtWidgets.QLineEdit(MaterialDialog)
        self.materialNameLineEdit.setWhatsThis("")
        self.materialNameLineEdit.setObjectName("materialNameLineEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.materialNameLineEdit)
        self.materialDescriptionLabel = QtWidgets.QLabel(MaterialDialog)
        self.materialDescriptionLabel.setObjectName("materialDescriptionLabel")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.materialDescriptionLabel)
        self.materialDescriptionTextEdit = QtWidgets.QTextEdit(MaterialDialog)
        self.materialDescriptionTextEdit.setObjectName("materialDescriptionTextEdit")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.materialDescriptionTextEdit)
        self.materialTypeLabel = QtWidgets.QLabel(MaterialDialog)
        self.materialTypeLabel.setObjectName("materialTypeLabel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.materialTypeLabel)
        self.materialTypeComboBox = QtWidgets.QComboBox(MaterialDialog)
        self.materialTypeComboBox.setObjectName("materialTypeComboBox")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.materialTypeComboBox)
        self.priceLabel = QtWidgets.QLabel(MaterialDialog)
        self.priceLabel.setObjectName("priceLabel")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.priceLabel)
        self.priceDoubleSpinBox = QtWidgets.QDoubleSpinBox(MaterialDialog)
        self.priceDoubleSpinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.priceDoubleSpinBox.setMaximum(100000.0)
        self.priceDoubleSpinBox.setObjectName("priceDoubleSpinBox")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.priceDoubleSpinBox)
        self.qtyPerPriceLabel = QtWidgets.QLabel(MaterialDialog)
        self.qtyPerPriceLabel.setObjectName("qtyPerPriceLabel")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.qtyPerPriceLabel)
        self.qtyPerPriceDoubleSpinBox = QtWidgets.QDoubleSpinBox(MaterialDialog)
        self.qtyPerPriceDoubleSpinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.qtyPerPriceDoubleSpinBox.setMaximum(10000.0)
        self.qtyPerPriceDoubleSpinBox.setProperty("value", 1000.0)
        self.qtyPerPriceDoubleSpinBox.setObjectName("qtyPerPriceDoubleSpinBox")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.qtyPerPriceDoubleSpinBox)
        self.verticalLayout.addLayout(self.formLayout)
        self.saveMaterialButton = QtWidgets.QPushButton(MaterialDialog)
        self.saveMaterialButton.setObjectName("saveMaterialButton")
        self.verticalLayout.addWidget(self.saveMaterialButton)

        self.retranslateUi(MaterialDialog)
        self.saveMaterialButton.clicked.connect(MaterialDialog.close)
        QtCore.QMetaObject.connectSlotsByName(MaterialDialog)
        MaterialDialog.setTabOrder(self.materialNameLineEdit, self.materialTypeComboBox)
        MaterialDialog.setTabOrder(self.materialTypeComboBox, self.priceDoubleSpinBox)
        MaterialDialog.setTabOrder(self.priceDoubleSpinBox, self.materialDescriptionTextEdit)
        MaterialDialog.setTabOrder(self.materialDescriptionTextEdit, self.saveMaterialButton)

    def retranslateUi(self, MaterialDialog):
        _translate = QtCore.QCoreApplication.translate
        MaterialDialog.setWindowTitle(_translate("MaterialDialog", "Material"))
        self.materialNameLabel.setText(_translate("MaterialDialog", "Name:"))
        self.materialDescriptionLabel.setText(_translate("MaterialDialog", "Description:"))
        self.materialTypeLabel.setText(_translate("MaterialDialog", "Material Type:"))
        self.priceLabel.setText(_translate("MaterialDialog", "Price:"))
        self.priceDoubleSpinBox.setPrefix(_translate("MaterialDialog", "$ "))
        self.qtyPerPriceLabel.setText(_translate("MaterialDialog", "Qty per Price:"))
        self.qtyPerPriceDoubleSpinBox.setSuffix(_translate("MaterialDialog", " g"))
        self.saveMaterialButton.setText(_translate("MaterialDialog", "Save"))
from . import Resource_rc