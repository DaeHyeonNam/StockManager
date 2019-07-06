# -*- coding: utf-8 -*-

import sys,os,main_dialog, product_dialog, receive_dialog, com_dialog

import csv ,datetime
import operator 

import PyQt5

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets,Qt
from PyQt5.QtGui import QIntValidator, QIcon


iconPath = "C:/Stock Manager/st_mark_iTO_2.ico"
directory = "C:/Stock Manager"
comDirectory = "C:/Stock Manager/company Data"
stockDataFilePath = "C:/Stock Manager/stockData.csv"
comDataFilePath = "C:/Stock Manager/comData.csv"
billTemplatePath = "C:/Stock Manager/거래명세서.xlsx"
billFileDirectory = "C:/Stock Manager/bills"


class ReceiveDialog(QDialog, receive_dialog.Ui_receive_dialog):
    def __init__(self, comName):
        QDialog.__init__(self,None)

        self.setupUi(self)

        self.setWindowIcon(QIcon(iconPath))

        self.comFilePath= comDirectory+"/"+ comName+".csv"

        #--- initializting ---#
        tableWidgetInit(self.r_tableWidget, 7)

        self.showing(comName)
    
    def showing(self, comName):
        with open(self.comFilePath, mode='r') as reader:
            csv_reader = csv.reader(reader, delimiter= ',')
            comData = list(csv_reader)

            with open(comDataFilePath, mode= 'r') as reader:
                csv_reader = csv.reader(reader, delimiter= ',')
                comFileData= list(csv_reader)
                line =comSearch(comName)
                index = line[0]
                notReceived= int(comFileData[index][3])

            for i in range(len(comData)-1,-1 ,-1):
                total = int(comData[i][5]) + int(comData[i][6])
                comData[i][4] = str('{:,}'.format(total)) 
                if notReceived >= total:
                    comData[i][5] = "0"
                    notReceived -= total
                elif notReceived < total and notReceived != 0:
                    comData[i][5] = str('{:,}'.format(total-notReceived)) 
                    notReceived= 0
                else:
                    comData[i][5] = comData[i][4]
                
                if comData[i][5] == "0" and comData[i][4] != "0":
                    comData[i][6] = "X"
                elif comData[i][5] >= comData[i][4]:
                    comData[i][6] = "O"
                else:
                    comData[i][6] = "△"
            
            tableWidgetShow(comData[::-1], self.r_tableWidget, 7, [])

class ComDialog(QDialog, com_dialog.Ui_Com_Dialog):
    def __init__(self, objectNum_=0):
        QDialog.__init__(self,None)
        self.setupUi(self)

        #--- initializing ---#

        self.setWindowIcon(QIcon(iconPath))

        self.objectNum = objectNum_
        tableWidgetInit(self.c_tableWidget,1)

        result = [[line] for line in comList]
        tableWidgetShow(result, self.c_tableWidget, 1, [])

        #--- functions ---#
        self.c_pushButton_search.clicked.connect(self.c_pushButton_search_clicked)
        self.c_pushButton_select.clicked.connect(self.c_pushButton_select_clicked)

        self.c_lineEdit_search.returnPressed.connect(self.c_pushButton_search_clicked)
        
        comLineEditSetCompleter(self.c_lineEdit_search)

    def c_pushButton_search_clicked(self):
        lines= comSearch(self.c_lineEdit_search.text())

        result= [[comList[i]] for i in lines]
       
        tableWidgetShow(result, self.c_tableWidget, 1, [])
              

    def c_pushButton_select_clicked(self):
        try:
            row= self.c_tableWidget.currentItem().row()
        except:
            return 
        if self.objectNum == 0:
            main_dialog.s_label_com.setText(self.c_tableWidget.item(row,0).text())
        elif self.objectNum == 1:
            main_dialog.c_label_com.setText(self.c_tableWidget.item(row,0).text())

        self.close()

class ProductDialog(QDialog, product_dialog.Ui_product_Dialog):
    def __init__(self):
        QDialog.__init__(self,None)
        self.setupUi(self)

        self.comName=""

        #--- initializing ---#
        self.setWindowIcon(QIcon(iconPath))

        tableWidgetInit(self.p_tableWidget,5)
        stockTableWidgetUpdate(self.p_tableWidget)

        #--- functions ---#
        self.p_pushButton_search.clicked.connect(self.p_pushButton_search_clicked)
        self.p_pushButton_select.clicked.connect(self.p_pushButton_select_clicked)
        self.p_lineEdit_search.returnPressed.connect(self.p_pushButton_search_clicked)

        self.p_tableWidget.cellClicked.connect(self.p_tableWidget_cellClicked)

        productLineEditSetCompleter(self.p_lineEdit_search, 3)

    def p_tableWidget_cellClicked(self):
        row= self.p_tableWidget.currentItem().row()

        product_id = self.p_tableWidget.item(row,0).text()
        product_name = self.p_tableWidget.item(row,1).text()

        comFile= comDirectory+"/"+ self.comName+".csv"

        with open(comFile, mode = 'r') as comFileReader:
            csv_reader = csv.reader(comFileReader, delimiter= ',')
            comData = list(csv_reader)
            comData = comData[::-1]

            check = True
            for line in comData:
                if line[1] == product_id and line[2] == product_name:
                    self.p_label_price.setText(str('{:,}'.format(int(line[3]))))
                    check = False
                    break
            if check:
                self.p_label_price.setText("0")

    def p_pushButton_search_clicked(self):
        lines = stockDataSearch(self.p_lineEdit_search.text())
        with open(stockDataFilePath, mode= 'r') as stockFile:
            csv_reader = csv.reader(stockFile, delimiter= ',')
            stockData = list(csv_reader)

            result= [stockData[i] for i in lines]
        
        tableWidgetShow(result, self.p_tableWidget, 5, [3])

    def p_pushButton_select_clicked(self):
        try:
            row= self.p_tableWidget.currentItem().row()
        except:
            return

        main_dialog.s_lineEdit_ID.setText(self.p_tableWidget.item(row,0).text())
        main_dialog.s_lineEdit_name.setText(self.p_tableWidget.item(row,1).text())
        main_dialog.s_lineEdit_price.setText(self.p_label_price.text())
        main_dialog.s_lineEdit_num.setText("0")

        self.close()

