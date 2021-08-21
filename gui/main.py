from tkinter import *
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
virtualni_seznam_predmetu = [] 
virtualni_seznam_dnu = []     
virtualni_seznam_prazdnych_ramcu = [] 
virtualni_seznam_plnych_ramcu = []
poradnikMAX = 0
ss = SubSort()

#   --- MAIN        ---
root = Tk()
root.title("Pomocnik pro rozzarovani seminaru 1.0.0")
root.geometry("1890x810")

#   --- FUNKCE      ---
def refresh():
    global statusbar
    global virtualni_seznam_plnych_ramcu
    global poradnikMAX
    global ss

    # update status baru
    statusbar.config(text="Přepočítávám...")

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
                    zmenBarvu(int(student_id), "#00ff00")
                else:
                    zmenBarvu(int(student_id), "#ffff00")
        
        poradnik += 1

    # update status baru
    statusbar.config(text="Přepočet dokončen.")

def zmenBarvu(id, barva):
    global virtualni_seznam_plnych_ramcu

    for skupinka in virtualni_seznam_plnych_ramcu:
        if int(skupinka[1].cget("text")) == id:
            skupinka[0].config(highlightbackground=barva, highlightcolor=barva, highlightthickness=2)

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
    # [Frame, ID Label, Jmeno Label, Prijmeni Label, 1.sem Entry, 2.sem Entry, 3.sem Entry, poradi_v_listu]
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

        virtualni_seznam_plnych_ramcu.append([frame, idLabel, jmLabel, prijLabel, firstSem, secondSem, thirdSem, poradiEntry])
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
                #skupinka[0].columnconfigure(6, weight=1, uniform=8)
                skupinka[0].config(bg="#000000")

                # umistovani do sloupecku
                skupinka[1].grid(row=0, column=0, stick="nsew")
                skupinka[2].grid(row=0, column=1, stick="nsew")
                skupinka[3].grid(row=0, column=2, stick="nsew")
                skupinka[4].grid(row=0, column=3, stick="nsew")
                skupinka[5].grid(row=0, column=4, stick="nsew")
                skupinka[6].grid(row=0, column=5, stick="nsew")
                #skupinka[7].grid(row=0, column=6, stick="nsew")
        poradnik += 1

    # update informaci
    refresh()

    # update statusbaru
    statusbar.config(text="Načítání studentů dokončeno.")

def nactiPredmetyZeSouboru():
    global statusbar
    global tempdir
    global index_prazdneho_ramce
    global virtualni_seznam_predmetu
    global poradnikMAX
    global ss
    
    # update status baru
    statusbar.config(text="Mažu předchozí seznam předmětů...")

    # mazani kvuli duplikaci předmětů         
    virtualni_seznam_predmetu = []

    # snaha o pamatovani si cesty
    currdir = os.getcwd()
    if tempdir is not ("" or currdir):
        currdir = tempdir
    
    # update status baru
    statusbar.config(text="Čekám na vybrání souboru...")

    # dialogove okno
    tempdir = fd.askopenfilename(parent=root, initialdir=currdir, title='Vyberte soubor se studenty')

    # nacitani predmetu
    statusbar.config(text="Načítání předmětů...")
    path = tempdir
    if ss.load_file_subjects(path) == False:    
        oznamovaciOkno("Chyba", "300x50", "Nepodařilo se načíst soubor s předměty.")
        statusbar.config(text="Načítání předmětů zrušeno důsledkem chyby při výběru souboru.")
        return

    # vytvareni framu pro kazdy predmet
    for key in ss.subject:
        virtualni_seznam_prazdnych_ramcu.append(Frame(root))

    # pridavani podrazenych poli do framu kazdeho predmetu
    # sklada se z listu: 
    # [Frame, CheckBox, ID Label]
    for key in ss.subject:
        pass
    pass

def pridejDen():
    global virtualni_seznam_dnu
    pass

def odeberDen():
    pass

def zmenaPredmetuStudenta():
    pass

def zmenaZaskrtnutychPredmetuVeDni():
    pass

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
menubar.add_command(label="PŘEPOČÍTEJ", command=refresh)
menubar.add_command(label="Vybrat soubor se studenty", command=nactiStudentyZeSouboru)
menubar.add_command(label="Vybrat soubor s předměty", command=nactiPredmetyZeSouboru)
menubar.add_command(label="Přidat nový den", command=pridejDen)
menubar.add_command(label="Odebrat poslední den", command=odeberDen)

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
nadpisStred = Label(root, text="Prostřední sloupec")
nadpisPravo = Label(root, text="Pravý sloupec") 
statusbar = Label(root, text="Nic nedělám.", bd=1, relief=SUNKEN, anchor="w")

# generovani te zasrane mrizky
root.columnconfigure(0, weight=1, minsize=650)      # seznam studentu
root.columnconfigure(1, weight=1, minsize=420)      # moznost zaskrtavat predmety jednotl. dnu
root.columnconfigure(2, weight=1, minsize=420)      # prehled predmetu s pocty studentu

root.rowconfigure(0, weight=2, minsize=25)          # nadpisy
root.rowconfigure(1, weight=10, minsize=680)        # dulezity obsah sloupcu (hodne mista)
root.rowconfigure(2, weight=1, minsize=12)          # status bar

# prirazeni do mrizky 
nadpisStred.grid(row=0, column=1)
nadpisPravo.grid(row=0, column=2)
statusbar.grid(row=3, column=0, columnspan=3, sticky="nsew")

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
#poradiLabel_nadp = Label(nadpisovyFrame, text="POŘADÍ", width=8)

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
#nadpisovyFrame.columnconfigure(6, weight=1, uniform=8)

# umistovani nadpisu do sloupecku
idLabel_nadp.grid(row=0, column=0, stick="nsew")
jmLabel_nadp.grid(row=0, column=1, stick="nsew")
prijLabel_nadp.grid(row=0, column=2, stick="nsew")
firstSemLabel_nadp.grid(row=0, column=3, stick="nsew")
secondSemLabel_nadp.grid(row=0, column=4, stick="nsew")
thirdSemLabel_nadp.grid(row=0, column=5, stick="nsew")
#poradiLabel_nadp.grid(row=0, column=6, stick="nsew")

#   --- END       ---
# aktualizace stavu na konci programu
# stisknuti krizku u okna prerusi mainloop
root.config(menu=menubar)
root.mainloop()