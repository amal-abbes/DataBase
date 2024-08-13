import datetime
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/projet_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)


# teb3a AGENDA lezimha test fazett Manytoone ***********************************************************************
# don't touch
class AGENDA(db.Model):
    numAgenda = db.Column(db.Integer, primary_key=True)
    dateCreation = db.Column(db.DateTime, default=datetime.datetime.now)
    numEmploye = db.Column(db.Text)

    def __init__(self, numAgenda, dateCreation, numEmploye):
        self.numAgenda = numAgenda
        self.dateCreation = dateCreation
        self.numEmploye = numEmploye


class AGENDASCHEMA(ma.Schema):
    class Meta:
        fields = ('numAgenda', 'dateCreation', 'numEmploye')


AGENDASCHEMA_schema = AGENDASCHEMA()
# hedhi kif yandou barcha
AGENDASCHEMAS_schema = AGENDASCHEMA(many=True)


# hedhi ti5dim
@app.route('/getAGENDA', methods=['GET'])
def get_ACTIVITESDEPT():
    all_DEPTS = AGENDA.query.all()
    results = AGENDASCHEMAS_schema.dump(all_DEPTS)
    return jsonify(results)


# hedhi ti5dim
@app.route('/getAGENDA/<numagd>/', methods=['GET'])
def Department_det(numagd):
    # article_det=Articles.query.get(id)
    Dep_det = AGENDA.query.get(numagd)
    return AGENDASCHEMA_schema.jsonify(Dep_det)


# hedhi ti5dim
@app.route('/updateAGENDA/<numagd>/', methods=['PUT'])
def updateACTIVITESDEPT(numagd):
    # article=Articles.query.get(id)
    dep = AGENDA.query.get(numagd)
    numAgenda = request.json['numAgenda']
    dateCreation = request.json['dateCreation']
    numEmploye = request.json['numEmploye']

    dep.numAct = numAgenda
    dep.typeD = dateCreation
    dep.dateAct = numEmploye

    try:
        db.session.commit()
    except:
        print("updateMAJ AGENDA chy")
    return AGENDASCHEMA_schema.jsonify(dep)


# hedhi ti5dim ama tal3itli rou7i
@app.route('/deleteAGENDA/<agd>/', methods=['DELETE'])
def delete_ACTIVITESDEPT(numDep):
    # article=Articles.query.get(id)
    dep = AGENDA.query.get(numDep)
    print(dep)
    try:
        db.session.delete(dep)
        db.session.commit()
    except:
        print("delete AGENDA chy")
    return AGENDASCHEMA_schema.jsonify(dep)


# BAZZZZZZZZ ti5dim

@app.route('/addAGENDA', methods=['POST'])
def add_AGENDA():
    numAgenda = request.json['numAgenda']
    dateCreation = request.json['dateCreation']
    numEmploye = request.json['numEmploye']

    dept = AGENDA(numAgenda, dateCreation, numEmploye)

    print(dept)
    try:
        db.session.add(dept)
        db.session.commit()
    except:
        print("o!oooooooooo")
    return AGENDA.jsonify(dept)


if __name__ == "__main__":
    app.run()
