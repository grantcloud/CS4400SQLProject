# CS4400
# Team 71
# ProjectGUI

import PyMySQLQs
import sys
import csv
import datetime
from datetime import datetime
import re
from typing import *
from loadSQLTable import *
from PyQt5.QtCore import Qt, QAbstractTableModel, QVariant
from PyQt5.QtWidgets import (
    QSpacerItem,
    QComboBox,
    QListWidget,
    QListWidgetItem,
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QPlainTextEdit,
    QListView,
    QAbstractItemView,
    QMessageBox,
    QLineEdit,
    QTableView, QDialog, qApp, QGroupBox, QFormLayout, QDialogButtonBox, QGridLayout)
from PyQt5.QtGui import (
    QStandardItemModel,
    QStandardItem,
    QPixmap,
    QIcon)


#############Global Variables#################
states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

bColor = "background-color:rgb(51, 153, 255)" #this is the light blue button color

#--- 1  ---#
class DbLoginDialog(QDialog):
    def __init__(self):
        super(DbLoginDialog, self).__init__()
        self.setModal(True)
        self.setWindowTitle("Atlanta Beltline Database")
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.icon = "buzz.png"
        self.setWindowIcon(QIcon(self.icon))
        self.GUI()
        self.connections()


    def GUI(self):
        self.vbox = QVBoxLayout()
        self.hbox1 = QHBoxLayout()
        self.title = QLabel("Atlanta Beltline Login")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font: 12pt;")
        self.hbox1.addWidget(self.title)
        self.grid = QGridLayout()
        self.emailTitle = QLabel("Email")
        self.emailTextBox = QLineEdit("")
        self.passwordTitle = QLabel("Password")
        self.passwordTextBox = QLineEdit("")
        self.grid.addWidget(self.emailTitle, 0, 1)
        self.grid.addWidget(self.emailTextBox, 0, 2)
        self.grid.addWidget(self.passwordTitle, 1, 1)
        self.grid.addWidget(self.passwordTextBox, 1, 2)
        self.hbox4 = QHBoxLayout()
        self.loginButton = QPushButton("Login")
        self.loginButton.setStyleSheet(bColor)
        self.registerButton = QPushButton("Register")
        self.registerButton.setStyleSheet(bColor)
        self.hbox4.addWidget(self.loginButton)
        self.hbox4.addWidget(self.registerButton)
        self.vbox.addLayout(self.hbox1)
        self.vbox.addLayout(self.grid)
        self.vbox.addLayout(self.hbox4)
        self.setLayout(self.vbox)

    def connections(self):
        self.registerButton.clicked.connect(self.registerUser)
        self.loginButton.clicked.connect(self.GetUserType)

    ##### What each button does when clicked ####
    #Takes you to register navigation page
    def registerUser(self):
        self.registerNav = RegisterNavigation()
        self.registerNav.show()

    #take you to the login placeholder screen
    def GetUserType(self):
        self.email = self.emailTextBox.text()
        exists = PyMySQLQs.login(self.email, self.passwordTextBox.text())
        # exists is a tuple (1, usertype) if user or visitor or master
        #exists = (1, usertype, employeetype) if an employee
        if exists:
            self.getUsername()
            #If the employee is just an employee
            if exists[1] == 'Visitor':
                self.usertype = 'Visitor'
                self.a = VisitorFunctionality(self.email, self.usertype, self.username)
            elif exists[1] == 'User':
                self.usertype = 'User'
                self.a = UserFunctionality(self.email, self.usertype, self.username)
            elif exists[1] == 'Master':
                self.usertype = 'Master'
                self.a = Placeholder(self.email, self.usertype, self.username)
            else:
                if exists[1] == 'Employee':
                    if exists[2] == 'Manager':
                        self.usertype = "Manager-Only"
                        self.a = ManagerFunctionality(self.email, self.usertype, self.username)
                    elif exists[2] == 'Staff':
                        self.usertype = 'Staff-Only'
                        self.a = StaffFunctionality(self.email,self.usertype, self.username)
                    elif exists[2] == 'Admin':
                        self.usertype = "Admin-Only"
                        self.a = AdminFunctionality(self.email, self.usertype, self.username)
                elif exists[1] == 'Employee-Visitor':
                    if exists[2] == 'Manager':
                        self.usertype = 'Manager-Visitor'
                        self.a = ManagerVisFunctionality(self.email, self.usertype, self.username)
                    elif exists[2] == 'Staff':
                        self.usertype = "Staff-Visitor"
                        self.a = StaffVisFunctionality(self.email, self.usertype, self.username)
                    elif exists[2] == 'Admin':
                        self.usertype = "Admin-Visitor"
                        self.a = AdminVisFunctionality(self.email, self.usertype, self.username)
            print(self.usertype, self.username)
            self.initViews()
            self.a.show()
        else:
            msgBox = QMessageBox()
            msgBox.setText("Invalid username/password combination. Please try again")
            msgBox.setWindowTitle("Notification")
            msgBox.exec_()

    def initViews(self):
        PyMySQLQs.InitViews(self.username)

    def getUsername(self):
        self.username = PyMySQLQs.getUsername(self.email)

#############################################################
#                                                           #
#                                                           #
#                      Registration Side                    #
#                                                           #
#                                                           #
#############################################################
#--- 2 ---#
class RegisterNavigation(QDialog):
    def __init__(self):
        super(RegisterNavigation, self).__init__()
        self.setModal(True)
        self.setWindowTitle("Atlanta Beltline Database")
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.icon = "buzz.png"
        self.setWindowIcon(QIcon(self.icon))
        self.GUI()
        self.connections()

    def GUI(self):
        self.grid = QGridLayout()
        self.title = QLabel("Register Navigation")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font: 20pt;")
        self.uButton = QPushButton("User Only")
        self.uButton.setStyleSheet(bColor)
        self.vButton = QPushButton("Visitor Only")
        self.vButton.setStyleSheet(bColor)
        self.eButton = QPushButton("Employee Only")
        self.eButton.setStyleSheet(bColor)
        self.evButton = QPushButton("Employee-Visitor")
        self.evButton.setStyleSheet(bColor)
        self.backButton = QPushButton("Back")
        self.backButton.setStyleSheet(bColor)
        self.grid.addWidget(self.title, 0, 1)
        self.grid.addWidget(self.uButton, 1, 1)
        self.grid.addWidget(self.vButton, 2, 1)
        self.grid.addWidget(self.eButton, 3, 1)
        self.grid.addWidget(self.evButton, 4, 1)
        self.grid.addWidget(self.backButton, 5, 1)
        self.setLayout(self.grid)

    def connections(self):
        self.uButton.clicked.connect(self.uRegistration)
        self.vButton.clicked.connect(self.vRegistration)
        self.eButton.clicked.connect(self.eRegistration)
        self.evButton.clicked.connect(self.evRegistration)
        self.backButton.clicked.connect(self.backtoLogin)

    #Back to the login page
    def backtoLogin(self):
        self.close()

    #User Registration
    def uRegistration(self):
        self.uOnlyReg = RegisterUserOnly()
        self.uOnlyReg.show()
        self.close()

    #Visitor Registration
    def vRegistration(self):
        self.vOnlyReg = RegisterVisitorOnly()
        self.vOnlyReg.show()
        self.close()

    #Employee Registration
    def eRegistration(self):
        self.eOnlyReg = RegisterEmployeeOnly()
        self.eOnlyReg.show()
        self.close()

    #Employee-Visitor Registration
    def evRegistration(self):
        self.evOnlyReg = RegisterEmployeeVis()
        self.evOnlyReg.show()
        self.close()

#--- 3 ---#
class RegisterUserOnly(QDialog):
    def __init__(self):
        super(RegisterUserOnly, self).__init__()
        self.setModal(True)
        self.setWindowTitle("Atlanta Beltline Database")
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.icon = "buzz.png"
        self.setWindowIcon(QIcon(self.icon))
        self.GUI()
        self.connections()

    def GUI(self):
        self.vbox = QVBoxLayout()
        self.hbox1 = QHBoxLayout()
        self.title = QLabel("Register User")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font: 12pt;")
        self.hbox1.addWidget(self.title)
        self.grid = QGridLayout()
        self.fnameEdit = QLineEdit("")
        self.fname = QLabel("First Name")
        self.lnameEdit = QLineEdit("")
        self.lname = QLabel("Last Name")
        self.userEdit = QLineEdit("")
        self.username = QLabel("Username")
        self.passEdit = QLineEdit("")
        self.password = QLabel("Password")
        self.confEdit = QLineEdit("")
        self.confirm = QLabel("Confirm Password")
        self.grid.addWidget(self.fname, 0, 1)
        self.grid.addWidget(self.fnameEdit, 0, 2)
        self.grid.addWidget(self.lname, 0, 3)
        self.grid.addWidget(self.lnameEdit, 0, 4)
        self.grid.addWidget(self.username, 1, 1)
        self.grid.addWidget(self.userEdit, 1, 2)
        self.grid.addWidget(self.password, 2, 1)
        self.grid.addWidget(self.passEdit, 2, 2)
        self.grid.addWidget(self.confirm, 2, 3)
        self.grid.addWidget(self.confEdit, 2, 4)
        self.hbox5 = QHBoxLayout()
        self.emailEdit = QLineEdit("")
        self.email = QLabel("Email")
        self.emailAdd = QPushButton("Add")
        self.hbox5.addWidget(self.email)
        self.hbox5.addWidget(self.emailEdit)
        self.hbox5.addWidget(self.emailAdd)
        self.hboxEmail = QHBoxLayout()
        self.emailWidget = QListWidget()
        self.removeButton = QPushButton("Remove Selected Email")
        self.hboxEmail.addWidget(QLabel("Emails"))
        self.hboxEmail.addWidget(self.emailWidget)
        self.hboxEmail.addWidget(self.removeButton)
        self.hbox6 = QHBoxLayout()
        self.backButton = QPushButton("Back")
        self.backButton.setStyleSheet(bColor)
        self.registerButton = QPushButton("Register")
        self.registerButton.setStyleSheet(bColor)
        self.hbox6.addWidget(self.backButton)
        self.hbox6.addWidget(self.registerButton)
        self.vbox.addLayout(self.hbox1)
        self.vbox.addLayout(self.grid)
        self.vbox.addLayout(self.hbox5)
        self.vbox.addLayout(self.hboxEmail)
        self.vbox.addLayout(self.hbox6)
        self.setLayout(self.vbox)

    def connections(self):
        self.emailAdd.clicked.connect(self.addingEmail)
        self.backButton.clicked.connect(self.backReg)
        self.removeButton.clicked.connect(self.removeSel)
        self.registerButton.clicked.connect(self.addUser)

    #Back to the registration navigation, doesn't save any info from previous page
    def backReg(self):
        self.backtoReg = RegisterNavigation()
        self.backtoReg.show()
        self.close()

    #Adds an email to the Emails list
    def addingEmail(self):
        email = self.emailEdit.text()
        #placeholder regex, need someone to go through and do te regex they specify
        #need to write a query in here as an elif statement to check if the email is unique
        if not re.match(r"[A-Za-z0-9]*@[A-Za-z0-9]*[.][A-Za-z0-9]*", email):
            print('email is not valid')
            msgBox = QMessageBox()
            msgBox.setText("Please enter an email in the following format: EmailAdress@ServiceProivder.domain")
            msgBox.setWindowTitle("Notification")
            msgBox.exec_()
        elif PyMySQLQs.checkemail(email):
            msgBox = QMessageBox()
            msgBox.setText("This email is already in the database. Please enter another email.")
            msgBox.setWindowTitle("Notification")
            msgBox.exec_()
        else:
            print('email is valid')
            self.emailWidget.addItem(email)
            self.emailEdit.clear()

    #Removes the selected email from the list
    def removeSel(self):
        listItems = self.emailWidget.selectedItems()
        if not listItems: return
        for item in listItems:
            self.emailWidget.takeItem(self.emailWidget.row(item))

    #registers the user into the database
    def addUser(self):
        fname = self.fnameEdit.text()
        lname = self.lnameEdit.text()
        username = self.userEdit.text()
        password = self.passEdit.text()
        confirmPass = self.confEdit.text()
        emaillist = [str(self.emailWidget.item(i).text()) for i in range(self.emailWidget.count())]
        if PyMySQLQs.registerusercheck(fname, lname, username, password, confirmPass, emaillist):
            msgBox = QMessageBox()
            msgBox.setText("{}".format(PyMySQLQs.registerusercheck(fname, lname, username, password, confirmPass, emaillist)))
            msgBox.setWindowTitle("Notification")
            msgBox.exec_()

        else:
            PyMySQLQs.registeruser(fname, lname, username, password, emaillist)
            msgBox = QMessageBox()
            msgBox.setText("Registration Successful!")
            msgBox.setWindowTitle("Notification")
            msgBox.exec_()

#--- 4 ---#
class RegisterVisitorOnly(QDialog):
    global countVis
    def __init__(self):
        super(RegisterVisitorOnly, self).__init__()
        self.setModal(True)
        self.setWindowTitle("Atlanta Beltline Database")
        self.setWindowFlags(Qt.WindowCloseButtonHint)


        self.vbox = QVBoxLayout()

        self.title = QLabel("Register Visitor")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font: 12pt;")
        self.fnameEdit = QLineEdit("")
        self.fname = QLabel("First Name")
        self.lnameEdit = QLineEdit("")
        self.lname = QLabel("Last Name")
        self.userEdit = QLineEdit("")
        self.username = QLabel("Username")
        self.passEdit = QLineEdit("")
        self.password = QLabel("Password")
        self.confEdit = QLineEdit("")
        self.confirm = QLabel("Confirm Password")
        self.emailEdit = QLineEdit("")
        self.email = QLabel("Email")
        self.emailAdd = QPushButton("Add")
        self.backButton = QPushButton("Back")
        self.backButton.setStyleSheet(bColor)
        self.registerButton = QPushButton("Register")
        self.registerButton.setStyleSheet(bColor)

        self.hbox1 = QHBoxLayout()
        self.hbox5 = QHBoxLayout()
        self.hbox6 = QHBoxLayout()

        self.grid = QGridLayout()

        self.hbox1.addWidget(self.title)
        self.grid.addWidget(self.fname, 0, 1)
        self.grid.addWidget(self.fnameEdit, 0, 2)
        self.grid.addWidget(self.lname, 0, 3)
        self.grid.addWidget(self.lnameEdit, 0, 4)
        self.grid.addWidget(self.username, 1, 1)
        self.grid.addWidget(self.userEdit, 1, 2)
        self.grid.addWidget(self.password, 2, 1)
        self.grid.addWidget(self.passEdit, 2, 2)
        self.grid.addWidget(self.confirm, 2, 3)
        self.grid.addWidget(self.confEdit, 2, 4)
        self.hbox5.addWidget(self.email)
        self.hbox5.addWidget(self.emailEdit)
        self.hbox5.addWidget(self.emailAdd)
        self.hbox6.addWidget(self.backButton)
        self.hbox6.addWidget(self.registerButton)


        self.emailAdd.clicked.connect(self.addingEmail)
        self.emailAdd.setEnabled(True)

        self.vbox.addLayout(self.hbox1)
        self.vbox.addLayout(self.grid)
        self.vbox.addLayout(self.hbox5)
        self.vbox.addLayout(self.hbox6)


        self.setLayout(self.vbox)

    def connections(self):
        self.emailAdd.clicked.connect(self.addingEmail)
        self.backButton.clicked.connect(self.backReg)
        self.removeButton.clicked.connect(self.removeSel)
        self.registerButton.clicked.connect(self.addUser)


    def backReg(self):
        self.backtoReg = RegisterNavigation()
        self.backtoReg.show()
        self.close()

    def addingEmail(self):
        email = self.emailEdit.text()
        #placeholder regex, need someone to go through and do te regex they specify
        #need to write a query in here as an elif statement to check if the email is unique
        if not re.match(r"[A-Za-z0-9]*@[A-Za-z0-9]*[.][A-Za-z0-9]*", email):
            print('email is not valid')
            msgBox = QMessageBox()
            msgBox.setText("Please enter an email in the following format: EmailAdress@ServiceProivder.domain")
            msgBox.setWindowTitle("Notification")
            msgBox.exec_()
        elif PyMySQLQs.checkemail(email):
            msgBox = QMessageBox()
            msgBox.setText("This email is already in the database. Please enter another email.")
            msgBox.setWindowTitle("Notification")
            msgBox.exec_()
        else:
            print('email is valid')
            self.emailWidget.addItem(email)
            self.emailEdit.clear()

    #Removes the selected email from the list
    def removeSel(self):
        listItems = self.emailWidget.selectedItems()
        if not listItems: return
        for item in listItems:
            self.emailWidget.takeItem(self.emailWidget.row(item))

    def addUser(self):
        fname = self.fnameEdit.text()
        lname = self.lnameEdit.text()
        username = self.userEdit.text()
        password = self.passEdit.text()
        confirmPass = self.confEdit.text()
        emaillist = [str(self.emailWidget.item(i).text()) for i in range(self.emailWidget.count())]
        if PyMySQLQs.registerusercheck(fname, lname, username, password, confirmPass, emaillist):
            msgBox = QMessageBox()
            msgBox.setText("{}".format(PyMySQLQs.registerusercheck(fname, lname, username, password, confirmPass, emaillist)))
            msgBox.setWindowTitle("Notification")
            msgBox.exec_()

        else:
            PyMySQLQs.registervisitor(fname, lname, username, password, emaillist)
            msgBox = QMessageBox()
            msgBox.setText("Registration Successful!")
            msgBox.setWindowTitle("Notification")
            msgBox.exec_()


#--- 5 ---#
class RegisterEmployeeOnly(QDialog):
    def __init__(self):
        super(RegisterEmployeeOnly, self).__init__()
        self.setModal(True)
        self.setWindowTitle("Atlanta Beltline Database")
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.icon = "buzz.png"
        self.setWindowIcon(QIcon(self.icon))
        self.GUI()
        self.connections()

    def GUI(self):
        self.vbox = QVBoxLayout()
        self.hbox1 = QHBoxLayout()
        self.title = QLabel("Register Employee")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font: 12pt;")
        self.hbox1.addWidget(self.title)
        self.vbox.addLayout(self.hbox1)
        self.grid1 = QGridLayout()
        self.fnameEdit = QLineEdit("")
        self.fname = QLabel("First Name")
        self.lnameEdit = QLineEdit("")
        self.lname = QLabel("Last Name")
        self.userEdit = QLineEdit("")
        self.username = QLabel("Username")
        self.userType = QLabel("User Type")
        self.userDrop = QComboBox()
        self.userDrop.addItems(["Manager","Staff"])
        self.passEdit = QLineEdit("")
        self.password = QLabel("Password")
        self.confEdit = QLineEdit("")
        self.confirm = QLabel("Confirm Password")
        self.grid1.addWidget(self.fname, 0, 1)
        self.grid1.addWidget(self.fnameEdit, 0, 2)
        self.grid1.addWidget(self.lname, 0, 3)
        self.grid1.addWidget(self.lnameEdit, 0, 4)
        self.grid1.addWidget(self.username, 1, 1)
        self.grid1.addWidget(self.userEdit, 1, 2)
        self.grid1.addWidget(self.userType, 1, 3)
        self.grid1.addWidget(self.userDrop, 1, 4)
        self.grid1.addWidget(self.password, 2, 1)
        self.grid1.addWidget(self.passEdit, 2, 2)
        self.grid1.addWidget(self.confirm, 2, 3)
        self.grid1.addWidget(self.confEdit, 2, 4)
        self.vbox.addLayout(self.grid1)
        self.hbox2 = QHBoxLayout()
        self.phone = QLabel("Phone")
        self.phoneEdit = QLineEdit("")
        self.address = QLabel("Address")
        self.addressEdit = QLineEdit("")
        self.hbox2.addWidget(self.phone)
        self.hbox2.addWidget(self.phoneEdit)
        self.hbox2.addWidget(self.address)
        self.hbox2.addWidget(self.addressEdit)
        self.vbox.addLayout(self.hbox2)
        self.hbox3 = QHBoxLayout()
        self.city = QLabel("City")
        self.cityEdit = QLineEdit("")
        self.state = QLabel("State")
        self.stateDrop = QComboBox()
        self.stateDrop.addItems(states)
        self.zipcode = QLabel("Zipcode")
        self.zipEdit = QLineEdit("")
        self.hbox3.addWidget(self.city)
        self.hbox3.addWidget(self.cityEdit)
        self.hbox3.addWidget(self.state)
        self.hbox3.addWidget(self.stateDrop)
        self.hbox3.addWidget(self.zipcode)
        self.hbox3.addWidget(self.zipEdit)
        self.vbox.addLayout(self.hbox3)
        self.hbox5 = QHBoxLayout()
        self.emailEdit = QLineEdit("")
        self.email = QLabel("Email")
        self.emailAdd = QPushButton("Add")
        self.hbox5.addWidget(self.email)
        self.hbox5.addWidget(self.emailEdit)
        self.hbox5.addWidget(self.emailAdd)
        self.vbox.addLayout(self.hbox5)
        self.hboxEmail = QHBoxLayout()
        self.emailWidget = QListWidget()
        self.removeButton = QPushButton("Remove Selected Email")
        self.hboxEmail.addWidget(QLabel("Emails"))
        self.hboxEmail.addWidget(self.emailWidget)
        self.hboxEmail.addWidget(self.removeButton)
        self.vbox.addLayout(self.hboxEmail)
        self.hbox6 = QHBoxLayout()
        self.backButton = QPushButton("Back")
        self.backButton.setStyleSheet(bColor)
        self.registerButton = QPushButton("Register")
        self.registerButton.setStyleSheet(bColor)
        self.hbox6 = QHBoxLayout()
        self.hbox6.addWidget(self.backButton)
        self.hbox6.addWidget(self.registerButton)
        self.vbox.addLayout(self.hbox6)
        self.setLayout(self.vbox)

    def connections(self):
        self.emailAdd.clicked.connect(self.addingEmail)
        self.backButton.clicked.connect(self.backReg)
        self.removeButton.clicked.connect(self.removeSel)
        self.registerButton.clicked.connect(self.addUser)

    def backReg(self):
        self.backtoReg = RegisterNavigation()
        self.backtoReg.show()
        self.close()

    def addingEmail(self):
        email = self.emailEdit.text()
        if not re.match(r"[A-Za-z0-9]*@[A-Za-z0-9]*[.][A-Za-z0-9]*", email):
            print('email is not valid')
            msgBox = QMessageBox()
            msgBox.setText("Please enter an email in the following format: EmailAdress@ServiceProivder.domain")
            msgBox.setWindowTitle("Notification")
            msgBox.exec_()
        elif PyMySQLQs.checkemail(email):
            msgBox = QMessageBox()
            msgBox.setText("This email is already in the database. Please enter another email.")
            msgBox.setWindowTitle("Notification")
            msgBox.exec_()
        else:
            print('email is valid')
            self.emailWidget.addItem(email)
            self.emailEdit.clear()

    def removeSel(self):
        listItems = self.emailWidget.selectedItems()
        if not listItems: return
        for item in listItems:
            self.emailWidget.takeItem(self.emailWidget.row(item))

    def addUser(self):
        fname = self.fnameEdit.text()
        lname = self.lnameEdit.text()
        username = self.userEdit.text()
        password = self.passEdit.text()
        confirmPass = self.confEdit.text()
        phone = self.phoneEdit.text()
        address = self.addressEdit.text()
        city = self.cityEdit.text()
        state = self.stateDrop.currentText()
        zipcode = self.zipEdit.text()
        emptype = self.userDrop.currentText()
        emailList = [str(self.emailWidget.item(i).text()) for i in range(self.emailWidget.count())]
        if PyMySQLQs.registeremployeecheck(fname, lname, username, emptype, password, confirmPass, phone, address, city, state, zipcode, emailList):
            msgBox = QMessageBox()
            msgBox.setText("{}".format(PyMySQLQs.registeremployeecheck(fname, lname, username, emptype, password, confirmPass, phone, address, city, state, zipcode, emailList)))
            msgBox.setWindowTitle("Notification")
            msgBox.exec_()

        else:
            PyMySQLQs.registeremployee(fname, lname, username, emptype, password, confirmPass, phone, address, city, state, zipcode, emailList)
            msgBox = QMessageBox()
            msgBox.setText("Registration Successful!")
            msgBox.setWindowTitle("Notification")
            msgBox.exec_()
