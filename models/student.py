from db import db

class StudentModel(db.Model):
  __tablename__ = 'students'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80))
  expense_items = db.relationship('ExpenseItemModel', lazy='dynamic')

  def __init__(self, name: str):
    self.name = name

  @property
  def total_expense_amount(self) -> float:
    return sum(i.amount for i in self.expense_items.all())

  def save_to_db(self):
    db.session.add(self)
    db.session.commit()

  def delete_from_db(self):
    for i in self.expense_items.all():
      db.session.delete(i)

    db.session.delete(self)
    db.session.commit()

  def json(self, include_expense_items: bool=True):
      return {
        'id': self.id, 
        'name': self.name,
        'total_expense_amount': self.total_expense_amount,
        **({'expense_items': [i.json() for i in self.expense_items.all()]} if include_expense_items else {})
      }
  
  @classmethod
  def find_by_name(cls, name):
    return cls.query.filter_by(name=name).first()
  
  @classmethod
  def find_by_id(cls, _id):
    return cls.query.filter_by(id=_id).first()