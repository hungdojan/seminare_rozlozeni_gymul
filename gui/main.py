from os import stat
from tkinter import *
from typing import Collection
from sortsubj import *
from tkinter import filedialog as fd


# UZITECNY LINK
# https://realpython.com/python-gui-tkinter/

#   --- objekty:    ---
# Label
# Button
# Entry     ...     textove interaktivni pole
# Frame     ...     ramec / skupina vice objektu

#   --- funkce:     ---
# .pack()           zobrazi na obrazovku
# .mainLoop()       bude prubezne aktualizovat stavy
# .grid()           priradi mrizce ! NELZE ZAROVEN S .grid A .pack !
# .get()            ziska obsah interaktivniho pole

#   --- argumenty:  ---
# prvni argument        =   matersky widget
# row                   =   cislo relativniho radku
# column                =   cislo relativniho sloupce 
# state                 =   ENABLED / DISABLED
# padx / pady           =   velikost v pixelech x/y
# command               =   jmenu funkce po aktivaci BEZ ZAVOREK
# fg                    =   foreground colour ve formatu "#000000"
# bg                    =   background colour ve formatu "#000000"
# width                 =   sirka v pixelech

#   --- GLOBALNI PROMENNE   ---
# nelze menit primo ve funkci kvuli pamatovani si poradi pro pripad nacitani vice souboru za sebou
tempdir = ""
index_prazdneho_ramce = 0       
virtualni_seznam_dnu = []     
virtualni_seznam_prazdnych_ramcu = [] 
virtualni_seznam_plnych_ramcu = []
poradnikMAX = 0
ss = SubSort()

#   --- MAIN        ---
root = Tk()
root.title("Pomocnik pro rozrazovani seminaru 1.1.0")
root.geometry("1920x810")

#   --- CORE            ---
# vytvareni objektu: cedulky
nadpisLevo = Label(root, text="Seznam studentů")
nadpisStred = Label(root, text="Přehled dnů")
nadpisPravo = Label(root, text="Přehled") 
statusbar = Label(root, text="Nic nedělám.", bd=1, relief=SUNKEN, anchor="w")

# generovani te zasrane mrizky
root.columnconfigure(0, weight=1, minsize=700)       # seznam studentu
root.columnconfigure(1, weight=1, minsize=1000)      # moznost zaskrtavat predmety jednotl. dnu
root.columnconfigure(2, weight=1, minsize=12)        # prehled predmetu s pocty studentu

root.rowconfigure(0, weight=2, minsize=25)          # nadpisy
root.rowconfigure(1, weight=10, minsize=680)        # dulezity obsah sloupcu (hodne mista)
root.rowconfigure(2, weight=1, minsize=12)          # status bar

# prirazeni do mrizky 
nadpisStred.grid(row=0, column=1)
nadpisPravo.grid(row=0, column=2)
statusbar.grid(row=3, column=0, columnspan=3, sticky="nsew")

# obri framy
megaFrameNaDny = Frame(root)                                # dny v prostrednim sloupci
megaFrameNaDny.grid(row=1, column=1, sticky='nsew')
megaFrameNaPredmety = Frame(root)                           # prehled predmetu v pravem sloupci
megaFrameNaPredmety.grid(row=1, column=2, sticky='nsew')    
#   --- MUSI BYT NAHORE ---


