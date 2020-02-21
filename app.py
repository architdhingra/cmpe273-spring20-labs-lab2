from flask import Flask, escape, request, jsonify
import json

app = Flask(__name__)
id = 1234456
cid = 1122334
data  =   {
    "students":[
        {
            "first_name" : "Mark",
            "last_name"  : "Justin",
            "id" : 110
         },
         {
            "first_name" : "Sean",
            "last_name"  : "Paul",
            "id" : 111
         }
    ],
    "classes" :[
        {
            "class_name" : "CMPE273",
            "class_id"   : 273
        },
        {
            "class_name" : "CMPE272",
            "class_id"   : 272
        },
        {
            "class_name" : "CMPE274",
            "class_id"   : 274
        }
    ]
}

@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'

@app.route('/students', methods=['POST'])
def createStudent():
    global id, data
    cc = request.get_json()
    data['students'].append({'id' : id, 'first_name': cc['name']})
    student = [stud for stud in data['students'] if stud["first_name"] == (cc['name'])]
    id = id+1
    return jsonify({"student":student})

@app.route('/students/<id>', methods=['GET'])
def getStudent(id):
    student = [stud for stud in data['students'] if stud["id"] == int(request.view_args['id'])]
    return jsonify({"student":student})

@app.route('/classes', methods=['POST'])
def createClass():
    global cid, data
    cc = request.get_json()
    data['classes'].append({'class_id' : cid, 'class_name': cc['name']})
    student = [stud for stud in data['classes'] if stud["class_name"] == (cc['name'])]
    cid = cid+1
    return jsonify({"Class":student})

@app.route('/classes/<id>', methods=['GET'])
def getClass(id):
    cl = [cl for cl in data['classes'] if cl["class_id"] == int(request.view_args['id'])]
    return jsonify({"Class":cl})

@app.route('/classes/<id>', methods=['PATCH'])
def updateClass(id):
    cc = request.get_json()
    stud = [stud for stud in data['students'] if stud["id"] == int(cc['student_id'])]
    index = 0
    for x in data['classes']:
        index = index+1
        if x["class_id"] == int(request.view_args['id']):
            cl = x
            break
    
    if ('students' in cl):
        flag = False
        for y in cl['students']:
            if y['id'] == int(cc['student_id']):
                flag = True
                return "Student Already Exists in the class"
        if (flag == False):
            data['classes'][index-1]['students'].extend(stud)
    else:
        data['classes'][index-1].update({'students' : stud})

    return jsonify({"Class": cl})
