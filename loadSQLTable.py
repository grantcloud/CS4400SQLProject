from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtSql import QSqlTableModel
from PyQt5.QtSql import *

def loadTable(table, querydata, header, attNo):
    table.setRowCount(0)
    table.setColumnCount(attNo + 1)
    table.setHorizontalHeaderLabels(header)
    table.verticalHeader().hide()
    table.horizontalHeader().setSortIndicatorShown(True)
    checkboxList = []
    if table.count == 1:
        for row_number, row_data in enumerate(querydata):
            item = QCheckBox()
            item.setStyleSheet("margin-left:50%; margin-right:50%;")
            checkboxList.append(item)
            # first we insert a row then the data is inserted
            table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                cell = QtWidgets.QTableWidgetItem(str(row_data[data]))
                cell.setFlags(QtCore.Qt.ItemIsEnabled)
                table.setItem(row_number, column_number + 1, cell)
            table.setCellWidget(row_number, 0, item)
    else:
        table.count = 1
    return checkboxList

def loadTableNoCheck(table, querydata, header, attNo):
    table.setRowCount(0)
    table.setColumnCount(attNo)
    table.setHorizontalHeaderLabels(header)
    table.verticalHeader().hide()
    table.horizontalHeader().setSortIndicatorShown(True)
    if table.count == 1:
            for row_number, row_data in enumerate(querydata):
                # first we insert a row then the data is inserted
                table.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    cell = QtWidgets.QTableWidgetItem(str(row_data[data]))
                    cell.setFlags(QtCore.Qt.ItemIsEnabled)
                    table.setItem(row_number, column_number, cell)
    else:
        table.count = 1


def loadExhibit(combobox, querydata):
    combobox.addItem("")
    for row_number, row_data in enumerate(querydata):
        for column_number, data in enumerate(row_data):
            combobox.addItem(str(data))

def loadRow(querydata):
    rowList = []
    for row_number, row_data in enumerate(querydata):
        for column_number, data in enumerate(row_data):
            rowList.append(str(data))

    return rowList