#--- 6 ---#
#### Changed addingUser function 4/16
class RegisterEmployeeVis(QDialog):
    def __init__(self):
        super(RegisterEmployeeVis, self).__init__()
        self.setModal(True)
        self.setWindowTitle("Atlanta Beltline Database")
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.icon = "buzz.png"
        self.setWindowIcon(QIcon(self.icon))
        self.GUI()
        self.connections()
    def GUI(self):
        self.vbox = QVBoxLayout()
        self.hbox1 = QHBoxLayout()
        self.title = QLabel("Register Employee Visitor")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font: 12pt;")
        self.hbox1.addWidget(self.title)
        self.vbox.addLayout(self.hbox1)
        self.grid1 = QGridLayout()
        self.fnameEdit = QLineEdit("")
        self.fname = QLabel("First Name")
        self.lnameEdit = QLineEdit("")
        self.lname = QLabel("Last Name")
        self.userEdit = QLineEdit("")
        self.username = QLabel("Username")
        self.userType = QLabel("User Type")
        self.userDrop = QComboBox()
        self.userDrop.addItems(["Manager","Staff"])
        self.passEdit = QLineEdit("")
        self.password = QLabel("Password")
        self.confEdit = QLineEdit("")
        self.confirm = QLabel("Confirm Password")
        self.grid1.addWidget(self.fname, 0, 1)
        self.grid1.addWidget(self.fnameEdit, 0, 2)
        self.grid1.addWidget(self.lname, 0, 3)
        self.grid1.addWidget(self.lnameEdit, 0, 4)
        self.grid1.addWidget(self.username, 1, 1)
        self.grid1.addWidget(self.userEdit, 1, 2)
        self.grid1.addWidget(self.userType, 1, 3)
        self.grid1.addWidget(self.userDrop, 1, 4)
        self.grid1.addWidget(self.password, 2, 1)
        self.grid1.addWidget(self.passEdit, 2, 2)
        self.grid1.addWidget(self.confirm, 2, 3)
        self.grid1.addWidget(self.confEdit, 2, 4)
        self.vbox.addLayout(self.grid1)
        self.hbox2 = QHBoxLayout()
        self.phone = QLabel("Phone")
        self.phoneEdit = QLineEdit("")
        self.address = QLabel("Address")
        self.addressEdit = QLineEdit("")
        self.hbox2.addWidget(self.phone)
        self.hbox2.addWidget(self.phoneEdit)
        self.hbox2.addWidget(self.address)
        self.hbox2.addWidget(self.addressEdit)
        self.vbox.addLayout(self.hbox2)
        self.hbox3 = QHBoxLayout()
        self.city = QLabel("City")
        self.cityEdit = QLineEdit("")
        self.state = QLabel("State")
        self.stateDrop = QComboBox()
        self.stateDrop.addItems(states)
        self.zipcode = QLabel("Zipcode")
        self.zipEdit = QLineEdit("")
        self.hbox3.addWidget(self.city)
        self.hbox3.addWidget(self.cityEdit)
        self.hbox3.addWidget(self.state)
        self.hbox3.addWidget(self.stateDrop)
        self.hbox3.addWidget(self.zipcode)
        self.hbox3.addWidget(self.zipEdit)
        self.vbox.addLayout(self.hbox3)
        self.hbox5 = QHBoxLayout()
        self.emailEdit = QLineEdit("")
        self.email = QLabel("Email")
        self.emailAdd = QPushButton("Add")
        self.hbox5.addWidget(self.email)
        self.hbox5.addWidget(self.emailEdit)
        self.hbox5.addWidget(self.emailAdd)
        self.vbox.addLayout(self.hbox5)
        self.hboxEmail = QHBoxLayout()
        self.emailWidget = QListWidget()
        self.removeButton = QPushButton("Remove Selected Email")
        self.hboxEmail.addWidget(QLabel("Emails"))
        self.hboxEmail.addWidget(self.emailWidget)
        self.hboxEmail.addWidget(self.removeButton)
        self.vbox.addLayout(self.hboxEmail)
        self.hbox6 = QHBoxLayout()
        self.backButton = QPushButton("Back")
        self.backButton.setStyleSheet(bColor)
        self.registerButton = QPushButton("Register")
        self.registerButton.setStyleSheet(bColor)
        self.hbox6 = QHBoxLayout()
        self.hbox6.addWidget(self.backButton)
        self.hbox6.addWidget(self.registerButton)
        self.vbox.addLayout(self.hbox6)
        self.setLayout(self.vbox)

    def connections(self):
        self.emailAdd.clicked.connect(self.addingEmail)
        self.backButton.clicked.connect(self.backReg)
        self.removeButton.clicked.connect(self.removeSel)
        self.registerButton.clicked.connect(self.addUser)

    def backReg(self):
        self.backtoReg = RegisterNavigation()
        self.backtoReg.show()
        self.close()

    #Adds an email to the Emails list
    def addingEmail(self):
        email = self.emailEdit.text()
        if not re.match(r"[A-Za-z0-9]*@[A-Za-z0-9]*[.][A-Za-z0-9]*", email):
            print('email is not valid')
            msgBox = QMessageBox()
            msgBox.setText("Please enter an email in the following format: EmailAdress@ServiceProivder.domain")
            msgBox.setWindowTitle("Notification")
            msgBox.exec_()
        elif PyMySQLQs.checkemail(email):
            msgBox = QMessageBox()
            msgBox.setText("This email is already in the database. Please enter another email.")
            msgBox.setWindowTitle("Notification")
            msgBox.exec_()
        else:
            print('email is valid')
            self.emailWidget.addItem(email)
            self.emailEdit.clear()

    #Removes the selected email from the list
    def removeSel(self):
        listItems = self.emailWidget.selectedItems()
        if not listItems: return
        for item in listItems:
            self.emailWidget.takeItem(self.emailWidget.row(item))

    #registers the user into the database
    def addUser(self):
        fname = self.fnameEdit.text()
        lname = self.lnameEdit.text()
        username = self.userEdit.text()
        password = self.passEdit.text()
        confirmPass = self.confEdit.text()
        phone = self.phoneEdit.text()
        address = self.addressEdit.text()
        city = self.cityEdit.text()
        state = self.stateDrop.currentText()
        zipcode = self.zipEdit.text()
        emptype = self.userDrop.currentText()
        emailList = [str(self.emailWidget.item(i).text()) for i in range(self.emailWidget.count())]
        if PyMySQLQs.registeremployeecheck(fname, lname, username, emptype, password, confirmPass, phone, address, city, state, zipcode, emailList):
            msgBox = QMessageBox()
            msgBox.setText("{}".format(PyMySQLQs.registeremployeecheck(fname, lname, username, emptype, password, confirmPass, phone, address, city, state, zipcode, emailList)))
            msgBox.setWindowTitle("Notification")
            msgBox.exec_()

        else:
            PyMySQLQs.registeremployeevisitor(fname, lname, username, emptype, password, confirmPass, phone, address, city, state, zipcode, emailList)
            msgBox = QMessageBox()
            msgBox.setText("Registration Successful!")
            msgBox.setWindowTitle("Notification")
            msgBox.exec_()
###########################################################
#                                                         #
#                                                         #
#                  End of Registration Side               #
#                                                         #
#                                                         #
###########################################################

#####################################################
#PLACEHOLDER SCREEN TO EASILY VIEW ALL LOGIN SCREENS#
#####################################################
#--- placeholder ---#
class Placeholder(QDialog):
    def __init__(self, email, usertype, username):
        self.email = email
        self.usertype = usertype
        self.username = username
        super(Placeholder, self).__init__()
        self.setModal(True)
        self.setWindowTitle("Atlanta Beltline Database")
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.icon = "buzz.png"
        self.setWindowIcon(QIcon(self.icon))
        self.GUI()
        self.connections()

    def GUI(self):
        self.vbox = QVBoxLayout()
        self.grid = QGridLayout()
        self.title = QLabel("Placeholder Screen")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font: bold 20pt;")
        self.uButton = QPushButton("User Only")
        self.uButton.setStyleSheet(bColor)
        self.aButton = QPushButton("Administrator Only")
        self.aButton.setStyleSheet(bColor)
        self.avButton = QPushButton("Admin-Visitor")
        self.avButton.setStyleSheet(bColor)
        self.mButton = QPushButton("Manager Only")
        self.mButton.setStyleSheet(bColor)
        self.mvButton = QPushButton("Manager-Visitor")
        self.mvButton.setStyleSheet(bColor)
        self.sButton = QPushButton("Staff Only")
        self.sButton.setStyleSheet(bColor)
        self.svButton = QPushButton("Staff-Visitor")
        self.svButton.setStyleSheet(bColor)
        self.vButton = QPushButton("Visitor Only")
        self.vButton.setStyleSheet(bColor)
        self.backButton = QPushButton("Back")
        self.backButton.setStyleSheet(bColor)
        self.hbox = QHBoxLayout()
        self.hbox2 = QHBoxLayout()
        self.hbox.addWidget(self.title)
        self.grid.addWidget(self.uButton, 0, 1)
        self.grid.addWidget(self.vButton, 0, 2)
        self.grid.addWidget(self.aButton, 1, 1)
        self.grid.addWidget(self.avButton, 1, 2)
        self.grid.addWidget(self.mButton, 2, 1)
        self.grid.addWidget(self.mvButton, 2, 2)
        self.grid.addWidget(self.sButton, 3, 1)
        self.grid.addWidget(self.svButton, 3, 2)
        self.hbox2.addWidget(self.backButton)
        self.vbox.addLayout(self.hbox)
        self.vbox.addLayout(self.grid)
        self.vbox.addLayout(self.hbox2)
        self.setLayout(self.vbox)

    def connections(self):
        self.backButton.clicked.connect(self.backtoLogin)
        self.uButton.clicked.connect(self.ShowUserFunctionality)
        self.aButton.clicked.connect(self.ShowAdminFunctionality)
        self.avButton.clicked.connect(self.ShowAdminVisFunctionality)
        self.mButton.clicked.connect(self.ShowManagerFunctionality)
        self.mvButton.clicked.connect(self.ShowManagerVisFunctionality)
        self.sButton.clicked.connect(self.ShowStaffFunctionality)
        self.svButton.clicked.connect(self.ShowStaffVisFunctionality)
        self.vButton.clicked.connect(self.ShowVisitorFunctionality)

    def backtoLogin(self):
        self.close()

    def ShowUserFunctionality(self):
        self.a = UserFunctionality(self.email, self.usertype, self.username)
        self.a.show()
        self.close()

    def ShowAdminFunctionality(self):
        self.a = AdminFunctionality(self.email, self.usertype, self.username)
        self.a.show()
        self.close()

    def ShowAdminVisFunctionality(self):
        self.a = AdminVisFunctionality(self.email, self.usertype, self.username)
        self.a.show()
        self.close()

    def ShowManagerFunctionality(self):
        self.a = ManagerFunctionality(self.email, self.usertype, self.username)
        self.a.show()
        self.close()

    def ShowManagerVisFunctionality(self):
        self.a = ManagerVisFunctionality(self.email, self.usertype, self.username)
        self.a.show()
        self.close()

    def ShowStaffFunctionality(self):
        self.a = StaffFunctionality(self.email, self.usertype, self.username)
        self.a.show()
        self.close()

    def ShowStaffVisFunctionality(self):
        self.a = StaffVisFunctionality(self.email, self.usertype, self.username)
        self.a.show()
        self.close()

    def ShowVisitorFunctionality(self):
        self.a = VisitorFunctionality(self.email, self.usertype, self.username)
        self.a.show()
        self.close()

#############################################################
#                                                           #
#                                                           #
#                                                           #
#                        Functionalities                    #
#                                                           #
#                                                           #
#                                                           #
#############################################################
#--- 7 ---#
class UserFunctionality(QDialog):
    def __init__(self, email, usertype, username):
        super(UserFunctionality, self).__init__()
        self.email = email
        self.usertype = usertype
        self.username = username
        self.setModal(True)
        self.setWindowTitle("Atlanta Beltline Database")
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.icon = "buzz.png"
        self.setWindowIcon(QIcon(self.icon))
        self.GUI()
        self.connections()

    def GUI(self):
        self.vbox = QVBoxLayout()
        self.title = QLabel("User Functionality")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font: bold 20pt;")
        self.takeTransitButton = QPushButton("Take Transit")
        self.takeTransitButton.setStyleSheet(bColor)
        self.viewTransitHistoryButton = QPushButton("View Transit History")
        self.viewTransitHistoryButton.setStyleSheet(bColor)
        self.backButton = QPushButton("Log Out")
        self.backButton.setStyleSheet(bColor)
        self.vbox.addWidget(self.title)
        self.vbox.addWidget(self.takeTransitButton)
        self.vbox.addWidget(self.viewTransitHistoryButton)
        self.vbox.addWidget(self.backButton)
        self.setLayout(self.vbox)

    def connections(self):
        self.backButton.clicked.connect(self.backtoLogin)
        self.takeTransitButton.clicked.connect(self.ShowTakeTransit)
        self.viewTransitHistoryButton.clicked.connect(self.ShowTransitHistory)

    def backtoLogin(self):
        self.close()

    def ShowTakeTransit(self):
        self.a = TakeTransit(self.email, self.usertype, self.username)
        self.a.show()
        self.close()

    def ShowTransitHistory(self):
        self.a = ShowTransitHistory(self.email, self.usertype, self.username)
        self.a.show()
        self.close()

#--- 8 ---#
class AdminFunctionality(QDialog):
    def __init__(self, email, usertype, username):
        self.email = email
        self.usertype = usertype
        self.username = username
        super(AdminFunctionality, self).__init__()
        self.setModal(True)
        self.setWindowTitle("Atlanta Beltline Database")
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.icon = "buzz.png"
        self.setWindowIcon(QIcon(self.icon))
        self.GUI()
        self.connections()

    def GUI(self):
        self.vbox = QVBoxLayout()
        self.grid = QGridLayout()
        self.title = QLabel("Administrator Functionality")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font: bold 20pt;")
        self.takeTransitButton = QPushButton("Take Transit")
        self.takeTransitButton.setStyleSheet(bColor)
        self.viewTransitHistoryButton = QPushButton("View Transit History")
        self.viewTransitHistoryButton.setStyleSheet(bColor)
        self.backButton = QPushButton("Log Out")
        self.backButton.setStyleSheet(bColor)
        self.manageProfile = QPushButton("Manage Profile")
        self.manageProfile.setStyleSheet(bColor)
        self.manageUser = QPushButton("Manage User")
        self.manageUser.setStyleSheet(bColor)
        self.manageTransit = QPushButton("Manage Transit")
        self.manageTransit.setStyleSheet(bColor)
        self.manageSite = QPushButton("Manage Site")
        self.manageSite.setStyleSheet(bColor)
        self.vbox.addWidget(self.title)
        self.grid.addWidget(self.takeTransitButton,0,2)
        self.grid.addWidget(self.viewTransitHistoryButton,1,2)
        self.grid.addWidget(self.backButton,2,2)
        self.grid.addWidget(self.manageProfile,0,1)
        self.grid.addWidget(self.manageUser,1,1)
        self.grid.addWidget(self.manageTransit,2,1)
        self.grid.addWidget(self.manageSite,3,1)
        self.vbox.addLayout(self.grid)
        self.setLayout(self.vbox)

    def connections(self):
        self.backButton.clicked.connect(self.backtoLogin)
        self.takeTransitButton.clicked.connect(self.ShowTakeTransit)
        self.viewTransitHistoryButton.clicked.connect(self.ShowViewTransitHistory)
        self.manageProfile.clicked.connect(self.ShowManageProfile)
        self.manageUser.clicked.connect(self.ShowManageUser)
        self.manageTransit.clicked.connect(self.ShowManageTransit)
        self.manageSite.clicked.connect(self.ShowManageSite)

    def backtoLogin(self):
        self.close()

    def ShowTakeTransit(self):
        self.a = TakeTransit(self.email, self.usertype, self.username)
        self.a.show()
        self.close()

    def ShowViewTransitHistory(self):
        self.a = ShowTransitHistory(self.email, self.usertype, self.username)
        self.a.show()
        self.close()

    def ShowManageTransit(self):
        self.a = ManageTransit(self.email, self.usertype, self.username)
        self.a.show()
        self.close()

    def ShowManageProfile(self):
        self.a = ManageProfile(self.email, self.usertype, self.username)
        self.a.show()
        self.close()

    def ShowManageUser(self):
        self.a = ManageUser(self.email, self.usertype, self.username)
        self.a.show()
        self.close()

    def ShowManageSite(self):
        self.a = ManageSite(self.email, self.usertype, self.username)
        self.a.show()
        self.close()


#--- 9 ---#
class AdminVisFunctionality(QDialog):
    def __init__(self, email, usertype, username):
        self.email = email
        self.usertype = usertype
        self.username = username
        super(AdminVisFunctionality, self).__init__()
        self.setModal(True)
        self.setWindowTitle("Atlanta Beltline Database")
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.icon = "buzz.png"
        self.setWindowIcon(QIcon(self.icon))
        self.GUI()
        self.connections()

    def GUI(self):
        self.vbox = QVBoxLayout()
        self.grid = QGridLayout()
        self.title = QLabel("Administrator Functionality")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font: bold 20pt;")
        self.takeTransitButton = QPushButton("Take Transit")
        self.takeTransitButton.setStyleSheet(bColor)
        self.exploreSiteButton = QPushButton("Explore Site")
        self.exploreSiteButton.setStyleSheet(bColor)
        self.exploreEventButton = QPushButton("Explore Event")
        self.exploreEventButton.setStyleSheet(bColor)
        self.viewVisitHistoryButton = QPushButton("View Visit History")
        self.viewVisitHistoryButton.setStyleSheet(bColor)
        self.viewTransitHistoryButton = QPushButton("View Transit History")
        self.viewTransitHistoryButton.setStyleSheet(bColor)
        self.backButton = QPushButton("Log Out")
        self.backButton.setStyleSheet(bColor)
        self.manageProfile = QPushButton("Manage Profile")
        self.manageProfile.setStyleSheet(bColor)
        self.manageUser = QPushButton("Manage User")
        self.manageUser.setStyleSheet(bColor)
        self.manageTransit = QPushButton("Manage Transit")
        self.manageTransit.setStyleSheet(bColor)
        self.manageSite = QPushButton("Manage Site")
        self.manageSite.setStyleSheet(bColor)
        self.vbox.addWidget(self.title)
        self.grid.addWidget(self.manageProfile,0,1)
        self.grid.addWidget(self.manageUser,0,2)
        self.grid.addWidget(self.manageTransit,1,1)
        self.grid.addWidget(self.takeTransitButton,1,2)
        self.grid.addWidget(self.manageSite,2,1)
        self.grid.addWidget(self.exploreSiteButton,2,2)
        self.grid.addWidget(self.exploreEventButton,3,1)
        self.grid.addWidget(self.viewVisitHistoryButton,3,2)
        self.grid.addWidget(self.viewTransitHistoryButton,4,1)
        self.grid.addWidget(self.backButton,4,2)
        self.vbox.addLayout(self.grid)
        self.setLayout(self.vbox)

    def connections(self):
        self.backButton.clicked.connect(self.backtoLogin)
        self.takeTransitButton.clicked.connect(self.ShowTakeTransit)
        self.viewTransitHistoryButton.clicked.connect(self.ShowViewTransitHistory)
        self.manageProfile.clicked.connect(self.ShowManageProfile)
        self.manageUser.clicked.connect(self.ShowManageUser)
        self.manageTransit.clicked.connect(self.ShowManageTransit)
        self.manageSite.clicked.connect(self.ShowManageSite)
        self.viewVisitHistoryButton.clicked.connect(self.ShowVisitHistory)
        self.exploreEventButton.clicked.connect(self.ShowExploreEvent)
        self.exploreSiteButton.clicked.connect(self.ShowExploreSite)

    def backtoLogin(self):
        self.close()

    def ShowTakeTransit(self):
        self.a = TakeTransit(self.email, self.usertype, self.username)
        self.a.show()
        self.close()

    def ShowViewTransitHistory(self):
        self.a = ShowTransitHistory(self.email, self.usertype, self.username)
        self.a.show()
        self.close()

    def ShowManageTransit(self):
        self.a = ManageTransit(self.email, self.usertype, self.username)
        self.a.show()
        self.close()

    def ShowManageProfile(self):
        self.a = ManageProfile(self.email, self.usertype, self.username)
        self.a.show()
        self.close()

    def ShowManageUser(self):
        self.a = ManageUser(self.email, self.usertype, self.username)
        self.a.show()
        self.close()

    def ShowManageSite(self):
        self.a = ManageSite(self.email, self.usertype, self.username)
        self.a.show()
        self.close()

    def ShowVisitHistory(self):
        self.a = VisitHistory(self.email, self.usertype, self.username)
        self.a.show()
        self.close()

    def ShowExploreEvent(self):
        self.a = ExploreEvent(self.email, self.usertype, self.username)
        self.a.show()
        self.close()

    def ShowExploreSite(self):
        self.a = ExploreSite(self.email, self.usertype, self.username)
        self.a.show()
        self.close()