#   --- FUNKCE      ---
def volbaKombinace(button_id): # ERROR, BUTTON_ID JE NEUSTALE 116
    okVar = IntVar()

    # otevirani okna
    volbaKombinaceOkno = Toplevel(root)
    volbaKombinaceOkno.title("Výběr kombinace")
    volbaKombinaceOkno.geometry("768x480")
    mainFrameKombinace = Frame(volbaKombinaceOkno)
    mainFrameKombinace.pack()

    mainFrameKombinace.columnconfigure(0, weight=1) # seznam kombinaci
    mainFrameKombinace.columnconfigure(1, weight=1) # tlacitko vyberu

    stisknuty_button = IntVar()         #Creating a variable which will track the selected checkbutton
    cb = []                             #Empty list which is going to hold all the checkbutton        

    pocitadloKombinace = 0
    for mozna_kombinace in ss.students[button_id].pass_subj:
        
        mainFrameKombinace.rowconfigure(pocitadloKombinace, weight=1)
        tempLabelKomb = Label(mainFrameKombinace, text=mozna_kombinace, width=24)
        tempButtonKomb = Checkbutton(mainFrameKombinace, onvalue = pocitadloKombinace, variable = stisknuty_button, width=2, state=DISABLED)
        cb.append(tempButtonKomb)

        tempLabelKomb.grid(row=pocitadloKombinace, column=0, sticky="nsew")
        cb[pocitadloKombinace].grid(row=pocitadloKombinace, column=1, sticky="nsew")

        if mozna_kombinace == ss.students[button_id].sel_subj:
            stisknuty_button.set(pocitadloKombinace)

        pocitadloKombinace += 1

    # close button
    mainFrameKombinace.rowconfigure(pocitadloKombinace, weight=1)
    CloseButtonKomb = Button(mainFrameKombinace, text="HOTOVO", state=DISABLED, command=lambda : okVar.set(1))
    CloseButtonKomb.grid(row=pocitadloKombinace, column=0, columnspan=2, sticky="nsew")

    # tesne pred cekanim umozneni volby
    for cudlik in cb:
        cudlik.config(state=NORMAL)
    CloseButtonKomb.config(state=NORMAL)

    # uzavreni okna
    volbaKombinaceOkno.wait_variable(okVar)

    # reseni vyberu dane kombinace a jeji oznameni algoritmu
    ss.student_sel_subject(button_id, stisknuty_button.get())

    # zavreni okna
    volbaKombinaceOkno.destroy()
    refresh()
    