class MainDialog(QDialog, main_dialog.Ui_MainDialog):
    def __init__(self):
        QDialog.__init__(self, None)
        self.setupUi(self)
        self.setFixedSize(815,545)

        #--- initializing ---#
        self.setWindowIcon(QIcon(iconPath))

        self.setTabOrder(self.rg_lineEdit_com, self.rg_lineEdit_name)
        self.setTabOrder(self.rg_lineEdit_name, self.rg_lineEdit_num)
        self.setTabOrder(self.rg_lineEdit_num, self.rg_pushButton)
        
        self.setTabOrder(self.s_dateEdit, self.s_lineEdit_ID)
        self.setTabOrder(self.s_lineEdit_ID, self.s_lineEdit_name)
        self.setTabOrder(self.s_lineEdit_name, self.s_lineEdit_price)
        self.setTabOrder(self.s_lineEdit_price, self.s_lineEdit_num)
        self.setTabOrder(self.s_lineEdit_num, self.s_pushButton_add)

        self.s_dateEdit.setDate(QtCore.QDate.currentDate())
        self.c_dateEdit_from.setDate(QtCore.QDate.currentDate())
        self.c_dateEdit_to.setDate(QtCore.QDate.currentDate())

        tableWidgetInit(self.b_tableWidget,5)
        tableWidgetInit(self.s_tableWidget,6)
        tableWidgetInit(self.st_tableWidget,5)
        tableWidgetInit(self.r_tableWidget,2)
        tableWidgetInit(self.c_tableWidget,7)

        stockTableWidgetUpdate(self.b_tableWidget)
        stockTableWidgetUpdate(self.st_tableWidget)
        receiveTableWidgetUpdate(self.r_tableWidget)

        self.b_lineEdit_num.setValidator(onlyInt)
        self.b_lineEdit_price.setValidator(onlyInt)
        self.s_lineEdit_num.setValidator(onlyInt)
        self.s_lineEdit_price.setValidator(onlyInt)
        self.r_lineEdit_receive.setValidator(onlyInt)
        self.rg_lineEdit_num.setValidator(onlyInt)

        #--- sorting the stock data ---#
        sortCsv()

        #--- stock tab ---#
        self.st_pushButton_search.clicked.connect(self.st_pushButton_search_clicked)
        self.st_pushButton_delete.clicked.connect(self.st_pushButton_delete_clicked)

        self.st_lineEdit_search.returnPressed.connect(self.st_pushButton_search_clicked)

        productLineEditSetCompleter(self.st_lineEdit_search, 3)
        
        #--- selling tab ---#
        self.com_dialog_0 = ComDialog(0)

        self.s_lineEdit_price.textChanged.connect(lambda state, lineEdit= self.s_lineEdit_price: moneyField(state, lineEdit))
        self.s_lineEdit_ID.textChanged.connect(lambda id_= self.s_lineEdit_ID.text(), lineEdit= self.s_lineEdit_name : fillNameWithID( id_, lineEdit))

        self.s_pushButton_product_search.clicked.connect(self.s_pushButton_product_search_clicked)
        self.s_pushButton_com_search.clicked.connect(self.s_pushButton_com_search_clicked)
        self.s_pushButton_add.clicked.connect(self.s_pushButton_add_clicked)
        self.s_pushButton_selling.clicked.connect(self.s_pushButton_selling_clicked)
        self.s_pushButton_delete.clicked.connect(self.s_pushButton_delete_clicked)

        productLineEditSetCompleter(self.s_lineEdit_ID, 0)
        productLineEditSetCompleter(self.s_lineEdit_name, 1)

        #--- buying tab ---#
        self.b_lineEdit_price.textChanged.connect(lambda state, lineEdit= self.b_lineEdit_price: moneyField(state, lineEdit))
        self.b_lineEdit_ID.textChanged.connect(lambda id_= self.b_lineEdit_ID.text(), lineEdit= self.b_lineEdit_name : fillNameWithID( id_, lineEdit))

        self.b_pushButton_add.clicked.connect(self.b_pushButton_add_clicked)
        self.b_pushButton_bring.clicked.connect(self.b_pushButton_bring_clicked)
        self.b_pushButton_search.clicked.connect(self.b_pushButton_search_clicked)
        
        self.b_lineEdit_search.returnPressed.connect(self.b_pushButton_search_clicked)

        productLineEditSetCompleter(self.b_lineEdit_search, 3)
        productLineEditSetCompleter(self.b_lineEdit_ID, 0)
        productLineEditSetCompleter(self.b_lineEdit_name, 1)
        productLineEditSetCompleter(self.b_lineEdit_com, 2)

        #--- Search Company tab ---#
        self.com_dialog_1 = ComDialog(1)

        self.c_pushButton_com_search.clicked.connect(self.c_pushButton_com_search_clicked)
        self.c_pushButton_search.clicked.connect(self.c_pushButton_search_clicked)
        self.c_pushButton_delete.clicked.connect(self.c_pushButton_delete_clicked)

        #--- Receive tab ---#
        self.r_lineEdit_receive.textChanged.connect(lambda state, lineEdit= self.r_lineEdit_receive: moneyField(state, lineEdit))

        comLineEditSetCompleter(self.r_lineEdit_search)
        self.r_lineEdit_search.returnPressed.connect(self.r_pushButton_search_clicked)
        self.r_pushButton_search.clicked.connect(self.r_pushButton_search_clicked)
        self.r_pushButton_receive.clicked.connect(self.r_pushButton_receive_clicked)
        self.r_pushButton_detail.clicked.connect(self.r_pushButton_detail_clicked)
        
        #--- company registeration tab ---#
        comLineEditSetCompleter(self.rg_lineEdit_com)

        self.rg_pushButton.clicked.connect(self.rg_pushButton_clicked)
        

    #--- stock tab function ---#
    
    def st_pushButton_search_clicked(self):
        lines = stockDataSearch(self.st_lineEdit_search.text())
        with open(stockDataFilePath, mode= 'r') as stockFile:
            csv_reader = csv.reader(stockFile, delimiter= ',')
            stockData = list(csv_reader)

            result= [stockData[i] for i in lines]
        tableWidgetShow(result, self.st_tableWidget, 5, [3])

    def st_pushButton_delete_clicked(self):
        tableWidget = self.st_tableWidget
        try:
            row= tableWidget.currentItem().row()
        except:
            return

        with open(stockDataFilePath, mode= 'r') as stockFile:
            csv_reader = csv.reader(stockFile, delimiter= ',')
            stockData = list(csv_reader)
            index=0
            for line in stockData:
                check=True
                for i in range(0,5):
                    if str(line[i]) != tableWidget.item(row,i).text().replace(",",""):
                        check= False
                        break
                if check:
                    break
                index+=1

            del stockData[index]

            updateCsv(stockData, stockDataFilePath, 5, [3,4])

        self.st_tableWidget.removeRow(row)
        stockTableWidgetUpdate(self.b_tableWidget)

    #--- selling tab function ---#
    def s_pushButton_product_search_clicked(self):
        if self.s_label_com.text() == "" :
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("매출처 미입력")
            msg.setInformativeText("회사 검색으로 매출처를 입력해주세요.")
            msg.setWindowTitle("Company Blank is not filled")
                
            retval = msg.exec_()

            return

        product_dialog.comName = self.s_label_com.text()
        product_dialog.show()

    def s_pushButton_com_search_clicked(self):
        
        self.com_dialog_0.show()

    def s_pushButton_add_clicked(self):
        if self.s_lineEdit_price.text() =="":
            self.s_lineEdit_price.setText("0")
        if self.s_lineEdit_num.text() =="":
            self.s_lineEdit_num.setText("0")

        price = str(int(self.s_lineEdit_price.text().replace(",",""))* int(self.s_lineEdit_num.text()))
        tax = str(int(round(int(price),-1)*0.1))
        line = [self.s_lineEdit_ID.text(), self.s_lineEdit_name.text(), self.s_lineEdit_price.text().replace(",",""), self.s_lineEdit_num.text(), price , tax]
        
        total= int(self.s_label_total_price.text().replace(",",""))+ int(int(price) + int(tax))
        self.s_label_total_price.setText('{:,}'.format(total))

        self.s_lineEdit_ID.setText("")
        self.s_lineEdit_name.setText("")
        self.s_lineEdit_price.setText("")
        self.s_lineEdit_num.setText("")
        tableWidgetRowAdd(line, self.s_tableWidget ,6, [2,4,5])
    
    def s_pushButton_selling_clicked(self):
        if self.s_label_com.text() == "":
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("매출처 미입력")
            msg.setInformativeText("회사 검색으로 매출처를 입력해주세요.")
            msg.setWindowTitle("Company Blank is not filled")
                
            retval = msg.exec_()

            return

        if self.s_tableWidget.rowCount() == "":
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("판매 물건 미등록")
            msg.setInformativeText("판매할 물건이 등록되지 않았습니다.")
            msg.setWindowTitle("Products to sell not registered")
                
            retval = msg.exec_()

            return
        
        row = self.s_tableWidget.rowCount()

        with open(stockDataFilePath, mode= 'r') as stockFile:
            csv_reader = csv.reader(stockFile, delimiter= ',')
            csv_reader = list(csv_reader)
            
            for i in range(0, row):
                check= False
                for j in range(0, len(csv_reader)):
                    if csv_reader[j][0] == self.s_tableWidget.item(i,0).text() and csv_reader[j][1] == self.s_tableWidget.item(i,1).text() and int(csv_reader[j][4])>= int(self.s_tableWidget.item(i,3).text()):
                        num = int(csv_reader[j][4])-int(self.s_tableWidget.item(i,3).text())
                        csv_reader[j][4] = str(num)
                        check= True
                        break

                if check == False:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Warning)
                    msg.setText("유효하지 않은 품번.품명.수량")
                    msg.setInformativeText("품번 또는 품명 또는 수량이 유효하지 않습니다. 수량이 유효한지 확인해 주세요.")
                    msg.setWindowTitle("Not valid ID or Name or num")
                        
                    retval = msg.exec_()

                    return
            updateCsv(csv_reader, stockDataFilePath, 5, [3,4])

        #--- 미수금 더하기
        buyer = "" # 성명
        buyer_num = "" # 사업자 번호
        with open(comDataFilePath, 'r') as comDataFileR:
            csv_reader = csv.reader(comDataFileR, delimiter= ',')
            comData = list(csv_reader)
            comLine=0
            for i in range(0, len(comData)):
                if comData[i][0] == self.s_label_com.text():
                    comLine = i
                    buyer = comData[i][1]
                    buyer_num = comData[i][2]
                    break
            with open(comDataFilePath, 'w') as comDataFileW:
                for i in range(0, len(comData)):
                    if i == comLine:
                        comDataFileW.write(comData[i][0]+","+comData[i][1]+","+comData[i][2]+","+str(int(comData[i][3])+int(self.s_label_total_price.text().replace(",","")))+"\n")    
                    else:
                        comDataFileW.write(comData[i][0]+","+comData[i][1]+","+comData[i][2]+","+comData[i][3]+"\n")

        comFilePath= comDirectory+"/"+ self.s_label_com.text()+".csv"
        
        #--- trading 데이터 저장
        pyTradeDate = self.s_dateEdit.date().toPyDate()
        tradeDate = str(self.s_dateEdit.date().toPyDate())

        with open(comFilePath, "a") as comFile:
            for i in range(0, row):
                comFile.write(tradeDate+","+self.s_tableWidget.item(i,0).text()+","+self.s_tableWidget.item(i,1).text()+","+self.s_tableWidget.item(i,2).text().replace(",","")+","+self.s_tableWidget.item(i,3).text()+","+self.s_tableWidget.item(i,4).text().replace(",","")+","+self.s_tableWidget.item(i,5).text().replace(",","")+"\n")

        #--- Excel 저장, pdf 저장 후 열기.

        from openpyxl import load_workbook

        numOfSheets = int((row-1)/10)+1
        rowsOfEachSheet = []
        for i in range(0,numOfSheets):
            if i < numOfSheets-1:
                rowsOfEachSheet.append(10)
            else:
                if row%10 == 0:
                    rowsOfEachSheet.append(10)
                else:
                    rowsOfEachSheet.append(row%10)
    
        for sheet in range(0, numOfSheets):
            load_wb = load_workbook(billTemplatePath)

            write_ws= load_wb.active
            write_ws = uglyBorderSet(write_ws)

            write_ws = fillIn(write_ws, "N", 3, tradeDate)
            write_ws = fillIn(write_ws, "R", 6, self.s_label_com.text())
            write_ws = fillIn(write_ws, "X", 6, buyer)

            price =0
            tax =0
            count =0
            for i in range(sheet*10, sheet*10 + rowsOfEachSheet[sheet]):
                write_ws = fillIn(write_ws, "B", count+10, str(pyTradeDate.month)+"/"+str(pyTradeDate.day))
                write_ws = fillIn(write_ws, "D", count+10, self.s_tableWidget.item(i,0).text())
                write_ws = fillIn(write_ws, "H", count+10, self.s_tableWidget.item(i,1).text())
                write_ws = fillIn(write_ws, "M", count+10, self.s_tableWidget.item(i,3).text())
                write_ws = fillIn(write_ws, "P", count+10, self.s_tableWidget.item(i,2).text())
                write_ws = fillIn(write_ws, "U", count+10, self.s_tableWidget.item(i,4).text())
                write_ws = fillIn(write_ws, "Z", count+10, self.s_tableWidget.item(i,5).text())
                price += int(self.s_tableWidget.item(i,4).text().replace(",",""))
                tax += int(self.s_tableWidget.item(i,5).text().replace(",",""))
                count += 1
            write_ws = fillIn(write_ws, "E", 20, str('{:,}'.format(price)))
            write_ws = fillIn(write_ws, "M", 20, str('{:,}'.format(tax)))
            write_ws = fillIn(write_ws, "V", 20, str('{:,}'.format(price+tax)))

            comDir = billFileDirectory+"/"+self.s_label_com.text() 
        
            if not os.path.exists(comDir):
                os.makedirs(comDir)

            billFile = comDir+"/"+str(self.s_dateEdit.date().toPyDate())+"("
            replication = 0
            while os.path.exists(billFile+str(replication)+").xlsx"):
                replication+=1
            
            billFile += str(replication)+")"

            load_wb.save(billFile+".xlsx")

            # if you want to make a pdf from excel, use this code

            # from win32com import client

            # xlApp = client.Dispatch("Excel.Application")
            # books = xlApp.Workbooks.Open(billFile+".xlsx")
            # ws = books.Worksheets[0]
            # ws.Visible = 1
            # ws.ExportAsFixedFormat(0, billFile+'.pdf')
            # books.Close()
            # xlApp.Quit()

            os.startfile(billFile+'.xlsx')


        #--- 초기화
        self.s_label_com.clear()
        self.s_dateEdit.setDate(QtCore.QDate.currentDate())
        self.s_label_total_price.setText("0")
        self.s_tableWidget.clearContents()
        self.s_tableWidget.setRowCount(0)

        receiveTableWidgetUpdate(self.r_tableWidget)
        stockTableWidgetUpdate(self.st_tableWidget)
        stockTableWidgetUpdate(self.b_tableWidget) 
        stockTableWidgetUpdate(product_dialog.p_tableWidget)


    def s_pushButton_delete_clicked(self):
        try:
            row= self.s_tableWidget.currentItem().row()
        except:
            return 

        total= int(self.s_label_total_price.text().replace(",",""))- int(int(self.s_tableWidget.item(row,4).text().replace(",","")) + int(self.s_tableWidget.item(row,5).text().replace(",","")))
        self.s_label_total_price.setText('{:,}'.format(total))

        self.s_tableWidget.removeRow(row)

    #--- buying tab function ---#

    def b_pushButton_add_clicked(self):
        with open(stockDataFilePath, mode= 'r') as stockFile:
            csv_reader = csv.reader(stockFile, delimiter= ',')
            csv_reader = list(csv_reader)
            check = False
            for row in range(0, len(csv_reader)):
                if csv_reader[row][0] == self.b_lineEdit_ID.text() and csv_reader[row][1] == self.b_lineEdit_name.text() and csv_reader[row][2] == self.b_lineEdit_com.text():
                    csv_reader[row][3] = self.b_lineEdit_price.text().replace(",","")
                    
                    num = int(csv_reader[row][4])+int(self.b_lineEdit_num.text())
                    csv_reader[row][4] = str(num)

                    updateCsv(csv_reader, stockDataFilePath, 5, [3,4])

                    check = True
                    break

        if check == False:
            with open(stockDataFilePath,"a") as stockFile:
                stockFile.write(self.b_lineEdit_ID.text()+","+self.b_lineEdit_name.text()+","+self.b_lineEdit_com.text()+","+self.b_lineEdit_price.text().replace(",","")+","+self.b_lineEdit_num.text()+"\n" )
        
        sortCsv()
        stockTableWidgetUpdate(self.b_tableWidget)
        stockTableWidgetUpdate(self.st_tableWidget)
        stockTableWidgetUpdate(product_dialog.p_tableWidget)

        self.b_lineEdit_ID.clear()
        self.b_lineEdit_com.clear()
        self.b_lineEdit_name.clear()
        self.b_lineEdit_price.clear()
        self.b_lineEdit_num.clear()
    
    def b_pushButton_bring_clicked(self):
        tableWidget = self.b_tableWidget
        try:
            row= tableWidget.currentItem().row()
        except:
            return

        self.b_lineEdit_ID.setText(tableWidget.item(row,0).text())
        self.b_lineEdit_name.setText(tableWidget.item(row,1).text())
        self.b_lineEdit_com.setText(tableWidget.item(row,2).text())
        self.b_lineEdit_price.setText(tableWidget.item(row,3).text())
        self.b_lineEdit_num.setText(tableWidget.item(row,4).text())

    def b_pushButton_search_clicked(self):
        lines = stockDataSearch(self.b_lineEdit_search.text())
        with open(stockDataFilePath, mode= 'r') as stockFile:
            csv_reader = csv.reader(stockFile, delimiter= ',')
            stockData = list(csv_reader)

            result= [stockData[i] for i in lines]
        tableWidgetShow(result, self.b_tableWidget, 5, [3])

    #--- search company tab ---#
    def c_pushButton_com_search_clicked(self):
        self.com_dialog_1.show()

    def c_pushButton_search_clicked(self):
        if self.c_label_com.text() == "":
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("업체명 미입력")
            msg.setInformativeText("업체명이 입력되지 않았습니다.")
            msg.setWindowTitle("Company Blank is not filled")
                
            retval = msg.exec_()

            return

        if self.c_dateEdit_from.date().toPyDate() > self.c_dateEdit_to.date().toPyDate():
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("조회 기간 유효하지 않음")
            msg.setInformativeText("조회 기간이 유효하지 않습니다.")
            msg.setWindowTitle("Not valid period")
                
            retval = msg.exec_()

            return

        comFile= comDirectory+"/"+ self.c_label_com.text()+".csv"

        with open(comFile, mode = 'r') as comFileReader:
            csv_reader = csv.reader(comFileReader, delimiter= ',')
            comData = list(csv_reader)
            showLine= []
            for line in comData:
                if self.c_dateEdit_from.date().toPyDate() <= datetime.datetime.strptime(line[0], '%Y-%m-%d').date() and self.c_dateEdit_to.date().toPyDate() >= datetime.datetime.strptime(line[0], '%Y-%m-%d').date():
                    showLine.append(line) 
            tableWidgetShow(showLine, self.c_tableWidget, 7, [3,5,6])
        
        self.calculateAndShow()

    def c_pushButton_delete_clicked(self):
        try:
            row= self.c_tableWidget.currentItem().row()
        except:
            return 

        comFile= comDirectory+"/"+ self.c_label_com.text()+".csv"

        deleteMoney=0
        with open(comFile, mode= 'r') as comFileReader:
            csv_reader = csv.reader(comFileReader, delimiter= ',')
            comData = list(csv_reader)
            index=0
            for line in comData:
                check=True
                for i in range(0,7):
                    if str(line[i]) != self.c_tableWidget.item(row,i).text().replace(",",""):
                        check= False
                        break
                if check:
                    deleteMoney = int(self.c_tableWidget.item(row, 5).text().replace(",",""))+int(self.c_tableWidget.item(row, 6).text().replace(",",""))
                    break
                index+=1

            del comData[index]

            updateCsv(comData, comFile, 7, [3,4,5,6])

        self.c_tableWidget.removeRow(row)
        
        self.calculateAndShow()

        with open(comDataFilePath, 'r') as comDataFileR:
            csv_reader = csv.reader(comDataFileR, delimiter= ',')
            comData = list(csv_reader)
            comLine=0
            for i in range(0, len(comData)):
                if comData[i][0] == self.c_label_com.text():
                    comLine = i
                    break
            with open(comDataFilePath, 'w') as comDataFileW:
                for i in range(0, len(comData)):
                    if i == comLine:
                        comDataFileW.write(comData[i][0]+","+comData[i][1]+","+comData[i][2]+","+str(int(comData[i][3])-deleteMoney)+"\n")    
                    else:
                        comDataFileW.write(comData[i][0]+","+comData[i][1]+","+comData[i][2]+","+comData[i][3]+"\n")
        
        receiveTableWidgetUpdate(self.r_tableWidget)

    def calculateAndShow(self):
        row = self.c_tableWidget.rowCount()

        price =0
        tax =0
        for i in range(0, row):
            price += int(self.c_tableWidget.item(i,5).text().replace(",",""))
            tax += int(self.c_tableWidget.item(i,6).text().replace(",",""))
        total = price + tax

        self.c_label_price.setText(str('{:,}'.format(price)))
        self.c_label_tax.setText(str('{:,}'.format(tax)))
        self.c_label_total.setText(str('{:,}'.format(total)))

    #--- Receive tab ---#

    def r_pushButton_search_clicked(self):
        lines= comSearch(self.r_lineEdit_search.text())

        with open(comDataFilePath, mode= 'r') as comDataFile:
            csv_reader = csv.reader(comDataFile, delimiter= ',')
            comData = list(csv_reader)

            data = [[comData[i][0], comData[i][3] ] for i in lines]
            tableWidgetShow(data, self.r_tableWidget, 2, [1])

    def r_pushButton_receive_clicked(self):
        try:
            row= self.r_tableWidget.currentItem().row()
        except:
            return 

        with open(comDataFilePath, mode= 'r') as comDataFile:
            csv_reader = csv.reader(comDataFile, delimiter= ',')
            comData = list(csv_reader)
            moneyLeft =""

            for i in range(0, len(comData)):
                if comData[i][0] == self.r_tableWidget.item(row,0).text():
                    moneyLeft= str(int(comData[i][3].replace(",", ""))- int(self.r_lineEdit_receive.text().replace(",","")))
                    comData[i][3] = moneyLeft
                    break

            self.r_tableWidget.item(row,1).setText(str('{:,}'.format(int(moneyLeft))))            
            updateCsv(comData, comDataFilePath, 4, [3])

        self.r_lineEdit_receive.setText("")
    
    def r_pushButton_detail_clicked(self):
        try:
            row= self.r_tableWidget.currentItem().row()
        except:
            return 

        self.receive_dialog = ReceiveDialog(self.r_tableWidget.item(row,0).text())
        self.receive_dialog.show()

    #--- company registeration tab ---#
    def rg_pushButton_clicked(self):
        if not os.path.exists(comDirectory):
            os.makedirs(comDirectory)
    
        msg = QMessageBox()

        if self.rg_lineEdit_com.text() == "":

            msg.setIcon(QMessageBox.Warning)
            msg.setText("업체명 미입력")
            msg.setInformativeText("업체명이 입력되지 않았습니다.")
            msg.setWindowTitle("Company Blank is not filled")
                
            retval = msg.exec_()

            return

        if self.rg_lineEdit_num.text() in comNumList:
            msg.setIcon(QMessageBox.Warning)
            msg.setText("이미 등록된 업체")
            msg.setInformativeText("이미 등록된 사업자 번호입니다.")
            msg.setWindowTitle("Registered Company Error")
                
            retval = msg.exec_()

            return

        comFile= comDirectory+"/"+ self.rg_lineEdit_com.text()+".csv"
        try:
            stockFile = open(comFile, 'r')

            msg.setIcon(QMessageBox.Warning)
            msg.setText("이미 등록된 업체")
            msg.setInformativeText("이미 등록된 업체입니다.")
            msg.setWindowTitle("Registered Company Error")
                
            retval = msg.exec_()

        except IOError:
            stockFile = open(comFile, 'w')
            
            with open(comDataFilePath, mode= 'a') as comFile:
                comFile.write(self.rg_lineEdit_com.text()+","+self.rg_lineEdit_name.text()+","+self.rg_lineEdit_num.text()+","+"0\n")
            
            comList.append(self.rg_lineEdit_com.text())
            comNumList.append(self.rg_lineEdit_num.text())

            comTableWidgetUpdate(self.com_dialog_0.c_tableWidget)

            comTableWidgetUpdate(self.com_dialog_1.c_tableWidget)

            self.rg_lineEdit_com.setText("")
            self.rg_lineEdit_name.setText("")
            self.rg_lineEdit_num.setText("")

            msg.setIcon(QMessageBox.Information)
            msg.setText("등록 완료")
            msg.setInformativeText("등록이 완료되었습니다.")
            msg.setWindowTitle("Company Registered")
                
            retval = msg.exec_()



