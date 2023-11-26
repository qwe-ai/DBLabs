from pymongo import MongoClient
from tkinter import ttk
from tkinter import Tk, Label, Entry, Button, Text
import json

# Подключение к базе данных
client = MongoClient("mongodb://192.168.112.103/")
db = client["22305"]
collection = db["sokolova-store"]


class Frame:
    def __init__(self, root):
        self.root = root
        self.root.title("Поиск")
        for i in range(2): root.grid_columnconfigure(index=i, weight=1)
        for j in range(5): root.grid_columnconfigure(index=j, weight=1)

        self.category_label = Label(root, text="Категория:")
        self.category_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        self.category_entry = ttk.Combobox(values=collection.distinct("category"))
        self.category_entry.grid(row=0, column=1, padx=10, pady=5, sticky="we")

        self.buyer_label = Label(root, text="Покупатель:")
        self.buyer_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)

        self.buyer_entry = ttk.Combobox(values=collection.distinct("buyers.name"))
        self.buyer_entry.grid(row=1, column=1, padx=10, pady=5, sticky="we")

        self.color_label = Label(root, text="Цвет:")
        self.color_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)

        self.color_entry = ttk.Combobox(values=collection.distinct("features.Цвет"))
        self.color_entry.grid(row=2, column=1, padx=10, pady=5, sticky="we")

        self.item_label = Label(root, text="Заданный товар:")
        self.item_label.grid(row=3, column=0, sticky="w", padx=10, pady=5)

        self.item_entry = ttk.Combobox(values=collection.distinct("name"))
        self.item_entry.grid(row=3, column=1, padx=10, pady=5, sticky="we")

        self.delivery_label = Label(root, text="Заданная доставка:")
        self.delivery_label.grid(row=4, column=0, sticky="w", padx=10, pady=5)

        self.delivery_entry = ttk.Combobox(values=collection.distinct("buyers.delivery_service"))
        self.delivery_entry.grid(row=4, column=1, padx=10, pady=5, sticky="we")

        self.result_button = Button(root, text="Показать результаты", command=self.get_results)
        self.result_button.grid(row=5, column=0, columnspan=2, padx=10, pady=5, sticky="we")

        self.document_textbox = Text(root)
        self.document_textbox.grid(row=7, column=0, columnspan=2, padx=10, pady=5, sticky="we")

        self.current_doc_data = dict()


    # def show_documents(self, query):
    #     self.document_textbox.delete(1.0, "end")  # Очищаем Text перед выводом новых данных
    #
    #     for document in collection.find(query):
    #         self.document_textbox.insert("end",
    #                                      json.dumps({x: document[x] for x in document if x not in "_id"}, indent=4,
    #                                                 ensure_ascii=False) + '\n_______________________________________\n\n')
    #
    def get_results(self):
        self.document_textbox.delete(1.0, "end")  # Очищаем Text перед выводом новых данных
        # получаем значения из полей ввода
        category = self.category_entry.get()
        buyer = self.buyer_entry.get()
        color = self.color_entry.get()
        item = self.item_entry.get()
        delivery = self.delivery_entry.get()

        if category == "" or buyer == "" or color == "" or item == "" or delivery == "":
            print("Не все поля заполнены!")
            return

        # список названий товаров, относящихся к заданной категории
        query1 = list(collection.find({"category": category}, {"name": 1}))

        # список характеристик товаров заданной категории
        query2 = list(collection.find({"category": category}, {"features": 1}))

        # список названий и стоимости товаров, купленных заданным покупателем
        query3 = list(collection.find({"buyers.name": buyer}, {"name": 1, "price": 1}))

        # список названий, производителей и цен на товары, имеющие заданный цвет
        query4 = list(collection.find({"features.Цвет": color}, {"name": 1, "brand": 1, "price": 1}))

        # общая сумма проданных товаров в каждой категории
        query5 = list(collection.aggregate([
            {"$group": {"_id": "null", "total_sales": {"$sum": "$price"}}}
        ]))

        # количество товаров в каждой категории
        query6 = list(collection.aggregate([
            {"$group": {"_id": "$category", "count": {"$sum": 1}}}
        ]))

        # список имен покупателей заданного товара
        query7 = list(collection.distinct("buyers.name", {"name": item}))

        # список имен покупателей заданного товара, с доставкой фирмы с заданным названием
        query8 = list(collection.find({"name": item, "buyers.delivery_service": delivery}, {"buyers.name": 1}))

        print("query1: "+str(query1))
        print("query2: "+str(query2))
        print("query3: "+str(query3))
        print("query4: "+str(query4))
        print("query5: "+str(query5))
        print("query6: "+str(query6))
        print("query7: "+str(query7))
        print("query8: "+str(query8))

root = Tk()
root.geometry("400x400")
frame = Frame(root)

root.mainloop()
