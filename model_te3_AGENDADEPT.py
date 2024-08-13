class AGENDADEPT(db.Model):

    numAgenda=db.Column(db.Integer,primary_key=True)
    dateMAJ=db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self,numAgenda,dateMAJ):
        self.numAgenda=numAgenda
        self.dateMAJ=dateMAJ

class AGENDADEPTSchema(ma.Schema):
    class Meta:
        fields=('numAgenda','dateMAJ')
AGNEDADEPT_schema=AGENDADEPTSchema()
#hedhi kif yandou barcha
AGNEDADEPTS_schema=AGENDADEPTSchema(many=True)
#hedhi ti5dim
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


#BAZZZZZZZZ ti5dim

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
