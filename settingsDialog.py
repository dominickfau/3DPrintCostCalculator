from PyQt5.QtWidgets import (
    QDialog
)

from ui.settingsDialog import Ui_SettingsDialog

class SettingsDialog(Ui_SettingsDialog):
    def __init__(self):
        self.window = QDialog()
        self.setupUi(self.window)
        
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
            "Energy Cost": energyCost,
            "Labor Rate": laborRate,
            "Failure Rate": failureRate
        }
        
        return formData
    
    def loadData(self, settings):
        self.clearForm()
        energyCost = settings["Energy Cost"]
        laborRate = settings["Labor Rate"]
        failureRate = settings["Failure Rate"]
        
        energyCost = self.energyCostDoubleSpinBox.setValue(energyCost)
        laborRate = self.laborCostDoubleSpinBox.setValue(laborRate)
        failureRate = self.failureRateDoubleSpinBox.setValue(failureRate)