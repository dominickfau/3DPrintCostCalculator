from PyQt5.QtWidgets import (
    QDialog, QTableWidgetItem
)

from ui.calculateServiceCostDialog import Ui_CalculateServiceCostDialog

class CalculateServiceCostDialog(Ui_CalculateServiceCostDialog):
    def __init__(self):
        self.window = QDialog()
        self.setupUi(self.window)
        
    def addItem(self, item):
        rowPosition = self.itemsTableWidget.rowCount()
        self.itemsTableWidget.insertRow(rowPosition)
        self.itemsTableWidget.setItem(rowPosition , 0, QTableWidgetItem(str(item["name"])))
        self.itemsTableWidget.setItem(rowPosition , 1, QTableWidgetItem(str(item["price"])))
        self.itemsTableWidget.setItem(rowPosition , 2, QTableWidgetItem(str(item["lifeInterval"])))
        
    def addBlankItem(self):
        rowPosition = self.itemsTableWidget.rowCount()
        self.itemsTableWidget.insertRow(rowPosition)
        self.itemsTableWidget.setItem(rowPosition , 0, QTableWidgetItem(""))
        self.itemsTableWidget.setItem(rowPosition , 1, QTableWidgetItem(""))
        self.itemsTableWidget.setItem(rowPosition , 2, QTableWidgetItem(""))
    
    
    def connectSignalsSlots(self):
        self.addItemButton.clicked.connect(self.addBlankItem)
        self.removeSelectedItemButton.clicked.connect(self.removeSelectedItem)
    
    def removeSelectedItem(self):
        selectedItems = self.itemsTableWidget.selectedIndexes()
        for item in selectedItems:
            index = item.row()
            self.itemsTableWidget.removeRow(index)
    
    def validateForm(self):
        formValid = True
        
        return formValid

    def clearForm(self):
        pass


    def getFormData(self):
        
        formData = {
        }
        
        return formData
    
    def loadDataFromDictionary(self, data):
        self.itemsTableWidget.setRowCount(0)
        self.itemsTableWidget.setHorizontalHeaderItem(0, QTableWidgetItem("Item"))
        self.itemsTableWidget.setHorizontalHeaderItem(1, QTableWidgetItem("Price ($)"))
        self.itemsTableWidget.setHorizontalHeaderItem(2, QTableWidgetItem("Life Interval (min)"))
        
        for item in data:
            self.addItem(item)