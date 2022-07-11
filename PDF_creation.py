from random import random
import string
from turtle import color
from fpdf import FPDF
import mysql.connector
from mysql.connector import Error


   #save FPDF class into a variable pdf
pdf = FPDF('P', 'mm', (300, 150))

#Add page
pdf.add_page()

epw = pdf.w - pdf.l_margin - pdf.r_margin
eph = pdf.h - pdf.t_margin - pdf.b_margin

# Draw new margins.
pdf.rect(pdf.l_margin, pdf.t_margin, w=epw, h=eph)   

#add format
#logo
pdf.image("sifi-icon.jpg", 0, 0, 20)
#font arial bold 15pts
pdf.set_font('Arial', 'B', 15)
#move to the right
pdf.cell(125)
# Title
pdf.cell(30, 10, 'SIFI WSS', 1, 0, 'C')
# Line break
pdf.ln(20)

try:
        connection = mysql.connector.connect(host='localhost',
                                         database='sifi',
                                         user='root',
                                         password='sifi')

        sql_select_Query = "select * from wss"
        cursor = connection.cursor()
        cursor.execute(sql_select_Query)
    # get all records
        records = cursor.fetchall()
        print("Total number of rows in table: ", cursor.rowcount)

        print("\nPrinting each row")
        for row in records:
            print("Id = ", row[0], )
            print("bssid = ", row[1])
            print("essid  = ", row[2])
            print("sifiagent  = ", row[3])
            print("handshake  = ", row[4])
            print("cracked_password  = ", row[5])
            print("test_type  = ", row[6], "\n")
            if row[4] is not None:
                print("Se ha capturado el handshake")
                
except Error as e:
        print("Error while connecting to MySQL", e)
finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
        print("MySQL connection is closed")

  
#create cells 
pdf.set_font("Arial", size= 13)
pdf.cell(200, 10,  txt= f"ID : {row[0]}", ln= 3, align= 'L')
pdf.cell(200, 10,  txt= f"BSSID : {row[1]}", ln= 4, align= 'L')
pdf.cell(200, 10,  txt= f"ESSID : {row[2]}", ln= 5, align= 'L')
pdf.cell(200, 10,  txt= f"Agente SIFI : {row[3]}", ln= 6, align= 'L')
pdf.cell(200, 10,  txt= f"El handshake capturado es : {row[4]}", ln= 7, align= 'L')
pdf.cell(200, 10,  txt= f"Contraseña del AP : {row[5]}", ln= 8, align= 'L')
pdf.cell(200, 10,  txt= f"Tipo de test realizado: {row[6]}", ln= 9, align= 'L')

if row[4] is not None:
    pdf.add_page()
    epw = pdf.w - pdf.l_margin - pdf.r_margin
    eph = pdf.h - pdf.t_margin - pdf.b_margin

# Draw new margins.
    pdf.rect(pdf.l_margin, pdf.t_margin, w=epw, h=eph)   

#add format
#logo
    pdf.image("sifi-icon.jpg", 0, 0, 20)
    pdf.set_font("Arial", size= 16)
    # pdf.ln(10)
    pdf.cell(110)
    pdf.cell(200, 10,  txt= "RECOMENDACIONES", ln= 12, align= 'L')
    pdf.set_font("Arial", size= 13)
    pdf.cell(-110)
    pdf.cell(200, 10, txt= "Se ha capturado el handshake. Lo que significa que se ha podido hacer una deautenticacion del cliente conectado al Access Point", ln= 13, align= 'L')
    pdf.cell(200, 10,  txt= "Se recomienda actualizar a una solución de autenticación 802.1X/EAP usando autenticación tunelada.", ln= 14, align= 'L')

else:
    pdf.cell(200, 10, txt= "No se ha capturado el handshake", ln= 11, align= 'L')
#PDF function
#class pdfcreator():

    # def getpdf(bssid, essid, devIP, ok):
    #     essid = essid
    #     bssid = bssid
    #     devIP = devIP

# def getpdf():

#save the pdf with the .pdf extension
# Go to 1.5 cm from bottom
pdf.set_x(5)
pdf.set_y(0)
# Select Arial italic 8
pdf.set_font('Arial', 'I', 8)
# Print centered page number
pdf.cell(0, 10, 'Page %s' % pdf.page_no(), 0, 0, 'C')
pdf.output("Assesment.pdf")