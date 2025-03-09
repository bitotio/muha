from tkinter import *
from random import *
from winsound import *

def play_sound_ok():
    files = []
    for i in range(1,7):
        files.append(f'hit{i}.wav')
    file = choice(files)
    PlaySound(file, SND_ASYNC | SND_FILENAME)

def play_sound_fail():
    files = []
    for i in range(1,8):
        files.append(f'miss{i}.wav')
        file = choice(files)
        PlaySound(file, SND_ASYNC | SND_FILENAME)

def collision_detection(x, y):
    position = canvas.coords(npc_id)
    left = position [0]
    top = position[1]
    right = position [0] + npc_width
    bottom = position [1] + npc_height

    return left <= x <= right and top <= y <= bottom

def hit():
    global score
    score += 1
    update_points()
    play_sound_ok()
    spawn()

def missclick():
    global score
    score -= 1
    if score < 0:
        game_over()
    else:
        update_points()
        play_sound_fail()

def spawn ():
    for i in range(100):
        x = randint(10, 600)
        y = randint(10, 400)
        if abs(mouse_x - x) > 200 or abs (mouse_y - y) > 200:
            break
    canvas.moveto(npc_id, x, y)
    if randint(1, 50) == 1:
        show_screamer()

def game_update():
    spawn()
    canvas.after(1000, game_update)


def update_points():
    canvas.itemconfig(text_id, text=f'очки: {score}')

def game_over():
    global gameover
    canvas.itemconfig(text_id, text='потрачено')
    canvas.create_text(game_width//2,game_height//2, fill="red", font="Times 50 bold", text='GAME OVER', anchor=CENTER)

    gameover = True
    PlaySound('gameover.wav', SND_ASYNC | SND_FILENAME)

def show_screamer():
    global gameover
    gameover = True
    canvas.itemconfig(screamer_id, state='normal')
    PlaySound('gameover.wav', SND_ASYNC | SND_FILENAME)

def mouse_click(e):
    print(collision_detection(e.x, e.y))
    if gameover:
        return
    if collision_detection(e.x, e.y):
        print('попал')
        hit()
    else:
        missclick()

def mouse_motion(event):
    global mouse_x, mouse_y
    mouse_x, mouse_y = event.x, event.y

game_width = 720
game_height = 720

npc_width = 120
npc_height = 95

score = 10
mouse_x = mouse_y = 0
gameover = False
window = Tk()
window.title('проучи тролля')
window.resizable(width=False, height=False)
canvas = Canvas(window, width=game_width, height=game_height)

phone_image = PhotoImage(file="fon.png")
canvas.create_image(0, 0, image=phone_image, anchor=NW)

npc_image = PhotoImage(file="muha.png")
npc_id = canvas.create_image(0, 0, image=npc_image, anchor=NW)
text_id = canvas.create_text(game_width - 1, 10, fill="white", font="Times 20 bold", text=f'очки: {score}', anchor=NE)

screamer_image = PhotoImage(file="screamer.png")
screamer_id = canvas.create_image(0, 0, image=screamer_image, anchor=NW)
canvas.itemconfig(screamer_id, state='hidden')



canvas.bind("<Button>", mouse_click)
canvas.bind("<Motion>", mouse_motion)
canvas.pack()

game_update()
window.mainloop()



