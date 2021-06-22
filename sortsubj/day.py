from .subject import Subject

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
        pass
    
    def __str__(self):
        # TODO:
        pass

