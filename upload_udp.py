from flask import Flask,jsonify,request
from werkzeug.utils import secure_filename
import os
import random
from datetime import datetime

#Codigo para que le permita consular el usuario
UPLOAD_CODE="P3ZdBX3aIGsW0qtQAFaz"
# Url del archivo



#Fin de sona editable



upload={}

@app.route('/Upload', methods=['POST'])
def upload_file():

    if request.method == 'POST':
        flowIdentifier = request.form['flowIdentifier']

        categoria=request.form['categoria']
        codigo=request.form['codigo']
        token=request.form['token']
        archivo=request.form['flowFilename']

        if current_chunk == 1 and check_user(request.form['token'],request.form['hash_id']) :
            return {'access':False}

        current_chunk  = int(request.form["flowChunkNumber"])
        total_chunks   = int(request.form["flowTotalChunks"])

        file = request.files['file']
        filename = secure_filename(file.filename)

        if (os.path.exists('static/'+codigo))==False:
            os.makedirs('static/'+codigo)
        if (os.path.exists('static/'+codigo+"/"+categoria))==False:
            os.makedirs('static/'+codigo+"/"+categoria)

        if flowIdentifier not in upload:

            nombre=filename.split(".")
            nombre[len(nombre)-2]=nombre[len(nombre)-2]+"_"+str(random.getrandbits(5))
            nombre=".".join(nombre)
            upload[flowIdentifier]=nombre
            F = open(os.path.join('static/'+codigo+"/"+categoria, nombre), "wb")
        else:
            nombre = upload[flowIdentifier]
            F = open(os.path.join('static/'+codigo+"/"+categoria, nombre), "a")


        F.write(file.read())
        F.close()

        if current_chunk != total_chunks:
          return "{}"



        return jsonify(File=B.json())

if __name__ =="__main__" and True:
    app.run(host='0.0.0.0',debug=True)