def refresh():
    global statusbar
    global virtualni_seznam_plnych_ramcu
    global virtualni_seznam_dnu
    global poradnikMAX
    global ss
    global megaFrameNaDny
    global megaFrameNaPredmety

    # update status baru
    statusbar.config(text="Přepočítávám...")
    
    # odblokovani tlacitek kontextoveho menu
    if len(virtualni_seznam_dnu) > 0:
        menubar.entryconfig(4, state=NORMAL)
    else:
        menubar.entryconfig(4, state=DISABLED)

    if len(ss.subject) > 0:
        menubar.entryconfig(3, state=NORMAL)
    else:
        menubar.entryconfig(3, state=DISABLED)

    if len(virtualni_seznam_dnu) >= 5:
        menubar.entryconfig(3, state=DISABLED)

    # vymazani pripadnych dnu z plochy
    for den in virtualni_seznam_dnu:

        for predmet in den[1]:
            for i in range(3):
                predmet[i].pack_forget()

        den[0].pack_forget()

    # pridani do gui zakladu pro dny
    megaFrameNaDny.grid(row=1, rowspan=2, column=1)

    # přidávání předmětů do aktivních dnů
    if len(virtualni_seznam_dnu) > 0 and len(ss.subject) > 0:
        pocitadloDnu = 0
        for den in virtualni_seznam_dnu:
            
            den[0].pack()
            den[0].config(highlightbackground="#000000", highlightcolor="#000000", highlightthickness=4)
            den[0].rowconfigure(0, weight=1)
            pocitadloSloupeckuVeDni = 0
            
            for predmet in den[1]:
                den[0].columnconfigure(pocitadloSloupeckuVeDni, weight=1)

                # umistovani jednotlivych polozek do radku
                predmet[0].grid(row=0, column=pocitadloSloupeckuVeDni)
                predmet[0].config(highlightbackground="#a0a0a0", highlightcolor="#a0a0a0", highlightthickness=1)
                predmet[0].rowconfigure(0, weight=1)
                predmet[0].columnconfigure(0, weight=2)
                predmet[0].columnconfigure(1, weight=1)

                predmet[1].grid(row=0, column=0)
                predmet[2].grid(row=0, column=1)

                # kontrola checkerboxu
                day = ss.days[pocitadloDnu]
                subject_name = predmet[1].cget("text")
                if predmet[3].get():
                    ss.add_subject_to_day(pocitadloDnu, subject_name)
                else:
                    ss.delete_subject_from_day(pocitadloDnu, subject_name)

                pocitadloSloupeckuVeDni += 1
            pocitadloDnu += 1

    # prezkoumani studentu se zmenenymi predmety
    # [Frame, ID Label, Jmeno Label, Prijmeni Label, 1.sem Entry, 2.sem Entry, 3.sem Entry, poradi, trida, tlacitko] = student
    for student in virtualni_seznam_plnych_ramcu:
       
        student_id = student[1].cget("text")
        sem = student[4].get(), student[5].get(), student[6].get()

        if (sem[0] in ss.subject) and (sem[1] in ss.subject) and (sem[2] in ss.subject):
            if (sem != ss.students[student_id].subjects):   # ZMENA, KTERA ROZBILA POCITANI PREDMETU
                ss.student_change_subjects(student_id, [student[4].get(),student[5].get(),student[6].get()])

        else:
            zmenBarvu(int(student_id), "#3333ff")
            statusbar.config(text="ERROR U MODRÉHO STUDENTA")
            return



    # update status baru
    statusbar.config(text="Zkoumám vhodné kombinace...")

    # prepocita kombinace
    ss.sort_data()

    if len(virtualni_seznam_dnu) > 0 and len(ss.subject) > 0:
        pocitadloDnu = 0
        for den in virtualni_seznam_dnu:
            for predmet in den[1]:
                if predmet[3].get():
                    # update poctu studentu
                    predmet[2].config(text=len(ss.days[pocitadloDnu].subjects[predmet[1].cget("text")].lof_students))
                else:
                    predmet[2].config(text="0")
            pocitadloDnu += 1

    # update status baru
    statusbar.config(text="Měním barvy ohraničení studentů...")

    # prochazi vsechny ramce ve virtualnim seznamu plnych ramcu
    poradnik = 0
    while poradnik <= poradnikMAX:
        for skupinka in virtualni_seznam_plnych_ramcu:
            
            if int(skupinka[7].get()) == poradnik:
                
                # obarveni podle vhodnych kombinaci
                student_id = skupinka[1].cget("text")
                pocet_komp_pred = len(ss.students[student_id].pass_subj)
                if pocet_komp_pred == 0:
                    # zadna vhodna kombinace
                    zmenBarvu(int(student_id), "#ff0000")
                    skupinka[9].config(state=DISABLED)
                elif pocet_komp_pred == 1:
                    # 1 spravna kombinace
                    zmenBarvu(int(student_id), "#00ff00")
                    skupinka[9].config(state=DISABLED)
                elif ss.students[student_id].sel_subj is not None:
                    # vice moznosti, jiz zvolena
                    zmenBarvu(int(student_id), "#6a15bf")
                    skupinka[9].config(state=NORMAL)
                else:
                    # vice moznzch kombinaci
                    zmenBarvu(int(student_id), "#ddff00")
                    skupinka[9].config(state=NORMAL)

        poradnik += 1

    # update status baru
    statusbar.config(text="Aktualizuji pravy sloupec...")

    # vymazani praveho sloupce
    for child in megaFrameNaPredmety.winfo_children():
        child.destroy()

    # vykresleni prehledu predmetu v pravem sloupci spolu s cislem prihlasenych zaku
    megaFrameNaPredmety.columnconfigure(0, weight=1)
    pocitadloRadkuVPravemSloupci = 0
    lof_subjects = list(ss.subject)
    lof_subjects.sort()
    poradnikPredmetuPravehoSloupce = len(ss.students)
    while poradnikPredmetuPravehoSloupce >= 0:
        for predmet in lof_subjects:
            if poradnikPredmetuPravehoSloupce == len(ss.students_per_subject[predmet]):
                megaFrameNaPredmety.rowconfigure(pocitadloRadkuVPravemSloupci, weight=1)

                tempPrehledovyFrame = Frame(megaFrameNaPredmety)
                tempPrehledovyLabel_predmet = Label(tempPrehledovyFrame, text=predmet, width=6)
                tempPrehledovyLabel_pocet = Label(tempPrehledovyFrame, text=len(ss.students_per_subject[predmet]), width=3)

                tempPrehledovyFrame.rowconfigure(0, weight=1)
                tempPrehledovyFrame.columnconfigure(0, weight=1)
                tempPrehledovyFrame.columnconfigure(1, weight=1)

                tempPrehledovyFrame.grid(row=pocitadloRadkuVPravemSloupci, column=0, sticky='w', padx=16)
                tempPrehledovyLabel_predmet.grid(row=0, column=0, sticky='nsew')
                tempPrehledovyLabel_pocet.grid(row=0, column=1, sticky='nsew')
                tempPrehledovyFrame.config(highlightbackground="#000000", highlightcolor="#000000", highlightthickness=1)

                pocitadloRadkuVPravemSloupci += 1
        poradnikPredmetuPravehoSloupce -= 1

    # update status baru
    statusbar.config(text="Všechny operace dokončeny, momentálně nepracuji.")

