from flask import Flask, render_template, jsonify, request,redirect
from flask.ext.mongoalchemy import MongoAlchemy
from portal_udp import Login, Portal4 as ayudantia
from listas import user_update
from flask.ext.htmlmin import HTMLMIN
from slimit import minify
VERSION = 7
DIA = "Martes"

app = Flask(__name__)
app.config['MINIFY_PAGE'] = True

HTMLMIN(app)

app.config['MONGOALCHEMY_DATABASE'] = 'UDP'
#app.config['MONGOALCHEMY_PORT'] = 27015
db = MongoAlchemy(app)

from crypto import *

from datetime import datetime,timedelta
dia = datetime.now()+timedelta(days=1)

class Salas_clases(object):
    def __init__(self):
        self.bloque = None
        self.tipo = None
        self.dia  = None
        self.sala = None


    def json(self):
        output = {}
        output['bloque'] = self.bloque
        output['tipo'] = self.tipo
        output['sala'] = self.sala
        output['dia'] = self.dia
        return output



class Cursos(db.Document):
    codigo = db.StringField()
    curso = db.StringField()
    profesor = db.StringField()
    facultad = db.StringField()
    keyp = db.ListField(db.StringField())
    keya = db.ListField(db.StringField())
    documentos = db.AnythingField()
    noticias = db.AnythingField()
    salas = db.AnythingField()
    profesor_sistema = db.AnythingField()
    alumnos = db.AnythingField()
    suspensiones = db.AnythingField()
    def json(self):
        obj = {}
        obj['curso'] = self.curso
        obj['profesor'] = self.profesor
        obj['sala'] = "sala"
        obj['bloque'] = self.bloque
        obj['dia'] = self.dia


        try:
            obj['codigo'] = str(self.mongo_id)
            obj['seccion'] = self.codigo.split("-")[1]
        except:
            pass
        return obj
    def arr(self,dia):
        ARX=[]
        for sala in self.salas:
            if str(sala['dia']) ==dia:
                obj = {}
                obj['curso'] = str(self.curso)
                obj['profesor'] = str(self.profesor)
                obj['bloque'] = str(sala['bloque'])
                obj['dia'] = str(sala['dia'])
                obj['sala'] = str(sala['sala'])
                obj['tipo'] = str(sala['tipo'])
                #obj['sala'] = "Suspendido"
                try:
                    obj['seccion'] = str(self.codigo.split("-")[1])
                    obj['codigo'] = str(self.mongo_id)
                    ARX.append(obj)
                except:
                    pass

        return ARX

Cursosx = Cursos


class Eventos(db.Document):
    nombre = db.StringField()
    expositor = db.StringField()
    fecha  = db.StringField()
    sala    = db.StringField()
    facultad  = db.StringField()
    cursos  = db.StringField()




class Usuarios(db.Document):
    rut = db.StringField()
    full_name = db.StringField()
    passwd = db.StringField()
    correo_udp         = db.StringField()
    correo_respaldo    = db.StringField()
    rol                = db.StringField()


class Salas(db.Document):
    facultad = db.StringField()
    sala     = db.StringField()
    capacidad= db.StringField()


class Ayudantias_blog(db.Document):
    codigo              = db.StringField()
    rut                 = db.StringField()
    hilos               = db.AnythingField()
    responsables         = db.AnythingField()



class Tareas(db.Document):
    codigo              = db.StringField()
    archivo             = db.StringField()
    fecha               = db.AnythingField()
    categoria           = db.StringField()
    rut                 = db.StringField()
    codigo_verificacion = db.StringField()
    responsable         = db.StringField()
    integrantes         = db.AnythingField()



class Profesores(db.Document):
    rut                = db.StringField()
    full_name          = db.StringField()
    passwd             = db.StringField()
    passwd_udp         = db.StringField()
    cursos             = db.ListField(db.StringField())
    direccion          = db.StringField()
    region             = db.StringField()
    ciudad             = db.StringField()
    comuna             = db.StringField()
    departamento       = db.StringField()
    villa              = db.StringField()
    telefono           = db.StringField()
    correo_udp         = db.StringField()
    correo_respaldo    = db.StringField()



class Alumnos(db.Document):
    rut                = db.StringField()
    full_name          = db.StringField()
    passwd = db.StringField()
    cursos = db.ListField(db.StringField())
    ayudantia = db.ListField(db.StringField())
    creditos    = db.StringField()
    ranking_escuela    = db.StringField()
    ranking_u    = db.StringField()
    promedio    = db.StringField()
    ingreso    = db.StringField()
    registro   = db.AnythingField()
    estado    =  db.AnythingField()
    carrera            = db.StringField()
    direccion          = db.StringField()
    region             = db.StringField()
    ciudad             = db.StringField()
    comuna             = db.StringField()
    departamento       = db.StringField()
    villa              = db.StringField()
    telefono           = db.StringField()
    correo_udp         = db.StringField()
    correo_respaldo    = db.StringField()
    sufragar           = db.AnythingField()


