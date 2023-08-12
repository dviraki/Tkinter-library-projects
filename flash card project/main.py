from tkinter import *
import pandas
import random

# ---------------------------- CONSTANTS ------------------------------- #
BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

#creates a csv file of word to learn
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")

# ---------------------------- FUNCTIONS ------------------------------- #

# show the word in French and wait 3 second for the answer
def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="French",fill="black")
    canvas.itemconfig(card_text,text=current_card["French"],font=("Ariel", 60, "bold"),fill="black")
    canvas.itemconfig(card_background, image=card_front_img)
    flip_timer = window.after(3000, flip_card)

# show the answer in english waiting for user respond
def flip_card():
    canvas.itemconfig(card_title, text="english",fill="white")
    canvas.itemconfig(card_text, text=current_card["English"], font=("Ariel", 60, "bold"),fill="white")
    canvas.itemconfig(card_background, image=card_back_img)

# removing words from to_learn the copy of french_words.csv
def is_known():
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, flip_card)

#Canvas
canvas = Canvas(width=800, height=526,highlightthickness=0)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400,263,image= card_front_img)
canvas.config(bg=BACKGROUND_COLOR)
canvas.grid(row=0, column=0, columnspan=2)
card_title = canvas.create_text(400,150,text="Title", font=("Ariel", 40, "italic"))
card_text = canvas.create_text(400,263,text="word", font=("Ariel", 60, "bold"))

#Buttons
cross_image = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=cross_image, highlightthickness=0, command=next_card)
unknown_button.grid(row=1,column=0)
check_image = PhotoImage(file="images/right.png")
known_button = Button(image=check_image, highlightthickness=0, command=is_known)
known_button.grid(row=1,column=1)

next_card()

window.mainloop()