
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMessageBox

#from PyQt5.QtCore import QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent 
from PyQt5.QtGui import * 
from PyQt5.uic import loadUiType
from PyQt5 import QtWidgets, QtCore
from datetime import date

import sqlite3
from sqlite3 import Error
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter, A4

import sys
from os import path
#import pymsgbox
import ctypes
from sqliteDb import *
myFunc = SqliteDb("C:/allFiles/carteVisiteSqlite.db")

today = date.today()

global msgBox
#import UI file
FORM_CLASS,_ =loadUiType(path.join(path.dirname(__file__),'carte_identite.ui'))	

class MyProject(QMainWindow, FORM_CLASS):
    def __init__(self, parent=None):
        super(MyProject, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        
        self.maFenetre()
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.table_student.setColumnWidth(0,0)
        self.table_student.setColumnWidth(1,30)
        self.table_student.setColumnWidth(2,80)
        self.table_student.setColumnWidth(3,80)
        self.table_student.setColumnWidth(4,100)
        self.table_student.setColumnWidth(5,20)
        self.table_student.setColumnWidth(6,190)
        self.table_student.setColumnWidth(7,250)
        self.afficher_student()
        text0=self.lineNo.text()
        self.table_student.setColumnWidth(0,0)
        
        
        self.btn_save.clicked.connect(self.insert_student)
        self.closeButton.clicked.connect(lambda: self.close())
        self.minimizeButton.clicked.connect(lambda: self.showMinimized())

        # self.btn_pdf.clicked.connect(self.show_ordonnance)
        self.btn_ShowPatients.clicked.connect(self.afficher_student)
        self.btn_delete.clicked.connect(self.delete_student)
        self.btn_update.clicked.connect(self.update_student)
        self.btn_fill.clicked.connect(self.fill_From_tableClient_ToTextBox)
        # self.btn_image.clicked.connect(self.afficher_image)
        self.btn_search.clicked.connect(self.recherche_student)
        self.btn_image.clicked.connect(self.import_Photo)
        self.btn_genererPDF.clicked.connect( self.genererPDF)

   
#*********************************************************************
    def msg_display(self,title,msg):
        self.msgBox = QMessageBox()
        self.msgBox.setWindowTitle(title)
        self.msgBox.setText(msg)
        self.msgBox.exec() 

    def import_Photo(self):   
        
        image_path,return_status=QFileDialog.getOpenFileName()
        print(image_path)
        self.lineEdit_photo.setText(str(image_path))
        if image_path.split('.')[1] not in ['img','jpg','jpeg','png']:
            self.msg_display("ERROR","Select only image files!")
        else:
            image=QPixmap(image_path).scaled(self.labelPhoto.height(),self.labelPhoto.width())
            self.labelPhoto.setPixmap(image)
        
        # with open(self.image_path, 'rb') as file:
        #     empPhoto = file.read() 
            
        # print(empPhoto)
    
    def insert_student(self):     
        try:
            text1=self.lineEdit_code.text()
            text2=self.lineEdit_fname.text()
            text3=self.lineEdit_lname.text()
            text4=self.lineEdit_date.text()
            text5=self.lineEdit_gender.text()
            text6=self.lineEdit_adress.text()
            text7=self.lineEdit_photo.text()  

            if text2.strip(" ") != "" and text3.strip(" ") != "" and text4.strip(" ") != "" and text5.strip(" ") != "" and text6.strip(" ") != "" and text7.strip(" ") != "":

                student =(text1,text2,text3,text4,text5,text6,text7)
                myFunc.insert("INSERT INTO student_profile(code,fname,lname,date,gender,adress,pathFile) VALUES (?,?,?,?,?,?,?)", student)
                
                self.refresh()
            else:
                self.msg_display("ERROR","Fill all boxes")
            #raise TypeError('doublons')
        except Exception as e:
            self.msg_display("ERROR","Doublons")
            print('error',e)        

            self.refresh()
            self.lineEdit_code.setText("")
            self.lineEdit_fname.setText("")
            self.lineEdit_lname.setText("")
            self.lineEdit_date.setText("")
            self.lineEdit_gender.setText("")
            self.lineEdit_adress.setText("")
            self.lineEdit_photo.setText("")
            self.labelPhoto.clear()

#**********************************************************************

                
    def update_student(self):
        
        global image_path
        id_update = self.getSelectedStudentId()
        text1=self.lineEdit_code.text()
        text2=self.lineEdit_fname.text()
        text3=self.lineEdit_lname.text()
        text4=self.lineEdit_date.text()
        text5=self.lineEdit_gender.text()
        text6=self.lineEdit_adress.text()
        text7=self.lineEdit_photo.text()
        
        
        if text2.strip(" ") != "" and text3.strip(" ") != "" and text4.strip(" ") != "" and text5.strip(" ") != "" and text6.strip(" ") != "" and text7.strip(" ") != "":

            
            student =(text1,text2,text3,text4,text5,text6,text7)
            
            myFunc.update("UPDATE student_profile SET code= ? ,fname = ?, lname= ? , date= ? , adress= ?, gender= ?  ,pathFile= ? WHERE id = "+id_update, student)
            self.refresh()
        else:
            self.msg_display("خطأ","  املأ الوقت")
            #QMessageBox.information(self, "Failed","ERROR") 
            
            
        self.refresh()
        self.lineEdit_code.setText("")
        self.lineEdit_fname.setText("")
        self.lineEdit_lname.setText("")
        self.lineEdit_date.setText("")
        self.lineEdit_gender.setText("")
        self.lineEdit_adress.setText("")
        self.lineEdit_photo.setText("")
        self.labelPhoto.clear()
        

# ********************************************************************
        
    def afficher_student(self):
        self.clearData()
        users = myFunc.select("SELECT * FROM student_profile")
        
        for row_number, user in enumerate(users):
            self.table_student.insertRow(row_number)
            for column_number, data in enumerate(user):
                cell = QtWidgets.QTableWidgetItem(str(data))
                self.table_student.setItem(row_number,column_number,cell)
            

#**********************************************************************
        
    def refresh(self):
        self.clearData()
        self.afficher_student()
        
#**********************************************************************
        
    def clearData(self):
        self.table_student.clearSelection()
        while(self.table_student.rowCount() > 0):
            self.table_student.removeRow(0)
            self.table_student.clearSelection()

            
#**********************************************************************

                
    def fill_From_tableClient_ToTextBox(self):

        resultat = myFunc.select("SELECT * FROM student_profile")
        # resultat = rs.execute(sql)
        for row in enumerate(resultat):
            if row[0] == self.table_student.currentRow():
                data=row[1]
                # self.lineEditEnregist.setText(str(data[1])+" "+str(data[2]))
                
                self.lineEdit_code.setText(str(data[1]))
                self.lineEdit_fname.setText(str(data[2]))
                self.lineEdit_lname.setText(str(data[3]))
                self.lineEdit_date.setText(str(data[4]))
                self.lineEdit_gender.setText(str(data[5]))
                self.lineEdit_adress.setText(str(data[6]))
                self.lineEdit_photo.setText(str(data[7]))

                self.labelPhoto.setPixmap(QPixmap(data[-1]))

            #     photo=data[6]
            #     print("Storing employee image and resume on disk \n")
            #     self.photoPath = "D:\photos\\" +" me" + ".jpg"
            #     # writeTofile(photo, photoPath)
            #     with open(self.photoPath, 'wb') as file:
            #         file.write(photo)
      		    # # print("Stored blob data into: ", filename, "\n")
            #     image=QPixmap(self.photoPath).scaled(self.labelPhoto.height(),self.labelPhoto.width())
            #     self.labelPhoto.setPixmap(image)
                       
#**********************************************************************           
    
    def delete_student(self):
        message=QMessageBox.question(self, "u حذاري ", "هل تريد حذف هذا الزبون   ",
                             QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if message == QMessageBox.Yes:
            id_delete = self.getSelectedStudentId()
            myFunc.delete("DELETE FROM student_profile WHERE id = "+id_delete)
            self.refresh() 
        else:
            return              
                
    def getSelectedStudentId(self):
        return self.table_student.item(self.getSelectedRowIdSudent(),0).text()             
                
                
    def getSelectedRowIdSudent(self):
        return self.table_student.currentRow()   

    def recherche_student(self):        
        search=self.lineEdit_rech.text() 
 
        sql="select * from student_profile Where fname LIKE ?"        
        result=myFunc.find2(sql, [search +"%"]) 
        self.table_student.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.table_student.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table_student.setItem(row_number, column_number, QTableWidgetItem(str(data)))
#        cnn.close()
                
  
    def SelectRowV(self):

        self.table_student.clearSelection()

  
    # def show_ordonnance(self): 

    #     self.open = ordonnance_sqlite_POO.My_ordonnance()
    #     self.open.show()
        
    def genererPDF(self): 
        id_update = str(self.getSelectedStudentId())
        print(id_update)
        r_set = myFunc.select("""SELECT * from student_profile WHERE id="""+id_update)

        # my_conn = sqlite3.connect('student_blob1.db') # connect to Database
        my_path='C:/allFiles/my_pdf62.pdf' # file name
        # r_set=my_conn.execute('SELECT * from student_profile WHERE id=44');
        
        # my_image='images/m2.jpg' # Path of the image
        for row in r_set:
             
        
            # image = Image.open(io.BytesIO(row[4]))
            # io_img = ImageReader(image) # read image
            c = canvas.Canvas(my_path,pagesize=(400,300)) # width and hight
            c.translate(inch,inch)
            
            
        # define a large font
            c.setFont("Helvetica", 14)
        # choose some colors
            c.setStrokeColorRGB(0.1,0.8,0.1)
            c.setFillColorRGB(0,0,1) # font colour
            c.drawImage('D:/VsCode_python/1_Projet_OK/Carte_sqliteSimple_pdf_ok/logoReport11.png',-0.9*inch,2.6*inch) #change path
            #####
            c.rotate(35) # Angle of water mark 
            c.setFillColorCMYK(0,0,0,0.08) # font colour
            c.setFont("Helvetica", 80) # font family and size 
            c.drawString(-1.1*inch, -0.5*inch, "BARIKA") # watermarking
            c.rotate(-35)# restore the angle 
            #####
            c.setFillColorRGB(1,0,0) # font colour
            c.setFont("Helvetica", 16) # font family and size 
            c.drawRightString(1.7*inch,2.3*inch,'Identity Card') # Label 
            c.setFillColorRGB(0,0,0)
            c.setFont("Helvetica", 12)
            c.drawRightString(0.3*inch,1.7*inch,'ID:')
            c.drawRightString(0.3*inch,1.3*inch,'FName:')
            c.drawRightString(0.3*inch,0.9*inch,'LName:')
            c.drawRightString(0.3*inch,0.5*inch,'Date:')
            c.drawRightString(0.3*inch,0.1*inch,'Gender:')
            c.drawRightString(0.3*inch,-0.3*inch,'Adress:')
            c.drawRightString(4.0*inch,-0.5*inch,'Signature')
         	#### Draw line and copyright information at the bottom part ###
            c.line(-1.1,-0.7*inch,5*inch,-0.7*inch)
            c.setFont("Helvetica",10)
            c.setFillColorRGB(1,0,0) # font colour
            c.drawString(0, -0.9*inch, u"\u00A9"+" milsbarika.com")
        
            
            c.drawString(0.5*inch,1.7*inch,str(row[1])) # id to String
            c.drawString(0.5*inch,1.3*inch,row[2])   # Name  
            c.drawString(0.5*inch,0.9*inch,row[3])    
            c.drawString(0.5*inch,0.5*inch,row[4]) 
            c.drawString(0.5*inch,0.1*inch,row[5])
            c.drawString(0.5*inch,-0.3*inch,row[6])
            my_image=str(row[-1])
            # c.drawImage(io_img,2*inch,0.7*inch) # Add image
            # c.drawImage(my_image,2.2*inch,0.7*inch, width=60, height=80) # Place Image 
            c.drawImage(my_image,2.2*inch,0.7*inch, width=60, height=80) # Place Image 
        
            c.showPage() # saves current page
            c.save() # save and close
                
 #*************************************FIN****************************************          
        
    def maFenetre(self):            
        self.setFixedSize(850,621)
        self.setWindowIcon(QIcon('chat.png'))     


def main():            
    app = QApplication(sys.argv)
    window = MyProject()
    # window.ord_medic=uic.loadUi("ord_medic.ui")
    # connection=get_sql_connection()
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()
        