#--- Common Functions ---#

### Init functions 
def tableWidgetInit(tableWidget, num):
    '''
    num: the number of categories
    '''
    tableWidget.setSortingEnabled(True)

    header= tableWidget.horizontalHeader()
    for i in range(0, num):
        header.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)

### Completer

def comLineEditSetCompleter(lineEdit):
    completer = QCompleter()
    model = QtCore.QStringListModel()
    model.setStringList(comList)
    completer.setModel(model)
    lineEdit.setCompleter(completer)

def productLineEditSetCompleter( lineEdit, select):
    completer = QCompleter()
    completer.setModel(autoCompletionModel(select))
    lineEdit.setCompleter(completer)

def autoCompletionModel( select):
    '''
    select: int
            0 for ID
            1 for name
            2 for com
            3 for Id, name, and com

    return : model
    '''
    model = QtCore.QStringListModel()

    with open(stockDataFilePath, mode= 'r') as stockFile:
        csv_reader = csv.reader(stockFile, delimiter= ',')
        stockData = list(csv_reader)
        IDs = [row[0] for row in stockData]
        names = [row[1] for row in stockData]
        coms = [row[2] for row in stockData]

    if select == 0:
        model.setStringList(IDs)
    elif select == 1:
        model.setStringList(names)
    elif select == 2:
        model.setStringList(coms)
    else:
        model.setStringList(IDs+names+coms)
    
    return model