#--- 10 ---#
class ManagerFunctionality(QDialog):
    def __init__(self, email, usertype, username):
        self.email = email
        self.usertype = usertype
        self.username = username
        super(ManagerFunctionality, self).__init__()
        self.setModal(True)
        self.setWindowTitle("Atlanta Beltline Database")
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.icon = "buzz.png"
        self.setWindowIcon(QIcon(self.icon))
        self.GUI()
        self.connections()

    def GUI(self):
        self.vbox = QVBoxLayout()
        self.grid = QGridLayout()
        self.title = QLabel("Manager Functionality")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font: bold 20pt;")
        self.takeTransitButton = QPushButton("Take Transit")
        self.takeTransitButton.setStyleSheet(bColor)
        self.viewSiteReportButton = QPushButton("View Site Report")
        self.viewSiteReportButton.setStyleSheet(bColor)
        self.viewTransitHistoryButton = QPushButton("View Transit History")
        self.viewTransitHistoryButton.setStyleSheet(bColor)
        self.backButton = QPushButton("Log Out")
        self.backButton.setStyleSheet(bColor)
        self.manageProfile = QPushButton("Manage Profile")
        self.manageProfile.setStyleSheet(bColor)
        self.manageEvent = QPushButton("Manage Event")
        self.manageEvent.setStyleSheet(bColor)
        self.viewStaff = QPushButton("View Staff")
        self.viewStaff.setStyleSheet(bColor)
        self.vbox.addWidget(self.title)
        self.grid.addWidget(self.manageProfile,0,1)
        self.grid.addWidget(self.viewSiteReportButton,0,2)
        self.grid.addWidget(self.manageEvent,1,1)
        self.grid.addWidget(self.takeTransitButton,1,2)
        self.grid.addWidget(self.viewStaff,2,1)
        self.grid.addWidget(self.viewTransitHistoryButton,2,2)
        self.vbox.addLayout(self.grid)
        self.vbox.addWidget(self.backButton)
        self.setLayout(self.vbox)

    def connections(self):
        self.backButton.clicked.connect(self.backtoLogin)
        self.takeTransitButton.clicked.connect(self.ShowTakeTransit)
        self.manageProfile.clicked.connect(self.ShowManageProfile)
        self.manageEvent.clicked.connect(self.ShowManageEvent)
        self.viewStaff.clicked.connect(self.ShowViewStaff)
        self.viewSiteReportButton.clicked.connect(self.ShowViewSiteReport)
        self.viewTransitHistoryButton.clicked.connect(self.ShowViewTransitHistory)

    def backtoLogin(self):
        self.close()

    def ShowTakeTransit(self):
        self.a = TakeTransit(self.email, self.usertype, self.username)
        self.a.show()
        self.close()

    def ShowManageProfile(self):
        self.a = ManageProfile(self.email, self.usertype, self.username)
        self.a.show()
        self.close()

    def ShowManageEvent(self):
        self.a = ManageEvent(self.email, self.usertype, self.username)
        self.a.show()
        self.close()

    def ShowViewStaff(self):
        self.a = ViewStaff(self.email,self.usertype, self.username)
        self.a.show()
        self.close()

    def ShowViewSiteReport(self):
        self.a = ViewSiteReport(self.email,self.usertype, self.username)
        self.a.show()
        self.close()

    def ShowViewTransitHistory(self):
        self.a = ShowTransitHistory(self.email,self.usertype, self.username)
        self.a.show()
        self.close()


#--- 11 ---#
class ManagerVisFunctionality(QDialog):
    def __init__(self, email, usertype, username):
        self.email = email
        self.usertype = usertype
        self.username = username
        super(ManagerVisFunctionality, self).__init__()
        self.setModal(True)
        self.setWindowTitle("Atlanta Beltline Database")
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.icon = "buzz.png"
        self.setWindowIcon(QIcon(self.icon))
        self.GUI()
        self.connections()

    def GUI(self):
        self.vbox = QVBoxLayout()
        self.grid = QGridLayout()
        self.title = QLabel("Manager Functionality")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font: bold 20pt;")
        self.takeTransitButton = QPushButton("Take Transit")
        self.takeTransitButton.setStyleSheet(bColor)
        self.exploreSiteButton = QPushButton("Explore Site")
        self.exploreSiteButton.setStyleSheet(bColor)
        self.exploreEventButton = QPushButton("Explore Event")
        self.exploreEventButton.setStyleSheet(bColor)
        self.viewVisitHistoryButton = QPushButton("View Visit History")
        self.viewVisitHistoryButton.setStyleSheet(bColor)
        self.viewTransitHistoryButton = QPushButton("View Transit History")
        self.viewTransitHistoryButton.setStyleSheet(bColor)
        self.backButton = QPushButton("Log Out")
        self.backButton.setStyleSheet(bColor)
        self.manageProfile = QPushButton("Manage Profile")
        self.manageProfile.setStyleSheet(bColor)
        self.manageEvent = QPushButton("Manage Event")
        self.manageEvent.setStyleSheet(bColor)
        self.viewStaff = QPushButton("View Staff")
        self.viewStaff.setStyleSheet(bColor)
        self.viewSiteReport = QPushButton("View Site Report")
        self.viewSiteReport.setStyleSheet(bColor)
        self.vbox.addWidget(self.title)
        self.grid.addWidget(self.manageProfile,0,1)
        self.grid.addWidget(self.manageEvent,0,2)
        self.grid.addWidget(self.viewStaff,1,1)
        self.grid.addWidget(self.viewSiteReport,1,2)
        self.grid.addWidget(self.exploreSiteButton,2,1)
        self.grid.addWidget(self.exploreEventButton,2,2)
        self.grid.addWidget(self.takeTransitButton,3,1)
        self.grid.addWidget(self.viewTransitHistoryButton,3,2)
        self.grid.addWidget(self.viewVisitHistoryButton,4,1)
        self.grid.addWidget(self.backButton,4,2)
        self.vbox.addLayout(self.grid)
        self.setLayout(self.vbox)

    def connections(self):
        self.backButton.clicked.connect(self.backtoLogin)
        self.takeTransitButton.clicked.connect(self.ShowTakeTransit)
        self.manageProfile.clicked.connect(self.ShowManageProfile)
        self.manageEvent.clicked.connect(self.ShowManageEvent)
        self.viewStaff.clicked.connect(self.ShowViewStaff)
        self.viewSiteReport.clicked.connect(self.ShowViewSiteReport)
        self.viewTransitHistoryButton.clicked.connect(self.ShowViewTransitHistory)
        self.viewVisitHistoryButton.clicked.connect(self.ShowVisitHistory)
        self.exploreEventButton.clicked.connect(self.ShowExploreEvent)
        self.exploreSiteButton.clicked.connect(self.ShowExploreSite)

    def backtoLogin(self):
        self.close()

    def ShowTakeTransit(self):
        self.a = TakeTransit(self.email, self.usertype, self.username)
        self.a.show()
        self.close()

    def ShowManageProfile(self):
        self.a = ManageProfile(self.email, self.usertype, self.username)
        self.a.show()
        self.close()

    def ShowManageEvent(self):
        self.a = ManageEvent(self.email, self.usertype, self.username)
        self.a.show()
        self.close()

    def ShowViewStaff(self):
        self.a = ViewStaff(self.email,self.usertype, self.username)
        self.a.show()
        self.close()

    def ShowViewSiteReport(self):
        self.a = ViewSiteReport(self.email,self.usertype, self.username)
        self.a.show()
        self.close()

    def ShowViewTransitHistory(self):
        self.a = ShowTransitHistory(self.email,self.usertype, self.username)
        self.a.show()
        self.close()

    def ShowVisitHistory(self):
        self.a = VisitHistory(self.email, self.usertype, self.username)
        self.a.show()
        self.close()

    def ShowExploreEvent(self):
        self.a = ExploreEvent(self.email, self.usertype, self.username)
        self.a.show()
        self.close()

    def ShowExploreSite(self):
        self.a = ExploreSite(self.email, self.usertype, self.username)
        self.a.show()
        self.close()

#--- 12 ---#
class StaffFunctionality(QDialog):
    def __init__(self, email, usertype, username):
        super(StaffFunctionality, self).__init__()
        self.email = email
        self.usertype = usertype
        self.username = username
        self.setModal(True)
        self.setWindowTitle("Atlanta Beltline Database")
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.icon = "buzz.png"
        self.setWindowIcon(QIcon(self.icon))
        self.GUI()
        self.connections()

    def GUI(self):
        self.vbox = QVBoxLayout()
        self.title = QLabel("Staff Functionality")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font: bold 20pt;")
        self.manageProfile = QPushButton("Manage Profile")
        self.manageProfile.setStyleSheet(bColor)
        self.viewSchedule = QPushButton("View Schedule")
        self.viewSchedule.setStyleSheet(bColor)
        self.takeTransitButton = QPushButton("Take Transit")
        self.takeTransitButton.setStyleSheet(bColor)
        self.viewTransitHistoryButton = QPushButton("View Transit History")
        self.viewTransitHistoryButton.setStyleSheet(bColor)
        self.backButton = QPushButton("Log Out")
        self.backButton.setStyleSheet(bColor)
        self.vbox.addWidget(self.title)
        self.vbox.addWidget(self.manageProfile)
        self.vbox.addWidget(self.viewSchedule)
        self.vbox.addWidget(self.takeTransitButton)
        self.vbox.addWidget(self.viewTransitHistoryButton)
        self.vbox.addWidget(self.backButton)
        self.setLayout(self.vbox)

    def connections(self):
        self.backButton.clicked.connect(self.backtoLogin)
        self.takeTransitButton.clicked.connect(self.ShowTakeTransit)
        self.manageProfile.clicked.connect(self.ShowManageProfile)
        self.viewTransitHistoryButton.clicked.connect(self.ShowViewTransitHistory)
        self.viewSchedule.clicked.connect(self.ShowViewSchedule)

    def backtoLogin(self):
        self.close()

    def ShowTakeTransit(self):
        self.a = TakeTransit(self.email, self.usertype, self.username)
        self.a.show()
        self.close()

    def ShowManageProfile(self):
        self.a = ManageProfile(self.email, self.usertype, self.username)
        self.a.show()
        self.close()

    def ShowViewTransitHistory(self):
        self.a = ShowTransitHistory(self.email,self.usertype, self.username)
        self.a.show()
        self.close()

    def ShowViewSchedule(self):
        self.a = ViewSchedule(self.email,self.usertype, self.username)
        self.a.show()
        self.close()

#--- 13 ---#
class StaffVisFunctionality(QDialog):
    def __init__(self, email, usertype, username):
        self.email = email
        self.usertype = usertype
        self.username = username
        super(StaffVisFunctionality, self).__init__()
        self.setModal(True)
        self.setWindowTitle("Atlanta Beltline Database")
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.icon = "buzz.png"
        self.setWindowIcon(QIcon(self.icon))
        self.GUI()
        self.connections()

    def GUI(self):
        self.vbox = QVBoxLayout()
        self.grid = QGridLayout()
        self.title = QLabel("Staff Functionality")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font: bold 20pt;")
        self.takeTransitButton = QPushButton("Take Transit")
        self.takeTransitButton.setStyleSheet(bColor)
        self.exploreSiteButton = QPushButton("Explore Site")
        self.exploreSiteButton.setStyleSheet(bColor)
        self.exploreEventButton = QPushButton("Explore Event")
        self.exploreEventButton.setStyleSheet(bColor)
        self.viewVisitHistoryButton = QPushButton("View Visit History")
        self.viewVisitHistoryButton.setStyleSheet(bColor)
        self.viewTransitHistoryButton = QPushButton("View Transit History")
        self.viewTransitHistoryButton.setStyleSheet(bColor)
        self.backButton = QPushButton("Log Out")
        self.backButton.setStyleSheet(bColor)
        self.manageProfile = QPushButton("Manage Profile")
        self.manageProfile.setStyleSheet(bColor)
        self.viewSchedule = QPushButton("View Schedule")
        self.viewSchedule.setStyleSheet(bColor)
        self.vbox.addWidget(self.title)
        self.grid.addWidget(self.manageProfile,0,1)
        self.grid.addWidget(self.exploreEventButton,0,2)
        self.grid.addWidget(self.viewSchedule,1,1)
        self.grid.addWidget(self.exploreSiteButton,1,2)
        self.grid.addWidget(self.takeTransitButton,2,1)
        self.grid.addWidget(self.viewVisitHistoryButton,2,2)
        self.grid.addWidget(self.viewTransitHistoryButton,3,1)
        self.grid.addWidget(self.backButton,3,2)
        self.vbox.addLayout(self.grid)
        self.setLayout(self.vbox)

    def connections(self):
        self.backButton.clicked.connect(self.backtoLogin)
        self.takeTransitButton.clicked.connect(self.ShowTakeTransit)
        self.manageProfile.clicked.connect(self.ShowManageProfile)
        self.viewTransitHistoryButton.clicked.connect(self.ShowViewTransitHistory)
        self.viewSchedule.clicked.connect(self.ShowViewSchedule)
        self.viewVisitHistoryButton.clicked.connect(self.ShowVisitHistory)
        self.exploreEventButton.clicked.connect(self.ShowExploreEvent)
        self.exploreSiteButton.clicked.connect(self.ShowExploreSite)

    def backtoLogin(self):
        self.close()

    def ShowTakeTransit(self):
        self.a = TakeTransit(self.email, self.usertype, self.username)
        self.a.show()
        self.close()

    def ShowManageProfile(self):
        self.a = ManageProfile(self.email, self.usertype, self.username)
        self.a.show()
        self.close()

    def ShowViewTransitHistory(self):
        self.a = ShowTransitHistory(self.email,self.usertype, self.username)
        self.a.show()
        self.close()

    def ShowViewSchedule(self):
        self.a = ViewSchedule(self.email,self.usertype, self.username)
        self.a.show()
        self.close()

    def ShowVisitHistory(self):
        self.a = ViewVisitHistory(self.email, self.usertype, self.username)
        self.a.show()
        self.close()

    def ShowExploreEvent(self):
        self.a = ExploreEvent(self.email, self.usertype, self.username)
        self.a.show()
        self.close()

    def ShowExploreSite(self):
        self.a = Site(self.email, self.usertype, self.username)
        self.a.show()
        self.close()

#--- 14 ---#
class VisitorFunctionality(QDialog):
    def __init__(self, email, usertype, username):
        self.usertype = usertype
        self.username = username
        super(VisitorFunctionality, self).__init__()
        self.email = email
        self.setModal(True)
        self.setWindowTitle("Atlanta Beltline Database")
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.icon = "buzz.png"
        self.setWindowIcon(QIcon(self.icon))
        self.GUI()
        self.connections()

    def GUI(self):
        self.vbox = QVBoxLayout()
        self.title = QLabel("Visitor Functionality")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font: bold 20pt;")
        self.exploreSiteButton = QPushButton("Explore Site")
        self.exploreSiteButton.setStyleSheet(bColor)
        self.exploreEventButton = QPushButton("Explore Event")
        self.exploreEventButton.setStyleSheet(bColor)
        self.viewVisitHistoryButton = QPushButton("View Visit History")
        self.viewVisitHistoryButton.setStyleSheet(bColor)
        self.takeTransitButton = QPushButton("Take Transit")
        self.takeTransitButton.setStyleSheet(bColor)
        self.viewTransitHistoryButton = QPushButton("View Transit History")
        self.viewTransitHistoryButton.setStyleSheet(bColor)
        self.backButton = QPushButton("Log Out")
        self.backButton.setStyleSheet(bColor)
        self.vbox.addWidget(self.title)
        self.vbox.addWidget(self.exploreEventButton)
        self.vbox.addWidget(self.exploreSiteButton)
        self.vbox.addWidget(self.viewVisitHistoryButton)
        self.vbox.addWidget(self.takeTransitButton)
        self.vbox.addWidget(self.viewTransitHistoryButton)
        self.vbox.addWidget(self.backButton)
        self.setLayout(self.vbox)

    def connections(self):
        self.backButton.clicked.connect(self.backtoLogin)
        self.takeTransitButton.clicked.connect(self.ShowTakeTransit)
        self.viewVisitHistoryButton.clicked.connect(self.ShowVisitHistory)
        self.exploreEventButton.clicked.connect(self.ShowExploreEvent)
        self.exploreSiteButton.clicked.connect(self.ShowExploreSite)
        self.viewTransitHistoryButton.clicked.connect(self.ShowViewTransitHistory)

    def backtoLogin(self):
        self.close()

    def ShowTakeTransit(self):
        self.a = TakeTransit(self.email, self.usertype, self.username)
        self.a.show()
        self.close()

    def ShowVisitHistory(self):
        self.a = ViewVisitHistory(self.email, self.usertype, self.username)
        self.a.show()
        self.close()

    def ShowExploreEvent(self):
        self.a = ExploreEvent(self.email, self.usertype, self.username)
        self.a.show()
        self.close()

    def ShowExploreSite(self):
        self.a = ExploreSite(self.email, self.usertype, self.username)
        self.a.show()
        self.close()

    def ShowViewTransitHistory(self):
        self.a = ShowTransitHistory(self.email,self.usertype, self.username)
        self.a.show()
        self.close()

###########################################################
#                                                         #
#                                                         #
#                  End of Functionalities                 #
#                                                         #
#                                                         #
###########################################################

#--- 15 ---#
class TakeTransit(QDialog):
    def __init__(self, email, usertype, username):
        super(TakeTransit, self).__init__()
        self.email = email
        self.usertype = usertype
        self.username = username
        self.setModal(True)
        self.setWindowTitle("Atlanta Beltline Database")
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.icon = "buzz.png"
        self.setWindowIcon(QIcon(self.icon))
        self.GUI()
        self.connections()

    def GUI(self):
        self.vbox = QVBoxLayout()
        self.title = QLabel("Take Transit")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font: bold 20pt;")
        self.grid1 = QGridLayout()
        self.containLabel = QLabel("Contain Site")
        self.siteDrop = QComboBox()
        self.siteDrop.addItem('-ALL-')
        self.transportLabel = QLabel("Transport Type")
        self.transportTypeDrop = QComboBox()
        self.transportTypeDrop.addItem('-ALL-')
        self.grid1.addWidget(self.containLabel,0,1)
        self.grid1.addWidget(self.siteDrop,0,2)
        self.grid1.addWidget(self.transportLabel,0,3)
        self.grid1.addWidget(self.transportTypeDrop,0,4)
        self.hbox2 = QHBoxLayout()
        self.priceLabel = QLabel("Price Range")
        self.lowRangeText = QLineEdit("")
        self.dashLabel = QLabel("--")
        self.highRangeText = QLineEdit("")
        self.filterButton = QPushButton("Filter")
        self.filterButton.setStyleSheet(bColor)
        self.hbox2.addWidget(self.priceLabel)
        self.hbox2.addWidget(self.lowRangeText)
        self.hbox2.addWidget(self.dashLabel)
        self.hbox2.addWidget(self.highRangeText)
        self.hbox2.addWidget(self.filterButton)
        self.initTable()
        self.hbox3 = QHBoxLayout()
        self.transitDateLabel = QLabel("Transit Date")
        self.transiteDateEdit = QLineEdit("")
        self.logTransit = QPushButton("Log Transit")
        self.logTransit.setStyleSheet(bColor)
        self.backButton = QPushButton("Back")
        self.backButton.setStyleSheet(bColor)
        self.hbox3.addWidget(self.backButton)
        self.hbox3.addWidget(self.transitDateLabel)
        self.hbox3.addWidget(self.transiteDateEdit)
        self.hbox3.addWidget(self.logTransit)
        self.vbox.addWidget(self.title)
        self.vbox.addLayout(self.grid1)
        self.vbox.addLayout(self.hbox2)
        self.info = QLabel("Click a column header to order ascending/descending by that column")
        self.info.setAlignment(Qt.AlignCenter)
        self.vbox.addWidget(self.info)
        self.vbox.addWidget(self.SQLtable)
        self.vbox.addLayout(self.hbox3)
        self.comboItems()
        self.setLayout(self.vbox)
        self.resize(700,440)

    def connections(self):
        self.backButton.clicked.connect(self.Back)
        self.logTransit.clicked.connect(self.LogATransit)
        self.SQLtable.horizontalHeader().sectionClicked.connect(self.headerClicked)
        self.filterButton.clicked.connect(self.resetOrder)

    def comboItems(self):
        self.siteList = PyMySQLQs.SiteComboBox()
        for aDict in self.siteList:
            for key in aDict:
                self.siteDrop.addItem(aDict[key])
        self.transportTypeDrop.addItems(['Bus', 'MARTA', 'Bike'])

    def Back(self):
        if self.usertype == 'Visitor':
            self.a = VisitorFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'User':
            self.a = UserFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Admin-Only':
            self.a = AdminFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Admin-Visitor':
            self.a = AdminVisFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Staff-Only':
            self.a = StaffFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Staff-Visitor':
            self.a = StaffVisFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Manager-Only':
            self.a = ManagerFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Manager-Visitor':
            self.a = ManagerVisFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Master':
            self.a = Placeholder(self.email, self.usertype, self.username)
        self.a.show()
        self.close()

    def initTable(self):
        self.sqlHeaderList = ['Select','Route','Transport Type','Price','# Connected Sites']
        self.orderdict = ['a',"asc","asc","asc","asc"]
        self.SQLtable = QtWidgets.QTableWidget()
        self.SQLtable.count = 0
        #initializing the view
        self.checkBoxes = loadTable(self.SQLtable, 'placeholder data', self.sqlHeaderList, 4)
        self.orderTuple = 'no order'

    def resetOrder(self):
        self.orderTuple = 'no order'
        self.populateTable()

    def populateTable(self):
        site = self.siteDrop.currentText()
        transType = self.transportTypeDrop.currentText()
        lowRange = self.lowRangeText.text()
        highRange = self.highRangeText.text()
        self.result = PyMySQLQs.TakeTransitTable(self.SQLtable, site, transType, lowRange, highRange, self.orderTuple)
        if type(self.result) == str:
            msgBox = QMessageBox()
            msgBox.setText("{}".format(self.result))
            msgBox.setWindowTitle("Notification")
            msgBox.exec_()
        else:
            self.checkBoxes = loadTable(self.SQLtable, self.result, self.sqlHeaderList, 4)

    def LogATransit(self):
        date = self.transiteDateEdit.text()
        for i in range(self.SQLtable.rowCount()):
            check = self.checkBoxes[i]
            if check.isChecked():
                route = self.SQLtable.item(i,1).text()
                transportType = self.SQLtable.item(i,2).text()
                price = self.SQLtable.item(i,3).text()
                numConnected = self.SQLtable.item(i,4).text()
                self.SQLtable.clearSelection()
                print(self.email, route, transportType, price, numConnected, date)
                self.result = PyMySQLQs.logTransit(self.username, transportType, route, date)
                if type(self.result) == str:
                    msgBox = QMessageBox()
                    msgBox.setText("Log Transit Failed. {}".format(self.result))
                    msgBox.setWindowTitle("Notification")
                    msgBox.exec_()
                else:
                    msgBox = QMessageBox()
                    msgBox.setText("Log Transit Succesful")
                    msgBox.setWindowTitle("Notification")
                    msgBox.exec_()

    def headerClicked(self):
        col = self.SQLtable.currentColumn()
        if col != 2 and col != 3 and col != 4:
            return 'a'
        else:
            if self.orderdict[col] == 'asc':
                self.orderdict[col] = 'desc'
            else:
                self.orderdict[col] = 'asc'
            self.orderTuple = (col, self.orderdict[col])
            self.populateTable()
            self.SQLtable.clearSelection()

