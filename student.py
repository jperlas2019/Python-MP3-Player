from sqlalchemy import Column, Text
from base import Base


class Student(Base):
    """ Student class """

    """ ORM: map db columns to instance variables in this class """
    __tablename__ = "student_tbl"
    student_id = Column(Text, primary_key=True)
    first_name = Column(Text, nullable=False)
    last_name = Column(Text, nullable=False)

    def __init__(self, student_id: str,
                       first_name: str = "-",
                       last_name: str = "-"):
        """ Validate and set initial values """
        self.student_id = student_id
        self.first_name = first_name
        self.last_name = last_name

    def update(self, new_data: object):
        """ Copy all changes fields into the actual object (self). """
        if not isinstance(new_data, Student):
            raise TypeError("new_data must be a Student object")
        if new_data.student_id != self.student_id:
            raise ValueError("Student ID cannot be changed")
        self.first_name = new_data.first_name
        self.last_name = new_data.last_name

    def to_dict(self):
        """ Return dictionary of instance state """
        output = dict()
        output["student_id"] = self.student_id
        output["first_name"] = self.first_name
        output["last_name"] = self.last_name

        return output

    @staticmethod
    def from_dict(d):
        """ Create and return instance from dictionary """
        for val in ("first_name", "last_name", "student_id"):
            if val not in d.keys():
                raise ValueError("Invalid dict")

        instance = Student(student_id=d["student_id"],
                           first_name=d["first_name"],
                           last_name=d["last_name"])
        return instance

    def __str__(self):
        return f"<Student {self.first_name} {self.last_name} " \
               f"({self.student_id})>"
