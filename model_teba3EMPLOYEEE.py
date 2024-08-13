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
class employe(db.Model):

    numEmploye = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.Text)
    prenom = db.Column(db.Text)
    telIntern = db.Column(db.Text)
    email = db.Column(db.Text)
    niveau = db.Column(db.Integer)
    numDept = db.Column(db.Integer)
    def __init__(self, numEmploye, nom,prenom,telIntern,email,niveau,numDept):
        self.numEmploye = numEmploye
        self.nom = nom
        self.prenom = prenom
        self.telIntern = telIntern
        self.email = email
        self.niveau = niveau
        self.numDept = numDept





class employeSCHEMA(ma.Schema):
    class Meta:
        fields = ('numEmploye', 'nom','prenom','telIntern','email','niveau','numDept')


employe_schema = employeSCHEMA()
# hedhi kif yandou barcha
employeS_SCHEMA = employeSCHEMA(many=True)


# hedhi ti5dim
@app.route('/getemployeS', methods=['GET'])
def get_ACTIVITESDEPT():
    all_EMPL = employe.query.all()
    results = employeS_SCHEMA.dump(all_EMPL)
    return jsonify(results)


# hedhi ti5dim
@app.route('/getemploye/<numamp>/', methods=['GET'])
def employe_det(numamp):
    # article_det=Articles.query.get(id)
    Dep_EMP = employe.query.get(numamp)
    return employe_schema.jsonify(Dep_EMP)


# hedhi ti5dim
@app.route('/updateemploye/<numEMP>/', methods=['PUT'])
def updateemploye(numEMP):
    # article=Articles.query.get(id)
    EMP = employe.query.get(numEMP)
    numEmploye = request.json['numEmploye']
    nom = request.json['nom']
    prenom = request.json['prenom']
    telIntern = request.json['telIntern']
    email = request.json['email']
    niveau = request.json['niveau']
    numDept = request.json['numDept']



    EMP.numEmploye = numEmploye
    EMP.nom = nom
    EMP.prenom = prenom
    EMP.telIntern = telIntern
    EMP.email = email
    EMP.niveau = niveau
    EMP.numDept = numDept


    try:
        db.session.commit()
    except:
        print("updateMAJ employe chy")
    return employe_schema.jsonify(EMP)


# hedhi ti5dim ama tal3itli rou7i
@app.route('/deleteemploye/<emp>/', methods=['DELETE'])
def delete_employe(emp):
    # article=Articles.query.get(id)
    dep = employe.query.get(emp)
    print(dep)
    try:
        db.session.delete(dep)
        db.session.commit()
    except:
        print("delete employeE chy")
    return employe_schema.jsonify(dep)

# BAZZZZZZZZ ti5dim

@app.route('/addemploye', methods=['POST'])
def add_employe():

    numEmploye = request.json['numEmploye']
    nom = request.json['nom']
    prenom = request.json['prenom']
    telIntern = request.json['telIntern']
    email = request.json['email']
    niveau = request.json['niveau']
    numDept = request.json['numDept']


    emp = employe(numEmploye,nom,prenom,telIntern,email,niveau,numDept)

    print(emp)
    try:
        db.session.add(emp)
        db.session.commit()
    except:
        print("employeE ADD NOOOOOOO")
    return employe_schema.jsonify(emp)


if __name__ == "__main__":
    app.run()
