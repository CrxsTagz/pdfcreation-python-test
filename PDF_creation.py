from gettext import lngettext
from msilib.schema import Font
from tkinter import font
import fpdf
from fpdf import FPDF
import mysql.connector
from mysql.connector import Error
from datetime import datetime

# This function does not have a return, it only generates the PDF assesment.
#customerName = 'PUCMM'

def pdfGenerator(customerName):
     # WSSid = int(WSSid)
     customerName = customerName
     # save FPDF class into a variable pdf
     pdf = FPDF('P', 'mm', (300, 150))
     date = datetime. now(). strftime("%Y_%m_%d-%I-%M-%S_%p")

     # Add page
     pdf.add_page()

     # set new margins equation
     epw = pdf.w - pdf.l_margin - pdf.r_margin
     eph = pdf.h - pdf.t_margin - pdf.b_margin

     # Draw new margins.
     pdf.rect(pdf.l_margin, pdf.t_margin, w=epw, h=eph)   

     # add format
     # logo
     pdf.image("sifi-icon.jpg", 0, 0, 20)
     # font arial bold 15pts
     pdf.set_font('Arial', 'B', 15)
     # move to the right
     pdf.cell(125)
     # Title
     pdf.cell(30, 10, 'SIFI WSS', 1, 0, 'C')
     # Line break
     pdf.ln(20)

     Assesment_ID = 0

     try:
         connection = mysql.connector.connect(host='localhost',
                                          database='sifi',
                                          user='root',
                                          password='sifi')
         cursor = connection.cursor()
         sql_select_Query = "SELECT * FROM wss"

         cursor.execute(sql_select_Query)
         # get all records
         records = cursor.fetchall()
         print("Total number of rows in table: ", cursor.rowcount)
         Assesment_ID = '{:0>5}'.format(int(records[0][0]))
         print("\nPrinting each row")
         for row in records:
             print("Id = ", row[0], )
             print("bssid = ", row[1])
             print("essid  = ", row[2])
             print("sifiagent  = ", row[3])
             print("handshake  = ", row[4])
             print("cracked_password  = ", row[5])
             print("test_type  = ", row[6], "\n")
             # print("Customer Name  = ", row[7], "\n")
             if row[4] is not None:
                 print("Se ha capturado el handshake")
             if row[5] is not None:
                 print("Se ha capturado la contraseña")

     except Error as e:
         print("Error while connecting to MySQL", e)
     finally:
         if connection.is_connected():
             cursor.close()
             connection.close()
         print("MySQL connection is closed")

     #create cells 
     pdf.set_font("Arial", 'B', size= 16)
     pdf.cell(200,10, txt= "Records capturados del Assessment:", align= 'L')
     pdf.ln(10)
     pdf.set_font("Arial", size= 13)
     pdf.cell(200, 10,  txt= f"- ID : {row[0]}", ln= 3, align= 'L')
     pdf.cell(200, 10,  txt= f"- BSSID : {row[1]}", ln= 4, align= 'L')
     pdf.cell(200, 10,  txt= f"- ESSID : {row[2]}", ln= 5, align= 'L')
     pdf.cell(200, 10,  txt= f"- Agente SIFI : {row[3]}", ln= 6, align= 'L')
     pdf.cell(200, 10,  txt= f"- El handshake capturado es : {row[4]}", ln= 7, align= 'L')
     pdf.cell(200, 10,  txt= f"- Contraseña del AP : {row[5]}", ln= 8, align= 'L')
     pdf.cell(200, 10,  txt= f"- Tipo de test realizado: {row[6]}", ln= 9, align= 'L')
     #pdf.cell(200, 10,  txt= f"Empresa/Cliente: {row[7]}", ln= 10, align= 'L')

     if row[4] is not None:
         pdf.add_page()
         epw = pdf.w - pdf.l_margin - pdf.r_margin
         eph = pdf.h - pdf.t_margin - pdf.b_margin

         # Draw new margins.
         pdf.rect(pdf.l_margin, pdf.t_margin, w=epw, h=eph)   

         #add format
         #logo
         pdf.image("cwsp_c.png", 0, 0, 20)
         pdf.set_font("Arial", size= 16)
         # pdf.ln(10)

     #ESTADO DE LA RED, SIFI WSS SCORE
     #Estable	Al menos 1 resultado negativo de cualquiera de las funciones principales
     if row[4] != "" and row[5] != "":

         pdf.set_font("Arial", 'B', size= 16)
         pdf.cell(120)
         pdf.cell(200, 10,  txt= "Valoración ", ln= 11, align= 'L')
         pdf.cell(200, 5,  txt= "SIFI WSS", ln= 12, align= 'L')

         #TABLE CREATION

         # Effective page width, or just epw
         epw = pdf.w - 2*pdf.l_margin
         
         # Set column width to 1/4 of effective page width to distribute content 
         # evenly across table and page
         col_width = epw/4
         
         # Since we do not need to draw lines anymore, there is no need to separate
         # headers from data matrix.
        
         wssdata = [['Estado', 'Descripcion'],
         ['Seguro', 'Todos los pentest con resultados positivos y ninguna vulnerabilidad detectada'],
         ['Estable', 'Al menos un resultado negativo en cualquiera de las funciones principales'],
         ['Vulnerable', 'Al menos dos resultados negativos en cualquiera de las funciones principales'],
         ['Critico', 'Todos los pentest con resultados negativos en las funciones principales']
         ]
         
         # Document title centered, 'B'old, 14 pt
         pdf.cell(115)
         
         pdf.cell(-115)
         pdf.set_font('Times','',12.0) 
         pdf.ln(2)

         # Text height is the same as current font size
         th = pdf.font_size
         
         for row in wssdata:
             for datum in row:
                 # Enter data in colums
                 # Notice the use of the function str to coerce any input to the 
                 # string type. This is needed
                 # since pyFPDF expects a string, not a number.
                 pdf.cell(1.9*col_width, th, str(datum), border=1)
         
             pdf.ln(th)
         
         # Line break equivalent to 4 lines
         

         pdf.cell(120)
         pdf.set_font("Arial", 'BI', size= 14)
         pdf.cell(-120)
         pdf.set_font("Arial", 'BI', size= 13)
         
         pdf.set_text_color(0,0,0)
         pdf.cell(200, 10,  txt= "Según la tabla de valoración SIFI, el estado de seguridad es:", ln= 13, align= 'L')

         #text colour orange
         pdf.set_text_color(255,127,0)
         pdf.cell(200, 10,  txt= "Estable. La red pudo ser vulnerada en al menos un ámbito.", ln= 13, align= 'L')

        #text colour black
         pdf.set_text_color(0,0,0)

         pdf.set_font("Arial", 'B', size= 16)
         pdf.cell(110)
         pdf.cell(200, 10,  txt= "Recomendaciones", ln= 14, align= 'L')
         pdf.set_font("Arial", size= 13)
         pdf.cell(-110)
         pdf.cell(200, 10, txt= "Se ha capturado el 4 way handshake. Lo que significa que se ha podido hacer una deautenticacion del cliente conectado al Access Point", ln= 15, align= 'L')
         pdf.cell(200, 10,  txt= "Segun el libro CWSP en su capitulo 9.1.8 se recomienda actualizar a una solución de autenticación 802.1X/EAP usando autenticación ", ln= 16, align= 'L')
         pdf.cell(200, 1,  txt= "tunelada.", ln= 15, align= 'L')


         
         pdf.add_page()

         # Define margins
         epw = pdf.w - pdf.l_margin - pdf.r_margin
         eph = pdf.h - pdf.t_margin - pdf.b_margin

         # Draw new margins.
         pdf.rect(pdf.l_margin, pdf.t_margin, w=epw, h=eph)

         pdf.set_font("Arial", size= 16)
         pdf.cell(100)
         pdf.cell(200, 10,  txt= "Directrices de contraseñas PCI-DSS", ln= 21, align= 'L')
         pdf.set_font("Arial", size= 13)
         pdf.cell(-100)

         #SETTING SPECIAL CHARACTERS TO PRESENT THE PCI-DSS handle
         chars = set('!#$%&()*+,-./:;<=>?@[\]^_`{|}~')
         for row in records:
            if any((c in chars) for c in row[5]):
             pass

            else:

             pdf.cell(200, 10, txt = "Su contraseña no tiene caracteres especiales por lo tanto presentamos tecnicas de se deben tener en cuenta: ", ln=23, align='J')
             # pdf.cell(200,1, txt= "deben tener en cuenta" , ln= 25, align= 'L')

            if len(row[5]) > 13:
                pass

            else:
             pdf.cell(200, 10, txt = "Su contraseña no posee la longitud recomendada, por lo tanto presentamos tecnicas de se deben tener en cuenta: ", ln=23, align='J')

            if any((c in chars) for c in row[5]) and len(row[5]) > 13:
             pdf.cell(200, 10, txt= " La contraseña tiene la longitud recomendada e incluye caracteres especiales, la misma tiene un nivel de seguridad mucho mayor ")
            else:
             pdf.cell(200, 10, txt = "- Se debe cambiar siempre los valores predeterminados que fueron proporcionados por el proveedor, esto incluye las contraseñas y las ", ln=23, align='J')
             pdf.cell(200, 1, txt= "configuraciones como tambien deshabilitar las cuentas innecesarias antes de instalar su propio sistema de red.  ", ln= 24, align='J')
             pdf.ln(5)
             pdf.cell(200, 10, txt= "- La contraseña debe tener al menos una longitud de 13 caracteres para que sea menos predecible.", ln=25, align="J")
             pdf.ln(2)
             pdf.cell(200, 10, txt= "- Eliminar o deshabilitar cuentas de usuarios inactivas dentro de 90 dias", ln= 26, align='J')
             pdf.cell(200, 10, txt= "- Limitar los intentos de acceso repetidos bloqueando el ID de usuario despues de mas de 5 intentos y establecer una duracion de", ln= 27, align='L')
             pdf.cell(200, 1, txt= "bloqueo en un minimo de 30 minutos o hasta que el administrador habilite el ID del usuario.", ln=28, align='L')
             pdf.ln(5)
             pdf.cell(200, 10, txt= "- Se debe cambiar la contraseña de los usuarios una vez cada 90 dias y no permitir que se repita las ultimas cuatro contraseñas.", ln= 29, align='L')
             pdf.ln(2)
             pdf.cell(200, 10, txt= "- Establecer contraseñas para el primer uso y al restablecerlas a un valor unico para cada usuario y cambiar inmediatamente despues", ln= 30, align='L')
             pdf.cell(200, 1,  txt= " del primer uso. Hacer cumplir la autenticacion multifactor ", ln= 31, align='L')

         #Vulnerable	2 pentesting con resultados negativos de cualquier función de la plataforma.
    
     elif row[4] != "" and row[5] == "":
         pdf.set_font("Arial", 'B', size= 16)
         pdf.cell(125)
         pdf.cell(200, 10,  txt= "Valoracion: ", ln= 24, align= 'L')
         pdf.cell(200, 5,  txt= "SIFI WSS", ln= 12, align= 'L')

         #TABLE CREATION

         # Effective page width, or just epw
         epw = pdf.w - 2*pdf.l_margin
         
         # Set column width to 1/4 of effective page width to distribute content 
         # evenly across table and page
         col_width = epw/4
         
         # Since we do not need to draw lines anymore, there is no need to separate
         # headers from data matrix.
        
         wssdata = [['Estado', 'Descripcion'],
         ['Seguro', 'Todos los pentest con resultados positivos y ninguna vulnerabilidad detectada'],
         ['Estable', 'Al menos un resultado negativo en cualquiera de las funciones principales'],
         ['Vulnerable', 'Al menos dos resultados negativos en cualquiera de las funciones principales'],
         ['Critico', 'Todos los pentest con resultados negativos en las funciones principales']
         ]
         
         # Document title centered, 'B'old, 14 pt
         pdf.cell(115)
         
         pdf.cell(-115)
         pdf.set_font('Times','',12.0) 
         pdf.ln(2)

         # Text height is the same as current font size
         th = pdf.font_size
         
         for row in wssdata:
             for datum in row:
                 # Enter data in colums
                 # Notice the use of the function str to coerce any input to the 
                 # string type. This is needed
                 # since pyFPDF expects a string, not a number.
                 pdf.cell(1.9*col_width, th, str(datum), border=1)
         
             pdf.ln(th)
         
         # Line break equivalent to 4 lines
         

         pdf.cell(120)
         pdf.set_font("Arial", 'BI', size= 14)
         pdf.cell(-120)
         pdf.set_font("Arial", 'BI', size= 13)
         
         pdf.set_text_color(0,0,0)
         pdf.cell(200, 10,  txt= "Según la tabla de valoración SIFI, el estado de seguridad es:", ln= 13, align= 'L')

         #text colour orange
         pdf.set_text_color(255,127,0)
         pdf.cell(200, 10,  txt= "Estable. La red pudo ser vulnerada en al menos un ámbito.", ln= 13, align= 'L')

        #text colour black
         pdf.set_text_color(0,0,0)

         pdf.set_font("Arial", 'B', size= 16)
         pdf.cell(110)
         pdf.cell(200, 10,  txt= "Recomendaciones", ln= 14, align= 'L')
         pdf.set_font("Arial", size= 13)
         pdf.cell(-110)
         pdf.cell(200, 10, txt= "Se ha capturado el 4 way handshake. Lo que significa que se ha podido hacer una deautenticacion del cliente conectado al Access Point", ln= 15, align= 'L')
         pdf.cell(200, 10,  txt= "Segun el libro CWSP en su capitulo 9.1.8 se recomienda actualizar a una solución de autenticación 802.1X/EAP usando autenticación ", ln= 16, align= 'L')
         pdf.cell(200, 1,  txt= "tunelada.", ln= 15, align= 'L')


    
     elif row[4] == "" and row[5] == "":
         pdf.set_font("Arial", 'BI', size= 16)
         pdf.cell(125)
         pdf.cell(200, 10,  txt= "Valoracion: ", ln= 24, align= 'L')
         pdf.cell(200, 5,  txt= "SIFI WSS", ln= 12, align= 'L')

         #TABLE CREATION

         # Effective page width, or just epw
         epw = pdf.w - 2*pdf.l_margin
         
         # Set column width to 1/4 of effective page width to distribute content 
         # evenly across table and page
         col_width = epw/4
         
         # Since we do not need to draw lines anymore, there is no need to separate
         # headers from data matrix.
        
         wssdata = [['Estado', 'Descripcion'],
         ['Seguro', 'Todos los pentest con resultados positivos y ninguna vulnerabilidad detectada'],
         ['Estable', 'Al menos un resultado negativo en cualquiera de las funciones principales'],
         ['Vulnerable', 'Al menos dos resultados negativos en cualquiera de las funciones principales'],
         ['Critico', 'Todos los pentest con resultados negativos en las funciones principales']
         ]
         
         # Document title centered, 'B'old, 14 pt
         pdf.cell(115)
         
         pdf.cell(-115)
         pdf.set_font('Times','',12.0) 
         pdf.ln(2)

         # Text height is the same as current font size
         th = pdf.font_size
         
         for row in wssdata:
             for datum in row:
                 # Enter data in colums
                 # Notice the use of the function str to coerce any input to the 
                 # string type. This is needed
                 # since pyFPDF expects a string, not a number.
                 pdf.cell(1.9*col_width, th, str(datum), border=1)
         
             pdf.ln(th)
         
         # Line break equivalent to 4 lines
         

         pdf.cell(120)
         pdf.set_font("Arial", 'BI', size= 14)
         pdf.cell(-120)
         pdf.set_font("Arial", 'BI', size= 13)
         
         pdf.set_text_color(0,0,0)
         pdf.cell(200, 10,  txt= "Según la tabla de valoración SIFI, el estado de seguridad es:", ln= 13, align= 'L')

         #text colour orange
         pdf.set_text_color(0,128,0)
         pdf.cell(200, 10,  txt= "Seguro. Todos los pentest con resultados positivos y ninguna vulnerabilidad detectada.", ln= 13, align= 'L')

     pdf.set_text_color(0,0,0)
         # pdf.cell(200, 10, txt= "No se ha capturado el handshake", ln= 11, align= 'L')
     pdf.add_page()

     # Define margins
     epw = pdf.w - pdf.l_margin - pdf.r_margin
     eph = pdf.h - pdf.t_margin - pdf.b_margin
 
     # Draw new margins.
     pdf.rect(pdf.l_margin, pdf.t_margin, w=epw, h=eph)
    

     pdf.set_font("Arial", 'B', size= 16)
     pdf.cell(110)
     pdf.cell(200, 10,  txt= "Politicas de seguridad (Generales)", ln= 24, align= 'L')
     pdf.set_font("Arial", 'B', size= 13)
     pdf.cell(-110)
     pdf.cell(200, 10,  txt= "- Política corporativa:", ln= 19, align= 'L')
     pdf.set_font("Arial", size= 13)
     pdf.cell(200, 1, txt= "Un apéndice adicional a las recomendaciones de seguridad podrían ser las recomendaciones de políticas WLAN corporativas.", ln= 20, align='L')
     pdf.cell(200, 10, txt= "El auditor puede ayudar al cliente a redactar una política de seguridad de la red inalámbrica si aún no tiene una.", ln= 20, align= 'L')
     pdf.ln(2)
     pdf.set_font("Arial", 'B', size= 13)
     pdf.cell(200, 10,  txt= "- Seguridad física:", ln= 21, align= 'L')
     pdf.set_font("Arial", size= 13)
     pdf.cell(200, 1, txt= "La instalación de unidades de cerramiento para proteger contra el robo y el acceso físico no autorizado a los puntos de acceso puede ", ln= 22, align= 'L')
     pdf.cell(200, 10,  txt= "ser una recomendación. Estas también se utilizan a menudo con fines estéticos. ", ln= 22, align= 'L')
     pdf.ln(2)
     pdf.set_font("Arial", 'B', size= 13)
     pdf.cell(200, 10, txt= "- Declaracion de autoridad:", ln = 22, align= 'L')
     pdf.set_font("Arial", size= 13)
     pdf.cell(200, 1, txt= "Define quien implemento la politica WLAN y la direccion ejecutiva que respalda la politica", ln = 22, align= 'L')
     pdf.ln(2)
     pdf.set_font("Arial", 'B', size= 13)
     pdf.cell(200, 10, txt= "- Audiencia aplicable:", ln= 27, align= 'L')
     pdf.set_font("Arial", size= 13)
     pdf.cell(200, 1, txt= "Define el publico al que se le aplica la politica, ya sea, empleados, visitantes o contratistas", ln = 22, align= 'L')
     pdf.ln(2)
     pdf.set_font("Arial", 'B', size= 13)
     pdf.cell(200, 10, txt= "- Evaluacion de riesgos y analisis de amenazas:", ln= 27, align= 'L')
     pdf.set_font("Arial", size= 13)
     pdf.cell(200, 1, txt= "Define los posibles riesgos y amenazas de seguridad inalámbrica y cuál será el impacto financiero en la empresa si se produce un", ln = 22, align= 'L')
     pdf.cell(200, 10, txt= "ataque con éxito." , ln= 22, align= 'L')
     # pdf.add_page()

     #     # Define margins
     # epw = pdf.w - pdf.l_margin - pdf.r_margin
     # eph = pdf.h - pdf.t_margin - pdf.b_margin

     # # Draw new margins.
     # pdf.rect(pdf.l_margin, pdf.t_margin, w=epw, h=eph)
     # pdf.cell("[1] Wireless Special Interest Group, “Overview of the PCI DSS wireless guideline information supplement,” PCI DSS Wireless Guideline, Jul-2009.  [Online]. Available: ")
     # pdf.cell(" https://www.pcisecuritystandards.org/documents/pci_dss_wireless_guideline_info_sup.pdf. [Accessed: 23-Jul-2022]. ")
   
   
   #Add page
     pdf.add_page()

     # set new margins equation
     epw = pdf.w - pdf.l_margin - pdf.r_margin
     eph = pdf.h - pdf.t_margin - pdf.b_margin

     # Draw new margins.
     pdf.rect(pdf.l_margin, pdf.t_margin, w=epw, h=eph)
     try:
         connection = mysql.connector.connect(host='100.64.0.1',
                                          database='sifi',
                                          user='root',
                                          password='sifi')
         cursor = connection.cursor()
         sql_select_Query = "SELECT * FROM wsecurity"

         cursor.execute(sql_select_Query)
         # get all records
         records = cursor.fetchall()
         print("Total number of rows in table: ", cursor.rowcount)
         Assesment_ID = '{:0>5}'.format(int(records[0][0]))
         print("\nPrinting each row")
         for row in records:
             print("idwsecurity = ", row[0], )
             print("bssid = ", row[1])
             print("channel  = ", row[2])
             print("privacy  = ", row[3])
             print("cipher  = ", row[4])
             print("authentication  = ", row[5])
             print("sifiagent  = ", row[6], "\n")

     except Error as e:
         print("Error while connecting to MySQL", e)
     finally:
         if connection.is_connected():
             cursor.close()
             connection.close()
         print("MySQL connection is closed")

     #create cells 
     pdf.set_font("Arial", 'B', size= 16)
     pdf.ln(10)
     pdf.cell(200,10, txt= "Advanced Wireless Security Information:", align= 'L')
     pdf.ln(10)
     pdf.set_font("Arial", size= 13)
     pdf.cell(200, 10,  txt= f"- Channel : {row[2]}", ln= 5, align= 'L')
     pdf.cell(200, 10,  txt= f"- Privacy : {row[3]}", ln= 6, align= 'L')
     pdf.cell(200, 10,  txt= f"- Cipher : {row[4]}", ln= 7, align= 'L')
     pdf.cell(200, 10,  txt= f"- Authentication : {row[5]}", ln= 8, align= 'L')
     
     if row[3] == "WPA2" and row[4] == "CCMP" and row[5] == "PSK":
         pdf.add_page()
            # set new margins equation
         epw = pdf.w - pdf.l_margin - pdf.r_margin
         eph = pdf.h - pdf.t_margin - pdf.b_margin

     # Draw new margins.
         pdf.rect(pdf.l_margin, pdf.t_margin, w=epw, h=eph)

         pdf.set_font("Arial", 'B', size= 16)
         pdf.cell(115)
            #dividir en secciones
         pdf.cell(200, 10, txt= "Recomendaciones para AWSI:")
         pdf.cell(-115)
         pdf.ln(10)
         if row[5] == "PSK":
            pdf.set_font("Arial", size= 13)
            pdf.cell(200, 10, txt="Best practices para PSK:", ln= 10, align='L')
            pdf.cell(200, 5, txt="- Se debera cambiar el PSK por defecto a una nueva", ln = 11, align='L')
            pdf.cell(200, 10, txt="- Generar un PSK nuevo/diferente para cada tunel VPN", ln = 11, align='L')
            pdf.cell(200, 10, txt="- Usar un generador de contraseñas aleatorias", ln = 11, align='L')
            pdf.cell(200, 10, txt="- Generar un PSK de 20 o mas caracteres para evitar ataques de fuerza bruta", ln = 11, align='L')
            pdf.cell(200, 10, txt="- Usar una combinacion de caracteres especiales y letras mayusculas en la generacion del PSK", ln = 11, align='L')
            pdf.cell(200, 10, txt="- No guardar el PSK en ningun otro lugar", ln = 11, align='L')
         if row[3] == "WPA2":
            pdf.cell(200,10, txt= "Hola")
        
        
         print ("Hola")

     
     #save the pdf with the .pdf extension
     pdf.output("SiFi_{}_{}.pdf".format(Assesment_ID, date))

pdfGenerator("Pucmm")