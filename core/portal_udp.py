#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from BeautifulSoup import BeautifulSoup
import urllib
import unicodedata
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import HTMLParser
h = HTMLParser.HTMLParser()

def curso_search(portal):
    soup = BeautifulSoup("".join(portal), fromEncoding="UTF-8")
    horario=soup.find("table",attrs={'id':'ctl00_cphBody_tblCursosInscritos'})
    tr=horario.findAll('tr')
    codes=[]
    nombres=[]
    profes=[]
    for t in range(2,len(tr)):
        td=tr[t].findAll("td")
        codes.append( td[1].getText() )

        nombres.append( td[2].getText() )
        profe =  td[4].getText()
        nombresx= profe.split(" - ")
        if len (nombresx) == 1:
            try:
                profes.append(nombresx[0])
            except:
                profes.append("")
        elif str(nombresx[1]) =="N.N":
            try:
                xx=nombresx[0].split(" ")
                profes.append(xx[1]+" "+xx[0])
            except:
                try:
                    xx=nombresx[2].split(" ")
                    profes.append(xx[1]+" "+xx[0])
                except:
                    profes.append("")
                    pass
        else :
            xx=nombresx[1].split(" ")
            profes.append(xx[1]+" "+xx[0])



    return codes,nombres,profes


from selenium import webdriver
from selenium.webdriver.common.keys import Keys



