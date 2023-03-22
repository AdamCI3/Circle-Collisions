import math
from tkinter.scrolledtext import ScrolledText
import tkinter.font
from tkinter import *
import tkinter as tk
from math import sqrt

root = Tk()
#root.geometry("450x600")
root.title("Kolizje kół")
root.config(background='#252526')
root.resizable(False, False)
root.iconphoto(False, tk.PhotoImage(file='test.png'))

ROOT_FONTTITLE = tkinter.font.Font(family='Arial', size=12, weight="bold")
ROOT_FONT = tkinter.font.Font(family='Arial', size=10, weight="bold")

# Struktura opisująca jakieś koło
class Circle:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "Circle()"

    def __str__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)


# Struktura pary kół opisująca jakiś rezultat
class CircleCollision:
    def __init__(self, c1, c2):
        self.c1 = c1
        self.c2 = c2

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self.c1) + " kolizja z " + str(self.c2)


inputData = []  # ( ( item index ) , value )
circles = []
errors = []
rowsDrawn = 0
Submit = {}
collisions = []

warning = []

# Funkcja odpowiedzialna za sprawdzenie czy tekst jest poprawną zmienną typu float
def ValidateFloat(text):
    if len(text) >= 23:
        return (False, -1)
    try:
        x = float(text)

        if math.isinf(x):
            return (False, -1)
        if math.isnan(x):
            return (False, -1)

        return (True, x)
    except ValueError:
        return (False, -1)

# Czy informacja o id item jest w zbiorze danych wejściowych
def isInData(item):
    matches = [ind for ind, x in enumerate(inputData) if x[0] == item]
    return -1 if len(matches) == 0 else matches[0]

# Czy informacja o id item jest w tablicy trzymającej informacje o błędnie wpisanych danych
def isInErrors(item):
    matches = [ind for ind, x in enumerate(errors) if x == item]
    return -1 if len(matches) == 0 else matches[0]

# Funkcja odpowiedzialna za dorysowanie dwóch pól do wpisywania wiejścia
def AddEntries():
    global rowsDrawn  # Szukaj poza zakresem lokalnym

    id = rowsDrawn
    rowsDrawn += 1

    label = Frame()
    lbl = Label(label, text=f"Koło {id}", font=ROOT_FONT, fg="#007acc")
    lbl.config(background="#2d2d30")
    lbl.pack(side=LEFT)

    box.window_create(END, window=label)
    box.insert(END, '\n')

    entries = Frame()

    sv = StringVar()
    sv.trace("w", lambda name, index, mode, params=(sv, id): callback(params[0], (params[1], 0)))

    entry1 = Entry(entries, textvariable=sv, fg="#007acc")
    entry1.config(background="#353537")
    entry1.pack(side=LEFT)

    sv2 = StringVar()
    sv2.trace("w", lambda name, index, mode, params=(sv2, id): callback(params[0], (params[1], 1)))

    entry2 = Entry(entries, textvariable=sv2, fg="#007acc")
    entry2.config(background="#353537")
    entry2.pack(side=LEFT)

    box.window_create(END, window=entries)
    box.insert(END, '\n')

# Event wykonywany przy każdym zmienieniu jakiegoś pola z danymi wejściowymi
def callback(sv, item):
    global rowsDrawn  # Szukaj poza zakresem lokalnym
    result = ValidateFloat(sv.get())
    index = isInData(item)
    errorState = isInErrors(item)

    if sv.get() == "":
        if errorState > -1:
            errors.pop(errorState)

        if index > -1:
            inputData.pop(index)

        if len(errors) == 0:
            Submit["state"] = "normal"
            warning["text"] = ""
        else:
            Submit["state"] = "disabled"
            warnMessage = "Są blędy w kolach: "
            for i in range(min(len(errors), 4)):
                warnMessage += str(errors[i][0]) + ("x" if errors[i][1] == 0 else "y") + ", "
            if len(errors) > 4:
                warnMessage = warnMessage + "..."
            else:
                warnMessage = warnMessage[:-2]
            warning["text"] = warnMessage
        return

    if result[0]:
        if errorState > -1:
            errors.pop(errorState)
        if index > -1:
            inputData[index] = (item, result[1])
        else:
            inputData.append((item, result[1]))
    else:
        if errorState == -1:
            errors.append(item)

        if index > -1:
            inputData.pop(index)

    if rowsDrawn * 2 == len(inputData):
        AddEntries()

    if len(errors) == 0:
        Submit["state"] = "normal"
        warning["text"] = ""
    else:
        Submit["state"] = "disabled"
        warnMessage = "Są blędy w kolach: "
        for i in range(min(len(errors), 4)):
            warnMessage += str(errors[i][0]) + ("x" if errors[i][1] == 0 else "y") + ", "
        if len(errors) > 4:
            warnMessage = warnMessage + "..."
        else:
            warnMessage = warnMessage[:-2]
        warning["text"] = warnMessage


# Funkcja obliczająca odległość euklidesową między dwoma punktami (x1, y1) i (x2, y2)
def distance(x1, y1, x2, y2):
    return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

