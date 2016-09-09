from core.core import app
from flask.ext.mongoalchemy import MongoAlchemy
app.config['MONGOALCHEMY_DATABASE'] = 'UDP'
db = MongoAlchemy(app)