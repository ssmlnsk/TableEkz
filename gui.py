from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidget, QTableWidgetItem, QMessageBox
import sys
from facade import Facade


class MainWindow(QMainWindow):
    def __init__(self, facade):
        super(MainWindow, self).__init__()
        self.ui = uic.loadUi("forms/products.ui", self)
        self.facade = facade
        self.window().setWindowTitle("Список продуктов")
        self.ui.btn_add.clicked.connect(self.add_product)
        self.ui.btn_save.clicked.connect(self.save_products_in_db)
        self.ui.btn_delete.clicked.connect(self.delete_product)
        self.table = self.ui.table_products
        self.cout_product()

    def save_products_in_db(self):  # сохраняем измененные ячейки в БД при нажатии на кнопку
        data = self.get_from_table()
        for string in data:
            if string[1] != '':  # если названия магазина есть, то обновляем данные
                self.facade.update(string[0], string[1], string[2])
            else:  # если названия магазина нет, то удаляем эту строку
                self.facade.delete(string[0])
        self.cout_product()

    def add_product(self):
        self.ui = InsertWidget(self.facade, self)
        self.ui.show()

    def cout_product(self):
        self.table.clear()
        rec = self.facade.read()
        self.table.setColumnCount(3)  # кол-во столбцов
        self.table.setRowCount(len(rec))  # кол-во строк
        self.table.setHorizontalHeaderLabels(['ID', 'Product', 'Quantity'])  # название колонок таблицы

        for i, product in enumerate(rec):
            for x, field in enumerate(product):  # i, x - координаты ячейки, в которую будем записывать текст
                item = QTableWidgetItem()
                item.setText(str(field))  # записываем текст в ячейку
                if x == 0:  # для id делаем некликабельные ячейки
                    item.setFlags(Qt.ItemIsEnabled)
                self.table.setItem(i, x, item)

    def get_from_table(self):  # получаем данные из таблицы, чтобы потом записать их в БД
        rows = self.table.rowCount()  # получаем кол-во строк таблицы
        cols = self.table.columnCount()  # получаем кол-во столбцов таблицы
        data = []
        for row in range(rows):
            tmp = []
            for col in range(cols):
                tmp.append(self.table.item(row, col).text())
            data.append(tmp)
        return data

    def delete_product(self):
        SelectedRow = self.table.currentRow()
        rowcount = self.table.rowCount()
        colcount = self.table.columnCount()

        if rowcount == 0:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setText("В таблице нет данных!")
            msg.setWindowTitle("Ошибка")
            msg.setStandardButtons(QMessageBox.Ok)
            retval = msg.exec_()

        elif SelectedRow == -1:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Выберите поле для удаления!")
            msg.setWindowTitle("Ошибка")
            msg.setStandardButtons(QMessageBox.Ok)
            retval = msg.exec_()

        else:
            for col in range(1, colcount):
                self.table.setItem(SelectedRow, col, QTableWidgetItem(''))
            ix = self.table.model().index(-1, -1)
            self.table.setCurrentIndex(ix)


class InsertWidget(QtWidgets.QWidget):
    def __init__(self, facade, link=None):
        self.facade = facade
        self.link = link
        super(InsertWidget, self).__init__()
        self.ui = uic.loadUi('forms/insert.ui', self)
        self.add_btn.clicked.connect(self.add)

    def add(self):
        product = self.ui.product.text()
        quanity = self.ui.quanity.text()
        if product != '' and quanity != '':
            self.facade.insert(product, quanity)
            self.link.cout_product()


class Builder:
    def __init__(self):
        self.facade = None
        self.gui = None

    def create_facade(self):
        self.facade = Facade()

    def create_gui(self):
        if self.facade is not None:
            self.gui = MainWindow(self.facade)

    def get_result(self):
        if self.facade is not None and self.gui is not None:
            return self.gui


if __name__ == '__main__':
    qapp = QtWidgets.QApplication(sys.argv)
    builder = Builder()
    builder.create_facade()
    builder.create_gui()
    window = builder.get_result()
    window.show()
    qapp.exec()
