#!/usr/bin/env python
# -*- coding: utf-8 -*-
from core.core import *
from core.portal_udp import Login_update

from selenium import webdriver
def DATA_cursos():

    driver = webdriver.PhantomJS()
    #driver = webdriver.Firefox()
    try:
        Cursos=[]
        CURSOSX =   Cursosx.query.filter().all()
        print len (CURSOSX)
        for cursos in CURSOSX:
            print "aca",cursos.curso
            if cursos.codigo not in Cursos:

                ixx=0
                try:
                    for alumno in Alumnos.query.filter({'cursos':{'$eq':cursos.codigo}}).all():
                #    try:
                        try:
                            Codes = Login_update(alumno.rut, alumno.passwd,driver)

                        except:
                            break
                        # print Codes
                        print alumno.rut
                        ok =False

                        for code in Codes['data'].iterkeys():
                            if code == cursos.codigo:
                                CURSO = cursos
                            else:

                                CURSO = Cursosx.query.filter({'codigo': code}).first()
                            try:
                                if CURSO.codigo not in Cursos:
                                    CURSO.documentos = Codes['data'][code]
                                    CURSO.noticias = Codes['data'][code]
                                    print CURSO.curso
                                    CURSO.save()
                                    Cursos.append(code)
                                    if CURSO.codigo == cursos.codigo:
                                        ok =True


                            except:
                                pass
                        if ok or ixx==3:
                            break
                        ixx=ixx+1


                except:
                    pass



    except:
        print "CAMBIO EL PASS",alumno.rut

import requests



from time import sleep
from json import loads
import json
def portar_db():
    ALUMNOS=[]
    ixx=0

    print "aca"
    for alumno in Alumnos.query.filter({'rut':'196785426'}).all():
        print "aqui"
        url= "http://localhost:8000/%s.txt"%(alumno.rut)
        print url
        Cursos={}
        r=requests.get(url)
        if r.status_code !=404:
            data=json.loads(r.text)
            print data
            if data['login']:
                for curso in data['docus']['Lista_curso'].keys():
                    xcurso=curso.split("_")
                    xcurso= xcurso[0]+"-"+xcurso[1][2:]
                    if xcurso not in Cursos.keys():
                        Cursos[xcurso]={}
                        for cu in data['cursos']:
                            if cu['code'] == curso.split("_")[0]:
                                Cursos[xcurso]['curso']=cu['name']
                                print Cursos[xcurso]['curso']
                                break
                    if curso.split("_")[1][:2]=="CA":
                        Cursos[xcurso]['lista']=data['docus']['Lista_curso'][curso]
                        Cursos[xcurso]['documentos']=data['docus']['archivos'][curso]
                    else:
                        Cursos[xcurso]['ayudante']=data['docus']['Lista_curso'][curso][0]

                print Cursos
                for curso in Cursos.keys():
                    cur=Cursosx.query.filter({'codigo':curso}).first()
                    if cur == None:
                        xc=Cursosx()
                        xc.codigo = curso
                        xc.curso=Cursos[curso]['curso']
                        xc.profesor=""
                        xc.facultad = ""
                        xc.keyp=[]
                        xc.keya=[]
                        xc.ayudante=""
                        try:
                            xc.documentos=Cursos[curso]['documentos']
                        except:
                            xc.documentos=[]
                        xc.noticias=[]
                        xc.salas=[]
                        xc.profesor_sistema=[]
                        try:
                            xc.alumnos=Cursos[curso]['lista']
                        except:
                            xc.alumnos=[]
                        xc.suspensiones=[]
                        xc.save()
                    else:
                        try:
                            if cur.ayudante=="Tabla vacía":
                                cur.ayudante=Cursos[xcurso]['ayudante']
                                cur.save()
                        except:
                            pass

                        try:


                            if len(cur.documentos) < len(Cursos[curso]['documentos']):
                                cur.documentos= Cursos[curso]['documentos']
                                cur.save()
                                print "update"
                        except:
                            pass
                alumno.estado=data['estado']
                alumno.firstname = data['firstname']
                alumno.lastname= data['lastname']
                alumno.ranking_escuela = data['posicionescuela']
                alumno.registro=data['cursos']
                alumno.promedio=data['promedio']
                alumno.ranking_u=data['rankingcarrera']
                alumno.dropbox=""
                alumno.cursos=Cursos.keys()
                alumno.sapstatus = "Portado"
            if False :
                alumno.firstname = ""
                alumno.lastname= ""
                alumno.sapstatus = data['motivo']

            alumno.save()



