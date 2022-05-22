from DataBase import DataBase
from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidget, QTableWidgetItem, QMessageBox
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = DataBase()
        self.ui = uic.loadUi("forms/shop.ui", self)
        self.window().setWindowTitle("Магазин")
        self.ui.btn_add_name.clicked.connect(self.add_shop)
        self.ui.btn_save_data.clicked.connect(self.save_shop_in_db)
        self.ui.btn_delete.clicked.connect(self.On_Delete_Click)
        self.table = self.ui.table_shop
        self.cout_shop()

    def save_shop_in_db(self):  # сохраняем измененные ячейки в БД при нажатии на кнопку
        data = self.get_from_table()
        for string in data:
            if string[1] != '':  # если названия магазина есть, то обновляем данные
                self.db.update(string[0], string[1], string[2])
            else:  # если названия магазина нет, то удаляем эту строку
                self.db.delete(string[0])
        self.cout_shop()

    def add_shop(self):  # добавляем новый магазин в БД и в таблицу
        name = self.ui.name.text()
        address = self.ui.address.text()
        if name != '' and address != '':
            self.db.insert(name, address)
            self.cout_shop()

    def cout_shop(self):
        self.table.clear()
        rec = self.db.read()
        self.table.setColumnCount(3)  # кол-во столбцов
        self.table.setRowCount(len(rec))  # кол-во строк
        self.table.setHorizontalHeaderLabels(['ID', 'Product', 'Quantity'])  # название колонок таблицы

        for i, shop in enumerate(rec):
            for x, field in enumerate(shop):  # i, x - координаты ячейки, в которую будем записывать текст
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

    @pyqtSlot()
    def On_Delete_Click(self):
        SelectedRow = self.table.currentRow()
        rowcount = self.table.rowCount()

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
            self.table.removeRow(SelectedRow)
            ix = self.table.model().index(SelectedRow, self.table.currentColumn())
            self.table.setCurrentIndex(ix)


if __name__ == '__main__':
    qapp = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    qapp.exec()
