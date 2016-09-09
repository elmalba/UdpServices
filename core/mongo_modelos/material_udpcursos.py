from config.mongo import db
#inicio del modelo

class Bilioteca_udp(db.Document):
    codigo          = db.StringField()
    archivo          = db.StringField()
    fecha           = db.StringField()
    categoria          = db.StringField()
    url             = db.StringField()
    #identificador   = db.StringField()
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