def portar_db_txt():
    ALUMNOS=[]
    ixx=0

    print "aca"
    ALUMNOS=[{'alumno':alumno.rut,'passwd':alumno.passwd} for alumno in Alumnos.query.filter({'sapstatus':'Pendiente'}).all()]

    file = open("usersKK.txt","w")
    file.write(json.dumps(ALUMNOS))
    file.close()
import os,time
def notificar_incorrecta():

    mensaje2= "te recomendamos volver a ingresar a https://udpcursos.com/ y volver a ingresarla"
    for alumno in Alumnos.query.filter({'sapstatus':'Contraseña incorrecta'}).all():
        celular=alumno.celular.replace("+","").replace(" ","")
        if len(celular) ==11:
            mensaje1 ="Estimado %s tu contraseña introducida en udpcursos no es la correcta en sap"%(alumno.full_name)
            len(celular)
            mensaje="/Volumes/OsXHDD/Malba/Downloads/yowsup-master/yowsup-cli demos -s  %s \"%s\"  -l 56984185094:\"R/65WaYGpTaxWHAyg/vQMEE2Zl0=\""%(celular,mensaje1)
            os.system(mensaje)
            time.sleep(1)
            mensaje="/Volumes/OsXHDD/Malba/Downloads/yowsup-master/yowsup-cli demos -s  %s \"%s\"  -l 56984185094:\"R/65WaYGpTaxWHAyg/vQMEE2Zl0=\""%(celular,mensaje2)
            os.system(mensaje)

            time.sleep(4)

def notificar_correcta():

    mensaje2= "por lo que ya puedes entrar a https://udpcursos.com incluso desde tu celular o tablet :)"
    for alumno in Alumnos.query.filter({'sapstatus':'Portado'}).all():
        celular=alumno.celular.replace("+","").replace(" ","")
        if len(celular) ==11:
            mensaje1 ="Estimado %s tu cuenta sap ya es compatible con udpcursos "%(alumno.full_name)
            len(celular)
            mensaje="/Volumes/OsXHDD/Malba/Downloads/yowsup-master/yowsup-cli demos -s  %s \"%s\"  -l 56984185094:\"R/65WaYGpTaxWHAyg/vQMEE2Zl0=\""%(celular,mensaje1)
            os.system(mensaje)
            time.sleep(1)
            mensaje="/Volumes/OsXHDD/Malba/Downloads/yowsup-master/yowsup-cli demos -s  %s \"%s\"  -l 56984185094:\"R/65WaYGpTaxWHAyg/vQMEE2Zl0=\""%(celular,mensaje2)
            os.system(mensaje)

            time.sleep(4)

def quitar():
    for alumno in Alumnos.query.filter({'sapstatus':'Portado'}).all():
        alumno.ayudantia=[]
        alumno.save()
        print "aca"

def correos():
    for alumno in Alumnos.query.filter({'sapstatus':"NotJet"}).limit(200).all():
        print alumno.correo_udp
        alumno.sapstatus="NotJet invitado"
        alumno.firstname = ""
        alumno.lastname= ""
        alumno.save()

def norm_cursos():
    for curso in Cursosx.query.all():
        for documento in curso.documentos:
            print "curl -o \"%s/%s\" \"%s\""%(curso.codigo,documento['archivo'],documento['url'])

#portar_db()
#norm_cursos()
portar_db()
#correos()

#notificar_correcta()


#notificar()

#portar_db_txt()




#DATA_cursos()