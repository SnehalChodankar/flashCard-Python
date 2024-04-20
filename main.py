import random

BACKGROUND_COLOR = "#B1DDC6"

from tkinter import *
import pandas

try:
    df_data = pandas.read_csv("./data/words_to_learn.csv")
except FileNotFoundError:
    df_data = pandas.read_csv("./data/french_words.csv")

# df_dict = {val.French: val.English for (key, val) in df_data.iterrows()}
df_dict = df_data.to_dict(orient="records")

data = {}


# print(df_dict)


def next_card():
    global data, flipTimer

    window.after_cancel(flipTimer)

    data = random.choice(df_dict)
    print(data["French"])
    print(data["English"])

    canvas.itemconfig(title_text, text="French", fill="black")
    canvas.itemconfig(word_text, text=data["French"], fill="black")
    canvas.itemconfig(img, image=img_front)

    flipTimer = window.after(3000, func=flip_card)

def flip_card():
    canvas.itemconfig(title_text, text="English", fill="white")
    canvas.itemconfig(word_text, text=data["English"], fill="white")
    canvas.itemconfig(img, image=img_back)


def word_learnt():
    df_dict.remove(data)

    new_data = pandas.DataFrame(df_dict)
    new_data.to_csv("./data/words_to_learn.csv", index=False)

    next_card()

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Flash Card")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flipTimer = window.after(3000, func=flip_card)

# bg image
canvas = Canvas(width=800, height=526)
img_front = PhotoImage(file="./images/card_front.png")
img_back = PhotoImage(file="./images/card_back.png")

img = canvas.create_image(400, 263, image=img_front)

title_text = canvas.create_text(400, 150, text="title", font=("Arial", 40, "italic"))
word_text = canvas.create_text(400, 263, text="word", font=("Arial", 60, "bold"))

canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(column=1, row=1, columnspan=2)

cross = PhotoImage(file="./images/wrong.png")
button_wrong = Button(image=cross, highlightthickness=0, command=next_card)
button_wrong.grid(column=1, row=2)

my_image = PhotoImage(file="./images/right.png")
button = Button(image=my_image, highlightthickness=0, command=word_learnt)
button.grid(column=2, row=2)

next_card()

window.mainloop()
