



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





