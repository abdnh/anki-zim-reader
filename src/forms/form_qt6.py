# Form implementation generated from reading ui file 'designer\form.ui'
#
# Created by: PyQt6 UI code generator 6.3.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(474, 330)
        Dialog.setWindowTitle("")
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.icon = QtWidgets.QLabel(Dialog)
        self.icon.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.icon.setObjectName("icon")
        self.verticalLayout.addWidget(self.icon)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label)
        self.wordFieldComboBox = QtWidgets.QComboBox(Dialog)
        self.wordFieldComboBox.setObjectName("wordFieldComboBox")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.ItemRole.FieldRole, self.wordFieldComboBox)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_2)
        self.definitionFieldComboBox = QtWidgets.QComboBox(Dialog)
        self.definitionFieldComboBox.setObjectName("definitionFieldComboBox")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.ItemRole.FieldRole, self.definitionFieldComboBox)
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_3)
        self.exampleFieldComboBox = QtWidgets.QComboBox(Dialog)
        self.exampleFieldComboBox.setObjectName("exampleFieldComboBox")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.ItemRole.FieldRole, self.exampleFieldComboBox)
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_4)
        self.genderFieldComboBox = QtWidgets.QComboBox(Dialog)
        self.genderFieldComboBox.setObjectName("genderFieldComboBox")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.ItemRole.FieldRole, self.genderFieldComboBox)
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(8, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_5)
        self.POSFieldComboBox = QtWidgets.QComboBox(Dialog)
        self.POSFieldComboBox.setObjectName("POSFieldComboBox")
        self.formLayout.setWidget(8, QtWidgets.QFormLayout.ItemRole.FieldRole, self.POSFieldComboBox)
        self.addButton = QtWidgets.QPushButton(Dialog)
        self.addButton.setObjectName("addButton")
        self.formLayout.setWidget(10, QtWidgets.QFormLayout.ItemRole.FieldRole, self.addButton)
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setObjectName("label_6")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_6)
        self.dictionaryComboBox = QtWidgets.QComboBox(Dialog)
        self.dictionaryComboBox.setObjectName("dictionaryComboBox")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.ItemRole.FieldRole, self.dictionaryComboBox)
        self.label_7 = QtWidgets.QLabel(Dialog)
        self.label_7.setObjectName("label_7")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_7)
        self.providerComboBox = QtWidgets.QComboBox(Dialog)
        self.providerComboBox.setObjectName("providerComboBox")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.providerComboBox)
        self.label_8 = QtWidgets.QLabel(Dialog)
        self.label_8.setObjectName("label_8")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_8)
        self.parserComboBox = QtWidgets.QComboBox(Dialog)
        self.parserComboBox.setObjectName("parserComboBox")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.ItemRole.FieldRole, self.parserComboBox)
        self.inflectionFieldComboBox = QtWidgets.QComboBox(Dialog)
        self.inflectionFieldComboBox.setObjectName("inflectionFieldComboBox")
        self.formLayout.setWidget(9, QtWidgets.QFormLayout.ItemRole.FieldRole, self.inflectionFieldComboBox)
        self.label_9 = QtWidgets.QLabel(Dialog)
        self.label_9.setObjectName("label_9")
        self.formLayout.setWidget(9, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_9)
        self.verticalLayout.addLayout(self.formLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.wordFieldComboBox, self.definitionFieldComboBox)
        Dialog.setTabOrder(self.definitionFieldComboBox, self.exampleFieldComboBox)
        Dialog.setTabOrder(self.exampleFieldComboBox, self.addButton)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        self.icon.setText(_translate("Dialog", "TextLabel"))
        self.label.setText(_translate("Dialog", "Word"))
        self.label_2.setText(_translate("Dialog", "Definition"))
        self.label_3.setText(_translate("Dialog", "Example"))
        self.label_4.setText(_translate("Dialog", "Gender"))
        self.label_5.setText(_translate("Dialog", "Part of Speech"))
        self.addButton.setText(_translate("Dialog", "Add"))
        self.label_6.setText(_translate("Dialog", "Dictionary"))
        self.label_7.setText(_translate("Dialog", "Source"))
        self.label_8.setText(_translate("Dialog", "Parser"))
        self.label_9.setText(_translate("Dialog", "Inflection"))