onlyInt = QIntValidator()

### Sharing functions

def comTableWidgetUpdate(tableWidget):
    tableWidget.clearContents()
    tableWidget.setRowCount(0)
    with open(comDataFilePath, mode= 'r') as stockFile:
        csv_reader = csv.reader(stockFile, delimiter= ',')

        for line in csv_reader:
            tableWidgetRowAdd(line, tableWidget, 1,[])

def stockTableWidgetUpdate( tableWidget):
    '''
    tableWidget: tableWidget to update base on the stock data csv
    '''
    tableWidget.clearContents()
    tableWidget.setRowCount(0)
    with open(stockDataFilePath, mode= 'r') as stockFile:
        csv_reader = csv.reader(stockFile, delimiter= ',')

        tableWidgetShow(csv_reader, tableWidget, 5, [3])

def receiveTableWidgetUpdate( tableWidget):
    '''
    tableWidget: tableWidget to update base on the data csv
    '''
    tableWidget.clearContents()
    tableWidget.setRowCount(0)
    with open(comDataFilePath, mode= 'r') as comDataFile:
        csv_reader = csv.reader(comDataFile, delimiter= ',')
        
        result = [[line[0], line[3]] for line in csv_reader]
        tableWidgetShow(result, tableWidget, 2, [1])


