import sys, json, datetime

from PyQt5.QtWidgets import (
    QApplication, QDialog, QMainWindow, QMessageBox, QTableWidgetItem, QFileDialog
)

from ui.mainWindow import Ui_MainWindow
from ui.calculateServiceCostDialog import Ui_CalculateServiceCostDialog
from ui.materialDialog import Ui_MaterialDialog
from ui.printerDialog import Ui_PrinterDialog
from ui.settingsDialog import Ui_SettingsDialog

import stlVolume

PROGRAM_NAME = ""

class CalculateServiceCostDialog(Ui_CalculateServiceCostDialog):
    def addItem(self, item):
        rowPosition = self.itemsTableWidget.rowCount()
        self.itemsTableWidget.insertRow(rowPosition)
        self.itemsTableWidget.setItem(rowPosition , 0, QTableWidgetItem(str(item["Item"])))
        self.itemsTableWidget.setItem(rowPosition , 1, QTableWidgetItem(str(item["Price"])))
        self.itemsTableWidget.setItem(rowPosition , 2, QTableWidgetItem(str(item["LifeInterval"])))
        
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
            
        
        
class SettingsDialog(Ui_SettingsDialog):
    def connectSignalsSlots(self):
        pass
    
    def validateForm(self):
        formValid = True
        energyCost = self.energyCostDoubleSpinBox.value()
        laborRate = self.laborCostDoubleSpinBox.value()
        failureRate = self.failureRateDoubleSpinBox.value()
        
        return formValid

    def clearForm(self):
        energyCost = self.energyCostDoubleSpinBox.setValue(0.00)
        laborRate = self.laborCostDoubleSpinBox.setValue(0.00)
        failureRate = self.failureRateDoubleSpinBox.setValue(0.00)


    def getFormData(self):
        energyCost = self.energyCostDoubleSpinBox.value()
        laborRate = self.laborCostDoubleSpinBox.value()
        failureRate = self.failureRateDoubleSpinBox.value()
        
        
        formData = {
            "EnergyCost": energyCost,
            "LaborRate": laborRate,
            "FailureRate": failureRate
        }
        
        return formData
    
    def loadDataFromDictionary(self, settings):
        self.clearForm()
        energyCost = settings["EnergyCost"]
        laborRate = settings["LaborRate"]
        failureRate = settings["FailureRate"]
        
        energyCost = self.energyCostDoubleSpinBox.setValue(energyCost)
        laborRate = self.laborCostDoubleSpinBox.setValue(laborRate)
        failureRate = self.failureRateDoubleSpinBox.setValue(failureRate)
        
    
    
class MaterialDialog(Ui_MaterialDialog):
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
        materialType = self.materialTypeComboBox.currentText()
        materialDescription = self.materialDescriptionTextEdit.toPlainText()
        
        
        formData = {
            "Name": materialName,
            "Data": {
                "Price": price,
                "Qty": qty,
                "Type": materialType,
                "Description": materialDescription
                
            }
        }
        
        return formData
    
    def clearForm(self):
        self.materialNameLineEdit.setText("")
        self.priceDoubleSpinBox.setValue(0.00)
        self.qtyPerPriceDoubleSpinBox.setValue(1000.00)
        self.materialTypeComboBox.setCurrentIndex(0)
        self.materialDescriptionTextEdit.clear()
        
    def loadDataFromDictionary(self, material):
        self.clearForm()
        
        materialName = material["Name"]
        price = material["Data"]["Price"]
        qty = material["Data"]["Qty"]
        materialType = material["Data"]["Type"]
        materialDescription = material["Data"]["Description"]
        
        self.materialNameLineEdit.setText(materialName)
        self.priceDoubleSpinBox.setValue(price)
        self.qtyPerPriceDoubleSpinBox.setValue(qty)
        self.materialTypeComboBox.setCurrentText(materialType)
        self.materialDescriptionTextEdit.clear()
        self.materialDescriptionTextEdit.insertPlainText(materialDescription)
        


