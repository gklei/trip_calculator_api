from flask_restful import Resource
from models.expense import ExpenseItemModel
from models.student import StudentModel

class StudentBalance:
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

class StudentTransaction:
  from_student: StudentModel
  to_student: StudentModel
  amount: float

  def __init__(self, from_student: StudentModel, to_student: StudentModel, amount: float):
    self.from_student = from_student
    self.to_student = to_student
    self.amount = amount
  
  def json(self):
    return {
      'from': self.from_student.json(include_expense_items=False),
      'to': self.to_student.json(include_expense_items=False),
      'amount': self.amount
    }

class Calculate(Resource):
  def get(self):
    items = ExpenseItemModel.query.all()
    students = StudentModel.query.all()
    total = sum(i.amount for i in items)
    average_amount = total / len(students) if students else 0

    txns = [StudentBalance(student=s, balance=round(average_amount - s.total_expense_amount, 3)) for s in students]
    owes = [t for t in txns if t.balance > 0]
    owes.sort(key=lambda t: t.balance, reverse=True)

    owed = [t for t in txns if t.balance <= 0]
    owed.sort(key=lambda t: t.balance, reverse=True)

    from_index = 0
    to_index = 0
    transactions = []

    while from_index < len(owes) and to_index < len(owed):
      from_student = owes[from_index]
      to_student = owed[to_index]

      if abs(to_student.balance) >= from_student.balance:
        transactions.append(
          StudentTransaction(
            from_student=from_student.student,
            to_student=to_student.student,
            amount=from_student.balance
          )
        )
        to_student.balance += from_student.balance
        from_student.balance = 0
        from_index += 1
        if to_student.balance == 0:
          to_index += 1
      else:
        transactions.append(
          StudentTransaction(
            from_student=from_student.student,
            to_student=to_student.student,
            amount=abs(to_student.balance)
          )
        )
        from_student.balance += to_student.balance
        to_student.balance = 0
        to_index += 1

    return {
      'total_amount': total,
      'average_amount': average_amount,
      'txns': [t.json() for t in transactions],
    }
