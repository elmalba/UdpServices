from config.mongo import db

class alumnos(db.Document):
    rut                = db.StringField()
    firstname          = db.StringField()
    lastname           = db.StringField()
    full_name          = db.StringField()
    dropbox          = db.StringField()
    sapstatus    = db.StringField()
    celular    = db.StringField()
    passwd = db.StringField()
    passwd2 = db.StringField()
    token = db.StringField()
    cursos = db.ListField(db.StringField())
    cursos_antiguo = db.ListField(db.StringField())
    ayudantia = db.ListField(db.StringField())
    creditos    = db.StringField()
    ranking_escuela    = db.StringField()
    ranking_u    = db.StringField()
    promedio    = db.StringField()
    ingreso    = db.StringField()
    registro   = db.AnythingField()
    registro_antiguo   = db.AnythingField()
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
    def json(self):
        ob={}
        ob['rut']=self.rut
        ob['full_name']=self.full_name
        ob['cursos']=self.cursos
        ob['ayudantia']=self.ayudantia
        ob['correo_udp']=self.correo_udp
        ob['registro']=self.registro
        ob['telefono']=self.telefono
        return ob

Alumnos=alumnos


# app_key = '9k48jzrqqrqqic1'
# app_secret = 'km5mm7m4wq94vmt'
#
# flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)
#
# authorize_url = flow.start()
#
# code = "E9T74lDW_5sAAAAAAAABrx5UrXMhlGSA0osQL4HSEQw"
# access_token, user_id = flow.finish(code)
# client = dropbox.client.DropboxClient(access_token)
#
# files=glob.glob("FIC1002-03/*")
#
# nombre="Ingles II"
# for file in files:
#     f = open(file, 'rb')
#     response = client.put_file('./%s/%s'%(nombre,file), f)
#
