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
class activites(db.Model):
    numActivite = db.Column(db.Integer, primary_key=True)
    typeA = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text)
    dateAct = db.Column(db.DateTime, default=datetime.datetime.now)
    hDebut = db.Column(db.DateTime, default=datetime.datetime.now)
    hFin = db.Column(db.DateTime, default=datetime.datetime.now)
    dateCreation = db.Column(db.DateTime, default=datetime.datetime.now)
    createur = db.Column(db.String(40), nullable=False)
    visible = db.Column(db.Integer)
    numAgenda = db.Column(db.Integer)


    def __init__(self, numActivite, typeA, description, dateAct, hDebut, hFin, dateCreation, createur, visible,numAgenda):
        self.numActivite = numActivite
        self.typeA = typeA
        self.description = description
        self.dateAct = dateAct
        self.hDebut = hDebut
        self.hFin = hFin
        self.dateCreation = dateCreation
        self.createur = createur
        self.visible = visible
        self.numAgenda = numAgenda


class ACTIVITYSCHEMA(ma.Schema):
    class Meta:
        fields = ('numActivite', 'typeA', 'description', 'dateAct', 'hDebut', 'hFin', 'dateCreation', 'createur', 'visible','numAgenda')


ACTIVITy_schema = ACTIVITYSCHEMA()
# hedhi kif yandou barcha
activites_schema = ACTIVITYSCHEMA(many=True)


# hedhi ti5dim
@app.route('/getACTIVITY', methods=['GET'])
def get_ACTIVITESDEPT():
    all_ACTIVI = activites.query.all()
    results = activites_schema.dump(all_ACTIVI)
    return jsonify(results)


# hedhi ti5dim
@app.route('/getACTIVITY/<numact>/', methods=['GET'])
def Department_det(numact):
    # article_det=Articles.query.get(id)
    ACT_det = activites.query.get(numact)
    return ACTIVITy_schema.jsonify(ACT_det)


# hedhi ti5dim
@app.route('/updateACTIVITY/<numact>/', methods=['PUT'])
def updateACTIVITESDEPT(numact):
    # article=Articles.query.get(id)
    dep = activites.query.get(numact)
    numActivite = request.json['numActivite']
    typeA = request.json['typeA']
    description = request.json['description']
    dateAct = request.json['dateAct']
    hDebut = request.json['hDebut']
    hFin = request.json['hFin']
    dateCreation = request.json['dateCreation']
    createur = request.json['createur']
    visible = request.json['visible']
    numAgenda = request.json['numAgenda']

    dep.numActivite = numActivite
    dep.typeA = typeA
    dep.description = description
    dep.dateAct = dateAct
    dep.hDebut = hDebut
    dep.hFin = hFin
    dep.dateCreation = dateCreation
    dep.createur = createur
    dep.visible = visible
    dep.numAgenda = numAgenda

    try:
        db.session.commit()
    except:
        print("updateMAJ activityp chy")
    return ACTIVITy_schema.jsonify(dep)


# hedhi ti5dim ama tal3itli rou7i
@app.route('/deleteACTIVITY/<numDep>/', methods=['DELETE'])
def delete_ACTIVITESDEPT(numDep):
    # article=Articles.query.get(id)
    dep = activites.query.get(numDep)
    print(dep)
    try:
        db.session.delete(dep)
        db.session.commit()
    except:
        print("delete ACTIVITY chy")
    return ACTIVITy_schema.jsonify(dep)


# BAZZZZZZZZ ti5dim

@app.route('/addACTIVITY', methods=['POST'])
def add_ACTIVITY():
    numActivite = request.json['numActivite']
    typeA = request.json['typeA']
    description = request.json['description']
    dateAct = request.json['dateAct']
    hDebut = request.json['hDebut']
    hFin = request.json['hFin']
    dateCreation = request.json['dateCreation']
    createur = request.json['createur']
    visible = request.json['visible']
    numAgenda = request.json['numAgenda']

    act = activites(numActivite, typeA, description, dateAct, hDebut, hFin, dateCreation, createur, visible,numAgenda)

    print(act)
    try:
        db.session.add(act)
        db.session.commit()
    except:
        print("o!oooooooooo")
    return activites.jsonify(act)


if __name__ == "__main__":
    app.run()
