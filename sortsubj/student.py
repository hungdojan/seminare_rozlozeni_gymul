## Trida studenta
#
#  @file student.py
#  @authors: Hung Do, Prokop Mikulasek
#  @version 1.0.0
#  @copyright GNU Public License v3.0
class Student:

    ## Konstruktor
    def __init__(self, index: int, name: str, class_id: str, subjects: list):
        ## Identifikacni cislo studenta
        self.index: int     = index
        ## Jmeno a prijmeni studenta
        self.name: str      = name
        ## Trida studenta
        self.class_id: str  = class_id
        ## Seznam vybranych predmetu
        self.subjects: list = subjects
        ## Seznam vyhovujicich kombinaci
        self.pass_subjs     = []
        ## Zak ma alespon jednu vyhovujici kombinaci
        self.success        = False

    def __str__(self):
        return "{} {} {} {}".format(self.index, self.name, self.class_id, self.subjects)