#--- 16 ---#
class ShowTransitHistory(QDialog):
    def __init__(self, email, usertype, username):
        super(ShowTransitHistory, self).__init__()
        self.email = email
        self.usertype = usertype
        self.username = username
        self.setModal(True)
        self.setWindowTitle("Atlanta Beltline Database")
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.icon = "buzz.png"
        self.setWindowIcon(QIcon(self.icon))
        self.GUI()
        self.connections()

    def GUI(self):
        self.vbox = QVBoxLayout()
        self.title = QLabel("Transit History")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font: bold 20pt;")
        self.grid1 = QGridLayout()
        self.containLabel = QLabel("Contain Site")
        self.siteDrop = QComboBox()
        self.siteDrop.addItem('-ALL-')
        self.transportLabel = QLabel("Transport Type")
        self.transportTypeDrop = QComboBox()
        self.transportTypeDrop.addItem('-ALL-')
        self.grid1.addWidget(self.containLabel,0,3)
        self.grid1.addWidget(self.siteDrop,0,4)
        self.grid1.addWidget(self.transportLabel,0,1)
        self.grid1.addWidget(self.transportTypeDrop,0,2)
        self.hbox2 = QHBoxLayout()
        self.routeLabel = QLabel("Route")
        self.routeEdit = QLineEdit("")
        self.startDateLabel = QLabel("Start Date")
        self.startDateEdit = QLineEdit("")
        self.endDateLabel = QLabel("End Date")
        self.endDateEdit = QLineEdit("")
        self.hbox2.addWidget(self.routeLabel)
        self.hbox2.addWidget(self.routeEdit)
        self.hbox2.addWidget(self.startDateLabel)
        self.hbox2.addWidget(self.startDateEdit)
        self.hbox2.addWidget(self.endDateLabel)
        self.hbox2.addWidget(self.endDateEdit)
        self.hboxFilter = QHBoxLayout()
        self.filterButton = QPushButton("Filter")
        self.filterButton.setStyleSheet(bColor)
        self.hboxFilter.addItem(QSpacerItem(250,20))
        self.hboxFilter.addWidget(self.filterButton)
        self.hboxFilter.addItem(QSpacerItem(250,20))
        self.initTable()
        self.hbox3 = QHBoxLayout()
        self.backButton = QPushButton("Back")
        self.backButton.setStyleSheet(bColor)
        self.hbox3.addItem(QSpacerItem(250, 20))
        self.hbox3.addWidget(self.backButton)
        self.hbox3.addItem(QSpacerItem(250, 20))
        self.vbox.addWidget(self.title)
        self.vbox.addLayout(self.grid1)
        self.vbox.addLayout(self.hbox2)
        self.vbox.addLayout(self.hboxFilter)
        self.info = QLabel("Click a column header to order ascending/descending by that column")
        self.info.setAlignment(Qt.AlignCenter)
        self.vbox.addWidget(self.info)
        self.vbox.addWidget(self.SQLtable)
        self.vbox.addLayout(self.hbox3)
        self.comboItems()
        self.setLayout(self.vbox)
        self.resize(600,440)

    def connections(self):
        self.backButton.clicked.connect(self.Back)
        self.filterButton.clicked.connect(self.resetOrder)
        self.SQLtable.horizontalHeader().sectionClicked.connect(self.headerClicked)

    def resetOrder(self):
        self.orderTuple = 'no order'
        self.populateTable()

    def comboItems(self):
        self.siteList = PyMySQLQs.SiteComboBox()
        for aDict in self.siteList:
            for key in aDict:
                self.siteDrop.addItem(aDict[key])
        self.transportTypeDrop.addItems(['Bus', 'MARTA', 'Bike'])

    def Back(self):
        print(self.usertype)
        if self.usertype == 'Visitor':
            self.a = VisitorFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'User':
            self.a = UserFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Admin-Only':
            self.a = AdminFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Admin-Visitor':
            self.a = AdminVisFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Staff-Only':
            self.a = StaffFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Staff-Visitor':
            self.a = StaffVisFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Manager-Only':
            self.a = ManagerFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Manager-Visitor':
            self.a = ManagerVisFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Master':
            self.a = Placeholder(self.email, self.usertype, self.username)
        self.a.show()
        self.close()

    def initTable(self):
        self.sqlHeaderList = ['Date','Route','Transport Type','Price']
        self.orderdict = ["asc","asc","asc","asc","asc","asc","asc"]
        self.SQLtable = QtWidgets.QTableWidget()
        self.SQLtable.count = 0
        self.checkBoxes = loadTableNoCheck(self.SQLtable, 'placeholder data', self.sqlHeaderList, 4)
        self.orderTuple = 'no order'

    def populateTable(self):
        site = self.siteDrop.currentText()
        transType = self.transportTypeDrop.currentText()
        route = self.routeEdit.text()
        startDate = self.startDateEdit.text()
        endDate = self.endDateEdit.text()
        self.result = PyMySQLQs.TransitHistoryTable(self.SQLtable, self.username, route, site, transType, startDate, endDate, self.orderTuple)
        if type(self.result) == str:
            msgBox = QMessageBox()
            msgBox.setText("{}".format(self.result))
            msgBox.setWindowTitle("Notification")
            msgBox.exec_()
        else:
            loadTableNoCheck(self.SQLtable, self.result, self.sqlHeaderList, 4)

    def headerClicked(self):
        col = self.SQLtable.currentColumn()
        if col != -1:
            if self.orderdict[col] == 'asc':
                self.orderdict[col] = 'desc'
            else:
                self.orderdict[col] = 'asc'
            self.orderTuple = (col, self.orderdict[col])
            self.populateTable()
            self.SQLtable.clearSelection()


#--- 17 ---#
class ManageProfile(QDialog):
    def __init__(self, email, usertype, username):
        super(ManageProfile, self).__init__()
        self.email = email
        self.usertype = usertype
        self.username = username
        self.setModal(True)
        self.setWindowTitle("Atlanta Beltline Database")
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.icon = "buzz.png"
        self.setWindowIcon(QIcon(self.icon))
        self.GUI()
        self.connections()

    def GUI(self):
        self.vbox = QVBoxLayout()
        self.title = QLabel("Manage Profile")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font: bold 20pt;")
        self.hbox1 = QHBoxLayout()
        self.hbox1.addWidget(QLabel("First Name"))
        self.fname = QLineEdit("")
        self.hbox1.addWidget(self.fname)
        self.hbox1.addWidget(QLabel("Last Name"))
        self.lname = QLineEdit("")
        self.hbox1.addWidget(self.lname)
        self.vbox.addWidget(self.title)
        self.vbox.addLayout(self.hbox1)
        self.hbox2 = QHBoxLayout()
        self.hbox2.addWidget(QLabel("Username"))
        self.initProfile()
        self.hbox2.addWidget(self.usernameLabel)
        self.hbox2.addWidget(QLabel("Site Name"))
        self.hbox2.addWidget(self.sitename)
        self.vbox.addLayout(self.hbox2)
        self.hbox3 = QHBoxLayout()
        self.hbox3.addWidget(QLabel("Employee ID"))
        self.hbox3.addWidget(self.employeeID)
        self.hbox3.addWidget(QLabel("Phone"))
        self.phone = QLineEdit("")
        self.hbox3.addWidget(self.phone)
        self.vbox.addLayout(self.hbox3)
        self.hbox4 = QHBoxLayout()
        self.hbox4.addWidget(QLabel("Address"))
        self.hbox4.addWidget(self.address)
        self.vbox.addLayout(self.hbox4)
        self.hbox5 = QHBoxLayout()
        self.emailEdit = QLineEdit("")
        self.email = QLabel("Email")
        self.emailAdd = QPushButton("Add")
        self.hbox5.addWidget(self.email)
        self.hbox5.addWidget(self.emailEdit)
        self.hbox5.addWidget(self.emailAdd)
        self.vbox.addLayout(self.hbox5)
        self.hboxEmail = QHBoxLayout()
        self.emailWidget = QListWidget()
        for item in PyMySQLQs.getemails(self.username):
            print(item)
            self.emailWidget.addItem(QListWidgetItem(item))
        self.removeButton = QPushButton("Remove Selected Email")
        self.hboxEmail.addWidget(QLabel("Emails"))
        self.hboxEmail.addWidget(self.emailWidget)
        self.hboxEmail.addWidget(self.removeButton)
        self.vbox.addLayout(self.hboxEmail)
        self.hbox6 = QHBoxLayout()
        self.hbox6.addItem(QSpacerItem(250,20))
        self.visitorCheck = QCheckBox()
        self.hbox6.addWidget(self.visitorCheck)
        self.hbox6.addWidget(QLabel("Visitor Account"))
        self.hbox6.addItem(QSpacerItem(250,20))
        self.vbox.addLayout(self.hbox6)
        self.hbox7 = QHBoxLayout()
        self.updateButton = QPushButton("Update")
        self.backButton = QPushButton("Back")
        self.updateButton.setStyleSheet(bColor)
        self.backButton.setStyleSheet(bColor)
        self.hbox7.addItem(QSpacerItem(200,20))
        self.hbox7.addWidget(self.updateButton)
        self.hbox7.addWidget(self.backButton)
        self.hbox7.addItem(QSpacerItem(200,20))
        self.vbox.addLayout(self.hbox7)
        self.setLayout(self.vbox)

    def connections(self):
        self.backButton.clicked.connect(self.Back)
        self.emailAdd.clicked.connect(self.addingEmail)
        self.removeButton.clicked.connect(self.removeSel)
        self.updateButton.clicked.connect(self.Update)

    def initProfile(self):
        #need to call function to get stuff from SQL database
        self.usernameLabel = QLabel(self.username)
        self.usernameLabel.setStyleSheet("font-weight: bold;")
        self.sitename = QLabel(PyMySQLQs.showsite(self.username, self.usertype))
        self.sitename.setStyleSheet("font-weight: bold;")
        self.employeeID = QLabel(PyMySQLQs.showempID(self.username))
        self.employeeID.setStyleSheet("font-weight: bold;")
        self.address = QLabel(PyMySQLQs.showaddress(self.username))
        self.address.setStyleSheet("font-weight: bold;")

    def addingEmail(self):
        email = self.emailEdit.text()
        if not re.match(r"[A-Za-z0-9]*@[A-Za-z0-9]*[.][A-Za-z0-9]*", email):
            print('email is not valid')
            msgBox = QMessageBox()
            msgBox.setText("Please enter an email in the following format: EmailAdress@ServiceProivder.domain")
            msgBox.setWindowTitle("Notification")
            msgBox.exec_()
        elif PyMySQLQs.checkemail(email):
            msgBox = QMessageBox()
            msgBox.setText("This email is already in the database. Please enter another email.")
            msgBox.setWindowTitle("Notification")
            msgBox.exec_()
        else:
            print('email is valid')
            self.emailWidget.addItem(email)
            self.emailEdit.clear()

    def removeSel(self):
        listItems = self.emailWidget.selectedItems()
        if not listItems: return
        for item in listItems:
            self.emailWidget.takeItem(self.emailWidget.row(item))
            PyMySQLQs.removeemail(item)

    def Back(self):
        if self.usertype == 'Visitor':
            self.a = VisitorFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'User':
            self.a = UserFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Admin-Only':
            self.a = AdminFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Admin-Visitor':
            self.a = AdminVisFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Staff-Only':
            self.a = StaffFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Staff-Visitor':
            self.a = StaffVisFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Manager-Only':
            self.a = ManagerFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Manager-Visitor':
            self.a = ManagerVisFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Master':
            self.a = Placeholder(self.email, self.usertype, self.username)
        self.a.show()
        self.close()

    def Update(self):
        emailList = [str(self.emailWidget.item(i).text()) for i in range(self.emailWidget.count())]
        check = self.visitorCheck.isChecked()
        if PyMySQLQs.updatecheck(self.fname.text(), self.lname.text(), self.username, self.phone.text(), check):
            return PyMySQLQs.updatecheck(self.fname.text(), self.lname.text(), self.username, self.phone.text(), check)
        PyMySQLQs.update(firstname, lastname, username, phone, visitoraccount)

#--- 18 ---#
class ManageUser(QDialog):
    def __init__(self, email, usertype, username):
        super(ManageUser, self).__init__()
        self.email = email
        self.usertype = usertype
        self.username = username
        self.setModal(True)
        self.setWindowTitle("Atlanta Beltline Database")
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.icon = "buzz.png"
        self.setWindowIcon(QIcon(self.icon))
        self.GUI()
        self.connections()

    def GUI(self):
        self.vbox = QVBoxLayout()
        self.title = QLabel("Manage User")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font: bold 20pt;")
        self.vbox.addWidget(self.title)
        self.hbox1 = QHBoxLayout()
        self.userTypeLabel = QLabel("Type")
        self.userTypeDrop = QComboBox()
        self.userTypeDrop.addItems(['-ALL-','User','Visitor','Staff','Manager'])
        self.statusLabel = QLabel("Status")
        self.statusDrop = QComboBox()
        self.statusDrop.addItems(['-ALL-','Approved','Pending','Declined'])
        self.hbox1.addWidget(QLabel("Username"))
        self.userEdit = QLineEdit("")
        self.hbox1.addWidget(self.userEdit)
        self.hbox1.addWidget(self.userTypeLabel)
        self.hbox1.addWidget(self.userTypeDrop)
        self.hbox1.addWidget(self.statusLabel)
        self.hbox1.addWidget(self.statusDrop)
        self.vbox.addLayout(self.hbox1)
        self.hbox2 = QHBoxLayout()
        self.filterButton = QPushButton("Filter")
        self.filterButton.setStyleSheet(bColor)
        self.hbox2.addItem(QSpacerItem(150,20))
        self.hbox2.addWidget(self.filterButton)
        self.hbox2.addItem(QSpacerItem(150,20))
        self.approveButton = QPushButton("Approve")
        self.approveButton.setStyleSheet(bColor)
        self.declineButton = QPushButton("Decline")
        self.declineButton.setStyleSheet(bColor)
        self.hbox2.addWidget(self.approveButton)
        self.hbox2.addWidget(self.declineButton)
        self.vbox.addLayout(self.hbox2)
        self.initTable()
        self.hbox3 = QHBoxLayout()
        self.backButton = QPushButton("Back")
        self.backButton.setStyleSheet(bColor)
        self.hbox3.addItem(QSpacerItem(250, 20))
        self.hbox3.addWidget(self.backButton)
        self.hbox3.addItem(QSpacerItem(250, 20))
        self.vbox.addWidget(QLabel("Click a column header to order ascending/descending by that column"))
        self.vbox.addWidget(self.SQLtable)
        self.vbox.addLayout(self.hbox3)
        self.setLayout(self.vbox)
        self.resize(700,440)

    def connections(self):
        self.backButton.clicked.connect(self.Back)
        self.SQLtable.horizontalHeader().sectionClicked.connect(self.headerClicked)
        self.filterButton.clicked.connect(self.resetOrder)
        self.approveButton.clicked.connect(self.approveUser)
        self.declineButton.clicked.connect(self.declineUser)

    def resetOrder(self):
        self.orderTuple = 'no order'
        self.populateTable()

    def approveUser(self):
        for i in range(self.SQLtable.rowCount()):
            check = self.checkBoxes[i]
            if check.isChecked():
                username = self.SQLtable.item(i,1).text()
                PyMySQLQs.approve(username)
                print(username + 'has been approved')
                self.SQLtable.clearSelection()

    def declineUser(self):
        for i in range(self.SQLtable.rowCount()):
            check = self.checkBoxes[i]
            if check.isChecked():
                username = self.SQLtable.item(i,1).text()
                PyMySQLQs.decline(self.username)
                self.SQLtable.clearSelection()

    def Back(self):
        if self.usertype == 'Visitor':
            self.a = VisitorFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'User':
            self.a = UserFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Admin-Only':
            self.a = AdminFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Admin-Visitor':
            self.a = AdminVisFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Staff-Only':
            self.a = StaffFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Staff-Visitor':
            self.a = StaffVisFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Manager-Only':
            self.a = ManagerFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Manager-Visitor':
            self.a = ManagerVisFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Master':
            self.a = Placeholder(self.email, self.usertype, self.username)
        self.a.show()
        self.close()

    def initTable(self):
        self.sqlHeaderList = ['Select','Username','Email Count','User Type','Status']
        self.orderdict = ["asc","asc","asc","asc","asc","asc","asc"]
        self.SQLtable = QtWidgets.QTableWidget()
        self.SQLtable.count = 0
        self.checkBoxes = loadTable(self.SQLtable, 'placeholder data', self.sqlHeaderList, 4)
        self.orderTuple = 'no order'

    def populateTable(self):
        status = self.statusDrop.currentText()
        userType = self.userTypeDrop.currentText()
        username = self.userEdit.text()
        #UPDATE WHEN PYMYSQLQs HAS QUERIES PUT IN
        self.result = PyMySQLQs.ManageUser(self.SQLtable, username, userType, status, self.orderTuple)
        #
        #GRANT MADE AN EDIT HERE 8:26 on 4/19
        #
        if type(self.result) == str:
            msgBox = QMessageBox()
            msgBox.setText("{}".format(PyMySQLQs.registerusercheck(fname, lname, username, password, confirmPass, emaillist)))
            msgBox.setWindowTitle("Notification")
            msgBox.exec_()
        else:
            self.checkBoxes = loadTable(self.SQLtable, self.result, self.sqlHeaderList, 4)

    def headerClicked(self):
        col = self.SQLtable.currentColumn()
        if col != -1:
            if self.orderdict[col] == 'asc':
                self.orderdict[col] = 'desc'
            else:
                self.orderdict[col] = 'asc'
            self.orderTuple = (col, self.orderdict[col])
            self.populateTable()
            self.SQLtable.clearSelection()


#--- 19 ---#
class ManageSite(QDialog):
    def __init__(self, email, usertype, username):
        super(ManageSite, self).__init__()
        self.email = email
        self.usertype = usertype
        self.username = username
        self.setModal(True)
        self.setWindowTitle("Atlanta Beltline Database")
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.icon = "buzz.png"
        self.setWindowIcon(QIcon(self.icon))
        self.GUI()
        self.connections()

    def GUI(self):
        self.vbox = QVBoxLayout()
        self.title = QLabel("Manage Site")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font: bold 20pt;")
        self.vbox.addWidget(self.title)
        self.hbox1 = QHBoxLayout()
        self.SiteLabel = QLabel("Site")
        self.SiteDrop = QComboBox()
        self.SiteDrop.addItem('-ALL-')
        self.managerLabel = QLabel("Manager")
        self.managerDrop = QComboBox()
        self.managerDrop.addItem('-ALL-')
        self.hbox1.addWidget(self.SiteLabel)
        self.hbox1.addWidget(self.SiteDrop)
        self.hbox1.addWidget(self.managerLabel)
        self.hbox1.addWidget(self.managerDrop)
        self.vbox.addLayout(self.hbox1)
        self.hbox2 = QHBoxLayout()
        self.openLabel = QLabel("Open Everyday")
        self.openDrop = QComboBox()
        self.openDrop.addItems(['-ALL-','Yes','No'])
        self.hbox2.addItem(QSpacerItem(150,20))
        self.hbox2.addWidget(self.openLabel)
        self.hbox2.addWidget(self.openDrop)
        self.hbox2.addItem(QSpacerItem(150,20))
        self.vbox.addLayout(self.hbox2)
        self.filterButton = QPushButton("Filter")
        self.filterButton.setStyleSheet(bColor)
        self.hboxButtons = QHBoxLayout()
        self.createButton = QPushButton("Create")
        self.editButton = QPushButton("Edit")
        self.deleteButton = QPushButton("Delete")
        self.createButton.setStyleSheet(bColor)
        self.editButton.setStyleSheet(bColor)
        self.deleteButton.setStyleSheet(bColor)
        self.hboxButtons.addWidget(self.filterButton)
        self.hboxButtons.addItem(QSpacerItem(150,20))
        self.hboxButtons.addWidget(self.createButton)
        self.hboxButtons.addWidget(self.editButton)
        self.hboxButtons.addWidget(self.deleteButton)
        self.vbox.addLayout(self.hboxButtons)
        self.initTable()
        self.hbox3 = QHBoxLayout()
        self.backButton = QPushButton("Back")
        self.backButton.setStyleSheet(bColor)
        self.hbox3.addItem(QSpacerItem(250, 20))
        self.hbox3.addWidget(self.backButton)
        self.hbox3.addItem(QSpacerItem(250, 20))
        self.vbox.addWidget(QLabel("Click a column header to order ascending/descending by that column"))
        self.vbox.addWidget(self.SQLtable)
        self.vbox.addLayout(self.hbox3)
        self.comboItems()
        self.Managers()
        self.setLayout(self.vbox)
        self.resize(700,440)

    def connections(self):
        self.backButton.clicked.connect(self.Back)
        self.SQLtable.horizontalHeader().sectionClicked.connect(self.headerClicked)
        self.filterButton.clicked.connect(self.resetOrder)
        self.createButton.clicked.connect(self.ShowCreateSite)
        self.editButton.clicked.connect(self.ShowEditSite)
        self.deleteButton.clicked.connect(self.DeleteSite)

    def ShowCreateSite(self):
        self.a = CreateSite(self.email, self.usertype, self.username)
        self.a.show()

    def ShowEditSite(self):
        for i in range(self.SQLtable.rowCount()):
            check = self.checkBoxes[i]
            sitename = self.SQLtable.item(i,1).text()
            if check.isChecked():
                name = PyMySQLQs.getEditInfo(sitename)[0]
                address =PyMySQLQs.getEditInfo(sitename)[1]
                zipcode = PyMySQLQs.getEditInfo(sitename)[2]
                print(type(address))
                openEveryday = PyMySQLQs.getEditInfo(sitename)[3]
                manager = PyMySQLQs.getEditInfo(sitename)[4]
                self.a = EditSite(self.email, self.usertype, self.username, name, zipcode, address, manager, openEveryday)
                self.a.show()

    def DeleteSite(self):
        for i in range(self.SQLtable.rowCount()):
            check = self.checkBoxes[i]
            if check.isChecked():
                sitename = self.SQLtable.item(i,1).text()
                manager = self.SQLtable.item(i, 2).text()
                try:
                    PyMySQLQs.deleteSite(sitename, manager)
                    msgBox = QMessageBox()
                    msgBox.setText("Deletion Succesful")
                    msgBox.setWindowTitle("Notification")
                    msgBox.exec_()
                except:
                    msgBox = QMessageBox()
                    msgBox.setText("Can't delete site with events")
                    msgBox.setWindowTitle("Notification")
                    msgBox.exec()
        self.resetOrder()

    def comboItems(self):
        self.siteList = PyMySQLQs.SiteComboBox()
        for aDict in self.siteList:
            for key in aDict:
                self.SiteDrop.addItem(aDict[key])
        #need to add query for manager box
    def Managers(self):
        self.managerList = PyMySQLQs.getManagers()
        for aDict in self.managerList:
            for key in aDict:
                self.managerDrop.addItem(aDict[key])

    def resetOrder(self):
        self.orderTuple = 'no order'
        self.populateTable()

    def Back(self):
        if self.usertype == 'Visitor':
            self.a = VisitorFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'User':
            self.a = UserFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Admin-Only':
            self.a = AdminFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Admin-Visitor':
            self.a = AdminVisFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Staff-Only':
            self.a = StaffFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Staff-Visitor':
            self.a = StaffVisFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Manager-Only':
            self.a = ManagerFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Manager-Visitor':
            self.a = ManagerVisFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Master':
            self.a = Placeholder(self.email, self.usertype, self.username)
        self.a.show()
        self.close()

    def initTable(self):
        self.sqlHeaderList = ['Select','Name','Manager','Open Everyday']
        self.orderdict = ["asc","asc","asc","asc","asc","asc","asc"]
        self.SQLtable = QtWidgets.QTableWidget()
        self.SQLtable.count = 0
        self.checkBoxes = loadTable(self.SQLtable, 'placeholder data', self.sqlHeaderList, 3)
        self.orderTuple = 'no order'

    def populateTable(self):
        site = self.SiteDrop.currentText()
        manager = self.managerDrop.currentText()
        openEveryday = self.openDrop.currentText()
        #UPDATE WHEN PYMYSQLQs HAS QUERIES PUT IN
        self.result = PyMySQLQs.AdminManageSite(self.SQLtable, site, manager, openEveryday, self.orderTuple)
        if type(self.result) == str:
            msgBox = QMessageBox()
            msgBox.setText("{}".format(PyMySQLQs.registerusercheck(fname, lname, username, password, confirmPass, emaillist)))
            msgBox.setWindowTitle("Notification")
            msgBox.exec_()
        else:
            self.checkBoxes = loadTable(self.SQLtable, self.result, self.sqlHeaderList, 3)

    def headerClicked(self):
        col = self.SQLtable.currentColumn()
        if self.orderdict[col] == 'asc':
            self.orderdict[col] = 'desc'
        else:
            self.orderdict[col] = 'asc'
        self.orderTuple = (col, self.orderdict[col])
        self.populateTable()
        self.SQLtable.clearSelection()

