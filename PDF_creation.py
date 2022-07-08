from random import random
from fpdf import FPDF

#PDF function
#class pdfcreator():

    # def getpdf(bssid, essid, devIP, ok):
    #     essid = essid
    #     bssid = bssid
    #     devIP = devIP

# def getpdf():
#random variables
prueba = random()
#save FPDF class into a variable pdf
pdf = FPDF()

#Add page
pdf.add_page()

# pdf.set_font("Arial", size= 13)

#add format
#logo
pdf.image("sifi-icon.jpg", 0, 0, 20)
#font arial bold 15pts
pdf.set_font('Arial', 'B', 15)
#move to the right
pdf.cell(80)
# Title
pdf.cell(30, 10, 'SIFI WSS', 1, 0, 'C')
# Line break
pdf.ln(20)

#create cells 
pdf.set_font("Arial", size= 13)
pdf.cell(200, 10,  txt= f"tu numero random de hoy es: {prueba}", ln= 2, align= 'L')
# pdf.cell(200, 10,  txt= f"Tu SSID seleccionado es: {essid}", ln= 2, align= 'L')
# pdf.cell(200, 10,  txt= f"La MAC BSSID del AP es: {bssid}", ln= 3, align= 'L')

#save the pdf with the .pdf extension

pdf.output("Prueba.pdf")