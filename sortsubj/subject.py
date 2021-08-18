## Trida predmetu
#
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
    #
    #  @param student Objekt studenta
    def add_student(self, student):
        # Pokud jiz student na seznamu je, tak se nepridava
        if student.id not in self.lof_students:
            self.lof_students[id] = student
    
    def remove_student(self, student_id):
        if student_id in self.lof_students:
            del self.lof_students[student_id]