## Soubor s knihovnimi funkcemi tridici studenty do jednotlivych skupin
#
#  @class SubSort
#  @file lib_sort_subjs.py
#  @authors: Hung Do, Prokop Mikulasek
#  @version 1.0.0
#  @copyright GNU Public License v3.0

import re
import os
import codecs
from sortsubj.subject import Subject
from sortsubj.student import Student
from sortsubj.day import Day
from sortsubj.consts import SPRAVNA_KONCOVKA

class SubSort:

    ## Konstruktor
    def __init__(self):
        ## Seznam studentu
        #  Klicem seznamu je ID studenta
        self.students: dict = dict()
        ## Seznam jednotlivych dnu
        self.days    : list = list()
        ## Mnozina predmetu
        self.subject : set = set()
        ## Flag ukazuje, ze byl seznam dnu/predmetu byl aktualizovan
        #  Studenti by meli byt znovu roztrizeni 
        self.__day_or_subj_updated = False
        ## Pocet studentu s vybranym 
        self.nof_sorted_students = 0

    # Aktualizace flagu
    def request_update(self):
        self.__day_or_subj_updated = False

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
        # Kontrola validity klice
        if id is None:
            raise Exception("ID zaka nemuze byt nedefinovana!")
        # Kontrola existence studenta
        if id in self.students:
            return False
        else:
            # Vytvori novou instanci studenta na danem klici
            # Klicem v dict je ID studenta
            self.students[id] = Student(id, first_name, last_name, class_id, subjects)
        
        return True
    
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
        # Kontrola validity klice a existence studenta
        if id not in self.students:
            return False
        else:
            # Mazani instance studenta ze seznamu spolecne s jeho klicem
            del self.students[id]
        return True
    
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
        if student_id not in self.studetns:
            raise Exception("Student jeste neni v seznamu")
        
        # Zjisti, zda byl student jiz prerazen
        output = self.students[student_id].set_sel_subj(index)

        if output:
            self.nof_sorted_students += 1
        else:
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
        # Kontrola hodnoty objektu
        if subjects is None:
            return
            
        # Ignoruje None -> nedefinovany predmet
        subjects = list(filter(None, subjects))
        # Kontroluje, zda jsou vsechny predmety v seznamu predmetu
        for subject in subjects:
            if subject not in self.subject:
                raise Exception("Nedefinovany predmet!")

        self.days.append(Day(subjects))

    ## Funkce odstrani instanci dne ze seznamu
    #
    #  @oaram index     Poradi dne (indexuje se od 0)
    def delete_day(self, index: int):
        """
        Pokud index neni mimo rozsah seznamu, instance objektu 'Day' je odstraneno (del).
        Pri uspesnem odstraneni dne je potreba nastavit flag.
        """
        # Zjisteni typu a velikosti indexu
        if type(index) is not int or index >= len(self.days):
            return
        
        del self.days[index]

    ## Funkce prida predmet do mnoziny predmetu
    #
    #  @param subj_name Jmeno predmetu
    def add_subject(self, subj_name: str):
        """
        Pokud predmet jiz existuje, funkce nic neprovede.
        Pri uspesnem pridani predmetu je potreba nastavit flag.
        """
        if subj_name not in self.subject and subj_name is not None:
            self.subject.add(subj_name)
            self.request_update() # zadost o aktualizaci flagu

    ## Funkce odstrani predmet z mnoziny predmetu
    #
    #  @param subj_name Jmeno predmetu
    def delete_subject(self, subj_name: str):
        """
        Pokud predmet neexistuje, funkce nic neprovede.
        Pri uspesnem odstraneni predmetu je potreba nastavit flag.
        """
        if subj_name in self.subject:
            self.subject.remove(subj_name)
            self.request_update() # zadost o aktualizaci flagu
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
        for id in list_id:
            # Kontrola existence studenta v seznamu
            if id in self.students:
                del self.students[id]

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
        # Kontrola existence souboru
        if not os.path.isfile(path):
            raise Exception("Soubor neexistuje!")
        # Kontrola spravneho formatu souboru
        elif path[-1*(len(SPRAVNA_KONCOVKA)):] != SPRAVNA_KONCOVKA:
            raise Exception("Soubor je spatneho typu")

        line_num = 0
        # Cteni souboru v utf-8 kodovani
        with codecs.open(path, encoding='utf-8') as f:
            for line in f:
                line_num += 1
                # rozdeleni radku pomoci znaku ',' a ';'
                # a mazani koncovky konce radku; os.linesep zajisti spravny znak napric OS
                data = re.split(',|;', line.rstrip(os.linesep))
                # ID studenta jiz existuje
                if data[0] in self.students:
                    raise Exception(f"Line {line_num}: Zak s ID={data[0]} jiz existuje!")
                else:
                    self.add_student(
                        data[0].strip(),
                        data[1].strip(),
                        data[2].strip(),
                        data[3].strip(),
                        tuple(data[4-len(data):])   # student muze mit vic nez 3 predmetu vybranych
                    )

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
        # Kontrola existence souboru
        if not os.path.isfile(path):
            raise Exception("Soubor neexistuje!")
        # Kontrola spravneho formatu souboru
        elif path[-1*(len(SPRAVNA_KONCOVKA)):] != SPRAVNA_KONCOVKA:
            raise Exception("Soubor je spatneho typu")
        
        # Cteni souboru v utf-8 kodovani
        with codecs.open(path, encoding='utf-8') as f:
            for line in f:
                # rozdeleni radku pomoci znaku ',' a ';'
                # a mazani koncovky konce radku; os.linesep zajisti spravny znak napric OS
                data = re.split(',|;', line.rstrip(os.linesep))
                data = set(data)
                # validace predmetu
                for subj in data:
                    if subj not in self.subject:
                        raise Exception(f'Predmet {subj} jeste neni definovany!')
                self.add_day(data)

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
        # Kontrola existence souboru
        if not os.path.isfile(path):
            raise Exception("Soubor neexistuje!")
        # Kontrola spravneho formatu souboru
        elif path[-1*(len(SPRAVNA_KONCOVKA)):] != SPRAVNA_KONCOVKA:
            raise Exception("Soubor je spatneho typu")
        
        with codecs.open(path, encoding='utf-8') as f:
            for line in f:
                self.add_subject(line.rstrip(os.linesep))

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
    def generate_files(self, dir_path: str):
        """
        Vygeneruje (minimalne) 2 souboru:
            output_zaci -> vsichni zaci; u kazdeho je seznam moznych kombinaci
            output_dny  -> u kazdeho predmetu je napsan seznam 100% studentu
        
        Jmena souboru se muze nadefinovat v souboru 'consts.py'. Soubory jsou generovany do definovane slozky.
        Cesta ke slozce muze byt absolutni nebo relativni -> je potreba zjistit jeji existenci.
        Pokud je dir_path == None, nebo slozka neexistuje, program hodi chybu
        """
        # Kontrola prijateho parametru
        if dir_path is None:
            raise Exception("Cesta vystupni slozky nemuze byt prazdna")
        elif not os.path.isdir(dir_path):
            raise Exception("Slozka neexistuje!")

        # Tvorba souboru output_dny.csv
        # format souboru:
        #   Den {cislo_dne}
        #   {jmeno_predmetu}
        #   {id_zaka},{jmeno_zaka},{prijmeni_zaka},{trida_zaka}
        #   {id_zaka},{jmeno_zaka},{prijmeni_zaka},{trida_zaka}
        #   ...
        with open(os.path.join(dir_path, "output_dny.csv"), 'w') as f:
            for i in range(len(self.days)):
                # Vybrany den
                f.write(f'Den {i}{os.linesep}')
                for subj in self.days[i].subjects:
                    # Vybrany predmet
                    f.write(subj + os.linesep)
                    for stud in subj.lof_students:
                        # Vypis studentu v predmetu
                        student = subj.lof_students[stud]
                        f.write('{},{},{},{}'.format(student.id, student.first_name, student.last_name, student.class_id))
                        f.write(os.linesep)

        # Tvorba souboru output_zaci.csv
        # format souboru:
        #   {id_zaka},{jmeno_zaka},{prijmeni_zaka},{trida_zaka},{prvni_predmet},{druhy_predmet},...
        #   {id_zaka},{jmeno_zaka},{prijmeni_zaka},{trida_zaka},{prvni_predmet},{druhy_predmet},...
        #   {id_zaka},{jmeno_zaka},{prijmeni_zaka},{trida_zaka},{prvni_predmet},{druhy_predmet},...
        #   ...
        with open(os.path.join(dir_path, "output_zaci.csv"), "w") as f:
            for id in self.students:
                # Vypis zaku
                student = subj.students[stud]
                f.write('{},{},{},{}'.formta(student.id, student.first_name, student.last_name, student.class_id))
                # Vypis jeho zvolenych predmtu
                for item in student.sel_subj:
                    f.write(f',{item}')
                f.write(os.linesep)

    ## Funkce vycisti cely objekt
    #
    #  Seznam studentu, dnu a predmetu se vynuluje
    def clear(self):
        self.students.clear()
        self.subject.clear()
        self.days.clear()
        self.__day_or_subj_updated = False
        self.nof_sorted_students = 0