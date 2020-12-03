from flask import Flask, jsonify
from flask_restful import Api

from resources.student import CreateStudent, DeleteStudent, StudentList
from resources.expense import ExpenseItem, DeleteExpenseItem, ExpenseItemList
from resources.calculate import Calculate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'ql_trip_calculator'
api = Api(app)

@app.before_first_request
def create_tables():
  db.create_all()
  
api.add_resource(CreateStudent, '/student')
api.add_resource(DeleteStudent, '/student/<string:student_id>')
api.add_resource(ExpenseItem, '/expense/<string:student_id>')
api.add_resource(DeleteExpenseItem, '/expense/<string:item_id>')
api.add_resource(StudentList, '/students')
api.add_resource(ExpenseItemList, '/expenses')
api.add_resource(Calculate, '/calculate')

if __name__ == '__main__':
  from db import db
  db.init_app(app)
  app.run(port=5000, debug=True)