from datetime import datetime
@app.route('/Register_vote', methods=['Post'])
def Alumno_voto():
    rut= request.form['rut']
    code = request.form['code']
    alumno = Alumnos.query.filter({'rut':rut}).first()
    if alumno== None:
        return "{'status':'ok'}"
    alumno.sufragar['Votaciones_2']={}
    alumno.sufragar['Votaciones_2']['habilitado']=False
    alumno.sufragar['Votaciones_2']['time']=datetime.now()
    alumno.sufragar['Votaciones_2']['code']=code
    return "{'status':'ok'}"
