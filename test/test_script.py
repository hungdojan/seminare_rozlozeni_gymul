## Testovaci skript
#
#  @file testing_script.py
#  @author Hung Do
from sortsubj import *
import pytest
import os

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
        s.delete_day(0)
    
    assert len(s.days) == 0

def test_load_file_student():
    s: SubSort = SubSort()

    # prazdna cesta
    with pytest.raises(Exception):
        s.load_file_student(None)
    # spatny format/typ
    with pytest.raises(Exception):
        s.load_file_student("my_file.txt")
    # neexistujici soubor
    with pytest.raises(Exception):
        s.load_file_student("my_file.csv")

    s.load_file_student(os.path.join(os.path.dirname(__file__), "input_zaci.csv"))
    assert len(s.students) == 10
    student1 = s.students["1"]
    student5 = s.students["5"]
    student10 = s.students["10"]

    assert student1.first_name == "Adéla"
    assert student5.first_name == "Adéla"
    assert student10.first_name == "Pavel"

    assert s.students["3"].first_name == "Ondřej"

    assert student1.subjects[0] == "ZSV"
    assert student5.subjects[2] == "Nj-DSD1"
    assert student10.subjects[1] == "Aj-FCE"

def test_load_file_subjects():
    s: SubSort = SubSort()

    # prazdna cesta
    with pytest.raises(Exception):
        s.load_file_subjects(None)
    # spatny format/typ
    with pytest.raises(Exception):
        s.load_file_subjects("my_file.txt")
    # neexistujici soubor
    with pytest.raises(Exception):
        s.load_file_subjects("my_file.csv")

    s.load_file_subjects(os.path.join(os.path.dirname(__file__),"input_predmety.csv"))
    assert len(s.subject) == 14
    assert "ZSV" in s.subject
    assert "M-VŠ" in s.subject
    assert not "zsv" in s.subject
    assert not "Aj-fce" in s.subject

def test_load_day_file():
    s: SubSort = SubSort()
    s.load_file_subjects(os.path.join(os.path.dirname(__file__),"input_predmety.csv"))
    # prazdna cesta
    with pytest.raises(Exception):
        s.load_file_days(None)
    # spatny format/typ
    with pytest.raises(Exception):
        s.load_file_days("my_file.txt")
    # neexistujici soubor
    with pytest.raises(Exception):
        s.load_file_days("my_file.csv")

    s.load_file_days(os.path.join(os.path.dirname(__file__),"input_dny.csv"))
    assert len(s.days) == 3
    assert "ZSV" in s.days[2].subjects
    assert "ZSV" in s.days[1].subjects
    assert not "ZSV" in s.days[0].subjects
    for days in s.days:
            assert len(days.subjects) == 6

    assert "Pr" in s.days[2].subjects
    assert "Fy" in s.days[1].subjects
    assert "Aj-Konv" in s.days[0].subjects

def test_generate_files():
    s: SubSort = SubSort()
    s.generate_files(os.path.dirname(__file__))
    counter = 0
    for file in os.listdir(os.path.dirname(__file__)):
        if file.startswith("output"):
            counter += 1
    
    assert counter >= 2

@pytest.fixture()
def setup_manual():
    s = SubSort()

    s.add_subject("s1")
    s.add_subject("s2")
    s.add_subject("s3")
    s.add_subject("s4")
    s.add_subject("s5")

    s.add_day({"s1", "s2", "s3", "s5"})
    s.add_day({"s2", "s4"})
    s.add_day({"s1", "s4"})

    for i in range(5):
        s.add_student(i, "Student", f"{i}", "O8", None)
    
    s.students[0].subjects = tuple(["s1"])
    s.students[1].subjects = tuple(["s1", "s2"])
    s.students[2].subjects = tuple(["s1", "s4"])
    s.students[3].subjects = tuple(["s3", "s2", "s1"])
    s.students[4].subjects = tuple(["s5", "s3", "s4"])
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

def test_sort_data(setup_manual):
    s: SubSort = setup_manual
    s.sort_data()

    assert len(s.students[0].pass_subj) == 2
    assert ("s1", None, None) in s.students[0].pass_subj
    assert (None, None, "s1") in s.students[0].pass_subj
    assert s.students[0].sel_subj == None
    assert s.students[0].sorted

    assert len(s.students[1].pass_subj) == 3
    assert ("s1", "s2", None) in s.students[1].pass_subj
    assert ("s2", None, "s1") in s.students[1].pass_subj
    assert (None, "s2", "s1") in s.students[1].pass_subj
    assert s.students[1].sel_subj == None
    assert s.students[1].sorted

    assert len(s.students[2].pass_subj) == 2
    assert ("s1", None, "s4") in s.students[2].pass_subj
    assert (None, "s4", "s1") in s.students[2].pass_subj
    assert s.students[2].sel_subj == None
    assert s.students[2].sorted

    assert len(s.students[3].pass_subj) == 1
    assert ("s3", "s2", "s1") in s.students[3].pass_subj
    assert s.students[3].sel_subj == ("s3", "s2", "s1")
    assert s.students[3].sorted

    assert len(s.students[4].pass_subj) == 0
    assert s.students[4].sel_subj == None
    assert s.students[4].sorted

    assert s.nof_sorted_students == 1

def test_set_sel_subj(setup_manual):
    s: SubSort = setup_manual

    s.sort_data()

    assert s.nof_sorted_students == 1

    with pytest.raises(Exception):
        s.student_sel_subject(-1, 0)
    with pytest.raises(Exception):
        s.student_sel_subject(10, 1)
    with pytest.raises(Exception):
        s.student_sel_subject(None, 0)

    s.student_sel_subject(0, 2)
    s.student_sel_subject(0, -1)

    assert s.nof_sorted_students == 1
    s.student_sel_subject(0, 1)

    assert s.nof_sorted_students == 2
    s.student_sel_subject(1, 1)
    assert s.nof_sorted_students == 3

    s.student_sel_subject(0, 0)
    assert s.nof_sorted_students == 3