def Portal2(username,password,drivers=None):
    import urllib2
    import urllib
    import cookielib
    print username,password
    OK = False #Por defecto, el usuario y contrasena son incorrectos



    #driver = webdriver.Phantomjs()

    if drivers ==None:
        driver = webdriver.Firefox()
    else:
        driver=drivers
    driver.get("http://alumno.udp.cl/Login.aspx")


    elem = driver.find_element_by_id("ctl00_cphBody_txtUserCodi")
    elem2 = driver.find_element_by_id("ctl00_cphBody_txtUserPass")
    elem.send_keys(username)
    elem2.send_keys(password)
    elem.send_keys(Keys.RETURN)
    import time
    time.sleep(2)

    output = driver.page_source
    if 'Portal Web del Alumno' not in output :
        OK = True
        print "ACA1"
        driver.get('http://alumno.udp.cl/Pages/ResultadoCargaAcademica.aspx')
        output =driver.page_source





    else :
        print '\nUsuario y/o Contrasena equivocado(s), intente nuevamente\n\n'
        if drivers==None:
            driver.close()
        return []


    Codigos= curso_search(output)

    driver.get("http://alumno.udp.cl")

    soup=driver.page_source
    soup = BeautifulSoup("".join(soup), fromEncoding="UTF-8")
    Datos=soup.findAll("td",attrs={'class':"celdaMicarrera"})
    xdatos=[]
    for Dato in Datos:
        xdatos.append(  Dato.getText() )

    driver.get("http://alumno.udp.cl/Pages/MiRegistroAcademico.aspx?CAME_CODIGO=1&MENU_AYUDA_ID=5")
    soup=driver.page_source
    soup = BeautifulSoup("".join(soup), fromEncoding="UTF-8")
    Datos=soup.findAll("table",attrs={'id':"ctl00_cphBody_tblRegistroAcademico"})

    ARX =Datos[0]
    ARX =ARX.tbody.findAll("tr")
    Output=[]
    from listas import recursive_cursos
    historial = recursive_cursos(ARX,Output)



    driver.get('http://alumno.udp.cl/Pages/MisDatosPersonales.aspx?CAME_CODIGO=1&amp;MENU_AYUDA_ID=0')
    Datos_output = driver.page_source


    soup = BeautifulSoup("".join(Datos_output), fromEncoding="UTF-8")
    soup.find(id='ctl00_cphBody_xrpDatosPersonales_idTblCorreo')

    EXPORT={}
    EXPORT['datos']=xdatos
    EXPORT['historial']=historial

    EXPORT['carrera']          =  str(h.unescape( soup.find(id='ctl00_ddlCarreraAlumno').option.getText()))
    # print EXPORT['carrera']
    EXPORT['direccion']          = soup.find(id='ctl00_cphBody_xrDatosAdicionales_lblDireccionP').getText()
    EXPORT['region']             = soup.find(id='ctl00_cphBody_xrDatosAdicionales_lblRegionP').getText()
    EXPORT['ciudad']             = soup.find(id='ctl00_cphBody_xrDatosAdicionales_lblCiudadP').getText()
    EXPORT['comuna']             = soup.find(id='ctl00_cphBody_xrDatosAdicionales_lblComunaP').getText()
    EXPORT['departamento']       = soup.find(id='ctl00_cphBody_xrDatosAdicionales_lblDepartamentoP').getText()
    EXPORT['villa']              = soup.find(id='ctl00_cphBody_xrDatosAdicionales_lblVillaP').getText()
    EXPORT['telefono']           = soup.find(id='ctl00_cphBody_xrDatosAdicionales_lblTelefonoFijo').getText()
    EXPORT['correo_udp']         = soup.find(id='ctl00_cphBody_xrpDatosPersonales_idTblCorreo').getText()
    EXPORT['correo_respaldo']    = soup.find(id='ctl00_cphBody_xrpDatosPersonales_idTblCorreoAlt').getText()

    driver.get('http://alumno.udp.cl/Pages/MiHorario.aspx')
    HORARIOX = driver.page_source

    EXPORT['horario'] = BeautifulSoup("".join(  (HORARIOX) ), fromEncoding="UTF-8").find(id="ctl00_cphBody_tblHorario").findAll("tr")



    DATA={}



    soup = BeautifulSoup("".join(output), fromEncoding="UTF-8")
    nombre = soup.find(id='ctl00_lblNombreCompleto').getText()


    for ij in range(len(Codigos[0])):

        for ix in range(2):

            soup = BeautifulSoup("".join(output), fromEncoding="UTF-8")
            filter= "aspxNBIClick(event, 'ctl00_axnavMenu', "+str(ij+1)+", "+str(5-(ix*4))+")"
            print filter
            filter=unicode(filter)
            registro=soup.find("li",onclick=filter)
            A=registro.a['href']
            print A

            driver.get('http://alumno.udp.cl'+A)
            Curso_output = driver.page_source




            soup = BeautifulSoup("".join(Curso_output), fromEncoding="UTF-8")
            curso_codigo=soup.find(id='ctl00_cphBody_lblSubtituloPagina')
            IXX= curso_codigo.getText().split(" - ")

            JXX=IXX[1]
            if len(JXX) == 1:
                JXX="0"+JXX

            codigo = IXX[0]+str("-")+JXX
            try:
                if ix==0:

                    if codigo in Codigos[0]:

                        Documentos =[]
                        documentos = soup.find("table",attrs={'id':'ctl00_cphBody_grvArchivosSubidos'})
                        documentos = documentos.findAll("tr")

                        docu=[]
                        for i in range(1,len(documentos)):
                            docu.append({'archivo':documentos[i].a.getText(),'url':documentos[i].a['href']})


                        if codigo not in DATA:
                            DATA[codigo]=docu
                elif ix==1:
                    if codigo in Codigos[0]:
                        Noticias =[]
                        #ctl00_cphBody_ncNoticiasPorCurso_ICell
                        noticias = soup.find("td",attrs={'id':'ctl00_cphBody_ncNoticiasPorCurso_ICell'})
                        noticias = noticias.findAll("tr")
                        noti=[]
                        for i in range(1,len(noticias)):
                            noti.append({'fecha':fecha,'titulo':titulo,'texto':texto})









            except:
                pass


    EXPORT['data']    = DATA
    EXPORT['nombre']  = nombre
    EXPORT['codigos'] = Codigos
    driver.get('http://alumno.udp.cl/Pages/ResultadoCargaAcademica.aspx')
    elem2 = driver.find_element_by_id("ctl00_axmnuMenu_DXI3_T")
    elem2.click()
    if drivers==None:
        driver.close()
    return EXPORT


def Portal4(username):
    import urllib2
    import urllib
    import cookielib
    print username
    OK = False #Por defecto, el usuario y contrasena son incorrectos

    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    login_data = urllib.urlencode({'rut':username[:-2],'RutFormat':username,'SelAnno':2016, 'Sede':1,'TipDoc':2})
    try:

        output=opener.open('http://portales.udp.cl/udpcom/verpagos/prof_detalle_pago.asp', login_data).read()
    except:
        return []

    soup = BeautifulSoup("".join(output), fromEncoding="UTF-8")
    codigos=[]
    for color in ["white",'#E9F3F3']:
        try :
            cursos=soup.findAll("tr",attrs={'bgcolor':color})



            for curso in cursos:

                codigo = curso.findNext('td').findNext('td').getText().replace("&nbsp;","")

                if codigo not in codigos:
                    codigos.append(str(codigo))
        except:
            pass


    return codigos








def Login(user,passwd):
    return Portal2(user,passwd)

def Login_update(user,passwd,drivers):
    return Portal2(user,passwd,drivers)



#Login_alumnos("18020677-9","mmae2010")