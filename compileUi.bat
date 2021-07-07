pyuic5 .\ui\CalculateServiceCostDialog.ui -o .\ui\calculateServiceCostDialog.py
pyuic5 .\ui\PrinterDialog.ui -o .\ui\printerDialog.py
pyuic5 .\ui\MaterialDialog.ui -o .\ui\materialDialog.py
pyuic5 .\ui\MainWindow.ui -o .\ui\mainWindow.py
pyuic5 .\ui\SettingsDialog.ui -o .\ui\settingsDialog.py
pyrcc5 -o .\ui\Resource_rc.py .\ui\Resource.qrc

python .\fixImportLine.py