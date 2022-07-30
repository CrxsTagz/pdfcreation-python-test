from fpdf import FPDF
import mysql.connector
from mysql.connector import Error
from datetime import datetime
from l2Query import l2pdfGenerator

# This function does not have a return, it only generates the PDF assesment.
#customerName = 'PUCMM'

wssdata = [['State', 'Description'],
         ['Secured', 'All pentests with positive results and no vulnerability detected'],
         ['Stable', 'At least a negative result in any of the principal functions'],
         ['Vulnerable', 'At least two negative results in any of the principal functions'],
         ['Critico', 'All penstests with negative results in any of the principal functions']
         ]

def pdfPrint(pdf, authenticationMode, wirelessPrivacy, cyphering):
    pdf.add_page()
    # set new margins equation
    epw = pdf.w - pdf.l_margin - pdf.r_margin
    eph = pdf.h - pdf.t_margin - pdf.b_margin
    # Draw new margins.
    pdf.rect(pdf.l_margin, pdf.t_margin, w=epw, h=eph)
    pdf.set_font("Arial", 'B', size= 16)
    pdf.cell(115)
    #dividir en secciones
    pdf.cell(200, 10, txt= "Advance Wireless Security Information:")
    pdf.cell(-115)
    pdf.ln(10)
    if authenticationMode == 'PSK':
        pdf.set_font("Arial",'B', size= 14)
        pdf.cell(200, 10, txt="PSKs are not recommended for use in enterprise WLAN deployments. A preshared key (PSK) is a common password or passphrase that is shared between the authenticator and the supplicant. ", ln= 10, align='L')
        pdf.cell(200, 5, txt="The PSK is used for authenticating the wireless client and is the derivative for the encryption keys generated to encrypt the data traffic. The Wi-Fi Alliance defines the use of PSKs in the WPA/WPA2-Personal certifications. Preshared keys are usually used in SOHO environments.", ln = 11, align='L')
        
        pdf.set_font("Arial",'B', size= 14)
        pdf.cell(200, 10, txt="PSK Best practices:", ln= 10, align='L')
        pdf.set_font("Arial", size= 13)
        pdf.cell(200, 5, txt="- The default PSK must be changed to a new one", ln = 11, align='L')
        pdf.cell(200, 10, txt="- Generate a new PSK/for each VPN tunnel", ln = 11, align='L')
        pdf.cell(200, 10, txt="- Usar un generador de contraseñas aleatorias", ln = 11, align='L')
        pdf.cell(200, 10, txt="- Generar un PSK de 20 o mas caracteres para evitar ataques de fuerza bruta", ln = 11, align='L')
        pdf.cell(200, 10, txt="- Usar una combinacion de caracteres especiales y letras mayusculas en la generacion del PSK", ln = 11, align='L')
        pdf.cell(200, 10, txt="- No guardar el PSK en ningun otro lugar", ln = 11, align='L')
    if wirelessPrivacy == 'WPA2':
        pdf.set_font("Arial", 'B', size= 14)
        pdf.cell(200,10, txt= "Best practices para WPA2:", ln = 10, align= 'L')
        pdf.set_font("Arial", size= 13)
        pdf.cell(200,10, txt= "- Si se tiene WPA2 personal se debe actualizar a una version mas reciente o a la solución de autenticación 802.1X/EAP mediante autenticación tunelada. ", ln=10, align= 'L')
        pdf.cell(200, 10, txt= "- Proporcionar un cliente de anti-virus que este en constante ejecucion y actualizado con los ultimos patches", ln= 12, align='L'   )
        pdf.cell(200, 10, txt= "- Tener un firewall en la red que este operacional en todo momento ", ln= 12, align='L' )
        pdf.add_page()
        # set new margins equation
        epw = pdf.w - pdf.l_margin - pdf.r_margin
        eph = pdf.h - pdf.t_margin - pdf.b_margin
        # Draw new margins.
        pdf.rect(pdf.l_margin, pdf.t_margin, w=epw, h=eph)
        pdf.cell(200, 10, txt= "- Tener una autenticacion doble factor", ln= 12, align='L'   )
        pdf.cell(200, 10, txt= "- La red debe ser configurada por el personal correspondiente ", ln= 12, align='L'   )
        if cyphering == 'CCMP':
            pass
        elif cyphering == 'CCMP TKIP':
            pass
        else:
            pass
    elif wirelessPrivacy == 'WPA':
        
        if cyphering == 'CCMP':
            pass
        elif cyphering == 'CCMP TKIP':
            pass
        else:
            pass
    elif wirelessPrivacy == 'WPA2 OPN':
        
        if cyphering == 'CCMP':
            pass
        elif cyphering == 'CCMP TKIP':
            pass
        else:
            pass
    else:
        
        if cyphering == 'CCMP':
            pass
        elif cyphering == 'CCMP TKIP':
            pass
        else:
            pass
    #return pdf
    

