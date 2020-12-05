from flask import jsonify
from flask_restful import Resource, reqparse
from models.expense import ExpenseItemModel
from models.student import StudentModel

class ExpenseItem(Resource):
  parser = reqparse.RequestParser()
  parser.add_argument('name',
      type=str,
      required=True,
      help="Every expense item needs a name."
  )
  parser.add_argument('amount',
      type=float,
      required=True,
      help="Every expense item needs an amount."
  )

  def get(self, student_id):
      items = ExpenseItemModel.find_by_student_id(student_id)
      if items is not None:
        return {
          'total_amount': sum(i.amount for i in items),
          'expense_items': [i.json() for i in items]
        }
      else:
        return {
          'message': 'Item not found'
        }, 404

  def post(self, student_id):
    data = ExpenseItem.parser.parse_args()
    name = data['name']
    amount = data['amount']

    if not StudentModel.find_by_id(student_id):
      return {
        'message': f"Student with id {student_id} does not exist"
      }, 400
    
    item = ExpenseItemModel(
      name=name,
      amount=amount,
      student_id=student_id
    )
    try:
      item.save_to_db()
    except:
      return {
        'message': 'An error occured while creating the expense item.'
      }, 500
    
    return item.json()

class DeleteExpenseItem(Resource):
  def delete(self, item_id):
    item = ExpenseItemModel.find_by_id(item_id)
    if item:
      item.delete_from_db()

    return {'message': 'Item deleted'}

class ExpenseItemList(Resource):
    def get(self):
      items = ExpenseItemModel.query.all()
      return {
        'total_amount': sum(i.amount for i in items),
        'expense_items': [i.json() for i in ExpenseItemModel.query.all()]
      }