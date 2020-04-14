from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base

from student import Student


class StudentManager:
    """
    The StudentManager class is responsible for coordinating all transactions
    between the higher level programs that use the data, and the actual
    database. Since each transaction is one of the crud operations (create,
    read, update, delete) we provide methods for each of these techniques.

    The class basically just reads and writes data to the database. The
    constructor sets up the initial connection (student object <-> database)
    and each of the other methods performs an autonomous transaction (ie:
    open db session, interact with db, commit changes, close session.
    """

    def __init__(self, student_db):
        """ Creates a Student object and map to the Database """

        if student_db is None or student_db == "":
            raise ValueError(f"Student database [{student_db}] not found")

        engine = create_engine('sqlite:///' + student_db)
        Base.metadata.bind = engine
        self._db_session = sessionmaker(bind=engine)

    def add_student(self, new_student: Student):
        """ Adds a new student to the student database """

        if new_student is None or not isinstance(new_student, Student):
            raise ValueError("Invalid Student Object")

        session = self._db_session()
        session.add(new_student)

        session.commit()

        student_id = new_student.student_id
        session.close()

        return student_id

    def update_student(self, student):
        """ Update existing student to match student_upd """
        if student is None or not isinstance(student, Student):
            raise ValueError("Invalid Student Object")

        session = self._db_session()

        existing_student = session.query(Student).filter(
                Student.student_id == student.student_id).first()
        if existing_student is None:
            raise ValueError(f"Student {student.student_id} does not exist")

        existing_student.update(student)

        session.commit()
        session.close()

    def get_student(self, student_id):
        """ Return student object matching ID"""
        if student_id is None or type(student_id) != str:
            raise ValueError("Invalid Student ID")

        session = self._db_session()

        student = session.query(Student).filter(
                Student.student_id == student_id).first()

        session.close()

        return student

    def delete_student(self, student_id):
        """ Delete a student from the database """
        if student_id is None or type(student_id) != str:
            raise ValueError("Invalid Student ID")

        session = self._db_session()

        student = session.query(Student).filter(
                Student.student_id == student_id).first()
        if student is None:
            session.close()
            raise ValueError("Student does not exist")

        session.delete(student)
        session.commit()

        session.close()

    def get_all_students(self):
        """ Return a list of all students in the DB """
        session = self._db_session()

        all_students = session.query(Student).all()

        session.close()

        return all_students
