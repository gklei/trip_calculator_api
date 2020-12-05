from flask_restful import Resource, reqparse
from models.student import StudentModel

class CreateStudent(Resource):
  parser = reqparse.RequestParser()
  parser.add_argument('name',
      type=str,
      required=True,
      help="Every student needs a name."
  )

  def post(self):
    data = CreateStudent.parser.parse_args()
    name = data['name']

    if StudentModel.find_by_name(name):
        return {'message': "Student '{}' already exists".format(name)}, 400
    
    student = StudentModel(name)
    try:
      student.save_to_db()
    except:
      return {'message': 'An error occured while creating the student'}, 500
    
    return student.json()

class DeleteStudent(Resource):
  def delete(self, student_id):
    student = StudentModel.find_by_id(student_id)
    if student:
      student.delete_from_db()
    
    return {
      'students': [s.json() for s in StudentModel.query.all()]
    }

class StudentList(Resource):
  def get(self):
    return {
      'students': [s.json() for s in StudentModel.query.all()]
    }