def zmenBarvu(id, barva):
    global virtualni_seznam_plnych_ramcu

    for skupinka in virtualni_seznam_plnych_ramcu:
        if int(skupinka[1].cget("text")) == id:
            skupinka[0].config(highlightbackground=barva, highlightcolor=barva, highlightthickness=4)

def nactiStudentyZeSouboru():
    global statusbar
    global tempdir
    global index_prazdneho_ramce
    global virtualni_seznam_plnych_ramcu
    global virtualni_seznam_prazdnych_ramcu
    global poradnikMAX
    global ss

    # update status baru
    statusbar.config(text="Mažu předchozí seznam studentů...")

    # mazani kvuli duplikaci studentu
    for group in virtualni_seznam_plnych_ramcu:
        for item in group:
            item.pack_forget()
    index_prazdneho_ramce = 0             
    virtualni_seznam_prazdnych_ramcu = [] 
    virtualni_seznam_plnych_ramcu = []
    poradnikMAX = 0

    # snaha o pamatovani si cesty
    currdir = os.getcwd()
    if tempdir is not ("" or currdir):
        currdir = tempdir
    
    # update status baru
    statusbar.config(text="Čekám na vybrání souboru...")

    # dialogove okno
    tempdir = fd.askopenfilename(parent=root, initialdir=currdir, title='Vyberte soubor se studenty')

    # pri zruseni vyberu
    if tempdir == "" or tempdir == None:
        statusbar.config(text="Výběr studentů zrušen.")
        return   

    # nacitani studentu do slovniku
    statusbar.config(text="Načítání studentů...")
    path = tempdir
    if ss.load_file_student(path) == False:    
        oznamovaciOkno("Chyba", "300x50", "Nepodařilo se načíst soubor se studenty.")
        statusbar.config(text="Načítání studentů zrušeno důsledkem chyby při výběru souboru.")
        return

    # vytvareni framu pro kazdeho studenta
    for key in ss.students:
        virtualni_seznam_prazdnych_ramcu.append(Frame(scrollable_frame))

    # pridavani podrazenych poli do framu kazdeho studenta
    # sklada se z listu: 
    # [Frame, ID Label, Jmeno Label, Prijmeni Label, 1.sem Entry, 2.sem Entry, 3.sem Entry, poradi, trida, TLACITKO NA ZMENU KOMBINACE]
    for key in ss.students:
        defPoradi = len(virtualni_seznam_plnych_ramcu)
        tempStudent = ss.students[key]
        tempID = tempStudent.id

        frame = virtualni_seznam_prazdnych_ramcu[index_prazdneho_ramce]
        idLabel = Label(frame, text=tempID, width=5)
        jmLabel = Label(frame, text=tempStudent.first_name, width=18)
        prijLabel = Label(frame, text=tempStudent.last_name, width=18)
        firstSem = Entry(frame, width=8); firstSem.insert(0, tempStudent.subjects[0])
        secondSem = Entry(frame, width=8); secondSem.insert(0, tempStudent.subjects[1])
        thirdSem = Entry(frame, width=8); thirdSem.insert(0, tempStudent.subjects[2])
        poradiEntry = Entry(frame, width=8); poradiEntry.insert(0, defPoradi)
        tridaLabel = Label(frame, text=tempStudent.class_id, width=5)
        zmenaKombinaceButton = Button(frame, text="komb.", state=DISABLED, command=lambda button_id = tempID: volbaKombinace(button_id))

        virtualni_seznam_plnych_ramcu.append([frame, idLabel, jmLabel, prijLabel, firstSem, secondSem, thirdSem, poradiEntry, tridaLabel, zmenaKombinaceButton])
        index_prazdneho_ramce += 1
        poradnikMAX = defPoradi

    # zobrazovani obsahu virtualniho seznamu v okne
    poradnik = 0
    while poradnik <= poradnikMAX:
        for skupinka in virtualni_seznam_plnych_ramcu:
            
            if int(skupinka[7].get()) == poradnik:

                # umisteni framu / ramce
                canvas.rowconfigure(poradnik, weight=1)
                skupinka[0].grid(row=poradnik, column=0, stick="nsew")
                
                # vygenerovani pomerovych sloupecku
                skupinka[0].rowconfigure(0, weight=1)
                skupinka[0].columnconfigure(0, weight=1, uniform=8)
                skupinka[0].columnconfigure(1, weight=10, uniform=18)
                skupinka[0].columnconfigure(2, weight=10, uniform=18)
                skupinka[0].columnconfigure(3, weight=3, uniform=12)
                skupinka[0].columnconfigure(4, weight=3, uniform=12)
                skupinka[0].columnconfigure(5, weight=3, uniform=12)
                skupinka[0].columnconfigure(6, weight=3, uniform=12)
                skupinka[0].columnconfigure(7, weight=3, uniform=12)
                skupinka[0].config(bg="#000000")

                # umistovani do sloupecku
                skupinka[1].grid(row=0, column=0, stick="nsew")
                skupinka[2].grid(row=0, column=1, stick="nsew")
                skupinka[3].grid(row=0, column=2, stick="nsew")
                skupinka[8].grid(row=0, column=3, stick="nsew")
                skupinka[4].grid(row=0, column=4, stick="nsew")
                skupinka[5].grid(row=0, column=5, stick="nsew")
                skupinka[6].grid(row=0, column=6, stick="nsew")
                skupinka[9].grid(row=0, column=7, stick="nsew")
        poradnik += 1

    # update statusbaru
    statusbar.config(text="Načítání studentů dokončeno.")

    # update informaci
    refresh()

