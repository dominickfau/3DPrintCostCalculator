from PyQt5.QtWidgets import (
    QDialog
)

from ui.materialDialog import Ui_MaterialDialog
import database


class MaterialDialog(Ui_MaterialDialog):
    def __init__(self):
        self.window = QDialog()
        self.setupUi(self.window)
        
        self.materialTypeComboBox.clear()
        materialTypes = database.MaterialType.find_all()
        for materialType in materialTypes:
            self.materialTypeComboBox.addItem(materialType.name)
        
    def connectSignalsSlots(self):
        pass
    
    def validateForm(self):
        formValid = True
        materialName = self.materialNameLineEdit.text()
        price = self.priceDoubleSpinBox.value()
        materialType = self.materialTypeComboBox.currentText()
        materialDescription = self.materialDescriptionTextEdit.toPlainText()
        
        if len(materialName) <= 0: formValid = False
        
        return formValid
    
    def getFormData(self):
        materialName = self.materialNameLineEdit.text()
        price = self.priceDoubleSpinBox.value()
        qty = self.qtyPerPriceDoubleSpinBox.value()
        materialTypeName = self.materialTypeComboBox.currentText()
        materialDescription = self.materialDescriptionTextEdit.toPlainText()
        
        
        formData = {
            "name": materialName,
            "price": price,
            "quantity": qty,
            "materialTypeName": materialTypeName,
            "description": materialDescription
        }
        
        return formData
    
    def clearForm(self):
        self.materialNameLineEdit.setText("")
        self.priceDoubleSpinBox.setValue(0.00)
        self.qtyPerPriceDoubleSpinBox.setValue(1000.00)
        self.materialTypeComboBox.setCurrentIndex(0)
        self.materialDescriptionTextEdit.clear()
        
    def loadData(self, material):
        self.clearForm()
        
        materialName = material.name
        price = material.price
        quantity = material.quantity
        materialTypeName = material.materialType.name
        materialDescription = material.description
        
        self.materialNameLineEdit.setText(materialName)
        self.priceDoubleSpinBox.setValue(price)
        self.qtyPerPriceDoubleSpinBox.setValue(quantity)
        self.materialTypeComboBox.setCurrentText(materialTypeName)
        self.materialDescriptionTextEdit.clear()
        self.materialDescriptionTextEdit.insertPlainText(materialDescription)