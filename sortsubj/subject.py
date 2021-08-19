## Trida predmetu
#
#  @class Subject
#  @file subject.py
#  @authors: Hung Do, Prokop Mikulasek
#  @version 1.0.0
#  @copyright GNU Public License v3.0

class Subject:

    ## Konstruktor
    def __init__(self, name):
        ## Jmeno predmetu
        self.__name = name
        ## Pocet studentu v danem predmetu
        self.lof_students = dict()

    ## Jmeno predmetu
    #
    #  @return Vraci jmeno predmetu
    @property
    def name(self):
        return self.__name
    
    ## Funkce prida studenta do seznamu studentu
    #  Pokud student na seznamu je, funkce ho ignoruje
    #
    #  @param student Objekt studenta
    def add_student(self, student):
        if student.id not in self.lof_students:
            self.lof_students[student.id] = student
    
    ## Funkce odstrani studenta ze seznamu
    #  Pokud student na seznamu neni, funkce ho ignoruje
    #
    #  @param student_id Studentuv id
    def remove_student(self, student_id):
        if student_id in self.lof_students:
            del self.lof_students[student_id]