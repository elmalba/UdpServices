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
    file = open("notificar2.txt","w")
    RUTS=[]

    print "aca"
    for alumno in Alumnos.query.all():
        print "aqui"
        url= "http://localhost:8000/%s.txt"%(alumno.rut)
        #print url
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
                                print xcurso
                                break
                    if curso.split("_")[1][:2]=="CA":
                        Cursos[xcurso]['lista']=data['docus']['Lista_curso'][curso]
                        Cursos[xcurso]['documentos']=data['docus']['archivos'][curso]
                    else:
                        Cursos[xcurso]['ayudante']=data['docus']['Lista_curso'][curso][0]

                #print Cursos
                if False:
                    for curso in Cursos.keys():
                        cur=Cursosx.query.filter({'codigo':curso}).first()
                        if cur == None:
                            xc=Cursosx()
                            xc.codigo = curso
                            print "ASFDA!"
                            print xc.codigo,alumno.rut
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
                RUTS.append(alumno.rut)
                alumno.full_name=alumno.firstname+" "+alumno.lastname
                alumno.sapstatus = "Portado"
                try:
                    print alumno.celular
                except:
                    alumno.celular=""

                try:
                    alumno.save()
                except:
                    alumno.villa=alumno.comuna=alumno.ciudad=alumno.direccion=""
                    alumno.full_name=alumno.firstname+" "+alumno.lastname
                    alumno.ingreso=data['semestreinicio']
                    alumno.creditos=""
                    alumno.departamento=""
                    alumno.carrera=data['carrera']
                    alumno.telefono=alumno.passwd2=alumno.region=""
                    alumno.correo_udp=alumno.correo_respaldo=alumno.token=""
                    alumno.sufragar={}

                    alumno.registro_antiguo=alumno.cursos_antiguo=[]
                    alumno.save()
            if False :
                alumno.firstname = ""
                alumno.lastname= ""
                alumno.sapstatus = data['motivo']

            print "aca2"
    file.write(json.dumps(RUTS))
    file.close()




