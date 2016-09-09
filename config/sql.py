from flask_sqlalchemy import SQLAlchemy
user="postgresql"
passwd="mmae2010"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://%s:%s@localhost/votaciones"%(user,passwd)
db = SQLAlchemy(app)