
OK = False #Por defecto, el usuario y contrasena son incorrectos

def RUT(rut):
    rut=str(rut)
    suma=0
    multi= 2
    for r in rut [::-1]:
        suma += int (r) * multi
        multi += 1
        if multi == 8:
            multi = 2
    resto = suma % 11
    resta = 11 - resto
    if resta == 11:
        return "0"
    elif resta == 10:
        return "K"
    else:
        return str(resta)

def usuario(XSa,pos):
    ob={}

    XS=XSa.a
    print XS

    try:
        ob['full_name']=XS.getText()
    except:
        ob['full_name']=XSa.getText().replace("&nbsp;","")

    try:
        if pos==0:
            ob['rut']=XS['href'].split("&rut=")[1].split("&cur=")[0]
        else:
            ob['rut']=XS['href'].split("rut=")[1].split("&")[0]
    except:
        ob['rut']=""

    try:
        ob['rut']=ob['rut']+"-"+RUT(ob['rut'])
    except:
        pass
    return ob

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep



def search(username,password):


    driver = webdriver.Firefox()




    driver.get("http://alumno.udp.cl")


    elem = driver.find_element_by_id("ctl00_cphBody_txtUserCodi")
    elem2 = driver.find_element_by_id("ctl00_cphBody_txtUserPass")
    elem.send_keys(username)
    elem2.send_keys(password)
    elem.send_keys(Keys.RETURN)
    from BeautifulSoup import BeautifulSoup
    soup=driver.page_source
    if 'Portal Web del Alumno' in soup:
        print "Incorrecto"
        driver.close()
        return {}


    soup = BeautifulSoup("".join(soup), fromEncoding="UTF-8")

    asdf=soup.find(id='ctl00_axnavMenu_I0i5_')
    driver.get('http://alumno.udp.cl'+asdf.a['href'])
    sleep(2)
    driver.get('http://portales.udp.cl/udpcom/portal/lista_cursos.asp')
    driver.switch_to.alert=False

    soup=driver.page_source
    soup = BeautifulSoup("".join(soup), fromEncoding="UTF-8")
    Cursos_javascript=soup.findAll(bgcolor="#ffffee")

    CURSOS={}
    for ixx in range(1,len(Cursos_javascript)):

        try:
            js=Cursos_javascript[ixx].a['href']
            codigo=Cursos_javascript[ixx].a['href'].split("javascript:ir_a_curso('")[1].split(" ")[0]
            codigos=codigo.split("-")
            if len(codigos[1]) == 1:
                codigo=str(codigos[0])+"-0"+str(codigos[1])
            else:
                codigo=str(codigos[0])+"-"+str(codigos[1])
            print codigo





            driver.execute_script((js))
            sleep(2)
            cod=js.split("','")[1]
            driver.get('http://portales.udp.cl/udpcom/portal/miscompaneros.asp?nom_curso=CBE2000-6+PROBABILIDADES+Y+ESTADISTICA&cod_curso='+str(cod))

            soup=driver.page_source
            soup = BeautifulSoup("".join(soup), fromEncoding="UTF-8")
            xc=soup.find(bgcolor="#c0c0c0")
            curso={}

            curso['profesor']=usuario(xc.td.nextSibling.nextSibling,1)
            curso['alumno']=[]


            xc=soup.find(bgcolor="#3f7dbc")
            xs=xc.findAll("tr")
            for i in range(1,len(xs)):
                curso['alumno'].append(usuario(xs[i],0) )

            print curso
            driver.get('http://portales.udp.cl/udpcom/portal/lista_cursos.asp')
            driver.switch_to.alert=False
            CURSOS[codigo]=curso


        except:
            print "TERMINO este"
            driver.close()
            return CURSOS
            break


    #driver.close()



def recursive_cursos(Datos,ARRX):
    creditos=0
    for dato in Datos:
        Dato=dato.findAll("td")
        if len(Dato) == 5:
            Xdato=[ Dato[0].getText(),Dato[1].getText(),Dato[2].getText(),Dato[3].getText(),Dato[4].getText()]
            ARRX.append(Xdato)
        if len(Dato) == 3:
            creditos=Dato[2].getText()

    return {'ramos':ARRX,'creditos':creditos}




def user_update(username,password):


    driver = webdriver.PhantomJS()




    driver.get("http://alumno.udp.cl")


    elem = driver.find_element_by_id("ctl00_cphBody_txtUserCodi")
    elem2 = driver.find_element_by_id("ctl00_cphBody_txtUserPass")
    elem.send_keys(username)
    elem2.send_keys(password)
    elem.send_keys(Keys.RETURN)
    from BeautifulSoup import BeautifulSoup
    soup=driver.page_source
    if 'Portal Web del Alumno' in soup:
        print "Incorrecto"
        driver.close()
        return {}


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
    historial = recursive_cursos(ARX,Output)
    #print historial
    driver.close()

    return {'historial':historial,'datos':xdatos}




if __name__ =="__main__":
    user_update("17677526-2","dariojara")