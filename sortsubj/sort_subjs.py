## Soubor s knihovnimi funkcemi tridici zaky do jednotlivych skupin
#
#  @file lib_sort_subjs.py
#  @authors: Hung Do, Prokop Mikulasek
#  @version 1.0.0
#  @copyright GNU Public License v3.0

from .student import Student
from .subject import Subject

class SubSort:

    ## Konstruktor tridy
    def __init__(self):
        ## Seznam studentu
        self.__students: dict = {}
        ## Seznam jednotlivych dnu
        self.__days    : list = []
        ## Seznam jednotlivych predmetu
        self.__subject : set = {}

    ## Pocet nastavenych dnu
    #
    #  @return Pocet dnu v seznamu
    def days_size(self):
        return len(self.__days)

    ## Pocet nactenych studentu
    #
    #  @return Pocet studentu v seznamu
    def student_size(self):
        return len(self.__students)

    ## Pocet nactenych predmetu
    #
    #  @return Pocet predmetu v seznamu
    def subject_size(self):
        return len(self.__subject)
    
    ## Funkce pridava noveho zaka do seznamu zaku
    #
    #  @param id        Identifikacni cislo zaka
    #  @return #TRUE pokud se zaka podarilo pridat; jeho id je jedinecne
    def add_student_obj(self, student: Student) -> bool:
        """
        Nejprve se zkontroluje, zda je id jedinecne (ve slovniku neni nikdo se stejnym id)
        Pokud ano, vrati false. Pokud ne, vytvori se nova instance zaka a prida se do slovniku
        s klicem id.
        """
        return True

    ## Funkce pridava noveho zaka do seznamu zaku
    #
    #  @param id        Identifikacni cislo zaka
    #  @param name      Jmeno a prijmeni zaka
    #  @param subjects  Seznam zakova vyberu
    #  @return #TRUE pokud se zaka podarilo pridat; jeho id je jedinecne
    def add_student_manual(self, id: int, name: str, class_id: str, subjects: list) -> bool:
        """
        Nejprve se zkontroluje, zda je id jedinecne (ve slovniku neni nikdo se stejnym id)
        Pokud ano, vrati false. Pokud ne, vytvori se nova instance zaka a prida se do slovniku
        s klicem id.
        """
        return False
    
    ## Funkce maze zaka ze seznamu zaku
    #
    #  Vyhledava se podle ID zaka
    #  @param id    Identifikacni cislo zaka
    #  @return #TRUE pokud se zaka podarilo odstranit; zaka se podarilo najit a smazat
    def delete_student(self, id: int) -> bool:
        """
        Vyhledava se podle klice (id). Pokud je obsah klice prazdny (dict[klic] == None), 
        vrati false. Jinak nastavi obsah na None a vrati true.
        """
        return False

    ## Funkce prida predmet do seznamu predmetu
    #
    #  @param subject   Jmeno predmetu
    def add_subject(self, name: str):
        pass

    ## Funkce maze predmet ze seznamu predmetu
    #
    #  @param subject   Jmeno predmetu
    def delete_subject(self, name: str):
        pass

    ## Funkce prida den do slovniku
    #
    #  @param subjects  Seznam predmetu v danem dni
    def add_day(self, subjects: list):
        pass

    ## Funkce smaze dany den podle indexu
    #
    #  @param day_id    Poradi dne
    #  @return #TRUE pokud se podarilo smazat den
    def delete_day(self, day_id: int):
        if (day_id >= self.days_size()):
            return False
        return False

    ## Funkce nacte soubor se studenty ve formatu .csv
    #
    #  @param path  Cesta k souboru
    def load_file_student(self, path: str):
        """
        Zkontroluje, zda soubor existuje a jestli ma spravnou koncovku
        pote nacte obsah a ulozi ho do self.__students
        Format souboru (misto ',' muze byt ';'):
            ID,jmeno,prijmeni,trida,s1,s2,s3
        osetrit prebytecne whitespace (prikaz trim??)
        """
        pass

    ## Funkce nacte soubor se dennimi rozlozenimi ve formatu .csv
    #
    #  @param path  Cesta k souboru
    def load_file_days(self, path: str):
        """
        Zkontroluje, zda soubor existuje a jestli ma spravnou koncovku
        pote nacte obsah a ulozi ho do self.__days
        Format souboru (misto ',' muze byt ';'):
            s1,s2,s3,s4...      <- dny jsou pod sebou
        """
        pass

    ## Funkce nacte soubor se seznamem predmetu
    #
    #  @param path  Cesta k souboru
    def load_file_subjects(self, path: str):
        """
        Zkontroluje, zda soubor existuje a jestli ma spravnou koncovku
        pote nacte obsah a ulozi ho do self.__days
        Format souboru (misto ',' muze byt ';'):
            s1
            s2
            s3
            ...
        """
        pass

    ## Funkce prerovna studenty do danych dnu a predmetu
    def sort_data(self):
        # TODO: hlavni cast programu; je mozne ze se obsah da do vice souboru
        # obsah teto funkce se ponecha pozdeji
        # mel by zpracovat informace
        # projekt kombinace a zjistit u kazdeho zaka, zda u nej vyhovyji predmety
        pass

    ## Funkce vygeneruje vysledna data
    #
    #  a ulozi je do predem pojmenovanych souboru
    def generate_files(self):
        """
        Vygeneruje (minimalne) 6 souboru:
            output_nezarazeni_zaci -> zaci splnuji vice nez jeden mozny vyber
            output_pocet_zaku_na_seminar -> pocet zaku na predmet v jednotlivych dnech
                -> zaci jsou pridani jen tehdy, pokud maji jen jednu moznost
            output_uspesni_zaci  -> zaci splnujici maximalne jednu kombinaci
            output_detailni_zaci -> vsichni zaci; u kazdeho je seznam moznych kombinaci
            output_detailni_dny  -> u kazdeho predmetu je napsan seznam 100% zaku
            output_zbyli_zaci    -> zaci nesplnuji ani jednu kombinaci
        """
        pass