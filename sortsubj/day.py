## Trida dnu
#
#  @class Dat
#  @file day.py
#  @authors: Hung Do, Prokop Mikulasek
#  @version 1.0.0
#  @copyright GNU Public License v3.0

from sortsubj.subject import Subject

class Day:
    def __init__(self, subjects):
        self.subjects: dict = {}
        self.__dict_init(subjects)
    
    ## Funkce priradi jednotlive predmety do daneho dne
    #
    #  @param subjects  Seznam predmetu
    def __dict_init(self, subjects):
        """
        Funkce projede cely seznam predmetu 'subject', zkontroluje, zda obsah 
        je typu 'retezec' a klic se jeste nenachazi ve slovniku. Pote ho
        do slovniku prida.

        Pokud klic jiz existuje, funkce vyhodi vyjimku.
        Pokud typ v seznamu neni retezec, vyhodi vyjimku TypeError.
        """
        for subj in subjects:
            if type(subj) is not str:
                raise TypeError("Datovy typ klice musi byt retezec")
            elif subj in self.subjects:
                raise Exception("Predmet je jiz na seznamu")
            self.subjects[subj] = Subject(subj)
    
    # Pridava jednotlivy predmet do dne
    def append_subject_to_day(self, subject_name):
        if subject_name not in self.subjects:
            self.subjects[subject_name] = Subject(subject_name)

    # Odstranuje jednotlivy predmet ze dne
    def remove_subject_to_day(self, subject_name):
        if subject_name in self.subjects:
            del self.subjects[subject_name]

    # Vymaze seznam zaku
    def clear_subs(self):
        for key in self.subjects:
            self.subjects[key].lof_students.clear()

    def __str__(self):
        # TODO:
        pass