#--- 20 ---#
class EditSite(QDialog):
    def __init__(self, email, usertype, username, name, zipcode, address, manager, openEveryday):
        super(EditSite, self).__init__()
        self.email = email
        self.usertype = usertype
        self.username = username
        self.name = name
        self.zipcode = str(zipcode)
        self.address = address
        self.manager = manager
        self.openEveryday = openEveryday
        self.setModal(True)
        self.setWindowTitle("Atlanta Beltline Database")
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.icon = "buzz.png"
        self.setWindowIcon(QIcon(self.icon))
        self.GUI()
        self.connections()

    def GUI(self):
        self.vbox = QVBoxLayout()
        self.title = QLabel("Edit Site")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font: bold 20pt;")
        self.hbox1 = QHBoxLayout()
        self.hbox1.addWidget(QLabel("Name"))
        self.nameEdit = QLineEdit(self.name)
        self.hbox1.addWidget(self.nameEdit)
        self.hbox1.addWidget(QLabel("Zipcode"))
        self.zipEdit = QLineEdit(self.zipcode)
        self.hbox1.addWidget(self.zipEdit)
        self.hbox2 = QHBoxLayout()
        self.hbox2.addWidget(QLabel("Address"))
        self.addressEdit = QLineEdit(self.address)
        self.hbox2.addWidget(self.addressEdit)
        self.hbox3 = QHBoxLayout()
        self.hbox3.addWidget(QLabel("Manager"))
        self.managerDrop = QComboBox()
        self.comboItems()
        self.hbox3.addWidget(self.managerDrop)
        self.openCheck = QCheckBox("Open Everyday")
        self.hbox3.addWidget(self.openCheck)
        if self.openEveryday:
            self.openCheck.setChecked(True)
        self.hbox4 = QHBoxLayout()
        self.backButton = QPushButton("Back")
        self.backButton.setStyleSheet(bColor)
        self.updateButton = QPushButton("Update")
        self.updateButton.setStyleSheet(bColor)
        self.hbox4.addWidget(self.backButton)
        self.hbox4.addItem(QSpacerItem(200, 20))
        self.hbox4.addWidget(self.updateButton)
        self.vbox.addWidget(self.title)
        self.vbox.addLayout(self.hbox1)
        self.vbox.addLayout(self.hbox2)
        self.vbox.addLayout(self.hbox3)
        self.vbox.addLayout(self.hbox4)
        self.setLayout(self.vbox)

    def connections(self):
        self.backButton.clicked.connect(self.Back)
        self.updateButton.clicked.connect(self.Update)

    def comboItems(self):
        self.managerDrop.addItem(self.manager)
        for item in PyMySQLQs.ManagerList():
            self.managerDrop.addItem(item)

    def Back(self):
        self.close()

    def Update(self):
        check = self.openCheck.isChecked()
        if PyMySQLQs.AdminEditCheck(self.zipcode, self.address):
            msgBox = QMessageBox()
            msgBox.setText("{}".format(PyMySQLQs.AdminEditCheck(self.zipcode, self.address)))
            msgBox.setWindowTitle("Notification")
            msgBox.exec_()
        else:
            PyMySQLQs.AdminEditSite(self.name, self.nameEdit.text(), self.zipEdit.text(), self.addressEdit.text(), self.managerDrop.currentText(), check)
            msgBox = QMessageBox()
            msgBox.setText("Update Successful")
            msgBox.setWindowTitle("Notification")
            msgBox.exec_()
        self.close()

#--- 21 ---#
class CreateSite(QDialog):
    def __init__(self, email, usertype, username):
        super(CreateSite, self).__init__()
        self.email = email
        self.usertype = usertype
        self.username = username
        self.setModal(True)
        self.setWindowTitle("Atlanta Beltline Database")
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.icon = "buzz.png"
        self.setWindowIcon(QIcon(self.icon))
        self.GUI()
        self.connections()

    def GUI(self):
        self.vbox = QVBoxLayout()
        self.title = QLabel("Create Site")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font: bold 20pt;")
        self.hbox1 = QHBoxLayout()
        self.hbox1.addWidget(QLabel("Name"))
        self.nameEdit = QLineEdit('')
        self.hbox1.addWidget(self.nameEdit)
        self.hbox1.addWidget(QLabel("Zipcode"))
        self.zipEdit = QLineEdit('')
        self.hbox1.addWidget(self.zipEdit)
        self.hbox2 = QHBoxLayout()
        self.hbox2.addWidget(QLabel("Address"))
        self.addressEdit = QLineEdit('')
        self.hbox2.addWidget(self.addressEdit)
        self.hbox3 = QHBoxLayout()
        self.hbox3.addWidget(QLabel("Manager"))
        self.managerDrop = QComboBox()
        self.comboItems()
        self.hbox3.addWidget(self.managerDrop)
        self.openCheck = QCheckBox("Open Everyday")
        self.hbox3.addWidget(self.openCheck)
        self.hbox4 = QHBoxLayout()
        self.backButton = QPushButton("Back")
        self.backButton.setStyleSheet(bColor)
        self.updateButton = QPushButton("Create")
        self.updateButton.setStyleSheet(bColor)
        self.hbox4.addWidget(self.backButton)
        self.hbox4.addItem(QSpacerItem(200, 20))
        self.hbox4.addWidget(self.updateButton)
        self.vbox.addWidget(self.title)
        self.vbox.addLayout(self.hbox1)
        self.vbox.addLayout(self.hbox2)
        self.vbox.addLayout(self.hbox3)
        self.vbox.addLayout(self.hbox4)
        self.setLayout(self.vbox)

    def connections(self):
        self.backButton.clicked.connect(self.Back)
        self.updateButton.clicked.connect(self.Update)

    def comboItems(self):
        for item in PyMySQLQs.ManagerList():
            self.managerDrop.addItem(item)

    def Back(self):
        self.close()

    def Update(self):
        check = self.openCheck.isChecked()
        if PyMySQLQs.checkSite(self.zipEdit.text(), self.addressEdit.text()):
            msgBox = QMessageBox()
            msgBox.setText("{}".format(PyMySQLQs.checkSite(self.zipEdit.text(), self.addressEdit.text())))
            msgBox.setWindowTitle("Notification")
            msgBox.exec_()
        else:
            PyMySQLQs.createdSite(self.nameEdit.text(), self.zipEdit.text(), self.addressEdit.text(), self.managerDrop.currentText(), check)
            msgBox = QMessageBox()
            msgBox.setText("Create Site Successful")
            msgBox.setWindowTitle("Notification")
            msgBox.exec_()
        self.close()

#--- 22 ---#
class ManageTransit(QDialog):
    def __init__(self, email, usertype, username):
        super(ManageTransit, self).__init__()
        self.email = email
        self.usertype = usertype
        self.username = username
        self.setModal(True)
        self.setWindowTitle("Atlanta Beltline Database")
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.icon = "buzz.png"
        self.setWindowIcon(QIcon(self.icon))
        self.GUI()
        self.connections()

    def GUI(self):
        self.vbox = QVBoxLayout()
        self.title = QLabel("Manage Transit")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font: bold 20pt;")
        self.vbox.addWidget(self.title)
        self.hbox1 = QHBoxLayout()
        self.hbox1.addWidget(QLabel("Transport Type"))
        self.transTypeDrop = QComboBox()
        self.transTypeDrop.addItems(["-ALL-",'Bus', 'MARTA', 'Bike'])
        self.hbox1.addWidget(self.transTypeDrop)
        self.hbox1.addWidget(QLabel("Route"))
        self.routeEdit = QLineEdit("")
        self.hbox1.addWidget(self.routeEdit)
        self.vbox.addLayout(self.hbox1)
        self.hbox2 = QHBoxLayout()
        self.hbox2.addWidget(QLabel("Contain Site"))
        self.siteDrop = QComboBox()
        self.siteDrop.addItem('-ALL-')
        self.hbox2.addWidget(self.siteDrop)
        self.hbox2.addWidget(QLabel("Price Range"))
        self.lowRange = QLineEdit("")
        self.hbox2.addWidget(self.lowRange)
        self.hbox2.addWidget(QLabel("--"))
        self.highRange = QLineEdit("")
        self.hbox2.addWidget(self.highRange)
        self.vbox.addLayout(self.hbox2)
        self.filterButton = QPushButton("Filter")
        self.filterButton.setStyleSheet(bColor)
        self.hboxButtons = QHBoxLayout()
        self.createButton = QPushButton("Create")
        self.editButton = QPushButton("Edit")
        self.deleteButton = QPushButton("Delete")
        self.createButton.setStyleSheet(bColor)
        self.editButton.setStyleSheet(bColor)
        self.deleteButton.setStyleSheet(bColor)
        self.hboxButtons.addWidget(self.filterButton)
        self.hboxButtons.addItem(QSpacerItem(150,20))
        self.hboxButtons.addWidget(self.createButton)
        self.hboxButtons.addWidget(self.editButton)
        self.hboxButtons.addWidget(self.deleteButton)
        self.vbox.addLayout(self.hboxButtons)
        self.initTable()
        self.hbox3 = QHBoxLayout()
        self.backButton = QPushButton("Back")
        self.backButton.setStyleSheet(bColor)
        self.hbox3.addItem(QSpacerItem(250, 20))
        self.hbox3.addWidget(self.backButton)
        self.hbox3.addItem(QSpacerItem(250, 20))
        self.info = QLabel("Click a column header to order ascending/descending by that column")
        self.info.setAlignment(Qt.AlignCenter)
        self.vbox.addWidget(self.info)
        self.vbox.addWidget(self.SQLtable)
        self.vbox.addLayout(self.hbox3)
        self.comboItems()
        self.setLayout(self.vbox)
        self.resize(850,440)

    def connections(self):
        self.backButton.clicked.connect(self.Back)
        self.SQLtable.horizontalHeader().sectionClicked.connect(self.headerClicked)
        self.filterButton.clicked.connect(self.resetOrder)
        self.createButton.clicked.connect(self.ShowCreateTransit)
        self.editButton.clicked.connect(self.ShowEditTransit)
        self.deleteButton.clicked.connect(self.DeleteTransit)

    def ShowCreateTransit(self):
        self.a = CreateTransit(self.email, self.usertype, self.username)
        self.a.show()
        msgBox = QMessageBox()
        msgBox.setText("Deletion Succesful")
        msgBox.setWindowTitle("Notification")
        msgBox.exec_()
        self.populateTable()


    def ShowEditTransit(self):
        for i in range(self.SQLtable.rowCount()):
            check = self.checkBoxes[i]
            if check.isChecked():
                route = self.SQLtable.item(i,1).text()
                transportype = self.SQLtable.item(i, 2).text()
                price = self.SQLtable.item(i, 3).text()
                self.a = EditTransit(self.email, self.usertype, self.username, transportype, route, price)
                self.a.show()
        msgBox = QMessageBox()
        msgBox.setText("Update Succesful")
        msgBox.setWindowTitle("Notification")
        msgBox.exec_()
        self.populateTable()

        #right now after edit the table doesn't auto update itself

    def DeleteTransit(self):
        for i in range(self.SQLtable.rowCount()):
            check = self.checkBoxes[i]
            if check.isChecked():
                route = self.SQLtable.item(i,1).text()
                transportType = self.SQLtable.item(i,2).text()
                price = self.SQLtable.item(i,3).text()
                numConnected = self.SQLtable.item(i,4).text()
                self.SQLtable.clearSelection()
                self.result = PyMySQLQs.deletetransit(route, transportType)
                msgBox = QMessageBox()
                msgBox.setText("Deletion Succesful")
                msgBox.setWindowTitle("Notification")
                msgBox.exec_()
        self.populateTable()

    def comboItems(self):
        self.siteList = PyMySQLQs.SiteComboBox()
        for aDict in self.siteList:
            for key in aDict:
                self.siteDrop.addItem(aDict[key])

    def resetOrder(self):
        self.orderTuple = 'no order'
        self.populateTable()

    def Back(self):
        if self.usertype == 'Visitor':
            self.a = VisitorFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'User':
            self.a = UserFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Admin-Only':
            self.a = AdminFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Admin-Visitor':
            self.a = AdminVisFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Staff-Only':
            self.a = StaffFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Staff-Visitor':
            self.a = StaffVisFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Manager-Only':
            self.a = ManagerFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Manager-Visitor':
            self.a = ManagerVisFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Master':
            self.a = Placeholder(self.email, self.usertype, self.username)
        self.a.show()
        self.close()

    def initTable(self):
        self.sqlHeaderList = ['Select','Route','Transport Type','Price','# Connected Sites','# Transit Logged']
        self.orderdict = ["asc","asc","asc","asc","asc","asc","asc"]
        self.SQLtable = QtWidgets.QTableWidget()
        self.SQLtable.count = 0
        self.checkBoxes = loadTable(self.SQLtable, 'placeholder data', self.sqlHeaderList, 5)
        self.orderTuple = 'no order'

    def populateTable(self):
        transType = self.transTypeDrop.currentText()
        route = self.routeEdit.text()
        site = self.siteDrop.currentText()
        lowRange = self.lowRange.text()
        highRange = self.highRange.text()
        #UPDATE WHEN PYMYSQLQs HAS QUERIES PUT IN
        self.result = PyMySQLQs.editManageTransit(self.SQLtable, site, transType, lowRange, highRange, route, self.orderTuple)
        if type(self.result) == str:
            msgBox = QMessageBox()
            msgBox.setText("{}".format(PyMySQLQs.editManageTransit(self.SQLtable, site, transType, lowRange, highRange, route, self.orderTuple)))
            msgBox.setWindowTitle("Notification")
            msgBox.exec_()
        else:
            self.checkBoxes = loadTable(self.SQLtable, self.result, self.sqlHeaderList, 5)

    def headerClicked(self):
        col = self.SQLtable.currentColumn()
        if col == 1 or col == 2:
            if self.orderdict[col] == 'asc':
                self.orderdict[col] = 'desc'
            else:
                self.orderdict[col] = 'asc'
            self.orderTuple = (col, self.orderdict[col])
            self.populateTable()
            self.SQLtable.clearSelection()

#--- 23 ---#
class EditTransit(QDialog):
    def __init__(self, email, usertype, username, transType, route, price):
        super(EditTransit, self).__init__()
        self.email = email
        self.usertype = usertype
        self.username = username
        self.transType = transType
        self.route = route
        self.price = price
        self.setModal(True)
        self.setWindowTitle("Atlanta Beltline Database")
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.icon = "buzz.png"
        self.setWindowIcon(QIcon(self.icon))
        self.GUI()
        self.connections()

    def GUI(self):
        self.vbox = QVBoxLayout()
        self.title = QLabel("Edit Transit")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font: bold 20pt;")
        self.hbox1 = QHBoxLayout()
        self.hbox1.addWidget(QLabel("Transport Type"))
        self.transTypeLabel = QLabel(self.transType)
        self.transTypeLabel.setStyleSheet("font: bold;")
        self.hbox1.addWidget(self.transTypeLabel)
        self.hbox1.addWidget(QLabel("Route"))
        self.routeEdit = QLineEdit(self.route)
        self.hbox1.addWidget(self.routeEdit)
        self.hbox1.addWidget(QLabel("Price ($)"))
        self.priceEdit = QLineEdit(self.price)
        self.hbox1.addWidget(self.priceEdit)
        self.hbox2 = QHBoxLayout()
        self.hbox2.addWidget(QLabel("Connected Sites"))
        self.siteList = QListWidget()
        self.hbox2.addWidget(self.siteList)
        self.siteList.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.hbox4 = QHBoxLayout()
        self.backButton = QPushButton("Back")
        self.updateButton = QPushButton("Update")
        self.hbox4.addWidget(self.backButton)
        self.hbox4.addItem(QSpacerItem(200, 20))
        self.hbox4.addWidget(self.updateButton)
        self.vbox.addWidget(self.title)
        self.vbox.addLayout(self.hbox1)
        self.vbox.addLayout(self.hbox2)
        self.vbox.addLayout(self.hbox4)
        self.getSites()
        self.setLayout(self.vbox)


    def getSites(self):
        self.sitesQ = PyMySQLQs.SiteComboBox()
        for aDict in self.sitesQ:
            for key in aDict:
                self.siteList.addItem(aDict[key])
        for item1 in PyMySQLQs.ListOfSites(self.transType, self.route):
            matching_items = self.siteList.findItems(item1, Qt.MatchExactly)
            for thing in matching_items:
                thing.setSelected(True)


    def connections(self):
        self.backButton.clicked.connect(self.Back)
        self.updateButton.clicked.connect(self.Update)

    def comboItems(self):
        self.managerDrop.addItem(self.manager)
        #need to add query for manager box

    def Back(self):
        self.close()

    def Update(self):
        selecteditems = [str(x.text()) for x in self.siteList.selectedItems()]
        PyMySQLQs.EditTransit(self.transTypeLabel.text(), self.route, self.routeEdit.text(), self.priceEdit.text(), selecteditems)

#--- 24 ---#
class CreateTransit(QDialog):
    def __init__(self, email, usertype, username):
        super(CreateTransit, self).__init__()
        self.email = email
        self.usertype = usertype
        self.username = username
        self.setModal(True)
        self.setWindowTitle("Atlanta Beltline Database")
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.icon = "buzz.png"
        self.setWindowIcon(QIcon(self.icon))
        self.GUI()
        self.connections()

    def GUI(self):
        self.vbox = QVBoxLayout()
        self.title = QLabel("Create Transit")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font: bold 20pt;")
        self.hbox1 = QHBoxLayout()
        self.hbox1.addWidget(QLabel("Transport Type"))
        self.transTypeDrop = QComboBox()
        self.transTypeDrop.addItems(['Bus', 'MARTA', 'Bike'])
        self.hbox1.addWidget(self.transTypeDrop)
        self.hbox1.addWidget(QLabel("Route"))
        self.routeEdit = QLineEdit("")
        self.hbox1.addWidget(self.routeEdit)
        self.hbox1.addWidget(QLabel("Price ($)"))
        self.priceEdit = QLineEdit("")
        self.hbox1.addWidget(self.priceEdit)
        self.hbox2 = QHBoxLayout()
        self.hbox2.addWidget(QLabel("Connected Sites"))
        self.siteList = QListWidget()
        self.hbox2.addWidget(self.siteList)
        self.siteList.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.hbox4 = QHBoxLayout()
        self.backButton = QPushButton("Back")
        self.updateButton = QPushButton("Create")
        self.backButton.setStyleSheet(bColor)
        self.updateButton.setStyleSheet(bColor)
        self.hbox4.addWidget(self.backButton)
        self.hbox4.addItem(QSpacerItem(200, 20))
        self.hbox4.addWidget(self.updateButton)
        self.vbox.addWidget(self.title)
        self.vbox.addLayout(self.hbox1)
        self.vbox.addLayout(self.hbox2)
        self.vbox.addLayout(self.hbox4)
        self.getSites()
        self.setLayout(self.vbox)

    def getSites(self):
        self.sitesQ = PyMySQLQs.SiteComboBox()
        for aDict in self.sitesQ:
            for key in aDict:
                self.siteList.addItem(aDict[key])

    def connections(self):
        self.backButton.clicked.connect(self.Back)
        self.updateButton.clicked.connect(self.Update)

    def comboItems(self):
        self.managerDrop.addItem(self.manager)
        #need to add query for manager box

    def Back(self):
        self.close()

    def Update(self):
        selecteditems = [str(x.text()) for x in self.siteList.selectedItems()]
        PyMySQLQs.CreateTransit(self.transTypeDrop.currentText(), self.routeEdit.text(), self.priceEdit.text(), selecteditems)


