## Testovaci skript
#
#  @file testing_script.py
#  @author Hung Do
from sortsubj import *
import pytest
import unittest

def test_empty_obj():
    s = SubSort()
    assert len(s.students) == 0
    assert len(s.days) == 0
    assert len(s.subject) == 0
    assert s.nof_sorted_students == 0

def test_add_student():
    s: SubSort = SubSort()
    assert s.add_student(1, "tvoje", "mama", "trida", None)
    assert s.add_student(2, "Student", "2", "lol", ("s1", "s2"))
    assert s.add_student("Proste nejake id", "Student", "2", "lol", ("s1", "s2"))

    # chybne pridani -> student jiz existuje
    assert not s.add_student(1, "ahoj", "mami", "lol", ("s1", "s2"))
    with pytest.raises(Exception):
        s.add_student(None, "jmeno", "prijmeni", "trida", None)

    assert len(s.students) == 3

    assert 1 in s.students
    assert 2 in s.students
    assert "Proste nejake id" in s.students

    student = s.students[1]
    assert student.first_name == "tvoje"
    assert student.last_name == "mama"
    assert student.class_id == "trida"
    assert student.subjects == None

def test_delete_student():
    s: SubSort = SubSort()
    assert s.add_student(1, "tvoje", "mama", "trida", None)
    assert s.add_student(2, "Student", "2", "lol", ("s1", "s2"))
    assert s.add_student("Proste nejake id", "Student", "2", "lol", ("s1", "s2"))

    assert len(s.students) == 3

    assert not s.delete_student(5)
    assert not s.delete_student("ahoj")
    assert s.delete_student(1)

    assert len(s.students) == 2
    assert not 1 in s.students

    assert s.delete_student(2)
    assert s.delete_student("Proste nejake id")

    assert len(s.students) == 0

def test_delete_students():
    s: SubSort = SubSort()
    assert s.add_student(1, "tvoje", "mama", "trida", None)
    assert s.add_student(2, "Student", "2", "lol", ("s1", "s2"))
    assert s.add_student("Proste nejake id", "Student", "2", "lol", ("s1", "s2"))

    s.delete_students([1, 2, 3])
    assert len(s.students) == 1

def test_add_subject():
    s: SubSort = SubSort()
    assert len(s.subject) == 0
    s.add_subject("s1")
    s.add_subject("s2")

    assert len(s.subject) == 2

    s.add_subject("s1")
    s.add_subject(None)
    assert not None in s.subject
    assert len(s.subject) == 2

def test_delete_subject():
    s: SubSort = SubSort()
    assert len(s.subject) == 0
    s.add_subject("s1")
    s.add_subject("s2")

    assert len(s.subject) == 2
    s.delete_subject(None)
    s.delete_subject(1)
    s.delete_subject("s3")
    assert len(s.subject) == 2

    s.delete_subject("s1")
    assert len(s.subject) == 1
    s.delete_subject("s2")
    assert len(s.subject) == 0

def test_add_day():
    s: SubSort = SubSort()
    assert len(s.days) == 0
    s.add_day(None)
    assert len(s.days) == 0

    with pytest.raises(Exception):
        s.add_day("s4")
    
    s.add_subject("s1") 
    s.add_subject("s2") 
    s.add_subject("s3") 

    s.add_day({"s1", "s2"})
    s.add_day({"s1"})
    s.add_day({"s1", "s2", "s3"})
    with pytest.raises(Exception):
        s.add_day({"s1", "s2", "s3", "s4"})

    assert len(s.days) == 3

def test_delete_day():
    s: SubSort = SubSort()
    assert len(s.days) == 0

    s.add_subject("s1") 
    s.add_subject("s2") 
    s.add_subject("s3") 

    s.add_day({"s1", "s2"})
    s.add_day({"s1"})
    s.add_day({"s1", "s2", "s3"})

    assert len(s.days) == 3
    s.delete_day(3)
    s.delete_day("Pondeli")
    assert len(s.days) == 3
    s.delete_day(0)
    s.delete_day(2)
    assert len(s.days) == 2

    assert len(s.days[0].subjects) == 1

    for i in range(2):
        s.delete_day(i)
    
    assert len(s.days) == 0

@pytest.fixture()
def setup_manual():
    s = SubSort()

    s.add_subject("s1")
    s.add_subject("s2")
    s.add_subject("s3")
    s.add_subject("s4")

    s.add_day({"s1", "s2", "s3"})
    s.add_day({"s2", "s4"})
    s.add_day({"s1", "s4"})

    for i in range(5):
        s.add_student(i, "Student", f"{i}", "O8", None)
    
    s.students[0].subjects = ("s1")
    s.students[1].subjects = ("s1", "s2")
    s.students[2].subjects = ("s1", "s4")
    s.students[3].subjects = ("s4", "s2", "s1")
    s.students[4].subjects = ("s2", "s3", "s4")
    yield s

def test_clear(setup_manual):
    s: SubSort = setup_manual
    assert not len(s.students) == 0
    assert not len(s.days) == 0
    assert not len(s.subject) == 0

    s.clear()

    assert len(s.students) == 0
    assert len(s.days) == 0
    assert len(s.subject) == 0
    assert s.nof_sorted_students == 0
