from flask import jsonify
from flask_restful import Resource, reqparse
from models.expense import ExpenseItemModel
from models.student import StudentModel
from typing import Dict

class StudentTransaction:
  student: StudentModel
  starting: float
  balance: float

  def __init__(self, student: StudentModel, balance: float):
    self.student = student
    self.starting = balance
    self.balance = balance
    self.txns = {}
  
  @property
  def name(self):
    return self.student.name
  
  def json(self):
    return {
      **self.student.json(include_expense_items=False),
      'balance': self.balance,
      'starting': self.starting
    }

class Calculate(Resource):
  def get(self):
    items = ExpenseItemModel.query.all()
    students = StudentModel.query.all()
    total = sum(i.amount for i in items)
    average_amount = total / len(students) if students else 0

    txns = [StudentTransaction(student=s, balance=round(average_amount - s.total_expense_amount, 3)) for s in students]
    owes = [t for t in txns if t.balance > 0]
    owes.sort(key=lambda t: t.balance, reverse=True)

    owed = [t for t in txns if t.balance <= 0]
    owed.sort(key=lambda t: t.balance, reverse=True)

    from_index = 0
    to_index = 0
    messages = []

    while from_index < len(owes) and to_index < len(owed):
      from_student = owes[from_index]
      to_student = owed[to_index]

      if abs(to_student.balance) >= from_student.balance:
        messages.append(f'{from_student.name} gives {to_student.name} {-from_student.balance}')
        to_student.balance += from_student.balance
        from_student.balance = 0
        from_index += 1
        if to_student.balance == 0:
          to_index += 1
      else:
        messages.append(f'{from_student.name} gives {to_student.name} {to_student.balance}')
        from_student.balance += to_student.balance
        to_student.balance = 0
        to_index += 1

    return {
      'total_amount': total,
      'average_amount': average_amount,
      'txns': messages,
    }