#--- 25 ---#
class ManageEvent(QDialog):
    def __init__(self, email, usertype, username):
        super(ManageEvent, self).__init__()
        self.email = email
        self.usertype = usertype
        self.username = username
        self.site = PyMySQLQs.getManSite(username)
        self.setModal(True)
        self.setWindowTitle("Atlanta Beltline Database")
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.icon = "buzz.png"
        self.setWindowIcon(QIcon(self.icon))
        self.GUI()
        self.connections()

    def GUI(self):
        self.vbox = QVBoxLayout()
        self.title = QLabel("Manage Event")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font: bold 20pt;")
        self.vbox.addWidget(self.title)
        self.grid = QGridLayout()
        self.grid.addWidget(QLabel("Name"),0,0)
        self.nameEdit = QLineEdit("")
        self.grid.addWidget(self.nameEdit,0,1)
        self.grid.addWidget(QLabel("Description Keyword"),0,2)
        self.keyword = QLineEdit("")
        self.grid.addWidget(self.keyword,0,3)
        self.grid.addWidget(QLabel("Start Date"),1,0)
        self.startDateEdit = QLineEdit("")
        self.grid.addWidget(self.startDateEdit,1,1)
        self.vbox.addLayout(self.grid)
        self.hbox3 = QHBoxLayout()
        self.hbox3.addWidget(QLabel("Duration Range"))
        self.lowDuration = QLineEdit("")
        self.hbox3.addWidget(self.lowDuration)
        self.hbox3.addWidget(QLabel("--"))
        self.highDuration = QLineEdit("")
        self.hbox3.addWidget(self.highDuration)
        self.hbox3.addWidget(QLabel("Total Visits Range"))
        self.lowVisit = QLineEdit("")
        self.hbox3.addWidget(self.lowVisit)
        self.hbox3.addWidget(QLabel("--"))
        self.highVisit = QLineEdit("")
        self.hbox3.addWidget(self.highVisit)
        self.vbox.addLayout(self.hbox3)
        self.hbox4 = QHBoxLayout()
        self.hbox4.addItem(QSpacerItem(200,20))
        self.hbox4.addWidget(QLabel("Total Revenue Range"))
        self.lowRev = QLineEdit("")
        self.hbox4.addWidget(self.lowRev)
        self.hbox4.addWidget(QLabel("--"))
        self.highRev = QLineEdit("")
        self.hbox4.addWidget(self.highRev)
        self.hbox4.addItem(QSpacerItem(200,20))
        self.vbox.addLayout(self.hbox4)
        self.filterButton = QPushButton("Filter")
        self.filterButton.setStyleSheet(bColor)
        self.hboxButtons = QHBoxLayout()
        self.createButton = QPushButton("Create")
        self.editButton = QPushButton("View/Edit")
        self.deleteButton = QPushButton("Delete")
        self.createButton.setStyleSheet(bColor)
        self.editButton.setStyleSheet(bColor)
        self.deleteButton.setStyleSheet(bColor)
        self.hboxButtons.addWidget(self.filterButton)
        self.hboxButtons.addItem(QSpacerItem(150,20))
        self.hboxButtons.addWidget(self.createButton)
        self.hboxButtons.addWidget(self.editButton)
        self.hboxButtons.addWidget(self.deleteButton)
        self.vbox.addLayout(self.hboxButtons)
        self.initTable()
        self.hboxBack = QHBoxLayout()
        self.backButton = QPushButton("Back")
        self.backButton.setStyleSheet(bColor)
        self.hboxBack.addItem(QSpacerItem(300, 20))
        self.hboxBack.addWidget(self.backButton)
        self.hboxBack.addItem(QSpacerItem(300, 20))
        self.info = QLabel("Click a column header to order ascending/descending by that column")
        self.info.setAlignment(Qt.AlignCenter)
        self.vbox.addWidget(self.info)
        self.vbox.addWidget(self.SQLtable)
        self.vbox.addLayout(self.hboxBack)
        self.setLayout(self.vbox)
        self.resize(900,650)

    def connections(self):
        self.backButton.clicked.connect(self.Back)
        self.SQLtable.horizontalHeader().sectionClicked.connect(self.headerClicked)
        self.filterButton.clicked.connect(self.resetOrder)
        self.createButton.clicked.connect(self.ShowCreateEvent)
        self.editButton.clicked.connect(self.ShowViewEditEvent)
        self.deleteButton.clicked.connect(self.DeleteEvent)

    def ShowCreateEvent(self):
        self.a = CreateEvent(self.email,self.usertype, self.username)
        self.a.show()

    def ShowViewEditEvent(self):
        for i in range(self.SQLtable.rowCount()):
            check = self.checkBoxes[i]
            if check.isChecked():
                eventName = self.SQLtable.item(i,1).text()
                startDate = self.SQLtable.item(i,2).text()
                self.SQLtable.clearSelection()
                self.a = ViewEditEvent(self.site, eventName, startDate)
                self.a.show()

    def DeleteEvent(self):
        for i in range(self.SQLtable.rowCount()):
            check = self.checkBoxes[i]
            if check.isChecked():
                eventName = self.SQLtable.item(i,1).text()
                startDate = self.SQLtable.item(i,2).text()
                self.SQLtable.clearSelection()
                self.result = PyMySQLQs.deleteEvent(eventName, startDate, self.site)
                msgBox = QMessageBox()
                msgBox.setText("Deletion Succesful")
                msgBox.setWindowTitle("Notification")
                msgBox.exec_()
        self.populateTable()

    def resetOrder(self):
        self.orderTuple = 'no order'
        self.populateTable()

    def Back(self):
        if self.usertype == 'Visitor':
            self.a = VisitorFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'User':
            self.a = UserFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Admin-Only':
            self.a = AdminFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Admin-Visitor':
            self.a = AdminVisFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Staff-Only':
            self.a = StaffFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Staff-Visitor':
            self.a = StaffVisFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Manager-Only':
            self.a = ManagerFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Manager-Visitor':
            self.a = ManagerVisFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Master':
            self.a = Placeholder(self.email, self.usertype, self.username)
        self.a.show()
        self.close()

    def initTable(self):
        self.sqlHeaderList = ['Select','Name','Start Date','Staff Count','Duration (days)','Total Visits','Total Revenue ($)']
        self.orderdict = ["asc","asc","asc","asc","asc","asc","asc"]
        self.SQLtable = QtWidgets.QTableWidget()
        self.SQLtable.count = 0
        self.checkBoxes = loadTable(self.SQLtable, 'placeholder data', self.sqlHeaderList, 6)
        self.orderTuple = 'no order'

    def populateTable(self):
        name = self.nameEdit.text()
        keyword = self.keyword.text()
        durLow = self.lowDuration.text()
        durHigh = self.highDuration.text()
        visLow = self.lowVisit.text()
        visHigh = self.highVisit.text()
        revLow = self.lowRev.text()
        revHigh = self.highRev.text()
        startDate = self.startDateEdit.text()
        self.result = PyMySQLQs.GetManageEvent(self.site, name, startDate, keyword, durLow, durHigh, visLow, visHigh, revLow, revHigh, self.orderTuple)
        if type(self.result) == str:
            msgBox = QMessageBox()
            msgBox.setText("{}".format(self.result))
            msgBox.setWindowTitle("Notification")
            msgBox.exec_()
        else:
            self.checkBoxes = loadTable(self.SQLtable, self.result, self.sqlHeaderList, 6)

    def headerClicked(self):
        col = self.SQLtable.currentColumn()
        if col != -1:
            if self.orderdict[col] == 'asc':
                self.orderdict[col] = 'desc'
            else:
                self.orderdict[col] = 'asc'
            self.orderTuple = (col, self.orderdict[col])
            self.populateTable()
            self.SQLtable.clearSelection()

#--- 26 ---#
class ViewEditEvent(QDialog):
    def __init__(self, site, name, startDate):
        super(ViewEditEvent, self).__init__()
        self.site = site
        self.name = name
        self.startDate = startDate
        self.setModal(True)
        self.setWindowTitle("Atlanta Beltline Database")
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.icon = "buzz.png"
        self.setWindowIcon(QIcon(self.icon))
        self.getInfo()
        self.GUI()
        self.connections()
        self.getAssignedStaff()

    def getInfo(self):
        infoDict1 = PyMySQLQs.getEventInfo2(self.site, self.name, self.startDate)[0]
        self.endDate = infoDict1['EndDate']
        self.price = infoDict1['EventPrice']
        self.minStaff = infoDict1['MinStaffRequired']
        self.capacity = infoDict1['Capacity']
        self.description = infoDict1['Description']

    def GUI(self):
        self.vbox = QVBoxLayout()
        self.title = QLabel("View/Edit Event")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font: bold 20pt;")
        self.vbox.addWidget(self.title)
        self.hbox1 = QHBoxLayout()
        self.nameLabel = QLabel(self.name)
        self.hbox1.addWidget(QLabel("Name"))
        self.hbox1.addWidget(self.nameLabel)
        self.nameLabel.setStyleSheet("font: bold;")
        self.hbox1.addWidget(QLabel("Price ($)"))
        self.priceLabel = QLabel(self.price)
        self.priceLabel.setStyleSheet("font: bold;")
        self.hbox1.addWidget(self.priceLabel)
        self.vbox.addLayout(self.hbox1)
        self.hbox2 = QHBoxLayout()
        self.hbox2.addWidget(QLabel("Start Date"))
        self.dateStart = QLabel(self.startDate)
        self.dateStart.setStyleSheet("font: bold;")
        self.hbox2.addWidget(self.dateStart)
        self.hbox2.addWidget(QLabel("End Date"))
        self.dateEnd = QLabel(self.endDate.strftime('%Y-%m-%d'))
        self.dateEnd.setStyleSheet("font: bold;")
        self.hbox2.addWidget(self.dateEnd)
        self.vbox.addLayout(self.hbox2)
        self.hbox3 = QHBoxLayout()
        self.hbox3.addWidget(QLabel("Minimum Staff Required"))
        self.staffReq = QLabel(str(self.minStaff))
        self.staffReq.setStyleSheet("font: bold;")
        self.hbox3.addWidget(self.staffReq)
        self.hbox3.addWidget(QLabel("Capacity"))
        self.capLabel = QLabel(str(self.capacity))
        self.capLabel.setStyleSheet("font: bold;")
        self.hbox3.addWidget(self.capLabel)
        self.vbox.addLayout(self.hbox3)
        self.grid2 = QGridLayout()
        self.grid2.addWidget(QLabel("Staff Assigned"),0,0)
        self.staffList = QListWidget()
        self.staffList.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.grid2.addWidget(self.staffList,0,1)
        self.grid2.addWidget(QLabel("Description"),1,0)
        self.descriptionText = QPlainTextEdit(self.description)
        self.descriptionText.resize(100, 300)
        self.grid2.addWidget(self.descriptionText,1,1)
        self.vbox.addLayout(self.grid2)
        self.hbox6 = QHBoxLayout()
        self.hbox6.addWidget(QLabel("Daily Visits Range"))
        self.visitLow = QLineEdit("")
        self.hbox6.addWidget(self.visitLow)
        self.hbox6.addWidget(QLabel("--"))
        self.visitHigh = QLineEdit("")
        self.hbox6.addWidget(self.visitHigh)
        self.hbox6.addWidget(QLabel("Daily Revenue Range"))
        self.revLow = QLineEdit("")
        self.hbox6.addWidget(self.revLow)
        self.hbox6.addWidget(QLabel("--"))
        self.revHigh = QLineEdit("")
        self.hbox6.addWidget(self.revHigh)
        self.vbox.addLayout(self.hbox6)
        self.filterButton = QPushButton("Filter")
        self.filterButton.setStyleSheet(bColor)
        self.hboxButtons = QHBoxLayout()
        self.updateButton = QPushButton("Update")
        self.updateButton.setStyleSheet(bColor)
        self.hboxButtons.addWidget(self.filterButton)
        self.hboxButtons.addItem(QSpacerItem(250,20))
        self.hboxButtons.addWidget(self.updateButton)
        self.vbox.addLayout(self.hboxButtons)
        self.initTable()
        self.hboxBack = QHBoxLayout()
        self.backButton = QPushButton("Back")
        self.backButton.setStyleSheet(bColor)
        self.hboxBack.addItem(QSpacerItem(250, 20))
        self.hboxBack.addWidget(self.backButton)
        self.hboxBack.addItem(QSpacerItem(250, 20))
        self.info = QLabel("Click a column header to order ascending/descending by that column")
        self.info.setAlignment(Qt.AlignCenter)
        self.vbox.addWidget(self.info)
        self.vbox.addWidget(self.SQLtable)
        self.vbox.addLayout(self.hboxBack)
        self.setLayout(self.vbox)
        self.resize(400,800)

    def getAssignedStaff(self):
        self.assignedStaff = PyMySQLQs.getAssignedStaff(self.site, self.name, self.startDate)
        for name in PyMySQLQs.getAllStaff():
            self.staffList.addItem(name)
        for item1 in self.assignedStaff:
            matching_items = self.staffList.findItems(item1, Qt.MatchExactly)
            for thing in matching_items:
                thing.setSelected(True)

    def connections(self):
        self.backButton.clicked.connect(self.Back)
        self.SQLtable.horizontalHeader().sectionClicked.connect(self.headerClicked)
        self.filterButton.clicked.connect(self.resetOrder)
        self.updateButton.clicked.connect(self.updateEvent)

    def updateEvent(self):
        selecteditems = [str(x.text()) for x in self.staffList.selectedItems()]
        if len(selecteditems) < int(self.staffReq.text()):
            msgBox = QMessageBox()
            msgBox.setText("Please select at least the minimum number of staff required for this event")
            msgBox.setWindowTitle("Notification")
            msgBox.exec_()
        else:
            PyMySQLQs.updateDescription(self.site, self.name, self.startDate, self.descriptionText.toPlainText(), selecteditems)
            print('event updated')
        #reload table

    def resetOrder(self):
        self.orderTuple = 'no order'
        self.populateTable()

    def Back(self):
        self.close()

    def initTable(self):
        self.sqlHeaderList = ['Date','Daily Visits','Daily Revenue ($)']
        self.orderdict = ["asc","asc","asc","asc","asc","asc","asc"]
        self.SQLtable = QtWidgets.QTableWidget()
        self.SQLtable.count = 0
        self.checkBoxes = loadTableNoCheck(self.SQLtable, 'placeholder data', self.sqlHeaderList,3)
        self.orderTuple = 'no order'

    def populateTable(self):
        self.result = PyMySQLQs.SpecificEventTable(self.name, self.startDate, self.orderTuple)
        print(self.result)
        if type(self.result) == str:
            msgBox = QMessageBox()
            msgBox.setText("{}".format(PyMySQLQs.registerusercheck(fname, lname, username, password, confirmPass, emaillist)))
            msgBox.setWindowTitle("Notification")
            msgBox.exec_()
        else:
            self.checkBoxes = loadTableNoCheck(self.SQLtable, self.result, self.sqlHeaderList,3)

    def headerClicked(self):
        col = self.SQLtable.currentColumn()
        if col != -1:
            if self.orderdict[col] == 'asc':
                self.orderdict[col] = 'desc'
            else:
                self.orderdict[col] = 'asc'
            self.orderTuple = (col, self.orderdict[col])
            self.populateTable()
            self.SQLtable.clearSelection()

#--- 27 ---#
class CreateEvent(QDialog):
    def __init__(self, email, usertype, username):
        super(CreateEvent, self).__init__()
        self.email = email
        self.usertype = usertype
        self.username = username
        self.site = PyMySQLQs.getManSite(username)
        self.setModal(True)
        self.setWindowTitle("Atlanta Beltline Database")
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.icon = "buzz.png"
        self.setWindowIcon(QIcon(self.icon))
        self.GUI()
        self.connections()

    def GUI(self):
        self.vbox = QVBoxLayout()
        self.title = QLabel("Create Event")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font: bold 20pt;")
        self.vbox.addWidget(self.title)
        self.grid = QGridLayout()
        self.hbox1 = QHBoxLayout()
        self.grid.addWidget(QLabel("Name"),0,0)
        self.name = QLineEdit("")
        self.hbox1.addWidget(self.name)
        self.grid.addLayout(self.hbox1,0,1)
        self.hbox2 = QHBoxLayout()
        self.grid.addWidget(QLabel("Price $"),1,0)
        self.price = QLineEdit("")
        self.hbox2.addWidget(self.price)
        self.hbox2.addWidget(QLabel("Capacity"))
        self.capacity = QLineEdit("")
        self.hbox2.addWidget(self.capacity)
        self.minStaff = QLineEdit("")
        self.hbox2.addWidget(QLabel("Minimum Staff Required"))
        self.hbox2.addWidget(self.minStaff)
        self.grid.addLayout(self.hbox2,1,1)
        self.hbox3 = QHBoxLayout()
        self.grid.addWidget(QLabel("Start Date"),2,0)
        self.startDateEdit = QLineEdit("")
        self.hbox3.addWidget(self.startDateEdit)
        self.hbox3.addWidget(QLabel("End Date"))
        self.endDateEdit = QLineEdit("")
        self.hbox3.addWidget(self.endDateEdit)
        self.grid.addLayout(self.hbox3,2,1)
        self.grid.addWidget(QLabel("Description"),3,0)
        self.descriptionText = QPlainTextEdit("")
        self.descriptionText.resize(100, 300)
        self.grid.addWidget(self.descriptionText,3,1)
        self.grid.addWidget(QLabel("Assign Staff"),4,0)
        self.staffList = QListWidget()
        self.staffList.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.grid.addWidget(self.staffList,4,1)
        self.vbox.addLayout(self.grid)
        self.hboxBack = QHBoxLayout()
        self.backButton = QPushButton("Back")
        self.backButton.setStyleSheet(bColor)
        self.hboxBack.addWidget(self.backButton)
        self.hboxBack.addItem(QSpacerItem(250, 20))
        self.createButton = QPushButton("Create")
        self.createButton.setStyleSheet(bColor)
        self.hboxBack.addWidget(self.createButton)
        self.vbox.addLayout(self.hboxBack)
        self.setLayout(self.vbox)
        self.resize(400,500)
        self.addtositelist()

    def addtositelist(self):
        stafflist = PyMySQLQs.getAllStaff()
        for item in stafflist:
            self.staffList.addItem(item)

    def connections(self):
        self.backButton.clicked.connect(self.Back)
        self.createButton.clicked.connect(self.CreateNewEvent)

    def CreateNewEvent(self):
        #query site name
        sitename = PyMySQLQs.getManSite(self.username)
        selecteditems = [str(x.text()) for x in self.staffList.selectedItems()]
        PyMySQLQs.createEvent(self.username, self.name.text(), self.startDateEdit.text(), sitename, self.endDateEdit.text(), self.price.text(), self.capacity.text(), self.minStaff.text(), self.descriptionText.toPlainText(), selecteditems)
        msgBox = QMessageBox()
        msgBox.setText("Event Created!")
        msgBox.setWindowTitle("Notification")
        msgBox.exec_()


    def Back(self):
        self.close()

#--- 28 ---#
class ViewStaff(QDialog):
    def __init__(self, email, usertype, username):
        super(ViewStaff, self).__init__()
        self.email = email
        self.usertype = usertype
        self.username = username
        self.site = PyMySQLQs.getManSite(username)
        self.setModal(True)
        self.setWindowTitle("Atlanta Beltline Database")
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.icon = "buzz.png"
        self.setWindowIcon(QIcon(self.icon))
        self.GUI()
        self.connections()

    def GUI(self):
        self.vbox = QVBoxLayout()
        self.title = QLabel("View Staff")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font: bold 20pt;")
        self.vbox.addWidget(self.title)
        self.grid1 = QGridLayout()
        self.grid1.addWidget(QLabel(""),0,0)
        self.site = QLabel("Site")
        self.site.setAlignment(Qt.AlignRight)
        self.grid1.addWidget(self.site,0,1)
        self.siteDrop = QComboBox()
        self.siteDrop.addItem("-ALL-")
        self.grid1.addWidget(self.siteDrop,0,2)
        self.grid1.addWidget(QLabel(""),0,3)
        self.comboItems()
        self.vbox.addLayout(self.grid1)
        self.grid = QGridLayout()
        self.grid.addWidget(QLabel("First Name"),0,0)
        self.fnameEdit = QLineEdit("")
        self.grid.addWidget(self.fnameEdit,0,1)
        self.grid.addWidget(QLabel("Last Name"),0,2)
        self.lnameEdit = QLineEdit("")
        self.grid.addWidget(self.lnameEdit,0,3)
        self.grid.addWidget(QLabel("Start Date"),1,0)
        self.startDateEdit = QLineEdit("")
        self.grid.addWidget(self.startDateEdit,1,1)
        self.grid.addWidget(QLabel("End Date"),1,2)
        self.endDateEdit = QLineEdit("")
        self.grid.addWidget(self.endDateEdit,1,3)
        self.vbox.addLayout(self.grid)
        self.filterButton = QPushButton("Filter")
        self.filterButton.setStyleSheet(bColor)
        self.hboxButtons = QHBoxLayout()
        self.hboxButtons.addItem(QSpacerItem(100,20))
        self.hboxButtons.addWidget(self.filterButton)
        self.hboxButtons.addItem(QSpacerItem(100,20))
        self.vbox.addLayout(self.hboxButtons)
        self.initTable()
        self.SQLtable.resize(200,300)
        self.hboxBack = QHBoxLayout()
        self.backButton = QPushButton("Back")
        self.backButton.setStyleSheet(bColor)
        self.hboxBack.addItem(QSpacerItem(100, 20))
        self.hboxBack.addWidget(self.backButton)
        self.hboxBack.addItem(QSpacerItem(100, 20))
        self.info = QLabel("Click a column header to order ascending/descending by that column")
        self.info.setAlignment(Qt.AlignCenter)
        self.vbox.addWidget(self.info)
        self.vbox.addWidget(self.SQLtable)
        self.vbox.addLayout(self.hboxBack)
        self.setLayout(self.vbox)
        self.resize(300,500)

    def connections(self):
        self.backButton.clicked.connect(self.Back)
        self.SQLtable.horizontalHeader().sectionClicked.connect(self.headerClicked)
        self.filterButton.clicked.connect(self.resetOrder)

    def comboItems(self):
        self.siteList = PyMySQLQs.SiteComboBox()
        for aDict in self.siteList:
            for key in aDict:
                self.siteDrop.addItem(aDict[key])

    def resetOrder(self):
        self.orderTuple = 'no order'
        self.populateTable()

    def Back(self):
        if self.usertype == 'Visitor':
            self.a = VisitorFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'User':
            self.a = UserFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Admin-Only':
            self.a = AdminFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Admin-Visitor':
            self.a = AdminVisFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Staff-Only':
            self.a = StaffFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Staff-Visitor':
            self.a = StaffVisFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Manager-Only':
            self.a = ManagerFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Manager-Visitor':
            self.a = ManagerVisFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Master':
            self.a = Placeholder(self.email, self.usertype, self.username)
        self.a.show()
        self.close()

    def initTable(self):
        self.sqlHeaderList = ['Staff Name','# Event Shifts']
        self.orderdict = ["asc","asc","asc","asc","asc","asc","asc"]
        self.SQLtable = QtWidgets.QTableWidget()
        self.SQLtable.count = 0
        self.checkBoxes = loadTableNoCheck(self.SQLtable, 'placeholder data', self.sqlHeaderList,2)
        self.orderTuple = 'no order'

    def populateTable(self):
        fname = self.fnameEdit.text()
        lname = self.lnameEdit.text()
        site = self.siteDrop.currentText()
        startDate = self.startDateEdit.text()
        endDate = self.endDateEdit.text()
        self.result = PyMySQLQs.ManageStaff(self.SQLtable, site, fname, lname, startDate, endDate, self.orderTuple)
        if type(self.result) == str:
            msgBox = QMessageBox()
            msgBox.setText("{}".format(self.result))
            msgBox.setWindowTitle("Notification")
            msgBox.exec_()
        else:
            self.checkBoxes = loadTableNoCheck(self.SQLtable, self.result, self.sqlHeaderList,2)

    def headerClicked(self):
        col = self.SQLtable.currentColumn()
        if col != -1:
            if self.orderdict[col] == 'asc':
                self.orderdict[col] = 'desc'
            else:
                self.orderdict[col] = 'asc'
            self.orderTuple = (col, self.orderdict[col])
            self.populateTable()
            self.SQLtable.clearSelection()

