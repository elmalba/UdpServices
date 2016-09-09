from config.mongo import db
#inicio del modelo

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