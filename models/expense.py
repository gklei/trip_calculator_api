from db import db

class ExpenseItemModel(db.Model):
  __tablename__ = 'expenseitems'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80))
  amount = db.Column(db.Float)

  student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
  student = db.relationship('StudentModel')

  def __init__(self, name: str, amount: float, student_id: int):
    self.name = name
    self.amount = amount
    self.student_id = student_id

  def json(self):
    return {
      'id': self.id,
      'name': self.name,
      'amount': self.amount,
      'student_id': self.student_id,
      'student_name': self.student.name
    }

  def save_to_db(self):
    db.session.add(self)
    db.session.commit()

  def delete_from_db(self):
      db.session.delete(self)
      db.session.commit()
  
  @classmethod
  def find_by_student_id(cls, student_id):
    return cls.query.filter_by(student_id=student_id).all()
  
  @classmethod
  def find_by_id(cls, _id):
    return cls.query.filter_by(id=_id).first()