#--- 29 ---#
class ViewSiteReport(QDialog):
    def __init__(self, email, usertype, username):
        super(ViewSiteReport, self).__init__()
        self.email = email
        self.usertype = usertype
        self.username = username
        self.site = PyMySQLQs.getManSite(username)
        self.setModal(True)
        self.setWindowTitle("Atlanta Beltline Database")
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.icon = "buzz.png"
        self.setWindowIcon(QIcon(self.icon))
        self.GUI()
        self.connections()

    def GUI(self):
        self.vbox = QVBoxLayout()
        self.title = QLabel("Site Report")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font: bold 20pt;")
        self.vbox.addWidget(self.title)
        self.hbox3 = QHBoxLayout()
        self.hbox3.addWidget(QLabel("Start Date"))
        self.startDateEdit = QLineEdit("")
        self.hbox3.addWidget(self.startDateEdit)
        self.hbox3.addWidget(QLabel("End Date"))
        self.endDateEdit = QLineEdit("")
        self.hbox3.addWidget(self.endDateEdit)
        self.vbox.addLayout(self.hbox3)
        self.grid = QGridLayout()
        self.grid.addWidget(QLabel("Event Count Range"),0,0)
        self.lowEvent = QLineEdit("")
        self.grid.addWidget(self.lowEvent,0,1)
        self.grid.addWidget(QLabel("--"),0,2)
        self.highEvent = QLineEdit("")
        self.grid.addWidget(self.highEvent,0,3)
        self.grid.addWidget(QLabel("Staff Count Range"),0,4)
        self.lowStaff = QLineEdit("")
        self.grid.addWidget(self.lowStaff,0,5)
        self.grid.addWidget(QLabel("--"),0,6)
        self.highStaff = QLineEdit("")
        self.grid.addWidget(self.highStaff,0,7)
        self.grid.addWidget(QLabel("Total Visits Range"),1,0)
        self.lowVisit = QLineEdit("")
        self.grid.addWidget(self.lowVisit,1,1)
        self.grid.addWidget(QLabel("--"),1,2)
        self.highVisit = QLineEdit("")
        self.grid.addWidget(self.highVisit,1,3)
        self.grid.addWidget(QLabel("Total Revenue Range"),1,4)
        self.lowRev = QLineEdit("")
        self.grid.addWidget(self.lowRev,1,5)
        self.grid.addWidget(QLabel("--"),1,6)
        self.highRev = QLineEdit("")
        self.grid.addWidget(self.highRev,1,7)
        self.vbox.addLayout(self.grid)
        self.filterButton = QPushButton("Filter")
        self.filterButton.setStyleSheet(bColor)
        self.hboxButtons = QHBoxLayout()
        self.dailyDetailButton = QPushButton("Daily Detail")
        self.dailyDetailButton.setStyleSheet(bColor)
        self.hboxButtons.addWidget(self.filterButton)
        self.hboxButtons.addItem(QSpacerItem(400,20))
        self.hboxButtons.addWidget(self.dailyDetailButton)
        self.vbox.addLayout(self.hboxButtons)
        self.initTable()
        self.hboxBack = QHBoxLayout()
        self.backButton = QPushButton("Back")
        self.backButton.setStyleSheet(bColor)
        self.hboxBack.addItem(QSpacerItem(300, 20))
        self.hboxBack.addWidget(self.backButton)
        self.hboxBack.addItem(QSpacerItem(300, 20))
        self.info = QLabel("Click a column header to order ascending/descending by that column")
        self.info.setAlignment(Qt.AlignCenter)
        self.vbox.addWidget(self.info)
        self.vbox.addWidget(self.SQLtable)
        self.vbox.addLayout(self.hboxBack)
        self.setLayout(self.vbox)
        self.resize(780,440)

    def connections(self):
        self.backButton.clicked.connect(self.Back)
        self.SQLtable.horizontalHeader().sectionClicked.connect(self.headerClicked)
        self.filterButton.clicked.connect(self.resetOrder)
        self.dailyDetailButton.clicked.connect(self.ShowDailyDetail)

    def ShowDailyDetail(self):
        for i in range(self.SQLtable.rowCount()):
            check = self.checkBoxes[i]
            if check.isChecked():
                date = self.SQLtable.item(i,1).text()
                site = self.site
                self.a = ViewDailyDetail(date, site)
                self.a.show()

    def resetOrder(self):
        self.orderTuple = 'no order'
        self.populateTable()

    def Back(self):
        if self.usertype == 'Visitor':
            self.a = VisitorFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'User':
            self.a = UserFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Admin-Only':
            self.a = AdminFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Admin-Visitor':
            self.a = AdminVisFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Staff-Only':
            self.a = StaffFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Staff-Visitor':
            self.a = StaffVisFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Manager-Only':
            self.a = ManagerFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Manager-Visitor':
            self.a = ManagerVisFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Master':
            self.a = Placeholder(self.email, self.usertype, self.username)
        self.a.show()
        self.close()

    def initTable(self):
        self.sqlHeaderList = ['Select','Date','Event Count','Staff Count','Total Visits','Total Revenue ($)']
        self.orderdict = ["asc","asc","asc","asc","asc","asc","asc"]
        self.SQLtable = QtWidgets.QTableWidget()
        self.SQLtable.count = 0
        self.checkBoxes = loadTable(self.SQLtable, 'placeholder data', self.sqlHeaderList, 5)
        self.orderTuple = 'no order'

    def populateTable(self):
        startDate = self.startDateEdit.text()
        endDate = self.endDateEdit.text()
        if startDate == '' or endDate == '':
            msgBox = QMessageBox()
            msgBox.setText("{}".format("You must enter a start and end date"))
            msgBox.setWindowTitle("Notification")
            msgBox.exec_()
            return 'a'
        self.result = PyMySQLQs.GetSiteReport(self.site, startDate, endDate, self.lowEvent.text(), self.highEvent.text(), self.lowStaff.text(), self.highStaff.text(), self.lowVisit.text(), self.highVisit.text(), self.lowRev.text(), self.highRev.text(), self.orderTuple)
        if type(self.result) == str:
            msgBox = QMessageBox()
            msgBox.setText("{}".format(self.result))
            msgBox.setWindowTitle("Notification")
            msgBox.exec_()
        else:
            self.checkBoxes = loadTable(self.SQLtable, self.result, self.sqlHeaderList, 5)

    def headerClicked(self):
        col = self.SQLtable.currentColumn()
        if col != -1:
            if self.orderdict[col] == 'asc':
                self.orderdict[col] = 'desc'
            else:
                self.orderdict[col] = 'asc'
            self.orderTuple = (col, self.orderdict[col])
            self.populateTable()
            self.SQLtable.clearSelection()

#--- 30 ---#
class ViewDailyDetail(QDialog):
    def __init__(self, date, site):
        super(ViewDailyDetail, self).__init__()
        self.site = site
        self.date = date
        self.orderTuple = 'no order'
        self.setModal(True)
        self.setWindowTitle("Atlanta Beltline Database")
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.icon = "buzz.png"
        self.setWindowIcon(QIcon(self.icon))
        self.GUI()
        self.connections()


    def GUI(self):
        self.vbox = QVBoxLayout()
        self.title = QLabel("Daily Detail")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font: bold 20pt;")
        self.vbox.addWidget(self.title)
        self.initTable()
        self.populateTable()
        self.hboxBack = QHBoxLayout()
        self.backButton = QPushButton("Back")
        self.backButton.setStyleSheet(bColor)
        self.hboxBack.addItem(QSpacerItem(175, 20))
        self.hboxBack.addWidget(self.backButton)
        self.hboxBack.addItem(QSpacerItem(175, 20))
        self.info = QLabel("Click a column header to order ascending/descending by that column")
        self.info.setAlignment(Qt.AlignCenter)
        self.vbox.addWidget(self.info)
        self.vbox.addWidget(self.SQLtable)
        self.vbox.addLayout(self.hboxBack)
        self.setLayout(self.vbox)
        self.resize(530,350)

    def connections(self):
        self.backButton.clicked.connect(self.Back)
        self.SQLtable.horizontalHeader().sectionClicked.connect(self.headerClicked)

    def resetOrder(self):
        self.orderTuple = 'no order'
        self.populateTable()

    def Back(self):
        self.close()

    def initTable(self):
        self.sqlHeaderList = ['Event Name','Staff Names','Visits','Revenue ($)']
        self.orderdict = ["asc","asc","asc","asc","asc","asc","asc"]
        self.SQLtable = QtWidgets.QTableWidget()
        self.SQLtable.count = 0
        self.checkBoxes = loadTableNoCheck(self.SQLtable, 'placeholder data', self.sqlHeaderList,4)
        self.orderTuple = 'no order'

    def populateTable(self):
        self.result = PyMySQLQs.GetDailyDetail(self.date, self.site, self.orderTuple)
        if type(self.result) == str:
            msgBox = QMessageBox()
            msgBox.setText("{}".format(self.result))
            msgBox.setWindowTitle("Notification")
            msgBox.exec_()
        else:
            self.checkBoxes = loadTableNoCheck(self.SQLtable, self.result, self.sqlHeaderList, 4)

    def headerClicked(self):
        col = self.SQLtable.currentColumn()
        if col != -1:
            if self.orderdict[col] == 'asc':
                self.orderdict[col] = 'desc'
            else:
                self.orderdict[col] = 'asc'
            self.orderTuple = (col, self.orderdict[col])
            self.populateTable()
            self.SQLtable.clearSelection()

#--- 31 ---#
class ViewSchedule(QDialog):
    def __init__(self, email, usertype, username):
        super(ViewSchedule, self).__init__()
        self.email = email
        self.usertype = usertype
        self.username = username
        self.setModal(True)
        self.setWindowTitle("Atlanta Beltline Database")
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.icon = "buzz.png"
        self.setWindowIcon(QIcon(self.icon))
        self.GUI()
        self.connections()

    def GUI(self):
        self.vbox = QVBoxLayout()
        self.title = QLabel("View Schedule")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font: bold 20pt;")
        self.vbox.addWidget(self.title)
        self.grid = QGridLayout()
        self.grid.addWidget(QLabel("Event Name"),0,0)
        self.eventEdit = QLineEdit("")
        self.grid.addWidget(self.eventEdit,0,1)
        self.grid.addWidget(QLabel("Desciption Keyword"),0,2)
        self.keyword = QLineEdit("")
        self.grid.addWidget(self.keyword,0,3)
        self.grid.addWidget(QLabel("Start Date"),1,0)
        self.startDateEdit = QLineEdit("")
        self.grid.addWidget(self.startDateEdit,1,1)
        self.grid.addWidget(QLabel("End Date"),1,2)
        self.endDateEdit = QLineEdit("")
        self.grid.addWidget(self.endDateEdit,1,3)
        self.vbox.addLayout(self.grid)
        self.filterButton = QPushButton("Filter")
        self.filterButton.setStyleSheet(bColor)
        self.hboxButtons = QHBoxLayout()
        self.viewEventButton = QPushButton("View Event")
        self.viewEventButton.setStyleSheet(bColor)
        self.hboxButtons.addWidget(self.filterButton)
        self.hboxButtons.addItem(QSpacerItem(400,20))
        self.hboxButtons.addWidget(self.viewEventButton)
        self.vbox.addLayout(self.hboxButtons)
        self.initTable()
        self.hboxBack = QHBoxLayout()
        self.backButton = QPushButton("Back")
        self.backButton.setStyleSheet(bColor)
        self.hboxBack.addItem(QSpacerItem(300, 20))
        self.hboxBack.addWidget(self.backButton)
        self.hboxBack.addItem(QSpacerItem(300, 20))
        self.info = QLabel("Click a column header to order ascending/descending by that column")
        self.info.setAlignment(Qt.AlignCenter)
        self.vbox.addWidget(self.info)
        self.vbox.addWidget(self.SQLtable)
        self.vbox.addLayout(self.hboxBack)
        self.setLayout(self.vbox)
        self.resize(800,440)

    def connections(self):
        self.backButton.clicked.connect(self.Back)
        self.SQLtable.horizontalHeader().sectionClicked.connect(self.headerClicked)
        self.filterButton.clicked.connect(self.resetOrder)
        self.viewEventButton.clicked.connect(self.ShowViewEvent)


    def ShowViewEvent(self):
        for i in range(self.SQLtable.rowCount()):
            check = self.checkBoxes[i]
            if check.isChecked():
                event = self.SQLtable.item(i,1).text()
                site = self.SQLtable.item(i,2).text()
                startDate = self.SQLtable.item(i,3).text()
                self.a = ViewEventDetail(self.username, self.email, self.usertype, event, site, startDate)
                self.a.show()

    def resetOrder(self):
        self.orderTuple = 'no order'
        self.populateTable()

    def Back(self):
        if self.usertype == 'Visitor':
            self.a = VisitorFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'User':
            self.a = UserFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Admin-Only':
            self.a = AdminFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Admin-Visitor':
            self.a = AdminVisFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Staff-Only':
            self.a = StaffFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Staff-Visitor':
            self.a = StaffVisFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Manager-Only':
            self.a = ManagerFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Manager-Visitor':
            self.a = ManagerVisFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Master':
            self.a = Placeholder(self.email, self.usertype, self.username)
        self.a.show()
        self.close()

    def initTable(self):
        self.sqlHeaderList = ['Select','Event Name','Site Name','Start Date','End Date','Staff Count']
        self.orderdict = ["asc","asc","asc","asc","asc","asc","asc","asc",'asc']
        self.SQLtable = QtWidgets.QTableWidget()
        self.SQLtable.count = 0
        self.checkBoxes = loadTable(self.SQLtable, 'placeholder data', self.sqlHeaderList, 5)
        self.orderTuple = 'no order'

    def populateTable(self):
        eventName = self.eventEdit.text()
        keyword = self.keyword.text()
        startDate = self.startDateEdit.text()
        endDate = self.endDateEdit.text()
        self.result = PyMySQLQs.StaffSchedule(self.SQLtable, self.username, eventName, keyword, startDate, endDate, self.orderTuple)
        if type(self.result) == str:
            msgBox = QMessageBox()
            msgBox.setText("{}".format(self.result))
            msgBox.setWindowTitle("Notification")
            msgBox.exec_()
        else:
            self.checkBoxes = loadTable(self.SQLtable, self.result, self.sqlHeaderList, 5)

    def headerClicked(self):
        col = self.SQLtable.currentColumn()
        if col != -1:
            if self.orderdict[col] == 'asc':
                self.orderdict[col] = 'desc'
            else:
                self.orderdict[col] = 'asc'
            self.orderTuple = (col, self.orderdict[col])
            self.populateTable()
            self.SQLtable.clearSelection()

#--- 32 AND 34 ---#
class ViewEventDetail(QDialog):
    def __init__(self, username, email, usertype, event, site, startDate):
        super(ViewEventDetail, self).__init__()
        self.site = site
        self.email = email
        self.usertype = usertype
        self.username = username
        self.event = event
        self.startDate = startDate
        self.setModal(True)
        self.setWindowTitle("Atlanta Beltline Database")
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.icon = "buzz.png"
        self.setWindowIcon(QIcon(self.icon))
        self.getEventInfo(site, event, startDate)
        self.GUI()
        self.connections()

    def GUI(self):
        # need to create string of names from list of names passed in
        self.vbox = QVBoxLayout()
        self.title = QLabel("Event Detail")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font: bold 20pt;")
        self.vbox.addWidget(self.title)
        self.hbox1 = QHBoxLayout()
        self.hbox1.addWidget(QLabel("Event"))
        self.eventLabel = QLabel(self.event)
        self.eventLabel.setStyleSheet("font: bold;")
        self.hbox1.addWidget(self.eventLabel)
        self.hbox1.addWidget(QLabel("Site"))
        self.siteLabel = QLabel(self.site)
        self.siteLabel.setStyleSheet("font: bold;")
        self.hbox1.addWidget(self.siteLabel)
        self.vbox.addLayout(self.hbox1)
        self.hbox2 = QHBoxLayout()
        self.hbox2.addWidget(QLabel("Start Date"))
        self.startDateLabel = QLabel(self.startDate)
        self.startDateLabel.setStyleSheet("font: bold;")
        self.hbox2.addWidget(self.startDateLabel)
        self.hbox2.addWidget(QLabel("End Date"))
        self.endDateLabel = QLabel(self.endDateBold)
        self.endDateLabel.setStyleSheet("font: bold;")
        self.hbox2.addWidget(self.endDateLabel)
        self.hbox2.addWidget(QLabel("Duration (Days)"))
        self.duration = QLabel(self.durationLabel)
        self.duration.setStyleSheet("font: bold;")
        self.hbox2.addWidget(self.duration)
        self.vbox.addLayout(self.hbox2)
        self.hbox3 = QHBoxLayout()
        self.hbox3.addWidget(QLabel("Staffs Assigned"))
        self.staffAssigned = QLabel(self.names)
        self.staffAssigned.setStyleSheet("font: bold;")
        self.staffAssigned.setWordWrap(True)
        self.hbox3.addWidget(self.staffAssigned)
        self.hbox3.addWidget(QLabel("Capacity"))
        self.capacity = QLabel(self.capacityLabel)
        self.capacity.setStyleSheet("font: bold;")
        self.hbox3.addWidget(self.capacity)
        self.hbox3.addWidget(QLabel("Price ($)"))
        self.price = QLabel(self.priceLabel)
        self.price.setStyleSheet("font: bold;")
        self.hbox3.addWidget(self.price)
        self.vbox.addLayout(self.hbox3)
        self.hbox4 = QHBoxLayout()
        self.hbox4.addWidget(QLabel("Description"))
        self.description = QLabel(self.descriptionLabel)
        self.description.setStyleSheet("font: bold;")
        self.description.setWordWrap(True)
        self.hbox4.addWidget(self.description)
        self.vbox.addLayout(self.hbox4)
        self.hboxBack = QHBoxLayout()
        self.backButton = QPushButton("Back")
        self.backButton.setStyleSheet(bColor)
        self.hboxBack.addItem(QSpacerItem(250, 20))
        self.hboxBack.addWidget(self.backButton)
        self.hboxBack.addItem(QSpacerItem(250, 20))
        self.hboxVis = QHBoxLayout()
        self.hboxVis.addItem(QSpacerItem(75,20))
        self.hboxVis.addWidget(QLabel("Visit Date"))
        self.dateEdit = QLineEdit("")
        self.hboxVis.addWidget(self.dateEdit)
        self.logVisButton = QPushButton("Log Visit")
        self.logVisButton.setStyleSheet(bColor)
        self.hboxVis.addWidget(self.logVisButton)
        self.hboxVis.addItem(QSpacerItem(75,20))
        if 'Visitor' in self.usertype:
            self.vbox.addLayout(self.hboxVis)
        self.vbox.addLayout(self.hboxBack)
        self.setLayout(self.vbox)
        self.resize(350,400)

    def connections(self):
        self.backButton.clicked.connect(self.Back)
        self.logVisButton.clicked.connect(self.LogVisit)

    def getEventInfo(self, site, event, startDate):
        self.names = PyMySQLQs.getEventStaff(event, site, startDate)
        infoList = PyMySQLQs.getEventInfo(event, site, startDate)
        self.endDateBold = infoList[0].strftime('%Y-%m-%d')
        self.datetime_objectStart = datetime.strptime(self.startDate, '%Y-%m-%d')
        self.datetime_objectEnd = datetime.strptime(self.endDateBold, '%Y-%m-%d')
        days = self.datetime_objectEnd - self.datetime_objectStart
        self.durationLabel = str(days.days + 1)
        self.priceLabel = str(infoList[1])
        self.capacityLabel = str(infoList[2])
        self.descriptionLabel = infoList[3]

    def LogVisit(self):
        date = self.dateEdit.text()
        self.result = PyMySQLQs.logVisitEvent(self.username, self.event, self.startDate, self.site, date, self.datetime_objectStart, self.datetime_objectEnd)
        if type(self.result) == str:
            msgBox = QMessageBox()
            msgBox.setText("Log Visit Failed. {}".format(self.result))
            msgBox.setWindowTitle("Notification")
            msgBox.exec_()
        else:
            msgBox = QMessageBox()
            msgBox.setText("Log Visit Succesful")
            msgBox.setWindowTitle("Notification")
            msgBox.exec_()

    def Back(self):
        self.close()

#--- 33 ---#
class ExploreEvent(QDialog):
    def __init__(self, email, usertype, username):
        super(ExploreEvent, self).__init__()
        self.email = email
        self.usertype = usertype
        self.username = username
        self.setModal(True)
        self.setWindowTitle("Atlanta Beltline Database")
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.icon = "buzz.png"
        self.setWindowIcon(QIcon(self.icon))
        self.GUI()
        self.connections()

    def GUI(self):
        self.vbox = QVBoxLayout()
        self.title = QLabel("Explore Event")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font: bold 20pt;")
        self.vbox.addWidget(self.title)
        self.grid = QGridLayout()
        self.grid.addWidget(QLabel("Name"),0,0)
        self.eventName = QLineEdit("")
        self.grid.addWidget(self.eventName,0,1)
        self.grid.addWidget(QLabel("Description Keyword"),0,2)
        self.keyword = QLineEdit("")
        self.grid.addWidget(self.keyword,0,3)
        self.grid.addWidget(QLabel("Site Name"),1,0)
        self.siteDrop = QComboBox()
        self.siteDrop.addItem("-ALL-")
        self.grid.addWidget(self.siteDrop,1,1)
        self.comboItems()
        self.grid.addWidget(QLabel("Start Date"),2,0)
        self.startDateEdit = QLineEdit("")
        self.grid.addWidget(self.startDateEdit,2,1)
        self.endDateEdit = QLineEdit("")
        self.grid.addWidget(QLabel("End Date"),2,2)
        self.grid.addWidget(self.endDateEdit,2,3)
        self.vbox.addLayout(self.grid)
        self.hboxHor = QHBoxLayout()
        self.hbox4 =  QHBoxLayout()
        self.hbox4.addWidget(QLabel("Total Visits Range"))
        self.lowVis = QLineEdit("")
        self.highVis = QLineEdit("")
        self.hbox4.addWidget(self.lowVis)
        self.hbox4.addWidget(QLabel("--"))
        self.hbox4.addWidget(self.highVis)
        self.lowPrice = QLineEdit("")
        self.highPrice = QLineEdit("")
        self.hbox4r = QHBoxLayout()
        self.hbox4r.addWidget(QLabel("Event Count Range"))
        self.hbox4r.addWidget(self.lowPrice)
        self.hbox4r.addWidget(QLabel("--"))
        self.hbox4r.addWidget(self.highPrice)
        self.hboxHor.addLayout(self.hbox4)
        self.hboxHor.addLayout(self.hbox4r)
        self.vbox.addLayout(self.hboxHor)
        self.grid5 = QGridLayout()
        self.includeVis = QCheckBox("Include Visited")
        self.includeSoldOut = QCheckBox("Include Sold Out Events")
        self.grid5.addWidget(QLabel("            "),0,0)
        self.grid5.addWidget(self.includeVis,0,1)
        self.grid5.addWidget(QLabel("            "),0,2)
        self.grid5.addWidget(self.includeSoldOut,0,3)
        self.grid5.addWidget(QLabel("            "),0,4)
        self.vbox.addLayout(self.grid5)
        self.filterButton = QPushButton("Filter")
        self.filterButton.setStyleSheet(bColor)
        self.hboxButtons = QHBoxLayout()
        self.eventDetailButton = QPushButton("Event Detail")
        self.eventDetailButton.setStyleSheet(bColor)
        self.hboxButtons.addWidget(self.filterButton)
        self.hboxButtons.addItem(QSpacerItem(500,20))
        self.hboxButtons.addWidget(self.eventDetailButton)
        self.vbox.addLayout(self.hboxButtons)
        self.initTable()
        self.hboxBack = QHBoxLayout()
        self.backButton = QPushButton("Back")
        self.backButton.setStyleSheet(bColor)
        self.hboxBack.addItem(QSpacerItem(350, 20))
        self.hboxBack.addWidget(self.backButton)
        self.hboxBack.addItem(QSpacerItem(350, 20))
        self.info = QLabel("Click a column header to order ascending/descending by that column")
        self.info.setAlignment(Qt.AlignCenter)
        self.vbox.addWidget(self.info)
        self.vbox.addWidget(self.SQLtable)
        self.vbox.addLayout(self.hboxBack)
        self.setLayout(self.vbox)
        self.resize(905,600)

    def connections(self):
        self.backButton.clicked.connect(self.Back)
        self.SQLtable.horizontalHeader().sectionClicked.connect(self.headerClicked)
        self.filterButton.clicked.connect(self.resetOrder)
        self.eventDetailButton.clicked.connect(self.ShowEventDetail)


    def ShowEventDetail(self):
        for i in range(self.SQLtable.rowCount()):
            check = self.checkBoxes[i]
            if check.isChecked():
                site = self.SQLtable.item(i,2).text()
                startdate = self.startDateEdit.text()
                self.a = ViewEventDetail(self.username, self.email, self.usertype, site, startDate)
                self.a.show()

    def resetOrder(self):
        self.orderTuple = 'no order'
        self.populateTable()

    def Back(self):
        if self.usertype == 'Visitor':
            self.a = VisitorFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'User':
            self.a = UserFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Admin-Only':
            self.a = AdminFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Admin-Visitor':
            self.a = AdminVisFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Staff-Only':
            self.a = StaffFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Staff-Vistor':
            self.a = StaffVisFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Manager-Only':
            self.a = ManagerFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Manager-Visitor':
            self.a = ManagerVisFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Master':
            self.a = Placeholder(self.email, self.usertype, self.username)
        self.a.show()
        self.close()

    def initTable(self):
        self.sqlHeaderList = ['Select','Event Name','Site Name','Ticket Price','Tickets Remaining','Total Visits','My Visits']
        self.orderdict = ["asc","asc","asc","asc","asc","asc","asc"]
        self.SQLtable = QtWidgets.QTableWidget()
        self.SQLtable.count = 0
        self.checkBoxes = loadTable(self.SQLtable, 'placeholder data', self.sqlHeaderList, 6)
        self.orderTuple = 'no order'

    def populateTable(self):
        name = self.eventName.text()
        keyword = self.keyword.text()
        siteName = self.siteDrop.currentText()
        visLow = self.lowVis.text()
        visHigh = self.highVis.text()
        priceLow = self.lowPrice.text()
        priceHigh = self.highPrice.text()
        startDate = self.startDateEdit.text()
        endDate = self.endDateEdit.text()
        includeVis = self.includeVis.isChecked()
        includeSoldOut = self.includeSoldOut.isChecked()
        self.result = PyMySQLQs.VisitorExploreEvent(self.SQLtable, name, keyword, siteName, startDate, endDate, visHigh, visLow, priceHigh, priceLow, includeVis, includeSoldOut, self.orderTuple)
        print(self.result)
        if type(self.result) == str:
            msgBox = QMessageBox()
            msgBox.setText("{}".format(self.result))
            msgBox.setWindowTitle("Notification")
            msgBox.exec_()
        else:
            self.checkBoxes = loadTable(self.SQLtable, self.result, self.sqlHeaderList, 6)

    def headerClicked(self):
        col = self.SQLtable.currentColumn()
        if col != -1:
            if self.orderdict[col] == 'asc':
                self.orderdict[col] = 'desc'
            else:
                self.orderdict[col] = 'asc'
            self.orderTuple = (col, self.orderdict[col])
            self.populateTable()
            self.SQLtable.clearSelection()

    def comboItems(self):
        self.siteList = PyMySQLQs.SiteComboBox()
        for aDict in self.siteList:
            for key in aDict:
                self.siteDrop.addItem(aDict[key])


