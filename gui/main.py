from tkinter import *
from sortsubj import *


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

#   --- DEFAULTNI HODNOTY   ---
# nelze menit primo ve funkci kvuli pamatovani si poradi pro pripad nacitani vice souboru za sebou
tempdir = ""
index_prazdneho_ramce = 0             
virtualni_seznam_prazdnych_ramcu = [] 
virtualni_seznam_plnych_ramcu = []

#   --- FUNKCE      ---
def nactiStudentyZeSouboru():
    
    # snaha o pamatovani si cesty
    currdir = os.getcwd()
    if tempdir is not ("" or curdir):
        currdir = tempdir
    
    # dialogove okno
    tempdir = tkFileDialog.askdirectory(parent=root, initialdir=currdir, title='Vyberte soubor se studenty')

    # nacitani studentu do slovniku
    path = tempdir
    ss = SubSort()
    ss.load_file_subjects(path)
    ss.load_file_student(path)

    # pridavani studentu do virtualniho seznamu:
    # student: 

    # vytvareni framu pro kazdeho studenta
    for key in ss.students:
        virtualni_seznam_prazdnych_ramcu.append(Frame(scrollable_frame))

    # pridavani podrazenych poli do framu kazdeho studenta
    # sklada se z listu: 
    # [Frame, ID Label, Jmeno Label, Prijmeni Label, 1.sem Entry, 2.sem Entry, 3.sem Entry, 4.sem Entry, poradi_v_listu]
    for key in ss.students:
        defPoradi = len(virtualni_seznam_plnych_ramcu)
        tempStudent = ss.students[key]

        frame = virtualni_seznam_prazdnych_ramcu[index_prazdneho_ramce]
        idLabel = Label(frame, text=tempStudent.id)
        jmLabel = Label(frame, text=tempStudent.first_name)
        prijLabel = Label(frame, text=tempStudent.last_name)
        firstSem = Entry(frame); firstSem.insert(0, tempStudent.subjects[0])
        secondSem = Entry(frame); secondSem.insert(0, tempStudent.subjects[0])
        thirdSem = Entry(frame); thirdSem.insert(0, tempStudent.subjects[0])
        fourthSem = Entry(frame); fourthSem.insert(0, tempStudent.subjects[0])
        poradiLabel = Label(frame, text=defPoradi)

        virtualni_seznam_plnych_ramcu.append([frame, idLabel, jmLabel, prijLabel, firstSem, secondSem, thirdSem, fourthSem, poradiLabel])
        index_prazdneho_ramce += 1

    # zobrazovani obsahu virtualniho seznamu v okne
    for ramec in virtualni_seznam_prazdnych_ramcu:
        ramec.pack() 

    # for i in range(50):
    #    Label(scrollable_frame, text="Sample scrolling label").pack()

#   --- MAIN        ---
root = Tk()
root.title("Pomocnik pro rozzarovani seminaru 1.0.0")
root.geometry("1440x900")

#   --- MENU BAR    ---
menubar = Menu(root)
menubar.add_command(label="Pridat soubor se studenty", command=nactiStudentyZeSouboru)

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
nadpisLevo = Label(root, text="Levý sloupec")
nadpisStred = Label(root, text="Prostřední sloupec")
nadpisPravo = Label(root, text="Pravý sloupec") 

# generovani te zasrane mrizky
root.columnconfigure(0, weight=1, minsize=420)      # seznam studentu
root.columnconfigure(1, weight=1, minsize=420)      # moznost zaskrtavat predmety jednotl. dnu
root.columnconfigure(2, weight=1, minsize=420)      # prehled predmetu s pocty studentu

root.rowconfigure(0, weight=1, minsize=50)          # nadpisy
root.rowconfigure(1, weight=3, minsize=680)         # dulezity obsah sloupcu (hodne mista)


# prirazeni do mrizky 
nadpisLevo.grid(row=0, column=0) 
nadpisStred.grid(row=0, column=1)
nadpisPravo.grid(row=0, column=2)

container.grid(row=1, column=0, sticky='nsew')
canvas.pack(side="left", fill=BOTH, expand=True)
scrollbar.pack(side="right", fill=Y)


#   --- END       ---
# aktualizace stavu na konci programu
# stisknuti krizku u okna prerusi mainloop
root.mainloop()