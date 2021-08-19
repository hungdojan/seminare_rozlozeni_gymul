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
import itertools
from sortsubj.student import Student
from sortsubj.day import Day
from sortsubj.consts import *

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
        self.students_per_subject = dict()
        ## Flag ukazuje, jestli byla aktualizace dnu zaznamenana
        #  Studenti by meli byt znovu roztrizeni 
        self.__day_up_to_dated = True
        ## Flag ukazuje, jestli byla aktualizace predmetu zaznamenana
        self.__subj_up_to_dated = True
        ## Pocet studentu s vybranym 
        self.nof_sorted_students = 0
        ## Hashmap moznych kombinaci
        self.__hashmap_combination = dict()
        ## Hashmap ostatnich kombinaci (pokud ma student vybrano mene predmetu nez je dnu)
        self.__hashmap_custom_combination = dict()

    ## Funkce prevadi kombinaci na klic
    #
    #  @param comb Kombinace, ktera je typu 'tuple'
    #  @return Vraci klice S1-S2-S3-...-Sn, kde Sn jsou vybrane predmety serazene abecedne
    def __combination_to_key(self, comb: tuple):
        my_list = list(comb)
        my_list.sort()
        return KEY_DELIM.join(my_list)
    
    ## Funkce vraci pocet zaku, ktery navstevuje dany predmet
    #
    #  @param subj_name Jmeno predmetu
    #  @return Pocet zaku v danem predmetu; #NONE pokud predmet neexistuje
    def get_nof_students_in_subject(self, subj_name):
        if subj_name in self.students_per_subject:
            return len(self.students_per_subject[subj_name])
        return None
    
    ## Funkce nove roztridi dny do hashmapy kombinaci
    def __update_combinations(self):
        # nacte seznam predmetu za kazdy den
        lof_subs_per_day = list()
        for days in self.days:
            lof_subs_per_day.append(days.subjects.keys())

        # vytvori permutaci (vsechny mozne kombinace)
        temp_list = list(itertools.product(*lof_subs_per_day))

        # pruchod vsemi kombinacemi
        for comb in temp_list:
            # filtrace duplikatu v jedne kombinace
            if len(comb) != len(set(comb)):
                continue
            # vytvoreni klice a nasledne vlozeni kombinace
            key = self.__combination_to_key(comb)
            if key not in self.__hashmap_combination:
                self.__hashmap_combination[key] = list()
            self.__hashmap_combination[key].append(comb)

    ## Aktualizace flagu a seznamu
    def request_update(self):
        self.__day_up_to_dated = False
        # vynulovani dat
        list(map(lambda x: self.students[x].clear_data(), self.students.keys()))
        list(map(lambda x: x.clear_subs, self.days))
        self.nof_sorted_students = 0
        # vynulovani hashmapy s kombinacemi a nasledne znovu nacteni
        self.__hashmap_combination.clear()
        self.__update_combinations()

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
        # Aktualizace pocitadla predmetu
        if self.students[id].subjects is not None:
            for i in subjects:
                if i not in self.students_per_subject:
                    self.students_per_subject[i] = set()
                self.students_per_subject[i].add(id)
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
            # Aktualizace pocitadla studentu
            if self.students[id].subjects is not None:
                for i in self.students[id].subjects:
                    if i in self.students_per_subject:
                        self.students_per_subject[i].remove(id)
                
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
        if student_id not in self.students:
            raise Exception("Student jeste neni v seznamu")
        if len(self.students[student_id].pass_subj) <= index or index < 0:
            return
        
        # Docasna ulozeni kombinace pro pripadne pozdejsi mazani
        temp_combination = self.students[student_id].sel_subj
        # Zjisti, zda byl student jiz prerazen
        output = self.students[student_id].set_sel_subj(index)

        # Pokud jsou predmety poprve vybrany, je student pridan do jednotlivych predmetu dle dne
        if output:
            for i in range(len(self.students[student_id].sel_subj)):
                if self.students[student_id].sel_subj[i] is None:
                    continue
                else:
                    self.days[i].subjects[self.students[student_id].sel_subj[i]].add_student(self.students[student_id])

            # Nasledne je aktualizovano pocitadlo rozrazenych studentu
            self.nof_sorted_students += 1

        # Pokud jiz byl student alespon jednou pridan
        # je odstranen z puvodni kombinace
        else:
            # Smazani studenta
            for i in range(len(temp_combination)):
                # pokud aktualni predmet nebyl definovany, tak je tato iterace preskocena
                if temp_combination[i] is None:
                    continue
                self.days[i].subjects[temp_combination[i]].remove_student(student_id)
            # Pridani studenta
            for i in range(len(self.students[student_id].sel_subj)):
                # pokud aktualni predmet neni definovany, tak je tato iterace preskocena
                if self.students[student_id].sel_subj[i] is None:
                    continue
                self.days[i].subjects[self.students[student_id].sel_subj[i]].add_student(self.students[student_id])
    
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
        # Vynulovani data u studentu a ostatnich dnu
        self.request_update()

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
        # Vynulovani data u studentu a ostatnich dnu
        self.request_update()

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
            self.__subj_up_to_dated = False
        
        if subj_name is not None:
            self.students_per_subject[subj_name] = set()

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
            self.__subj_up_to_dated = False
    
        if subj_name is not None and subj_name in self.students_per_subject:
            del self.students_per_subject[subj_name]

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
                data = re.split(INPUT_FILE_DELIM, line.rstrip(EOF))
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
                data = re.split(INPUT_FILE_DELIM, line.rstrip(EOF))
                data = set(data)
                # validace predmetu
                for subj in data:
                    if subj not in self.subject:
                        raise Exception(f'Predmet {subj} jeste neni definovany!')
                self.add_day(data)
        self.__subj_up_to_dated = False

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
                self.add_subject(line.rstrip(EOF))
        self.request_update()

    ## Funkce zjistuje, zda neuplna kombinace jde setridit
    #
    #  @param subject Studentuv vyber predmetu
    def __get_custom_combination(self, subject: tuple):
        """
            Prochazi se cely seznam vsech kombinaci, kde se vezmou jednotlive klice, ty se rozdeli 
            na jednotlive predmety podle KEY_DELIM a ulozi do listu.
                Pr. aj-b-d --> ['aj', 'b', 'd']
            Pote odstrani nedefinovane predmety u studenta.
                Pr. ('a', 'd', None) -> ['a', 'd']
            A porovnava tyto listy. Pokud budou vsechny predmety ve studentovem seznamu v kombinovanem seznamu.
            Projedou se jednotlive kombinace nachazejici se pod danym klicem (self.__hashmap_combination['aj-b-d'])
            a zkontroluje se, zda v dany den muze student tento predmet navstevovat. Pokud ne, na takovem miste nastavi
            hodnotu #NONE. Nakonec vyslednou kombinaci ulozi do seznamu nalezenych kombinaci a tu nakonec vrati.
                Pr. nalezena kombinace je ['a', None, 'd']
        """
        all_combinations = list()
        # studentuv vyber bez None
        temp_student_list = list(filter(None, subject))
        for key in self.__hashmap_combination:
            # predmety v kombinaci
            key_list = key.split(KEY_DELIM)
    
            # Vsechny predmety souhlasi
            if all(item in key_list for item in temp_student_list):
                # Vysledny list se vybery dnu
                # prochazi vsechny predmety v kombinaci (dnu)
                for comb in self.__hashmap_combination[key]:
                    output_list = list()
                    for sub in comb:
                        # pokud je dany predmet vybran i studenten, je vlozen 
                        if sub in temp_student_list:
                            output_list.append(sub)
                        # pokud student nema vybrany dany predmet, je do toho dne nastaven #NONE
                        else:
                            output_list.append(None)

                    output_list = tuple(output_list)
                    # prida finalni kombinaci, pokud jeste nebyla ulozena
                    if output_list not in all_combinations:
                        all_combinations.append(output_list)

        return all_combinations

    ## Funkce prerovna studenty do danych dnu a predmetu
    def sort_data(self):
        # TODO: hlavni cast programu; je mozne ze se obsah da do vice souboru
        # obsah teto funkce se ponecha pozdeji
        # mel by zpracovat informace
        # projekt kombinace a zjistit u kazdeho studenta, zda u nej vyhovyji predmety
        """
            Funkce se zklada ze 2 casti:
                - funkce projede vsechny studenty a najde u nic uspesne kombinace
                - pokud ma student jen jednu uspesnou kombinaci, kombinace je ulozena do student.pass_subj
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
        for id in self.students:
            
            # student ma vybrano vice predmetu
            if len(self.students[id].subjects) > len(self.days):
                continue
            key = self.__combination_to_key(self.students[id].subjects)
            if len(self.students[id].subjects) == len(self.days):
                # vyhledavani v predem setrizenem seznamu
                if key in self.__hashmap_combination:
                    self.students[id].pass_subj = self.__hashmap_combination[key]
            # student ma mene predmetu nez je dnu
            else:
                if key not in self.__hashmap_combination:
                    self.__hashmap_custom_combination[key] = self.__get_custom_combination(self.students[id].subjects)
                self.students[id].pass_subj = self.__hashmap_custom_combination[key]

            # student ma jedinou moznost
            if len(self.students[id].pass_subj) == 1:
                self.student_sel_subject(id, 0)
            
            self.students[id].sorted = True
        
        # Uprava flagu
        self.__day_up_to_dated = True
        self.__subj_up_to_dated = True

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
        with open(os.path.join(dir_path, "output_dny.csv"), 'w', encoding='utf-8') as f:
            for i in range(len(self.days)):
                # Vybrany den
                f.write(f'Den {i}{OUTPUT_EOF}')
                for subj_key in self.days[i].subjects:
                    # Vybrany predmet
                    f.write(subj_key + OUTPUT_EOF)
                    for stud in self.days[i].subjects[subj_key].lof_students:
                        # Vypis studentu v predmetu
                        student = self.days[i].subjects[subj_key].lof_students[stud]
                        f.write('{},{},{},{}'.format(student.id, student.first_name, student.last_name, student.class_id))
                        f.write(OUTPUT_EOF)
                    f.write(OUTPUT_EOF)
                f.write(OUTPUT_EOF)

        # Tvorba souboru output_zaci.csv
        # format souboru:
        #   {id_zaka},{jmeno_zaka},{prijmeni_zaka},{trida_zaka},{prvni_predmet},{druhy_predmet},...
        #   {id_zaka},{jmeno_zaka},{prijmeni_zaka},{trida_zaka},{prvni_predmet},{druhy_predmet},...
        #   {id_zaka},{jmeno_zaka},{prijmeni_zaka},{trida_zaka},{prvni_predmet},{druhy_predmet},...
        #   ...
        with open(os.path.join(dir_path, "output_zaci.csv"), "w", encoding='utf-8') as f:
            for id in self.students:
                # Vypis zaku
                student = self.students[id]
                f.write('{},{},{},{}'.format(student.id, student.first_name, student.last_name, student.class_id))
                # Vypis jeho zvolenych predmtu
                if student.sel_subj is not None:
                    for item in student.sel_subj:
                        f.write(f',{item}')
                f.write(OUTPUT_EOF)

    ## Funkce vycisti cely objekt
    #
    #  Seznam studentu, dnu a predmetu se vynuluje
    def clear(self):
        self.students.clear()
        self.subject.clear()
        self.days.clear()
        self.__day_up_to_dated = True
        self.__subj_up_to_dated = True
        self.nof_sorted_students = 0