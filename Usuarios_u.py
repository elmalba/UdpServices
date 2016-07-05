from core.core  import *
from json import dumps

def Get_Alumnos():

    alumnos={}

    for usuario in Alumnos.query.all():
        alumnos[usuario.rut]={'carrera':usuario.carrera,'hash_id':str(usuario.mongo_id),'rut':usuario.rut,'full_name':usuario.full_name }


    CURSOSX =   Cursosx.query.filter().all()
    for cursos in CURSOSX:
        for usuario in  cursos.alumnos:
            if usuario['rut'] not in alumnos:
                rut = usuario['rut']
                alumnos[usuario['rut']]={'rut':rut,'full_name':usuario['full_name']}
    return alumnos

# data = Get_Alumnos()
# with open('user.json', 'w') as outfile:
#     outfile.write(dumps(data, sort_keys = True, ensure_ascii=False))



def problem():

    CURSOSX =   Cursosx.query.filter({'alumnos':{'$elemMatch': {'rut': '-0'}}}).all()
    for cursos in CURSOSX:
        for usuario in  cursos.alumnos:
            if usuario['rut'] =='-0':
                print usuario['full_name']
problem()