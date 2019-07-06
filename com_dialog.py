# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './com_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Com_Dialog(object):
    def setupUi(self, Com_Dialog):
        Com_Dialog.setObjectName("Com_Dialog")
        Com_Dialog.resize(425, 306)
        font = QtGui.QFont()
        font.setFamily("나눔스퀘어")
        font.setPointSize(11)
        Com_Dialog.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../../../Downloads/st_mark_icons/st_mark_iTO_1.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Com_Dialog.setWindowIcon(icon)
        self.gridLayout = QtWidgets.QGridLayout(Com_Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.c_pushButton_select = QtWidgets.QPushButton(Com_Dialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.c_pushButton_select.setFont(font)
        self.c_pushButton_select.setAutoDefault(False)
        self.c_pushButton_select.setObjectName("c_pushButton_select")
        self.gridLayout.addWidget(self.c_pushButton_select, 4, 2, 1, 1)
        self.c_tableWidget = QtWidgets.QTableWidget(Com_Dialog)
        self.c_tableWidget.setShowGrid(True)
        self.c_tableWidget.setGridStyle(QtCore.Qt.SolidLine)
        self.c_tableWidget.setCornerButtonEnabled(True)
        self.c_tableWidget.setObjectName("c_tableWidget")
        self.c_tableWidget.setColumnCount(1)
        self.c_tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("나눔스퀘어 Bold")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.c_tableWidget.setHorizontalHeaderItem(0, item)
        self.c_tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.c_tableWidget.verticalHeader().setVisible(True)
        self.gridLayout.addWidget(self.c_tableWidget, 3, 0, 1, 3)
        self.c_lineEdit_search = QtWidgets.QLineEdit(Com_Dialog)
        self.c_lineEdit_search.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.c_lineEdit_search.setObjectName("c_lineEdit_search")
        self.gridLayout.addWidget(self.c_lineEdit_search, 2, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(105, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 1)
        self.c_pushButton_search = QtWidgets.QPushButton(Com_Dialog)
        self.c_pushButton_search.setStyleSheet("font: 10pt \"나눔스퀘어\";\n"
"")
        self.c_pushButton_search.setObjectName("c_pushButton_search")
        self.gridLayout.addWidget(self.c_pushButton_search, 2, 2, 1, 1)
        self.label = QtWidgets.QLabel(Com_Dialog)
        font = QtGui.QFont()
        font.setFamily("나눔고딕")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 3)
        self.frame_2 = QtWidgets.QFrame(Com_Dialog)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.gridLayout.addWidget(self.frame_2, 1, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 6, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 1, 0, 1, 1)

        self.retranslateUi(Com_Dialog)
        QtCore.QMetaObject.connectSlotsByName(Com_Dialog)

    def retranslateUi(self, Com_Dialog):
        _translate = QtCore.QCoreApplication.translate
        Com_Dialog.setWindowTitle(_translate("Com_Dialog", "회사 검색"))
        self.c_pushButton_select.setText(_translate("Com_Dialog", "선 택"))
        self.c_tableWidget.setSortingEnabled(True)
        item = self.c_tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Com_Dialog", "회사명"))
        self.c_pushButton_search.setText(_translate("Com_Dialog", "검 색"))
        self.label.setText(_translate("Com_Dialog", "<html><head/><body><p align=\"center\"><span style=\" font-size:11pt; font-weight:600;\">회사 검색</span></p></body></html>"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Com_Dialog = QtWidgets.QDialog()
    ui = Ui_Com_Dialog()
    ui.setupUi(Com_Dialog)
    Com_Dialog.show()
    sys.exit(app.exec_())

