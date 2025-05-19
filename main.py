# Вызов библиотек
from tkinter import *
from tensorflow.keras import backend as K
from tensorflow import keras
K.set_image_data_format('channels_first')
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np
import re

import cv2
import easyocr

class App:
    def __init__(self):
        # Загрузка модели (при запуске)
        self.model = keras.models.load_model('CardsDetectorNew.keras')
        # Инициализация EasyOCR
        reader = easyocr.Reader(['ru'], gpu=False)
        self.root = Tk()  # создаем корневой объект - окно
        self.root.title("Приложение на распознание пропусков")  # устанавливаем заголовок окна
        self.root.geometry("420x500")  # устанавливаем размеры окна

        # создаем рабочую область
        self.frame = Frame(self.root)
        self.frame.grid()

        # Добавим изображение
        self.filepath = "NewPhoto.jpg"
        self.canvas = Canvas(self.root, height=400, width=400)
        self.changePhoto()

        self.label1 = Label(text="Выберете фотографию для определения")  # создаем текстовую метку
        self.label1.grid(row=1, column=1)  # размещаем метку в окне
        self.label2 = Label(text="Вы ещё не выбрали фото")  # создаем текстовую метку
        self.label2.grid(row=4, column=1)  # размещаем метку в окне
        self.label3 = Label(text="Здесь после выбора фото, будет написан номер")  # создаем текстовую метку
        self.label3.grid(row=5, column=1)  # размещаем метку в окне
        self.btn = Button(text="Выбрать новое фото", command=self.click_button).grid(row=2, column=1)
        self.root.mainloop()

    def predicting(self):
        image = keras.utils.load_img(self.filepath, target_size=(290, 290))
        input_arr = keras.utils.img_to_array(image)
        input_arr = np.array([input_arr])
        prediction = self.model.predict(input_arr)
        if prediction[0] > 0.50:
            return 1
        else:
            return 0

    def changePhoto(self):
        self.image = Image.open(self.filepath)
        self.image = self.image.resize([400, 400])
        self.photo = ImageTk.PhotoImage(self.image)
        self.image = self.canvas.create_image(20, 20, anchor='nw', image=self.photo)
        self.canvas.grid(row=3, column=1)

    def click_button(self):
        q=-1
        filepath = ""
        self.filepath = filedialog.askopenfilename(title="Выбор фотографии", initialdir="D://tkinter", defaultextension="img", initialfile="test.img")
        print(self.filepath)
        if self.filepath != "":
            with open(self.filepath, "r") as file:
                self.changePhoto()
                q = self.predicting()
        text = ""
        if q==-1:
            text = "Не удалось прочитать файл("
        if q==1:
            text = "На фото пропуск СПБГУ"
            self.checkNumber()
        if q==0:
            text = "На фото не пропуск СПБГУ"
        # изменяем текст
        self.label2["text"] = text

    def сheckNumber(self):

        image_path =  self.filepath
        image = cv2.imread(image_path)

        # Распознавание текста на изображении
        results = reader.readtext(image)

        # Поиск возможного номера карты
        card_number_pattern = re.compile(r'(\d[\s-]?){4,8}')

        text =""
        for bbox, text, conf in results:
            normalized = re.sub(r'\D', '', text)
            if 4 <= len(normalized) <= 8 and normalized.isdigit():
                text = f"Возможный номер карты: {normalized}"
                print(f"Возможный номер карты: {normalized}")
            else:
                text = "Не удалось распознать номер карты"
        # изменяем текст
        self.label3["text"] = text





app= App()


