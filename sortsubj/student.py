## Trida studenta
#
#  @file student.py
#  @authors: Hung Do, Prokop Mikulasek
#  @version 1.0.0
#  @copyright GNU Public License v3.0
class Student:

    ## Konstruktor
    #
    #  @param id            ID studenta
    #  @param first_name    Jmeno studenta
    #  @param last_name     Prijmeni studenta
    #  @param class_id      Nazev tridy studenta
    #  @param subjects      N-tice vybranych predmetu
    def __init__(self, id, first_name: str, last_name: str, class_id: str, subjects: tuple):
        ## Identifikacni cislo studenta
        self.id              = id
        ## Jmeno studenta
        self.first_name: str = first_name
        ## Prijmeni studenta
        self.last_name: str  = last_name
        ## Trida studenta
        self.class_id: str   = class_id
        ## N-tice vybranych predmetu
        self.__subjects: tuple = subjects
        ## Seznam vyhovujicich kombinaci
        self.pass_subj: list = []
        ## Vybrana kombinace
        self.__sel_subj: tuple = None
        ## Student byl roztrizen alespon jednou
        #  Slouzi pro optimalizaci
        self.sorted          = False

    @property
    def sel_subj(self):
        return self.__sel_subj
    
    @property
    def subjects(self):
        return self.__subjects

    @subjects.setter
    def subjects(self, value):
        self.sorted = False
        self.__subjects = value

    ## Manualni selekce kombinace
    #
    #  Pokud je vybrany index mimo rozsah seznamu uspesnych kombinaci, 
    #  funkce automaticky vraci #FALSE
    #  @param index     Poradi kombinace v listu 
    #  @return #TRUE pokud funkce nastavila novou hodnotu a puvodni hodnota vyberu byla #NONE
    def set_sel_subj(self, index: int) -> bool:
        if index >= len(self.pass_subj):
            return False
        is_set = self.__sel_subj is None
        self.__sel_subj = self.pass_subj[index]
        # Nova hodnota je non-None
        return is_set and self.__sel_subj is not None

    def __str__(self):
        # TODO:
        pass