## Soubor s knihovnimi funkcemi tridici studenty do jednotlivych skupin
#
#  @class SubSort
#  @file lib_sort_subjs.py
#  @authors: Hung Do, Prokop Mikulasek
#  @version 1.0.0
#  @copyright GNU Public License v3.0

from .subject import Subject
from .student import Student
from .day import Day

class SubSort:

    ## Konstruktor
    def __init__(self):
        ## Seznam studentu
        #  Klicem seznamu je ID studenta
        self.students: dict = {}
        ## Seznam jednotlivych dnu
        self.days    : list = []
        ## Mnozina predmetu
        self.subject : set = {}
        ## Flag ukazuje, ze byl seznam dnu/predmetu byl aktualizovan
        #  Studenti by meli byt znovu roztrizeni 
        self.__day_or_subj_updated = False
        ## Pocet studentu s vybranym 
        self.nof_sorted_students = 0

    ## Funkce pridava noveho studenta do seznamu studentu
    #
    #  @param id        ID studenta
    #  @param name      Jmeno a prijmeni studenta
    #  @param subjects  Seznam studentova vyberu
    #  @return #TRUE pokud se studenta podarilo pridat; jeho id je jedinecne
    def add_student(self, id, first_name: str, last_name: str, class_id: str, subjects: tuple) -> bool:
        """
        Nejprve se zkontroluje, zda je id jedinecne (ve slovniku neni nikdo se stejnym id)
        Pokud ano, vrati false. Pokud ne, vytvori se nova instance studenta a prida se do slovniku
        s klicem id.
        """
        return False
    
    ## Funkce maze studenta ze seznamu studentu
    #
    #  Vyhledava se podle ID studenta
    #  @param id    ID studenta
    #  @return #TRUE pokud se studenta podarilo odstranit; studenta se podarilo najit a smazat
    def delete_student(self, id) -> bool:
        """
        Vyhledava se podle klice (id). Pokud je obsah klice prazdny (if "key" not in 'dict'), 
        vrati false. Jinak nastavi obsah na None a vrati true.
        """
        return False
    
    ## Funkce vybere kombinaci predmetu podle seznamu uspesnych kombinaci
    #
    #  @param index     Poradi kombinace v seznamu uspesnych kombinaci
    def student_sel_subject(self, student_id, index: int):
        """
        Vyhleda ve slovniku podle student_id. Pokud se student ve slovniku nenachazi,
        funkce vyhodi vyjimku.
        Vola se funkce student.set_sel_subj()
            -> pokud je output true -> nof_sorted_students++
        """
        pass
    
    ## Funkce vytvori a prida instanci dne
    #
    #  @param subjects  Mnozina predmetu v danem dni
    def add_day(self, subjects: set):
        """
        Kontrola, zda jsou vsechny predmety v 'subjects' definovane. 
        Pokud ne, funkce vyhodi vyjimku a nic se neprida.
        Pokud je (subjects == None), funkce nic neudela
        Pri uspesnem pridani dne je potreba nastavit flag.
        """
        pass

    ## Funkce odstrani instanci dne ze seznamu
    #
    #  @oaram index     Poradi dne (indexuje se od 0)
    def delete_day(self, index: int):
        """
        Pokud index neni mimo rozsah seznamu, instance objektu 'Day' je odstraneno (del).
        Pri uspesnem odstraneni dne je potreba nastavit flag.
        """
        pass

    ## Funkce prida predmet do mnoziny predmetu
    #
    #  @param subj_name Jmeno predmetu
    def add_subject(self, subj_name: str):
        """
        Pokud predmet jiz existuje, funkce nic neprovede.
        Pri uspesnem pridani predmetu je potreba nastavit flag.
        """
        pass

    ## Funkce odstrani predmet z mnoziny predmetu
    #
    #  @param subj_name Jmeno predmetu
    def delete_subject(self, subj_name: str):
        """
        Pokud predmet neexistuje, funkce nic neprovede.
        Pri uspesnem odstraneni predmetu je potreba nastavit flag.
        """
        pass
    
    ## Funkce smaze vice studentu podle seznamu id
    #
    #  Pokud student v seznamu neni, je ignorovan
    #  @param list_id   Seznam iden. cisel studentu
    def delete_students(self, list_id: list):
        """
        Smaze studenty podle seznamu id studentu. Pokud studentuv id
        na seznamu neni, je ignorovan a preskocen.
        """
        pass

    ## Funkce nacte soubor se studenty ve formatu .csv
    #
    #  @param path  Cesta k souboru
    def load_file_student(self, path: str):
        """
        Zkontroluje, zda soubor existuje a jestli ma spravnou koncovku
        pote nacte obsah a ulozi ho do self.students
        Format souboru (misto ',' muze byt ';'):
            ID,jmeno,prijmeni,trida,s1,s2,s3
        osetrit prebytecne whitespace (prikaz trim??)

        Funkce vyhodi vyjimku, kdyz:
            soubor neexistuje
            soubor je spatneho formatu/typu
            v souboru se vyskytuje student s jiz existujicim id
                -> funkce vypise chybove hlaseni, ve kterem bude napsano na jakem radku jakeho souboru
        """
        pass

    ## Funkce nacte soubor se dennimi rozlozenimi ve formatu .csv
    #
    #  @param path  Cesta k souboru
    def load_file_days(self, path: str):
        """
        Zkontroluje, zda soubor existuje a jestli ma spravnou koncovku
        pote nacte obsah a ulozi ho do self.days
        Format souboru (misto ',' muze byt ';'):
            s1,s2,s3,s4...      <- dny jsou pod sebou
        
        Funkce vyhodi vyjimku, kdyz:
            soubor neexistuje
            soubor je spatneho formatu/typu
            ve dni se nachazi predmet, ktery jeste nebyl definovan

        Duplikace by meli byt vyreseny (pomoci objektu 'set')
        Vytvori se nova instance 'Day' a prida se do seznamu dnu. 
        """
        pass

    ## Funkce nacte soubor se seznamem predmetu
    #
    #  @param path  Cesta k souboru
    def load_file_subjects(self, path: str):
        """
        Zkontroluje, zda soubor existuje a jestli ma spravnou koncovku
        pote nacte obsah a ulozi ho do self.subject
        Format souboru (misto ',' muze byt ';'):
            s1
            s2
            s3
            ...
        
        Funkce vyhodi vyjimku, kdyz:
            soubor neexistuje
            soubor je spatneho formatu/typu
        """
        pass

    ## Funkce kontoluje, zda je mozne sestavit vybranou kombinaci z nastavenych dnu
    #
    #  @param subjects  N-tice predmetu
    #  @param #TRUE pokud je zadana kombinace predmetu mozna sestavit
    def valid_combination(self, subjects: tuple) -> bool:
        return False
    
    ## Funkce prerovna studenty do danych dnu a predmetu
    def sort_data(self):
        # TODO: hlavni cast programu; je mozne ze se obsah da do vice souboru
        # obsah teto funkce se ponecha pozdeji
        # mel by zpracovat informace
        # projekt kombinace a zjistit u kazdeho studenta, zda u nej vyhovyji predmety
        """
        Funkce se zklada ze 2 casti:
            - funkce projede vsechny studenty a najde u nic uspesne kombinace
            - pokud ma student jen jednu uspesnou kombinaci, kombinace je ulozena do student.sel_subjs
                - pokud nema zadnou, nebo vice, attribut neni nastaven
        
        Funkce pracuje s nactenymi daty. U kazdeho studenta je potreba zjistit vsechna
        mozna rozlozeni -> nezalezi na poradi jeho vyberu. 
        Pokud je dnu mene nez pocet vybranych predmetu u studenta, funkce vyhodi vyjimku.

        Pohlidat si, ze student ma vybrane predmety nastavene.

        Pseudokod:
            # Den1: s1, s2, s3
            # Den2: s2, s4
            # Den3: s1, s4

            print(student_a.subjects)   # ('s4', 's2', 's1')
            my_sort_function()          # Let magic happen
            print(student_a.pass_subj)  # [ ('s1', 's2', 's4'), ('s2', 's4', 's1')]
        
        Funkce nastavi jednotlive flagy pro lepsi optimalizaci:
        if self.__days_or_subj_updated:
            # projet vsechny studenty znovu
        else:
            if not student.sorted:
                # provedu funkci na studentovi
                # nastavim flag, ze uz je sorted

        POZOR: Dnu muze byt vice nez ma student vybranych predmetu.
        Pak je u dne, u ktereho se nevybira, nastaven 'None'

        Pr.
            # Den1: s1, s2, s3
            # Den2: s2, s4
            # Den3: s1, s4

            print(student.subjects)     # ('s1', 's4')
            my_sort_function()          # Let magic happen
            print(student.pass_subj)    # [('s1', 's4', None), (None, 's4', 's1')]

        Pokud ma student jen jednu moznou kombinaci, je mu automaticky prirazena.
            -> aktualizace self.nof_sorted_students podle vystupu funkce

        Doporucuju si napsat nejake pomocne funkce
            -> pokud budou v teto tride -> nazev zacina dvema podtrzitky; pr.: __moje_funkce(self)
        """
        pass

    ## Funkce vygeneruje vysledna data
    #
    #  a ulozi je do predem pojmenovanych souboru
    #  @param dir_path  Vytvoreni souboru do oznacene slozky
    def generate_files(self, dir_path: str = None):
        """
        Vygeneruje (minimalne) 6 souboru:
            output_nezarazeni_zaci -> zaci splnuji vice nez jeden mozny vyber
            output_pocet_studentu_na_seminar -> pocet studentu na predmet v jednotlivych dnech
                -> zaci jsou pridani jen tehdy, pokud maji jen jednu moznost
            output_uspesni_zaci  -> zaci splnujici maximalne jednu kombinaci
            output_detailni_zaci -> vsichni zaci; u kazdeho je seznam moznych kombinaci
            output_detailni_dny  -> u kazdeho predmetu je napsan seznam 100% studentu
            output_zbyli_zaci    -> zaci nesplnuji ani jednu kombinaci
        
        Jmena souboru se muze nadefinovat v souboru 'consts.py'. Soubory jsou generovany do definovane slozky.
        Cesta ke slozce muze byt absolutni nebo relativni -> je potreba zjistit jeji existenci.
        Pokud je dir_path == None, nebo slozka neexistuje, jsou soubory vytvorene ve stejne slozce, ve kterem
        se nachazi exe/skript
        """
        pass

    ## Funkce vycisti cely objekt
    #
    #  Seznam studentu, dnu a predmetu se vynuluje
    def clear():
        pass