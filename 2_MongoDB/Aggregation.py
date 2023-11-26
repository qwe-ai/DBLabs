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
        self.root.title("Агрегация")

        for i in range(2): root.grid_columnconfigure(index=i, weight=1)
        for j in range(5): root.grid_columnconfigure(index=j, weight=1)

        self.what_label = Label(root, text="Что:")
        self.what_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        self.what_entry = ttk.Combobox(values=["гол", "пенальти", "удар по воротам"])
        self.what_entry.grid(row=0, column=1, padx=10, pady=5, sticky="we")

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
        self.document_textbox.delete(1.0, "end")  # Очищаем Text перед выводом новых данных

        print(list(collection.aggregate(query)))
        # self.document_textbox.insert("end", collection.aggregate([{}]))

    def get_results(self):
        what = self.what_entry.get()
        comp_symb = self.comp_entry.get()
        value = self.value_entry.get()

        if what == "" or comp_symb == "" or value == "":
            self.document_textbox.insert("end", "Не все поля заполнены!")
            return

        if what == "гол":
            key = "goals"
        elif what == "пенальти":
            key = "penalties"
        else:
            key = "shots_on_goal"

        # формируем запрос
        if comp_symb == '>':
            comp_symb = '$gt'
        elif comp_symb == '>=':
            comp_symb = '$gte'
        elif comp_symb == '=':
            comp_symb = '$eq'
        elif comp_symb == '<=':
            comp_symb = '$lte'
        elif comp_symb == '<':
            comp_symb = '$lt'
        else:
            # Обработка некорректного сравнения
            print("Некорректное сравнение")

        query = [
            {
                '$unwind': f"${key}"
            },
            {
                '$group': {
                    '_id': f'${key}.author',
                    f'{key}_count': {'$sum': 1}
                }
            },
            {
                '$match': {
                    f'{key}_count': {comp_symb: int(value)}
                }
            },
            {
                '$count': 'total_players'
            }
        ]

        self.show_documents(query)
        # print(str(query))

root = Tk()
root.geometry("400x400")
frame = Frame(root)

root.mainloop()