#--- 35 ---#
class ExploreSite(QDialog):
    def __init__(self, email, usertype, username):
        super(ExploreSite, self).__init__()
        self.email = email
        self.usertype = usertype
        self.username = username
        self.setModal(True)
        self.setWindowTitle("Atlanta Beltline Database")
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.icon = "buzz.png"
        self.setWindowIcon(QIcon(self.icon))
        self.GUI()
        self.connections()

    def GUI(self):
        self.vbox = QVBoxLayout()
        self.title = QLabel("Explore Site")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font: bold 20pt;")
        self.vbox.addWidget(self.title)
        self.grid = QGridLayout()
        self.grid.addWidget(QLabel("Site Name"),0,0)
        self.siteDrop = QComboBox()
        self.siteDrop.addItem("-ALL-")
        self.grid.addWidget(self.siteDrop,0,1)
        self.comboItems()
        self.grid.addWidget(QLabel("Open Everyday"),0,2)
        self.openDrop = QComboBox()
        self.openDrop.addItems(["-ALL-","Yes","No"])
        self.grid.addWidget(self.openDrop,0,3)
        self.grid.addWidget(QLabel("Start Date"),1,0)
        self.startDateEdit = QLineEdit("")
        self.grid.addWidget(self.startDateEdit,1,1)
        self.endDateEdit = QLineEdit("")
        self.grid.addWidget(QLabel("End Date"),1,2)
        self.grid.addWidget(self.endDateEdit,1,3)
        self.vbox.addLayout(self.grid)
        self.hbox4 =  QHBoxLayout()
        self.hbox4.addWidget(QLabel("Total Visits Range"))
        self.lowVis = QLineEdit("")
        self.highVis = QLineEdit("")
        self.hbox4.addWidget(self.lowVis)
        self.hbox4.addWidget(QLabel("--"))
        self.hbox4.addWidget(self.highVis)
        self.lowPrice = QLineEdit("")
        self.highPrice = QLineEdit("")
        self.hbox4.addItem(QSpacerItem(75,20))
        self.hbox4.addWidget(QLabel("Event Count Range"))
        self.hbox4.addWidget(self.lowPrice)
        self.hbox4.addWidget(QLabel("--"))
        self.hbox4.addWidget(self.highPrice)
        self.vbox.addLayout(self.hbox4)
        self.hbox5 = QHBoxLayout()
        self.hbox5.addItem(QSpacerItem(260,20))
        self.includeVis = QCheckBox()
        self.hbox5.addWidget(self.includeVis)
        self.hbox5.addWidget(QLabel("Include Visited"))
        self.hbox5.addItem(QSpacerItem(260,20))
        self.vbox.addLayout(self.hbox5)
        self.filterButton = QPushButton("Filter")
        self.filterButton.setStyleSheet(bColor)
        self.hboxButtons = QHBoxLayout()
        self.siteDetailButton = QPushButton("Site Detail")
        self.siteDetailButton.setStyleSheet(bColor)
        self.transitDetailButton = QPushButton("Transit Detail")
        self.transitDetailButton.setStyleSheet(bColor)
        self.hboxButtons.addWidget(self.filterButton)
        self.hboxButtons.addItem(QSpacerItem(200,20))
        self.hboxButtons.addWidget(self.siteDetailButton)
        self.hboxButtons.addWidget(self.transitDetailButton)
        self.vbox.addLayout(self.hboxButtons)
        self.initTable()
        self.hboxBack = QHBoxLayout()
        self.backButton = QPushButton("Back")
        self.backButton.setStyleSheet(bColor)
        self.hboxBack.addItem(QSpacerItem(250, 20))
        self.hboxBack.addWidget(self.backButton)
        self.hboxBack.addItem(QSpacerItem(250, 20))
        self.info = QLabel("Click a column header to order ascending/descending by that column")
        self.info.setAlignment(Qt.AlignCenter)
        self.vbox.addWidget(self.info)
        self.vbox.addWidget(self.SQLtable)
        self.vbox.addLayout(self.hboxBack)
        self.setLayout(self.vbox)
        self.resize(652,550)

    def connections(self):
        self.backButton.clicked.connect(self.Back)
        self.SQLtable.horizontalHeader().sectionClicked.connect(self.headerClicked)
        self.filterButton.clicked.connect(self.resetOrder)
        self.siteDetailButton.clicked.connect(self.ShowSiteDetail)
        self.transitDetailButton.clicked.connect(self.ShowTransitDetail)

    def ShowSiteDetail(self):
        for i in range(self.SQLtable.rowCount()):
            check = self.checkBoxes[i]
            if check.isChecked():
                site = self.SQLtable.item(i,1).text()
                self.SQLtable.clearSelection()
                self.a = ViewSiteDetail(self.username,'','',site)
                self.a.show()

    def ShowTransitDetail(self):
        self.a = ViewTransitDetail('','','','')
        self.a.show()

    def resetOrder(self):
        self.orderTuple = 'no order'
        self.populateTable()

    def Back(self):
        if self.usertype == 'Visitor':
            self.a = VisitorFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'User':
            self.a = UserFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Admin-Only':
            self.a = AdminFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Admin-Visitor':
            self.a = AdminVisFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Staff-Only':
            self.a = StaffFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Staff-Visitor':
            self.a = StaffVisFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Manager-Only':
            self.a = ManagerFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Manager-Visitor':
            self.a = ManagerVisFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Master':
            self.a = Placeholder(self.email, self.usertype, self.username)
        self.a.show()
        self.close()

    def initTable(self):
        self.sqlHeaderList = ['Select','Site Name','Event Count','Total Visits','My Visits']
        self.orderdict = ["asc","asc","asc","asc","asc","asc","asc"]
        self.SQLtable = QtWidgets.QTableWidget()
        self.SQLtable.count = 0
        self.checkBoxes = loadTable(self.SQLtable, 'placeholder data', self.sqlHeaderList, 4)
        self.orderTuple = 'no order'

    def populateTable(self):
        startDate = self.startDateEdit.text()
        endDate = self.endDateEdit.text()
        self.result = PyMySQLQs.ToughScene()
        if type(self.result) == str:
            msgBox = QMessageBox()
            msgBox.setText("{}".format(PyMySQLQs.registerusercheck(fname, lname, username, password, confirmPass, emaillist)))
            msgBox.setWindowTitle("Notification")
            msgBox.exec_()
        else:
            self.checkBoxes = loadTable(self.SQLtable, self.result, self.sqlHeaderList, 4)

    def headerClicked(self):
        col = self.SQLtable.currentColumn()
        if col != -1:
            if self.orderdict[col] == 'asc':
                self.orderdict[col] = 'desc'
            else:
                self.orderdict[col] = 'asc'
            self.orderTuple = (col, self.orderdict[col])
            self.populateTable()
            self.SQLtable.clearSelection()

    def comboItems(self):
        self.siteList = PyMySQLQs.SiteComboBox()
        for aDict in self.siteList:
            for key in aDict:
                self.siteDrop.addItem(aDict[key])

#--- 36 ---#
class ViewTransitDetail(QDialog):
    def __init__(self, email, usertype, username, site):
        super(ViewTransitDetail, self).__init__()
        self.email = email
        self.usertype = usertype
        self.username = username
        self.setModal(True)
        self.setWindowTitle("Atlanta Beltline Database")
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.icon = "buzz.png"
        self.setWindowIcon(QIcon(self.icon))
        self.GUI()
        self.connections()

    def GUI(self):
        self.vbox = QVBoxLayout()
        self.title = QLabel("Transit Detail")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font: bold 20pt;")
        self.vbox.addWidget(self.title)
        self.hbox1 = QHBoxLayout()
        self.hbox1.addWidget(QLabel("Site Name"))
        self.site = QLabel("aa")
        self.site.setStyleSheet("font: bold;")
        self.hbox1.addWidget(self.site)
        self.hbox1.addWidget(QLabel("Transport Type"))
        self.transTypeDrop = QComboBox()
        self.transTypeDrop.addItems(["-ALL-",'Bus', 'MARTA', 'Bike'])
        self.hbox1.addWidget(self.transTypeDrop)
        self.vbox.addLayout(self.hbox1)
        self.initTable()
        self.hbox3 = QHBoxLayout()
        self.transitDateLabel = QLabel("Transit Date")
        self.transiteDateEdit = QLineEdit("")
        self.logTransit = QPushButton("Log Transit")
        self.logTransit.setStyleSheet(bColor)
        self.backButton = QPushButton("Back")
        self.backButton.setStyleSheet(bColor)
        self.hbox3.addWidget(self.backButton)
        self.hbox3.addItem(QSpacerItem(100,20))
        self.hbox3.addWidget(self.transitDateLabel)
        self.hbox3.addWidget(self.transiteDateEdit)
        self.hbox3.addItem(QSpacerItem(100,20))
        self.hbox3.addWidget(self.logTransit)
        self.vbox.addWidget(QLabel("Click a column header to order ascending/descending by that column"))
        self.vbox.addWidget(self.SQLtable)
        self.vbox.addLayout(self.hbox3)
        self.setLayout(self.vbox)
        self.resize(655,440)

    def connections(self):
        self.backButton.clicked.connect(self.Back)
        self.SQLtable.horizontalHeader().sectionClicked.connect(self.headerClicked)
        self.logTransit.clicked.connect(self.LogATransit)

    def LogATransit(self):
        date = self.transiteDateEdit.text()
        for i in range(self.SQLtable.rowCount()):
            check = self.checkBoxes[i]
            if check.isChecked():
                route = self.SQLtable.item(i,1).text()
                transportType = self.SQLtable.item(i,2).text()
                price = self.SQLtable.item(i,3).text()
                numConnected = self.SQLtable.item(i,4).text()
                self.SQLtable.clearSelection()
                print(self.email, route, transportType, price, numConnected, date)
                self.result = PyMySQLQs.logTransit(self.username, transportType, route, date)
                if type(self.result) == str:
                    msgBox = QMessageBox()
                    msgBox.setText("Log Transit Failed. {}".format(self.result))
                    msgBox.setWindowTitle("Notification")
                    msgBox.exec_()
                else:
                    msgBox = QMessageBox()
                    msgBox.setText("Log Transit Succesful")
                    msgBox.setWindowTitle("Notification")
                    msgBox.exec_()

    def resetOrder(self):
        self.orderTuple = 'no order'
        self.populateTable()

    def Back(self):
        self.close()

    def initTable(self):
        self.sqlHeaderList = ['Select','Route','Transport Type','Price','# Connected Sites']
        self.orderdict = ["asc","asc","asc","asc","asc","asc","asc"]
        self.SQLtable = QtWidgets.QTableWidget()
        self.SQLtable.count = 0
        self.checkBoxes = loadTable(self.SQLtable, 'placeholder data', self.sqlHeaderList, 4)
        self.orderTuple = 'no order'

    def populateTable(self):
        startDate = self.startDateEdit.text()
        endDate = self.endDateEdit.text()
        #UPDATE WHEN PYMYSQLQs HAS QUERIES PUT IN
        #self.result = PyMySQLQs.ManageSiteTable(status, userType, username, self.orderTuple)
        if type(self.result) == str:
            msgBox = QMessageBox()
            msgBox.setText("{}".format(PyMySQLQs.registerusercheck(fname, lname, username, password, confirmPass, emaillist)))
            msgBox.setWindowTitle("Notification")
            msgBox.exec_()
        else:
            self.checkBoxes = loadTable(self.SQLtable, self.result, self.sqlHeaderList, 4)

    def headerClicked(self):
        col = self.SQLtable.currentColumn()
        if col != -1:
            if self.orderdict[col] == 'asc':
                self.orderdict[col] = 'desc'
            else:
                self.orderdict[col] = 'asc'
            self.orderTuple = (col, self.orderdict[col])
            self.populateTable()
            self.SQLtable.clearSelection()

#--- 37 ---#
class ViewSiteDetail(QDialog):
    def __init__(self, username, email, usertype, site):
        super(ViewSiteDetail, self).__init__()
        self.site = site
        self.email = email
        self.usertype = usertype
        self.username = username
        self.setModal(True)
        self.setWindowTitle("Atlanta Beltline Database")
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.icon = "buzz.png"
        self.setWindowIcon(QIcon(self.icon))
        self.getInfo()
        self.GUI()
        self.connections()

    def getInfo(self):
        resultDict = PyMySQLQs.getSiteInfo(self.site)
        print(resultDict)
        self.address = resultDict['Address']
        self.openEveryday = resultDict['OpenEveryday']

    def GUI(self):
        # need to create string of names from list of names passed in
        self.vbox = QVBoxLayout()
        self.title = QLabel("Site Detail")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font: bold 20pt;")
        self.vbox.addWidget(self.title)
        self.hbox1 = QHBoxLayout()
        self.hbox1.addWidget(QLabel("Site"))
        self.siteLabel = QLabel(self.site)
        self.siteLabel.setStyleSheet("font: bold;")
        self.hbox1.addWidget(self.siteLabel)
        self.hbox1.addWidget(QLabel("Open Everyday"))
        self.eventLabel = QLabel(self.openEveryday)
        self.eventLabel.setStyleSheet("font: bold;")
        self.hbox1.addWidget(self.eventLabel)
        self.vbox.addLayout(self.hbox1)
        self.hbox2 = QHBoxLayout()
        self.hbox2.addWidget(QLabel("Address"))
        self.addressLabel = QLabel(self.address)
        self.addressLabel.setStyleSheet("font: bold;")
        self.hbox2.addWidget(self.addressLabel)
        self.vbox.addLayout(self.hbox2)
        self.hbox3 = QHBoxLayout()
        self.hbox3.addItem(QSpacerItem(100,20))
        self.hbox3.addWidget(QLabel("Visit Date"))
        self.dateEdit = QLineEdit("")
        self.hbox3.addWidget(self.dateEdit)
        self.logVisButton = QPushButton("Log Visit")
        self.logVisButton.setStyleSheet(bColor)
        self.hbox3.addWidget(self.logVisButton)
        self.hbox3.addItem(QSpacerItem(100,20))
        self.vbox.addLayout(self.hbox3)
        self.hboxBack = QHBoxLayout()
        self.backButton = QPushButton("Back")
        self.backButton.setStyleSheet(bColor)
        self.hboxBack.addItem(QSpacerItem(175, 20))
        self.hboxBack.addWidget(self.backButton)
        self.hboxBack.addItem(QSpacerItem(175, 20))
        self.vbox.addLayout(self.hboxBack)
        self.setLayout(self.vbox)
        self.resize(400,200)

    def connections(self):
        self.backButton.clicked.connect(self.Back)
        self.logVisButton.clicked.connect(self.LogVisit)

    def LogVisit(self):
        visitDate = self.dateEdit.text()
        a = PyMySQLQs.logSiteVisit1(self.username, self.site, visitDate)
        if type(a) == str:
            msgBox = QMessageBox()
            msgBox.setText("{}".format(a))
            msgBox.setWindowTitle("Notification")
            msgBox.exec_()
        else:
            msgBox = QMessageBox()
            msgBox.setText("Log Visit Succesful")
            msgBox.setWindowTitle("Notification")
            msgBox.exec_()

    def Back(self):
        self.close()

#--- 38 ---#
class ViewVisitHistory(QDialog):
    def __init__(self, email, usertype, username):
        super(ViewVisitHistory, self).__init__()
        self.email = email
        self.usertype = usertype
        self.username = username
        self.setModal(True)
        self.setWindowTitle("Atlanta Beltline Database")
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.icon = "buzz.png"
        self.setWindowIcon(QIcon(self.icon))
        self.GUI()
        self.connections()

    def GUI(self):
        self.vbox = QVBoxLayout()
        self.title = QLabel("Visit History")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font: bold 20pt;")
        self.vbox.addWidget(self.title)
        self.grid = QGridLayout()
        self.grid.addWidget(QLabel("Event"),0,0)
        self.eventEdit = QLineEdit("")
        self.grid.addWidget(self.eventEdit,0,1)
        self.grid.addWidget(QLabel("Site"),0,2)
        self.siteDrop = QComboBox()
        self.siteDrop.addItem("-ALL-")
        self.grid.addWidget(self.siteDrop,0,3)
        self.comboItems()
        self.startDateLabel = QLabel("Start Date")
        self.startDateEdit = QLineEdit("")
        self.endDateLabel = QLabel("End Date")
        self.endDateEdit = QLineEdit("")
        self.grid.addWidget(self.startDateLabel,1,0)
        self.grid.addWidget(self.startDateEdit,1,1)
        self.grid.addWidget(self.endDateLabel,1,2)
        self.grid.addWidget(self.endDateEdit,1,3)
        self.vbox.addLayout(self.grid)
        self.hbox4 = QHBoxLayout()
        self.hbox4.addItem(QSpacerItem(205,20))
        self.filterButton = QPushButton("Filter")
        self.filterButton.setStyleSheet(bColor)
        self.hbox4.addWidget(self.filterButton)
        self.hbox4.addItem(QSpacerItem(205,20))
        self.vbox.addLayout(self.hbox4)
        self.initTable()
        self.hbox3 = QHBoxLayout()
        self.hbox3.addItem(QSpacerItem(205,20))
        self.backButton = QPushButton("Back")
        self.backButton.setStyleSheet(bColor)
        self.hbox3.addWidget(self.backButton)
        self.hbox3.addItem(QSpacerItem(205,20))
        self.info = QLabel("Click a column header to order ascending/descending by that column")
        self.info.setAlignment(Qt.AlignCenter)
        self.vbox.addWidget(self.info)
        self.vbox.addWidget(self.SQLtable)
        self.vbox.addLayout(self.hbox3)
        self.setLayout(self.vbox)
        self.resize(440,440)

    def connections(self):
        self.backButton.clicked.connect(self.Back)
        self.filterButton.clicked.connect(self.populateTable)
        self.SQLtable.horizontalHeader().sectionClicked.connect(self.headerClicked)

    def resetOrder(self):
        self.orderTuple = 'no order'
        self.populateTable()

    def Back(self):
        if self.usertype == 'Visitor':
            self.a = VisitorFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'User':
            self.a = UserFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Admin-Only':
            self.a = AdminFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Admin-Visitor':
            self.a = AdminVisFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Staff-Only':
            self.a = StaffFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Staff-Visitor':
            self.a = StaffVisFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Manager-Only':
            self.a = ManagerFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Manager-Visitor':
            self.a = ManagerVisFunctionality(self.email, self.usertype, self.username)
        elif self.usertype == 'Master':
            self.a = Placeholder(self.email, self.usertype, self.username)
        self.a.show()
        self.close()

    def initTable(self):
        self.sqlHeaderList = ['Date','Event','Site','Price']
        self.orderdict = ["asc","asc","asc","asc","asc","asc","asc"]
        self.SQLtable = QtWidgets.QTableWidget()
        self.SQLtable.count = 0
        self.checkBoxes = loadTableNoCheck(self.SQLtable, 'placeholder data', self.sqlHeaderList, 4)
        self.orderTuple = 'no order'

    def populateTable(self):
        event = self.eventEdit.text()
        site = self.siteDrop.currentText()
        startDate = self.startDateEdit.text()
        endDate = self.endDateEdit.text()
        self.result = PyMySQLQs.GetVisitHistory(event, site, startDate, endDate, self.orderTuple)
        if type(self.result) == str:
            msgBox = QMessageBox()
            msgBox.setText("{}".format(self.result))
            msgBox.setWindowTitle("Notification")
            msgBox.exec_()
        else:
            self.checkBoxes = loadTableNoCheck(self.SQLtable, self.result, self.sqlHeaderList, 4)


    def headerClicked(self):
        col = self.SQLtable.currentColumn()
        if col != -1:
            if self.orderdict[col] == 'asc':
                self.orderdict[col] = 'desc'
            else:
                self.orderdict[col] = 'asc'
            self.orderTuple = (col, self.orderdict[col])
            self.populateTable()
            self.SQLtable.clearSelection()

    def comboItems(self):
        self.siteList = PyMySQLQs.SiteComboBox()
        for aDict in self.siteList:
            for key in aDict:
                self.siteDrop.addItem(aDict[key])



if __name__=='__main__':
    app = QApplication(sys.argv)
    login = DbLoginDialog()
    sys.exit(login.exec())