def nactiPredmetyZeSouboru():
    global statusbar
    global tempdir
    global index_prazdneho_ramce
    global poradnikMAX
    global ss
    global megaFrameNaDny
    
    # update status baru
    statusbar.config(text="Mažu předchozí seznam předmětů...")

    # snaha o pamatovani si cesty
    currdir = os.getcwd()
    if tempdir is not ("" or currdir):
        currdir = tempdir
    
    # update status baru
    statusbar.config(text="Čekám na vybrání souboru...")

    # dialogove okno
    tempdir = fd.askopenfilename(parent=root, initialdir=currdir, title='Vyberte soubor s předměty')

    # nacitani predmetu
    statusbar.config(text="Načítání předmětů...")
    path = tempdir
    if ss.load_file_subjects(path) == False:    
        oznamovaciOkno("Chyba", "300x50", "Nepodařilo se načíst soubor s předměty.")
        statusbar.config(text="Načítání předmětů zrušeno důsledkem chyby při výběru souboru.")
        return

    # update status baru
    statusbar.config(text="Načítání předmětů dokončeno.")

    refresh()

def pridejDen():
    global virtualni_seznam_dnu
    global statusbar

    # update status baru
    statusbar.config(text="Přidávám další den...")


    ss.add_day([])
    tempFrameDne = Frame(megaFrameNaDny)
    tempSeznamPredmetu = []

    # pridavani podrazenych poli do framu kazdeho predmetu
    # sklada se z listu: 
    # [Frame, CheckBox s nazvem predmetu, pocet studentu Label, zavisla promenna pro checkerbox]
    lof_subjects = list(ss.subject)
    lof_subjects.sort()
    for predmet in lof_subjects:
        checkerboxPromenna = IntVar()
        tempFramePredmetu = Frame(tempFrameDne)
        tempCheckButton = Checkbutton(tempFramePredmetu, text=predmet, variable=checkerboxPromenna, onvalue=1, offvalue=0)
        tempLabel = Label(tempFramePredmetu, text="0", width=2)

        tempSeznamPredmetu.append([tempFramePredmetu, tempCheckButton, tempLabel, checkerboxPromenna])

    virtualni_seznam_dnu.append([tempFrameDne, tempSeznamPredmetu])
    
    refresh()

def odeberDen():
    global virtualni_seznam_dnu
    global statusbar

    # update status baru
    statusbar.config(text="Odebírám poslední přidaný den...")

    if len(virtualni_seznam_dnu) > 0:
        for predmet in (virtualni_seznam_dnu[-1])[1]:
            for x in range(3):
                predmet[x].pack_forget()

        (virtualni_seznam_dnu[-1])[0].pack_forget()

        virtualni_seznam_dnu.pop()
        ss.delete_day((len(virtualni_seznam_dnu)-1))

        refresh()

def oznamovaciOkno(jmeno, rozliseni, textHlaseni):     
    
    # Toplevel object which will
    # be treated as a new window
    newWindow = Toplevel(root)
 
    # sets the title of the
    # Toplevel widget
    newWindow.title(jmeno)
 
    # sets the geometry of toplevel
    newWindow.geometry(rozliseni)
 
    # A Label widget to show in toplevel
    Label(newWindow,
          text=textHlaseni).pack()