def tableWidgetShow(data, tableWidget, numCategories, moneyFieldIndexes):
    '''
    data: [-1, numCategories] list of string
    moneyFieldIndexes: (list of int)the list of indexes which need money field
    '''
    tableWidget.clearContents()
    tableWidget.setRowCount(0)

    for line in data:
        tableWidgetRowAdd(line, tableWidget, numCategories, moneyFieldIndexes)

def tableWidgetRowAdd(line, tableWidget, numCategories, moneyFieldIndexes):
    '''
    line: (list of str)row data with numCategries elems
    numCategories: (int)the number of Categories
    moneyFieldIndexes: (list of int)the list of indexes which need money field

    '''
    row = tableWidget.rowCount()

    tableWidget.insertRow(row)

    for col in range(0, numCategories):
        if col in moneyFieldIndexes:
            price = int(line[col])
            item = QTableWidgetItem(str('{:,}'.format(price)))
            item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
            item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            tableWidget.setItem(row, col, item)

        else:
            item = QTableWidgetItem(line[col])
            item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
            item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            tableWidget.setItem(row, col, item)

def moneyField(state,lineEdit):
    '''
    state: Don't care
    lineEdit: lineEdit

    return: None
    '''
    try:
        price = int(lineEdit.text().replace(",",""))
        moneyText= str('{:,}'.format(price))
        lineEdit.setText(moneyText)
    except:
        pass

