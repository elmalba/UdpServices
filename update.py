from core.core import *
from core.portal_udp import Login_update

from selenium import webdriver
def DATA_cursos():

    driver = webdriver.PhantomJS()
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

DATA_cursos()