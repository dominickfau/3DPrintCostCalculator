from PyQt5.QtWidgets import (
    QDialog, QMessageBox
)

from ui.printerDialog import Ui_PrinterDialog
from calculateServiceCostDialog import CalculateServiceCostDialog
import database


class PrinterDialog(Ui_PrinterDialog):
    def __init__(self):
        self.window = QDialog()
        self.setupUi(self.window)
        
        self.calculateServiceCostDialog = CalculateServiceCostDialog()
        self.calculateServiceCostDialog.connectSignalsSlots()
        
        self.serviceCostCalcRows = []
        
        self.printerTypeComboBox.clear()
        materialTypes = database.MaterialType.find_all()
        for materialType in materialTypes:
            self.printerTypeComboBox.addItem(materialType.name)
        
        
    def connectSignalsSlots(self):
        self.priceDoubleSpinBox.valueChanged.connect(self.calculateDeprecationValue)
        self.depreciationTimeDoubleSpinBox.valueChanged.connect(self.calculateDeprecationValue)
        self.totalServiceCostDoubleSpinBox.valueChanged.connect(self.calculateDeprecationValue)
        self.totalServiceCostCalculateButton.clicked.connect(self.openCalculateServiceCostDialog)
        
    def openCalculateServiceCostDialog(self):
        deprecationTime = self.depreciationTimeDoubleSpinBox.value()
        if deprecationTime == 0.00:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Warning")
            msg.setText("Please enter a Deprecation Time and run this action again.")
            msg.exec_()
            self.depreciationTimeDoubleSpinBox.setFocus()
            self.depreciationTimeDoubleSpinBox.selectAll()
            return
        
        self.calculateServiceCostDialog.loadDataFromDictionary(self.serviceCostCalcRows)
        self.calculateServiceCostDialog.window.exec()
        rowCount = self.calculateServiceCostDialog.itemsTableWidget.rowCount()
        
        self.serviceCostCalcRows = []
        
        for index in range(rowCount):
            try:
                item = self.calculateServiceCostDialog.itemsTableWidget.item(index, 0).text()
                price = float(self.calculateServiceCostDialog.itemsTableWidget.item(index, 1).text())
                lifeInterval = float(self.calculateServiceCostDialog.itemsTableWidget.item(index, 2).text())
                
                self.serviceCostCalcRows.append(
                {
                    "name": item,
                    "price": price,
                    "lifeInterval": lifeInterval
                }
                        )
                
            except ValueError:
                continue
        
        self.calculateServiceCost()
    
    def calculateServiceCost(self):
        deprecationTime = self.depreciationTimeDoubleSpinBox.value()
        total = 0.00
        
        for row in self.serviceCostCalcRows:
            item = row["name"]
            price = row["price"]
            lifeInterval = row["lifeInterval"]
            
            pricePerMin = price / lifeInterval
            total += (pricePerMin * 60) * deprecationTime
        
        self.totalServiceCostDoubleSpinBox.setValue(total)
        
    def calculateDeprecationValue(self):
        price = self.priceDoubleSpinBox.value()
        deprecationTime = self.depreciationTimeDoubleSpinBox.value()
        totalServiceCost = self.totalServiceCostDoubleSpinBox.value()
        
        try:
            deprecationValue = (price + totalServiceCost) / deprecationTime
        except Exception:
            deprecationValue = 0.00
        
        self.depreciationDoubleSpinBox.setValue(deprecationValue)
        
        
    def validateForm(self):
        formValid = True
        
        printerName = self.printerNameLineEdit.text()
        printerType = self.printerTypeComboBox.currentText()
        price = self.priceDoubleSpinBox.value()
        deprecationTime = self.depreciationTimeDoubleSpinBox.value()
        totalServiceCost = self.totalServiceCostDoubleSpinBox.value()
        energyConsumption = self.energyConsumptionDoubleSpinBox.value()
        deprecationValue = self.depreciationDoubleSpinBox.value()
        bedSizeLength = self.bedLengthDoubleSpinBox.value()
        bedSizeWidth = self.bedWidthDoubleSpinBox.value()
        bedSizeHeight = self.bedHeightDoubleSpinBox.value()
        
        if len(printerName) <= 0: formValid = False
        
        return formValid
    
    def getFormData(self):
        printerName = self.printerNameLineEdit.text()
        materialTypeName = self.printerTypeComboBox.currentText()
        price = self.priceDoubleSpinBox.value()
        deprecationTime = self.depreciationTimeDoubleSpinBox.value()
        totalServiceCost = self.totalServiceCostDoubleSpinBox.value()
        energyConsumption = self.energyConsumptionDoubleSpinBox.value()
        deprecationPerHour = self.depreciationDoubleSpinBox.value()
        bedSizeLength = self.bedLengthDoubleSpinBox.value()
        bedSizeWidth = self.bedWidthDoubleSpinBox.value()
        bedSizeHeight = self.bedHeightDoubleSpinBox.value()
        
        serviceCostItems = []
        
        for serviceCostRow in self.serviceCostCalcRows:
            serviceCostRow["printerId"] = database.Printer.find_id_by_name(printerName)
            serviceCostItem = database.ServiceCostItem.from_dictionary(serviceCostRow)
            serviceCostItems.append(serviceCostItem)

        formData = {
            "bedSizeHeight": bedSizeHeight,
            "bedSizeLength": bedSizeLength,
            "bedSizeWidth": bedSizeWidth,
            "deprecationPerHour": deprecationPerHour,
            "deprecationTime": deprecationTime,
            "energyConsumption": energyConsumption,
            "materialTypeName": materialTypeName,
            "name": printerName,
            "price": price,
            "totalServiceCost": totalServiceCost,
            "serviceCostItems": serviceCostItems
        }
        
        return formData
    
    def clearForm(self):
        self.printerNameLineEdit.setText("")
        self.printerTypeComboBox.setCurrentText("")
        self.priceDoubleSpinBox.setValue(0.00)
        self.depreciationTimeDoubleSpinBox.setValue(0.00)
        self.totalServiceCostDoubleSpinBox.setValue(0.00)
        self.energyConsumptionDoubleSpinBox.setValue(0.00)
        self.depreciationDoubleSpinBox.setValue(0.00)
        self.bedLengthDoubleSpinBox.setValue(0.00)
        self.bedWidthDoubleSpinBox.setValue(0.00)
        self.bedHeightDoubleSpinBox.setValue(0.00)
        
    def loadData(self, printer):
        if printer is None:
            self.clearForm()
            return
        
        if not isinstance(printer, database.Printer): raise TypeError("printer must be of type Printer()")
        
        printerName = printer.name
        printerType = printer.materialType.name
        price = printer.price
        deprecationTime = printer.deprecationTime
        totalServiceCost = printer.totalServiceCost
        energyConsumption = printer.energyConsumption
        deprecationValue = printer.deprecationPerHour
        bedSizeLength = printer.bedSizeLength
        bedSizeWidth = printer.bedSizeWidth
        bedSizeHeight = printer.bedSizeHeight
    
        self.serviceCostCalcRows = []
        for item in database.ServiceCostItem.find_all_by_printer_id(printer.id):
            self.serviceCostCalcRows.append(
                {
                    "id": item.id,
                    "name": item.name,
                    "price": item.price,
                    "lifeInterval": item.lifeInterval
                }
            )
            
        self.printerNameLineEdit.setText(printerName)
        self.printerTypeComboBox.setCurrentText(printerType)
        self.priceDoubleSpinBox.setValue(price)
        self.depreciationTimeDoubleSpinBox.setValue(deprecationTime)
        self.totalServiceCostDoubleSpinBox.setValue(totalServiceCost)
        self.energyConsumptionDoubleSpinBox.setValue(energyConsumption)
        self.depreciationDoubleSpinBox.setValue(deprecationValue)
        self.bedLengthDoubleSpinBox.setValue(bedSizeLength)
        self.bedWidthDoubleSpinBox.setValue(bedSizeWidth)
        self.bedHeightDoubleSpinBox.setValue(bedSizeHeight)