def fillNameWithID( ID, lineEdit):
    '''
    ID: fill name lineEdit with this ID
    lineEdit: name lineEdit to fill
    '''
    ls = searchByID(ID)

    if len(ls) is not 0:
        name = ls[1]
        lineEdit.setText(name)
    

def searchByID(ID):
    '''
    ID: string
    return: list of a row
    '''
    with open(stockDataFilePath, mode= 'r') as stockFile:
        csv_reader = csv.reader(stockFile, delimiter= ',')
        for line in csv_reader:
            if line[0] == ID:
                return list(line)
    return []
            

def stockDataSearch( word):
    '''
    word: string
    return: list with index of contents
    '''
    with open(stockDataFilePath, mode= 'r') as stockFile:
        csv_reader = csv.reader(stockFile, delimiter= ',')
        stockData = list(csv_reader)
        lines = []
        for row in range(0, len(stockData)):
            for col in range(0,3):
                if word in stockData[row][col]:
                    lines += [row]
                    break
    return lines

def comSearch(word):
    lines= []
    for i in range(0, len(comList)):
        if word in comList[i]:
            lines +=[i]
            
    return lines 

def sortCsv():
    sortedData= list
    with open(stockDataFilePath, mode= 'r') as stockFile:
        csv_reader = csv.reader(stockFile, delimiter= ',')
        sortedData = sorted(csv_reader, key=operator.itemgetter(0))
        
    updateCsv(sortedData, stockDataFilePath, 5, [3,4])

