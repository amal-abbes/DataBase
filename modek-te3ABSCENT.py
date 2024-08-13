import datetime
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/projet_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)


# teb3a absent lezimha test fazett Manytoone ***********************************************************************
# don't touch
class absent(db.Model):
    numEmploye = db.Column(db.Integer, primary_key=True)
    numActDept = db.Column(db.Integer, primary_key=True)
    motif = db.Column(db.Text)

    def __init__(self, numEmploye, numActDept, motif):
        self.numEmploye = numEmploye
        self.numActDept = numActDept
        self.motif = motif


class ABSENTSCHEMA(ma.Schema):
    class Meta:
        fields = ('numEmploye', 'numActDept', 'motif')


ABSENT_schema = ABSENTSCHEMA()
# hedhi kif yandou barcha
ABSCNETS_SCHEMA = ABSENTSCHEMA(many=True)


# hedhi ti5dim
@app.route('/getABSENTS', methods=['GET'])
def get_ACTIVITESDEPT():
    all_abs = absent.query.all()
    results = ABSCNETS_SCHEMA.dump(all_abs)
    return jsonify(results)


# hedhi ti5dim
# @app.route('/get/<numact>/', methods=['GET'])
# def Department_det(numact):
#    # article_det=Articles.query.get(id)
#    ACT_det = ACTIVITIES.query.get(numact)
#    return ACTIVITy_schema.jsonify(ACT_det)


# hedhi ti5dim
@app.route('/updateABSENT/<numemp>/<numActDept>/', methods=['PUT'])
def updateABSENT(numemp, numActDept):
    # article=Articles.query.get(id)
    dep = absent.query.get(numemp, numActDept)
    numEmploye = request.json['numEmploye']
    numActDept = request.json['numActDept']
    motif = request.json['motif']

    dep.numEmploye = numEmploye
    dep.numActDept = numActDept
    dep.motif = motif

    try:
        db.session.commit()
    except:
        print("updateMAJ abscent chy")
    return ABSENT_schema.jsonify(dep)


# hedhi ti5dim ama tal3itli rou7i
@app.route('/deleteABSCENT/<numemp>/<numActDept>', methods=['DELETE'])
def delete_ACTIVITESDEPT(numemp, numActDept):
    # article=Articles.query.get(id)
    dep = absent.query.get(numemp, numActDept)
    print(dep)
    try:
        db.session.delete(dep)
        db.session.commit()
    except:
        print("delete abscent chy")
    return ABSENT_schema.jsonify(dep)


# BAZZZZZZZZ ti5dim

@app.route('/addABSENT', methods=['POST'])
def add_ABSCENT():
    numActivite = request.json['numActivite']
    numActDept = request.json['numActDept']
    motif = request.json['motif']

    act = absent(numActivite, numActDept, motif)

    print(act)
    try:
        db.session.add(act)
        db.session.commit()
    except:
        print("o!oooooooooo")
    return absent.jsonify(act)


if __name__ == "__main__":
    app.run()