# Funkcja znajdująca wszystkie kolizje między kołami
def find_collisions(circles):
    circles.sort(key=lambda c: c.x)
    collisions = []
    for i in range(0, len(circles)):
        for j in range(i + 1, len(circles)):
            c1 = circles[i]
            c2 = circles[j]
            d = distance(c1.x, c1.y, c2.x, c2.y)
            if d < 2:
                collisions.append(CircleCollision(c1, c2))
    return collisions

# Event odpowiedzialny za obliczenie kolizji i wyświetlenie danych
def onClick():
    global root
    temp = []
    isChanged = []
    for i in range(rowsDrawn - 1):
        temp.append([0, 0])
        isChanged.append(False)

    for x in inputData:
        id = x[0]
        value = x[1]
        temp[id[0]][id[1]] = value
        isChanged[id[0]] = True

    for i in range(len(temp)):
        x = temp[i]
        data = Circle(x[0], x[1])
        if data not in circles:
            if isChanged[i]:
                circles.append(data)

    # Obliczanie wyniku
    collisions = find_collisions(circles)

    root.destroy()

if __name__ == "__main__":
    # Kod opowiedzialny za rysowanie UI z wejściem danych
    label = Label(root, text='Witaj! Wprowadź koordynaty kól do sprawdzenia:', fg='#007acc', font=ROOT_FONTTITLE)
    label.config(background='#252526')
    label.pack()

    label = Label(root, text='Możesz zostawić puste pola tam gdzie nie chcesz wpisywać danych', fg='#007acc', font=ROOT_FONT)
    label.config(background='#252526')
    label.pack()

    label = Label(root, text='Gdy wszystko będzie gotowe naciśnij przycisk Submit', fg='#007acc', font=ROOT_FONT)
    label.config(background='#252526')
    label.pack()

    box = ScrolledText(root, width=40)
    box.config(state=DISABLED, background='#2d2d30')
    box.pack()

    warning = Label(root, text='', fg='#f00')
    warning.config(background='#252526')
    warning.pack()

    AddEntries()

    Submit = Button(root, text="Submit", command=onClick, fg="#ffffff")
    Submit.config(background='#252526')
    Submit.pack()

    root.mainloop()

    # Kod opowiedzialny za rysowanie UI z wypisywaniem rezultatów
    COLLISIONS = find_collisions(circles)
    # Okienko do wyświetlania wyników
    DISPLAY_WINDOW = tk.Tk()
    DISPLAY_WINDOW.geometry("450x600")
    DISPLAY_WINDOW.title("Znalezione kolizje kół")
    DISPLAY_WINDOW.config(background='#252526')
    DISPLAY_WINDOW.resizable(True, False)
    DISPLAY_WINDOW.iconphoto(False, tk.PhotoImage(file='test.png'))
    # Czcionka do wyswietlania
    DISPLAY_FONTTITLE = tkinter.font.Font(family='Arial', size=30, weight="bold")
    DISPLAY_FONT = tkinter.font.Font(family='Arial', size=20, weight="bold")

    LABEL = Label(DISPLAY_WINDOW)
    LABEL.config(background='#252526')
    LABEL.pack()
    # przycisk wyjscia
    EXIT = Button(DISPLAY_WINDOW, text="Wyjscie", command=DISPLAY_WINDOW.destroy, fg='white')
    EXIT.config(background='#252526')
    EXIT.pack()

    # Label po przycisku
    LABEL2 = Label(DISPLAY_WINDOW)
    LABEL2.config(background='#252526', text=f"Liczba kolizji: {len(COLLISIONS)}", fg='#007acc', font=DISPLAY_FONTTITLE)
    LABEL2.pack()
    LABEL3 = Label(DISPLAY_WINDOW)
    LABEL3.config(background='#252526')
    LABEL3.pack()
    LABEL4 = Label(DISPLAY_WINDOW)
    LABEL4.config(background='#252526')
    LABEL4.pack()

    # Zrobienie okienka ze scrollem
    SCROLL = ScrolledText(DISPLAY_WINDOW, width=50)
    SCROLL.pack(fill=BOTH, side=LEFT, expand=True)
    SCROLL.config(background='#2d2d30')

    # Tablica kolizji


    # Wyświetlanie w pętli
    for i in range(len(COLLISIONS)):
        # Tworze frame by uumeiscic w nim wyniki
        LABEL1 = Frame()
        # Tworze przerwę by wyniki nie były od razu przy lewej sciance
        SCROLL.window_create(END, window=LABEL1)
        SCROLL.insert(END, '\t')

        LBL = Label(LABEL1, text=f"{i + 1}. {str(COLLISIONS[i])}", font=DISPLAY_FONT, fg='#007acc')
        LBL.config(background='#2d2d30')
        LBL.grid()
        # Przechodze do nastepnej linii
        SCROLL.window_create(END, window=LABEL1)
        SCROLL.insert(END, '\n')

    SCROLL.config(state=DISABLED)
    DISPLAY_WINDOW.mainloop()