def updateCsv(csvData, filePath, numCategories, numArea):
    '''
    csvData: [-1, numCategories] of data to save in Csv
    filePath: String for filePath
    numArea: [int] the index of numArea
    '''
    with open(filePath, mode = 'w') as file:
        for line in csvData:
            for col in range(0,numCategories):
                if col in numArea:
                    if line[col] == "":
                        line[col] = "0"    
                file.write(line[col]+",")
            file.write("\n")

def fillIn(write_ws, col, row, word):
    '''
    write_ws
    col: string
    row: int
    word: string to fill
    '''
    write_ws[col+str(row)] = word
    write_ws[col+str(row+22)] = word

    return write_ws

def uglyBorderSet(write_ws):    
    from openpyxl.styles.borders import Border, Side

    blue_dot_border = Border(right=Side(style='thin', color= 'FF0059FF'), bottom=Side(style='hair', color = 'FF0059FF')) 
    blue_thin_border = Border(right=Side(style='thin', color= 'FF0059FF')) 

    red_dot_bt_border = Border(right=Side(style='thin', color= 'FFFF0000'), bottom=Side(style='hair', color = 'FFFF0000')) 
    red_dot_border = Border(right=Side(style='hair', color= 'FFFF0000'), bottom=Side(style='hair', color = 'FFFF0000')) 

    red_thin_border = Border(right=Side(style='thin', color= 'FFFF0000')) 

    red_hair_border = Border(right=Side(style='hair', color= 'FFFF0000')) 
    red_thin_bt_border = Border(right=Side(style='thin', color= 'FFFF0000'), bottom=Side(style='thin', color = 'FFFF0000')) 

    red_top_thin_right_hair = Border(right=Side(style='hair', color= 'FFFF0000'), top=Side(style='thin', color = 'FFFF0000'))
    red_right_hair = Border(right=Side(style='hair', color= 'FFFF0000')) 

    write_ws['AB4'].border = blue_thin_border
    write_ws['AB7'].border = blue_dot_border
    write_ws['AB8'].border = blue_thin_border
    write_ws['AB15'].border = blue_dot_border
    write_ws['AB16'].border = blue_dot_border
    write_ws['AB17'].border = blue_dot_border
    write_ws['AB18'].border = blue_dot_border
    write_ws['AB19'].border = blue_thin_border

    write_ws['M25'].border = red_top_thin_right_hair
    write_ws['S25'].border = red_top_thin_right_hair
    write_ws['AA25'].border = red_top_thin_right_hair
    write_ws['N26'].border = red_right_hair


    write_ws['AB26'].border = red_thin_border
    write_ws['AB29'].border = red_dot_bt_border
    write_ws['AB30'].border = red_thin_bt_border
    write_ws['AB31'].border = red_dot_bt_border
    write_ws['AB32'].border = red_dot_bt_border
    write_ws['AB33'].border = red_dot_bt_border
    write_ws['AB34'].border = red_dot_bt_border
    write_ws['AB35'].border = red_dot_bt_border
    write_ws['AB36'].border = red_thin_bt_border
    write_ws['AB37'].border = red_dot_bt_border
    write_ws['AB38'].border = red_dot_bt_border
    write_ws['AB39'].border = red_dot_bt_border
    write_ws['AB40'].border = red_dot_bt_border
    write_ws['AB41'].border = red_thin_bt_border


    write_ws['G33'].border = red_dot_border
    write_ws['G34'].border = red_dot_border
    write_ws['G35'].border = red_dot_border
    write_ws['G36'].border = red_hair_border
    write_ws['G38'].border = red_dot_border
    write_ws['G39'].border = red_dot_border
    write_ws['G40'].border = red_dot_border
    write_ws['G41'].border = red_hair_border

    return write_ws


