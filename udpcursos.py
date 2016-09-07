from core.core import *
from services.Info import simple_page
#from services.Upload import upload
from services.acceso import check
from services.Test import test

app.register_blueprint(test, url_prefix='/test')
app.register_blueprint(simple_page, url_prefix='/api')
#app.register_blueprint(upload, url_prefix='/upload')
app.register_blueprint(check, url_prefix='/check')


print "HOLAA!"




if __name__ =="__main__" and True:
    app.run(host='0.0.0.0',debug=True,port=5010)
    #socketio.port=5001
    #socketio.host="0.0.0.0"
    #socketio.run(app, host='0.0.0.0')
