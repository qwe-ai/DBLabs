from pymongo import MongoClient
from tkinter import ttk
from tkinter import Tk, Label, Entry, Button, Text
import json

# Подключение к базе данных
client = MongoClient("mongodb://192.168.112.103/")
db = client["22305"]
collection = db["sokolova-games"]

class Frame:
    def __init__(self, root):
        self.root = root
        self.root.title("Поиск")
        for i in range(2): root.grid_columnconfigure(index=i, weight=1)
        for j in range(5): root.grid_columnconfigure(index=j, weight=1)

        self.key_label = Label(root, text="Ключ:")
        self.key_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        self.key_entry = Entry(root)
        self.key_entry.grid(row=0, column=1, padx=10, pady=5, sticky="we")

        self.comp_label = Label(root, text="Сравнение:")
        self.comp_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)

        self.comp_entry = ttk.Combobox(values=["<", "<=", ">", ">=", "="])
        self.comp_entry.grid(row=1, column=1, padx=10, pady=5, sticky="we")
        

        self.value_label = Label(root, text="Значение:")
        self.value_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)

        self.value_entry = Entry(root)
        self.value_entry.grid(row=2, column=1, padx=10, pady=5, sticky="we")
        

        self.result_button = Button(root, text="Показать результаты", command=self.get_results)
        self.result_button.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="we")

        self.document_textbox = Text(root)
        self.document_textbox.grid(row=5, column=0, columnspan=2, padx=10, pady=5, sticky="we")

        self.current_doc_data = dict()

    def show_documents(self, query):
        self.document_textbox.delete(1.0, "end") # Очищаем Text перед выводом новых данных

        for document in collection.find(query):
            self.document_textbox.insert("end", json.dumps({x: document[x] for x in document if x not in "_id"}, indent=4, ensure_ascii=False) + '\n_______________________________________\n\n')

    def get_results(self):
        key = self.key_entry.get()
        comp_symb = self.comp_entry.get()
        value = self.value_entry.get()

        if key == "" or comp_symb == "" or value == "":
            self.document_textbox.insert("end", "Не все поля заполнены!")
            return

        # формируем запрос
        if comp_symb == '>':
            query = {key: {'$gt': value}}
        elif comp_symb == '>=':
            query = {key: {'$gte': value}}
        elif comp_symb == '=':
            query = {key: {'$eq': value}}
        elif comp_symb == '<=':
            query = {key: {'$lte': value}}
        elif comp_symb == '<':
            query = {key: {'$lt': value}}
        else:
            # Обработка некорректного сравнения
            print("Некорректное сравнение")

        self.show_documents(query)
        print(str(query))

root = Tk()
root.geometry("400x400")
frame = Frame(root)

root.mainloop()
