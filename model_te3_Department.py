import datetime
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/projet_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)


# teb3a Departement lezimha test fazett Manytoone ***********************************************************************
# don't touch
class Departement(db.Model):
    num = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(40), nullable=False)
    num_chef = db.Column(db.Integer)
    num_agenda_dept = db.Column(db.Integer, db.ForeignKey('agendadepartment.num'))
    agenda_dept = db.relationship('AgendaDepartment', backref='department')

    def __init__(self, num, nom,num_chef,num_agenda_dept,agenda_dept):
        self.num = num
        self.nom = nom
        self.num_chef = num_chef
        self.num_agenda_dept = num_agenda_dept
        self.agenda_dept = agenda_dept

class DepartmentSchema(ma.Schema):
    class Meta:
        fields = ('num', 'nom', 'num_chef', 'num_agenda_dept')


DEPARTMENT_schema = DepartmentSchema()
# hedhi kif yandou barcha
DEPARTMENTS_schema = DepartmentSchema(many=True)


# hedhi ti5dim
@app.route('/getDepartment', methods=['GET'])
def get_Department():
    all_DEPTS = Departement.query.all()
    results = DEPARTMENT_schema.dump(all_DEPTS)
    return jsonify(results)


# hedhi ti5dim
@app.route('/getDepartment/<numDep>/', methods=['GET'])
def Department_det(numDep):
    # article_det=Articles.query.get(id)
    Dep_det = Departement.query.get(numDep)
    return DEPARTMENT_schema.jsonify(Dep_det)


# hedhi ti5dim
@app.route('/updateDepartment/<numDep>/', methods=['PUT'])
def updateDep(numDep):
    # article=Articles.query.get(id)
    dep = Departement.query.get(numDep)
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
        print("updateMAJ agendadepts chy")
    return DEPARTMENT_schema.jsonify(dep)


# hedhi ti5dim ama tal3itli rou7i
@app.route('/deleteDepartment/<numDep>/', methods=['DELETE'])
def delete_Art(numDep):
    # article=Articles.query.get(id)
    dep = Departement.query.get(numDep)
    print(dep)
    try:
        db.session.delete(dep)
        db.session.commit()
    except:
        print("delete chy")
    return DEPARTMENT_schema.jsonify(dep)


# a reviser one to many and many to one

# BAZZZZZZZZ ti5dim

@app.route('/addDepartment', methods=['POST'])
def add_Department():
    num = request.json['num']
    nom = request.json['nom']
    numChef = request.json['numChef']
    numAgendaDep = request.json['numAgendaDep']

    dept = Departement(num, nom, numChef, numAgendaDep)

    print(dept)
    try:
        db.session.add(dept)
        db.session.commit()
    except:
        print("o!oooooooooo")
    return DEPARTMENT_schema.jsonify(dept)


if __name__ == "__main__":
    app.run()
