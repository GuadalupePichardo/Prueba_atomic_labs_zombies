import tkinter
from tkinter import *
import random
import time as t

window = tkinter.Tk()
window.geometry("850x690")

frame1=Frame(window)
frame1.pack(side=LEFT)

frame2=Frame(window)
frame2.pack(side=RIGHT)

persons_cords = [(9,1), (3,3), (6,3), (11,3), (15,3), (4,5), 
(15,6), (2,7), (7,7),(3,8),(17,8), (11,9), (13,12), (3,13), 
(17,13), (6,14), (10,15),(3,17), (7,17), (13,17)]

windows_cords = [(3, 0), (4,0), (5,0), (6,0), (13,0), (14,0),(15,0),(16,0)]

zombies_cords = []

cells = []
persons = []
zombies = []

aux_exit =[]
persons_salv = 0

def init_view():
    init_zombies()
    init_cells()
    #windows_cords.clear()
    zombies_cords.clear()
    
    button_start = tkinter.Button(window, text="Iniciar", command=start_chase)

    toolbar=Frame(frame2,bg='grey')
    toolbar.pack(side=TOP,fill=X)
    button_start.pack()
    window.mainloop()

def init_cells():
    n_rows = 20
    n_cols = 20
    
    for row in range (n_rows):
        for col in range (n_cols):
            cell = define_colors(row, col)          
            label = tkinter.Label(frame1,bg=cell.get("color"), text=cell.get("name"),borderwidth=1, relief="solid", width=5, height=2)
            label.grid(column= col, row= row)

def define_colors(row, col):
    cell = {
        "color" : "white",
        "x" : 0,
        "y" : 0,
        "name":"",
        "type": "",
        "infected": False,
        "infected_await": 0
    }

    #Definir paredes
    if row == 0 or row==19 or col ==0 or col == 19: cell["color"] ="black"; cell["type"] = "walk"
    elif col >= 2 and col<=7 and row ==4:  cell["color"] ="black"; cell["type"] = "walk"
    elif col >= 10 and col<=16 and row ==4: cell["color"] ="black"; cell["type"] = "walk"
    elif row >= 5 and row<=7 and col ==13: cell["color"] ="black"; cell["type"] = "walk"
    elif col >= 1 and col<=8 and row ==10: cell["color"] ="black"; cell["type"] = "walk"
    elif col >= 12 and col<=18 and row ==10: cell["color"] ="black"; cell["type"] = "walk"
    elif col >= 2 and col<=7 and row ==12: cell["color"] ="black"; cell["type"] = "walk"
    elif col >= 2 and col<=7 and row ==16: cell["color"] ="black"; cell["type"] = "walk"
    elif row >= 12 and row<=15 and col ==12: cell["color"] ="black"; cell["type"] = "walk"
    elif row >= 12 and row<=15 and col ==16:cell["color"] ="black"; cell["type"] = "walk"
    else: cell["color"] ="white"

    #Definir ventanas 
    if(col, row) in windows_cords:
        cell["color"] ="white"
        cell["type"] = "window"
    

    cell["x"] = col
    cell["y"] = row

    if col == 19 and row >=15 and row <19:
        cell["color"] ="red"
        cell["type"] = "exit"
        aux_exit.append((col,row))

    #Definir zombies
    if (col, row) in zombies_cords:
        cell["color"] ="green"
        cell["type"] = "zombie"
        zombies.append(cell)

    #Definir personas
    if (col, row) in persons_cords:
        cell["name"]=(persons_cords.index((col, row))+1)
        cell["color"] = "blue"
        cell["type"] = "person"
        persons.append(cell)

    cells.append(cell)
    return cell
iteracion = 1

def start_chase():
    global iteracion
    windows_cords.extend( [(3, 0), (4,0), (5,0), (6,0), (13,0), (14,0),(15,0),(16,0)])
    
   # while len(persons_cords) > 0:
    for i in range(2):
        persons_cords.clear()
        move_persons()
        for j in range(2):
            zombies_cords.clear()
            move_zombies()
        
        zombies.clear()
        persons.clear()
        
        init_cells()

    review_persons()
    iteracion +=1
    with open('zombies.txt', 'a') as f:
        f.write(f"{iteracion} | {len(zombies_cords)} | {len(persons_cords)} | {persons_salv} \n")
    print(f"{iteracion} | {len(zombies_cords)} | {len(persons_cords)} | {persons_salv}")
        

