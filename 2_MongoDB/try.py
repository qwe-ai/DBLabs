from pymongo import MongoClient
from tkinter import Tk, Label, Entry, Button, Text
import json

# Подключение к базе данных
client = MongoClient("mongodb://192.168.112.103/")
db = client["22305"]
collection = db["sokolova-teams"]

class Frame:
    def __init__(self, root):
        self.root = root
        self.root.title("Футбол")
        for i in range(2): root.grid_columnconfigure(index=i, weight=1)
        for j in range(5): root.grid_columnconfigure(index=j, weight=1)

        self.key_label = Label(root, text="Ключ:")
        self.key_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        self.key_entry = Entry(root)
        self.key_entry.grid(row=0, column=1, padx=10, pady=5, sticky="we")

        self.value_label = Label(root, text="Значение:")
        self.value_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)

        self.value_entry = Entry(root)
        self.value_entry.grid(row=1, column=1, padx=10, pady=5, sticky="we")

        self.add_button = Button(root, text="Добавить ключ-значение", command=self.add_key_value)
        self.add_button.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="we")

        self.save_button = Button(root, text="Сохранить документ", command=lambda: (self.save_document(), self.show_documents()))
        self.save_button.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="we")

        self.show_button = Button(root, text="Показать документы", command=self.show_documents)
        self.show_button.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="we")

        self.document_textbox = Text(root)
        self.document_textbox.grid(row=5, column=0, columnspan=2, padx=10, pady=5, sticky="we")

        self.current_doc_data = dict()

    def store_data(self, data, keys, value):
        if len(keys) == 1:
            data[keys[0]] = value
        else:
            key = keys[0]
            if key not in data:
                data[key] = {}
            self.store_data(data[key], keys[1:], value)

    def add_key_value(self):
        key = self.key_entry.get()
        value = self.value_entry.get()

        # разделяем вложенные ключи по точке
        keys = key.split(".")

        self.store_data(self.current_doc_data, keys, value)

        print(self.current_doc_data)

        self.key_entry.delete(0, "end")
        self.value_entry.delete(0, "end")

    def save_document(self):
        collection.insert_one(self.current_doc_data)
        self.current_doc_data = {}

    def show_documents(self):
        self.document_textbox.delete(1.0, "end") # Очищаем Text перед выводом новых данных

        for document in collection.find():
            self.document_textbox.insert("end", json.dumps({x: document[x] for x in document if x not in "_id"}, indent=4, ensure_ascii=False) + '\n_______________________________________\n\n')

root = Tk()
root.geometry("400x400")
frame = Frame(root)

root.mainloop()
