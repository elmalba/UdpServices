from config.mongo import db
#inicio del modelo


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
class cursos(db.Document):
    codigo = db.StringField()
    curso = db.StringField()
    profesor = db.StringField()
    ayudante = db.StringField()
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

Cursos=cursos
Cursosx = Cursos