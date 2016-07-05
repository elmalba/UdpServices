from core.core import *
from core.crypto import *
def login(user, passwd):
    consulta_1 = {'rut': user}
    alumno = Alumnosx.query.filter(consulta_1).first()
    if alumno == None:
        alumno = alumno_up(Alumnosx(),user,passwd)[0]
    elif str(alumno.passwd) != str(passwd):
        alumno_up(alumno,user,passwd)[0]


    Codes = alumno.cursos + alumno.ayudantia

    Curso_output = []
    Codigos = []
    for codigo in Codes:
        Codigos.append({'codigo':str(codigo)})

    cursos_xo=[]

    consulta={ '$or': Codigos}

    print "POR AQUO",consulta
    cursos = Cursosx.query.filter(consulta).all()
    print len (cursos)
    Codigos = []
    for curso in cursos:
        Codigos.append(str(curso.mongo_id))
        cursos_xo.append({ 'hash' :str(curso.mongo_id),'curso' : str(curso.curso),'profesor':str(curso.profesor),'seccion':curso.codigo.split("-")[1]})

    return jsonify(codigos=Codigos,cursos=cursos_xo)


from flask_restful import reqparse, abort, Api, Resource

api = Api(app)

@app.route('/Cursos.js', methods=['GET'])
def Curso_js():
    def getKey(custom):
        return custom['bloque']

    CURXX=[]
    for curso in  Cursos.query.filter({"salas" : { '$elemMatch': { "dia" : DIA } } }).all():
        CURXX=CURXX+curso.arr(DIA)
    CURXX=sorted(CURXX,key=getKey)
    js = render_template("cursos.js", cursos=CURXX,version=VERSION)
    #js = minify(js, mangle=True, mangle_toplevel=True)
    return js


# class Cursos(Resource):
#     def get(self):
#         try:
#             usuario,passwd=decode_token(request.args['token'])
#             return login(usuario, passwd)
#         except:
#             ob = {'resultados': "Usuario y/o password invalidos"}
#             print ob
#             return ob
#
#     def post(self):
#
#         try:
#             usuario,passwd=decode_token(request.json['token'])
#             return login(usuario, passwd)
#
#             pass
#         except:
#             ob = {'resultados': "Usuario y/o password invalidos"}
#             return ob
#
#
# api.add_resource(Cursos, '/Cursos')


class Documentos(Resource):
    def get(self, curso_id):
        Curso = Cursosx.query.get(curso_id)
        return Curso.documentos
api.add_resource(Documentos, '/Documentos/<curso_id>')



if __name__ =="__main__":
    #update_user()
    #DATA_cursos()
    app.run(port=5001, host="0.0.0.0", debug=True)

