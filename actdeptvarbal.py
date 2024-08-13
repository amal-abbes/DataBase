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
class actdeptverbal(db.Model):
    numAct = db.Column(db.Integer, primary_key=True)
    numProcesV = db.Column(db.Integer, primary_key=True)

    def __init__(self, numAct, numProcesV):
        self.numAct = numAct
        self.numProcesV = numProcesV


class actdeptverbalSCHEMA(ma.Schema):
    class Meta:
        fields = ('numAct', 'numProcesV')


actdeptverbal_schema = actdeptverbalSCHEMA()
# hedhi kif yandou barcha
actdeptverbals_SCHEMA = actdeptverbalSCHEMA(many=True)


# hedhi ti5dim
@app.route('/getactdeptverbal', methods=['GET'])
def get_actdeptverbal():
    all_abs = actdeptverbal.query.all()
    results = actdeptverbals_SCHEMA.dump(all_abs)
    return jsonify(results)


# hedhi ti5dim
# @app.route('/get/<numact>/', methods=['GET'])
# def Department_det(numact):
#    # article_det=Articles.query.get(id)
#    ACT_det = ACTIVITIES.query.get(numact)
#    return ACTIVITy_schema.jsonify(ACT_det)


@app.route('/addactdeptverbals', methods=['POST'])
def add_actdeptverbal():
    numAct = request.json['numAct']
    numProcesV = request.json['numProcesV']

    act = actdeptverbal(numAct, numProcesV)

    print(act)
    try:
        db.session.add(act)
        db.session.commit()
    except:
        print("o!oooooooooo")
    return actdeptverbal.jsonify(act)


if __name__ == "__main__":
    app.run()
