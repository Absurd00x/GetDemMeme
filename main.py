import tkinter as tk
import requests as rq
import re
from PIL import Image
from io import BytesIO
from random import choice

HEIGHT = 500
WIDTH = 600
pattern = re.compile(r'http:\/\/.+\.jpg')


def get_meme(entry):
    url = 'http://www.1001mem.ru/search'
    params = {'q': entry}
    response = rq.get(url, params=params)
    status = response.status_code
    if status != 200:
        label['image'] = dummy_image
    else:
        text = response.text
        found = re.findall(pattern, text)
        found.pop()  # Удаляем тупую картинку с рекламой
        # будет очень смешно, если рекламы не будет на сайте ахахахха
        memes = []
        for link in found:
            # TODO: Тут может очень смешно изображения не быть
            # И мне приедет валидный html ответ "я ниче ни нашол"
            byte_image = rq.get(link).content
            meme_image = Image.open(BytesIO(byte_image))
            memes.append(meme_image)
        chosen_meme = choice(memes)
        # TODO: Мб тут придется каждый раз новое название брать для файла с мемом
        # Или не придёцца
        chosen_meme.save('meme.png')
        meme_png = tk.PhotoImage(file='meme.png')
        label['image'] = meme_png


root = tk.Tk()

dummy_image = tk.PhotoImage(file='dummy.png')

canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

background_image = tk.PhotoImage(file='landscape.png')
background_label = tk.Label(root, image=background_image)
background_label.place(relwidth=1, relheight=1)

frame = tk.Frame(root, bg='#80c1ff', bd=5)
frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor='n')

entry = tk.Entry(frame, font=40)
entry.place(relwidth=0.65, relheight=1)

button = tk.Button(frame, text='Найти мем!', font=40,
                   command=lambda: get_meme(entry.get()))
button.place(relx=0.7, relwidth=0.3, relheight=1)

lower_frame = tk.Frame(root, bg='#80c1ff', bd=10)
lower_frame.place(relx=0.5, rely=0.25, relwidth=0.75, relheight=0.6, anchor='n')

label = tk.Label(lower_frame)
label.place(relwidth=1, relheight=1)

root.mainloop()
