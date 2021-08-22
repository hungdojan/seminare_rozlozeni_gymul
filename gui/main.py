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
root.title("Pomocnik pro rozzarovani seminaru 1.0.0")
root.geometry("1920x810")

#   --- FUNKCE      ---
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
    # TODO:

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
    statusbar.config(text="¨Měním barvy ohraničení studentů...")

    # prochazi vsechny ramce ve virtualnim seznamu plnych ramcu
    poradnik = 0
    while poradnik <= poradnikMAX:
        for skupinka in virtualni_seznam_plnych_ramcu:
            
            if int(skupinka[7].get()) == poradnik:
                
                # obarveni podle vhodnych kombinaci
                student_id = skupinka[1].cget("text")
                pocet_komp_pred = len(ss.students[student_id].pass_subj)
                if pocet_komp_pred == 0:
                    zmenBarvu(int(student_id), "#ff0000")
                elif pocet_komp_pred == 1:
                    zmenBarvu(int(student_id), "#33ff00")
                else:
                    zmenBarvu(int(student_id), "#ffff00")
        
        poradnik += 1

    # update status baru
    statusbar.config(text="Aktualizuji pravy sloupec...")

    # vymazani praveho sloupce
    for child in megaFrameNaPredmety.winfo_children():
        child.destroy()

    # vykresleni prehledu predmetu v pravem sloupci spolu s cislem prihlasenych zaku
    megaFrameNaPredmety.columnconfigure(0, weight=1)
    pocitadloRadkuVPravemSloupci = 0
    for predmet in ss.subject:

        megaFrameNaPredmety.rowconfigure(pocitadloRadkuVPravemSloupci, weight=1)

        tempPrehledovyFrame = Frame(megaFrameNaPredmety)
        tempPrehledovyFrame_predmet = Label(tempPrehledovyFrame, text=predmet, width=14)
        tempPrehledovyLabel_pocet = Label(tempPrehledovyFrame, text=len(ss.students_per_subject[predmet]), width=5)

        tempPrehledovyFrame.rowconfigure(0, weight=1)
        tempPrehledovyFrame.columnconfigure(0, weight=1)
        tempPrehledovyFrame.columnconfigure(1, weight=1)

        tempPrehledovyFrame.grid(row=pocitadloRadkuVPravemSloupci, column=0, sticky='w', padx=16)
        tempPrehledovyFrame_predmet.grid(row=0, column=0, sticky='nsew')
        tempPrehledovyLabel_pocet.grid(row=0, column=1, sticky='nsew')
        tempPrehledovyFrame.config(highlightbackground="#000000", highlightcolor="#000000", highlightthickness=1)

        pocitadloRadkuVPravemSloupci += 1

    # update status baru
    statusbar.config(text="Přepočet dokončen.")

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
    # [Frame, ID Label, Jmeno Label, Prijmeni Label, 1.sem Entry, 2.sem Entry, 3.sem Entry, poradi, trida]
    for key in ss.students:
        defPoradi = len(virtualni_seznam_plnych_ramcu)
        tempStudent = ss.students[key]

        frame = virtualni_seznam_prazdnych_ramcu[index_prazdneho_ramce]
        idLabel = Label(frame, text=tempStudent.id, width=5)
        jmLabel = Label(frame, text=tempStudent.first_name, width=18)
        prijLabel = Label(frame, text=tempStudent.last_name, width=18)
        firstSem = Entry(frame, width=12); firstSem.insert(0, tempStudent.subjects[0])
        secondSem = Entry(frame, width=12); secondSem.insert(0, tempStudent.subjects[1])
        thirdSem = Entry(frame, width=12); thirdSem.insert(0, tempStudent.subjects[2])
        poradiEntry = Entry(frame, width=8); poradiEntry.insert(0, defPoradi)
        tridaLabel = Label(frame, text=tempStudent.class_id, width=5)

        virtualni_seznam_plnych_ramcu.append([frame, idLabel, jmLabel, prijLabel, firstSem, secondSem, thirdSem, poradiEntry, tridaLabel])
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
                skupinka[0].config(bg="#000000")

                # umistovani do sloupecku
                skupinka[1].grid(row=0, column=0, stick="nsew")
                skupinka[2].grid(row=0, column=1, stick="nsew")
                skupinka[3].grid(row=0, column=2, stick="nsew")
                skupinka[8].grid(row=0, column=3, stick="nsew")
                skupinka[4].grid(row=0, column=4, stick="nsew")
                skupinka[5].grid(row=0, column=5, stick="nsew")
                skupinka[6].grid(row=0, column=6, stick="nsew")
        poradnik += 1

    # update informaci
    refresh()

    # update statusbaru
    statusbar.config(text="Načítání studentů dokončeno.")

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

    refresh()

    # update status baru
    statusbar.config(text="Načítání předmětů dokončeno.")

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
    for predmet in ss.subject:
        checkerboxPromenna = IntVar()
        tempFramePredmetu = Frame(tempFrameDne)
        tempCheckButton = Checkbutton(tempFramePredmetu, text=predmet, variable=checkerboxPromenna, onvalue=1, offvalue=0)
        tempLabel = Label(tempFramePredmetu, text="0")

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

#   --- MENU BAR    ---
menubar = Menu(root, tearoff=0)
menubar.add_command(label="PŘEPOČÍTEJ", command=refresh)                                # 0
menubar.add_command(label="Vybrat soubor se studenty", command=nactiStudentyZeSouboru)  # 1
menubar.add_command(label="Vybrat soubor s předměty", command=nactiPredmetyZeSouboru)   # 2
menubar.add_command(label="Přidat nový den", command=pridejDen, state=DISABLED)         # 3
menubar.add_command(label="Odebrat poslední den", command=odeberDen, state=DISABLED)    # 4

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


#   --- CORE        ---
# vytvareni objektu: cedulky
nadpisLevo = Label(root, text="Seznam studentů")
nadpisStred = Label(root, text="Přehled dnů")
nadpisPravo = Label(root, text="Přehled předmětů") 
statusbar = Label(root, text="Nic nedělám.", bd=1, relief=SUNKEN, anchor="w")

# generovani te zasrane mrizky
root.columnconfigure(0, weight=1, minsize=650)      # seznam studentu
root.columnconfigure(1, weight=1, minsize=750)      # moznost zaskrtavat predmety jednotl. dnu
root.columnconfigure(2, weight=1, minsize=300)      # prehled predmetu s pocty studentu

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

# scrollovaci oblast v layoutu
container.grid(row=1, column=0, sticky='nsew')
canvas.pack(side="left", fill=BOTH, expand=True)
canvas.columnconfigure(0, weight=1, minsize=620)
scrollbar.pack(side="right", fill=Y)

#   --- NADPISY LEVEHO SLOUPCE  ---
# bunka s nadpisy (jako by neexistujici student nahore ve sloupecku, ale nebude veden v zadnem virtualnim seznamu)
nadpisovyFrame = Frame(root)
idLabel_nadp = Label(nadpisovyFrame, text="ID", width=5)
jmLabel_nadp = Label(nadpisovyFrame, text="JMÉNO", width=17)
prijLabel_nadp = Label(nadpisovyFrame, text="PŘÍJMENÍ", width=17)
firstSemLabel_nadp = Label(nadpisovyFrame, text="1. SEMINÁŘ", width=11)
secondSemLabel_nadp = Label(nadpisovyFrame, text="2. SEMINÁŘ", width=11)
thirdSemLabel_nadp = Label(nadpisovyFrame, text="3. SEMINÁŘ", width=11)
tridaLabel_nadp = Label(nadpisovyFrame, text="TŘÍDA", width=8)

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