def pdfGenerator(WSSid, customerName):
    WSSid = int(WSSid)
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
    pdf.set_font('Arial', 'B', 25)
    # move to the right
    pdf.cell(65)
    # Title
    pdf.cell(100, 100, 'SIFI Wireless Assessment Report', 'C')
    pdf.ln(5)
    pdf.cell(120)
    pdf.cell(100, 110, f'{customerName}', 'C')
    pdf.set_font('Arial', 'B', 10)
    pdf.ln(0)
    pdf.cell(230)
    pdf.set_y(5)
    pdf.cell(0, 0, f'{date}', 0, 0, 'R')
    # pdf.cell(100, 100, f'{date}')
    # Line break
    pdf.ln(20)
    Assesment_ID = 0

    try:
        connection = mysql.connector.connect(host='100.64.0.1',
                                            database='sifi',
                                            user='root',
                                            password='sifi')
        cursor = connection.cursor()
        sql_select_Query = "SELECT * FROM wss WHERE wssID =" + str(WSSid) + ";"
            
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
            print("Customer Name  = ", row[7], "\n")
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

    pdf.add_page()
    #create cells 
    pdf.set_font("Arial", 'B', size= 16)
    pdf.cell(200,10, txt= "Records capturados del Assesment:", align= 'L')
    pdf.ln(10)
    pdf.set_font("Arial", size= 13)
    pdf.cell(200, 10,  txt= f"- ID : {row[0]}", ln= 3, align= 'L')
    pdf.cell(200, 10,  txt= f"- BSSID : {row[1]}", ln= 4, align= 'L')
    pdf.cell(200, 10,  txt= f"- ESSID : {row[2]}", ln= 5, align= 'L')
    pdf.cell(200, 10,  txt= f"- Agente SIFI : {row[3]}", ln= 6, align= 'L')
    # pdf.cell(200, 10,  txt= f"- El handshake capturado es : {row[4]}", ln= 7, align= 'L')
    # pdf.cell(200, 10,  txt= f"- Contraseña del AP : {row[5]}", ln= 8, align= 'L')
    pdf.cell(200, 10,  txt= f"- Tipo de test realizado: {row[6]}", ln= 9, align= 'L')
    pdf.cell(200, 10,  txt= f"- Empresa/Cliente: {row[7]}", ln= 10, align= 'L')

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

         pdf.set_font("Arial", 'B', size= 30)
         pdf.cell(70,25, txt= "SIFI Score", align= 'L')
         pdf.ln(25)
        #pdf.cell(200, 5,  txt= "SIFI WSS", ln= 12, align= 'L')
        #TABLE CREATION
        # Effective page width, or just epw
         pdf.cell(20)
         epw = pdf.w - 0.5*pdf.l_margin
        
        
        # Set column width to 1/4 of effective page width to distribute content 
        # evenly across table and page
         col_width = epw/4
        
        # Document title centered, 'B'old, 14 pt
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
                pdf.cell(1.9*col_width, 2*th, str(datum), border=1)
        
            pdf.ln(2*th)
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
             pdf.cell(200, 10, txt= "- Se debe cambiar la contraseña una vez cada 90 dias y no permitir que se repita las ultimas cuatro contraseñas.", ln= 29, align='L')

        #PCI NEXT PAGE

            #SETTING SPECIAL CHARACTERS TO PRESENT THE PCI-DSS handle
            chars = set('!#$%&()*+,-./:;<=>?@[\]^_`{|}~')

            if any((c in chars) for c in row[5]):
                #print a longer message, password meets requirements
                pdf.cell(200, 10, txt = "La contraseña que tiene posee caracteres especiales", ln=23, align='L')
            else:
            
                pdf.cell(200, 10, txt = "Su contraseña no tiene caracteres especiales por lo tanto presentamos tecnicas de se deben tener en cuenta: ", ln=23, align='L')
                # pdf.cell(200,1, txt= "deben tener en cuenta" , ln= 25, align= 'L')

            if len(row[5]) > 13:
                pdf.cell(200,10, txt= "La contraseña posee la longitud recomendada")

            else:
                pdf.cell(200, 10, txt = "Su contraseña no posee la longitud recomendada, por lo tanto presentamos tecnicas de se deben tener en cuenta", ln=23, align='L')

            if any((c in chars) for c in row[5]) and len(row[5]) > 13:
                pdf.cell(200, 10, txt= " La contraseña tiene la longitud recomendada e incluye caracteres especiales, la misma tiene un nivel de seguridad mucho mayor ")
            else:
                pdf.cell(200, 10, txt = "- Se debe cambiar siempre los valores predeterminados que fueron proporcionados por el proveedor, esto incluye las contraseñas y las ", ln=23, align='J')
                pdf.cell(200, 1, txt= "configuraciones como tambien deshabilitar las cuentas innecesarias antes de instalar su propio sistema de red.  ", ln= 24, align='J')
                pdf.ln(5)
                pdf.cell(200, 10, txt= "- La contraseña debe tener al menos una longitud de 13 caracteres para que sea menos predecible.", ln=25, align="J")
                pdf.ln(2)
                pdf.cell(200, 10, txt= "- Se debe cambiar la contraseña una vez cada 90 dias y no permitir que se repita las ultimas cuatro contraseñas.", ln= 29, align='L')


          #ESTADO DE LA RED, SIFI WSS SCORE
    #Estable	Al menos 1 resultado negativo de cualquiera de las funciones principales

    elif row[4] != "" and row[5] == "":
         pdf.set_font("Arial", 'B', size= 30)
         pdf.cell(70,25, txt= "SIFI Score", align= 'L')
         pdf.ln(25)
        #pdf.cell(200, 5,  txt= "SIFI WSS", ln= 12, align= 'L')
        #TABLE CREATION
        # Effective page width, or just epw
         pdf.cell(20)
         epw = pdf.w - 0.5*pdf.l_margin
        
        
        # Set column width to 1/4 of effective page width to distribute content 
        # evenly across table and page
         col_width = epw/4
        
        # Document title centered, 'B'old, 14 pt
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
                pdf.cell(1.9*col_width, 2*th, str(datum), border=1)
        
            pdf.ln(2*th)
        
        
         pdf.set_font("Arial", 'BI', size= 13)
         pdf.cell(200, 10,  txt= "Estable. La red pudo ser vulnerada en al menos un ambito.", ln= 26, align= 'L')
         pdf.set_font("Arial", 'B', size= 16)
         pdf.cell(110)
         pdf.cell(200, 10,  txt= "Recomendaciones", ln= 24, align= 'L')
         pdf.set_font("Arial", size= 13)
         pdf.cell(-110)
         pdf.cell(200, 10, txt= "Se ha capturado el 4 way handshake. Lo que significa que se ha podido hacer una deautenticacion del cliente conectado al Access Point", ln= 13, align= 'L')
         pdf.cell(200, 10,  txt= "Segun el libro CWSP en su capitulo 9.1.8 se recomienda actualizar a una solución de autenticación 802.1X/EAP usando autenticación ", ln= 14, align= 'L')
         pdf.cell(200, 1,  txt= "tunelada.", ln= 15, align= 'L')

    elif row[4] == "" and row[5] == "":
         pdf.set_font("Arial", 'B', size= 30)
         pdf.cell(70,25, txt= "SIFI Score", align= 'L')
         pdf.ln(25)
        #pdf.cell(200, 5,  txt= "SIFI WSS", ln= 12, align= 'L')
        #TABLE CREATION
        # Effective page width, or just epw
         pdf.cell(20)
         epw = pdf.w - 0.5*pdf.l_margin
        
        
        # Set column width to 1/4 of effective page width to distribute content 
        # evenly across table and page
         col_width = epw/4
        
        # Document title centered, 'B'old, 14 pt
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
                pdf.cell(1.9*col_width, 2*th, str(datum), border=1)
        
            pdf.ln(2*th)
         
         # Line break equivalent to 4 lines
         

         pdf.cell(120)
         pdf.set_font("Arial", 'BI', size= 14)
         pdf.cell(-120)
        
        
         pdf.set_text_color(0,0,0)
         pdf.cell(200, 10,  txt= "Según la tabla de valoración SIFI, el estado de seguridad es:", ln= 13, align= 'L')

        #text colour orange
         pdf.set_font("Arial", 'BI', size= 13)
         pdf.set_text_color(0,128,0)
         pdf.cell(200, 10,  txt= "Seguro. Todos los pentest con resultados positivos y ninguna vulnerabilidad detectada.", ln= 13, align= 'L')

    pdf.set_text_color(0,0,0)
    pdf.add_page()
    
    # Define margins
    epw = pdf.w - pdf.l_margin - pdf.r_margin
    eph = pdf.h - pdf.t_margin - pdf.b_margin
    
    # Draw new margins.
    pdf.rect(pdf.l_margin, pdf.t_margin, w=epw, h=eph) 
    
    pdf.set_font("Arial", 'B', size= 16)
    pdf.cell(110)
    pdf.cell(200, 10,  txt= "Políticas de seguridad (Generales)", ln= 17, align= 'L')
    pdf.set_font("Arial", 'B', size= 13)
    pdf.cell(-110)


    pdf.cell(200, 10,  txt= "- Política corporativa:", ln= 18, align= 'L')
    pdf.set_font("Arial", size= 13)
    pdf.cell(200, 1, txt= "Un apéndice adicional a las recomendaciones de seguridad podrían ser las recomendaciones de políticas WLAN corporativas.", ln= 19, align= 'L')
    pdf.cell(200, 10, txt= "El auditor puede ayudar al cliente a redactar una política de seguridad de la red inalámbrica si aún no tiene una.", ln= 20, align= 'L')
    pdf.ln(2)


    pdf.set_font("Arial", 'B', size= 13)
    pdf.cell(200, 10,  txt= "- Seguridad física:", ln= 21, align= 'L')
    pdf.set_font("Arial", size= 13)
    pdf.cell(200, 1, txt= "La instalación de unidades de cerramiento para proteger contra el robo y el acceso físico no autorizado a los puntos de acceso puede", ln= 22, align= 'L')
    pdf.cell(200, 10,  txt= "ser una recomendación. Estas también se utilizan a menudo con fines estéticos. ", ln= 23, align= 'L')
    pdf.ln(2)


    pdf.set_font("Arial", 'B', size= 13)
    pdf.cell(200, 10, txt= "- Declaración de autoridad:", ln = 24, align= 'L')
    pdf.set_font("Arial", size= 13)
    pdf.cell(200, 1, txt= "Define quien implementó la política WLAN y la dirección ejecutiva que respalda la política.", ln = 25, align= 'L')
    pdf.ln(2)


    pdf.set_font("Arial", 'B', size= 13)
    pdf.cell(200, 10, txt= "- Audiencia aplicable:", ln= 26, align= 'L')
    pdf.set_font("Arial", size= 13)
    pdf.cell(200, 1, txt= "Define el público al que se le aplica la política, ya sea empleados, visitantes o contratistas.", ln = 27, align= 'L')
    pdf.ln(2)


    pdf.set_font("Arial", 'B', size= 13)
    pdf.cell(200, 10, txt= "- Evaluación de riesgos y análisis de amenazas:", ln= 28, align= 'L')
    pdf.set_font("Arial", size= 13)
    pdf.cell(200, 1, txt= "Define los posibles riesgos y amenazas de seguridad inalámbrica y cuál será el impacto financiero en la empresa si se produce un ", ln = 29, align= 'L')
    pdf.cell(200, 10, txt= "ataque con éxito.", ln= 30, align='L')

    pdf.set_font("Arial", 'B', size= 13)
    pdf.cell(200, 10, txt= "- Procedimientos de denuncia de infracciones:", ln= 28, align= 'L')
    pdf.set_font("Arial", size= 13)
    pdf.cell(200, 1, txt= "Define cómo se aplicará la política de seguridad de WLAN, incluidas las acciones que se deben tomar y quién está a cargo de la ", ln = 29, align= 'L')
    pdf.cell(200, 10, txt= "aplicación.", ln= 30, align='L')
    

    pdf.set_font("Arial", 'B', size= 13)
    pdf.cell(200, 10, txt= "- Auditoría de seguridad: ", ln= 28, align= 'L')
    pdf.set_font("Arial", size= 13)
    pdf.cell(200, 1, txt= "Define los procedimientos de auditoría interna, así como la necesidad de auditorías externas independientes.", ln = 29, align= 'L')
        

    
    
      # pdf.cell(200, 10, txt= "No se ha capturado el handshake", ln= 11, align= 'L')

#  # Add page
#     pdf.add_page()

#     # set new margins equation
#     epw = pdf.w - pdf.l_margin - pdf.r_margin
#     eph = pdf.h - pdf.t_margin - pdf.b_margin

#     # Draw new margins.
#     pdf.rect(pdf.l_margin, pdf.t_margin, w=epw, h=eph)   

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
    
    pdfPrint(pdf, row[5], row[3], row[4])

    
    #save the pdf with the .pdf extension
    pdfFilePath = "SiFi_{}_{}.pdf".format(Assesment_ID, date)
    pdf.output(pdfFilePath)
    
    l2pdfGenerator(WSSid)