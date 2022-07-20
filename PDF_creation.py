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
    pdf.set_font("Arial", size= 13)
    pdf.cell(200, 10,  txt= f"ID : {row[0]}", ln= 3, align= 'L')
    pdf.cell(200, 10,  txt= f"BSSID : {row[1]}", ln= 4, align= 'L')
    pdf.cell(200, 10,  txt= f"ESSID : {row[2]}", ln= 5, align= 'L')
    pdf.cell(200, 10,  txt= f"Agente SIFI : {row[3]}", ln= 6, align= 'L')
    pdf.cell(200, 10,  txt= f"El handshake capturado es : {row[4]}", ln= 7, align= 'L')
    pdf.cell(200, 10,  txt= f"Contraseña del AP : {row[5]}", ln= 8, align= 'L')
    pdf.cell(200, 10,  txt= f"Tipo de test realizado: {row[6]}", ln= 9, align= 'L')
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
    if row[4] != "" and row[5] is not None:
        pdf.set_font("Arial", size= 16)
        pdf.cell(125)
        pdf.cell(200, 10,  txt= "Sifi Score: ", ln= 24, align= 'L')
        pdf.set_font("Arial", size= 13)
        pdf.cell(-125)
        pdf.cell(200, 10,  txt= "Segun el assesment de la red, la puntuacion asignada es: ", ln= 25, align= 'L')
        pdf.cell(200, 10,  txt= "Sifi Score: Vulnerable. La red pudo ser vulnerada en al menos dos ambitos. ", ln= 26, align= 'L')
        pdf.set_font("Arial", size= 16)
        pdf.cell(110)
        pdf.cell(200, 10,  txt= "RECOMENDACIONES", ln= 24, align= 'L')
        pdf.set_font("Arial", size= 13)
        pdf.cell(-110)
        pdf.cell(200, 10, txt= "A parte de haber capturado el 4-full way handshake, se pudo hacer un crack de la contraseña", ln= 13, align= 'L')
        pdf.cell(200, 10,  txt= "Segun el libro CWSP en su capitulo 9.1.8 se recomienda actualizar a una solución de autenticación 802.1X/EAP usando autenticación ", ln= 14, align= 'L')
        pdf.cell(200, 1,  txt= "tunelada.", ln= 15, align= 'L')
        pdf.set_font("Arial", size= 16)
        pdf.cell(110)
        pdf.cell(200, 10,  txt= "Mejores practicas a tomar", ln= 24, align= 'L')
        pdf.set_font("Arial", size= 13)
        pdf.cell(-110)
        pdf.cell(200, 10,  txt= "- Política corporativa: Un apéndice adicional a las recomendaciones de seguridad podrían ser las recomendaciones de políticas WLAN ", ln= 19, align= 'L')
        pdf.cell(200, 1,  txt= "corporativas. El auditor puede ayudar al cliente a redactar una política de seguridad de la red inalámbrica si aún no tiene una.", ln= 20, align= 'L')
        pdf.ln(2)
        pdf.cell(200, 10,  txt= "- Seguridad física: La instalación de unidades de cerramiento para proteger contra el robo y el acceso físico no autorizado a los puntos", ln= 21, align= 'L')
        pdf.cell(200, 1,  txt= "de acceso puede ser una recomendación. Estas también se utilizan a menudo con fines estéticos. ", ln= 22, align= 'L')
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
        if any((c in chars) for c in row[5]):
            # Password meets requirements
            # Print message
            pass
            
        else:
            
            pdf.cell(200, 10, txt = "Su contraseña no tiene caracteres especiales por lo tanto presentamos tecnicas de se deben tener en cuenta: ", ln=23, align='L')
            # pdf.cell(200,1, txt= "deben tener en cuenta" , ln= 25, align= 'L')
            
        if len(row[5]) > 13:
           pdf.cell(200,10, txt= "La contraseña posee la longitud recomendada")
            
        else:
            pdf.cell(200, 10, txt = "Su contraseña no posee la longitud recomendada, por lo tanto presentamos tecnicas de se deben tener en cuenta", ln=23, align='L')
        
        if any((c in chars) for c in row[5]) and len(row[5]) > 13:
            pdf.cell(200, 100, txt= " La contraseña tiene la longitud recomendada e incluye caracteres especiales")
        else:
            pdf.cell(200, 10,  txt= "Segun la guia de PCI-DSS en la seccion 4.4 se plantean las siguientes recomendaciones para mas seguridad:", ln= 22, align= 'L')
            pdf.ln(5)
            pdf.cell(200, 10, txt = "- Se debe cambiar siempre los valores predeterminados que fueron proporcionados por el proveedor, esto incluye las contraseñas y las ", ln=23, align='L')
            pdf.cell(200, 1, txt= "configuraciones como tambien deshabilitar las cuentas innecesarias antes de instalar su propio sistema de red.  ", ln= 24, align='L')
            pdf.ln(2)
            pdf.cell(200, 10, txt= "- Eliminar o deshabilitar cuentas de usuarios inactivas dentro de 90 dias", ln= 25, align='L')
            pdf.cell(200, 10, txt= "- Limitar los intentos de acceso repetidos bloqueando el ID de usuario despues de mas de 5 intentos y establecer una duracion de", ln= 26, align='L')
            pdf.cell(200, 1, txt= "bloqueo en un minimo de 30 minutos o hasta que el administrador habilite el ID del usuario.", ln=27, align='L')
            pdf.ln(2)
            pdf.cell(200, 10, txt= "- Se debe cambiar la contraseña de los usuarios una vez cada 90 dias y no permitir que se repita las ultimas cuatro contraseñas.", ln= 28, align='L')
            pdf.ln(2)
            pdf.cell(200, 10, txt= "- Establecer contraseñas para el primer uso y al restablecerlas a un valor unico para cada usuario y cambiar inmediatamente despues", ln= 29, align='L')
            pdf.cell(200, 1, txt= " del primer uso. Hacer cumplir la autenticacion multifactor ", ln= 30, align='L')
            
        #Vulnerable	2 pentesting con resultados negativos de cualquier función de la plataforma.

    elif row[4] != "" and row[5] is None:
        pdf.set_font("Arial", size= 16)
        pdf.cell(125)
        pdf.cell(200, 10,  txt= "Sifi Score: ", ln= 24, align= 'L')
        pdf.set_font("Arial", size= 13)
        pdf.cell(-125)
        pdf.cell(200, 10,  txt= "Segun el assesment de la red, la puntuacion asignada es: ", ln= 25, align= 'L')
        pdf.cell(200, 10,  txt= "Sifi Score: Estable. La red pudo ser vulnerada en al menos un ambito.", ln= 26, align= 'L')
        pdf.set_font("Arial", size= 16)
        pdf.cell(110)
        pdf.cell(200, 10,  txt= "RECOMENDACIONES", ln= 24, align= 'L')
        pdf.set_font("Arial", size= 13)
        pdf.cell(-110)
        pdf.cell(200, 10, txt= "Se ha capturado el 4 way handshake. Lo que significa que se ha podido hacer una deautenticacion del cliente conectado al Access Point", ln= 13, align= 'L')
        pdf.cell(200, 10,  txt= "Segun el libro CWSP en su capitulo 9.1.8 se recomienda actualizar a una solución de autenticación 802.1X/EAP usando autenticación ", ln= 14, align= 'L')
        pdf.cell(200, 1,  txt= "tunelada.", ln= 15, align= 'L')
        pdf.set_font("Arial", size= 16)
        pdf.cell(110)
        pdf.cell(200, 10,  txt= "Mejores practicas a tomar", ln= 24, align= 'L')
        pdf.set_font("Arial", size= 13)
        pdf.cell(-110)
        pdf.cell(200, 10,  txt= "- Política corporativa: Un apéndice adicional a las recomendaciones de seguridad podrían ser las recomendaciones de políticas WLAN ", ln= 19, align= 'L')
        pdf.cell(200, 1,  txt= "corporativas. El auditor puede ayudar al cliente a redactar una política de seguridad de la red inalámbrica si aún no tiene una.", ln= 20, align= 'L')
        pdf.ln(2)
        pdf.cell(200, 10,  txt= "- Seguridad física: La instalación de unidades de cerramiento para proteger contra el robo y el acceso físico no autorizado a los puntos", ln= 21, align= 'L')
        pdf.cell(200, 1,  txt= "de acceso puede ser una recomendación. Estas también se utilizan a menudo con fines estéticos. ", ln= 22, align= 'L')

    elif row[4] != "" and row[5] is None:
        pdf.set_font("Arial", size= 16)
        pdf.cell(125)
        pdf.cell(200, 10,  txt= "Sifi Score: ", ln= 24, align= 'L')
        pdf.set_font("Arial", size= 13)
        pdf.cell(-125)
        pdf.cell(200, 10,  txt= "Segun el assesment de la red, la puntuacion asignada es: ", ln= 25, align= 'L')
        pdf.cell(200, 10,  txt= "Sifi Score: Seguro. Todos los pentest poseen resultados positivos y con ninguna vulnerabilidad detectada.", ln= 26, align= 'L')

        # pdf.cell(200, 10, txt= "No se ha capturado el handshake", ln= 11, align= 'L')

    #save the pdf with the .pdf extension
    pdf.output("SiFi_{}_{}.pdf".format(Assesment_ID, date))
    
pdfGenerator("Pucmm")