class PrinterDialog(Ui_PrinterDialog):
    def __init__(self):
        self.calculateServiceCostDialog = QDialog()
        self.calculateServiceCostDialog.ui = CalculateServiceCostDialog()
        self.calculateServiceCostDialog.ui.setupUi(self.calculateServiceCostDialog)
        self.calculateServiceCostDialog.ui.connectSignalsSlots()
        
        self.serviceCostCalcRows = []
        
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
        
        self.calculateServiceCostDialog.ui.loadDataFromDictionary(self.serviceCostCalcRows)
        self.calculateServiceCostDialog.exec()
        rowCount = self.calculateServiceCostDialog.ui.itemsTableWidget.rowCount()
        
        self.serviceCostCalcRows = []
        
        for index in range(rowCount):
            try:
                item = self.calculateServiceCostDialog.ui.itemsTableWidget.item(index, 0).text()
                price = float(self.calculateServiceCostDialog.ui.itemsTableWidget.item(index, 1).text())
                lifeInterval = float(self.calculateServiceCostDialog.ui.itemsTableWidget.item(index, 2).text())
                
                self.serviceCostCalcRows.append(
                {
                    "Item": item,
                    "Price": price,
                    "LifeInterval": lifeInterval
                }
                        )
                
            except ValueError:
                continue
        
        self.calculateServiceCost()
    
    def calculateServiceCost(self):
        deprecationTime = self.depreciationTimeDoubleSpinBox.value()
        total = 0.00
        
        for row in self.serviceCostCalcRows:
            item = row["Item"]
            price = row["Price"]
            lifeInterval = row["LifeInterval"]
            
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
        printerType = self.printerTypeComboBox.currentText()
        price = self.priceDoubleSpinBox.value()
        deprecationTime = self.depreciationTimeDoubleSpinBox.value()
        totalServiceCost = self.totalServiceCostDoubleSpinBox.value()
        energyConsumption = self.energyConsumptionDoubleSpinBox.value()
        deprecationValue = self.depreciationDoubleSpinBox.value()
        bedSizeLength = self.bedLengthDoubleSpinBox.value()
        bedSizeWidth = self.bedWidthDoubleSpinBox.value()
        bedSizeHeight = self.bedHeightDoubleSpinBox.value()
        
        formData = {
            "Name": printerName,
            "Data": {
                "Type": printerType,
                "Price": price,
                "DeprecationTime": deprecationTime,
                "ServiceCostRows": self.serviceCostCalcRows,
                "TotalServiceCost": totalServiceCost,
                "EnergyConsumption": energyConsumption,
                "DeprecationValue": deprecationValue,
                "BedSize": {
                    "Length": bedSizeLength,
                    "Width": bedSizeWidth,
                    "Height": bedSizeHeight
                }
            }
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
        
    def loadDataFromDictionary(self, printer):
        if printer is None:
            self.clearForm()
            return
        
        printerName = printer["Name"]
        printerType = printer["Data"]["Type"]
        price = printer["Data"]["Price"]
        deprecationTime = printer["Data"]["DeprecationTime"]
        totalServiceCost = printer["Data"]["TotalServiceCost"]
        energyConsumption = printer["Data"]["EnergyConsumption"]
        deprecationValue = printer["Data"]["DeprecationValue"]
        bedSizeLength = printer["Data"]["BedSize"]["Length"]
        bedSizeWidth = printer["Data"]["BedSize"]["Width"]
        bedSizeHeight = printer["Data"]["BedSize"]["Height"]
        
        self.serviceCostCalcRows = printer["Data"]["ServiceCostRows"]
            
        
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


class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.mainWindow = Ui_MainWindow()
        self.mainWindow.setupUi(self)

        self.saveDataFile = "saveData.json"
        self.printers = {}
        self.materials = {}
        self.settings = {}
        
        self.printerDialog = QDialog()
        self.printerDialog.ui = PrinterDialog()
        self.printerDialog.ui.setupUi(self.printerDialog)
        self.printerDialog.ui.connectSignalsSlots()
        
        self.materialDialog = QDialog()
        self.materialDialog.ui = MaterialDialog()
        self.materialDialog.ui.setupUi(self.materialDialog)
        self.materialDialog.ui.connectSignalsSlots()
        
        self.settingsDialog = QDialog()
        self.settingsDialog.ui = SettingsDialog()
        self.settingsDialog.ui.setupUi(self.settingsDialog)
        self.settingsDialog.ui.connectSignalsSlots()
        
        self.loadSavedData()
        self.connectSignalsSlots()
        self.mainWindow.quoteDateEdit.setDate(datetime.datetime.now().date())
        

    def closeEvent(self, event):
        self.saveData()
        event.accept()
        
    def getFormData(self):
        printerName = self.mainWindow.printerComboBox.currentText()
        materialName = self.mainWindow.materialComboBox.currentText()
        modelWeight = self.mainWindow.modelWeightDoubleSpinBox.value()
        printTime = self.mainWindow.printTimeDoubleSpinBox.value()
        customerName = self.mainWindow.customerNameLineEdit.text()
        quoteDate = self.mainWindow.quoteDateEdit.text()
        description = self.mainWindow.descriptionTextEdit.toPlainText()
        modelPrepTime = self.mainWindow.modelPrepTimeDoubleSpinBox.value()
        slicingTime = self.mainWindow.slicingPrepTimeDoubleSpinBox.value()
        materialChangeTime = self.mainWindow.materialChangePrepTimeDoubleSpinBox.value()
        transferStartTime = self.mainWindow.transferStartPrepTimeDoubleSpinBox.value()
        jobRemovalTime = self.mainWindow.jobRemovalPostTimeDoubleSpinBox.value()
        supportRemovalTime = self.mainWindow.supportRemovalPostTimeDoubleSpinBox.value()
        additionalTime = self.mainWindow.additionalWorkPostTimeSpinBox.value()
        consumablesCost = self.mainWindow.consumablesDoubleSpinBox.value()
        materialCost = self.mainWindow.materialCostDoubleSpinBox.value()
        electricityCost = self.mainWindow.electricityCostDoubleSpinBox.value()
        printerDepreciationCost = self.mainWindow.printerDepreciationCostDoubleSpinBox.value()
        preparationCost = self.mainWindow.prepCostDoubleSpinBox.value()
        postProcessingCost = self.mainWindow.postCostDoubleSpinBox.value()
        otherCost = self.mainWindow.otherCostDoubleSpinBox.value()
        subtotalCost = self.mainWindow.subtotalCostDoubleSpinBox.value()
        subtotalCostWithFailures = self.mainWindow.subtotalWithFailuresCostDoubleSpinBox.value()
        quoteMarkup = self.mainWindow.quoteMarkupDoubleSpinBox.value()
        quotedPrice = self.mainWindow.quotedPriceDoubleSpinBox.value()
        profit = self.mainWindow.quoteProfitDoubleSpinBox.value()
        
        
        formData = {
            "PrinterName": printerName,
            "MaterialName": materialName,
            "ModelWeight": modelWeight,
            "PrintTime": printTime,
            "CustomerName": customerName,
            "QuoteDate": quoteDate,
            "Description": description,
            "ModelPrepTime": modelPrepTime,
            "SlicingTime": slicingTime,
            "MaterialChangeTime": materialChangeTime,
            "TransferStartTime": transferStartTime,
            "JobRemovalTime": jobRemovalTime,
            "SupportRemovalTime": supportRemovalTime,
            "AdditionalTime": additionalTime,
            "ConsumablesCost": consumablesCost,
            "TotalMaterialsCost": materialCost,
            "TotalElectricityCost": electricityCost,
            "TotalPrinterDepreciationCost": printerDepreciationCost,
            "TotalPreparationCost": preparationCost,
            "TotalPostProcessingCost": postProcessingCost,
            "TotalOtherCost": otherCost,
            "SubtotalCost": subtotalCost,
            "SubtotalCostWithFailures": subtotalCostWithFailures,
            "QuoteMarkup": quoteMarkup,
            "QuotedPrice": quotedPrice,
            "Profit": profit
        }
        
        return formData

    def connectSignalsSlots(self):
        self.mainWindow.actionSettings.triggered.connect(self.openSettings)
        
        self.mainWindow.printerAddButton.clicked.connect(self.addPrinter)
        self.mainWindow.printerEditButton.clicked.connect(self.editPrinter)
        self.mainWindow.printerDeleteButton.clicked.connect(self.deletePrinter)
        self.mainWindow.printerComboBox.currentTextChanged.connect(self.reloadMaterials)
        self.mainWindow.materialComboBox.currentTextChanged.connect(self.recalculate)
        self.mainWindow.materialAddButton.clicked.connect(self.addMaterial)
        self.mainWindow.materialEditButton.clicked.connect(self.editMaterial)
        self.mainWindow.materialDeleteButton.clicked.connect(self.deleteMaterial)
        self.mainWindow.modelWeightDoubleSpinBox.valueChanged.connect(self.recalculate)
        self.mainWindow.modelWeightEstimateButton.clicked.connect(self.calculateModelWeight)
        self.mainWindow.printTimeDoubleSpinBox.valueChanged.connect(self.recalculate)
        
        # Preparation
        self.mainWindow.modelPrepTimeDoubleSpinBox.valueChanged.connect(self.recalculate)
        self.mainWindow.slicingPrepTimeDoubleSpinBox.valueChanged.connect(self.recalculate)
        self.mainWindow.materialChangePrepTimeDoubleSpinBox.valueChanged.connect(self.recalculate)
        self.mainWindow.transferStartPrepTimeDoubleSpinBox.valueChanged.connect(self.recalculate)
        
        # Post-Processing
        self.mainWindow.jobRemovalPostTimeDoubleSpinBox.valueChanged.connect(self.recalculate)
        self.mainWindow.supportRemovalPostTimeDoubleSpinBox.valueChanged.connect(self.recalculate)
        self.mainWindow.additionalWorkPostTimeSpinBox.valueChanged.connect(self.recalculate)
        
        # Other
        self.mainWindow.consumablesDoubleSpinBox.valueChanged.connect(self.recalculate)
        
        # Quote
        self.mainWindow.quoteMarkupDoubleSpinBox.valueChanged.connect(self.recalculate)
        
    
    def saveData(self):
        with open(self.saveDataFile, mode="w") as f:
            saveData = {}
            saveData["Settings"] = self.settings
            saveData["Printers"] = self.printers
            saveData["Materials"] = self.materials
            
            f.write(json.dumps(saveData, indent=4))
    
    def loadSavedData(self):
        self.printers = {}
        self.materials = {}
        self.settings = {}
        
        try:
            with open(self.saveDataFile, mode="r") as f:
                try:
                    saveData = json.loads(f.read())
                    self.settings = saveData["Settings"]
                    self.printers = saveData["Printers"]
                    self.materials = saveData["Materials"]
                except Exception:
                    pass
        except FileNotFoundError:
            pass
        
        if len(self.printers) > 0:
            for printerName in self.printers:
                printer = self.printers[printerName]
                self.mainWindow.printerComboBox.addItem(printer["Name"])
            
            self.reloadMaterials(list(self.printers.keys())[0])
        
    def reloadMaterials(self, printerName):
        materialType = self.printers[printerName]["Data"]["Type"]
        
        if len(self.materials) > 0:
            self.mainWindow.materialComboBox.clear()
            
            for materialName in self.materials:
                material = self.materials[materialName]
                if material["Data"]["Type"] == materialType:
                    self.mainWindow.materialComboBox.addItem(material["Name"])
                    
            self.recalculate()


    def addPrinter(self):
        self.printerDialog.ui.clearForm()
        self.printerDialog.exec()
        printerData = self.printerDialog.ui.getFormData()
        self.printers[printerData["Name"]] = printerData
        self.mainWindow.printerComboBox.addItem(printerData["Name"])
        self.mainWindow.printerComboBox.setCurrentText(printerData["Name"])
        self.saveData()
    
    def editPrinter(self):
        selectedName = self.mainWindow.printerComboBox.currentText()
        selectedIndex = self.mainWindow.printerComboBox.currentIndex()
        
        printer = self.printers.pop(selectedName, None)
        if printer is None:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Data Integrity Warning")
            msg.setText("Could not find selected printer.")
            msg.setDetailedText(f"Failed to find printer:\n   '{selectedName}'.\nDefault data will be loaded.")
            
            msg.exec_()
            
        self.printerDialog.ui.loadDataFromDictionary(printer)
        
        self.printerDialog.exec()
        printerData = self.printerDialog.ui.getFormData()
        self.printers[printerData["Name"]] = printerData
        self.mainWindow.printerComboBox.setItemText(selectedIndex, printerData["Name"])
        self.saveData()
        
    def deletePrinter(self):
        selectedName = self.mainWindow.printerComboBox.currentText()
        selectedIndex = self.mainWindow.printerComboBox.currentIndex()
        
        if len(selectedName) > 0:
            buttonReply = QMessageBox.question(self, "Printer Delete", f"Are you sure you want to delete '{selectedName}'", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if buttonReply == QMessageBox.No:
                return
        
            printer = self.printers.pop(selectedName, None)
            self.mainWindow.printerComboBox.removeItem(selectedIndex)
            self.saveData()
    
    def addMaterial(self):
        self.materialDialog.ui.clearForm()
        self.materialDialog.exec()
        materialData = self.materialDialog.ui.getFormData()
        self.materials[materialData["Name"]] = materialData
        self.mainWindow.materialComboBox.addItem(materialData["Name"])
        self.saveData()
        self.recalculate()
    
    def editMaterial(self):
        selectedName = self.mainWindow.materialComboBox.currentText()
        selectedIndex = self.mainWindow.materialComboBox.currentIndex()
        
        material = self.materials.pop(selectedName, None)
        if material is None:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Data Integrity Warning")
            msg.setText("Could not find selected material.")
            msg.setDetailedText(f"Failed to find material:\n   '{selectedName}'.\nDefault data will be loaded.")
            
            msg.exec_()
            
        self.materialDialog.ui.loadDataFromDictionary(material)
        
        self.materialDialog.exec()
        materialData = self.materialDialog.ui.getFormData()
        self.materials[materialData["Name"]] = materialData
        self.mainWindow.materialComboBox.setItemText(selectedIndex, materialData["Name"])
        self.saveData()
        self.recalculate()

    def deleteMaterial(self):
        selectedName = self.mainWindow.materialComboBox.currentText()
        selectedIndex = self.mainWindow.materialComboBox.currentIndex()
        
        if len(selectedName) > 0:
            buttonReply = QMessageBox.question(self, "Material Delete", f"Are you sure you want to delete '{selectedName}'", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if buttonReply == QMessageBox.No:
                return
            
            material = self.materials.pop(selectedName, None)
            self.mainWindow.materialComboBox.removeItem(selectedIndex)
            self.saveData()
    
    
    def openSettings(self):
        self.settingsDialog.ui.loadDataFromDictionary(self.settings)
        self.settingsDialog.exec()
        self.settings = self.settingsDialog.ui.getFormData()
        self.saveData()
    
    def recalculate(self):
        self.calculateMaterialCost()
        self.calculateElectricityCost()
        self.calculatePrinterDepreciationCost()
        self.calculateTotalPreparation()
        self.calculateTotalPostProcessing()
        self.calculateTotalOther()
        self.calculateTotalCost()
        self.calculateQuote()

    def calculateQuote(self):
        quoteMarkup = self.mainWindow.quoteMarkupDoubleSpinBox.value()
        subtotalCost = self.mainWindow.subtotalCostDoubleSpinBox.value()
        subtotalCostWithFailures = self.mainWindow.subtotalWithFailuresCostDoubleSpinBox.value()
        
        total = subtotalCost + (quoteMarkup / 100)
        profit = total - subtotalCost
        self.mainWindow.quotedPriceDoubleSpinBox.setValue(total)
        self.mainWindow.quoteProfitDoubleSpinBox.setValue(profit)
        
    def calculateMaterialCost(self):
        materialName = self.mainWindow.materialComboBox.currentText()
        if materialName == "":
            return
        
        materialPrice = self.materials[materialName]["Data"]["Price"]
        materialQtyPerPrice = self.materials[materialName]["Data"]["Qty"]
        
        modelWeight = self.mainWindow.modelWeightDoubleSpinBox.value()
    
        total = (materialPrice / materialQtyPerPrice) * modelWeight
        self.mainWindow.materialCostDoubleSpinBox.setValue(total)
    
    def calculateElectricityCost(self):
        printerName = self.mainWindow.printerComboBox.currentText()
        energyCostRate = self.settings["EnergyCost"]
        printerEnergyUsageRate = self.printers[printerName]["Data"]["EnergyConsumption"]
        printTime = self.mainWindow.printTimeDoubleSpinBox.value()
        
        totalEnergyUsage = printerEnergyUsageRate * (printTime / 60)
        
        total = totalEnergyUsage * energyCostRate
        self.mainWindow.electricityCostDoubleSpinBox.setValue(total)
    
    def calculatePrinterDepreciationCost(self):
        printerName = self.mainWindow.printerComboBox.currentText()
        printerDeprecationRate = self.printers[printerName]["Data"]["DeprecationValue"]
        printTime = self.mainWindow.printTimeDoubleSpinBox.value()

        total = (printTime / 60) * printerDeprecationRate
        self.mainWindow.printerDepreciationCostDoubleSpinBox.setValue(total)
    
    def calculateTotalPreparation(self):
        laborRateMinutes = self.settings["LaborRate"] / 60
        
        modelPrepTime = self.mainWindow.modelPrepTimeDoubleSpinBox.value()
        slicingTime = self.mainWindow.slicingPrepTimeDoubleSpinBox.value()
        materialChangeTime = self.mainWindow.materialChangePrepTimeDoubleSpinBox.value()
        transferStartTime = self.mainWindow.transferStartPrepTimeDoubleSpinBox.value()

        total = (modelPrepTime + slicingTime + materialChangeTime + transferStartTime) * laborRateMinutes
        
        self.mainWindow.prepCostDoubleSpinBox.setValue(total)
        
    def calculateTotalPostProcessing(self):
        laborRateMinutes = self.settings["LaborRate"] / 60
        
        jobRemovalTime = self.mainWindow.jobRemovalPostTimeDoubleSpinBox.value()
        supportRemovalTime = self.mainWindow.supportRemovalPostTimeDoubleSpinBox.value()
        additionalTime = self.mainWindow.additionalWorkPostTimeSpinBox.value()
        
        total = (jobRemovalTime + supportRemovalTime + additionalTime) * laborRateMinutes
        
        self.mainWindow.postCostDoubleSpinBox.setValue(total)
        
    def calculateTotalOther(self):
        consumablesCost = self.mainWindow.consumablesDoubleSpinBox.value()

        total = consumablesCost
        
        self.mainWindow.otherCostDoubleSpinBox.setValue(total)
        
    def calculateTotalCost(self):
        failureRateValue = self.settings["FailureRate"]
        
        materialCost = self.mainWindow.materialCostDoubleSpinBox.value()
        electricityCost = self.mainWindow.electricityCostDoubleSpinBox.value()
        printerDepreciationCost = self.mainWindow.printerDepreciationCostDoubleSpinBox.value()
        preparationCost = self.mainWindow.prepCostDoubleSpinBox.value()
        postProcessingCost = self.mainWindow.postCostDoubleSpinBox.value()
        otherCost = self.mainWindow.otherCostDoubleSpinBox.value()
        
        total = materialCost + electricityCost + printerDepreciationCost + preparationCost + postProcessingCost + otherCost
        totalWithFailures = total * (failureRateValue / 100 + 1)
        
        self.mainWindow.subtotalCostDoubleSpinBox.setValue(total)
        self.mainWindow.subtotalWithFailuresCostDoubleSpinBox.setValue(totalWithFailures)
        
    def calculateModelWeight(self):
        path = QFileDialog.getOpenFileName(self, 'Select a stl file', '', 'STL Files (*.stl)')
        if path != ('', ''):
            filePath = path[0]
            data = stlVolume.calculate(filePath)
            if len(data) > 0:
                modelVolume = data["ModelVolume"] * 1.1
                self.mainWindow.modelWeightDoubleSpinBox.setValue(modelVolume)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())