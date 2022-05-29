from DataBase import DataBase


class Facade:
    def __init__(self, name='products.db'):
        self.DB = DataBase(name)

    def insert(self, product, quanity):
        self.DB.insert(product, quanity)

    def read(self):
        readed = self.DB.read()
        return readed

    def update(self, id, product, quanity):
        self.DB.update(id, product, quanity)

    def delete(self, id):
        self.DB.delete(id)