#--- main function ---#
if __name__ == "__main__":
    if not os.path.exists(directory):
        if (not os.path.exists("./st_mark_iTO_2.ico")) or (not os.path.exists("./거래명세서.xlsx")):
            app = QApplication(sys.argv)
    
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("파일 위치 오류")
            msg.setInformativeText("stock Manager 최초 실행시, st_mark_iTo_2.ico 파일과 거래명세서.xlsx 파일이 같은 폴더 내에 있어야 합니다.")
            msg.setWindowTitle("File Location Error")
                
            retval = msg.exec_()
            
            import time
            time.sleep(3)

            exit()
            
        os.makedirs(directory)
        os.rename("./st_mark_iTO_2.ico", directory+"/st_mark_iTO_2.ico")
        os.rename("./거래명세서.xlsx", directory+"/거래명세서.xlsx")

    if not os.path.exists(billFileDirectory):
        os.makedirs(billFileDirectory)

    try:
        stockFile = open(stockDataFilePath, 'r')
    except IOError:
        stockFile = open(stockDataFilePath, 'w')

    try:
        comFile = open(comDataFilePath, 'r')
    except IOError:
        comFile = open(comDataFilePath, 'w')
        
    if not os.path.exists(comDirectory):
        os.makedirs(comDirectory)

    with open(comDataFilePath, mode='r') as comFile:
        csv_reader = csv.reader(comFile, delimiter= ',')
        comData = list(csv_reader)
        comList = [elem[0] for elem in comData]
        comNumList = [elem[2] for elem in comData]

    app = QApplication(sys.argv)
    
    main_dialog = MainDialog()
    product_dialog = ProductDialog()
    
    main_dialog.show()
    app.exec_()