def exportDat():
    refresh()
    cesta_export = fd.askdirectory(title='Vyberte složku pro export dat')
    if cesta_export == "" or cesta_export == None:
        oznamovaciOkno("ERROR", "250x100", "Nepodařilo se vyexportovat data")
    else:    
        ss.generate_files(cesta_export)
        hlaseni_o_exportu = "Data byla úspěšně vyexportována do " + cesta_export
        oznamovaciOkno("Úspěch", "500x100", hlaseni_o_exportu)

#   --- KONEC FUNKCI    ---


#   --- MENU BAR    ---
menubar = Menu(root, tearoff=0)
menubar.add_command(label="REFRESH", command=refresh)                                  # 0
menubar.add_command(label="Vybrat soubor se studenty", command=nactiStudentyZeSouboru) # 1
menubar.add_command(label="Vybrat soubor s předměty", command=nactiPredmetyZeSouboru)  # 2
menubar.add_command(label="Přidat nový den", command=pridejDen, state=DISABLED)        # 3
menubar.add_command(label="Odebrat poslední den", command=odeberDen, state=DISABLED)   # 4
menubar.add_command(label="Exportovat data do souboru", command=exportDat)             # 5

#   --- SCROLL BAR  ---
container = Frame(root) 
canvas = Canvas(container)
scrollbar = Scrollbar(container, orient="vertical", command=canvas.yview)
scrollable_frame = Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

canvas.configure(yscrollcommand=scrollbar.set)

# scrollovaci oblast v layoutu
container.grid(row=1, column=0, sticky='nsew')
canvas.pack(side="left", fill=BOTH, expand=True)
canvas.columnconfigure(0, weight=1, minsize=620)
scrollbar.pack(side="right", fill=Y)

#   --- NADPISY LEVEHO SLOUPCE  ---
# bunka s nadpisy (jako by neexistujici student nahore ve sloupecku, ale nebude veden v zadnem virtualnim seznamu)
nadpisovyFrame = Frame(root)
idLabel_nadp = Label(nadpisovyFrame, text="ID", width=5)
jmLabel_nadp = Label(nadpisovyFrame, text="JMÉNO", width=18)
prijLabel_nadp = Label(nadpisovyFrame, text="PŘÍJMENÍ", width=11)
firstSemLabel_nadp = Label(nadpisovyFrame, text="SEM1", width=7)
secondSemLabel_nadp = Label(nadpisovyFrame, text="SEM2", width=7)
thirdSemLabel_nadp = Label(nadpisovyFrame, text="SEM3", width=7)
tridaLabel_nadp = Label(nadpisovyFrame, text="TŘÍDA", width=6)

# umisteni nadpisoveho framu
nadpisovyFrame.grid(row=0, column=0, stick="w")

# vygenerovani pomerovych sloupecku pro nadp. frame
nadpisovyFrame.rowconfigure(0, weight=1)
nadpisovyFrame.columnconfigure(0, weight=1, uniform=8)
nadpisovyFrame.columnconfigure(1, weight=10, uniform=18)
nadpisovyFrame.columnconfigure(2, weight=10, uniform=18)
nadpisovyFrame.columnconfigure(3, weight=3, uniform=12)
nadpisovyFrame.columnconfigure(4, weight=3, uniform=12)
nadpisovyFrame.columnconfigure(5, weight=3, uniform=12)
nadpisovyFrame.columnconfigure(6, weight=3, uniform=12)

# umistovani nadpisu do sloupecku
idLabel_nadp.grid(row=0, column=0, stick="nsew")
jmLabel_nadp.grid(row=0, column=1, stick="nsew")
prijLabel_nadp.grid(row=0, column=2, stick="nsew")
tridaLabel_nadp.grid(row=0, column=3, stick="nsew")
firstSemLabel_nadp.grid(row=0, column=4, stick="nsew")
secondSemLabel_nadp.grid(row=0, column=5, stick="nsew")
thirdSemLabel_nadp.grid(row=0, column=6, stick="nsew")

#   --- END       ---
# aktualizace stavu na konci programu
# stisknuti krizku u okna prerusi mainloop
root.config(menu=menubar)
root.mainloop()
