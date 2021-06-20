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
        self.nof_students = 0

    ## Jmeno predmetu
    #
    #  @return Vraci jmeno predmetu
    @property
    def name(self):
        return self.__name