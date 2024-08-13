import datetime
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/projet_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)
class AGENDA(db.Model):
    numAgenda = db.Column(db.Integer, primary_key=True)
    dateCreation = db.Column(db.DateTime, default=datetime.datetime.now)
    numEmploye = db.Column(db.Text,db.ForeignKey('employe.numEmploye'))

    def __init__(self, numAgenda, dateCreation, numEmploye):
        self.numAgenda = numAgenda
        self.dateCreation = dateCreation
        self.numEmploye = numEmploye
class employe(db.Model):

    numEmploye = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.Text)
    prenom = db.Column(db.Text)
    telIntern = db.Column(db.Text)
    email = db.Column(db.Text)
    niveau = db.Column(db.Integer)
    numDept = db.Column(db.Integer,db.ForeignKey('agendadept.numAgenda'))

    def __init__(self, numEmploye, nom, prenom,telIntern,email,niveau,numDept):
        self.numEmploye = numEmploye
        self.nom = nom
        self.prenom = prenom
        self.telIntern = telIntern
        self.email = email
        self.niveau = niveau
        self.numDept = numDept
class AGENDADEPT(db.Model):

    numAgenda=db.Column(db.Integer,primary_key=True)
    dateMAJ=db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self,numAgenda,dateMAJ):
        self.numAgenda=numAgenda
        self.dateMAJ=dateMAJ
class departement(db.Model):
    num = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(40), nullable=False)
    numChef = db.Column(db.Integer,db.ForeignKey('employe.numEmploye'))
    numAgendaDept = db.Column(db.Integer, db.ForeignKey('agendadept.numAgenda'))


    def __init__(self, num, nom,numChef,numAgendaDept):
        self.num = num
        self.nom = nom
        self.numChef = numChef
        self.numAgendaDept = numAgendaDept
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
    numAgenda = db.Column(db.Integer,db.ForeignKey('agenda.numAgenda'))


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
        #hedhiactivities
class ACTIVITESDEPT(db.Model):
        numAct = db.Column(db.Integer, primary_key=True)
        typeD = db.Column(db.String(20), nullable=False)
        descript = db.Column(db.Text)
        dateAct = db.Column(db.DateTime, default=datetime.datetime.now)
        hDebut = db.Column(db.DateTime, default=datetime.datetime.now)
        hFin = db.Column(db.DateTime, default=datetime.datetime.now)
        dateCreation = db.Column(db.DateTime, default=datetime.datetime.now)
        createur = db.Column(db.String(40), nullable=False)
        numAgenda = db.Column(db.Integer,db.ForeignKey('agenda.numAgenda'))

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
class absent(db.Model):
    numEmploye = db.Column(db.Integer, primary_key=True)
    numActDept = db.Column(db.Integer, primary_key=True)
    motif = db.Column(db.Text)

    def __init__(self, numEmploye, numActDept, motif):
        self.numEmploye = numEmploye
        self.numActDept = numActDept
        self.motif = motif

class ACTIVITESDEPTSCHEMA(ma.Schema):
    class Meta:
        fields = ('numAct', 'typeD', 'descript', 'dateAct', 'hDebut', 'hFin', 'dateCreation', 'createur', 'numagenda')
ACTIVITESDEPT_schema = ACTIVITESDEPTSCHEMA()
ACTIVITESDEPTS_schema = ACTIVITESDEPTSCHEMA(many=True)
class ACTIVITYSCHEMA(ma.Schema):
    class Meta:
        fields = ('numActivite', 'typeA', 'description', 'dateAct', 'hDebut', 'hFin', 'dateCreation', 'createur', 'visible','numAgenda')

ACTIVITy_schema = ACTIVITYSCHEMA()
# hedhi kif yandou barcha
ACTIVITIES_schema = ACTIVITYSCHEMA(many=True)

# hedhi ti5dim
@app.route('/getACTIVITESDEPT', methods=['GET'])
def get_ACTIVITESDEPT():
    all_DEPTS = ACTIVITESDEPT.query.all()
    results = ACTIVITESDEPTS_schema.dump(all_DEPTS)
    return jsonify(results)

# hedhi ti5dim
@app.route('/getACTIVITESDEPT/<numact>/', methods=['GET'])
def activitydep_det(numact):
    # article_det=Articles.query.get(id)
    Dep_det = ACTIVITESDEPT.query.get(numact)
    return ACTIVITESDEPT_schema.jsonify(Dep_det)
@app.route('/updateACTIVITESDEPT/<numact>/', methods=['PUT'])
def updateACTIVITESDEPTs(numact):
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
def delete_ACTIVITYDEPSDEPT(numDep):
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

@app.route('/getACTIVITY', methods=['GET'])
def get_ACTIVITES():
    all_ACTIVI = activites.query.all()
    results = ACTIVITIES_schema.dump(all_ACTIVI)
    return jsonify(results)
@app.route('/getACTIVITY/<numact>/', methods=['GET'])
def activity_det(numact):
    # article_det=Articles.query.get(id)
    ACT_det = activites.query.get(numact)
    return ACTIVITy_schema.jsonify(ACT_det)
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
    return ACTIVITy_schema.jsonify(act)
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

# hedhi ti5dim ama tal3itli rou7i

#AGENDADEPT
class AGENDADEPTSchema(ma.Schema):
    class Meta:
        fields=('numAgenda', 'dateMAJ')
AGNEDADEPT_schema=AGENDADEPTSchema()
AGNEDADEPTS_schema=AGENDADEPTSchema(many=True)
#DEPARTMENT
class DepartmentSchema(ma.Schema):
    class Meta:
        fields = ('num', 'nom', 'num_chef', 'num_agenda_dept')
