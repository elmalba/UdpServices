from flask import Blueprint, request
from flask_restful import Resource, Api
test = Blueprint('Test', __name__)

api = Api(test)



from core.mongo_modelos import Cursos,Profesores,Bilioteca_udp
from config import cur

class Test(Resource):
    def get(self):
        codigos= {}
        # materiales = Bilioteca_udp.query.filter({'curso':'CIT1000','categoria':'otros'}).all()
        # for material in materiales:
        #     material.responsable="Nicolas Rosso"
        #     material.save()
        # return "adsf"

        ix=0
        ij=0
        for cu in cur:
            codigo = cu['codigo']
            for id in range(15):
                codigo=codigo.replace("%s "%id,"%s,"%id)

            codigo=codigo.replace(" ","")
            codigo =codigo.split(",")
            print codigo
            #print cu
            for cod in codigo:
                if cod != u'':
                    ij=ij+1

                    curso = Cursos.query.filter({'codigo':cod}).first()
                    if curso != None:
                        codigos[str(curso.mongo_id)]={}
                        codigos[str(curso.mongo_id)]['curso']=curso.curso
                        codigos[str(curso.mongo_id)]['profesor']=curso.profesor
                        codigos[str(curso.mongo_id)]['tipo']="Examen"
                        codigos[str(curso.mongo_id)]['sala']=cu['sala']
                        codigos[str(curso.mongo_id)]['seccion']=cod.split("-")[1]
                        codigos[str(curso.mongo_id)]['bloque']=cu['bloque']
                        ix=ix+1
                    else:
                        print cu

        print ix,ij
        return codigos



        # profesores={}
        # cursos = Cursos.query.all()
        # for curso in cursos:
        #     if curso.profesor_sistema !={}:
        #         rut=curso.profesor_sistema['rut']
        #         if rut not in profesores.iterkeys():
        #             profesores[rut]={'full_name':curso.profesor_sistema['full_name'],'cursos':[] }
        #         profesores[rut]['cursos'].append(curso.codigo)
        #
        #
        # del profesores['-0']
        # del profesores['90-6']
        # for profesor in profesores.iterkeys():
        #     xprofesor = Profesores()
        #     xprofesor.rut                = profesor
        #     xprofesor.full_name          = profesores[profesor]['full_name']
        #     xprofesor.passwd             = ""
        #     xprofesor.passwd_udp         = ""
        #     xprofesor.cursos             = profesores[profesor]['cursos']
        #     xprofesor.direccion          = ""
        #     xprofesor.region             = ""
        #     xprofesor.ciudad             = ""
        #     xprofesor.comuna             = ""
        #     xprofesor.departamento       = ""
        #     xprofesor.villa              = ""
        #     xprofesor.telefono           = ""
        #     xprofesor.correo_udp         = ""
        #     xprofesor.correo_respaldo    = ""
        #     xprofesor.save()
        #
        #
        # return profesores
        #
        #



api.add_resource(Test, '/Tests')

@test.route("/cas")
def run():
    codigos= {}
    materiales = Bilioteca_udp.query.filter({'codigo':'CIT1000'}).all()
    for material in materiales:
        material.responsable="NICOLAS ROSSO"
        material.save()
    return "adsf"