class Bilioteca_udp(db.Document):
    codigo          = db.StringField()
    archivo          = db.StringField()
    fecha           = db.StringField()
    categoria          = db.StringField()
    url             = db.StringField()
    identificador   = db.StringField()
    responsable     = db.StringField()
    rut             = db.StringField()
    validar         = db.IntField()
    denuncias       = db.AnythingField()
    def json(self):
        ob={}
        ob['archivo']=self.archivo
        ob['categoria']=self.categoria
        ob['url']=self.url
        ob['responsable']=self.responsable
        ob['fecha']=self.fecha.split(" ")[0]
        return ob




def recuperar_info(XDATA,xc,bloque,dia):
    if str(xc.getText() ) != "":
        codigo = xc['title'].split("\n")[0].split(":")[1].split(" - ")
        if len (codigo[1]) < 2:
            codigo=codigo[0]+"-0"+codigo[1]
        else:
            codigo=codigo[0]+"-"+codigo[1]


        #print xc.getText(),bloque,dias[dia],codigo
        if codigo not in XDATA.keys():
            XDATA[str(codigo)]={}
        XD= XDATA[str(codigo)]
        if dias[dia] not in  XD.keys():
            XD[dias[dia]]=[bloque]
        else :
            XD[dias[dia]].append(bloque)

    if dia < 5:
        recuperar_info(XDATA,xc.nextSibling,bloque,dia+1)

def Horario_check(Horario,codigos,Codes):
    XCODES={}
    first=False

    for xc in Horario:
        if first:
            bloque =  xc.td.getText()
            recuperar_info(XCODES,xc.td.nextSibling,bloque,0)

        first=True

    for ixx in range(len(codigos[0])):
        try:

            print codigos[0][ixx],codigos[1][ixx],codigos[2][ixx],XCODES[" "+str( codigos[0][ixx])]
        except:
            pass

        curso = Cursosx.query.filter({'codigo':codigos[0][ixx]}).first()
        #print str(curso.mongo_id)
        if curso == None:
            print "NUEVO CURSO"
            SALAS=[]
            try:
                XT=XCODES[" "+str( codigos[0][ixx])]
                for dia in XT.keys():
                    sala=Salas_clases()
                    for bloque in XT[dia]:
                        sala.bloque = bloque
                        sala.sala   = ""
                        sala.dia    = dia
                        sala.tipo   = ""
                        SALAS.append(sala.json())
            except:
                pass

            CURX = Cursosx()
            CURX.curso        = codigos[1][ixx]
            CURX.codigo       = codigos[0][ixx]
            try:
                CURX.documentos=Codes['data'][codigos[0][ixx]]
            except:
                CURX.documentos=[]
            CURX.profesor     = codigos[2][ixx]
            CURX.suspensiones = {"18/04/2016":{'supension':'Terminal'}}
            CURX.facultad     = ""
            CURX.keyp         = []
            CURX.keya         = []
            CURX.salas        = SALAS
            CURX.profesor_sistema = {}
            CURX.noticias=[]
            CURX.alumnos = []

            CURX.save()
            print CURX.codigo
        else :
            try:
                curso.documentos=Codes['data'][codigos[0][ixx]]
            except:
                curso.documentos=[]
            curso.save()



def alumno_up(alumno,user,passwd):
    Codes = Login(str(user), str(passwd))
    if Codes==[]:
        return

    Horario_check(Codes['horario'],Codes['codigos'],Codes)
    alumno.full_name = Codes['nombre']
    alumno.rut = str(user)
    alumno.passwd = str(passwd)
    alumno.cursos = Codes['codigos'][0]

    ayuda= ayudantia(str(user))


    alumno.ayudantia = ayuda
    #alumno.ayudantia = []
    alumno.direccion          = Codes['direccion']
    alumno.carrera            = Codes['carrera']
    alumno.region             = Codes['region']
    alumno.ciudad             = Codes['ciudad']
    alumno.departamento       = Codes['departamento']
    alumno.comuna             = Codes['comuna']
    alumno.villa              = Codes['villa']
    alumno.telefono           = Codes['telefono']
    alumno.correo_udp         = Codes['correo_udp']
    alumno.correo_respaldo    = Codes['correo_respaldo']

    data=Codes

    registros=[]
    for ix in range(1,len(data['historial']['ramos'])):
        xdata=data['historial']['ramos'][ix]
        registro={}
        registro['ano_semestre']=xdata[0]
        registro['codigo']=xdata[1]
        registro['nombre']=xdata[2]
        registro['nota']=xdata[3]
        registro['creditos']=xdata[4]
        registros.append(registro)
    alumno.registro = registros
    alumno.ingreso=data['datos'][0]
    alumno.ranking_escuela=data['datos'][1]
    alumno.ranking_u=data['datos'][2]
    alumno.estado=data['datos'][3]
    alumno.promedio=data['datos'][4]
    alumno.creditos = str(data['historial']['creditos'])
    alumno.sufragar={'Votaciones_1':{'habilitado':True,'time':None,'code':None}}
    alumno.save()
    insert_server_vote(alumno)
    print "Guardado"
    return alumno,Codes

@app.errorhandler(404)
def page_not_found(e):
    return redirect("https://udpcursos.com")
