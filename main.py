import sys, json, datetime
import stlVolume, database

from PyQt5.QtWidgets import (
    QApplication, QDialog, QMainWindow, QMessageBox, QFileDialog
)

from ui.mainWindow import Ui_MainWindow
from printerDialog import PrinterDialog
from materialDialog import MaterialDialog
from settingsDialog import SettingsDialog


PROGRAM_NAME = "3D Print Cost Calculator"

class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.mainWindow = Ui_MainWindow()
        self.mainWindow.setupUi(self)
        
        self.printerDialog = PrinterDialog()
        self.printerDialog.connectSignalsSlots()
        
        self.materialDialog= MaterialDialog()
        self.materialDialog.connectSignalsSlots()
        
        self.settingsDialog = SettingsDialog()
        self.settingsDialog.connectSignalsSlots()
        
        self.loadData()
        self.connectSignalsSlots()
        self.mainWindow.quoteDateEdit.setDate(datetime.datetime.now().date())
        
    def loadData(self):
        printers = database.Printer.find_all()
        if len(printers) > 0:
            self.mainWindow.printerEditButton.setEnabled(True)
            self.mainWindow.printerDeleteButton.setEnabled(True)
        for printer in printers:
            self.mainWindow.printerComboBox.addItem(printer.name)
        self.mainWindow.printerComboBox.setCurrentIndex(0)
        
        materials = database.Material.find_all()
        if len(materials) > 0:
            self.mainWindow.materialEditButton.setEnabled(True)
            self.mainWindow.materialDeleteButton.setEnabled(True)
        for material in materials:
            self.mainWindow.materialComboBox.addItem(material.name)
        
        self.reloadMaterials()
        
    def closeEvent(self, event):
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
        
        
    def reloadMaterials(self):
        selectedPrinterName = self.mainWindow.printerComboBox.currentText()
        printer = database.Printer.from_name(selectedPrinterName)
        
        self.mainWindow.materialComboBox.clear()
        
        for material in database.Material.find_all():
            if material.materialType.name == printer.materialType.name:
                self.mainWindow.materialComboBox.addItem(material.name)
                
        self.recalculate()


    def addPrinter(self):
        self.printerDialog.clearForm()
        self.printerDialog.window.exec()
        
        if self.printerDialog.validateForm():
            printerData = self.printerDialog.getFormData()
            printer = database.Printer.from_dictionary(printerData)
            printer.insert()
            
            self.mainWindow.printerComboBox.addItem(printer.name)
            self.mainWindow.printerComboBox.setCurrentText(printer.name)
            self.reloadMaterials()
            self.mainWindow.printerEditButton.setEnabled(True)
            self.mainWindow.printerDeleteButton.setEnabled(True)
    
    def editPrinter(self):
        selectedName = self.mainWindow.printerComboBox.currentText()
        
        printer = database.Printer.from_name(selectedName)
        id = printer.id
        
        if printer is None:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Data Integrity Warning")
            msg.setText("Could not find selected printer.")
            msg.setDetailedText(f"Failed to find printer:\n   '{selectedName}'.")
            
            msg.exec_()
            return
            
        self.printerDialog.loadData(printer)
        
        self.printerDialog.window.exec()
        
        if self.printerDialog.validateForm():
            printerData = self.printerDialog.getFormData()
            printer = database.Printer.from_dictionary(printerData)
            printer.update(id)
            self.reloadMaterials()
        
    def deletePrinter(self):
        selectedName = self.mainWindow.printerComboBox.currentText()
        selectedIndex = self.mainWindow.printerComboBox.currentIndex()
        
        if len(selectedName) > 0:
            buttonReply = QMessageBox.question(self, "Printer Delete", f"Are you sure you want to delete '{selectedName}'", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if buttonReply == QMessageBox.No:
                return
        
            printer = database.Printer.from_name(selectedName)
            id = printer.id
            printer.delete(id)
            self.mainWindow.printerComboBox.removeItem(selectedIndex)
            printers = database.Printer.find_all()
            if len(printers) <= 0:
                self.mainWindow.printerEditButton.setEnabled(False)
                self.mainWindow.printerDeleteButton.setEnabled(False)
    
    def addMaterial(self):
        selectedPrinterName = self.mainWindow.printerComboBox.currentText()
        printer = database.Printer.from_name(selectedPrinterName)
        
        self.materialDialog.clearForm()
        self.materialDialog.materialTypeComboBox.setCurrentText(printer.materialType.name)
        
        self.materialDialog.window.exec()
        if self.materialDialog.validateForm():
            materialData = self.materialDialog.getFormData()
            material = database.Material.from_dictionary(materialData)
            material.insert()
            self.mainWindow.materialComboBox.addItem(material.name)
            self.mainWindow.materialComboBox.setCurrentText(material.name)
            self.recalculate()
            self.mainWindow.materialEditButton.setEnabled(True)
            self.mainWindow.materialDeleteButton.setEnabled(True)
    
    def editMaterial(self):
        selectedName = self.mainWindow.materialComboBox.currentText()
        selectedIndex = self.mainWindow.materialComboBox.currentIndex()
        
        material = database.Material.from_name(selectedName)
        id = material.id
        
        if material is None:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Data Integrity Warning")
            msg.setText("Could not find selected material.")
            msg.setDetailedText(f"Failed to find material:\n   '{selectedName}'.")
            
            msg.exec_()
            return
            
        self.materialDialog.loadData(material)
        
        self.materialDialog.window.exec()
        if self.materialDialog.validateForm():
            materialData = self.materialDialog.getFormData()
            material = database.Material.from_dictionary(materialData)
            material.update(id)
            self.mainWindow.materialComboBox.setItemText(selectedIndex, materialData["Name"])
            self.recalculate()

    def deleteMaterial(self):
        selectedName = self.mainWindow.materialComboBox.currentText()
        selectedIndex = self.mainWindow.materialComboBox.currentIndex()
        
        if len(selectedName) > 0:
            buttonReply = QMessageBox.question(self, "Material Delete", f"Are you sure you want to delete '{selectedName}'", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if buttonReply == QMessageBox.No:
                return
            
            material = database.Material.from_name(selectedName)
            id = material.id
            material.delete(id)
            self.mainWindow.materialComboBox.removeItem(selectedIndex)
            
            materials = database.Material.find_all()
            if len(materials) <= 0:
                self.mainWindow.materialEditButton.setEnabled(False)
                self.mainWindow.materialDeleteButton.setEnabled(False)
    
    
    def openSettings(self):
        settings = {}
        settings["Energy Cost"] = database.Setting.from_name("Energy Cost").value
        settings["Labor Rate"] = database.Setting.from_name("Labor Rate").value
        settings["Failure Rate"] = database.Setting.from_name("Failure Rate").value
        
        self.settingsDialog.loadData(settings)
        self.settingsDialog.window.exec()
        settings = self.settingsDialog.getFormData()
        
        for key in settings:
            setting = database.Setting.from_name(key)
            setting.value = settings[key]
            setting.update()
    
    def recalculate(self):
        try:
            self.calculateMaterialCost()
            self.calculateElectricityCost()
            self.calculatePrinterDepreciationCost()
            self.calculateTotalPreparation()
            self.calculateTotalPostProcessing()
            self.calculateTotalOther()
            self.calculateTotalCost()
            self.calculateQuote()
        except Exception:
            pass

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
        
        material = database.Material.from_name(materialName)
        modelWeight = self.mainWindow.modelWeightDoubleSpinBox.value()
    
        total = (material.price / material.quantity) * modelWeight
        self.mainWindow.materialCostDoubleSpinBox.setValue(total)
    
    def calculateElectricityCost(self):
        printerName = self.mainWindow.printerComboBox.currentText()
        printer = database.Printer.from_name(printerName)
        printTime = self.mainWindow.printTimeDoubleSpinBox.value()
        
        totalEnergyUsage = printer.energyConsumption * (printTime / 60)
        
        total = totalEnergyUsage * database.Setting.from_name("Energy Cost").value
        self.mainWindow.electricityCostDoubleSpinBox.setValue(total)
    
    def calculatePrinterDepreciationCost(self):
        printerName = self.mainWindow.printerComboBox.currentText()
        printer = database.Printer.from_name(printerName)
        
        printTime = self.mainWindow.printTimeDoubleSpinBox.value()

        total = (printTime / 60) * printer.deprecationPerHour
        self.mainWindow.printerDepreciationCostDoubleSpinBox.setValue(total)
    
    def calculateTotalPreparation(self):
        laborRateMinutes = database.Setting.from_name("Labor Rate").value / 60
        
        modelPrepTime = self.mainWindow.modelPrepTimeDoubleSpinBox.value()
        slicingTime = self.mainWindow.slicingPrepTimeDoubleSpinBox.value()
        materialChangeTime = self.mainWindow.materialChangePrepTimeDoubleSpinBox.value()
        transferStartTime = self.mainWindow.transferStartPrepTimeDoubleSpinBox.value()

        total = (modelPrepTime + slicingTime + materialChangeTime + transferStartTime) * laborRateMinutes
        
        self.mainWindow.prepCostDoubleSpinBox.setValue(total)
        
    def calculateTotalPostProcessing(self):
        laborRateMinutes = database.Setting.from_name("Labor Rate").value / 60
        
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
        failureRateValue = database.Setting.from_name("Failure Rate").value
        
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
    database.create_blank_database()
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())