def portar_db_txt():
    ALUMNOS=[]
    ixx=0

    print "aca"
    ALUMNOS=[{'alumno':alumno.rut,'passwd':alumno.passwd} for alumno in Alumnos.query.filter({'sapstatus':'Nuevo'}).all()]

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
    ruts=['147451741.txt', '16662262k.txt', '169644365.txt', '171757959.txt', '172689906.txt', '173257090.txt', '173496494.txt', '174028834.txt', '174158509.txt', '176753056.txt', '176759496.txt', '176999934.txt', '177021946.txt', '178399365.txt', '178592831.txt', '179069091.txt', '179233169.txt', '179910772.txt', '180220542.txt', '18079008k.txt', '181277564.txt', '181690860.txt', '182114421.txt', '182773158.txt', '183000535.txt', '183360175.txt', '183411772.txt', '183560913.txt', '183567225.txt', '183913816.txt', '183916408.txt', '183969293.txt', '183970763.txt', '183991337.txt', '184263416.txt', '184575353.txt', '184590980.txt', '184650339.txt', '184650606.txt', '184850958.txt', '185248917.txt', '185316203.txt', '185333906.txt', '18541275k.txt', '185472493.txt', '186120647.txt', '186228448.txt', '186351126.txt', '186378369.txt', '186391225.txt', '186611098.txt', '186661575.txt', '18670584k.txt', '187226473.txt', '187262550.txt', '187318165.txt', '187326699.txt', '187648696.txt', '187674182.txt', '187676665.txt', '187688248.txt', '188324436.txt', '188403808.txt', '188631428.txt', '188659454.txt', '188661696.txt', '18883230k.txt', '189057881.txt', '189061137.txt', '189087454.txt', '189284411.txt', '189323867.txt', '189329245.txt', '189385129.txt', '189396155.txt', '189491336.txt', '189547714.txt', '189724667.txt', '189766327 .txt', '189913397.txt', '190338991.txt', '190357341.txt', '190375781.txt', '190386074.txt', '190609111.txt', '190798496.txt', '190806537.txt', '191454987.txt', '192097029.txt', '192162033.txt', '192193559.txt', '192756197.txt', '192802121.txt', '192909287.txt', '193066321.txt', '193229646.txt', '193235786.txt', '193242901.txt', '19375010.txt', '193919790.txt', '194051271.txt', '194092237.txt', '19419667.txt', '194232225.txt', '19430790k.txt', '194856954.txt', '195143196.txt', '195150877.txt', '195158541.txt', '195170401.txt', '195384541.txt', '195399182.txt', '195712220.txt', '195837229.txt', '196033645.txt', '196050264.txt', '196062424 .txt', '196199284.txt', '196478299.txt', '196687637.txt', '196689923.txt', '196712836.txt', '19687035.txt', '197395540.txt', '197458216.txt', '19792702k.txt', '198102091.txt', '198280437.txt', '198386154.txt', '198895881.txt', '199029932.txt', '199126679.txt', '224788215.txt', '234694553.txt']
    ruts=['108552077.txt', '123424271.txt', '126330812.txt', '132320195.txt', '147451741.txt', '160432012.txt', '161634360.txt', '16662262k.txt', '169089930.txt', '169644365.txt', '17021946.txt', '170918584.txt', '17105127.txt', '171757959.txt', '172676537.txt', '172689906.txt', '172715370.txt', '173136072.txt', '173257090.txt', '173496494.txt', '174028834.txt', '174158509.txt', '174869498.txt', '175173773.txt', '175983023.txt', '176753056.txt', '176759496.txt', '176761997.txt', '176999934.txt', '177021946.txt', '177278939.txt', '177642061.txt', '177699098.txt', '177885592.txt', '17788863k.txt', '178399365.txt', '178592831.txt', '178652524.txt', '178783815.txt', '179031884.txt', '179069091.txt', '179233169.txt', '179849119.txt', '179910772.txt', '180196803.txt', '180214119.txt', '180219641.txt', '180220542.txt', '180239049.txt', '180525025.txt', '18064220k.txt', '180645659.txt', '18079008k.txt', '181210869.txt', '181277564.txt', '181652020.txt', '181673699.txt', '181690860.txt', '181714786.txt', '181721367.txt', '181723122.txt', '18210843k.txt', '182114421.txt', '18273814k.txt', '182741515.txt', '182773158.txt', '182826103.txt', '182943681.txt', '183000535.txt', '183360175.txt', '183396099.txt', '183411772.txt', '183550411.txt', '183560913.txt', '183567225.txt', '183626152.txt', '1839.txt', '18390.txt', '183904361.txt', '183911430.txt', '183913816.txt', '183916408.txt', '18393872k.txt', '183969293.txt', '183970763.txt', '183991337.txt', '184238101.txt', '184263416.txt', '184556561.txt', '184575353.txt', '184589494.txt', '184590980.txt', '184618869.txt', '184637286.txt', '184650339.txt', '184650606.txt', '184657989.txt', '184850958.txt', '18495804k.txt', '185134717.txt', '185248917.txt', '18528851k.txt', '185292053.txt', '185302161k.txt', '185316203.txt', '185321991.txt', '185333906.txt', '185409287.txt', '185410641.txt', '18541275k.txt', '185472493.txt', '185688801.txt', '1859546130.txt', '186087615.txt', '186120647.txt', '186140796.txt', '18621899K.txt', '186228448.txt', '186346866.txt', '186351126.txt', '186351347.txt', '186378369.txt', '18638976k.txt', '186391225.txt', '186392183.txt', '186392884.txt', '186611098.txt', '18665658k.txt', '186661575.txt', '18670584k.txt', '186980468.txt', '187226473.txt', '187261783.txt', '187262550.txt', '187318165.txt', '187326699.txt', '187437253.txt', '187512417.txt', '187648696.txt', '187658838.txt', '187670357.txt', '187674182.txt', '187676665.txt', '187688248.txt', '187785227.txt', '187862297.txt', '188324436.txt', '188332307.txt', '188403808.txt', '188597939.txt', '188631428.txt', '188659454.txt', '188661696.txt', '18883230.txt', '18883230k.txt', '189057881.txt', '189061137.txt', '189087454.txt', '18925007k.txt', '189261195.txt', '189284411.txt', '189323867.txt', '189326688.txt', '189329245.txt', '189347435.txt', '189356846.txt', '189385129.txt', '189396155.txt', '189491336.txt', '189547714.txt', '189553050.txt', '189556373.txt', '189724667.txt', '189758111.txt', '189766327 .txt', '189913397.txt', '19.323.7029.txt', '19.txt', '190213814.txt', '190232271.txt', '190327558.txt', '190337557.txt', '190338991.txt', '190357341.txt', '190375781.txt', '190386074.txt', '190391418.txt', '190576175.txt', '190609111.txt', '190647072.txt', '190685829.txt', '190742520.txt', '19077333k.txt', '190794016.txt', '190798496.txt', '190806537.txt', '191121368.txt', '191122380.txt', '191124006.txt', '191141083.txt', '191150317.txt', '191168402.txt', '191339924.txt', '19136581k.txt', '191366808.txt', '191414993.txt', '191454987.txt', '19145987.txt', '191624408.txt', '191860284.txt', '191870891.txt', '191890280.txt', '191893476.txt', '192086086.txt', '192097029.txt', '192098327.txt', '192162033.txt', '192193559.txt', '192356881.txt', '192389755.txt', '192435528.txt', '192439906.txt', '19245350k.txt', '19250452k.txt', '192541.txt', '192594278.txt', '192694278.txt', '192756197.txt', '192767571.txt', '192778204.txt', '192789206.txt', '192791189.txt', '192802121.txt', '192811139.txt', '192811239.txt', '192815363.txt', '1928456691.txt', '192892880.txt', '192898420.txt', '192909287.txt', '192911567.txt', '192914000.txt', '192990335.txt', '193066321.txt', '193069559.txt', '193069969.txt', '19307099k.txt', '193080278.txt', '193109063.txt', '19311749k.txt', '193229646.txt', '193235786.txt', '193242901.txt', '193413536.txt', '193445675.txt', '193470475.txt', '193484052.txt', '193596118.txt', '19375010.txt', '193907458.txt', '193919790.txt', '194051271.txt', '194092237.txt', '194121164.txt', '19419667.txt', '194225369.txt', '194232225.txt', '194287518.txt', '19430790k.txt', '194434499.txt', '194753950.txt', '194856954.txt', '194944365.txt', '195143196.txt', '195150877.txt', '195153590.txt', '195158541.txt', '195159459 .txt', '195170401.txt', '195177732.txt', '195223793.txt', '19522389.txt', '195231745.txt', '19524538k.txt', '195256764.txt', '195283370.txt', '195384541.txt', '195399182.txt', '195436010.txt', '195452423.txt', '195639175.txt', '195712220.txt', '195837229.txt', '195895880.txt', '196033645.txt', '196050264.txt', '196062424 .txt', '196062424.txt', '196182411.txt', '196199284.txt', '196358544.txt', '196379037.txt', '196433007.txt', '196468781.txt', '196478299.txt', '196484388.txt', '196687637.txt', '196689923.txt', '196698140.txt', '196708111.txt', '196712836.txt', '196804366.txt', '196816488.txt', '19683768k.txt', '196839720.txt', '19687035.txt', '197019387.txt', '197052244.txt', '197296488.txt', '197394242.txt', '197395540.txt', '197405880.txt', '197407948.txt', '197426322.txt', '197442417.txt', '197458216.txt', '197458348.txt', '197552077.txt', '197775513.txt', '197895527.txt', '19792702k.txt', '198102091.txt', '198280437.txt', '198299642.txt', '198386154.txt', '198568872.txt', '19878835k.txt', '198895881.txt', '199029932.txt', '199126679.txt', '199142739.txt', '1o.txt', '1p.txt', '212904678.txt', '219790732.txt', '224788215.txt', '234694553.txt', 'de registro feb mar mar .txt', 'sofita.1@gmail.com.txt']
    mensaje2= "por lo que ya puedes entrar a https://udpcursos.com incluso desde tu celular o tablet :)"
    for rut in ruts:
        for alumno in Alumnos.query.filter({'sapstatus':'Portado','rut':rut.replace(".txt","")}).all():
            try:
                celular=alumno.celular.replace("+","").replace(" ","")
                if len(celular) ==11:
                    mensaje1 ="Estimado %s tu cuenta sap ya es compatible con udpcursos "%(alumno.full_name)
                    len(celular)
                    mensaje="python yowsup-cli demos -s  %s \"%s\"  -l 56984185094:\"R/65WaYGpTaxWHAyg/vQMEE2Zl0=\""%(celular,mensaje1)
                    print mensaje
                    print "sleep 1"
                    mensaje="python yowsup-cli demos -s  %s \"%s\"  -l 56984185094:\"R/65WaYGpTaxWHAyg/vQMEE2Zl0=\""%(celular,mensaje2)
                    print mensaje
                    print "sleep 4"
            except:
                pass

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

def email():
    for alumno in Alumnos.query.filter({'sapstatus':'Portado'}).all():
        try:
            if alumno.correo_udp!="":
                print alumno.correo_udp
        except:
            pass


def whats():
    pass




#email()


#portar_db()
#norm_cursos()
#portar_db()
#correos()

#notificar_correcta()


#notificar()
#notificar_correcta()