def review_persons():
    for person in persons:
        p_x =person.get("x")
        p_y = person.get("y")
        
        if (p_x+1, p_y) in zombies_cords or (p_x, p_y+2) in zombies_cords or (p_x-1, p_y) in zombies_cords or (p_x, p_y-1) in zombies_cords:
            person["infected"] =True
            index_infected = next((p_x, p_y) for (p_x, p_y) in persons_cords)
            persons_cords.remove(index_infected)
            zombies_cords.append((p_x, p_y))
            zombies.append(
                            {
                    "color" : "green",
                    "x" : p_x,
                    "y" : p_y,
                    "name":"",
                    "type": "zombie",
                    "infected": False
                }
            )
            persons.remove(person)
            print(f"Humano infectado en la casilla {p_x}, {p_y}")
        

def move_persons():
    global persons_salv
    for person in persons:
        x = person.get('x')
        y = person.get('y')
        is_next_walk = where_is_walk(x, y)

        if y <= 9:
            if is_next_walk != "down":
                person["y"] = advance(y) 
            elif x<=8:
                person["x"] = advance(x)
            elif x>8:
                person["x"] = back_off(x)
        elif y ==10  and is_next_walk != "right":
            person["x"] = advance(x)
        elif y< 16:
            if x >= 9 and x <=11 and is_next_walk != "down":
                person["y"] = advance(y)
            elif  x<9:
                person["x"] = advance(x)
            elif x>9:
                person["y"] = advance(y)
        elif y >= 15 and is_next_walk != "right":
            person["x"] = advance(x)

        if person.get("infected") == True:
            person["infected_await"] +=1
        
        if (person.get("x"), person.get("y")) in aux_exit:
            rescued_person=persons.index(person)
            persons.pop(rescued_person)
            persons_salv += 1
            print(f"Humano salvado en la casilla {person.get('x')}, {person.get('y')}")
        elif  (person.get("x"), person.get("y")) in persons_cords:
            if is_next_walk != "down":
                persons_cords.append((person.get("x"), person.get("y")+1))
            else: persons_cords.append((person.get("x"), person.get("y")-1))
        else : persons_cords.append((person.get("x"), person.get("y")))
   
def advance(coordinate):
    return coordinate+1

def back_off(coordinate):
    return coordinate-1

def where_is_walk(x, y):
    position = ""

    for cell in cells:
        if cell.get("y") == y+1 and cell.get("x") == x and cell["type"] == "walk": #Pared debajo de la celda
            position = "down"
        if cell.get("y") == y-1 and cell.get("x") == x and cell["type"] == "walk": #Pared arriba de la celda
            position = "up"
        if cell.get("y") == y and cell.get("x") == x+1 and cell["type"] == "walk": #Pared a la der de la celda
            position = "right"
        if cell.get("y") == y and cell.get("x") == x-1 and cell["type"] == "walk": #Pared a la izq de la celda
            position = "left"
    return position

def init_zombies():
    for i in range(2):
        zombie = random.choice(windows_cords)
        index_zombie = windows_cords.index(zombie)
        windows_cords.pop(index_zombie)
        zombies_cords.append(zombie)

def move_zombies():
    for zombie in zombies:
        x = zombie.get('x')
        y = zombie.get('y')
        move = random.randint(1,8)
        if move == 1 and where_is_walk(x-1,y) != "up" and y-1 >0 and (x-1,y-1) not in zombies_cords:
            zombie["x"] = back_off(x)
            zombie["y"] = back_off(y)
        else: 
            move = random.randint(2,8)
            if move == 2 and where_is_walk(x,y) != "up" and y-1 >0 and (x,y-1) not in zombies_cords: 
                zombie["y"] = back_off(y)
            else:
                move = random.randint(3,8)
                if move == 3 and where_is_walk(x+1,y) != "up" and y-1 >0 and (x+1,y-1) not in zombies_cords:
                    zombie["x"] = advance(x)
                    zombie["y"] = back_off(y)
                else: 
                    move = random.randint(4,8)
                    if move == 4 and where_is_walk(x,y) != "left"  and (x-1,y) not in zombies_cords: 
                        zombie["x"] = back_off(x)
                    else:
                        move = random.randint(5,8)
                        if move == 5 and where_is_walk(x,y) != "right" and (x+1,y) not in zombies_cords: 
                            zombie["x"] = advance(x)
                        else:
                            move = random.randint(6,8)
                            if move == 6 and where_is_walk(x-1,y) != "down" and (x-1,y+1) not in zombies_cords:
                                zombie["x"] = back_off(x)
                                zombie["y"] = advance(y)
                            else:
                                move = random.randint(7,8)
                                if move == 7 and where_is_walk(x,y) != "down" and (x,y+1) not in zombies_cords:
                                    zombie["y"] = advance(y)
                                elif where_is_walk(x+1,y) != "down" and where_is_walk(x,y+1) != "right":
                                    zombie["x"] = advance(x)
                                    zombie["y"] = advance(y)
        zombies_cords.append((zombie["x"], zombie["y"]))

if __name__ == '__main__':
    init_view()