import datetime
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/projet_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)


# teb3a ACTIVITYSDEPT lezimha test fazett Manytoone ***********************************************************************
# don't touch
class ACTIVITESDEPT(db.Model):
    numAct = db.Column(db.Integer, primary_key=True)
    typeD = db.Column(db.String(20), nullable=False)
    descript = db.Column(db.Text)
    dateAct = db.Column(db.DateTime, default=datetime.datetime.now)
    hDebut = db.Column(db.DateTime, default=datetime.datetime.now)
    hFin = db.Column(db.DateTime, default=datetime.datetime.now)
    dateCreation = db.Column(db.DateTime, default=datetime.datetime.now)
    createur = db.Column(db.String(40), nullable=False)
    numagenda = db.Column(db.Integer)

    def __init__(self, numAct, typeD, descript, dateAct, hDebut, hFin, dateCreation, createur, numagenda):
        self.numAct = numAct
        self.typeD = typeD
        self.descript = descript
        self.dateAct = dateAct
        self.hDebut = hDebut
        self.hFin = hFin
        self.dateCreation = dateCreation
        self.createur = createur
        self.numagenda = numagenda


class ACTIVITESDEPTSCHEMA(ma.Schema):
    class Meta:
        fields = ('numAct', 'typeD', 'descript', 'dateAct', 'hDebut', 'hFin', 'dateCreation', 'createur', 'numagenda')


ACTIVITESDEPT_schema = ACTIVITESDEPTSCHEMA()
# hedhi kif yandou barcha
ACTIVITESDEPTS_schema = ACTIVITESDEPTSCHEMA(many=True)


# hedhi ti5dim
@app.route('/getACTIVITESDEPT', methods=['GET'])
def get_ACTIVITESDEPT():
    all_DEPTS = ACTIVITESDEPT.query.all()
    results = ACTIVITESDEPTS_schema.dump(all_DEPTS)
    return jsonify(results)


# hedhi ti5dim
@app.route('/getACTIVITESDEPT/<numact>/', methods=['GET'])
def Department_det(numact):
    # article_det=Articles.query.get(id)
    Dep_det = ACTIVITESDEPT.query.get(numact)
    return ACTIVITESDEPT_schema.jsonify(Dep_det)


# hedhi ti5dim
@app.route('/updateACTIVITESDEPT/<numact>/', methods=['PUT'])
def updateACTIVITESDEPT(numact):
    # article=Articles.query.get(id)
    dep = ACTIVITESDEPT.query.get(numact)
    numAct = request.json['numAct']
    typeD = request.json['typeD']
    decript = request.json['decript']
    dateAct = request.json['dateAct']
    hDebut = request.json['hDebut']
    hFin = request.json['hFin']
    dateCreation = request.json['dateCreation']
    createur = request.json['createur']
    numAgenda = request.json['numAgenda']

    dep.numAct = numAct
    dep.typeD = typeD
    dep.dateAct = dateAct
    dep.decript = decript
    dep.hDebut = hDebut
    dep.hFin = hFin
    dep.dateCreation = dateCreation
    dep.createur = createur
    dep.numAgenda = numAgenda

    try:
        db.session.commit()
    except:
        print("updateMAJ activitiesDep chy")
    return ACTIVITESDEPT_schema.jsonify(dep)


# hedhi ti5dim ama tal3itli rou7i
@app.route('/deleteACTIVITESDEPT/<numDep>/', methods=['DELETE'])
def delete_ACTIVITESDEPT(numDep):
    # article=Articles.query.get(id)
    dep = ACTIVITESDEPT.query.get(numDep)
    print(dep)
    try:
        db.session.delete(dep)
        db.session.commit()
    except:
        print("delete ACTIVITYDEP chy")
    return ACTIVITESDEPT_schema.jsonify(dep)


# BAZZZZZZZZ ti5dim

@app.route('/addACTIVITYDEP', methods=['POST'])
def add_ACTIVITYDEP():
    numAct = request.json['numAct']
    typeD = request.json['typeD']
    decript = request.json['decript']
    dateAct = request.json['dateAct']
    hDebut = request.json['hDebut']
    hFin = request.json['hFin']
    dateCreation = request.json['dateCreation']
    createur = request.json['createur']
    numAgenda = request.json['numAgenda']

    dept = ACTIVITESDEPT(numAct, typeD, decript, dateAct, hDebut, hFin, dateCreation, createur, numAgenda)

    print(dept)
    try:
        db.session.add(dept)
        db.session.commit()
    except:
        print("o!oooooooooo")
    return ACTIVITESDEPT.jsonify(dept)


if __name__ == "__main__":
    app.run()
