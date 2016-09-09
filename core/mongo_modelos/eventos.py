from config.mongo import db
#inicio del modelo

class Eventos(db.Document):
    nombre = db.StringField()
    expositor = db.StringField()
    fecha  = db.StringField()
    sala    = db.StringField()
    facultad  = db.StringField()
    cursos  = db.StringField()
