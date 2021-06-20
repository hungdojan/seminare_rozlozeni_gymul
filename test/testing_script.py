## Testovaci skript
#
#  @file testing_script.py
#  @author Hung Do
from sortsubj import *
import unittest
# import pytest

class TestClass(unittest.TestCase):

    ## Test prazdneho objektu
    def test_empty_obj(self):
        sub_sort = SubSort()
        self.assertEqual(sub_sort.days_size(), 0)

    ## Test pridani studentu
    def test_add_student(self):
        student_list = []
        sub_sort = SubSort()
        student_list.append(Student(1, "Student1", "O8", None))
        student_list.append(Student(2, "Student2", "O8", None))
        student_list.append(Student(3, "Student3", "O8", None))

        self.assertTrue(sub_sort.add_student_obj(student_list[0]))
        self.assertTrue(sub_sort.add_student_obj(student_list[1]))
        self.assertTrue(sub_sort.add_student_obj(student_list[2]))

        # Pridani jiz existujiciho studenta
        self.assertFalse(sub_sort.add_student_obj(student_list[0]))
        self.assertEqual(len(sub_sort.student_size()), 3)

if __name__ == '__main__':
    unittest.main()