DEPARTMENT_schema = DepartmentSchema()
DEPARTMENTS_schema = DepartmentSchema(many=True)
# hedhi ti5dim
class EMPLOYEESCHEMA(ma.Schema):
    class Meta:
        fields = ('numEmploye', 'nom','prenom','telIntern','email','niveau','numDept')
EMPLOYEE_schema = EMPLOYEESCHEMA()
# hedhi kif yandou barcha
EMPLOYEES_SCHEMA = EMPLOYEESCHEMA(many=True)
@app.route('/getEMPLOYEES', methods=['GET'])
def get_employee():
    all_EMPL = employe.query.all()
    results = EMPLOYEES_SCHEMA.dump(all_EMPL)
    return jsonify(results)
@app.route('/getEMPLOYEE/<numamp>/', methods=['GET'])
def EMPLOYEE_det(numamp):
    # article_det=Articles.query.get(id)
    Dep_EMP = employe.query.get(numamp)
    return EMPLOYEE_schema.jsonify(Dep_EMP)
@app.route('/updateemploye/<numEMP>/', methods=['PUT'])
def updateemploye(numEMP):
    # article=Articles.query.get(id)
    EMP = employe.query.get(numEMP)
    print(EMP)
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
    return EMPLOYEE_schema.jsonify(EMP)

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
    return EMPLOYEE_schema.jsonify(dep)
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
    return EMPLOYEE_schema.jsonify(emp)


@app.route('/getDepartment', methods=['GET'])
def get_Department():
    all_DEPTS = departement.query.all()
    results = DEPARTMENTS_schema.dump(all_DEPTS)
    return jsonify(results)

@app.route('/getDepartment/<numDep>/', methods=['GET'])
def Department_det(numDep):
    Dep_det = departement.query.get(numDep)
    print(Dep_det)
    return DEPARTMENT_schema.jsonify(Dep_det)

@app.route('/updateDepartment/<numDep>/', methods=['PUT'])
def updateDep(numDep):

    dep = departement.query.get(numDep)
    num = request.json['num']
    nom = request.json['nom']
    num_chef = request.json['numChef']
    numAgendaDept = request.json['numAgendaDept']
    dep.num = num
    dep.nom = nom
    dep.num_chef = num_chef
    dep.numAgendaDept = numAgendaDept

    try:
        db.session.commit()
    except:
        print("updateMAJ department chy")
    return DEPARTMENT_schema.jsonify(dep)
@app.route('/deleteDepartment/<numDep>/', methods=['DELETE'])
def delete_department(numDep):
    # article=Articles.query.get(id)
    dep = departement.query.get(numDep)
    print(dep)
    try:
        db.session.delete(dep)
        db.session.commit()
    except:
        print("delete department fechla  chy")
    return DEPARTMENT_schema.jsonify(dep)
@app.route('/addDepartment', methods=['POST'])
def add_Department():

    num = request.json['num']
    nom = request.json['nom']
    num_chef = request.json['numChef']
    numAgendaDept = request.json['numAgendaDept']
    dept = departement(num, nom, num_chef, numAgendaDept)
    print(dept)
    try:
        db.session.add(dept)
        db.session.commit()
    except:
        print("o!oooooooooo")
    return DEPARTMENT_schema.jsonify(dept)

@app.route('/getAGENDAS', methods=['GET'])
def get_AGNEDADEPS():
    all_DEPTS=AGENDADEPT.query.all()
    results=AGNEDADEPTS_schema.dump(all_DEPTS)
    return jsonify(results)
#hedhi ti5dim
@app.route('/getAGENDAS/<numAgenda>/', methods=['GET'])
def article_det(numAgenda):
    #article_det=Articles.query.get(id)
    agendadep_det=AGENDADEPT.query.get(numAgenda)
    return AGNEDADEPT_schema.jsonify(agendadep_det)
#hedhi ti5dim
@app.route('/updateMAJAGENDA/<numAgenda>/', methods=['PUT'])
def updateMAJArt(numAgenda):
    #article=Articles.query.get(id)
    agendadep=AGENDADEPT.query.get(numAgenda)
    id=request.json['numAgenda']
    dateMAJ=request.json['dateMAJ']
    agendadep.numAgenda=numAgenda
    agendadep.dateMAJ=dateMAJ
    try:
        db.session.commit()
    except:
        print("updateMAJ agendadepts chy")
    return  AGNEDADEPT_schema.jsonify(agendadep)

#hedhi ti5dim ama tal3itli rou7i
@app.route('/deleteAGENDADEP/<numAgenda>/', methods=['DELETE'])
def delete_Art(numAgenda):
    #article=Articles.query.get(id)
    agendadep=AGENDADEPT.query.get(numAgenda)
    print(agendadep)
    try:
        db.session.delete(agendadep)
        db.session.commit()
    except:
        print("delete chy")
    return  AGNEDADEPT_schema.jsonify(agendadep)

@app.route('/add',methods= ['POST'])
def add_articles():
    numAgenda=request.json['numAgenda']
    dateMAJ=request.json['dateMAJ']
    agendadept=AGENDADEPT(numAgenda,dateMAJ)

    print(agendadept)
    try:
        db.session.add(agendadept)
        db.session.commit()
    except:
        print("o!oooooooooo")
    return AGNEDADEPT_schema.jsonify(agendadept)


if __name__ == "__main__":
    app.run()
